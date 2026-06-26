#!/usr/bin/env python3
"""Validate Agent-Reach P9S source-direct authorization request."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-request-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-request-20260626.md"

FORBIDDEN_ACTIONS = {
    "credential_write",
    "browser_cookie_extraction",
    "credentialed_api",
    "login_required_page",
    "kds_canonical_write",
    "gfis_source_of_record_write",
    "production_config_write",
    "global_mcp_config_write",
    "production_integration",
    "accepted_claim",
    "integrated_claim",
    "production_ready_claim",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_authorization_request=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_report() -> dict[str, Any]:
    request = load_json(REQUEST)
    precheck = load_json(ROOT / request["precheck_fixture"])
    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("request_status_mismatch")
    if request.get("required_text") != "授权执行 Agent-Reach P9S Source Direct Hit-Rate Live Run":
        fail("required_text_mismatch")
    if precheck.get("status") != "p9_source_direct_hit_rate_precheck_ready":
        fail("precheck_status_mismatch")
    scope = request.get("execution_scope", {})
    if scope.get("target_count") != 13 or scope.get("domain_count") != 10:
        fail("scope_target_domain_count_mismatch")
    if scope.get("max_targets") != 13 or scope.get("max_entrypoints_per_target") != 3 or scope.get("max_pages_per_entrypoint") != 5:
        fail("scope_limits_mismatch")
    fields = request.get("required_authorization_fields", {})
    if fields.get("authorization_id") != "agent-reach-p9-source-direct-hit-rate-live-run":
        fail("authorization_id_mismatch")
    if fields.get("authorization_status") != "approved_for_p9_source_direct_hit_rate_live_run":
        fail("authorization_status_mismatch")
    if fields.get("allow_external_network") is not True:
        fail("external_network_not_true")
    if fields.get("allow_write_evidence_only") is not True:
        fail("write_scope_not_evidence_only")
    if not FORBIDDEN_ACTIONS <= set(fields.get("forbidden_actions", [])):
        fail("forbidden_actions_missing")
    for field in request.get("security_controls", {}):
        if request["security_controls"][field] is not False:
            fail(f"security_control_not_false:{field}")
    return {
        "id": "agent-reach-p9-source-direct-authorization-request-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_authorization_request_ready",
        "current_admission": "limited_candidate_only",
        "required_text": request["required_text"],
        "authorization_file_to_create_after_human_approval": request["authorization_file_to_create_after_human_approval"],
        "max_targets": scope["max_targets"],
        "max_entrypoints_per_target": scope["max_entrypoints_per_target"],
        "max_pages_per_entrypoint": scope["max_pages_per_entrypoint"],
        "live_external_fetch_invoked": False,
        "non_claims": request["non_claims"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-AUTHORIZATION-REQUEST-20260626",
            "title: Agent-Reach P9S Source Direct 授权请求 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-authorization-request-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-authorization-request-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct 授权请求 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- required_text: `{report['required_text']}`",
            f"- max_targets: `{report['max_targets']}`",
            f"- max_entrypoints_per_target: `{report['max_entrypoints_per_target']}`",
            f"- max_pages_per_entrypoint: `{report['max_pages_per_entrypoint']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            "",
            "## 边界",
            "",
            "- 本证据只准备 P9S source-direct 授权请求。",
            "- 本证据不执行目标站点直连读取。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_authorization_request=pass "
        f"status={report['status']} max_targets={report['max_targets']} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
