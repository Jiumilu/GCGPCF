#!/usr/bin/env python3
"""Validate CodeGraph dev execution localization debt closure."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-document-localization-debt-closure-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-document-localization-debt-closure-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-DOCUMENT-LOCALIZATION-DEBT-011.md"
LOCALIZATION_REPORT = ROOT / "09-status/globalcloud-chinese-localization-governance-report.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["GPCF_PROJECT_GROUP_GATE_DELEGATED"] = "1"
    return subprocess.run(args, cwd=ROOT, env=env, text=True, capture_output=True, check=False)


def extract_json(stdout: str) -> dict[str, Any]:
    start = stdout.find("{")
    end = stdout.rfind("}")
    require(start >= 0 and end >= start, f"no JSON object in command output: {stdout}")
    return json.loads(stdout[start : end + 1])


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    report = read(LOCALIZATION_REPORT)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-DOCUMENT-LOCALIZATION-DEBT-CLOSURE-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-DOCUMENT-LOCALIZATION-DEBT-011", "invalid scope")
    require(evidence["status"] == "document_localization_debt_closed", "invalid status")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012", "invalid next round")

    localization = evidence["localization_gate_evidence"]
    require(localization["localization_gate"] == "pass", "localization gate must pass")
    require(localization["docs_checked"] >= 822, "docs_checked below expected floor")
    require(localization["software_files_checked"] >= 240, "software_files_checked below expected floor")
    require(localization["findings"] == 0, "localization findings must be zero")
    require(localization["findings_by_kind"] == {}, "findings_by_kind must be empty")
    require(localization["localization_debt"] is False, "localization_debt must be false")

    loop_gate = evidence["loop_document_gate_evidence"]
    require(loop_gate["gate"] == "pass", "Loop document gate must pass")
    require(loop_gate["missing_metadata"] == 0, "missing_metadata must be zero")
    require(loop_gate["missing_readme_dirs"] == 0, "missing_readme_dirs must be zero")
    require(loop_gate["localization_debt"] is False, "Loop gate localization_debt must be false")
    require(loop_gate["fixed_doc_id_drift"] is False, "fixed_doc_id_drift must be false")

    governance = evidence["governance_evidence"]
    require(governance["document_pollution"] == "pass", "document pollution must pass")
    require(governance["kds_token"] == "pass", "KDS token must pass")
    require(governance["report_contains_current_pass_judgement"] is True, "report pass judgement missing")
    require(governance["report_stale_debt_claim_removed"] is True, "stale debt claim must be removed")
    require(governance["codegraph_git_isolated"] is True, ".codegraph must be git-isolated")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for forbidden in [
        "business implementation completed",
        "accepted",
        "integrated",
        "production_ready",
        "git commit performed",
        "git push performed",
        "deployment performed",
        "GFIS clean reindex performed",
    ]:
        require(forbidden in evidence["forbidden_claims"], f"missing forbidden claim: {forbidden}")

    for phrase in [
        "中文化门禁：`pass`",
        "问题总数：0",
        "`localization_debt=false`",
        "不得继续因中文化债务保持 `rework_required`",
    ]:
        require(phrase in report, f"localization report missing phrase: {phrase}")
    require("本报告证明当前项目群存在存量中文化债务。" not in report, "stale localization debt claim remains")

    for phrase in [
        "localization_gate=pass",
        "findings=0",
        "loop_document_gate=pass",
        "localization_debt=false",
        "不声明业务实现完成",
        "GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    localization_result = run(["python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json"])
    require(localization_result.returncode == 0, f"localization gate failed: {localization_result.stdout}{localization_result.stderr}")
    live_localization = extract_json(localization_result.stdout)
    require(live_localization["localization_gate"] == "pass", "live localization gate must pass")
    require(live_localization["docs_checked"] >= 822, "live docs_checked below expected floor")
    require(live_localization["software_files_checked"] >= 240, "live software_files_checked below expected floor")
    require(live_localization["findings"] == 0, "live localization findings must be zero")
    require(live_localization["findings_by_kind"] == {}, "live findings_by_kind must be empty")

    loop_result = run(["python3", "tools/kds-sync/loop_document_gate.py", "--check-only"])
    require(loop_result.returncode == 0, f"Loop document gate failed: {loop_result.stdout}{loop_result.stderr}")
    live_loop = extract_json(loop_result.stdout)
    require(live_loop["gate"] == "pass", "live Loop gate must pass")
    require(live_loop["missing_metadata"] == 0, "live missing_metadata must be zero")
    require(live_loop["missing_readme_dirs"] == 0, "live missing_readme_dirs must be zero")
    require(live_loop["localization_debt"] is False, "live localization_debt must be false")
    require(live_loop["fixed_doc_id_drift"] is False, "live fixed_doc_id_drift must be false")

    pollution_result = run(["python3", "tools/kds-sync/check_document_pollution.py"])
    require(pollution_result.returncode == 0, f"document pollution failed: {pollution_result.stdout}{pollution_result.stderr}")
    require("document_pollution=pass" in pollution_result.stdout, "document pollution output must pass")

    token_result = run(["python3", "tools/kds-sync/validate_kds_token.py"])
    require(token_result.returncode == 0, f"KDS token failed: {token_result.stdout}{token_result.stderr}")
    require("kds_token=pass" in token_result.stdout, "KDS token output must pass")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f".codegraph git status failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_document_localization_debt_closure=pass "
        "localization_gate=pass findings=0 "
        "loop_document_gate=pass localization_debt=false "
        "document_pollution=pass kds_token=pass "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
