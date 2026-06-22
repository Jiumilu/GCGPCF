#!/usr/bin/env python3
"""Validate CodeGraph goal optimization admission for Loop Engineering."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "02-governance/loop/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_PLAN.md"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-goal-optimization-20260620.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-goal-optimization-20260620.json"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-GOAL-OPT-001.md"
RECORD_TEMPLATE = ROOT / "templates/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_RECORD_TEMPLATE.md"
GITIGNORE = ROOT / ".gitignore"


REQUIRED_FRONTMATTER_KEYS = [
    "doc_id:",
    "title:",
    "project:",
    "related_projects:",
    "domain:",
    "status:",
    "version:",
    "owner:",
    "kds_space:",
    "kds_path:",
    "source_path:",
    "sync_direction:",
    "last_reviewed:",
    "supersedes:",
    "superseded_by:",
]

REQUIRED_FIELDS = [
    "codegraph_enabled",
    "codegraph_scope_query",
    "impacted_symbols",
    "impacted_files",
    "manual_source_check",
    "related_validators",
    "exploration_tool_calls_before",
    "exploration_tool_calls_after",
    "file_reads_before",
    "file_reads_after",
    "scope_precision_result",
    "optimization_feedback",
]

TARGET_LOOP_STEPS = [
    "目标声明",
    "图谱预检",
    "影响面收敛",
    "最小动作计划",
    "验证选择",
    "执行",
    "结果度量",
    "规则沉淀",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def frontmatter(path: Path, text: str) -> str:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    return text[:end]


def validate_controlled(path: Path, text: str, source_path: str) -> None:
    metadata = frontmatter(path, text)
    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in metadata, f"{path.relative_to(ROOT)} missing front matter key {key}")
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    plan = read(PLAN)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    record_template = read(RECORD_TEMPLATE)
    gitignore = read(GITIGNORE)
    evidence = load_json(EVIDENCE_JSON)

    validate_controlled(PLAN, plan, "02-governance/loop/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_PLAN.md")
    validate_controlled(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/loop-codegraph-goal-optimization-20260620.md",
    )
    validate_controlled(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-CODEGRAPH-GOAL-OPT-001.md",
    )
    validate_controlled(
        RECORD_TEMPLATE,
        record_template,
        "templates/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_RECORD_TEMPLATE.md",
    )

    require(".codegraph/" in gitignore, ".gitignore must exclude .codegraph/")

    for phrase in [
        "colbymchenry/codegraph",
        "代码图谱感知",
        "目标优化",
        "P0 准入设计",
        "P1 本地试点",
        "P2 对照度量",
        "P3 模板固化",
        "P4 持续进化",
        "Definition of Done",
        "`.codegraph/` 必须保持本地缓存",
        "不证明 GFIS runtime SOP E2E 已通过",
        "不授权生产写入",
        "Harness/WAES",
    ]:
        require(phrase in plan, f"plan missing phrase: {phrase}")

    for field in REQUIRED_FIELDS:
        require(field in plan, f"plan missing required CodeGraph field: {field}")
        require(field in evidence_md, f"evidence markdown missing required CodeGraph field: {field}")
        require(field in record_template, f"record template missing required CodeGraph field: {field}")

    for step in TARGET_LOOP_STEPS:
        require(step in plan, f"plan missing target optimization step: {step}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "substantive_rounds",
        "completed_p0_admission",
        "未执行，保持授权边界",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for phrase in [
        "目标声明",
        "CodeGraph 预检",
        "影响面收敛",
        "最小动作计划",
        "验证选择",
        "执行后度量",
        "反馈沉淀",
        "不证明业务完成",
    ]:
        require(phrase in record_template, f"record template missing phrase: {phrase}")

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-GOAL-OPT-20260620", "invalid evidence id")
    require(evidence.get("status") == "p0_admission_pass", "evidence status must be p0_admission_pass")
    scope = evidence.get("scope", {})
    require(scope.get("installation_performed") is False, "installation must not be recorded as performed")
    require(scope.get("mcp_configuration_changed") is False, "MCP config must not be recorded as changed")
    require(scope.get("codegraph_index_created") is False, "CodeGraph index must not be recorded as created")
    require(scope.get("production_write") is False, "production write must be false")
    require(scope.get("external_api_write") is False, "external API write must be false")

    evidence_fields = evidence.get("required_fields", [])
    require(isinstance(evidence_fields, list), "evidence required_fields must be a list")
    for field in REQUIRED_FIELDS:
        require(field in evidence_fields, f"evidence JSON missing required field: {field}")

    controls = evidence.get("admission_controls", {})
    require(controls.get("codegraph_cache_gitignored") is True, "cache gitignore control must be true")
    require(controls.get("manual_source_check_required") is True, "manual source check must be required")
    require(controls.get("harness_waes_not_replaced") is True, "Harness/WAES replacement must be blocked")
    require(controls.get("kds_token_not_written") is True, "KDS token must not be written")
    require(controls.get("status_upgrade_allowed") is False, "status upgrade must not be allowed")

    non_claims = "\n".join(evidence.get("non_claims", []))
    for phrase in [
        "does not prove GFIS runtime SOP E2E passed",
        "does not create source-of-record",
        "does not authorize production write",
        "does not replace source review",
    ]:
        require(phrase in non_claims, f"evidence non-claims missing phrase: {phrase}")

    codegraph_available = shutil.which("codegraph") is not None
    print(
        "loop_codegraph_goal_optimization=pass "
        "evidence=LOOP-CODEGRAPH-GOAL-OPT-20260620 "
        "status=p0_admission_pass "
        f"required_fields={len(REQUIRED_FIELDS)} "
        f"codegraph_cli_available={str(codegraph_available).lower()} "
        "installation_performed=false mcp_configuration_changed=false "
        "codegraph_index_created=false status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
