from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "tools/kds-sync/run_gcworld_kds_controlled_classification.py"


def load_scanner():
    spec = importlib.util.spec_from_file_location("gcworld_kds_controlled_classification", SCANNER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


class GCWorldKDSControlledClassificationTest(unittest.TestCase):
    def test_sensitive_decision_is_strictest_and_never_exposes_plaintext(self) -> None:
        scanner = load_scanner()

        decision = scanner.classification_decision(
            "concepts/team/合作方案.md",
            "visibility:\n  level: S1\n联系人：张三 13800138000\n密码：绝不能输出",
        )
        record = scanner.safe_source_record(
            relative="concepts/team/合作方案.md",
            source_sha256="a" * 64,
            byte_size=120,
            modified_time_ns=1,
            media_type="text/markdown",
            decision=decision,
            parse_status="已解析",
        )

        self.assertEqual(decision["classification"], "S3")
        self.assertNotIn("sourcePath", record)
        self.assertEqual(
            set(record),
            {
                "opaqueSourceId",
                "pathSha256",
                "sourceSha256",
                "mediaType",
                "byteSize",
                "classification",
                "classificationReasonCodes",
                "reviewStatus",
            },
        )
        serialized = json.dumps(record, ensure_ascii=False)
        self.assertNotIn("张三", serialized)
        self.assertNotIn("13800138000", serialized)
        self.assertNotIn("绝不能输出", serialized)
        self.assertEqual(record["reviewStatus"], "需要人工复核")

    def test_ooxml_text_extraction_covers_word_powerpoint_and_excel(self) -> None:
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixtures = {
                "资料.docx": ("word/document.xml", "<w:document xmlns:w='w'><w:t>云舟科技有限公司</w:t></w:document>"),
                "汇报.pptx": ("ppt/slides/slide1.xml", "<p:sld xmlns:p='p' xmlns:a='a'><a:t>项目负责人张三</a:t></p:sld>"),
                "清单.xlsx": ("xl/sharedStrings.xml", "<sst xmlns='s'><si><t>合作伙伴李四</t></si></sst>"),
            }
            for name, (member, xml) in fixtures.items():
                with zipfile.ZipFile(root / name, "w") as archive:
                    archive.writestr(member, xml)

            extracted = {name: scanner.extract_supported_text(root / name)[0] for name in fixtures}

            self.assertIn("云舟科技有限公司", extracted["资料.docx"])
            self.assertIn("项目负责人张三", extracted["汇报.pptx"])
            self.assertIn("合作伙伴李四", extracted["清单.xlsx"])

    def test_git_lfs_pointer_is_an_explicit_exception_without_parser_noise(self) -> None:
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "资料.pdf"
            path.write_text(
                "version https://git-lfs.github.com/spec/v1\n"
                "oid sha256:" + "a" * 64 + "\nsize 123\n",
                encoding="utf-8",
            )

            text, status = scanner.extract_supported_text(path)

            self.assertEqual(text, "")
            self.assertEqual(status, "Git LFS指针，实体内容未在快照工作树中展开")

    def test_candidates_remain_unresolved_and_are_not_merged_across_sources(self) -> None:
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "资料").mkdir()
            (root / "资料/甲.md").write_text(
                "组织：云舟科技有限公司\n负责人：张三\n张三担任项目负责人",
                encoding="utf-8",
            )
            (root / "资料/乙.md").write_text(
                "客户：海岳集团有限公司\n联系人：张三",
                encoding="utf-8",
            )

            payload = scanner.build_ledgers(root, "fixture-snapshot")
            people = [item for item in payload["candidates"] if item["candidateType"] == "人员" and item["displayName"] == "张三"]

            self.assertEqual(len(people), 2)
            self.assertEqual(len({item["candidateId"] for item in people}), 2)
            self.assertTrue(all(item["identityDisposition"] == "未决候选" for item in people))
            self.assertTrue(all(item["worldAssetId"] is None for item in people))
            self.assertTrue(any(item["relationEvidenceRefs"] for item in people))
            self.assertGreaterEqual(payload["summary"]["organizationCandidates"], 2)

    def test_inventory_is_deterministic_and_source_tree_is_unchanged(self) -> None:
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "公开").mkdir()
            (root / "公开/组织.md").write_text("组织：GlobalCloud团队", encoding="utf-8")
            (root / "图片.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            before = tree_hashes(root)

            first = scanner.build_ledgers(root, "fixture-snapshot")
            second = scanner.build_ledgers(root, "fixture-snapshot")

            self.assertEqual(first["ledgerSha256"], second["ledgerSha256"])
            self.assertEqual(first["sources"], second["sources"])
            self.assertEqual(first["candidates"], second["candidates"])
            self.assertEqual(first["relations"], second["relations"])
            self.assertEqual(first["exceptions"], second["exceptions"])
            self.assertEqual(tree_hashes(root), before)
            self.assertEqual(first["summary"]["sourceFilesModified"], 0)
            image = next(item for item in first["sources"] if item["mediaType"] == "image/png")
            self.assertEqual(image["classification"], "S3")
            self.assertNotIn("sourcePath", image)

    def test_production_cli_rejects_source_root_override(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCANNER), "--execute-authorized-scan", "--source-root", "/tmp/伪造快照"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unrecognized arguments", result.stderr)


if __name__ == "__main__":
    unittest.main()
