#!/usr/bin/env python3
"""Validate Loop Engineering self-correction integrity after GFIS subject drift."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")
SELF_CORRECTION_DOC = ROOT / "02-governance/loop/LOOP_ENGINEERING_SELF_CORRECTION.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
GFIS_RUNTIME_EVIDENCE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dry-run-result.json"
GFIS_KDS_COVERAGE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json"
GFIS_FAILURE_ANALYSIS = GFIS_ROOT / "docs/harness/sop-e2e/e2e-failure-analysis.md"
GFIS_API = GFIS_ROOT / "gcfis_custom/gcfis_custom/api.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def run_gfis_validator() -> list[str]:
    validator = GFIS_ROOT / "scripts/validate_gfis_runtime_sop_e2e.py"
    require(validator.exists(), "GFIS runtime SOP E2E validator is missing")
    result = subprocess.run(
        [sys.executable, str(validator.relative_to(GFIS_ROOT))],
        cwd=str(GFIS_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    lines = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines() if line.strip()]
    if result.returncode not in {0, 2} and not any(line.startswith("gfis_runtime_sop_e2e=") for line in lines):
        lines.append("gfis_runtime_sop_e2e=repair_required")
    require(any(line.startswith("gfis_runtime_sop_e2e=") for line in lines), "GFIS validator did not emit status")
    require(result.returncode in {0, 1, 2}, f"unexpected GFIS validator exit code: {result.returncode}")
    return lines


def run_gfis_contract_validator() -> str:
    validator = GFIS_ROOT / "scripts/validate_gfis_work_order_api_contract.py"
    require(validator.exists(), "GFIS work-order API contract validator is missing")
    result = subprocess.run(
        [sys.executable, str(validator.relative_to(GFIS_ROOT))],
        cwd=str(GFIS_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    output = result.stdout + "\n" + result.stderr
    require(result.returncode == 0, f"GFIS contract validator failed: {output.strip()}")
    require(
        "gfis work-order API contract validation passed" in output,
        "GFIS contract validator did not emit pass marker",
    )
    return output


def main() -> int:
    doc = read(SELF_CORRECTION_DOC)
    control = read(CONTROL_BOARD)
    status = read(STATUS_MATRIX)
    loop_state = read(LOOP_STATE)
    gfis_agents = read(GFIS_ROOT / "AGENTS.md")
    gfis_readme = read(GFIS_ROOT / "README.md")
    gfis_manifest = read(GFIS_ROOT / "PROJECT_HARNESS_MANIFEST.md")
    gfis_failure_analysis = read(GFIS_FAILURE_ANALYSIS)
    gfis_api_source = read(GFIS_API)
    validator_output = run_gfis_validator()
    contract_validator_output = run_gfis_contract_validator()
    validator_text = "\n".join(validator_output)
    gfis_runtime_evidence = json.loads(read(GFIS_RUNTIME_EVIDENCE))
    gfis_kds_coverage = json.loads(read(GFIS_KDS_COVERAGE))

    for phrase in [
        "GFIS 运行层",
        "GFIS Demo",
        "不能用于",
        "二次复盘结论",
        "关键问题重述",
        "Loop 重新总结",
        "Loop Engineering 定义",
        "自我发现失败根因",
        "自我发现闭环",
        "自我发现触发器",
        "解决问题路线",
        "防复发工程门禁",
        "Loop Engineering 操作模型",
        "主体权威门禁",
        "失败优先门禁",
        "E2E 测试大师失败",
        "SOP Master 结论公式",
        "P0 级 Loop 事故",
        "问题到门禁映射",
        "subject_drift_detected",
        "sop_e2e_master=failed_or_repair_required",
        "pass_demo_only",
        "controlled_reference_not_live_proof",
        "verified live artifact",
        "SOP E2E Master 门禁",
        "事故复盘",
        "substantive_rounds",
        "事实层",
        "工程层",
        "治理层",
        "自我发现",
        "自我降级",
        "自我拆解",
        "自我修复",
        "自我防复发",
        "quality_inspection",
        "delivery_note",
        "gfis_runtime_sop_e2e=repair_required",
        "work_order_runtime=runtime_api_passed_temp_created_cleanup_required",
        "runtime_sop_chain_gate=blocked",
        "sample_request",
        "production_release_gate",
        "raw_material_plan",
        "proof_of_delivery",
        "project_group_score=78",
        "Loop Engineering 重定义 v2",
        "主体先行",
        "失败先行",
        "证据分层",
        "最小实质修复",
        "机器门禁",
        "审计回放",
        "防复发学习",
        "自我发现与解决机制",
        "高质量可用判定",
        "下一轮工程方向",
        "GFIS runtime verified artifact collection",
        "open/collected 计数",
        "全类别 ready 判定",
        "GFIS runtime verified artifact collection dossier",
        "采集案卷",
        "proof anchors",
        "weak verified artifact",
    ]:
        require(phrase in doc, f"self-correction doc missing phrase: {phrase}")

    for phrase in [
        "sop_e2e_master=failed_or_repair_required",
        "gfis_runtime_sop_e2e=repair_required",
        "demo_e2e=pass_demo_only",
        "P0 事故",
        "subject=GFIS运行层",
        "单类有效 POD/WAES/KDS 凭证仍必须保持",
        "runtime_verified_artifact_collection_dossier=verified_artifact_collection_dossier_open",
        "source_record_uri",
        "source_record_hash",
        "verification_actor",
        "verification_method",
        "weak artifact",
    ]:
        require(phrase in gfis_failure_analysis, f"GFIS failure analysis missing phrase: {phrase}")

    for phrase in [
        "source_record_uri",
        "source_record_hash",
        "verification_actor",
        "verification_method",
        "source_system_not_allowed_for_category",
        "invalid_source_record_hash",
        "invalid_source_record_uri",
        "demo_source_not_allowed",
    ]:
        require(phrase in gfis_api_source, f"GFIS API source missing proof-anchor phrase: {phrase}")

    require(
        "gfis work-order API contract validation passed" in contract_validator_output,
        "GFIS contract validator pass marker missing",
    )

    for phrase in [
        "GFIS 运行层",
        "GFIS Demo 只用于展示",
        "不作为 SOP 实现主体",
    ]:
        require(phrase in gfis_agents + "\n" + gfis_readme + "\n" + gfis_manifest, f"GFIS subject boundary missing: {phrase}")

    for phrase in [
        "gfis_runtime_sop_e2e=repair_required",
        "runtime_contract_status=loaded_current_contract",
        "work_order_runtime=runtime_api_passed_temp_created_cleanup_required",
        "runtime_sop_chain_gate=blocked",
        "runtime_sample_request_gate=blocked",
        "runtime_raw_material_gate=blocked",
        "runtime_production_execution_gate=blocked",
        "runtime_quality_inventory_gate=blocked",
        "runtime_delivery_logistics_gate=blocked",
        "runtime_pod_gate=blocked",
        "runtime_finance_boundary_gate=blocked",
        "runtime_gap_resolution_plan=repair_required",
        "runtime_gfis_repair_candidate=runtime_gfis_repair_candidate_passed_temp_created_cleanup_required",
        "runtime_live_input_gate=missing_live_business_inputs",
        "runtime_verified_artifact_gate=missing_verified_live_artifacts",
        "runtime_verified_artifact_intake=missing_verified_artifact_intake",
        "runtime_weak_verified_artifact=weak_verified_artifact_blocked",
        "runtime_verified_artifact_intake_summary=missing_verified_artifact_intake",
        "runtime_verified_artifact_request_package=verified_artifact_requests_open",
        "runtime_verified_artifact_request_candidate=runtime_verified_artifact_request_candidate_passed_temp_created_cleanup_required",
        "runtime_verified_artifact_collection=verified_artifact_collection_open",
        "runtime_verified_artifact_collection_dossier=verified_artifact_collection_dossier_open",
        "runtime_verified_artifact_collection_priority=verified_artifact_collection_priority_open",
        "runtime_sample_signoff_release_gate=missing_sample_signoff_release_evidence",
        "runtime_liaoning_yuanhang_sample_release_gate=missing_liaoning_yuanhang_sample_release_proofs",
        "runtime_liaoning_yuanhang_proof_collection_package=liaoning_yuanhang_original_proof_collection_open",
        "runtime_sop_e2e_master=failed_or_repair_required",
        "runtime_sample_candidates=",
        "runtime_sample_candidate_passed_temp_created_cleanup_required",
        "runtime_sample_candidate_contract=available",
        "runtime_evidence_candidates=",
        "runtime_candidate_passed_temp_created_cleanup_required",
        "runtime_handoff_candidate=runtime_handoff_candidate_passed_temp_created_cleanup_required",
        "runtime_evidence_candidate_contract=available",
        "runtime_handoff_candidate_contract=available",
        "kds_controlled_coverage=available",
        "missing_live_business_inputs=5",
        "demo_substitution=false",
    ]:
        require(phrase in validator_text, f"GFIS validator output missing phrase: {phrase}")
    missing_source_line = next(
        (line for line in validator_output if line.startswith("missing_inputs=")),
        "",
    )
    require("missing_kds_source_paths=" in missing_source_line, "GFIS validator output missing KDS source path count")
    missing_source_count = int(missing_source_line.split("missing_kds_source_paths=", 1)[1].split()[0])
    require(
        0 <= missing_source_count <= 3,
        f"GFIS KDS source path debt exceeded controlled range: {missing_source_count}",
    )

    repair_candidate_gaps = {
        str(call.get("gap"))
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "create_runtime_sop_gfis_actionable_repair_candidate"
        and call.get("result") == "pass"
    }
    require("production_execution" in repair_candidate_gaps, "GFIS runtime evidence missing production_execution repair candidate")
    require("raw_material_plan" in repair_candidate_gaps, "GFIS runtime evidence missing raw_material_plan repair candidate")
    require("raw_material_batch" in repair_candidate_gaps, "GFIS runtime evidence missing raw_material_batch repair candidate")
    require("incoming_quality_inspection" in repair_candidate_gaps, "GFIS runtime evidence missing incoming_quality_inspection repair candidate")
    require("quality_inspection" in repair_candidate_gaps, "GFIS runtime evidence missing quality_inspection repair candidate")
    require("delivery_note" in repair_candidate_gaps, "GFIS runtime evidence missing delivery_note repair candidate")
    require("logistics_record" in repair_candidate_gaps, "GFIS runtime evidence missing logistics_record repair candidate")

    verified_artifact_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_gate"
        and call.get("result") == "pass"
    ]
    require(verified_artifact_calls, "GFIS runtime evidence missing verified artifact gate call")
    verified_gate = verified_artifact_calls[-1]
    require(
        verified_gate.get("gate_status") == "missing_verified_live_artifacts",
        "verified artifact gate must remain missing_verified_live_artifacts",
    )
    require(
        int(verified_gate.get("verified_artifact_count", -1)) == 0,
        "verified artifact gate must report zero verified artifacts after strict source reclassification",
    )
    require(
        int(verified_gate.get("missing_verified_artifact_count", -1)) == 5,
        "verified artifact gate must report five missing verified artifacts",
    )
    gap_objects = {
        str(gap.get("object"))
        for gap in gfis_runtime_evidence.get("runtime_gap_register", [])
        if isinstance(gap, dict)
    }
    require("VerifiedLiveArtifactGate" in gap_objects, "GFIS runtime gap register missing VerifiedLiveArtifactGate")
    for category, item in gfis_kds_coverage.get("live_proof", {}).items():
        for candidate in item.get("candidates", []):
            if not isinstance(candidate, dict):
                continue
            disqualifiers = {str(reason) for reason in candidate.get("disqualifiers", [])}
            if {
                "loop_generated_trace_not_business_artifact",
                "loop_trace_text_not_business_artifact",
                "governance_document_not_business_artifact",
            } & disqualifiers:
                require(
                    candidate.get("artifact_status") != "verified_live_artifact",
                    f"Loop/governance trace must not become verified live artifact: {category}",
                )

    verified_artifact_intake_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_intake_gate"
        and not call.get("scenario")
        and call.get("result") == "pass"
    ]
    require(verified_artifact_intake_calls, "GFIS runtime evidence missing verified artifact intake gate call")
    intake_gate = verified_artifact_intake_calls[-1]
    require(
        intake_gate.get("gate_status") == "missing_verified_artifact_intake",
        "verified artifact intake gate must remain missing_verified_artifact_intake without real artifacts",
    )
    require(
        int(intake_gate.get("intake_artifact_count", -1)) == 0,
        "verified artifact intake gate must report zero KDS-derived intake artifacts after strict source reclassification",
    )
    require(
        int(intake_gate.get("valid_verified_artifact_count", -1)) == 0,
        "verified artifact intake gate must report zero valid verified artifacts",
    )
    require("VerifiedArtifactIntakeGate" in gap_objects, "GFIS runtime gap register missing VerifiedArtifactIntakeGate")
    require("WeakVerifiedArtifactIntakeGate" in gap_objects, "GFIS runtime gap register missing WeakVerifiedArtifactIntakeGate")
    weak_verified_artifact_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_intake_gate"
        and call.get("scenario") == "weak_verified_artifact_rejection"
        and call.get("result") == "pass"
    ]
    require(weak_verified_artifact_calls, "GFIS runtime evidence missing weak verified artifact rejection call")
    weak_verified_artifact_call = weak_verified_artifact_calls[-1]
    require(
        weak_verified_artifact_call.get("gate_status") == "missing_verified_artifact_intake",
        "weak verified artifact rejection must keep intake missing",
    )
    require(
        int(weak_verified_artifact_call.get("valid_verified_artifact_count", -1)) == 0,
        "weak verified artifact rejection must not count valid artifacts",
    )
    require(
        int(weak_verified_artifact_call.get("blocked_artifact_count", -1)) == 1,
        "weak verified artifact rejection must block one artifact",
    )
    weak_reasons = [str(reason) for reason in weak_verified_artifact_call.get("block_reasons", [])]
    require(
        any("source_record_hash" in reason for reason in weak_reasons),
        "weak verified artifact rejection must require source_record_hash",
    )
    require(
        any("source_record_uri" in reason for reason in weak_reasons),
        "weak verified artifact rejection must require source_record_uri",
    )

    verified_artifact_intake_summary_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_intake_summary"
        and call.get("result") == "pass"
    ]
    require(
        verified_artifact_intake_summary_calls,
        "GFIS runtime evidence missing verified artifact intake summary call",
    )
    intake_summary = verified_artifact_intake_summary_calls[-1]
    require(
        intake_summary.get("gate_status") == "missing_verified_artifact_intake",
        "verified artifact intake summary must remain missing_verified_artifact_intake without real artifacts",
    )
    require(
        int(intake_summary.get("ready_category_count", -1)) == 0,
        "verified artifact intake summary must report zero ready categories after strict source reclassification",
    )
    require(
        int(intake_summary.get("missing_category_count", -1)) == 5,
        "verified artifact intake summary must report five missing categories",
    )
    require(
        int(intake_summary.get("blocked_artifact_count", -1)) == 0,
        "verified artifact intake summary must report zero blocked artifacts for empty intake",
    )
    require(
        "VerifiedArtifactIntakeSummary" in gap_objects,
        "GFIS runtime gap register missing VerifiedArtifactIntakeSummary",
    )

    verified_artifact_request_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_request_package"
        and call.get("result") == "pass"
    ]
    require(verified_artifact_request_calls, "GFIS runtime evidence missing verified artifact request package call")
    request_package = verified_artifact_request_calls[-1]
    require(
        request_package.get("gate_status") == "verified_artifact_requests_open",
        "verified artifact request package must remain open while real artifacts are missing",
    )
    require(
        int(request_package.get("request_count", -1)) == 5,
        "verified artifact request package must report five requests",
    )
    require(
        int(request_package.get("open_request_count", -1)) == 5,
        "verified artifact request package must report five open requests",
    )
    require("VerifiedArtifactRequestPackage" in gap_objects, "GFIS runtime gap register missing VerifiedArtifactRequestPackage")

    verified_artifact_request_candidate_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "create_runtime_verified_artifact_request_candidate"
        and call.get("result") == "pass"
    ]
    require(
        verified_artifact_request_candidate_calls,
        "GFIS runtime evidence missing verified artifact request candidate call",
    )
    request_candidate = verified_artifact_request_candidate_calls[-1]
    require(
        request_candidate.get("action_gate") == "runtime_verified_artifact_request_candidate_only",
        "verified artifact request candidate must remain candidate-only",
    )
    require(
        int(request_candidate.get("request_count", -1)) == 5,
        "verified artifact request candidate must report five requests",
    )
    require(
        int(request_candidate.get("open_request_count", -1)) == 5,
        "verified artifact request candidate must report five open requests",
    )
    require(
        "VerifiedArtifactRequestCandidate" in gap_objects,
        "GFIS runtime gap register missing VerifiedArtifactRequestCandidate",
    )

    verified_artifact_collection_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_collection_status"
        and call.get("result") == "pass"
    ]
    require(
        verified_artifact_collection_calls,
        "GFIS runtime evidence missing verified artifact collection status call",
    )
    collection_status = verified_artifact_collection_calls[-1]
    require(
        collection_status.get("collection_status") == "verified_artifact_collection_open",
        "verified artifact collection must remain open without real artifacts",
    )
    require(
        int(collection_status.get("open_request_count", -1)) == 5,
        "verified artifact collection must report five open requests",
    )
    require(
        int(collection_status.get("collected_artifact_count", -1)) == 0,
        "verified artifact collection must report zero collected artifacts",
    )
    require(
        "VerifiedArtifactCollectionStatus" in gap_objects,
        "GFIS runtime gap register missing VerifiedArtifactCollectionStatus",
    )

    verified_artifact_dossier_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_collection_dossier"
        and call.get("result") == "pass"
    ]
    require(
        verified_artifact_dossier_calls,
        "GFIS runtime evidence missing verified artifact collection dossier call",
    )
    collection_dossier = verified_artifact_dossier_calls[-1]
    require(
        int(collection_dossier.get("open_request_count", -1)) == 5,
        "verified artifact collection dossier must report five open requests",
    )
    require(
        int(collection_dossier.get("collected_artifact_count", -1)) == 0,
        "verified artifact collection dossier must count zero collected artifacts after strict source reclassification",
    )
    require(
        "VerifiedArtifactCollectionDossier" in gap_objects,
        "GFIS runtime gap register missing VerifiedArtifactCollectionDossier",
    )

    verified_artifact_priority_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_verified_artifact_collection_priority"
        and call.get("result") == "pass"
    ]
    require(
        verified_artifact_priority_calls,
        "GFIS runtime evidence missing verified artifact collection priority call",
    )
    collection_priority = verified_artifact_priority_calls[-1]
    require(
        collection_priority.get("priority_status") == "verified_artifact_collection_priority_open",
        "verified artifact collection priority must remain open",
    )
    require(
        int(collection_priority.get("open_request_count", -1)) == 5,
        "verified artifact collection priority must report five open requests",
    )
    require(
        collection_priority.get("top_priority_category") in {"live_pod_waes_kds_receipt", "live_sample_signoff_release"},
        "verified artifact collection priority top item must be a real proof-anchor gap",
    )
    priority_business_fields = collection_priority.get("top_priority_business_required_fields", [])
    for field in ["sample_request_id", "customer_signoff_attachment_uri", "production_release_approval_id", "waes_evidence_ref"]:
        require(
            field in priority_business_fields,
            f"verified artifact collection priority missing sample signoff business field: {field}",
        )
    priority_business_hints = collection_priority.get("top_priority_business_trace_hints", [])
    for hint in ["辽宁远航", "23 个样箱", "江西委托工厂", "2026-05 辽宁远航项目报价单", "2026-06 现代精工产线量产计划"]:
        require(
            any(hint in str(business_hint) for business_hint in priority_business_hints),
            f"verified artifact collection priority missing sample signoff business trace hint: {hint}",
        )
    sample_signoff_gate_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_sample_signoff_release_evidence_gate"
        and call.get("result") == "pass"
    ]
    require(
        sample_signoff_gate_calls,
        "GFIS runtime evidence missing sample signoff release evidence gate call",
    )
    sample_signoff_gate = sample_signoff_gate_calls[-1]
    require(
        sample_signoff_gate.get("gate_status") == "missing_sample_signoff_release_evidence",
        "sample signoff release gate must remain missing while original proof is absent",
    )
    require(
        sample_signoff_gate.get("document_trace_allowed_as_live_proof") is False,
        "sample signoff release gate must reject Loop/GPCF document traces as live proof",
    )
    require(
        int(sample_signoff_gate.get("verified_candidate_count", -1)) == 0,
        "sample signoff release gate must report zero verified candidates",
    )
    sample_candidate_refs = sample_signoff_gate.get("candidate_refs", [])
    require(
        int(sample_signoff_gate.get("candidate_count", 0)) >= 12,
        "sample signoff release gate must include KDS and GPC read-only candidate refs",
    )
    require(
        len(sample_candidate_refs) == int(sample_signoff_gate.get("candidate_count", 0)),
        "sample signoff release gate must expose every KDS candidate ref",
    )
    for candidate_ref in sample_candidate_refs:
        if candidate_ref.get("artifact_status") != "verified_live_artifact":
            require(
                candidate_ref.get("exclusion_reason") or candidate_ref.get("missing_verifiers"),
                "sample signoff rejected candidate must explain missing verifier or exclusion",
            )
    related_candidate_refs = [
        candidate_ref
        for candidate_ref in sample_candidate_refs
        if candidate_ref.get("source_scope") == "related_project_readonly"
        or str(candidate_ref.get("kds_path", "")).startswith("related-project-readonly/GPC/")
    ]
    require(
        len(related_candidate_refs) >= 3,
        "sample signoff release gate must expose GPC read-only fixture/retrieval/round candidates",
    )
    for candidate_ref in related_candidate_refs:
        disqualifiers = set(candidate_ref.get("disqualifiers", []))
        require(
            {
                "related_project_readonly_not_kds_live_artifact",
                "related_project_fixture_not_live_artifact",
                "mock_reference_not_live_artifact",
                "local_mirror_not_live_business_record",
                "real_customer_signoff_unavailable",
            }
            & disqualifiers,
            "GPC read-only candidate must be disqualified as fixture/mock/local mirror rather than live proof",
        )
    sample_missing_fields = sample_signoff_gate.get("missing_business_fields", [])
    for field in ["sample_request_id", "customer_signoff_attachment_uri", "production_release_approval_id", "waes_evidence_ref", "kds_backlink_path"]:
        require(
            field in sample_missing_fields,
            f"sample signoff release gate missing business field: {field}",
        )
    require(
        "SampleSignoffReleaseEvidenceGate" in gap_objects,
        "GFIS runtime gap register missing SampleSignoffReleaseEvidenceGate",
    )
    liaoning_gate_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_liaoning_yuanhang_sample_release_gate"
        and call.get("result") == "pass"
    ]
    require(
        liaoning_gate_calls,
        "GFIS runtime evidence missing Liaoning Yuanhang sample release gate call",
    )
    liaoning_gate = liaoning_gate_calls[-1]
    require(
        liaoning_gate.get("gate_status") == "missing_liaoning_yuanhang_sample_release_proofs",
        "Liaoning Yuanhang gate must remain missing while original proof is absent",
    )
    require(
        int(liaoning_gate.get("proof_item_count", -1)) == 4,
        "Liaoning Yuanhang gate must split four proof items",
    )
    require(
        int(liaoning_gate.get("missing_proof_count", -1)) == 4,
        "Liaoning Yuanhang gate must keep four missing proof items",
    )
    require(
        liaoning_gate.get("candidate_refs_are_live_proof") is False,
        "Liaoning Yuanhang gate must reject candidates as live proof",
    )
    require(
        liaoning_gate.get("proof_search_status") == "missing_liaoning_yuanhang_sample_release_proofs",
        "Liaoning Yuanhang proof search status must remain missing",
    )
    require(
        int(liaoning_gate.get("proof_search_candidate_count", -1)) >= 4,
        "Liaoning Yuanhang proof search must expose candidate counts",
    )
    missing_proof_keys = set(liaoning_gate.get("missing_proof_keys", []))
    required_proof_keys = [
        "liaoning_yuanhang_sample_test_record",
        "jiangxi_subcontract_sample_production_record",
        "liaoning_yuanhang_project_quotation",
        "modern_jinggong_mass_production_release",
    ]
    for proof_key in required_proof_keys:
        require(
            proof_key in missing_proof_keys,
            f"Liaoning Yuanhang gate missing proof key: {proof_key}",
        )
    proof_items = liaoning_gate.get("proof_items", [])
    require(isinstance(proof_items, list), "Liaoning Yuanhang gate must include proof item ledger")
    proof_by_key = {item.get("proof_key"): item for item in proof_items if isinstance(item, dict)}
    require(set(proof_by_key) == set(required_proof_keys), "Liaoning Yuanhang proof item ledger keys mismatch")
    proof_candidate_total = 0
    for proof_key in required_proof_keys:
        item = proof_by_key[proof_key]
        require(item.get("status") == "missing_verified_artifact", f"Liaoning Yuanhang proof item must remain missing: {proof_key}")
        require(
            item.get("search_status") in {"candidate_found_not_verified", "missing_input"},
            f"Liaoning Yuanhang proof item must not be verified without original proof: {proof_key}",
        )
        candidate_refs = item.get("candidate_refs", [])
        require(isinstance(candidate_refs, list), f"Liaoning Yuanhang proof item candidates must be a list: {proof_key}")
        require(
            int(item.get("candidate_count", -1)) == len(candidate_refs),
            f"Liaoning Yuanhang proof item candidate_count mismatch: {proof_key}",
        )
        proof_candidate_total += len(candidate_refs)
        for candidate_ref in candidate_refs:
            if candidate_ref.get("artifact_status") != "verified_live_artifact":
                require(
                    candidate_ref.get("exclusion_reason") or candidate_ref.get("missing_verifiers"),
                    f"Liaoning Yuanhang rejected candidate must explain rejection: {proof_key}",
                )
                require(
                    isinstance(candidate_ref.get("missing_anchor_fields"), list),
                    f"Liaoning Yuanhang rejected candidate must expose missing anchor fields: {proof_key}",
                )
    require(
        int(liaoning_gate.get("proof_search_candidate_count", -1)) == proof_candidate_total,
        "Liaoning Yuanhang proof search candidate total mismatch",
    )
    require(
        "LiaoningYuanhangSampleReleaseGate" in gap_objects,
        "GFIS runtime gap register missing LiaoningYuanhangSampleReleaseGate",
    )
    liaoning_collection_package_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_liaoning_yuanhang_proof_collection_package"
        and call.get("result") == "pass"
    ]
    require(
        liaoning_collection_package_calls,
        "GFIS runtime evidence missing Liaoning Yuanhang proof collection package call",
    )
    liaoning_collection_package = liaoning_collection_package_calls[-1]
    require(
        liaoning_collection_package.get("package_status") == "liaoning_yuanhang_original_proof_collection_open",
        "Liaoning Yuanhang proof collection package must remain open",
    )
    require(
        int(liaoning_collection_package.get("request_count", -1)) == 4,
        "Liaoning Yuanhang proof collection package must contain four requests",
    )
    require(
        int(liaoning_collection_package.get("open_request_count", -1)) == 4,
        "Liaoning Yuanhang proof collection package must keep four open requests",
    )
    require(
        int(liaoning_collection_package.get("verified_proof_item_count", -1)) == 0,
        "Liaoning Yuanhang proof collection package must not verify proof items",
    )
    require(
        int(liaoning_collection_package.get("missing_proof_item_count", -1)) == 4,
        "Liaoning Yuanhang proof collection package must keep four missing proof items",
    )
    collection_requests = liaoning_collection_package.get("collection_requests", [])
    require(isinstance(collection_requests, list), "Liaoning Yuanhang proof collection package must include collection requests")
    collection_by_key = {item.get("proof_key"): item for item in collection_requests if isinstance(item, dict)}
    require(set(collection_by_key) == set(required_proof_keys), "Liaoning Yuanhang proof collection package keys mismatch")
    for proof_key, request_item in collection_by_key.items():
        require(
            request_item.get("collection_status") == "original_proof_collection_open",
            f"Liaoning Yuanhang collection request must stay open: {proof_key}",
        )
        require(
            request_item.get("target_system") in {"GPC", "GFIS", "WAES"},
            f"Liaoning Yuanhang collection request target system invalid: {proof_key}",
        )
        require(
            request_item.get("business_trace", {}).get("trace_status") == "business_hint_pending_original_proof",
            f"Liaoning Yuanhang collection request must keep business trace pending proof: {proof_key}",
        )
        for field in ["source_record_uri", "source_record_hash", "kds_backlink_path"]:
            require(
                field in request_item.get("minimum_fields", []),
                f"Liaoning Yuanhang collection request missing proof anchor field: {field}",
            )
        require(
            isinstance(request_item.get("candidate_field_gap_summary"), dict),
            f"Liaoning Yuanhang collection request must expose field gap summary: {proof_key}",
        )
        require(
            isinstance(request_item.get("top_candidate_refs"), list),
            f"Liaoning Yuanhang collection request must expose top candidate refs: {proof_key}",
        )
        require(
            isinstance(request_item.get("missing_fields"), list) and request_item.get("missing_fields"),
            f"Liaoning Yuanhang collection request must expose missing fields: {proof_key}",
        )
        field_summary = request_item.get("candidate_field_gap_summary", {})
        if proof_key == "liaoning_yuanhang_project_quotation":
            require(
                request_item.get("missing_fields") == ["客户确认函"],
                f"Liaoning Yuanhang quotation request must narrow PDF-backed gap to customer confirmation only: {request_item}",
            )
            require(
                "报价附件URI" in field_summary.get("best_candidate_present_anchor_fields", []),
                f"Liaoning Yuanhang quotation best candidate must preserve PDF attachment anchor: {request_item}",
            )
            require(
                request_item.get("weak_acknowledgement_candidate_count", 0) > 0,
                f"Liaoning Yuanhang quotation request must expose weak business acknowledgement refs without verifying them: {request_item}",
            )
            weak_policy = request_item.get("weak_acknowledgement_policy", {})
            require(
                weak_policy.get("may_satisfy_formal_confirmation") is False,
                f"Liaoning Yuanhang weak acknowledgement must not satisfy formal customer confirmation: {request_item}",
            )
            require(
                weak_policy.get("formal_customer_confirmation_still_required") is True,
                f"Liaoning Yuanhang quotation must still require formal customer confirmation: {request_item}",
            )
        if proof_key == "liaoning_yuanhang_sample_test_record":
            require(
                "报价/" not in str(field_summary.get("best_candidate_kds_path", "")),
                f"Liaoning Yuanhang sample-test best candidate must not be a quotation document: {request_item}",
            )
            require(
                set(request_item.get("missing_fields", [])) >= {"测试记录编号", "测试签收附件", "客户反馈原件", "客户签收单号"},
                f"Liaoning Yuanhang sample-test request must keep formal test anchors missing: {request_item}",
            )
        if proof_key == "modern_jinggong_mass_production_release":
            require(
                "wiki/sources/_llmwiki_canonical/工业绿链/项目/葛化/" in str(field_summary.get("best_candidate_kds_path", "")),
                f"Modern Jinggong release best candidate must come from Gehua/Modern Jinggong controlled sources: {request_item}",
            )
            require(
                request_item.get("formal_missing_reason_refs") or field_summary.get("formal_missing_reason_refs"),
                f"Modern Jinggong release request must expose KDS formal missing reason refs: {request_item}",
            )
            require(
                set(request_item.get("missing_fields", [])) >= {"转量产批准单号", "放行批准附件", "量产计划编号", "WAES evidence ref"},
                f"Modern Jinggong release must keep all formal release anchors missing: {request_item}",
            )
    require(
        "LiaoningYuanhangProofCollectionPackage" in gap_objects,
        "GFIS runtime gap register missing LiaoningYuanhangProofCollectionPackage",
    )

    sop_master_calls = [
        call
        for call in gfis_runtime_evidence.get("runtime_calls", [])
        if isinstance(call, dict)
        and call.get("api") == "get_runtime_sop_e2e_master_status"
        and call.get("result") == "pass"
    ]
    require(sop_master_calls, "GFIS runtime evidence missing SOP E2E Master status call")
    sop_master = sop_master_calls[-1]
    require(
        sop_master.get("sop_e2e_master") == "failed_or_repair_required",
        "SOP E2E Master must remain failed_or_repair_required until real artifacts are collected",
    )
    require(
        sop_master.get("runtime_sop_e2e") == "repair_required",
        "runtime SOP E2E must remain repair_required",
    )
    require(
        sop_master.get("demo_e2e_status") == "pass_demo_only",
        "Demo E2E must remain pass_demo_only",
    )
    require(
        int(sop_master.get("open_request_count", -1)) == 5,
        "SOP E2E Master must report five open artifact requests",
    )
    require(
        int(sop_master.get("collected_artifact_count", -1)) == 0,
        "SOP E2E Master must report zero collected artifacts",
    )
    require(
        int(sop_master.get("verified_artifact_count", -1)) == 0,
        "SOP E2E Master must report zero verified artifacts after strict source reclassification",
    )
    require("SOPE2EMasterStatus" in gap_objects, "GFIS runtime gap register missing SOPE2EMasterStatus")

    for phrase in [
        "repair_required",
        "GFIS 运行层",
        "Demo",
        "79",
    ]:
        require(phrase in control + "\n" + status + "\n" + loop_state, f"GPCF control plane missing phrase: {phrase}")

    forbidden_claims = [
        "GFIS runtime SOP E2E=pass",
        "GFIS 运行层 SOP E2E 已完成",
        "GFIS accepted",
        "GFIS integrated",
        "project_group_score=100",
    ]
    combined = doc + "\n" + control + "\n" + status + "\n" + loop_state
    for claim in forbidden_claims:
        require(claim not in combined, f"forbidden completion claim found: {claim}")

    print(
        "loop_engineering_integrity=pass "
        "gfis_subject=runtime_layer "
        "demo_substitution=false "
        "runtime_sop_e2e=repair_required "
        "project_group_score=78"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
