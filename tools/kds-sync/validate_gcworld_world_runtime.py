#!/usr/bin/env python3
"""确定性校验 GCWORLD 世界运行服务、闭环、补偿和模拟隔离契约。"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import unicodedata
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
SCHEMA_PATH = ARTIFACTS / "gcworld-world-runtime.schema.json"
FIXTURES_PATH = ARTIFACTS / "gcworld-world-runtime-fixtures.json"
MANIFEST_PATH = ARTIFACTS / "gcworld-world-runtime-contract-manifest.yaml"
LIFECYCLE_STAGES = [
    "observe",
    "resolve",
    "snapshot",
    "reason",
    "adjudicate",
    "confirm",
    "execute",
    "evidence",
    "promote",
    "learn",
]
EXPECTED_SERVICES = {
    "world_registry",
    "identity_resolution",
    "world_projection",
    "context_builder",
    "event_engine",
    "action_runtime",
    "agent_runtime",
    "simulation_engine",
    "governance_adapter",
    "query_view",
}
ID_FIELDS = {
    "serviceRegistry": ("serviceId", "service"),
    "runtimeRuns": ("runId", "runtime-run"),
    "tasks": ("taskId", "task"),
    "commitments": ("commitmentId", "commitment"),
    "actionReceipts": ("receiptId", "action-receipt"),
    "compensationReceipts": ("compensationReceiptId", "compensation-receipt"),
    "commandLedger": ("entryId", "command-entry"),
    "simulationBranches": ("branchId", "simulation-branch"),
    "promotionCandidates": ("candidateId", "promotion-candidate"),
}
RISK_RANK = {f"R{number}": number for number in range(5)}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON根节点必须为对象：{path}")
    return payload


def stable_id(kind: str, stable_key: str) -> str:
    normalized = unicodedata.normalize("NFC", stable_key)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:24]
    return f"gcw:{kind}:{digest}"


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def locate(document: dict[str, Any], dotted_path: str) -> tuple[Any, str]:
    parts = dotted_path.split(".")
    target: Any = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    return target, parts[-1]


def set_path(document: dict[str, Any], dotted_path: str, value: Any) -> None:
    target, last = locate(document, dotted_path)
    if isinstance(target, list):
        target[int(last)] = deepcopy(value)
    else:
        target[last] = deepcopy(value)


def remove_path(document: dict[str, Any], dotted_path: str) -> None:
    target, last = locate(document, dotted_path)
    if isinstance(target, list):
        del target[int(last)]
    else:
        target.pop(last, None)


def render_case(base: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    document = deepcopy(base)
    for collection, entries in case.get("append", {}).items():
        document[collection].extend(deepcopy(entries))
    for dotted_path, value in case.get("replace", {}).items():
        set_path(document, dotted_path, value)
    for dotted_path in case.get("remove", []):
        remove_path(document, dotted_path)
    return document


def semantic_digest(document: dict[str, Any]) -> str:
    canonical = deepcopy(document)
    for collection, (id_field, _) in ID_FIELDS.items():
        canonical[collection] = sorted(canonical[collection], key=lambda item: item[id_field])
    unordered_fields = {
        "evidenceRefs",
        "dependencyRefs",
        "sourceEvidenceRefs",
        "resultEvidenceRefs",
        "acceptanceEvidenceRefs",
        "actionRefs",
        "actionReceiptRefs",
        "assumptionRefs",
        "executionRefs",
        "formalWriteReceiptRefs",
    }

    def normalize(value: Any, field: str | None = None) -> Any:
        if isinstance(value, dict):
            return {key: normalize(item, key) for key, item in sorted(value.items())}
        if isinstance(value, list):
            items = [normalize(item) for item in value]
            if field in unordered_fields:
                return sorted(items, key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True))
            return items
        return value

    encoded = json.dumps(normalize(canonical), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def schema_reasons(validator: Draft202012Validator, document: dict[str, Any]) -> set[str]:
    return {"schema_error"} if list(validator.iter_errors(document)) else set()


def validate_stable_ids(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    all_ids: set[str] = set()
    for collection, (id_field, kind) in ID_FIELDS.items():
        for item in document[collection]:
            item_id = item[id_field]
            if item_id in all_ids:
                reasons.add("duplicate_id")
            all_ids.add(item_id)
            if item_id != stable_id(kind, item["stableKey"]):
                reasons.add("stable_id_mismatch")
    return reasons


def validate_services(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    service_types = [item["serviceType"] for item in document["serviceRegistry"]]
    if len(service_types) != len(EXPECTED_SERVICES) or set(service_types) != EXPECTED_SERVICES:
        reasons.add("service_registry_incomplete")
    if len(service_types) != len(set(service_types)):
        reasons.add("service_registry_duplicate")
    for service in document["serviceRegistry"]:
        if (
            service["authorityMode"] == "authority_owner"
            or service["writesAuthoritativeFacts"]
            or service["executesBusinessSideEffects"]
        ):
            reasons.add("authority_boundary_broken")
    return reasons


def validate_runtime_runs(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    receipts = {item["receiptId"]: item for item in document["actionReceipts"]}
    for run in document["runtimeRuns"]:
        names = [stage["name"] for stage in run["stages"]]
        if names != LIFECYCLE_STAGES[: len(names)]:
            reasons.add("stage_sequence_broken")
        stage_map = {stage["name"]: stage for stage in run["stages"]}
        times = [parse_time(stage["occurredAt"]) for stage in run["stages"]]
        if times != sorted(times):
            reasons.add("stage_time_reversed")

        terminal_seen = False
        for stage in run["stages"]:
            if terminal_seen and stage["status"] == "completed":
                if stage["name"] == "promote":
                    reasons.add("status_promotion_bypassed")
                else:
                    reasons.add("stage_sequence_broken")
            if stage["status"] != "completed":
                terminal_seen = True

        execute = stage_map.get("execute")
        confirm = stage_map.get("confirm")
        adjudicate = stage_map.get("adjudicate")
        evidence = stage_map.get("evidence")
        promote = stage_map.get("promote")
        if execute is not None and execute["status"] == "completed":
            if adjudicate is None or adjudicate["status"] != "completed" or not run.get("decisionRef"):
                reasons.add("adjudication_bypassed")
            if RISK_RANK[run["riskLevel"]] >= 3 or run["requestedImpact"] == "external":
                if confirm is None or confirm["status"] != "completed" or not run.get("confirmationRef"):
                    reasons.add("confirmation_bypassed")
        if promote is not None and promote["status"] == "completed":
            if evidence is None or evidence["status"] != "completed":
                reasons.add("status_promotion_bypassed")
        if run["state"] == "completed" and (names != LIFECYCLE_STAGES or any(item["status"] != "completed" for item in run["stages"])):
            reasons.add("completed_run_incomplete")
        if run["state"] == "awaiting_confirmation":
            if execute is not None or confirm is None or confirm["status"] != "pending":
                reasons.add("awaiting_confirmation_boundary_broken")
        if not set(run["actionReceiptRefs"]).issubset(receipts):
            reasons.add("dangling_action_receipt_ref")
    return reasons


def validate_tasks_and_commitments(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    receipt_ids = {item["receiptId"] for item in document["actionReceipts"]}
    for task in document["tasks"]:
        if task["status"] == "closed" and (
            not task["resultEvidenceRefs"]
            or not task["acceptanceEvidenceRefs"]
            or not task["actionRefs"]
            or not set(task["actionRefs"]).issubset(receipt_ids)
        ):
            reasons.add("task_close_evidence_missing")
    for commitment in document["commitments"]:
        if commitment["status"] == "closed" and (
            not commitment["resultEvidenceRefs"]
            or not commitment["acceptanceEvidenceRefs"]
            or not commitment["actionRefs"]
            or not set(commitment["actionRefs"]).issubset(receipt_ids)
        ):
            reasons.add("commitment_close_evidence_missing")
    return reasons


def validate_receipts_and_compensation(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    runs = {item["runId"]: item for item in document["runtimeRuns"]}
    compensations_by_action: dict[str, list[dict[str, Any]]] = {}
    for item in document["compensationReceipts"]:
        compensations_by_action.setdefault(item["actionReceiptId"], []).append(item)

    for receipt in document["actionReceipts"]:
        run = runs.get(receipt["runId"])
        if run is None:
            reasons.add("dangling_runtime_run_ref")
            continue
        if receipt["receiptId"] not in run["actionReceiptRefs"]:
            reasons.add("run_receipt_link_mismatch")
        if receipt["result"] == "succeeded" and not receipt["evidenceRefs"]:
            reasons.add("successful_receipt_without_evidence")
        if RISK_RANK[receipt["riskLevel"]] >= 3 and receipt["result"] == "succeeded":
            if not receipt.get("decisionRef") or not receipt.get("confirmationRef"):
                reasons.add("high_risk_receipt_incomplete")
        if receipt["result"] == "partial":
            compensations = compensations_by_action.get(receipt["receiptId"], [])
            if not receipt.get("compensationPolicyRef") or not compensations:
                reasons.add("partial_failure_uncompensated")
            elif not any(item["result"] == "completed" for item in compensations):
                reasons.add("partial_failure_uncompensated")
            if any(item["result"] == "failed" for item in compensations) and run["state"] == "completed":
                reasons.add("compensation_failure_hidden")
    for compensation in document["compensationReceipts"]:
        receipt = next((item for item in document["actionReceipts"] if item["receiptId"] == compensation["actionReceiptId"]), None)
        if receipt is None:
            reasons.add("dangling_compensation_ref")
        elif receipt.get("compensationPolicyRef") != compensation["policyRef"]:
            reasons.add("compensation_policy_mismatch")
    return reasons


def validate_idempotency(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    receipt_ids = {item["receiptId"] for item in document["actionReceipts"]}
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entry in document["commandLedger"]:
        grouped.setdefault(entry["idempotencyKey"], []).append(entry)
        if entry["actionReceiptRef"] not in receipt_ids:
            reasons.add("dangling_command_receipt_ref")
    for entries in grouped.values():
        if len(entries) <= 1:
            continue
        receipt_refs = {entry["actionReceiptRef"] for entry in entries}
        effects = sum(1 for entry in entries if entry["effectApplied"])
        non_duplicate = sum(1 for entry in entries if not entry["duplicate"])
        if len(receipt_refs) != 1 or effects != 1 or non_duplicate != 1:
            reasons.add("idempotency_broken")
    return reasons


def validate_simulation(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    snapshots = {item["worldSnapshotRef"] for item in document["runtimeRuns"]}
    branches = {item["branchId"]: item for item in document["simulationBranches"]}
    for branch in branches.values():
        if branch["baselineSnapshotRef"] not in snapshots:
            reasons.add("simulation_baseline_missing")
        if branch["writesFactWorld"] or branch["grantsRealAuthorization"]:
            reasons.add("simulation_isolation_broken")
    for candidate in document["promotionCandidates"]:
        if candidate["simulationBranchId"] not in branches:
            reasons.add("dangling_simulation_branch_ref")
        gates_ready = (
            candidate["evidenceComplete"]
            and candidate["ruleValidationPassed"]
            and candidate["impactAssessmentCompleted"]
            and bool(candidate.get("humanConfirmationRef"))
        )
        if candidate["status"] == "ready_for_review" and not gates_ready:
            reasons.add("promotion_review_gate_incomplete")
        if candidate["status"] == "promoted" or candidate["factWriteAuthorized"] or candidate["formalWriteReceiptRefs"]:
            reasons.add("direct_fact_promotion")
    return reasons


def validate_semantics(document: dict[str, Any]) -> set[str]:
    reasons = validate_stable_ids(document)
    reasons |= validate_services(document)
    reasons |= validate_runtime_runs(document)
    reasons |= validate_tasks_and_commitments(document)
    reasons |= validate_receipts_and_compensation(document)
    reasons |= validate_idempotency(document)
    reasons |= validate_simulation(document)
    return reasons


def validate_manifest() -> None:
    payload = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("gcworld_world_runtime=fail reason=manifest_invalid")
    for item in payload.get("artifacts", []):
        path = ROOT / item["path"]
        if not path.is_file():
            raise SystemExit(f"gcworld_world_runtime=fail reason=manifest_file_missing path={item['path']}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            raise SystemExit(f"gcworld_world_runtime=fail reason=manifest_hash_mismatch path={item['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--determinism-runs", type=int, default=3)
    args = parser.parse_args()
    if args.determinism_runs < 1:
        raise SystemExit("gcworld_world_runtime=fail reason=invalid_determinism_runs")

    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    fixtures = load_json(FIXTURES_PATH)
    base = fixtures["baseDocument"]

    positive = 0
    digests: list[str] = []
    for case in fixtures["positiveCases"]:
        document = render_case(base, case)
        reasons = schema_reasons(validator, document)
        if not reasons:
            reasons |= validate_semantics(document)
        if reasons:
            raise SystemExit(f"gcworld_world_runtime=fail case={case['name']} reasons={','.join(sorted(reasons))}")
        digest = semantic_digest(document)
        for _ in range(args.determinism_runs):
            if semantic_digest(document) != digest:
                raise SystemExit(f"gcworld_world_runtime=fail case={case['name']} reason=nondeterministic_digest")
        digests.append(digest)
        positive += 1

    negative = 0
    for case in fixtures["negativeCases"]:
        document = render_case(base, case)
        reasons = schema_reasons(validator, document)
        if not reasons:
            reasons |= validate_semantics(document)
        expected = set(case["expected_reasons"])
        if not expected.issubset(reasons):
            actual = ",".join(sorted(reasons)) or "none"
            missing = ",".join(sorted(expected - reasons))
            raise SystemExit(f"gcworld_world_runtime=fail case={case['name']} missing={missing} actual={actual}")
        negative += 1

    validate_manifest()
    matrix_digest = hashlib.sha256("".join(sorted(digests)).encode("utf-8")).hexdigest()
    print(
        "gcworld_world_runtime=pass "
        f"positive={positive} negative={negative} services={len(EXPECTED_SERVICES)} "
        f"lifecycle_stages={len(LIFECYCLE_STAGES)} determinism_runs={args.determinism_runs} "
        f"matrix_sha256={matrix_digest} real_executions=0 fact_writes=0 kds_writes=0 "
        "business_writes=0 external_writes=0 status_promotions=0"
    )


if __name__ == "__main__":
    main()
