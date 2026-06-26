#!/usr/bin/env python3
"""Validate P9S source-direct authorization template is complete but not executable."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
TEMPLATE = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.template.json"
INTAKE = ROOT / "tools/kds-sync/validate_agent_reach_p9_source_direct_live_authorization_intake.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-template-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-template-20260626.md"

REQUIRED_PLACEHOLDER_FIELDS = {"authorized_by", "authorized_at", "expires_at"}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_authorization_template=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_intake():
    spec = importlib.util.spec_from_file_location("agent_reach_p9s_authorization_intake_for_template", INTAKE)
    if spec is None or spec.loader is None:
        fail("intake_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_template(request: dict[str, Any], template: dict[str, Any]) -> list[str]:
    required = request["required_authorization_fields"]
    reasons: list[str] = []
    for key, value in required.items():
        if key not in template:
            reasons.append(f"missing_template_field:{key}")
            continue
        if key in REQUIRED_PLACEHOLDER_FIELDS:
            if not str(template[key]).startswith("<required-"):
                reasons.append(f"template_placeholder_missing:{key}")
        elif template[key] != value:
            reasons.append(f"template_field_mismatch:{key}")
    if template.get("human_authorization_text") != request.get("required_text"):
        reasons.append("human_authorization_text_mismatch")
    if "scope_note" not in template or "禁止写凭据" not in template["scope_note"]:
        reasons.append("scope_note_missing_boundary")
    return reasons


def build_report() -> dict[str, Any]:
    request = read_json(REQUEST)
    template = read_json(TEMPLATE)
    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("authorization_request_status_mismatch")
    reasons = validate_template(request, template)
    if reasons:
        fail(",".join(reasons))
    intake = load_intake()
    intake_report = intake.build_report(TEMPLATE)
    if intake_report.get("authorization_valid") is not False:
        fail("template_unexpectedly_valid")
    if intake_report.get("ready_for_live_execution") is not False:
        fail("template_unexpectedly_ready")
    if intake_report.get("live_external_fetch_invoked") is not False:
        fail("template_intake_live_fetch_invoked")
    return {
        "id": "agent-reach-p9-source-direct-authorization-template-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_authorization_template_ready",
        "current_admission": "limited_candidate_only",
        "template_path": TEMPLATE.relative_to(ROOT).as_posix(),
        "authorization_request": REQUEST.relative_to(ROOT).as_posix(),
        "template_field_count": len(template),
        "placeholder_fields": sorted(REQUIRED_PLACEHOLDER_FIELDS),
        "template_intake_status": intake_report["status"],
        "template_authorization_valid": intake_report["authorization_valid"],
        "template_ready_for_live_execution": intake_report["ready_for_live_execution"],
        "live_external_fetch_invoked": False,
        "completion_claim_allowed": False,
        "non_claims": [
            "authorization_template_only",
            "template_not_valid_authorization",
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
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-AUTHORIZATION-TEMPLATE-20260626",
            "title: Agent-Reach P9S Source Direct Authorization Template 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-authorization-template-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-authorization-template-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Authorization Template 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- template_path: `{report['template_path']}`",
            f"- template_authorization_valid: `{report['template_authorization_valid']}`",
            f"- template_ready_for_live_execution: `{report['template_ready_for_live_execution']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence validates the human-fill authorization template only.",
            "- The template intentionally remains invalid until placeholder fields are replaced by human authorization values.",
            "- This evidence does not invoke live target-site fetch.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_authorization_template=pass "
        f"status={report['status']} template_valid=false live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
