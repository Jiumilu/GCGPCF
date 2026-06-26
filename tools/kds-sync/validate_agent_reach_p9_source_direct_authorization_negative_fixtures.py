#!/usr/bin/env python3
"""Validate P9S source-direct authorization intake rejects unsafe negative fixtures."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
INTAKE = ROOT / "tools/kds-sync/validate_agent_reach_p9_source_direct_live_authorization_intake.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_authorization_negative_fixtures=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_intake():
    spec = importlib.util.spec_from_file_location("agent_reach_p9s_authorization_intake", INTAKE)
    if spec is None or spec.loader is None:
        fail("intake_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def positive_auth(request: dict[str, Any]) -> dict[str, Any]:
    fields = deepcopy(request["required_authorization_fields"])
    fields["authorized_by"] = "negative-fixture-validator"
    fields["authorized_at"] = "2026-06-26T00:00:00+08:00"
    fields["expires_at"] = "2027-06-26T23:59:59+08:00"
    return fields


def negative_cases(base_auth: dict[str, Any]) -> list[tuple[str, dict[str, Any], str]]:
    cases: list[tuple[str, dict[str, Any], str]] = []

    auth = deepcopy(base_auth)
    auth["expires_at"] = "2026-06-25T23:59:59+08:00"
    cases.append(("expired_authorization", auth, "authorization_expired"))

    auth = deepcopy(base_auth)
    auth["allowed_methods"] = ["target_url", "credentialed_api"]
    cases.append(("method_out_of_scope", auth, "allowed_methods_mismatch"))

    auth = deepcopy(base_auth)
    auth["max_pages_per_entrypoint"] = 50
    cases.append(("page_limit_too_high", auth, "max_pages_per_entrypoint_mismatch"))

    auth = deepcopy(base_auth)
    auth["max_targets"] = 99
    cases.append(("target_limit_too_high", auth, "max_targets_mismatch"))

    auth = deepcopy(base_auth)
    auth["allow_write_evidence_only"] = False
    cases.append(("write_scope_not_evidence_only", auth, "write_scope_not_evidence_only"))

    auth = deepcopy(base_auth)
    auth["forbidden_actions"] = [item for item in auth["forbidden_actions"] if item != "credentialed_api"]
    cases.append(("forbidden_action_missing", auth, "forbidden_actions_missing"))

    auth = deepcopy(base_auth)
    auth["logging_redaction"]["redact_cookies"] = False
    cases.append(("redaction_missing", auth, "redaction_not_true:redact_cookies"))

    auth = deepcopy(base_auth)
    del auth["authorized_by"]
    cases.append(("required_field_missing", auth, "authorization_missing_fields:authorized_by"))

    return cases


def run_case(intake, tmp_dir: Path, case_id: str, auth: dict[str, Any], expected_reason: str) -> dict[str, Any]:
    auth_path = tmp_dir / f"{case_id}.json"
    auth_path.write_text(json.dumps(auth, ensure_ascii=False, indent=2), encoding="utf-8")
    report = intake.build_report(auth_path)
    reasons = report.get("authorization_reasons", [])
    passed = (
        report.get("status") == "blocked_invalid_p9_source_direct_authorization"
        and report.get("authorization_valid") is False
        and report.get("ready_for_live_execution") is False
        and expected_reason in reasons
        and report.get("live_external_fetch_invoked") is False
    )
    if not passed:
        fail(f"negative_case_unexpected_result:{case_id}:{reasons}")
    return {
        "case_id": case_id,
        "expected_reason": expected_reason,
        "status": report["status"],
        "authorization_valid": report["authorization_valid"],
        "ready_for_live_execution": report["ready_for_live_execution"],
        "live_external_fetch_invoked": report["live_external_fetch_invoked"],
    }


def build_report() -> dict[str, Any]:
    request = read_json(REQUEST)
    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("authorization_request_status_mismatch")
    intake = load_intake()
    base_auth = positive_auth(request)
    with tempfile.TemporaryDirectory(prefix="agent-reach-p9s-negative-auth-") as tmp:
        tmp_dir = Path(tmp)
        results = [run_case(intake, tmp_dir, case_id, auth, expected) for case_id, auth, expected in negative_cases(base_auth)]
    return {
        "id": "agent-reach-p9-source-direct-authorization-negative-fixtures-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_authorization_negative_fixtures_pass",
        "current_admission": "limited_candidate_only",
        "mode": "authorization_negative_fixture_no_live_fetch",
        "negative_case_count": len(results),
        "negative_cases": results,
        "live_external_fetch_invoked": False,
        "completion_claim_allowed": False,
        "non_claims": [
            "negative_fixture_only",
            "not_live_fetch_invoked",
            "not_live_run_completed",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "---",
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-AUTHORIZATION-NEGATIVE-FIXTURES-20260626",
        "title: Agent-Reach P9S Source Direct Authorization Negative Fixtures 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct Authorization Negative Fixtures 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- negative_case_count: `{report['negative_case_count']}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
        "",
        "## Negative Cases",
        "",
    ]
    for item in report["negative_cases"]:
        lines.append(f"- `{item['case_id']}` -> `{item['expected_reason']}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This evidence validates negative authorization fixtures only.",
            "- This evidence does not invoke live target-site fetch.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_authorization_negative_fixtures=pass "
        f"cases={report['negative_case_count']} live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
