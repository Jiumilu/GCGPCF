#!/usr/bin/env python3
"""Validate Headroom project-group admission and cost-model evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOV_DOC = ROOT / "02-governance/GlobalCloud项目群Headroom接入应用与成本评估模型.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-project-group-admission-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-project-group-admission-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-ADMISSION-001.md"
COST_CALCULATOR = ROOT / "tools/kds-sync/calculate_headroom_cost_model.py"
MEASUREMENT_TEMPLATE = ROOT / "fixtures/headroom/headroom-cost-measurement-template.json"
L2_DRY_RUN_EVIDENCE = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
RUNTIME_PROBE_EVIDENCE = ROOT / "docs/harness/evidence/headroom-runtime-probe-20260621.json"
RUNTIME_ADAPTER_DRY_RUN_EVIDENCE = ROOT / "docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json"
RUNTIME_SCENARIO_MATRIX_EVIDENCE = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json"
COST_MEASUREMENT_OUTPUT_EVIDENCE = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.json"
MARKER_PRESERVATION_POLICY_EVIDENCE = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"
CONTROLLED_METRIC_PILOT_EVIDENCE = ROOT / "docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json"
LOOP_COST_OBSERVATION_EVIDENCE = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-20260621.json"
LOOP_COST_OBSERVATION_SERIES_EVIDENCE = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json"
MARKER_PRESERVING_ADAPTER_PILOT_EVIDENCE = ROOT / "docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json"
INDEPENDENT_LOOP_ROUND_REPLAY_EVIDENCE = ROOT / "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json"
PRODUCTION_TOKEN_INTAKE_GATE_EVIDENCE = ROOT / "docs/harness/evidence/headroom-production-token-intake-gate-20260621.json"
PRODUCTION_TOKEN_LEDGER_TEMPLATE = ROOT / "fixtures/headroom/headroom-production-token-ledger-template.json"
PRODUCTION_TOKEN_LEDGER_TEMPLATE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_ledger_template.py"
PRODUCTION_TOKEN_LEDGER_EVALUATOR = ROOT / "tools/kds-sync/evaluate_headroom_production_token_ledger.py"
PRODUCTION_TOKEN_LEDGER_NEGATIVE_FIXTURES = ROOT / "fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json"
PRODUCTION_TOKEN_LEDGER_NEGATIVE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py"
PRODUCTION_TOKEN_AUTHORIZATION_PACKAGE = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json"
PRODUCTION_TOKEN_AUTHORIZATION_PACKAGE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_authorization_package.py"
PRODUCTION_TOKEN_AUTHORIZATION_ACTION_QUEUE = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json"
PRODUCTION_TOKEN_AUTHORIZATION_ACTION_QUEUE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_authorization_action_queue.py"
PROJECT_GROUP_APPLICATION_ROUTER = ROOT / "docs/harness/evidence/headroom-project-group-application-router-20260621.json"
PROJECT_GROUP_APPLICATION_ROUTER_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_project_group_application_router.py"
PROJECT_APPLICATION_COVERAGE_MATRIX = ROOT / "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.json"
PROJECT_APPLICATION_COVERAGE_MATRIX_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_project_application_coverage_matrix.py"
COST_SENSITIVITY_MODEL = ROOT / "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json"
COST_SENSITIVITY_MODEL_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_cost_sensitivity_model.py"

PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")
    require(
        "last_reviewed: 2026-06-21" in metadata
        or "last_reviewed: 2026-06-22" in metadata
        or "last_reviewed: 2026-06-23" in metadata,
        f"{path.relative_to(ROOT)} missing controlled marker: last_reviewed",
    )


def require_phrases(text_name: str, text: str, phrases: list[str]) -> None:
    for phrase in phrases:
        require(phrase in text, f"{text_name} missing phrase: {phrase}")


def main() -> int:
    gov_doc = read(GOV_DOC)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    cost_calculator = read(COST_CALCULATOR)
    measurement_template = load_json(MEASUREMENT_TEMPLATE)
    l2_dry_run_evidence = load_json(L2_DRY_RUN_EVIDENCE)
    runtime_probe_evidence = load_json(RUNTIME_PROBE_EVIDENCE)
    runtime_adapter_dry_run_evidence = load_json(RUNTIME_ADAPTER_DRY_RUN_EVIDENCE)
    runtime_scenario_matrix_evidence = load_json(RUNTIME_SCENARIO_MATRIX_EVIDENCE)
    cost_measurement_output_evidence = load_json(COST_MEASUREMENT_OUTPUT_EVIDENCE)
    marker_preservation_policy_evidence = load_json(MARKER_PRESERVATION_POLICY_EVIDENCE)
    controlled_metric_pilot_evidence = load_json(CONTROLLED_METRIC_PILOT_EVIDENCE)
    loop_cost_observation_evidence = load_json(LOOP_COST_OBSERVATION_EVIDENCE)
    loop_cost_observation_series_evidence = load_json(LOOP_COST_OBSERVATION_SERIES_EVIDENCE)
    marker_preserving_adapter_pilot_evidence = load_json(MARKER_PRESERVING_ADAPTER_PILOT_EVIDENCE)
    independent_loop_round_replay_evidence = load_json(INDEPENDENT_LOOP_ROUND_REPLAY_EVIDENCE)
    production_token_intake_gate_evidence = load_json(PRODUCTION_TOKEN_INTAKE_GATE_EVIDENCE)
    production_token_ledger_template = load_json(PRODUCTION_TOKEN_LEDGER_TEMPLATE)
    production_token_ledger_template_validator = read(PRODUCTION_TOKEN_LEDGER_TEMPLATE_VALIDATOR)
    production_token_ledger_evaluator = read(PRODUCTION_TOKEN_LEDGER_EVALUATOR)
    production_token_ledger_negative_fixtures = load_json(PRODUCTION_TOKEN_LEDGER_NEGATIVE_FIXTURES)
    production_token_ledger_negative_validator = read(PRODUCTION_TOKEN_LEDGER_NEGATIVE_VALIDATOR)
    production_token_authorization_package = load_json(PRODUCTION_TOKEN_AUTHORIZATION_PACKAGE)
    production_token_authorization_package_validator = read(PRODUCTION_TOKEN_AUTHORIZATION_PACKAGE_VALIDATOR)
    production_token_authorization_action_queue = load_json(PRODUCTION_TOKEN_AUTHORIZATION_ACTION_QUEUE)
    production_token_authorization_action_queue_validator = read(PRODUCTION_TOKEN_AUTHORIZATION_ACTION_QUEUE_VALIDATOR)
    project_group_application_router = load_json(PROJECT_GROUP_APPLICATION_ROUTER)
    project_group_application_router_validator = read(PROJECT_GROUP_APPLICATION_ROUTER_VALIDATOR)
    project_application_coverage_matrix = load_json(PROJECT_APPLICATION_COVERAGE_MATRIX)
    project_application_coverage_matrix_validator = read(PROJECT_APPLICATION_COVERAGE_MATRIX_VALIDATOR)
    cost_sensitivity_model = load_json(COST_SENSITIVITY_MODEL)
    cost_sensitivity_model_validator = read(COST_SENSITIVITY_MODEL_VALIDATOR)

    require_frontmatter(GOV_DOC, gov_doc)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "HEADROOM-PROJECT-GROUP-ADMISSION-20260621", "invalid evidence id")
    require(evidence.get("status") == "admission_and_cost_model_defined", "invalid evidence status")

    tool = evidence.get("tool", {})
    require(tool.get("name") == "headroom", "tool name mismatch")
    require(tool.get("role") == "ai_context_compression_infrastructure_candidate", "tool role mismatch")
    require(tool.get("license") == "Apache-2.0", "license mismatch")
    require(tool.get("telemetry_required_default") == "off", "telemetry default must be off")

    project_group = evidence.get("project_group", {})
    covered = project_group.get("projects_covered", [])
    require(covered == PROJECTS, "project coverage list mismatch")
    require(project_group.get("admission_level") == "L1_governance_defined_L2_dry_run_ready", "admission level mismatch")
    for key in ["accepted", "integrated", "production_ready"]:
        require(project_group.get(key) is False, f"{key} must remain false")

    artifacts = evidence.get("artifacts", {})
    for key, expected in {
        "governance_doc": GOV_DOC.relative_to(ROOT).as_posix(),
        "evidence_md": EVIDENCE_MD.relative_to(ROOT).as_posix(),
        "loop_round": LOOP_ROUND.relative_to(ROOT).as_posix(),
        "validator": "tools/kds-sync/validate_headroom_project_group_admission.py",
        "cost_calculator": COST_CALCULATOR.relative_to(ROOT).as_posix(),
        "measurement_template": MEASUREMENT_TEMPLATE.relative_to(ROOT).as_posix(),
        "l2_project_group_dry_run": L2_DRY_RUN_EVIDENCE.relative_to(ROOT).as_posix(),
        "runtime_probe": RUNTIME_PROBE_EVIDENCE.relative_to(ROOT).as_posix(),
        "runtime_adapter_dry_run": RUNTIME_ADAPTER_DRY_RUN_EVIDENCE.relative_to(ROOT).as_posix(),
        "runtime_scenario_matrix": RUNTIME_SCENARIO_MATRIX_EVIDENCE.relative_to(ROOT).as_posix(),
        "cost_measurement_output": COST_MEASUREMENT_OUTPUT_EVIDENCE.relative_to(ROOT).as_posix(),
        "marker_preservation_policy": MARKER_PRESERVATION_POLICY_EVIDENCE.relative_to(ROOT).as_posix(),
        "controlled_metric_pilot": CONTROLLED_METRIC_PILOT_EVIDENCE.relative_to(ROOT).as_posix(),
        "loop_cost_observation": LOOP_COST_OBSERVATION_EVIDENCE.relative_to(ROOT).as_posix(),
        "loop_cost_observation_series": LOOP_COST_OBSERVATION_SERIES_EVIDENCE.relative_to(ROOT).as_posix(),
        "marker_preserving_adapter_pilot": MARKER_PRESERVING_ADAPTER_PILOT_EVIDENCE.relative_to(ROOT).as_posix(),
        "independent_loop_round_replay": INDEPENDENT_LOOP_ROUND_REPLAY_EVIDENCE.relative_to(ROOT).as_posix(),
        "production_token_intake_gate": PRODUCTION_TOKEN_INTAKE_GATE_EVIDENCE.relative_to(ROOT).as_posix(),
        "production_token_ledger_template": PRODUCTION_TOKEN_LEDGER_TEMPLATE.relative_to(ROOT).as_posix(),
        "production_token_ledger_template_validator": PRODUCTION_TOKEN_LEDGER_TEMPLATE_VALIDATOR.relative_to(ROOT).as_posix(),
        "production_token_ledger_evaluator": PRODUCTION_TOKEN_LEDGER_EVALUATOR.relative_to(ROOT).as_posix(),
        "production_token_ledger_negative_fixtures": PRODUCTION_TOKEN_LEDGER_NEGATIVE_FIXTURES.relative_to(ROOT).as_posix(),
        "production_token_ledger_negative_validator": PRODUCTION_TOKEN_LEDGER_NEGATIVE_VALIDATOR.relative_to(ROOT).as_posix(),
        "production_token_authorization_package": PRODUCTION_TOKEN_AUTHORIZATION_PACKAGE.relative_to(ROOT).as_posix(),
        "production_token_authorization_package_validator": PRODUCTION_TOKEN_AUTHORIZATION_PACKAGE_VALIDATOR.relative_to(ROOT).as_posix(),
        "production_token_authorization_action_queue": PRODUCTION_TOKEN_AUTHORIZATION_ACTION_QUEUE.relative_to(ROOT).as_posix(),
        "production_token_authorization_action_queue_validator": PRODUCTION_TOKEN_AUTHORIZATION_ACTION_QUEUE_VALIDATOR.relative_to(ROOT).as_posix(),
        "project_group_application_router": PROJECT_GROUP_APPLICATION_ROUTER.relative_to(ROOT).as_posix(),
        "project_group_application_router_validator": PROJECT_GROUP_APPLICATION_ROUTER_VALIDATOR.relative_to(ROOT).as_posix(),
        "project_application_coverage_matrix": PROJECT_APPLICATION_COVERAGE_MATRIX.relative_to(ROOT).as_posix(),
        "project_application_coverage_matrix_validator": PROJECT_APPLICATION_COVERAGE_MATRIX_VALIDATOR.relative_to(ROOT).as_posix(),
        "cost_sensitivity_model": COST_SENSITIVITY_MODEL.relative_to(ROOT).as_posix(),
        "cost_sensitivity_model_validator": COST_SENSITIVITY_MODEL_VALIDATOR.relative_to(ROOT).as_posix(),
    }.items():
        require(artifacts.get(key) == expected, f"artifact path mismatch: {key}")

    cost_model = evidence.get("cost_model", {})
    for key in [
        "baseline_cost_formula",
        "headroom_cost_formula",
        "saving_rate_formula",
        "minimum_l2_saving_rate",
        "minimum_l3_saving_rate",
        "minimum_l4_candidate_saving_rate",
    ]:
        require(key in cost_model, f"cost model missing key: {key}")
    require(cost_model.get("minimum_l2_saving_rate") == 0.2, "L2 saving threshold mismatch")
    require(cost_model.get("minimum_l3_saving_rate") == 0.3, "L3 saving threshold mismatch")
    require(cost_model.get("minimum_l4_candidate_saving_rate") == 0.4, "L4 saving threshold mismatch")
    require(cost_model.get("measured_project_group_tokens") is False, "measured tokens must not be claimed")

    require(measurement_template.get("measurement_id") == "HEADROOM-COST-MEASUREMENT-TEMPLATE", "template id mismatch")
    require(measurement_template.get("sensitive_raw_text_stored") is False, "template must not store raw text")
    require(measurement_template.get("telemetry") == "off", "template telemetry must be off")
    require(measurement_template.get("minimum_saving_rate") == 0.2, "template L2 threshold mismatch")
    require(measurement_template.get("answer_equivalence") == "pass", "template answer equivalence must pass")
    require(measurement_template.get("sensitive_redaction_gate") == "pass", "template redaction gate must pass")
    require("gross_saving" in cost_calculator, "cost calculator missing gross_saving")
    require("admission_gate" in cost_calculator, "cost calculator missing admission_gate")
    require(l2_dry_run_evidence.get("evidence_id") == "HEADROOM-L2-PROJECT-GROUP-DRY-RUN-20260621", "L2 evidence id mismatch")
    require(l2_dry_run_evidence.get("project_count") == 15, "L2 project count mismatch")
    require(l2_dry_run_evidence.get("headroom_runtime_used") is False, "L2 must not claim real runtime use")
    require(l2_dry_run_evidence.get("measured_production_tokens") is False, "L2 must not claim production measurements")
    require(l2_dry_run_evidence.get("aggregate", {}).get("all_admission_gates_pass") is True, "L2 dry-run gates must pass")
    require(runtime_probe_evidence.get("evidence_id") == "HEADROOM-RUNTIME-PROBE-20260621", "runtime probe evidence id mismatch")
    require(runtime_probe_evidence.get("project_count") == 15, "runtime probe project count mismatch")
    require(runtime_probe_evidence.get("headroom_runtime_used") is True, "runtime probe must execute runtime")
    require(runtime_probe_evidence.get("aggregate", {}).get("runtime_saving_rate") == 0.0, "runtime probe saving rate must remain explicit")
    require(runtime_probe_evidence.get("decision", {}).get("runtime_admission_gate") is False, "runtime admission must remain blocked")
    require(runtime_probe_evidence.get("measured_production_tokens") is False, "runtime probe must not claim production measurements")
    require(runtime_adapter_dry_run_evidence.get("evidence_id") == "HEADROOM-RUNTIME-ADAPTER-DRY-RUN-20260621", "runtime adapter evidence id mismatch")
    require(runtime_adapter_dry_run_evidence.get("project_count") == 15, "runtime adapter project count mismatch")
    require(runtime_adapter_dry_run_evidence.get("headroom_runtime_used") is True, "runtime adapter must execute runtime")
    adapter_aggregate = runtime_adapter_dry_run_evidence.get("aggregate", {})
    require(adapter_aggregate.get("tokens_saved", 0) > 0, "runtime adapter must prove positive compression")
    require(adapter_aggregate.get("all_marker_gates_pass") is True, "runtime adapter marker gates must pass")
    require(
        adapter_aggregate.get("runtime_adapter_saving_rate", 0) < adapter_aggregate.get("minimum_saving_rate", 0.2),
        "runtime adapter must remain below threshold until remeasured",
    )
    require(runtime_adapter_dry_run_evidence.get("decision", {}).get("runtime_adapter_admission_gate") is False, "runtime adapter admission must remain false")
    require(runtime_adapter_dry_run_evidence.get("measured_production_tokens") is False, "runtime adapter must not claim production measurements")
    require(runtime_scenario_matrix_evidence.get("evidence_id") == "HEADROOM-RUNTIME-SCENARIO-MATRIX-20260621", "runtime scenario matrix evidence id mismatch")
    require(runtime_scenario_matrix_evidence.get("project_count") == 15, "runtime scenario matrix project count mismatch")
    require(runtime_scenario_matrix_evidence.get("scenario_count") == 4, "runtime scenario matrix scenario count mismatch")
    require(runtime_scenario_matrix_evidence.get("headroom_runtime_used") is True, "runtime scenario matrix must execute runtime")
    matrix_aggregate = runtime_scenario_matrix_evidence.get("aggregate", {})
    require(matrix_aggregate.get("scenario_gate_pass_count") == 1, "runtime scenario matrix must remain partial")
    require(matrix_aggregate.get("all_scenario_gates_pass") is False, "runtime scenario matrix must not claim all scenarios pass")
    require(runtime_scenario_matrix_evidence.get("decision", {}).get("runtime_matrix_admission_gate") is False, "runtime matrix admission must remain false")
    require(runtime_scenario_matrix_evidence.get("measured_production_tokens") is False, "runtime scenario matrix must not claim production measurements")
    require(cost_measurement_output_evidence.get("evidence_id") == "HEADROOM-COST-MEASUREMENT-OUTPUT-20260621", "cost measurement output evidence id mismatch")
    require(cost_measurement_output_evidence.get("schema", {}).get("name") == "HeadroomCostMeasurement", "cost measurement output schema mismatch")
    require(cost_measurement_output_evidence.get("aggregate", {}).get("output_gate") is True, "cost measurement output gate must pass")
    require(cost_measurement_output_evidence.get("measured_production_tokens") is False, "cost measurement output must not claim production measurements")
    require(marker_preservation_policy_evidence.get("evidence_id") == "HEADROOM-MARKER-PRESERVATION-POLICY-20260621", "marker policy evidence id mismatch")
    marker_policy = marker_preservation_policy_evidence.get("policy", {})
    require(marker_policy.get("marker_loss_is_hard_block") is True, "marker loss must hard block")
    require(marker_policy.get("below_saving_threshold_is_hard_block") is True, "saving threshold must hard block")
    require("loop_validation_log" in marker_policy.get("rejected_scenarios", []), "log scenario must be rejected")
    require("rg_marker_search_output" in marker_policy.get("rejected_scenarios", []), "search scenario must be rejected")
    require(marker_preservation_policy_evidence.get("measured_production_tokens") is False, "marker policy must not claim production measurements")
    require(controlled_metric_pilot_evidence.get("evidence_id") == "HEADROOM-CONTROLLED-METRIC-PILOT-20260621", "controlled metric pilot evidence id mismatch")
    require(controlled_metric_pilot_evidence.get("pilot_scope") == "structured_metric_and_marker_preserving_adapter_outputs", "controlled metric pilot scope mismatch")
    require(controlled_metric_pilot_evidence.get("aggregate", {}).get("all_allowed_applications_applied") is True, "controlled metric pilot must apply allowed scenario")
    require(controlled_metric_pilot_evidence.get("aggregate", {}).get("all_rejected_applications_blocked") is True, "controlled metric pilot must block rejected scenarios")
    require(controlled_metric_pilot_evidence.get("decision", {}).get("controlled_metric_pilot_gate") is True, "controlled metric pilot gate must pass")
    require(controlled_metric_pilot_evidence.get("decision", {}).get("production_admission_gate") is False, "controlled metric pilot must not pass production gate")
    require(controlled_metric_pilot_evidence.get("measured_production_tokens") is False, "controlled metric pilot must not claim production measurements")
    require(loop_cost_observation_evidence.get("evidence_id") == "HEADROOM-LOOP-COST-OBSERVATION-20260621", "loop cost observation evidence id mismatch")
    require(loop_cost_observation_evidence.get("decision", {}).get("loop_cost_observation_gate") is True, "loop cost observation gate must pass")
    require(loop_cost_observation_evidence.get("aggregate", {}).get("all_blocked_scenarios_excluded") is True, "loop cost observation must exclude blocked scenarios")
    require(loop_cost_observation_evidence.get("aggregate", {}).get("runtime_saving_rate", 0) > 0, "loop cost observation must show runtime saving")
    require(loop_cost_observation_evidence.get("decision", {}).get("production_admission_gate") is False, "loop cost observation production gate must remain false")
    require(loop_cost_observation_evidence.get("measured_production_tokens") is False, "loop cost observation must not claim production measurements")
    require(loop_cost_observation_series_evidence.get("evidence_id") == "HEADROOM-LOOP-COST-OBSERVATION-SERIES-20260621", "loop cost observation series evidence id mismatch")
    require(loop_cost_observation_series_evidence.get("window_count") == 3, "loop cost observation series window count mismatch")
    series_aggregate = loop_cost_observation_series_evidence.get("aggregate", {})
    require(series_aggregate.get("all_window_gates_pass") is True, "loop cost observation series window gates must pass")
    require(series_aggregate.get("window_scope_normalized") is True, "loop cost observation series window scope must be normalized")
    require(series_aggregate.get("saving_rate_stability_gate") is True, "loop cost observation series stability gate must pass")
    require(series_aggregate.get("max_runtime_saving_rate_drift", 1) <= series_aggregate.get("drift_gate_threshold", 0), "loop cost observation series drift must stay within threshold")
    require(series_aggregate.get("production_admission_gate") is False, "loop cost observation series production gate must remain false")
    require(loop_cost_observation_series_evidence.get("decision", {}).get("loop_cost_observation_series_gate") is True, "loop cost observation series gate must pass")
    require(loop_cost_observation_series_evidence.get("decision", {}).get("production_admission_gate") is False, "loop cost observation series decision production gate must remain false")
    require(loop_cost_observation_series_evidence.get("measured_production_tokens") is False, "loop cost observation series must not claim production measurements")
    require(marker_preserving_adapter_pilot_evidence.get("evidence_id") == "HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-20260621", "marker-preserving adapter pilot evidence id mismatch")
    require(marker_preserving_adapter_pilot_evidence.get("adapter_scope") == "log_and_search_outputs_only", "marker-preserving adapter pilot scope mismatch")
    marker_adapter_aggregate = marker_preserving_adapter_pilot_evidence.get("aggregate", {})
    require(marker_adapter_aggregate.get("scenario_count") == 2, "marker-preserving adapter scenario count mismatch")
    require(marker_adapter_aggregate.get("adapter_gate_pass_count") == 2, "marker-preserving adapter pass count mismatch")
    require(marker_adapter_aggregate.get("all_marker_gates_pass") is True, "marker-preserving adapter marker gates must pass")
    require(marker_adapter_aggregate.get("all_adapter_gates_pass") is True, "marker-preserving adapter gates must pass")
    require(marker_preserving_adapter_pilot_evidence.get("decision", {}).get("marker_preserving_adapter_pilot_gate") is True, "marker-preserving adapter pilot gate must pass")
    require(marker_preserving_adapter_pilot_evidence.get("decision", {}).get("production_admission_gate") is False, "marker-preserving adapter production gate must remain false")
    require(marker_preserving_adapter_pilot_evidence.get("measured_production_tokens") is False, "marker-preserving adapter must not claim production measurements")
    require(independent_loop_round_replay_evidence.get("evidence_id") == "HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-20260621", "independent replay evidence id mismatch")
    require(independent_loop_round_replay_evidence.get("decision", {}).get("independent_round_gate") is True, "independent replay gate must pass")
    require(independent_loop_round_replay_evidence.get("decision", {}).get("production_admission_gate") is False, "independent replay production gate must remain false")
    require(independent_loop_round_replay_evidence.get("measured_production_tokens") is False, "independent replay must not claim production measurements")
    require(production_token_intake_gate_evidence.get("evidence_id") == "HEADROOM-PRODUCTION-TOKEN-INTAKE-GATE-20260621", "production token intake gate evidence id mismatch")
    require(production_token_intake_gate_evidence.get("gate", {}).get("production_token_intake_gate") is False, "production token intake gate must remain blocked")
    require(production_token_intake_gate_evidence.get("gate", {}).get("production_admission_gate") is False, "production token intake production gate must remain false")
    require(production_token_intake_gate_evidence.get("measured_production_tokens") is False, "production token intake must not claim production measurements")
    require(production_token_ledger_template.get("ledger_id") == "HEADROOM-PRODUCTION-TOKEN-LEDGER-TEMPLATE", "production token ledger template id mismatch")
    require(production_token_ledger_template.get("measured_production_tokens") is False, "production token ledger template must not claim production measurements")
    require(production_token_ledger_template.get("authorization", {}).get("authorized_window_id") is None, "production token ledger template must not claim authorization")
    require("admission_gate" in production_token_ledger_template_validator, "production token ledger validator must evaluate admission gate")
    require("evaluate_ledger" in production_token_ledger_evaluator, "production token ledger evaluator must expose evaluate_ledger")
    require(len(production_token_ledger_negative_fixtures.get("cases", [])) >= 5, "production token ledger negative fixtures too small")
    require("negative case was accepted" in production_token_ledger_negative_validator, "production token ledger negative validator must reject accepted negative cases")
    require(production_token_authorization_package.get("authorization", {}).get("status") == "pending", "production token authorization package must remain pending")
    require(production_token_authorization_package.get("gate", {}).get("authorization_package_gate") is False, "production token authorization package gate must remain false")
    require("authorization_package_gate" in production_token_authorization_package_validator, "production token authorization package validator must check gate")
    require(production_token_authorization_action_queue.get("gate", {}).get("authorization_action_queue_gate") is False, "production token authorization action queue gate must remain false")
    require(production_token_authorization_action_queue.get("gate", {}).get("action_count") == 6, "production token authorization action queue count mismatch")
    require("authorization_action_queue_gate" in production_token_authorization_action_queue_validator, "production token authorization action queue validator must check gate")
    require(project_group_application_router.get("evidence_id") == "HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-20260621", "project group application router evidence id mismatch")
    require(project_group_application_router.get("gate", {}).get("application_router_gate") is True, "application router gate must pass")
    require(project_group_application_router.get("gate", {}).get("dry_run_application_gate") is True, "dry-run application gate must pass")
    require(project_group_application_router.get("gate", {}).get("allowed_route_count") == 3, "application router allowed route count mismatch")
    require(project_group_application_router.get("gate", {}).get("blocked_route_count") == 3, "application router blocked route count mismatch")
    require(project_group_application_router.get("gate", {}).get("production_admission_gate") is False, "application router production gate must remain false")
    require(project_group_application_router.get("measured_production_tokens") is False, "application router must not claim production measurements")
    require("application_router_gate" in project_group_application_router_validator, "application router validator must check gate")
    require(project_application_coverage_matrix.get("evidence_id") == "HEADROOM-PROJECT-APPLICATION-COVERAGE-MATRIX-20260621", "project application coverage evidence id mismatch")
    require(project_application_coverage_matrix.get("gate", {}).get("project_count") == 15, "project application coverage project count mismatch")
    require(project_application_coverage_matrix.get("gate", {}).get("projects_with_l2_measurement") == 15, "project application coverage L2 count mismatch")
    require(project_application_coverage_matrix.get("gate", {}).get("projects_with_dry_run_routes") == 15, "project application dry-run coverage mismatch")
    require(project_application_coverage_matrix.get("gate", {}).get("projects_with_production_routes") == 0, "project application production routes must be zero")
    require(project_application_coverage_matrix.get("gate", {}).get("project_application_coverage_gate") is True, "project application coverage gate must pass")
    require(project_application_coverage_matrix.get("gate", {}).get("production_admission_gate") is False, "project application production gate must remain false")
    require(project_application_coverage_matrix.get("measured_production_tokens") is False, "project application coverage must not claim production measurements")
    require("project_application_coverage_gate" in project_application_coverage_matrix_validator, "project application coverage validator must check gate")
    require(cost_sensitivity_model.get("evidence_id") == "HEADROOM-COST-SENSITIVITY-MODEL-20260621", "cost sensitivity evidence id mismatch")
    require(cost_sensitivity_model.get("gate", {}).get("profile_count") == 3, "cost sensitivity profile count mismatch")
    require(cost_sensitivity_model.get("gate", {}).get("project_count") == 15, "cost sensitivity project count mismatch")
    require(cost_sensitivity_model.get("gate", {}).get("all_profiles_admission_gate") is True, "cost sensitivity profiles must pass")
    require(cost_sensitivity_model.get("gate", {}).get("cost_sensitivity_gate") is True, "cost sensitivity gate must pass")
    require(cost_sensitivity_model.get("gate", {}).get("production_admission_gate") is False, "cost sensitivity production gate must remain false")
    require(cost_sensitivity_model.get("measured_production_tokens") is False, "cost sensitivity must not claim production measurements")
    require("cost_sensitivity_gate" in cost_sensitivity_model_validator, "cost sensitivity validator must check gate")

    for key, value in evidence.get("security_gates", {}).items():
        require(value is True, f"security gate must be true: {key}")
    for key, value in evidence.get("loop_engineering", {}).items():
        require(value is True, f"loop engineering marker must be true: {key}")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")

    common_phrases = [
        "Headroom",
        "ai_context_compression_infrastructure_candidate",
        "HEADROOM_TELEMETRY=off",
        "baseline_cost",
        "headroom_cost",
        "saving_rate",
        "HeadroomScenario",
        "HeadroomCostMeasurement",
        "HeadroomEquivalenceGate",
        "HeadroomSecurityGate",
        "HeadroomCostDecision",
        "accepted",
        "integrated",
        "production_ready",
    ]
    require_phrases("governance doc", gov_doc, common_phrases)
    require_phrases("evidence md", evidence_md, ["HEADROOM-PROJECT-GROUP-ADMISSION-20260621", "not_done", "Cost calculator", "Project-group L2 sample measurement", "Real Headroom runtime probe", "Runtime adapter dry-run", "Runtime scenario matrix", "HeadroomCostMeasurement", "Marker preservation policy", "Controlled metric pilot", "Loop cost observation", "Loop cost observation series", "Marker-preserving adapter pilot", "Independent LOOP round replay", "Production token intake gate", "Production token ledger template", "Production token ledger negative fixtures", "Production token authorization package", "Production token authorization action queue", "Project-group application router", "Project application coverage matrix", "Cost sensitivity model"])
    require_phrases("loop round", loop_round, ["输入", "动作", "输出", "检查", "反馈", "calculate_headroom_cost_model.py"])
    for project in PROJECTS:
        require(project in gov_doc, f"governance doc missing project: {project}")
        require(project in evidence_md, f"evidence md missing project: {project}")

    print(
        "headroom_project_group_admission=pass "
        "status=admission_and_cost_model_defined "
        "projects_covered=15 "
        "l1_governance=pass l2_dry_run_ready=pass "
        "cost_model=defined cost_calculator=pass measured_tokens=false "
        "telemetry_required_default=off accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
