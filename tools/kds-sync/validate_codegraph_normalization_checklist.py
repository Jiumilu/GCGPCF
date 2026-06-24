#!/usr/bin/env python3
"""Validate the CodeGraph normalization checklist and its operational gates."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CHECKLIST = ROOT / "02-governance/loop/LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST.md"
README = ROOT / "02-governance/loop/README.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-normalization-checklist-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-normalization-checklist-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-NORMALIZATION-CHECKLIST-001.md"
AUTH_TEMPLATE = ROOT / "templates/CODEGRAPH_DEV_EXECUTION_AUTHORIZATION_TEMPLATE.json"
EVIDENCE_TEMPLATE = ROOT / "templates/CODEGRAPH_DEV_EXECUTION_EVIDENCE_TEMPLATE.json"
PROJECT_GROUP_COVERAGE = ROOT / "02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md"
GOAL_OPTIMIZATION = ROOT / "02-governance/loop/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_PLAN.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def extract_json(stdout: str) -> dict[str, Any]:
    start = stdout.find("{")
    end = stdout.rfind("}")
    require(start >= 0 and end >= start, f"no JSON object in command output: {stdout}")
    return json.loads(stdout[start : end + 1])


def main() -> int:
    checklist = read(CHECKLIST)
    readme = read(README)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    auth = load_json(AUTH_TEMPLATE)
    evidence_template = load_json(EVIDENCE_TEMPLATE)
    coverage = read(PROJECT_GROUP_COVERAGE)
    goal = read(GOAL_OPTIMIZATION)

    for phrase in [
        "所有开发任务开工前强制执行 `codegraph query / node / affected`。",
        "任务单必须固定写 `target_nodes`、`affected_scope`、`files_allowed_to_change`、`files_not_to_touch`。",
        "`affected_tests=[]` 时必须带 `fallback_tests` 和 `fallback_reason`。",
        "缺少 `codegraph_evidence` 的任务，直接阻断进入实现。",
        "每个业务变更的 evidence 固定包含 `codegraph_evidence`。",
        "Harness / WAES 不把 CodeGraph 当参考材料，而是当验收输入之一。",
        "每轮 Loop 都要看 14 仓 `codegraph status`。",
        "`.codegraph/` 始终保持 Git 隔离。",
        "有 drift 先 watch，不直接 sync。",
        "`sync / reindex` 继续走授权边界。",
        "CodeGraph 准入、pilot pack、Harness gate、impact metrics baseline",
        "CodeGraph 不替代源码审查。",
    ]:
        require(phrase in checklist, f"checklist missing phrase: {phrase}")

    require("LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST.md" in readme, "README must link the normalization checklist")

    for phrase in [
        "target_nodes",
        "affected_scope",
        "files_allowed_to_change",
        "files_not_to_touch",
        "affected_tests or fallback_reason",
        "post_change_status",
    ]:
        require(phrase in json.dumps(auth, ensure_ascii=False), f"authorization template missing field: {phrase}")

    for phrase in [
        "codegraph_evidence",
        "target_nodes",
        "affected_scope",
        "files_allowed_to_change",
        "files_not_to_touch",
        "expected_tests",
        "fallback_tests",
        "fallback_reason",
        "manual_scan_files",
        "codegraph_candidate_files",
        "actual_changed_files",
        "missed_impact_count",
        "time_to_first_target",
    ]:
        require(phrase in json.dumps(evidence_template, ensure_ascii=False), f"evidence template missing field: {phrase}")

    for phrase in [
        "14 个本机 Git 仓库纳入 CodeGraph",
        "WAS世界资产体系",
        "CodeGraph 项目群覆盖表",
    ]:
        require(phrase in coverage, f"project group coverage missing phrase: {phrase}")

    for phrase in [
        "探索工具调用、读文件数、轮次耗时、返工次数和影响遗漏",
        "trend_down",
        "至少 3 个真实任务记录 CodeGraph 查询、影响面、测试选择和结果",
    ]:
        require(phrase in goal, f"goal optimization plan missing phrase: {phrase}")

    for key in ["project_group_steady_state_verify", "dev_execution_admission", "dev_execution_pilot_pack", "dev_execution_harness_gate", "impact_metrics_baseline", "impact_report_dry_run", "dev_execution_steady_state_monitor"]:
        require(evidence["operational_gates"][key] in {"pass", "pass_with_watch"}, f"gate must be pass-like: {key}")

    require(evidence["current_state"]["repo_count"] == 14, "repo count mismatch")
    require(evidence["current_state"]["all_repo_codegraph_initialized"] is True, "all repos must be initialized")
    require(evidence["current_state"]["all_codegraph_git_isolated"] is True, "all repos must keep codegraph git isolation")
    require(evidence["current_state"]["codegraph_reindex_recommended"] is False, "reindex must not be recommended")
    require(evidence["current_state"]["watchlist_mode"] == "monitor_only", "watchlist mode must be monitor_only")

    loop_gate = run(["python3", "tools/kds-sync/loop_document_gate.py", "--check-only"])
    require(loop_gate.returncode == 0, f"Loop gate failed: {loop_gate.stderr}{loop_gate.stdout}")
    loop_gate_json = extract_json(loop_gate.stdout)
    require(loop_gate_json["gate"] == "pass", "Loop gate must pass")

    loc = run(["python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json"])
    require(loc.returncode == 0, f"localization gate failed: {loc.stderr}{loc.stdout}")
    loc_json = extract_json(loc.stdout)
    require(loc_json["localization_gate"] == "pass", "localization gate must pass")
    require(loc_json["findings"] == 0, "localization findings must be zero")

    pollution = run(["python3", "tools/kds-sync/check_document_pollution.py"])
    require(pollution.returncode == 0 and "document_pollution=pass" in pollution.stdout, "document pollution must pass")

    token = run(["python3", "tools/kds-sync/validate_kds_token.py"])
    require(token.returncode == 0 and "kds_token=pass" in token.stdout, "KDS token must pass")

    require("normalization_checklist_ready_with_watch" in evidence["status"], "evidence status mismatch")
    require("GPCF-CODEGRAPH-NORMALIZATION-WATCH-002" in evidence["next_round"], "next round mismatch")
    require("CodeGraph 常态化清单已固化为受控文档" in evidence_md, "evidence md missing summary")
    require("CodeGraph 常态化归一清单" in loop_round, "loop round missing title")

    print(
        "codegraph_normalization_checklist=pass "
        "repo_count=14 all_repo_codegraph_initialized=true all_codegraph_git_isolated=true "
        "watchlist_mode=monitor_only "
        "next=GPCF-CODEGRAPH-NORMALIZATION-WATCH-002"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
