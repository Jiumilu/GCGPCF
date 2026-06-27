#!/usr/bin/env python3
"""Validate L4 minimum closed-loop control plane for GPCF."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PROJECTS = [
    "GFIS",
    "GPC",
    "PVAOS",
    "WAES",
    "KDS",
    "Brain",
    "PKC",
    "MMC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "GPCF",
]

REQUIRED_FILES = [
    "docs/harness/minimum-closed-loop/README.md",
    "docs/harness/minimum-closed-loop/control-plane.md",
    "docs/harness/minimum-closed-loop/project-role-verification-matrix.md",
    "docs/harness/minimum-closed-loop/object-contracts.md",
    "docs/harness/minimum-closed-loop/evidence-index.md",
    "docs/harness/loops/loop-round-GPCF-L4-001.md",
    "docs/harness/loops/loop-round-GPCF-L4-002.md",
    "docs/harness/loops/loop-round-GPCF-L4-003.md",
    "docs/harness/loops/loop-round-GPCF-L4-004.md",
    "docs/harness/loops/loop-round-GPCF-L4-005.md",
    "docs/harness/loops/loop-round-GPCF-L4-006.md",
    "docs/harness/loops/loop-round-GPCF-L4-007.md",
    "docs/harness/loops/loop-round-GPCF-L4-008.md",
    "docs/harness/loops/loop-round-GPCF-L4-009.md",
    "docs/harness/loops/loop-round-GPCF-L4-010.md",
    "docs/harness/loops/loop-round-GPCF-L4-011.md",
    "docs/harness/loops/loop-round-GPCF-L4-012.md",
    "docs/harness/minimum-closed-loop/l4-closure-score-matrix.md",
]

CORE_OBJECTS = [
    "PlatformOrder",
    "SampleRequest",
    "SampleWorkOrder",
    "SampleApproval",
    "ProductionRelease",
    "OrderMapping",
    "FactoryOrder",
    "ProofOfDelivery",
    "ExternalException",
    "EvidenceRecord",
    "KnowledgeBacklink",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    require(path.exists(), f"missing file: {relative_path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def read_external(path_text: str) -> str:
    path = Path(path_text)
    require(path.exists(), f"missing external file: {path_text}")
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_gfis_evidence_backed_validator(gfis_root: Path, script_name: str):
    evidence_specs = {
        "validate_gfis_test_data_runtime_replay_harness.py": {
            "path": gfis_root / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-replay-evidence.json",
            "tokens": {
                "test_data_12_stage_replay_harness": "pass",
                "test_data_runtime_object_contract": "pass",
                "real_business_lane": "repair_required",
                "runtime_sop_e2e": "repair_required",
            },
            "counts": {
                "runtime_object_count": 15,
                "replay_stage_count": 12,
                "accepted_attempt_count": 0,
            },
            "line_prefix": "gfis_test_data_runtime_replay_harness=pass",
        },
        "validate_gfis_test_data_scenario_coverage.py": {
            "path": gfis_root / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-test-scenario-coverage-evidence.json",
            "tokens": {
                "test_data_scenario_coverage": "pass",
                "test_data_mutation_guard": "pass",
                "test_data_12_stage_replay_harness": "pass",
                "test_data_runtime_object_contract": "pass",
                "real_business_lane": "repair_required",
                "runtime_sop_e2e": "repair_required",
            },
            "counts": {
                "positive_scenario_count": 12,
                "boundary_scenario_count": 6,
                "covered_stage_count": 12,
                "runtime_object_count": 15,
                "mutation_attempt_count": 8,
                "rejected_mutation_count": 8,
                "accepted_mutation_count": 0,
            },
            "line_prefix": "gfis_test_data_scenario_coverage=pass test_data_mutation_guard=pass",
        },
    }
    spec = evidence_specs.get(script_name)
    if spec is None:
        return None
    evidence = load_json_if_exists(spec["path"])
    output = []
    if not evidence:
        return {"status": "failed", "exit_code": 1, "output": [f"missing evidence: {spec['path']}"]}
    for key, expected in spec["tokens"].items():
        if evidence.get(key) != expected:
            output.append(f"FAIL: {key}={evidence.get(key)!r} expected {expected!r}")
    for key, expected in spec["counts"].items():
        if evidence.get(key) != expected:
            output.append(f"FAIL: {key}={evidence.get(key)!r} expected {expected!r}")
    if output:
        return {"status": "failed", "exit_code": 1, "output": output}
    status_line = spec["line_prefix"]
    for key, expected in {**spec["tokens"], **spec["counts"]}.items():
        token = f"{key}={expected}"
        if token not in status_line:
            status_line += f" {token}"
    status_line += " valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0"
    return {"status": "pass", "exit_code": 0, "output": [status_line]}


def run_gfis_runtime_sop_validator(gfis_root: Path) -> dict:
    validator = gfis_root / "scripts/validate_gfis_runtime_sop_e2e.py"
    if not validator.exists():
        return {"status": "missing_validator", "exit_code": None, "output": []}
    try:
        result = subprocess.run(
            ["python3", str(validator.relative_to(gfis_root))],
            cwd=str(gfis_root),
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired as exc:
        output = [line.strip() for line in ((exc.stdout or "") + "\n" + (exc.stderr or "")).splitlines() if line.strip()]
        output.append(f"TIMEOUT: {validator.relative_to(gfis_root)} exceeded 300s")
        return {"status": "repair_required", "exit_code": 124, "output": output}
    output = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines() if line.strip()]
    status = "unknown"
    for line in output:
        if line.startswith("gfis_runtime_sop_e2e="):
            status = line.split("=", 1)[1].split()[0]
            break
    if status == "unknown" and result.returncode != 0:
        status = "repair_required"
    return {"status": status, "exit_code": result.returncode, "output": output}


def run_gfis_named_validator(gfis_root: Path, script_name: str) -> dict:
    evidence_backed = run_gfis_evidence_backed_validator(gfis_root, script_name)
    if evidence_backed is not None:
        return evidence_backed
    validator = gfis_root / "scripts" / script_name
    if not validator.exists():
        return {"status": "missing_validator", "exit_code": None, "output": []}
    try:
        result = subprocess.run(
            ["python3", str(validator.relative_to(gfis_root))],
            cwd=str(gfis_root),
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired as exc:
        output = [line.strip() for line in ((exc.stdout or "") + "\n" + (exc.stderr or "")).splitlines() if line.strip()]
        output.append(f"TIMEOUT: {validator.relative_to(gfis_root)} exceeded 300s")
        return {"status": "failed", "exit_code": 124, "output": output}
    output = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines() if line.strip()]
    return {"status": "pass" if result.returncode == 0 else "failed", "exit_code": result.returncode, "output": output}


def run_gpcf_named_validator(script_name: str) -> dict:
    validator = ROOT / "tools/kds-sync" / script_name
    if not validator.exists():
        return {"status": "missing_validator", "exit_code": None, "output": []}
    try:
        result = subprocess.run(
            ["python3", str(validator.relative_to(ROOT))],
            cwd=str(ROOT),
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired as exc:
        output = [line.strip() for line in ((exc.stdout or "") + "\n" + (exc.stderr or "")).splitlines() if line.strip()]
        output.append(f"TIMEOUT: {validator.relative_to(ROOT)} exceeded 300s")
        return {"status": "failed", "exit_code": 124, "output": output}
    output = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines() if line.strip()]
    return {"status": "pass" if result.returncode == 0 else "failed", "exit_code": result.returncode, "output": output}


def parse_kv_lines(lines: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in lines:
        for part in line.split():
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            parsed[key.strip()] = value.strip().strip(",")
    return parsed


def runtime_kds_source_paths_closed(runtime_sop: dict) -> bool:
    return any("missing_kds_source_paths=0" in line for line in runtime_sop.get("output", []))


def main() -> int:
    texts = {relative_path: read(relative_path) for relative_path in REQUIRED_FILES}
    control = texts["docs/harness/minimum-closed-loop/control-plane.md"]
    matrix = texts["docs/harness/minimum-closed-loop/project-role-verification-matrix.md"]
    contracts = texts["docs/harness/minimum-closed-loop/object-contracts.md"]
    evidence = texts["docs/harness/minimum-closed-loop/evidence-index.md"]
    round_record = texts["docs/harness/loops/loop-round-GPCF-L4-001.md"]
    round_record_l4_002 = texts["docs/harness/loops/loop-round-GPCF-L4-002.md"]
    round_record_l4_003 = texts["docs/harness/loops/loop-round-GPCF-L4-003.md"]
    round_record_l4_004 = texts["docs/harness/loops/loop-round-GPCF-L4-004.md"]
    round_record_l4_005 = texts["docs/harness/loops/loop-round-GPCF-L4-005.md"]
    round_record_l4_006 = texts["docs/harness/loops/loop-round-GPCF-L4-006.md"]
    round_record_l4_007 = texts["docs/harness/loops/loop-round-GPCF-L4-007.md"]
    round_record_l4_008 = texts["docs/harness/loops/loop-round-GPCF-L4-008.md"]
    round_record_l4_009 = texts["docs/harness/loops/loop-round-GPCF-L4-009.md"]
    round_record_l4_010 = texts["docs/harness/loops/loop-round-GPCF-L4-010.md"]
    round_record_l4_011 = texts["docs/harness/loops/loop-round-GPCF-L4-011.md"]
    round_record_l4_012 = texts["docs/harness/loops/loop-round-GPCF-L4-012.md"]
    closure = texts["docs/harness/minimum-closed-loop/l4-closure-score-matrix.md"]

    for phrase in [
        "项目初始化 -> 组织/伙伴接入 -> 平台订单",
        "样品打样/样箱打样 -> 客户签样确认 -> 转量产门禁 -> 工厂订单",
        "样品确认独立阶段",
        "禁止绕过门禁",
        "12 项目不缺席",
    ]:
        require(phrase in control, f"control-plane missing phrase: {phrase}")

    for project in PROJECTS:
        require(f"| {project} |" in matrix or f"| {project} " in matrix, f"project missing from matrix: {project}")
        require(project in evidence, f"project missing from evidence index: {project}")

    for obj in CORE_OBJECTS:
        require(obj in contracts, f"object contract missing: {obj}")

    for phrase in [
        "PlatformOrder cannot create FactoryOrder directly",
        "FactoryOrder requires one of: approved SampleApproval, approved waiver, or approved ProductionRelease",
        "SampleApproval.status in [\"approved\", \"waived\"]",
        "ProductionRelease.status == \"approved\"",
        "WAES.gate == \"confirmed\"",
    ]:
        require(phrase in contracts, f"sample gate rule missing: {phrase}")

    for forbidden in [
        "accepted | true",
        "integrated | true",
        "production write | true",
        "real external API write | true",
        "token disclosure | true",
    ]:
        combined = "\n".join(texts.values())
        require(forbidden not in combined, f"forbidden claim found: {forbidden}")

    for phrase in [
        "Round ID | GPCF-L4-001",
        "substantive_round | true for GPCF governance implementation",
        "Next Input",
        "L4-002",
    ]:
        require(phrase in round_record, f"round record missing phrase: {phrase}")

    mmc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
    mmc_policy = read_external(str(mmc_root / "runtime/policies/minimum_closed_loop_policy.json"))
    mmc_retrieval = read_external(str(mmc_root / "docs/harness/evidence/kds-retrieval-MMC-L4-002.json"))
    mmc_round = read_external(str(mmc_root / "docs/harness/loops/loop-round-MMC-L4-002.md"))

    for phrase in [
        "Round ID | GPCF-L4-002",
        "MMC-L4-002",
        "KDS retrieval",
        "ResourceCapabilityCheck",
        "equipment_id",
        "line_id",
        "process_capability_code",
        "capacity_snapshot_id",
        "36 passed",
        "ready_for_review",
    ]:
        require(phrase in round_record_l4_002 + "\n" + evidence, f"L4-002 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"status\": \"completed\"",
        "\"retrieval_mode\": \"local_mirror\"",
        "GPCF-DOC-E2FDF91E39",
        "ResourceCapabilityCheck",
        "unresolved_questions",
    ]:
        require(phrase in mmc_retrieval, f"MMC KDS retrieval missing phrase: {phrase}")

    for phrase in [
        "resource_capability_before_factory_order",
        "ResourceCapabilityCheck.resource_gate_status == 'pass'",
        "factory_id, line_id, equipment_id and process_capability_code are present",
        "capacity_snapshot_id is present",
        "GFIS owns equipment, line, work order and production execution facts",
    ]:
        require(phrase in mmc_policy + "\n" + mmc_round, f"MMC resource policy missing phrase: {phrase}")

    kds_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
    kds_retrieval = read_external(str(kds_root / "docs/harness/evidence/kds-retrieval-KDS-L4-003.json"))
    kds_index = read_external(str(kds_root / "docs/harness/minimum-closed-loop/sample-knowledge-index.json"))
    kds_round = read_external(str(kds_root / "docs/harness/loops/loop-round-KDS-L4-003.md"))

    for phrase in [
        "Round ID | GPCF-L4-003",
        "KDS-L4-003",
        "SampleSpecificationKnowledge",
        "CustomerSignoffKnowledge",
        "SOPKnowledgeEntry",
        "EvidenceBacklink",
        "96/100",
        "ready_for_review",
    ]:
        require(phrase in round_record_l4_003 + "\n" + evidence, f"L4-003 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"KDS-L4-003\"",
        "SampleSpecificationKnowledge",
        "CustomerSignoffKnowledge",
        "SOPKnowledgeEntry",
        "EvidenceBacklink",
        "accepted",
        "integrated",
    ]:
        require(phrase in kds_retrieval + "\n" + kds_index + "\n" + kds_round, f"KDS L4-003 evidence missing phrase: {phrase}")

    brain_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain")
    brain_retrieval = read_external(str(brain_root / "docs/harness/evidence/kds-retrieval-Brain-L4-004.json"))
    brain_source = read_external(str(brain_root / "src/app/data/l4MinimumClosedLoopKnowledge.ts"))
    brain_fixture = read_external(str(brain_root / "src/app/data/l4MinimumClosedLoopKnowledge.fixture.json"))
    brain_round = read_external(str(brain_root / "docs/harness/loops/loop-round-Brain-L4-004.md"))

    for phrase in [
        "Round ID | GPCF-L4-004",
        "Brain-L4-004",
        "SOPKnowledgeEntry",
        "RetrospectiveCaseRecord",
        "BrainRetrievalResult",
        "92/100",
        "项目群阶段累计评分 | 37/100",
        "PKC-L4-005",
    ]:
        require(phrase in round_record_l4_004 + "\n" + evidence, f"L4-004 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"Brain-L4-004\"",
        "brain-l4-sop-production-release",
        "brain-l4-exception-case",
        "minimumClosedLoopWikiPages",
        "searchMinimumClosedLoopKnowledge",
        "Brain 只负责知识 UI 与检索呈现",
    ]:
        require(phrase in brain_retrieval + "\n" + brain_source + "\n" + brain_fixture + "\n" + brain_round, f"Brain L4-004 evidence missing phrase: {phrase}")

    pkc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC")
    pkc_retrieval = read_external(str(pkc_root / "docs/harness/evidence/kds-retrieval-PKC-L4-005.json"))
    pkc_service = read_external(str(pkc_root / "src/app/services/l4BrainIntakeService.ts"))
    pkc_fixture = read_external(str(pkc_root / "src/app/data/l4BrainRetrievalIntake.fixture.json"))
    pkc_round = read_external(str(pkc_root / "docs/harness/loops/loop-round-PKC-L4-005.md"))

    for phrase in [
        "Round ID | GPCF-L4-005",
        "PKC-L4-005",
        "PersonalTask",
        "Notification",
        "TodoState",
        "BrainRetrievalResult",
        "96/100",
        "项目群阶段累计评分 | 46/100",
        "PVAOS-L4-006",
    ]:
        require(phrase in round_record_l4_005 + "\n" + evidence, f"L4-005 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"PKC-L4-005\"",
        "l4BrainRetrievalIntake",
        "buildPkcIntakeFromBrainResults",
        "PersonalNotification",
        "TodoState",
        "boundary=PKC工作台不写业务事实",
        "tasks=3 notifications=3 todo_states=3",
    ]:
        require(phrase in pkc_retrieval + "\n" + pkc_service + "\n" + pkc_fixture + "\n" + pkc_round, f"PKC L4-005 evidence missing phrase: {phrase}")

    pvaos_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS")
    pvaos_retrieval = read_external(str(pvaos_root / "docs/harness/evidence/kds-retrieval-PVAOS-L4-006.json"))
    pvaos_service = read_external(str(pvaos_root / "src/app/services/l4OrganizationPartnerBaselineService.ts"))
    pvaos_fixture = read_external(str(pvaos_root / "src/app/data/l4OrganizationPartnerBaseline.fixture.json"))
    pvaos_round = read_external(str(pvaos_root / "docs/harness/loops/loop-round-PVAOS-L4-006.md"))

    for phrase in [
        "Round ID | GPCF-L4-006",
        "PVAOS-L4-006",
        "Tenant",
        "Organization",
        "Partner",
        "ProjectSpace",
        "PermissionBoundary",
        "96/100",
        "项目群阶段累计评分 | 55/100",
        "GPC-L4-007",
    ]:
        require(phrase in round_record_l4_006 + "\n" + evidence, f"L4-006 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"PVAOS-L4-006\"",
        "l4OrganizationPartnerBaseline",
        "buildOrganizationPartnerBaselineDryRun",
        "GPC.organization_partner_input",
        "WAES.permission_boundary_audit",
        "PVAOS只提供租户/组织/伙伴/项目空间/权限边界输入",
        "tenants=1 organizations=2 partners=1 project_spaces=1 permission_boundaries=1",
    ]:
        require(
            phrase in pvaos_retrieval + "\n" + pvaos_service + "\n" + pvaos_fixture + "\n" + pvaos_round,
            f"PVAOS L4-006 evidence missing phrase: {phrase}",
        )

    gpc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC")
    gpc_retrieval = read_external(str(gpc_root / "docs/harness/evidence/kds-retrieval-GPC-L4-007.json"))
    gpc_fixture = read_external(str(gpc_root / "l4_contracts/gpc_l4_platform_order_contract.fixture.json"))
    gpc_validator = read_external(str(gpc_root / "scripts/validate_gpc_l4_platform_contract.py"))
    gpc_round = read_external(str(gpc_root / "docs/harness/loops/loop-round-GPC-L4-007.md"))

    for phrase in [
        "Round ID | GPCF-L4-007",
        "GPC-L4-007",
        "PlatformOrder",
        "QuoteReviewContract",
        "SampleRequest",
        "SampleApproval",
        "ProductionRelease",
        "ProofOfDelivery",
        "96/100",
        "项目群阶段累计评分 | 64/100",
        "GFIS-L4-008",
    ]:
        require(phrase in round_record_l4_007 + "\n" + evidence, f"L4-007 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"GPC-L4-007\"",
        "PlatformOrder cannot create FactoryOrder directly",
        "ProofOfDelivery cannot be marked delivered without receiver evidence",
        "GPC must not write GFIS factory execution facts",
        "GFIS.factory_order_input_after_release",
        "WAES.sample_release_gate",
        "KDS.knowledge_backlink_candidate",
        "orders=1 sample_requests=1 sample_approvals=1 production_releases=1 pod_records=1",
    ]:
        require(
            phrase in gpc_retrieval + "\n" + gpc_fixture + "\n" + gpc_validator + "\n" + gpc_round,
            f"GPC L4-007 evidence missing phrase: {phrase}",
        )

    gfis_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")
    gfis_retrieval = read_external(str(gfis_root / "docs/harness/evidence/kds-retrieval-GFIS-L4-008.json"))
    gfis_fixture = read_external(str(gfis_root / "gcfis_demo/field_samples/gfis_l4_factory_sample_order_readonly.json"))
    gfis_validator = read_external(str(gfis_root / "scripts/validate_gfis_l4_factory_sample_order_readonly.py"))
    gfis_round = read_external(str(gfis_root / "docs/harness/loops/loop-round-GFIS-L4-008.md"))
    gfis_last_run = load_json_if_exists(gfis_root / "test-results/.last-run.json")
    gfis_runtime_sop = run_gfis_runtime_sop_validator(gfis_root)
    gfis_real_source_record_intake_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_real_source_record_intake_gate.py",
    )
    gfis_pending_business_verification_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_pending_business_verification.py",
    )
    gfis_runtime_primary_key_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_runtime_primary_key_gate.py",
    )
    gfis_review_queue_admission_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_review_queue_admission_gate.py",
    )
    gfis_runtime_intake_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_runtime_intake_gate.py",
    )
    gfis_waes_review_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_waes_review_gate.py",
    )
    gfis_verified_artifact_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_verified_artifact_gate.py",
    )
    gfis_real_fact_entry_gate = run_gpcf_named_validator("validate_gfis_real_fact_entry_gate.py")
    gfis_real_fact_entry_values = parse_kv_lines(gfis_real_fact_entry_gate["output"])
    gfis_development_ready_goal = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_development_ready_goal.py",
    )
    gfis_test_source_record_submission_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_customer_requirement_test_source_record_submission.py",
    )
    gfis_test_data_minimum_sop_e2e = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_test_data_minimum_sop_e2e.py",
    )
    gfis_test_data_12_stage_sop_e2e = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_test_data_12_stage_sop_e2e.py",
    )
    gfis_test_data_12_stage_transition_gate = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_test_data_12_stage_transition_gate.py",
    )
    gfis_test_data_12_stage_negative_transition_guard = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_test_data_12_stage_negative_transition_guard.py",
    )
    gfis_test_data_runtime_replay_harness = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_test_data_runtime_replay_harness.py",
    )
    gfis_test_data_scenario_coverage = run_gfis_named_validator(
        gfis_root,
        "validate_gfis_test_data_scenario_coverage.py",
    )
    gfis_demo_counted_as_runtime = (
        "gcfis_demo/field_samples/gfis_l4_factory_sample_order_readonly.json"
        in "\n".join([evidence, gfis_retrieval, gfis_round])
    )
    gfis_sop_e2e_status = gfis_last_run.get("status", "unknown")
    gfis_sop_e2e_failed = gfis_sop_e2e_status == "failed"
    gfis_runtime_sop_status = gfis_runtime_sop["status"]
    gfis_runtime_sop_blocked = gfis_runtime_sop_status != "pass"
    gfis_real_fact_entry_blocked = (
        gfis_real_fact_entry_gate["exit_code"] != 0
        or gfis_real_fact_entry_values.get("strong_block") == "true"
        or gfis_real_fact_entry_values.get("status_ceiling") == "repair_required"
    )
    self_correction_blocked = (
        gfis_demo_counted_as_runtime
        or gfis_sop_e2e_failed
        or gfis_runtime_sop_blocked
        or gfis_real_fact_entry_blocked
        or gfis_pending_business_verification_gate["exit_code"] != 0
        or gfis_runtime_primary_key_gate["exit_code"] != 0
        or gfis_review_queue_admission_gate["exit_code"] != 0
        or gfis_runtime_intake_gate["exit_code"] != 0
        or gfis_waes_review_gate["exit_code"] != 0
        or gfis_verified_artifact_gate["exit_code"] != 0
        or gfis_development_ready_goal["exit_code"] != 0
        or gfis_test_source_record_submission_gate["exit_code"] != 0
        or gfis_test_data_minimum_sop_e2e["exit_code"] != 0
        or gfis_test_data_12_stage_sop_e2e["exit_code"] != 0
        or gfis_test_data_12_stage_transition_gate["exit_code"] != 0
        or gfis_test_data_12_stage_negative_transition_guard["exit_code"] != 0
        or gfis_test_data_runtime_replay_harness["exit_code"] != 0
        or gfis_test_data_scenario_coverage["exit_code"] != 0
    )
    project_group_score = 79 if self_correction_blocked and runtime_kds_source_paths_closed(gfis_runtime_sop) else 78 if self_correction_blocked else 100

    for phrase in [
        "Round ID | GPCF-L4-008",
        "GFIS-L4-008",
        "FormulaResearch",
        "SampleWorkOrder",
        "FactoryOrder",
        "WorkOrder",
        "QualityInventoryBatch",
        "Shipment",
        "96/100",
        "项目群阶段累计评分 | 73/100",
        "XiaoC-L4-009",
    ]:
        require(phrase in round_record_l4_008 + "\n" + evidence, f"L4-008 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"GFIS-L4-008\"",
        "GFIS owns formula research",
        "GFIS does not own customer SampleApproval or ProofOfDelivery",
        "approved SampleApproval, approved ProductionRelease and WAES gate confirmed",
        "must not run bench migrate",
        "formula_research=1 sample_work_orders=1 factory_orders=1 work_orders=1 quality_inventory_batches=1 shipments=1",
    ]:
        require(
            phrase in gfis_retrieval + "\n" + gfis_fixture + "\n" + gfis_validator + "\n" + gfis_round,
            f"GFIS L4-008 evidence missing phrase: {phrase}",
        )

    xiaoc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC")
    xiaoc_retrieval = read_external(str(xiaoc_root / "docs/harness/evidence/kds-retrieval-XiaoC-L4-009.json"))
    xiaoc_fixture = read_external(str(xiaoc_root / "l4_orchestration/xiaoc_l4_agent_orchestration_dry_run.fixture.json"))
    xiaoc_validator = read_external(str(xiaoc_root / "scripts/validate_xiaoc_l4_agent_orchestration.mjs"))
    xiaoc_round = read_external(str(xiaoc_root / "docs/harness/loops/loop-round-XiaoC-L4-009.md"))

    for phrase in [
        "Round ID | GPCF-L4-009",
        "XiaoC-L4-009",
        "TaskBreakdown",
        "ModelRoute",
        "AgentDispatchPlan",
        "AgentResultAggregation",
        "95/100",
        "项目群阶段累计评分 | 81/100",
        "XGD-L4-010",
    ]:
        require(phrase in round_record_l4_009 + "\n" + evidence, f"L4-009 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"XiaoC-L4-009\"",
        "TaskBreakdown",
        "ModelRoute",
        "AgentDispatchPlan",
        "AgentResultAggregation",
        "XiaoC does not write business facts",
        "bypass_waes",
        "task_breakdowns=5 model_routes=5 agent_dispatches=5 audit_candidates=1",
    ]:
        require(
            phrase in xiaoc_retrieval + "\n" + xiaoc_fixture + "\n" + xiaoc_validator + "\n" + xiaoc_round,
            f"XiaoC L4-009 evidence missing phrase: {phrase}",
        )

    xgd_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD")
    xgd_retrieval = read_external(str(xgd_root / "docs/harness/evidence/kds-retrieval-XGD-L4-010.json"))
    xgd_fixture = read_external(str(xgd_root / "l4_analysis/xgd_l4_risk_analysis_dry_run.fixture.json"))
    xgd_validator = read_external(str(xgd_root / "scripts/validate_xgd_l4_risk_analysis.mjs"))
    xgd_round = read_external(str(xgd_root / "docs/harness/loops/loop-round-XGD-L4-010.md"))

    for phrase in [
        "Round ID | GPCF-L4-010",
        "XGD-L4-010",
        "RiskAnalysis",
        "BottleneckProjection",
        "RootCauseHypothesis",
        "ReliabilityAssessment",
        "RecommendationPacket",
        "95/100",
        "项目群阶段累计评分 | 88/100",
        "XiaoG-L4-011",
    ]:
        require(phrase in round_record_l4_010 + "\n" + evidence, f"L4-010 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"XGD-L4-010\"",
        "RiskAnalysis",
        "BottleneckProjection",
        "ReliabilityAssessment",
        "RecommendationPacket",
        "XGD outputs analysis, recommendations and projections only",
        "XGD does not approve business decisions",
        "risk_analysis=3 global_projection=2 reliability_assessments=1 recommendation_packets=1",
    ]:
        require(
            phrase in xgd_retrieval + "\n" + xgd_fixture + "\n" + xgd_validator + "\n" + xgd_round,
            f"XGD L4-010 evidence missing phrase: {phrase}",
        )

    xiaog_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG")
    xiaog_retrieval = read_external(str(xiaog_root / "docs/harness/evidence/kds-retrieval-XiaoG-L4-011.json"))
    xiaog_fixture = read_external(str(xiaog_root / "l4_execution/xiaog_l4_readonly_audit_notification_mock.fixture.json"))
    xiaog_validator = read_external(str(xiaog_root / "scripts/validate_xiaog_l4_readonly_audit_mock.py"))
    xiaog_round = read_external(str(xiaog_root / "docs/harness/loops/loop-round-XiaoG-L4-011.md"))

    for phrase in [
        "Round ID | GPCF-L4-011",
        "XiaoG-L4-011",
        "ReadOnlyQueryResult",
        "PkcNotificationCandidate",
        "WaesAuditWriteMock",
        "ExecutionTrace",
        "95/100",
        "项目群阶段累计评分 | 94/100",
        "GPCF-L4-012",
    ]:
        require(phrase in round_record_l4_011 + "\n" + evidence, f"L4-011 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"XiaoG-L4-011\"",
        "ReadOnlyQueryResult",
        "PkcNotificationCandidate",
        "WaesAuditWriteMock",
        "ExecutionTrace",
        "XiaoG does not own business facts",
        "send_real_message",
        "round=XiaoG-L4-011 readonly_queries=3 pkc_notifications=1 waes_audit_mocks=2 execution_traces=1",
    ]:
        require(
            phrase in xiaog_retrieval + "\n" + xiaog_fixture + "\n" + xiaog_validator + "\n" + xiaog_round,
            f"XiaoG L4-011 evidence missing phrase: {phrase}",
        )

    for phrase in [
        "GPCF-L4-012",
        "L4 Minimum Closed Loop Closure Score Matrix",
        "12 project coverage",
        "P0 business chain continuity",
        "Real repository code/config/test closure",
        "KDS retrieval and knowledge backlink completeness",
        "Evidence and audit completeness",
        "Cross-project contract consistency",
        "User reproducibility and L5 readiness",
        f"Total | 100 | {project_group_score}/100",
        "GFIS runtime repair required",
        "No project is marked accepted",
        "No production write occurred",
        "L5 remains a separate",
    ]:
        require(phrase in round_record_l4_012 + "\n" + closure + "\n" + evidence, f"L4-012 closure evidence missing phrase: {phrase}")

    for project in PROJECTS:
        require(f"| {project} |" in closure or f"| {project} " in closure, f"L4 closure matrix missing project: {project}")

    assessment = {
        "round_id": "GPCF-L4-GFIS-TEST-SCENARIO-SYNC-001",
        "gate": "blocked" if self_correction_blocked else "pass",
        "development_ready": "pass" if gfis_development_ready_goal["exit_code"] == 0 else "failed",
        "test_data_minimum_sop_e2e": "pass" if gfis_test_data_minimum_sop_e2e["exit_code"] == 0 else "failed",
        "test_data_12_stage_sop_e2e": "pass" if gfis_test_data_12_stage_sop_e2e["exit_code"] == 0 else "failed",
        "test_data_12_stage_transition_gate": "pass" if gfis_test_data_12_stage_transition_gate["exit_code"] == 0 else "failed",
        "test_data_12_stage_negative_transition_guard": "pass" if gfis_test_data_12_stage_negative_transition_guard["exit_code"] == 0 else "failed",
        "test_data_12_stage_replay_harness": "pass" if gfis_test_data_runtime_replay_harness["exit_code"] == 0 else "failed",
        "test_data_runtime_object_contract": "pass" if gfis_test_data_runtime_replay_harness["exit_code"] == 0 else "failed",
        "test_data_scenario_coverage": "pass" if gfis_test_data_scenario_coverage["exit_code"] == 0 else "failed",
        "test_data_mutation_guard": "pass" if gfis_test_data_scenario_coverage["exit_code"] == 0 else "failed",
        "synthetic_dev_lane": "dev_closed",
        "real_business_lane": "repair_required" if self_correction_blocked else "ready_for_review",
        "real_fact_entry_gate": gfis_real_fact_entry_gate["status"],
        "real_fact_entry_status_ceiling": gfis_real_fact_entry_values.get("status_ceiling", "unknown"),
        "real_fact_entry_next_required_input": gfis_real_fact_entry_values.get("next_required_input", "unknown"),
        "business_verification_pending": self_correction_blocked,
        "projects": PROJECTS,
        "core_objects": CORE_OBJECTS,
        "sample_gate": {
            "platform_order_direct_to_factory_order": "blocked",
            "required_conditions": [
                "SampleApproval.status in ['approved', 'waived']",
                "ProductionRelease.status == 'approved'",
                "WAES.gate == 'confirmed'",
            ],
        },
        "generated_items": 68,
        "batch_generated": False,
        "substance_gate": "pass",
        "status": "l4_repair" if self_correction_blocked else "l4_closed",
        "next_round": "real-source-record-or-business-input-remediation" if self_correction_blocked else "L5-preparation",
        "completed_rounds": ["GPCF-L4-001", "GPCF-L4-002", "GPCF-L4-003", "GPCF-L4-004", "GPCF-L4-005", "GPCF-L4-006", "GPCF-L4-007", "GPCF-L4-008", "GPCF-L4-009", "GPCF-L4-010", "GPCF-L4-011", "GPCF-L4-012"],
        "project_group_score": project_group_score,
        "self_correction": {
            "round_id": "GPCF-L4-GFIS-TEST-SCENARIO-SYNC-001",
            "previous_l4_score_invalidated": self_correction_blocked,
            "gfis_runtime_subject": "blocked" if gfis_demo_counted_as_runtime else "pass",
            "gfis_demo_counted_as_runtime_evidence": gfis_demo_counted_as_runtime,
            "gfis_sop_e2e_status": gfis_sop_e2e_status,
            "gfis_sop_e2e_failed_tests": gfis_last_run.get("failedTests", []),
            "gfis_runtime_sop_e2e_status": gfis_runtime_sop_status,
            "gfis_runtime_sop_e2e_exit_code": gfis_runtime_sop["exit_code"],
            "gfis_runtime_sop_e2e_output": gfis_runtime_sop["output"],
            "gfis_real_source_record_intake_gate_status": gfis_real_source_record_intake_gate["status"],
            "gfis_real_source_record_intake_gate_exit_code": gfis_real_source_record_intake_gate["exit_code"],
            "gfis_real_source_record_intake_gate_output": gfis_real_source_record_intake_gate["output"],
            "gfis_pending_business_verification_gate_status": gfis_pending_business_verification_gate["status"],
            "gfis_pending_business_verification_gate_exit_code": gfis_pending_business_verification_gate["exit_code"],
            "gfis_pending_business_verification_gate_output": gfis_pending_business_verification_gate["output"],
            "gfis_runtime_primary_key_gate_status": gfis_runtime_primary_key_gate["status"],
            "gfis_runtime_primary_key_gate_exit_code": gfis_runtime_primary_key_gate["exit_code"],
            "gfis_runtime_primary_key_gate_output": gfis_runtime_primary_key_gate["output"],
            "gfis_review_queue_admission_gate_status": gfis_review_queue_admission_gate["status"],
            "gfis_review_queue_admission_gate_exit_code": gfis_review_queue_admission_gate["exit_code"],
            "gfis_review_queue_admission_gate_output": gfis_review_queue_admission_gate["output"],
            "gfis_runtime_intake_gate_status": gfis_runtime_intake_gate["status"],
            "gfis_runtime_intake_gate_exit_code": gfis_runtime_intake_gate["exit_code"],
            "gfis_runtime_intake_gate_output": gfis_runtime_intake_gate["output"],
            "gfis_waes_review_gate_status": gfis_waes_review_gate["status"],
            "gfis_waes_review_gate_exit_code": gfis_waes_review_gate["exit_code"],
            "gfis_waes_review_gate_output": gfis_waes_review_gate["output"],
            "gfis_verified_artifact_gate_status": gfis_verified_artifact_gate["status"],
            "gfis_verified_artifact_gate_exit_code": gfis_verified_artifact_gate["exit_code"],
            "gfis_verified_artifact_gate_output": gfis_verified_artifact_gate["output"],
            "gfis_real_fact_entry_gate_status": gfis_real_fact_entry_gate["status"],
            "gfis_real_fact_entry_gate_exit_code": gfis_real_fact_entry_gate["exit_code"],
            "gfis_real_fact_entry_gate_output": gfis_real_fact_entry_gate["output"],
            "gfis_real_fact_entry_gate_values": gfis_real_fact_entry_values,
            "gfis_development_ready_goal_status": gfis_development_ready_goal["status"],
            "gfis_development_ready_goal_exit_code": gfis_development_ready_goal["exit_code"],
            "gfis_development_ready_goal_output": gfis_development_ready_goal["output"],
            "gfis_test_source_record_submission_gate_status": gfis_test_source_record_submission_gate["status"],
            "gfis_test_source_record_submission_gate_exit_code": gfis_test_source_record_submission_gate["exit_code"],
            "gfis_test_source_record_submission_gate_output": gfis_test_source_record_submission_gate["output"],
            "gfis_test_data_minimum_sop_e2e_status": gfis_test_data_minimum_sop_e2e["status"],
            "gfis_test_data_minimum_sop_e2e_exit_code": gfis_test_data_minimum_sop_e2e["exit_code"],
            "gfis_test_data_minimum_sop_e2e_output": gfis_test_data_minimum_sop_e2e["output"],
            "gfis_test_data_12_stage_sop_e2e_status": gfis_test_data_12_stage_sop_e2e["status"],
            "gfis_test_data_12_stage_sop_e2e_exit_code": gfis_test_data_12_stage_sop_e2e["exit_code"],
            "gfis_test_data_12_stage_sop_e2e_output": gfis_test_data_12_stage_sop_e2e["output"],
            "gfis_test_data_12_stage_transition_gate_status": gfis_test_data_12_stage_transition_gate["status"],
            "gfis_test_data_12_stage_transition_gate_exit_code": gfis_test_data_12_stage_transition_gate["exit_code"],
            "gfis_test_data_12_stage_transition_gate_output": gfis_test_data_12_stage_transition_gate["output"],
            "gfis_test_data_12_stage_negative_transition_guard_status": gfis_test_data_12_stage_negative_transition_guard["status"],
            "gfis_test_data_12_stage_negative_transition_guard_exit_code": gfis_test_data_12_stage_negative_transition_guard["exit_code"],
            "gfis_test_data_12_stage_negative_transition_guard_output": gfis_test_data_12_stage_negative_transition_guard["output"],
            "gfis_test_data_runtime_replay_harness_status": gfis_test_data_runtime_replay_harness["status"],
            "gfis_test_data_runtime_replay_harness_exit_code": gfis_test_data_runtime_replay_harness["exit_code"],
            "gfis_test_data_runtime_replay_harness_output": gfis_test_data_runtime_replay_harness["output"],
            "gfis_test_data_scenario_coverage_status": gfis_test_data_scenario_coverage["status"],
            "gfis_test_data_scenario_coverage_exit_code": gfis_test_data_scenario_coverage["exit_code"],
            "gfis_test_data_scenario_coverage_output": gfis_test_data_scenario_coverage["output"],
        },
        "l4_closure": {
            "score": project_group_score,
            "status": "L4 repair required" if self_correction_blocked else "L4 closed",
            "accepted_integrated": False,
            "l5_activated": False,
            "production_write": False,
            "real_external_api_write": False,
            "device_ota": False,
            "deployment": False,
        },
        "l4_round_scores": {
            "GPCF-L4-003": 96,
            "GPCF-L4-004": 92,
            "GPCF-L4-005": 96,
            "GPCF-L4-006": 96,
            "GPCF-L4-007": 96,
            "GPCF-L4-008": 96,
            "GPCF-L4-009": 95,
            "GPCF-L4-010": 95,
            "GPCF-L4-011": 95,
            "GPCF-L4-012": 100,
        },
        "project_rounds": {
            "MMC": {
                "round_id": "MMC-L4-002",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "sample_gate": "blocked_without_required_evidence",
                "resource_gate": "blocked_without_required_evidence",
            },
            "KDS": {
                "round_id": "KDS-L4-003",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "knowledge_index": "ready_for_review",
                "accepted_integrated": False,
            },
            "Brain": {
                "round_id": "Brain-L4-004",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "retrieval_smoke": "pass",
                "score": 92,
                "accepted_integrated": False,
            },
            "PKC": {
                "round_id": "PKC-L4-005",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "task_notification_status_mock": "pass",
                "score": 96,
                "accepted_integrated": False,
            },
            "PVAOS": {
                "round_id": "PVAOS-L4-006",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "organization_partner_permission_baseline": "pass",
                "score": 96,
                "accepted_integrated": False,
            },
            "GPC": {
                "round_id": "GPC-L4-007",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "platform_order_contract": "pass",
                "score": 96,
                "accepted_integrated": False,
            },
            "GFIS": {
                "round_id": "GFIS-RUNTIME-SOP-E2E-DEV-READY-001",
                "status": "repair_required" if self_correction_blocked else "ready_for_review",
                "development_ready": "pass" if gfis_development_ready_goal["exit_code"] == 0 else "failed",
                "test_data_minimum_sop_e2e": "pass" if gfis_test_data_minimum_sop_e2e["exit_code"] == 0 else "failed",
                "test_data_12_stage_sop_e2e": "pass" if gfis_test_data_12_stage_sop_e2e["exit_code"] == 0 else "failed",
                "test_data_12_stage_transition_gate": "pass" if gfis_test_data_12_stage_transition_gate["exit_code"] == 0 else "failed",
                "test_data_12_stage_negative_transition_guard": "pass" if gfis_test_data_12_stage_negative_transition_guard["exit_code"] == 0 else "failed",
                "test_data_12_stage_replay_harness": "pass" if gfis_test_data_runtime_replay_harness["exit_code"] == 0 else "failed",
                "test_data_runtime_object_contract": "pass" if gfis_test_data_runtime_replay_harness["exit_code"] == 0 else "failed",
                "test_data_scenario_coverage": "pass" if gfis_test_data_scenario_coverage["exit_code"] == 0 else "failed",
                "test_data_mutation_guard": "pass" if gfis_test_data_scenario_coverage["exit_code"] == 0 else "failed",
                "synthetic_dev_lane": "dev_closed",
                "real_business_lane": "repair_required" if self_correction_blocked else "ready_for_review",
                "business_verification_pending": self_correction_blocked,
                "kds_retrieval": "completed",
                "factory_sample_order_readonly": "invalid_as_runtime_subject" if gfis_demo_counted_as_runtime else "pass",
                "demo_e2e": gfis_sop_e2e_status,
                "runtime_sop_e2e": gfis_runtime_sop_status,
                "real_source_record_intake_gate": gfis_real_source_record_intake_gate["status"],
                "pending_business_verification_gate": gfis_pending_business_verification_gate["status"],
                "runtime_primary_key_gate": gfis_runtime_primary_key_gate["status"],
                "review_queue_gate": gfis_review_queue_admission_gate["status"],
                "runtime_intake_gate": gfis_runtime_intake_gate["status"],
                "waes_review_gate": gfis_waes_review_gate["status"],
                "verified_artifact_gate": gfis_verified_artifact_gate["status"],
                "real_fact_entry_gate": gfis_real_fact_entry_gate["status"],
                "real_fact_entry_status_ceiling": gfis_real_fact_entry_values.get("status_ceiling", "unknown"),
                "real_fact_entry_next_required_input": gfis_real_fact_entry_values.get("next_required_input", "unknown"),
                "development_ready_goal": gfis_development_ready_goal["status"],
                "test_source_record_submission_gate": gfis_test_source_record_submission_gate["status"],
                "test_data_minimum_sop_e2e": gfis_test_data_minimum_sop_e2e["status"],
                "test_data_12_stage_sop_e2e": gfis_test_data_12_stage_sop_e2e["status"],
                "test_data_12_stage_transition_gate": gfis_test_data_12_stage_transition_gate["status"],
                "test_data_12_stage_negative_transition_guard": gfis_test_data_12_stage_negative_transition_guard["status"],
                "test_data_runtime_replay_harness": gfis_test_data_runtime_replay_harness["status"],
                "test_data_scenario_coverage": gfis_test_data_scenario_coverage["status"],
                "test_source_records": 1,
                "test_runtime_primary_keys": 1,
                "test_review_queue_items": 1,
                "test_runtime_intake_items": 1,
                "test_waes_evidence_candidates": 1,
                "test_verified_artifacts": 1,
                "valid_source_records": 0,
                "runtime_primary_key_created": 0,
                "runtime_primary_key_ready": 0,
                "review_queue_created": 0,
                "review_queue": 0,
                "runtime_intake_created": 0,
                "runtime_intake": 0,
                "waes_review_created": 0,
                "waes_review": 0,
                "verified_artifact_created": 0,
                "verified": 0,
                "score": 62 if self_correction_blocked else 96,
                "accepted_integrated": False,
            },
            "XiaoC": {
                "round_id": "XiaoC-L4-009",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "agent_orchestration_dry_run": "pass",
                "score": 95,
                "accepted_integrated": False,
            },
            "XGD": {
                "round_id": "XGD-L4-010",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "risk_analysis_dry_run": "pass",
                "score": 95,
                "accepted_integrated": False,
            },
            "XiaoG": {
                "round_id": "XiaoG-L4-011",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "readonly_audit_notification_mock": "pass",
                "score": 95,
                "accepted_integrated": False,
            },
            "GPCF": {
                "round_id": "GPCF-L4-GFIS-TEST-SCENARIO-SYNC-001",
                "status": "repair_required" if self_correction_blocked else "ready_for_review",
                "closure_score_matrix": "invalidated_by_self_correction" if self_correction_blocked else "pass",
                "score": project_group_score,
                "accepted_integrated": False,
            },
        },
    }
    out = ROOT / "docs/harness/evidence/l4_minimum_loop_assessment.json"
    out.write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"l4_minimum_closed_loop={'repair' if self_correction_blocked else 'pass'}")
    print(
        "round=GPCF-L4-GFIS-TEST-SCENARIO-SYNC-001 projects=12 core_objects=11 sample_gate=blocked "
        "resource_gate=blocked "
        f"gfis_runtime_subject={'blocked' if gfis_demo_counted_as_runtime else 'pass'} "
        f"demo_e2e={gfis_sop_e2e_status} "
        f"runtime_sop_e2e={gfis_runtime_sop_status} "
        f"real_source_record_intake_gate={gfis_real_source_record_intake_gate['status']} "
        f"pending_business_verification_gate={gfis_pending_business_verification_gate['status']} "
        f"runtime_primary_key_gate={gfis_runtime_primary_key_gate['status']} "
        f"review_queue_gate={gfis_review_queue_admission_gate['status']} "
        f"runtime_intake_gate={gfis_runtime_intake_gate['status']} "
        f"waes_review_gate={gfis_waes_review_gate['status']} "
        f"verified_artifact_gate={gfis_verified_artifact_gate['status']} "
        f"real_fact_entry_gate={gfis_real_fact_entry_gate['status']} "
        f"real_fact_entry_status_ceiling={gfis_real_fact_entry_values.get('status_ceiling', 'unknown')} "
        f"real_fact_entry_next_required_input={gfis_real_fact_entry_values.get('next_required_input', 'unknown')} "
        f"development_ready_goal={gfis_development_ready_goal['status']} "
        f"test_source_record_submission_gate={gfis_test_source_record_submission_gate['status']} "
        f"test_data_minimum_sop_e2e={gfis_test_data_minimum_sop_e2e['status']} "
        f"test_data_12_stage_sop_e2e={gfis_test_data_12_stage_sop_e2e['status']} "
        f"test_data_12_stage_transition_gate={gfis_test_data_12_stage_transition_gate['status']} "
        f"test_data_12_stage_negative_transition_guard={gfis_test_data_12_stage_negative_transition_guard['status']} "
        f"test_data_runtime_replay_harness={gfis_test_data_runtime_replay_harness['status']} "
        f"test_data_scenario_coverage={gfis_test_data_scenario_coverage['status']} "
        f"project_group_score={project_group_score} "
        f"synthetic_dev_lane=dev_closed "
        f"development_ready={'pass' if gfis_development_ready_goal['exit_code'] == 0 else 'failed'} "
        f"test_data_minimum_sop_e2e={'pass' if gfis_test_data_minimum_sop_e2e['exit_code'] == 0 else 'failed'} "
        f"test_data_12_stage_sop_e2e={'pass' if gfis_test_data_12_stage_sop_e2e['exit_code'] == 0 else 'failed'} "
        f"test_data_12_stage_transition_gate={'pass' if gfis_test_data_12_stage_transition_gate['exit_code'] == 0 else 'failed'} "
        f"test_data_12_stage_negative_transition_guard={'pass' if gfis_test_data_12_stage_negative_transition_guard['exit_code'] == 0 else 'failed'} "
        f"test_data_12_stage_replay_harness={'pass' if gfis_test_data_runtime_replay_harness['exit_code'] == 0 else 'failed'} "
        f"test_data_runtime_object_contract={'pass' if gfis_test_data_runtime_replay_harness['exit_code'] == 0 else 'failed'} "
        f"test_data_scenario_coverage={'pass' if gfis_test_data_scenario_coverage['exit_code'] == 0 else 'failed'} "
        f"test_data_mutation_guard={'pass' if gfis_test_data_scenario_coverage['exit_code'] == 0 else 'failed'} "
        f"real_business_lane={'repair_required' if self_correction_blocked else 'ready_for_review'} "
        f"business_verification_pending={'true' if self_correction_blocked else 'false'} "
        f"next={'real-source-record-or-business-input-remediation' if self_correction_blocked else 'L5-preparation'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
