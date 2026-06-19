#!/usr/bin/env python3
"""Evaluate the Loop document governance gate and optionally write a health report."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "09-status/globalcloud-document-health-report.md"
MIRROR_REPORT = ROOT / ".kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-health-report.md"


def run(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def iter_repo_md() -> list[Path]:
    paths = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or ".kds" in path.parts:
            continue
        paths.append(path)
    return sorted(paths)


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def is_okf_bundle_doc(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if not rel.startswith(".okf/bundles/"):
        return False
    if path.name in {"index.md", "log.md"}:
        return True
    fm = read_frontmatter(path)
    return bool(fm.get("type"))


def count_unique_mirror_docs(path: Path) -> int:
    if not path.exists():
        return 0
    unique_paths: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("status") != "mirrored":
            continue
        kds_path = entry.get("kds_path")
        if isinstance(kds_path, str) and kds_path:
            unique_paths.add(kds_path)
    return len(unique_paths)


def write_report(summary: dict[str, object], command_results: dict[str, str]) -> None:
    status_counts = summary["status_counts"]
    project_counts = summary["project_counts"]
    lines = [
        "---",
        "doc_id: GPCF-DOC-C436DDB0F6",
        "title: GlobalCloud 文档健康报告",
        "project: GPCF",
        "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]",
        "domain: status",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/91-治理与验收/09-status/globalcloud-document-health-report.md",
        "source_path: 09-status/globalcloud-document-health-report.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-12",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# GlobalCloud 文档健康报告",
        "",
        f"生成时间：{datetime.now(timezone.utc).isoformat()}",
        "",
        f"Loop 文档门禁：`{summary['gate']}`",
        "",
        "## 总览",
        "",
        f"- 仓库 Markdown：{summary['repo_md']}",
        f"- KDS 镜像 Markdown：{summary['kds_md']}",
        f"- KDS 本地镜像流水：{summary['local_mirror_ledger_lines']}",
        f"- KDS 本地镜像唯一文档：{summary['local_mirror_unique_docs']}",
        f"- KDS API 同步流水：{summary['api_sync_ledger_lines']}",
        f"- 元数据缺失：{summary['missing_metadata']}",
        f"- README 缺失目录：{summary['missing_readme_dirs']}",
        "",
        "## 状态分布",
        "",
    ]
    for key, value in sorted(status_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 项目分布", ""])
    for key, value in sorted(project_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 命令结果", ""])
    for name, output in command_results.items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append("```text")
        lines.append(output or "(no output)")
        lines.append("```")
        lines.append("")
    content = "\n".join(lines)
    REPORT.write_text(content, encoding="utf-8")
    MIRROR_REPORT.parent.mkdir(parents=True, exist_ok=True)
    MIRROR_REPORT.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-only",
        "--no-write-report",
        action="store_true",
        dest="check_only",
        help="evaluate the gate without writing the health report or KDS mirror",
    )
    args = parser.parse_args()

    docs = iter_repo_md()
    missing_metadata = 0
    status_counts: Counter[str] = Counter()
    project_counts: Counter[str] = Counter()
    for path in docs:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".codex/skills/") and path.name == "SKILL.md":
            continue
        if is_okf_bundle_doc(path):
            status_counts["okf_derived"] += 1
            project_counts["KDS"] += 1
            continue
        fm = read_frontmatter(path)
        if not fm.get("doc_id"):
            missing_metadata += 1
        status_counts[fm.get("status", "missing")] += 1
        project_counts[fm.get("project", "missing")] += 1
    missing_readme_dirs = 0
    for directory in {path.parent for path in docs}:
        if directory == ROOT:
            continue
        if directory.relative_to(ROOT).as_posix().startswith(".okf/bundles/"):
            continue
        if not (directory / "README.md").exists():
            missing_readme_dirs += 1
    kds_md = len(list((ROOT / ".kds/development-space/开发").rglob("*.md"))) if (ROOT / ".kds/development-space/开发").exists() else 0
    local_mirror_ledger = ROOT / ".kds/local-mirror-ledger.jsonl"
    local_mirror_ledger_lines = len(local_mirror_ledger.read_text(encoding="utf-8").splitlines()) if local_mirror_ledger.exists() else 0
    local_mirror_unique_docs = count_unique_mirror_docs(local_mirror_ledger)
    api_sync_ledger = ROOT / ".kds/sync-ledger.jsonl"
    api_sync_ledger_lines = len(api_sync_ledger.read_text(encoding="utf-8").splitlines()) if api_sync_ledger.exists() else 0
    checks = {
        "document_pollution": run([sys.executable, "tools/kds-sync/check_document_pollution.py"]),
        "kds_token": run([sys.executable, "tools/kds-sync/validate_kds_token.py"]),
    }
    hard_failures = [name for name, (code, _) in checks.items() if code != 0 and name != "kds_token"]
    token_blocked = checks["kds_token"][0] != 0
    if missing_metadata or missing_readme_dirs or hard_failures:
        gate = "rework_required"
    elif token_blocked:
        gate = "blocked"
    elif kds_md < local_mirror_unique_docs:
        gate = "partial"
    else:
        gate = "pass"
    summary = {
        "gate": gate,
        "repo_md": len(docs),
        "kds_md": kds_md,
        "local_mirror_ledger_lines": local_mirror_ledger_lines,
        "local_mirror_unique_docs": local_mirror_unique_docs,
        "api_sync_ledger_lines": api_sync_ledger_lines,
        "missing_metadata": missing_metadata,
        "missing_readme_dirs": missing_readme_dirs,
        "status_counts": dict(status_counts),
        "project_counts": dict(project_counts),
    }
    command_results = {name: output for name, (_, output) in checks.items()}
    if not args.check_only:
        write_report(summary, command_results)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if gate == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
