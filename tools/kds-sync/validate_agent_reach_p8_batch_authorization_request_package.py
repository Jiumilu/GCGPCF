#!/usr/bin/env python3
"""Validate the Agent-Reach P8 batch authorization request package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
PLAN_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-plan-20260622.json"
OUTPUT_GATE = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-batch-authorization-request-package-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-batch-authorization-request-package-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-AUTHORIZATION-REQUEST-PACKAGE-001.md"

ALLOWED_CHANNELS = {"web", "rss", "bilibili"}
FORBIDDEN_ACTIONS = {
    "credential_write",
    "browser_cookie_extraction",
    "kds_canonical_write",
    "gfis_source_of_record_write",
    "production_config_write",
    "global_mcp_config_write",
    "production_integration",
    "accepted_claim",
    "integrated_claim",
    "production_ready_claim",
}
REDACTION_FIELDS = {
    "redact_tokens",
    "redact_cookies",
    "redact_authorization_headers",
    "redact_query_personal_data",
    "persist_redacted_snippets_only",
}
SECURITY_FALSE_FIELDS = [
    "agent_reach_binary_invoked",
    "live_external_search_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_batch_authorization_request_package=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def validate_required_fields(fields: dict[str, Any], batch_id: str, query_count: int) -> None:
    if fields.get("authorization_status") != "approved_for_p8_project_group_full_live_search_batch":
        fail(f"required_status_mismatch:{batch_id}")
    if fields.get("authorized_by") != "lujunxiang":
        fail(f"required_authorized_by_mismatch:{batch_id}")
    if fields.get("batch_id") != batch_id:
        fail(f"required_batch_id_mismatch:{batch_id}")
    if set(fields.get("allowed_channels", [])) != ALLOWED_CHANNELS:
        fail(f"required_allowed_channels_mismatch:{batch_id}")
    if fields.get("max_queries") != query_count:
        fail(f"required_max_queries_mismatch:{batch_id}")
    if fields.get("max_results_per_query") != 10:
        fail(f"required_max_results_per_query_mismatch:{batch_id}")
    if fields.get("allow_agent_reach_binary_invocation") is not False:
        fail(f"binary_invocation_must_remain_false:{batch_id}")
    if fields.get("allow_external_network") is not True:
        fail(f"external_network_not_requested:{batch_id}")
    if fields.get("allow_write_evidence_only") is not True:
        fail(f"write_scope_not_evidence_only:{batch_id}")
    if not FORBIDDEN_ACTIONS.issubset(set(fields.get("forbidden_actions", []))):
        fail(f"required_forbidden_actions_missing:{batch_id}")
    redaction = fields.get("logging_redaction", {})
    for field in REDACTION_FIELDS:
        if redaction.get(field) is not True:
            fail(f"required_redaction_not_true:{batch_id}:{field}")


def main() -> None:
    request = load_json(REQUEST)
    plan = load_json(PLAN)
    plan_evidence = load_json(PLAN_EVIDENCE)
    output_gate = load_json(OUTPUT_GATE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    if request.get("authorization_status") != "pending_human_authorization":
        fail("request_status_mismatch")
    if request.get("generated_local_authorization_files") is not False:
        fail("request_generated_local_auth_not_false")
    if request.get("execution_allowed_now") is not False:
        fail("request_execution_allowed_not_false")
    if request.get("source_plan") != "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json":
        fail("source_plan_mismatch")
    if plan.get("execution_authorization_required_before_live") is not True:
        fail("plan_authorization_not_required")
    if plan_evidence.get("status") != "full_project_group_live_coverage_plan_ready":
        fail("plan_evidence_not_ready")
    if output_gate.get("status") != "full_project_group_live_coverage_output_quality_gate_ready":
        fail("output_quality_gate_not_ready")

    plan_batches = {batch["batch_id"]: batch for batch in plan.get("batches", [])}
    requests = request.get("batch_authorization_requests", [])
    if len(requests) != 3:
        fail("batch_request_count_mismatch")
    seen_batches: set[str] = set()
    local_auth_paths: list[Path] = []
    for item in requests:
        batch_id = item.get("batch_id")
        if batch_id not in plan_batches:
            fail(f"batch_out_of_plan:{batch_id}")
        if batch_id in seen_batches:
            fail(f"duplicate_batch_request:{batch_id}")
        seen_batches.add(batch_id)
        plan_batch = plan_batches[batch_id]
        queries = plan_batch.get("queries", [])
        if item.get("required_text") != plan_batch.get("authorization_required_text"):
            fail(f"required_text_mismatch:{batch_id}")
        if item.get("projects") != [query["project"] for query in queries]:
            fail(f"projects_mismatch:{batch_id}")
        if item.get("query_ids") != [query["query_id"] for query in queries]:
            fail(f"query_ids_mismatch:{batch_id}")
        local_auth_path = ROOT / item.get("authorization_file_to_create_after_human_approval", "")
        local_auth_paths.append(local_auth_path)
        if local_auth_path.exists():
            fail(f"local_authorization_file_exists_before_human_approval:{local_auth_path.relative_to(ROOT)}")
        validate_required_fields(item.get("required_authorization_fields", {}), batch_id, len(queries))
    if set(plan_batches) != seen_batches:
        fail("not_all_batches_have_request")

    if evidence.get("status") != "p8_batch_authorization_request_package_ready":
        fail("evidence_status_mismatch")
    if evidence.get("completion_claim_allowed") is not False:
        fail("completion_claim_allowed_not_false")
    checks = evidence.get("request_checks", {})
    for field in [
        "request_package_created",
        "three_batch_requests_created",
        "required_text_matches_plan",
        "local_authorization_files_not_created",
        "required_fields_machine_validatable",
        "output_quality_gate_ready_before_execution",
        "execution_still_requires_human_authorization",
    ]:
        if checks.get(field) is not True:
            fail(f"request_check_not_true:{field}")
    controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    for marker in [
        "p8_batch_authorization_request_package_ready",
        "授权执行 Agent-Reach P8 Project Group Full Live Search Batch 1",
        "授权执行 Agent-Reach P8 Project Group Full Live Search Batch 2",
        "授权执行 Agent-Reach P8 Project Group Full Live Search Batch 3",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p8_batch_authorization_request_package=pass "
        "status=p8_batch_authorization_request_package_ready "
        "batch_requests=3 local_authorization_files_created=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
