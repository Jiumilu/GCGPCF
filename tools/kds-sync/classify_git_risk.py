#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
OUTPUT_JSON = ROOT / "docs/harness/evidence/git-risk-classification-20260617.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/git-risk-classification-20260617.md"


def run_git(repo: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", "-c", "core.quotePath=false", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed in {repo}: {completed.stdout}{completed.stderr}")
    return completed.stdout


def parse_status_line(line: str) -> tuple[str, str, str]:
    status = line[:2]
    path = line[3:]
    if " -> " in path:
        _old, path = path.split(" -> ", 1)
    return status, path, line


def category_for(repo_name: str, status: str, path: str) -> str:
    lower = path.lower()
    if path == ".codex/config.toml" or any(token in lower for token in [".env", "token", "secret", "private_key", ".pem", ".key"]):
        return "sensitive_config_review"
    if status.strip().startswith("D"):
        return "deletion_or_missing_file_risk"
    if path.startswith(".kds/"):
        return "kds_local_mirror_and_ledger"
    if path.startswith("docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-") or path.startswith(
        "docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-"
    ):
        return "legacy_or_prior_loop_round_artifacts"
    if repo_name == "GFIS" and (
        path.startswith("docs/harness/sop-e2e/")
        or path.startswith("docs/harness/evidence/")
        or path.startswith("docs/harness/loop")
        or path.startswith("scripts/build_gfis_")
        or path.startswith("scripts/validate_gfis_")
        or path == "gcfis_custom/gcfis_custom/api.py"
    ):
        return "gfis_runtime_repair"
    if repo_name == "GFIS" and (path.startswith("gcfis_demo/") or path.startswith("tests/e2e/")):
        return "gfis_demo_regression"
    if repo_name == "GPCF" and (
        path.startswith("02-governance/")
        or path.startswith("09-status/")
        or path.startswith("docs/harness/")
        or path.startswith("tools/kds-sync/")
        or path.startswith("08-evidence-samples/")
    ):
        return "gpcf_governance_and_control_sync"
    if path.endswith(".md") or path in {"AGENTS.md", "README.md", "PROJECT_HARNESS_MANIFEST.md"}:
        return "project_documentation"
    return "unclassified_requires_manual_review"


def classify_repo(repo_name: str, repo: Path) -> dict[str, Any]:
    branch_line = run_git(repo, ["status", "--short", "--branch"]).splitlines()[0]
    status_lines = run_git(repo, ["status", "--porcelain=v1"]).splitlines()
    entries: list[dict[str, str]] = []
    categories: dict[str, list[dict[str, str]]] = defaultdict(list)
    status_counts: Counter[str] = Counter()

    for line in status_lines:
        status, path, raw = parse_status_line(line)
        category = category_for(repo_name, status, path)
        item = {"status": status, "path": path, "category": category, "raw": raw}
        entries.append(item)
        categories[category].append(item)
        if status == "??":
            status_counts["untracked"] += 1
        elif "D" in status:
            status_counts["deleted_or_missing"] += 1
        elif "M" in status:
            status_counts["modified"] += 1
        else:
            status_counts["other"] += 1

    high_risk_categories = [
        "sensitive_config_review",
        "deletion_or_missing_file_risk",
        "unclassified_requires_manual_review",
    ]
    high_risk_count = sum(len(categories.get(category, [])) for category in high_risk_categories)

    return {
        "repo": repo_name,
        "path": str(repo),
        "branch": branch_line,
        "total_items": len(entries),
        "status_counts": dict(status_counts),
        "category_counts": {key: len(value) for key, value in sorted(categories.items())},
        "high_risk_count": high_risk_count,
        "entries": entries,
        "recommendation": "classify_before_commit_no_delete_no_reset",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Git 风险分类报告",
        "",
        f"- generated_at: `{report['generated_at']}`",
        "- scope: GPCF + GFIS",
        "- policy: 只分类、不删除、不 reset、不 checkout",
        "- next: 按分类形成提交候选，再从 KDS 候选提取 5 类真实凭证责任方回执任务",
        "",
        "## 汇总",
        "",
        "| 仓库 | 分支 | total | modified | untracked | deleted/missing | high risk |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for repo in report["repositories"]:
        counts = repo["status_counts"]
        lines.append(
            "| {repo} | `{branch}` | {total} | {modified} | {untracked} | {deleted} | {high} |".format(
                repo=repo["repo"],
                branch=repo["branch"],
                total=repo["total_items"],
                modified=counts.get("modified", 0),
                untracked=counts.get("untracked", 0),
                deleted=counts.get("deleted_or_missing", 0),
                high=repo["high_risk_count"],
            )
        )
    lines.extend(["", "## 分类计数", ""])
    for repo in report["repositories"]:
        lines.extend([f"### {repo['repo']}", "", "| 分类 | 数量 | 处置建议 |", "|---|---:|---|"])
        for category, count in repo["category_counts"].items():
            advice = {
                "gfis_runtime_repair": "优先作为 runtime repair 提交候选复核",
                "gpcf_governance_and_control_sync": "优先作为总控同步提交候选复核",
                "kds_local_mirror_and_ledger": "确认是否属于 KDS 开发空间镜像与审计流水",
                "gfis_demo_regression": "只作为 pass_demo_only 展示层回归候选",
                "legacy_or_prior_loop_round_artifacts": "按历史轮次证据归档或提交，不能计为新实质轮次",
                "project_documentation": "复核是否属于主体定位或治理文档更新",
                "sensitive_config_review": "必须人工复核，默认不得提交",
                "deletion_or_missing_file_risk": "必须人工复核，禁止自动删除",
                "unclassified_requires_manual_review": "人工判定归属后再提交",
            }.get(category, "人工复核")
            lines.append(f"| `{category}` | {count} | {advice} |")
        sample_items = repo["entries"][:20]
        lines.extend(["", "前 20 项样例：", ""])
        for item in sample_items:
            lines.append(f"- `{item['status']}` `{item['path']}` -> `{item['category']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "classify_only_no_delete_no_reset_no_checkout",
        "repositories": [
            classify_repo("GPCF", ROOT),
            classify_repo("GFIS", GFIS_ROOT),
        ],
        "next_order": [
            "split_git_changes_by_category_before_commit",
            "extract_five_real_proof_owner_receipt_tasks_from_kds_candidates",
            "prioritize_customer_requirement_or_platform_order_source_of_record",
            "prioritize_customer_requirement_or_platform_order_dispatch_confirmation",
            "then_waes_confirmation_kds_write_receipt_runtime_primary_key",
        ],
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(report) + "\n", encoding="utf-8")
    for repo in report["repositories"]:
        print(
            "git_risk_classification=pass "
            f"repo={repo['repo']} total={repo['total_items']} "
            f"modified={repo['status_counts'].get('modified', 0)} "
            f"untracked={repo['status_counts'].get('untracked', 0)} "
            f"deleted_or_missing={repo['status_counts'].get('deleted_or_missing', 0)} "
            f"high_risk={repo['high_risk_count']}"
        )


if __name__ == "__main__":
    main()
