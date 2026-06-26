#!/usr/bin/env python3
"""Validate CodeGraph real-input dispatch authorization request evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-dispatch-authorization-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-dispatch-authorization-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-DISPATCH-AUTHORIZATION-019.md"
COLLECTION_PACK = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-collection-pack-20260626.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    collection = load_json(COLLECTION_PACK)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-REAL-INPUT-DISPATCH-AUTHORIZATION-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-DISPATCH-AUTHORIZATION-019", "invalid scope")
    require(evidence["status"] == "dispatch_authorization_request_ready_not_authorized", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(collection["status"] == "real_input_collection_pack_prepared_not_dispatched", "collection pack source status mismatch")

    collection_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_real_input_collection_pack.py"])
    require(collection_gate.returncode == 0, f"collection pack gate failed: {collection_gate.stdout}{collection_gate.stderr}")

    state = evidence["authorization_state"]
    require(state["request_prepared"] is True, "authorization request must be prepared")
    require(state["authorization_received"] is False, "authorization must not be received")
    require(state["default_if_no_answer"] == "not_authorized", "default must be not_authorized")
    require(state["dispatch_allowed"] is False, "dispatch must not be allowed")
    require(state["dispatch_performed"] is False, "dispatch must not be performed")
    require(state["external_notifications_sent"] == 0, "external notifications must be zero")
    require(state["external_api_write"] is False, "external API write must be false")
    require(state["real_kds_write"] is False, "real KDS write must be false")
    require(state["real_waes_write"] is False, "real WAES write must be false")

    questions = evidence["authorization_questions"]
    require(len(questions) == 1, "must contain exactly one authorization question")
    question = questions[0]
    require(question["id"] == "real_input_collection_dispatch", "invalid question id")
    require(question["recommended_option"] == "not_authorized_keep_prepared", "recommended option must be keep prepared")
    require(question["default_if_no_answer"] == "not_authorized", "question default must be not_authorized")
    option_ids = {item["id"] for item in question["options"]}
    require("not_authorized_keep_prepared" in option_ids, "missing keep-prepared option")
    require("authorize_dispatch_precheck_only" in option_ids, "missing precheck-only option")
    require("authorize_actual_dispatch_later" in option_ids, "missing later-dispatch option")

    for key, value in evidence["dispatch_prerequisites"].items():
        require(value is False, f"{key} must stay false before authorization")

    for phrase in [
        "recipient identity confirmation",
        "manual channel confirmation",
        "payload preview",
        "no-send dry run",
    ]:
        require(phrase in evidence["allowed_future_precheck_scope"], f"missing allowed precheck scope: {phrase}")

    for phrase in [
        "external notification dispatch",
        "external API write",
        "real KDS write",
        "real WAES write",
        "git commit",
        "git push",
        "accepted/integrated/production_ready/customer_accepted status upgrade",
    ]:
        require(phrase in evidence["forbidden_in_this_round"], f"missing forbidden action: {phrase}")

    decision = evidence["decision"]
    require(decision["dispatch_authorization_request"] == "ready", "request decision mismatch")
    require(decision["dispatch_authorization"] == "not_authorized", "dispatch authorization must be not_authorized")
    require(decision["real_business_execution"] == "blocked_until_real_source_input_arrives", "real business execution must remain blocked")
    require(decision["runtime_state"] == "not_verified", "runtime state must not be verified")
    require(decision["status_ceiling"] == "partial", "status ceiling must be partial")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "dispatch_authorization_request_ready_not_authorized",
        "authorization_received=false",
        "default_if_no_answer=not_authorized",
        "dispatch_allowed=false",
        "not_authorized_keep_prepared",
        "authorize_dispatch_precheck_only",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-DISPATCH-PRECHECK-020",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-AUTHORIZATION-WAITING-020",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "authorization_request_ready_not_authorized"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_real_input_dispatch_authorization=ready_not_authorized "
        "request_prepared=true "
        "authorization_received=false "
        "default_if_no_answer=not_authorized "
        "dispatch_allowed=false "
        "dispatch_performed=false "
        "next_if_authorized=GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-DISPATCH-PRECHECK-020 "
        "next_if_not_authorized=GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-AUTHORIZATION-WAITING-020"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
