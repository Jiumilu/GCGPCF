#!/usr/bin/env python3
"""在获批隔离快照上执行GCWORLD全量受控分级与候选提取。"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from io import BytesIO
import json
import mimetypes
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
from typing import Any
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

import yaml


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
AUTHORIZATION_PATH = ARTIFACTS / "gcworld-kds-full-classification-authorization-20260823.yaml"
AUTHORIZATION_SHA256 = "ee6470809e761a702887ecba6d5f0266bc93237dc31728bab7a73c31d7886f5d"

SOURCE_LEDGER = ARTIFACTS / "gcworld-kds-source-classification-ledger-20260823.jsonl"
CANDIDATE_LEDGER = ARTIFACTS / "gcworld-kds-asset-candidate-ledger-20260823.jsonl"
RELATION_LEDGER = ARTIFACTS / "gcworld-kds-relation-evidence-ledger-20260823.jsonl"
EXCEPTION_LEDGER = ARTIFACTS / "gcworld-kds-classification-exception-queue-20260823.jsonl"
MACHINE_SUMMARY = ARTIFACTS / "gcworld-kds-controlled-classification-summary-20260823.json"

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".csv", ".tsv",
    ".py", ".sh", ".js", ".ts", ".css", ".html", ".xml", ".srt", ".sql",
    ".log", ".patch", ".template", ".exit", ".sha256", ".pid", ".tag", ".bak",
}
OOXML_EXTENSIONS = {".docx", ".pptx", ".xlsx"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"}
DERIVED_EXTENSIONS = {".lance", ".txn", ".manifest", ".pyc", ".tmp"}
ARCHIVE_EXTENSIONS = {".zip", ".gz", ".bz2", ".xz", ".7z", ".rar", ".tar"}
MAX_ZIP_MEMBERS = 10000
MAX_ZIP_UNCOMPRESSED_BYTES = 256 * 1024 * 1024
MAX_CANDIDATES_PER_SOURCE = 1000

S3_PATH_MARKERS = (
    "private/", "personal/", "family/", "contacts/", "私密", "私人", "个人/", "家庭/",
    "联系人", ".env", "credential", "secret", "private-key", "auth-key", "token",
)
S2_PATH_MARKERS = (
    "team/", "partner/", "ops/", "合同", "财务", "资金", "客户", "合作伙伴", "政府",
    "会议", "纪要", "工业绿链", "pva价值联盟",
)
S0_PATH_MARKERS = ("public/", "公开/")

TECHNICAL_PATH_PATTERNS = (
    ".llm-wiki/lancedb/", "node_modules/", "__pycache__/", ".pytest_cache/", ".ruff_cache/",
    ".obsidian/", ".git/", "/.git/",
)

COMMON_FALSE_PEOPLE = {
    "项目负责人", "相关人员", "工作人员", "参会人员", "联系人", "负责人", "管理员",
    "申请人", "审批人", "执行人", "验收人", "发起人", "责任人", "所有人", "任何人",
}


def fail(reason: str, detail: str = "") -> None:
    suffix = f" detail={detail}" if detail else ""
    print(f"gcworld_kds_controlled_classification=blocked reason={reason}{suffix}", file=os.sys.stderr)
    raise SystemExit(2)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def opaque_source_id(relative: str) -> str:
    return "gcw:source:" + digest_text(unicodedata.normalize("NFC", relative))[:24]


def path_sha256(relative: str) -> str:
    return digest_text(unicodedata.normalize("NFC", relative))


def stable_candidate_id(source_id: str, candidate_type: str, display_name: str) -> str:
    return "gcw:candidate:" + digest_text(f"{source_id}|{candidate_type}|{display_name}")[:32]


def stable_relation_id(source_id: str, subject_id: str, predicate: str, object_label: str) -> str:
    return "gcw:relation-candidate:" + digest_text(
        f"{source_id}|{subject_id}|{predicate}|{object_label}"
    )[:32]


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=environment,
    )


def load_authorization() -> dict[str, Any]:
    if not AUTHORIZATION_PATH.is_file():
        fail("授权文件缺失")
    if sha256(AUTHORIZATION_PATH.read_bytes()).hexdigest() != AUTHORIZATION_SHA256:
        fail("授权文件摘要不匹配")
    payload = yaml.safe_load(AUTHORIZATION_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("status") != "已批准一次性全量受控分级扫描":
        fail("授权状态无效")
    boundary = payload.get("status_boundary") or {}
    if any(boundary.get(key) is not False for key in (
        "kds_write_authorized", "mmc_write_authorized", "business_system_write_authorized",
        "deployment_authorized", "acceptance_authorized",
    )):
        fail("授权越过只读边界")
    return payload


def verify_authorized_snapshot(payload: dict[str, Any]) -> tuple[Path, str]:
    scope = payload.get("snapshot_scope") or {}
    source_root = Path(str(scope.get("isolated_snapshot", ""))).resolve()
    if not source_root.is_dir():
        fail("隔离快照不存在")
    head = run_git(source_root, "rev-parse", "HEAD")
    if head.returncode != 0 or head.stdout.decode().strip() != scope.get("head"):
        fail("隔离快照提交不匹配")
    status_result = run_git(source_root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if status_result.returncode != 0:
        fail("隔离快照状态不可读取")
    status_hash = sha256(status_result.stdout).hexdigest()
    entries = len([item for item in status_result.stdout.split(b"\0") if item])
    if status_hash != scope.get("worktree_status_sha256") or entries != scope.get("worktree_entries"):
        fail("隔离快照工作树不匹配", f"entries={entries}")
    snapshot_id = f"{scope['head']}:{status_hash}"
    return source_root, snapshot_id


def metadata_snapshot(root: Path) -> dict[str, tuple[int, int, int, int, int, bool]]:
    records: dict[str, tuple[int, int, int, int, int, bool]] = {}
    normalized_paths: set[str] = set()
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for directory in sorted(directories):
            path = current_path / directory
            if directory == ".git":
                continue
            if path.is_symlink():
                relative = path.relative_to(root).as_posix()
                normalized = unicodedata.normalize("NFC", relative)
                if normalized in normalized_paths:
                    fail("规范化路径冲突")
                normalized_paths.add(normalized)
                file_stat = path.lstat()
                records[relative] = (
                    file_stat.st_size, file_stat.st_mtime_ns, file_stat.st_mode,
                    file_stat.st_dev, file_stat.st_ino, True,
                )
            else:
                retained.append(directory)
        directories[:] = retained
        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(root).as_posix()
            normalized = unicodedata.normalize("NFC", relative)
            if normalized in normalized_paths:
                fail("规范化路径冲突")
            normalized_paths.add(normalized)
            file_stat = path.lstat()
            records[relative] = (
                file_stat.st_size, file_stat.st_mtime_ns, file_stat.st_mode,
                file_stat.st_dev, file_stat.st_ino, path.is_symlink(),
            )
    return records


def secure_read(path: Path, expected: tuple[int, int, int, int, int, bool]) -> bytes:
    size, modified_ns, mode, device, inode, is_symlink = expected
    if is_symlink or not stat.S_ISREG(mode):
        fail("不安全的来源类型")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        identity = (before.st_size, before.st_mtime_ns, before.st_mode, before.st_dev, before.st_ino)
        if identity != (size, modified_ns, mode, device, inode):
            fail("读取前来源发生变化")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (after.st_size, after.st_mtime_ns, after.st_mode, after.st_dev, after.st_ino) != identity:
            fail("读取过程中来源发生变化")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def decode_text(raw: bytes) -> tuple[str, str]:
    if b"\x00" in raw[:8192]:
        return "", "二进制内容无法作为文本解析"
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "big5"):
        try:
            return raw.decode(encoding), "已解析"
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "替换非法字符后解析"


def extract_ooxml_text(raw: bytes, suffix: str) -> tuple[str, str]:
    try:
        with zipfile.ZipFile(BytesIO(raw)) as archive:
            members = archive.infolist()
            if len(members) > MAX_ZIP_MEMBERS:
                return "", "压缩包成员过多"
            if sum(item.file_size for item in members) > MAX_ZIP_UNCOMPRESSED_BYTES:
                return "", "解压后内容过大"
            names = []
            for item in members:
                name = item.filename
                if suffix == ".docx" and name.startswith("word/") and name.endswith(".xml"):
                    names.append(name)
                elif suffix == ".pptx" and name.startswith("ppt/slides/") and name.endswith(".xml"):
                    names.append(name)
                elif suffix == ".xlsx" and (
                    name == "xl/sharedStrings.xml" or name.startswith("xl/worksheets/") and name.endswith(".xml")
                ):
                    names.append(name)
            text_parts: list[str] = []
            for name in sorted(names):
                try:
                    root = ET.fromstring(archive.read(name))
                except (ET.ParseError, KeyError, RuntimeError):
                    continue
                text_parts.extend(part.strip() for part in root.itertext() if part.strip())
            if not text_parts:
                return "", "OOXML未提取到文本"
            return "\n".join(text_parts), "已解析"
    except (zipfile.BadZipFile, OSError, RuntimeError):
        return "", "OOXML文件损坏或不可读取"


def extract_pdf_text(raw: bytes) -> tuple[str, str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return "", "PDF解析依赖不可用"
    try:
        reader = PdfReader(BytesIO(raw), strict=False)
        if reader.is_encrypted and reader.decrypt("") == 0:
            return "", "PDF已加密"
        parts = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(part for part in parts if part)
        return (text, "已解析") if text else ("", "PDF未提取到文本")
    except Exception:
        return "", "PDF损坏或不可解析"


def extract_supported_text(path: Path, raw: bytes | None = None) -> tuple[str, str]:
    suffix = path.suffix.lower()
    content = path.read_bytes() if raw is None else raw
    if content.startswith(b"version https://git-lfs.github.com/spec/v1"):
        return "", "Git LFS指针，实体内容未在快照工作树中展开"
    if suffix in TEXT_EXTENSIONS or not suffix:
        return decode_text(content)
    if suffix in OOXML_EXTENSIONS:
        return extract_ooxml_text(content, suffix)
    if suffix == ".pdf":
        if not content.startswith(b"%PDF-"):
            return "", "扩展名与PDF文件头不一致"
        return extract_pdf_text(content)
    if suffix in IMAGE_EXTENSIONS:
        return "", "图像未执行OCR"
    if suffix in ARCHIVE_EXTENSIONS:
        return "", "归档文件未展开"
    return "", "不支持的媒体类型"


def is_technical_exclusion(relative: str, suffix: str, is_symlink: bool) -> bool:
    lowered = relative.lower()
    return (
        is_symlink
        or suffix in DERIVED_EXTENSIONS
        or any(marker in lowered for marker in TECHNICAL_PATH_PATTERNS)
        or lowered.endswith((".db", ".sqlite", ".sqlite3"))
    )


def classification_decision(relative: str, text: str, parse_status: str = "已解析") -> dict[str, Any]:
    lowered_path = unicodedata.normalize("NFC", relative).lower()
    levels: list[tuple[int, str]] = []
    for match in re.findall(
        r"(?:access_level|visibility(?:_level)?|sensitivity|密级|敏感等级|level)\s*[:=]\s*[\"']?([SL][0-3])",
        text,
        flags=re.IGNORECASE,
    ):
        normalized = "S" + match[-1]
        levels.append((int(normalized[-1]), f"内容显式标级{normalized}"))
    if any(marker in lowered_path for marker in S0_PATH_MARKERS):
        levels.append((0, "路径声明为公开空间"))
    if any(marker in lowered_path for marker in S2_PATH_MARKERS):
        levels.append((2, "路径属于受限业务空间"))
    if any(marker in lowered_path for marker in S3_PATH_MARKERS):
        levels.append((3, "路径属于机密或个人空间"))

    s3_patterns = (
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)(?:password|passwd|token|secret|api[_-]?key|access[_-]?key)\s*[:=]\s*[\"']?[^\s\"']{8,}",
        r"(?:密码|口令|令牌|私钥|访问密钥)\s*[:：=]\s*\S{4,}",
        r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx](?!\d)",
        r"(?:银行卡|银行账号|收款账号)\s*[:：]?\s*\d{12,19}",
    )
    if any(re.search(pattern, text) for pattern in s3_patterns):
        levels.append((3, "内容检测到秘密或强个人识别信息"))

    s2_patterns = (
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
        r"(?<!\d)1[3-9]\d{9}(?!\d)",
        r"(?:合同|报价|财务|融资|客户|合作伙伴|政府|会议纪要|商业秘密)",
    )
    if any(re.search(pattern, text) for pattern in s2_patterns):
        levels.append((2, "内容包含受限业务或联系方式信息"))

    if parse_status not in {"已解析", "替换非法字符后解析"}:
        levels.append((3, "内容无法可靠解析，按最严格等级处置"))
    if not levels:
        levels.append((1, "未显式标级，按KDS默认内部等级处置"))
    maximum = max(level for level, _ in levels)
    reasons = sorted({reason for level, reason in levels if level == maximum})
    return {"classification": f"S{maximum}", "classificationReasonCodes": reasons}


def safe_source_record(
    *,
    relative: str,
    source_sha256: str,
    byte_size: int,
    modified_time_ns: int,
    media_type: str,
    decision: dict[str, Any],
    parse_status: str,
    technical_exclusion: bool = False,
) -> dict[str, Any]:
    source_id = opaque_source_id(relative)
    record: dict[str, Any] = {
        "opaqueSourceId": source_id,
        "pathSha256": path_sha256(relative),
        "sourceSha256": source_sha256,
        "mediaType": media_type,
        "byteSize": byte_size,
        "classification": decision["classification"],
        "classificationReasonCodes": decision["classificationReasonCodes"],
        "reviewStatus": "需要人工复核" if decision["classification"] == "S3" else "待身份复核",
    }
    if decision["classification"] != "S3":
        record.update({
            "modifiedTimeNs": modified_time_ns,
            "parseStatus": parse_status,
            "disposition": "技术排除" if technical_exclusion else "已分级",
            "sourcePath": relative,
        })
    return record


def normalized_candidate_name(value: str) -> str:
    return re.sub(r"[\s，,。；;：:、（）()\[\]【】]+$", "", value.strip())


def extract_candidates_and_relations(text: str, source_record: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_id = source_record["opaqueSourceId"]
    source_hash = source_record["sourceSha256"]
    candidate_pairs: set[tuple[str, str]] = set()

    organization_pattern = re.compile(
        r"[A-Za-z0-9\u4e00-\u9fff·（）()\-]{2,40}(?:有限责任公司|股份有限公司|有限公司|集团|公司|委员会|政府|研究院|研究所|大学|学院|中心|协会|团队|项目组|部门)"
    )
    for match in organization_pattern.findall(text):
        name = normalized_candidate_name(match)
        if 2 <= len(name) <= 48:
            candidate_pairs.add(("组织", name))

    person_patterns = (
        re.compile(r"(?:负责人|联系人|参会人|参与人|成员|姓名|责任人|申请人|审批人|执行人|验收人)\s*[:：=]\s*([\u4e00-\u9fff·]{2,4})"),
        re.compile(r"([\u4e00-\u9fff·]{2,4})(?:担任|任职|作为|负责)"),
    )
    for pattern in person_patterns:
        for match in pattern.findall(text):
            name = normalized_candidate_name(match)
            if name and name not in COMMON_FALSE_PEOPLE:
                candidate_pairs.add(("人员", name))

    ordered_pairs = sorted(candidate_pairs)[:MAX_CANDIDATES_PER_SOURCE]
    candidates: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    for candidate_type, display_name in ordered_pairs:
        candidate_id = stable_candidate_id(source_id, candidate_type, display_name)
        relation_id = stable_relation_id(source_id, candidate_id, "由来源提及", source_id)
        candidates.append({
            "candidateId": candidate_id,
            "candidateType": candidate_type,
            "displayName": display_name,
            "identityDisposition": "未决候选",
            "worldAssetId": None,
            "sourceEvidenceRef": source_id,
            "sourceSha256": source_hash,
            "relationEvidenceRefs": [relation_id],
        })
        relations.append({
            "relationCandidateId": relation_id,
            "subjectCandidateId": candidate_id,
            "predicate": "由来源提及",
            "objectRef": source_id,
            "evidenceStatus": "未决候选",
            "sourceEvidenceRef": source_id,
            "sourceSha256": source_hash,
        })

    role_patterns = (
        re.compile(r"(?:负责人|联系人|责任人|申请人|审批人|执行人|验收人)\s*[:：=]\s*([\u4e00-\u9fff·]{2,4})"),
        re.compile(r"([\u4e00-\u9fff·]{2,4})(?:担任|任职|作为)([\u4e00-\u9fffA-Za-z0-9·\-]{2,20})"),
    )
    people = {item["displayName"]: item for item in candidates if item["candidateType"] == "人员"}
    for pattern_index, pattern in enumerate(role_patterns):
        for match in pattern.findall(text):
            if isinstance(match, tuple):
                person, role = match
            else:
                person = match
                role = "联系人或责任职能"
            person = normalized_candidate_name(person)
            if person not in people:
                continue
            candidate_id = people[person]["candidateId"]
            relation_id = stable_relation_id(source_id, candidate_id, "承担候选职能", role)
            relations.append({
                "relationCandidateId": relation_id,
                "subjectCandidateId": candidate_id,
                "predicate": "承担候选职能",
                "objectLabel": role,
                "evidenceStatus": "未决候选",
                "sourceEvidenceRef": source_id,
                "sourceSha256": source_hash,
            })
            people[person]["relationEvidenceRefs"].append(relation_id)

    relations = sorted({item["relationCandidateId"]: item for item in relations}.values(), key=lambda item: item["relationCandidateId"])
    for item in candidates:
        item["relationEvidenceRefs"] = sorted(set(item["relationEvidenceRefs"]))
    return candidates, relations


def exception_record(source_record: dict[str, Any], reason: str) -> dict[str, Any]:
    record = {
        "exceptionId": "gcw:exception:" + digest_text(f"{source_record['opaqueSourceId']}|{reason}")[:32],
        "opaqueSourceId": source_record["opaqueSourceId"],
        "pathSha256": source_record["pathSha256"],
        "classification": source_record["classification"],
        "exceptionReasonCode": reason,
        "reviewStatus": "需要人工复核",
    }
    if source_record["classification"] != "S3" and "sourcePath" in source_record:
        record["sourcePath"] = source_record["sourcePath"]
    return record


def build_ledgers(source_root: Path, snapshot_id: str) -> dict[str, Any]:
    before = metadata_snapshot(source_root)
    sources: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []

    for relative in sorted(before):
        size, modified_ns, mode, _, _, is_symlink = before[relative]
        path = source_root / relative
        suffix = path.suffix.lower()
        media_type = mimetypes.guess_type(relative)[0] or "application/octet-stream"
        technical = is_technical_exclusion(relative, suffix, is_symlink)
        if is_symlink:
            target_text = os.readlink(path)
            raw = target_text.encode("utf-8", errors="surrogateescape")
            parse_status = "符号链接未跟随"
            text = ""
        else:
            raw = secure_read(path, before[relative])
            if technical:
                parse_status = "技术来源不执行内容提取"
                text = ""
            else:
                text, parse_status = extract_supported_text(path, raw)
        source_hash = sha256(raw).hexdigest()
        decision = classification_decision(relative, text, parse_status)
        if technical:
            decision = {
                "classification": "S3",
                "classificationReasonCodes": ["技术来源或秘密文件按最严格等级隔离"],
            }
        record = safe_source_record(
            relative=relative,
            source_sha256=source_hash,
            byte_size=size,
            modified_time_ns=modified_ns,
            media_type=media_type,
            decision=decision,
            parse_status=parse_status,
            technical_exclusion=technical,
        )
        sources.append(record)
        if record["classification"] == "S3":
            exceptions.append(exception_record(record, "S3仅保留受控索引，不输出正文或候选"))
        elif parse_status not in {"已解析", "替换非法字符后解析"}:
            exceptions.append(exception_record(record, parse_status))
        elif text:
            source_candidates, source_relations = extract_candidates_and_relations(text, record)
            candidates.extend(source_candidates)
            relations.extend(source_relations)

    after = metadata_snapshot(source_root)
    if after != before:
        fail("扫描期间快照发生变化")

    sources.sort(key=lambda item: item["opaqueSourceId"])
    candidates.sort(key=lambda item: item["candidateId"])
    relations.sort(key=lambda item: item["relationCandidateId"])
    exceptions.sort(key=lambda item: item["exceptionId"])
    classification_counts = Counter(item["classification"] for item in sources)
    summary = {
        "sourceFiles": len(sources),
        "classificationCounts": dict(sorted(classification_counts.items())),
        "technicalExclusions": sum(
            "技术来源或秘密文件按最严格等级隔离" in item["classificationReasonCodes"]
            for item in sources
        ),
        "personCandidates": sum(item["candidateType"] == "人员" for item in candidates),
        "organizationCandidates": sum(item["candidateType"] == "组织" for item in candidates),
        "relationCandidates": len(relations),
        "exceptions": len(exceptions),
        "sourceFilesModified": 0,
        "kdsWrites": 0,
        "mmcWrites": 0,
        "businessSystemWrites": 0,
    }
    canonical = {
        "snapshotId": snapshot_id,
        "summary": summary,
        "sources": sources,
        "candidates": candidates,
        "relations": relations,
        "exceptions": exceptions,
    }
    return {
        **canonical,
        "contractVersion": "gcworld-kds-controlled-classification/v1",
        "authorizationId": "GCWORLD-KDS-FULL-CLASSIFICATION-20260823-001",
        "ledgerSha256": sha256(canonical_json(canonical).encode("utf-8")).hexdigest(),
    }


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def jsonl_content(records: list[dict[str, Any]]) -> str:
    return "".join(canonical_json(item) + "\n" for item in records)


def write_outputs(payload: dict[str, Any]) -> dict[str, Any]:
    atomic_write_text(SOURCE_LEDGER, jsonl_content(payload["sources"]))
    atomic_write_text(CANDIDATE_LEDGER, jsonl_content(payload["candidates"]))
    atomic_write_text(RELATION_LEDGER, jsonl_content(payload["relations"]))
    atomic_write_text(EXCEPTION_LEDGER, jsonl_content(payload["exceptions"]))
    output_hashes = {
        path.name: sha256(path.read_bytes()).hexdigest()
        for path in (SOURCE_LEDGER, CANDIDATE_LEDGER, RELATION_LEDGER, EXCEPTION_LEDGER)
    }
    summary = {
        "contractVersion": payload["contractVersion"],
        "authorizationId": payload["authorizationId"],
        "authorizationSha256": AUTHORIZATION_SHA256,
        "snapshotId": payload["snapshotId"],
        "summary": payload["summary"],
        "ledgerSha256": payload["ledgerSha256"],
        "outputSha256": output_hashes,
        "status": "部分完成，全部来源已处置，候选仍待人工复核",
    }
    atomic_write_text(MACHINE_SUMMARY, canonical_json(summary) + "\n")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-authorized-scan", action="store_true", required=True)
    args = parser.parse_args()
    if not args.execute_authorized_scan:
        fail("未提供执行确认")
    authorization = load_authorization()
    source_root, snapshot_id = verify_authorized_snapshot(authorization)
    payload = build_ledgers(source_root, snapshot_id)
    summary = write_outputs(payload)
    print(
        "gcworld_kds_controlled_classification=pass "
        f"snapshot={snapshot_id} "
        f"source_files={summary['summary']['sourceFiles']} "
        f"person_candidates={summary['summary']['personCandidates']} "
        f"organization_candidates={summary['summary']['organizationCandidates']} "
        f"relation_candidates={summary['summary']['relationCandidates']} "
        f"exceptions={summary['summary']['exceptions']} "
        f"ledger_sha256={summary['ledgerSha256']} "
        "source_files_modified=0 kds_writes=0 mmc_writes=0 business_system_writes=0"
    )


if __name__ == "__main__":
    main()
