#!/usr/bin/env python3
"""按已批准授权生成 GCWORLD KDS 确定性只读来源清单。"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Any
import unicodedata

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AUTHORIZATION = (
    ROOT
    / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
    / "gcworld-kds-readonly-source-authorization-v1.yaml"
)
AUTHORIZED_SHA256 = "3869c1a6f015c8a957827170f35cf9d28feccd0f5accf3ed03e1df3fd558aba2"
F013_ADMISSION = ROOT / "tools/kds-sync/validate_f013_kds_apply_admission.py"


def blocked(reason: str, detail: str = "") -> None:
    suffix = f" detail={detail}" if detail else ""
    print(f"gcworld_kds_readonly_census=blocked reason={reason}{suffix}", file=sys.stderr)
    raise SystemExit(2)


def load_authorization(path: Path) -> dict[str, Any]:
    if not path.is_file():
        blocked("authorization_missing")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        blocked("authorization_invalid")
    if path.resolve() == DEFAULT_AUTHORIZATION.resolve():
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != AUTHORIZED_SHA256:
            blocked("authorization_hash_mismatch")
    scope = payload.get("repository_scope", {})
    if payload.get("status") != "approved_for_local_readonly_census":
        blocked("authorization_not_approved")
    if scope.get("write_allowed") is not False or scope.get("kds_api_allowed") is not False:
        blocked("authorization_not_readonly")
    if payload.get("execution_gates", {}).get("dirty_snapshot_override_allowed") is not False:
        blocked("dirty_override_not_forbidden")
    return payload


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )


def git_snapshot(root: Path) -> str:
    probe = run_git(root, "rev-parse", "--is-inside-work-tree")
    if probe.returncode != 0:
        return "not_git"
    status = run_git(root, "status", "--porcelain=v1")
    if status.returncode != 0:
        blocked("git_status_failed")
    changed = [line for line in status.stdout.splitlines() if line]
    if changed:
        blocked("dirty_worktree", str(len(changed)))
    divergence = run_git(root, "rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if divergence.returncode == 0:
        behind, ahead = (int(value) for value in divergence.stdout.split())
        if ahead:
            blocked("unreviewed_ahead_commits", str(ahead))
        if behind:
            blocked("snapshot_behind_upstream", str(behind))
    head = run_git(root, "rev-parse", "HEAD")
    if head.returncode != 0:
        blocked("git_head_unavailable")
    return head.stdout.strip()


def f013_admission() -> str:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    result = subprocess.run(
        [sys.executable, str(F013_ADMISSION)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )
    if result.returncode != 0:
        blocked("f013_admission_check_failed")
    match = re.search(r"\badmission=([^\s]+)", result.stdout)
    if match is None:
        blocked("f013_admission_result_missing")
    admission = match.group(1)
    if admission != "ready_for_authorization":
        blocked("f013_admission", admission)
    return admission


def matches(path: str, pattern: str) -> bool:
    if pattern.startswith("**/") and fnmatch.fnmatchcase(path, pattern[3:]):
        return True
    normalized = pattern.removesuffix("/**")
    return path == normalized or path.startswith(f"{normalized}/") or fnmatch.fnmatchcase(path, pattern)


def source_patterns(authorization: dict[str, Any]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for item in authorization.get("registered_knowledge_spaces", {}).get("spaces", []):
        result.append((str(item["id"]), str(item["source_pattern"])))
    for item in authorization.get("registered_access_spaces", {}).get("spaces", []):
        for pattern in item.get("source_patterns", []):
            result.append((str(item["id"]), str(pattern)))
    for index, pattern in enumerate(authorization.get("additional_fact_source_roots", []), start=1):
        result.append((f"ADDITIONAL_{index:02d}", str(pattern)))
    return result


def classification(path: str, authorization: dict[str, Any]) -> tuple[str, bool]:
    boundary = authorization.get("classification_boundary", {})
    matched: set[str] = set()
    for item in boundary.get("classification_overrides", []):
        if matches(path, str(item["source_pattern"])):
            matched.add(str(item["classification"]))
    if "S3" in matched:
        return "S3", True
    if len(matched) == 1:
        level = matched.pop()
        return (level, True) if level in {"S0", "S1", "S2"} else ("S1", False)
    return str(boundary.get("unclassified_document_default", "S1")), False


def metadata_snapshot(root: Path) -> dict[str, tuple[int, int, int, int, int, bool]]:
    result: dict[str, tuple[int, int, int, int, int, bool]] = {}
    normalized_paths: set[str] = set()
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for directory in sorted(directories):
            path = current_path / directory
            if directory == ".git":
                continue
            if path.is_symlink():
                relative = path.relative_to(root).as_posix()
                normalized = unicodedata.normalize("NFC", relative)
                if normalized in normalized_paths:
                    blocked("normalized_path_collision")
                normalized_paths.add(normalized)
                file_stat = path.lstat()
                result[relative] = (
                    file_stat.st_size,
                    file_stat.st_mtime_ns,
                    file_stat.st_mode,
                    file_stat.st_dev,
                    file_stat.st_ino,
                    True,
                )
            else:
                retained_directories.append(directory)
        directories[:] = retained_directories
        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(root).as_posix()
            normalized = unicodedata.normalize("NFC", relative)
            if normalized in normalized_paths:
                blocked("normalized_path_collision")
            normalized_paths.add(normalized)
            file_stat = path.lstat()
            result[relative] = (
                file_stat.st_size,
                file_stat.st_mtime_ns,
                file_stat.st_mode,
                file_stat.st_dev,
                file_stat.st_ino,
                path.is_symlink(),
            )
    return result


def secure_sha256(path: Path, expected: tuple[int, int, int, int, int, bool]) -> str:
    size, modified_ns, mode, device, inode, is_symlink = expected
    if is_symlink or not stat.S_ISREG(mode):
        blocked("unsafe_source_type")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        identity = (before.st_size, before.st_mtime_ns, before.st_mode, before.st_dev, before.st_ino)
        if identity != (size, modified_ns, mode, device, inode):
            blocked("source_changed_before_read")
        digest = hashlib.sha256()
        while chunk := os.read(descriptor, 1024 * 1024):
            digest.update(chunk)
        after = os.fstat(descriptor)
        if (after.st_size, after.st_mtime_ns, after.st_mode, after.st_dev, after.st_ino) != identity:
            blocked("source_changed_during_read")
        return digest.hexdigest()
    finally:
        os.close(descriptor)


def file_record(
    root: Path,
    relative: str,
    stat_data: tuple[int, int, int, int, int, bool],
    authorization: dict[str, Any],
    patterns: list[tuple[str, str]],
) -> dict[str, Any]:
    size, modified_ns, mode, _, _, is_symlink = stat_data
    exclusions = authorization.get("technical_exclusions", {}).get("content_read_forbidden_patterns", [])
    excluded = is_symlink or not stat.S_ISREG(mode) or any(matches(relative, str(pattern)) for pattern in exclusions)
    space_id = next((space for space, pattern in patterns if matches(relative, pattern)), None)
    level, classification_resolved = classification(relative, authorization)
    opaque_id = "gcw:source:" + hashlib.sha256(relative.encode("utf-8")).hexdigest()[:24]

    disposition = "content_readonly_included"
    content_read = True
    source_hash: str | None = None
    visible_path: str | None = relative
    review_status = "not_required"
    if excluded:
        disposition = "technical_exclusion"
        content_read = False
        visible_path = None
    elif level == "S3":
        disposition = "s3_metadata_only"
        content_read = False
        visible_path = None
        review_status = "human_review_required"
    elif not classification_resolved or space_id is None:
        disposition = "unclassified_exception"
        content_read = False
        review_status = "classification_review_required"
    if content_read:
        source_hash = secure_sha256(root / relative, stat_data)

    media_type = mimetypes.guess_type(relative)[0] or "application/octet-stream"
    if level == "S3":
        return {
            "opaque_source_id": opaque_id,
            "registered_space_id": space_id,
            "media_type": media_type,
            "byte_size": size,
            "modified_time": modified_ns,
            "classification": level,
            "review_status": review_status,
        }
    return {
        "opaqueSourceId": opaque_id,
        "registeredSpaceId": space_id,
        "sourcePath": visible_path,
        "mediaType": media_type,
        "byteSize": size,
        "modifiedTimeNs": modified_ns,
        "classification": level,
        "disposition": disposition,
        "reviewStatus": review_status,
        "contentRead": content_read,
        "sourceSha256": source_hash,
    }


def build_inventory(authorization: dict[str, Any], source_root: Path, snapshot_id: str) -> dict[str, Any]:
    before = metadata_snapshot(source_root)
    patterns = source_patterns(authorization)
    records = [
        file_record(source_root, relative, before[relative], authorization, patterns)
        for relative in sorted(before)
    ]
    after = metadata_snapshot(source_root)
    if after != before:
        blocked("source_changed_during_census")
    summary = {
        "sourceFiles": len(records),
        "contentReadonlyIncluded": sum(item.get("disposition") == "content_readonly_included" for item in records),
        "s3MetadataOnly": sum(item.get("classification") == "S3" for item in records),
        "technicalExclusions": sum(item.get("disposition") == "technical_exclusion" for item in records),
        "unclassifiedExceptions": sum(item.get("disposition") == "unclassified_exception" for item in records),
        "sourceFilesModified": 0,
    }
    canonical = {"snapshotId": snapshot_id, "summary": summary, "records": records}
    digest = hashlib.sha256(
        json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "contractVersion": "gcworld-kds-readonly-census/v1",
        "censusMode": "local_readonly",
        "authorizationId": authorization["authorization_id"],
        "sourceRevision": snapshot_id,
        "snapshotId": snapshot_id,
        "ordering": "unicode_nfc_posix_path_ascending",
        "summary": summary,
        "records": records,
        "inventorySha256": digest,
        "kdsWrites": 0,
        "mmcWrites": 0,
        "businessSystemWrites": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    authorization = load_authorization(DEFAULT_AUTHORIZATION)
    source_root = Path(authorization["repository_scope"]["local_root"]).resolve()
    if not source_root.is_dir():
        blocked("source_root_missing")
    admission = f013_admission()
    snapshot_id = git_snapshot(source_root)
    if authorization.get("execution_gates", {}).get("may_execute_content_census_now") is not True:
        blocked("authorization_gate_closed")
    payload = build_inventory(authorization, source_root, snapshot_id)
    payload["authorizationSha256"] = AUTHORIZED_SHA256
    payload["admission"] = admission
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
