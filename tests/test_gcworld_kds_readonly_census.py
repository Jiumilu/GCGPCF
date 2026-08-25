from __future__ import annotations

import hashlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "tools/kds-sync/run_gcworld_kds_readonly_census.py"
MODULE_SPEC = importlib.util.spec_from_file_location("gcworld_kds_readonly_census", READER)
assert MODULE_SPEC and MODULE_SPEC.loader
READER_MODULE = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(READER_MODULE)


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    }


class GCWorldKDSReadonlyCensusTest(unittest.TestCase):
    def make_authorization(self, root: Path, may_execute: bool = True) -> dict:
        return {
            "authorization_id": "GCWORLD-KDS-READONLY-TEST",
            "status": "approved_for_local_readonly_census",
            "repository_scope": {
                "local_root": str(root),
                "execution_mode": "本地文件系统只读",
                "kds_api_allowed": False,
                "external_network_allowed": False,
                "write_allowed": False,
            },
            "registered_knowledge_spaces": {
                "spaces": [
                    {"id": "PUBLIC", "source_pattern": "公开/**"},
                    {"id": "PRIVATE", "source_pattern": "私密/**"},
                ]
            },
            "registered_access_spaces": {"spaces": []},
            "additional_fact_source_roots": [],
            "classification_boundary": {
                "unclassified_document_default": "S1",
                "classification_overrides": [
                    {"source_pattern": "公开/**", "classification": "S1"},
                    {"source_pattern": "私密/**", "classification": "S3"}
                ],
            },
            "s3_handling": {
                "content_read_allowed": False,
                "extraction_allowed": False,
                "preview_allowed": False,
                "embedding_allowed": False,
                "agent_memory_allowed": False,
            },
            "technical_exclusions": {
                "content_read_forbidden_patterns": [".git/**", "**/*.db"]
            },
            "execution_gates": {
                "current_admission": "admitted_clean_snapshot",
                "may_execute_content_census_now": may_execute,
                "dirty_snapshot_override_allowed": False,
            },
        }

    def test_deterministic_inventory_masks_s3_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "kds"
            (source_root / "公开").mkdir(parents=True)
            (source_root / "私密").mkdir(parents=True)
            (source_root / "公开/组织.md").write_text("GlobalCloud组织资料", encoding="utf-8")
            (source_root / "私密/人员.md").write_text("S3人员资料不得输出", encoding="utf-8")
            (source_root / "未登记.md").write_text("未知分级不得读取", encoding="utf-8")
            authorization = self.make_authorization(source_root)
            before = tree_snapshot(source_root)

            payloads = [
                READER_MODULE.build_inventory(authorization, source_root, "fixture-snapshot")
                for _ in range(5)
            ]
            first_payload = payloads[0]

            self.assertTrue(all(item["inventorySha256"] == first_payload["inventorySha256"] for item in payloads))
            self.assertTrue(all(item["records"] == first_payload["records"] for item in payloads))
            self.assertEqual(first_payload["summary"]["sourceFiles"], 3)
            public_record = next(item for item in first_payload["records"] if item["classification"] == "S1")
            private_record = next(item for item in first_payload["records"] if item["classification"] == "S3")
            unknown_record = next(
                item
                for item in first_payload["records"]
                if item.get("sourcePath") == "未登记.md"
            )
            self.assertEqual(public_record["disposition"], "content_readonly_included")
            self.assertIsNotNone(public_record["sourceSha256"])
            self.assertEqual(
                set(private_record),
                {
                    "opaque_source_id",
                    "registered_space_id",
                    "media_type",
                    "byte_size",
                    "modified_time",
                    "classification",
                    "review_status",
                },
            )
            self.assertEqual(private_record["review_status"], "human_review_required")
            self.assertEqual(unknown_record["disposition"], "unclassified_exception")
            self.assertEqual(unknown_record["classification"], "S1")
            self.assertIsNone(unknown_record["sourceSha256"])
            self.assertFalse(unknown_record["contentRead"])
            self.assertEqual(tree_snapshot(source_root), before)

    def test_secret_and_symlink_sources_are_never_followed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            source_root = base / "kds"
            outside = base / "outside"
            (source_root / "公开").mkdir(parents=True)
            outside.mkdir()
            (outside / "外部.md").write_text("不得越界读取", encoding="utf-8")
            (source_root / "根级秘密.db").write_text("不得读取", encoding="utf-8")
            (source_root / "公开/外部链接.md").symlink_to(outside / "外部.md")
            (source_root / "公开/外部目录").symlink_to(outside, target_is_directory=True)
            authorization = self.make_authorization(source_root)

            payload = READER_MODULE.build_inventory(authorization, source_root, "fixture-snapshot")

            excluded = [item for item in payload["records"] if item.get("disposition") == "technical_exclusion"]
            self.assertEqual(len(excluded), 3)
            self.assertTrue(all(item["sourcePath"] is None for item in excluded))
            self.assertTrue(all(item["sourceSha256"] is None for item in excluded))
            self.assertNotIn("不得越界读取", str(payload))

    def test_conflicting_classification_uses_strictest_level(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "kds"
            (source_root / "公开").mkdir(parents=True)
            (source_root / "公开/冲突.md").write_text("不得按S1读取", encoding="utf-8")
            authorization = self.make_authorization(source_root)
            authorization["classification_boundary"]["classification_overrides"].append(
                {"source_pattern": "公开/**", "classification": "S3"}
            )

            payload = READER_MODULE.build_inventory(authorization, source_root, "fixture-snapshot")

            self.assertEqual(payload["records"][0]["classification"], "S3")
            self.assertEqual(set(payload["records"][0]), {
                "opaque_source_id",
                "registered_space_id",
                "media_type",
                "byte_size",
                "modified_time",
                "classification",
                "review_status",
            })

    def test_production_cli_rejects_authorization_override(self) -> None:
        result = subprocess.run(
            [sys.executable, str(READER), "--authorization", "/tmp/伪造授权.yaml"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unrecognized arguments", result.stderr)

    def test_dirty_git_worktree_is_rejected_before_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "kds"
            (source_root / "公开").mkdir(parents=True)
            source = source_root / "公开/组织.md"
            source.write_text("初始内容", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=source_root, check=True)
            subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=source_root, check=True)
            subprocess.run(["git", "config", "user.name", "GCWORLD测试"], cwd=source_root, check=True)
            subprocess.run(["git", "add", "公开/组织.md"], cwd=source_root, check=True)
            subprocess.run(["git", "commit", "-qm", "基线"], cwd=source_root, check=True)
            source.write_text("未处置变更", encoding="utf-8")
            self.make_authorization(source_root)
            stderr = io.StringIO()

            with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
                READER_MODULE.git_snapshot(source_root)

            self.assertEqual(raised.exception.code, 2)
            self.assertIn("gcworld_kds_readonly_census=blocked", stderr.getvalue())
            self.assertIn("reason=dirty_worktree", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
