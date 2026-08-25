#!/usr/bin/env python3
"""确定性校验 GCWORLD 数据分层、投影重建、可靠事件、安全与阶段治理契约。"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
SCHEMA_PATH = ARTIFACTS / "gcworld-engineering-governance.schema.json"
FIXTURES_PATH = ARTIFACTS / "gcworld-engineering-governance-fixtures.json"
MANIFEST_PATH = ARTIFACTS / "gcworld-engineering-governance-contract-manifest.yaml"

EXPECTED_LAYERS = {"source", "candidate", "kds_fact", "world_projection", "runtime_state", "simulation_branch", "evidence_audit"}
EXPECTED_STORAGES = {"kds", "graph", "relational", "event", "object", "retrieval_index", "cache"}
EXPECTED_INTERFACES = {"world_query", "context", "identity", "agent", "action", "simulation", "governance", "event_stream"}
EXPECTED_METRICS = {
    "source_coverage_rate", "unresolved_identity_rate", "fact_conflict_rate",
    "projection_latency", "snapshot_build_duration", "adjudication_latency",
    "action_success_rate", "compensation_rate", "overreach_block_rate",
    "agent_candidate_acceptance_rate", "evidence_completeness_rate",
}
EXPECTED_PHASES = [f"P{number}" for number in range(8)]
FACT_PROMOTION_GATES = {"证据完整", "规则校验通过", "影响评估完成", "人工确认完成", "正式写入回执"}
COLLECTION_IDS = {
    "dataLayers": "layerId",
    "promotionRules": "ruleId",
    "storageResponsibilities": "storageId",
    "projectionRebuilds": "rebuildId",
    "worldObjects": "worldAssetId",
    "domainInterfaces": "interfaceId",
    "reliableEvents": "eventId",
    "observabilityMetrics": "metricId",
    "deliveryPhases": "phaseId",
}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON根节点必须为对象：{path}")
    return payload


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
    for collection, id_field in COLLECTION_IDS.items():
        canonical[collection] = sorted(canonical[collection], key=lambda item: item[id_field])
    unordered_fields = {
        "allowedPromotionTargets", "sourceRefs", "evidenceRefs", "requiredGates",
        "differenceRefs", "priorAssetRefs", "connectorWhitelist", "secretPlaintextLocations",
        "exitMetricRefs",
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


def validate_unique_ids(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    identifiers: set[str] = set()
    for collection, id_field in COLLECTION_IDS.items():
        for item in document[collection]:
            identifier = item[id_field]
            if identifier in identifiers:
                reasons.add("duplicate_id")
            identifiers.add(identifier)
    return reasons


def validate_layers_and_promotions(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    layers = document["dataLayers"]
    types = [item["layerType"] for item in layers]
    if len(types) != len(set(types)):
        reasons.add("data_layer_duplicate")
    if len(types) != len(EXPECTED_LAYERS) or set(types) != EXPECTED_LAYERS:
        reasons.add("data_layers_incomplete")
    for layer in layers:
        if layer["authoritativeFactSource"] and layer["layerType"] != "kds_fact":
            reasons.add("non_kds_layer_claims_fact_authority")
        if layer["layerType"] == "kds_fact" and not layer["authoritativeFactSource"]:
            reasons.add("kds_fact_authority_missing")

    for rule in document["promotionRules"]:
        if rule["fromLayer"] == "simulation_branch" and rule["toLayer"] == "kds_fact":
            reasons.add("simulation_direct_fact_promotion")
        if rule["toLayer"] == "kds_fact":
            if rule["fromLayer"] != "candidate" or not FACT_PROMOTION_GATES.issubset(set(rule["requiredGates"])):
                reasons.add("fact_promotion_gates_incomplete")
        if rule["directAuthorityWriteAllowed"]:
            reasons.add("direct_authority_write_allowed")
    return reasons


def validate_storages_and_rebuilds(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    storages = document["storageResponsibilities"]
    types = [item["storageType"] for item in storages]
    if len(types) != len(set(types)):
        reasons.add("storage_role_duplicate")
    if len(types) != len(EXPECTED_STORAGES) or set(types) != EXPECTED_STORAGES:
        reasons.add("storage_roles_incomplete")
    for storage in storages:
        if storage["storesAuthoritativeFacts"] and storage["storageType"] != "kds":
            reasons.add("derived_storage_claims_fact_authority")
        if storage["storageType"] in {"graph", "retrieval_index", "cache"} and not storage["reconstructible"]:
            reasons.add("derived_storage_not_reconstructible")
        if storage["storageType"] == "kds" and not storage["storesAuthoritativeFacts"]:
            reasons.add("kds_fact_authority_missing")

    for rebuild in document["projectionRebuilds"]:
        digests_match = rebuild["expectedDigest"] == rebuild["actualDigest"]
        if rebuild["status"] == "match" and (
            not digests_match or rebuild["differenceCount"] != 0 or rebuild["differenceRefs"]
        ):
            reasons.add("projection_match_digest_mismatch")
        if rebuild["status"] == "difference":
            if digests_match or rebuild["differenceCount"] < 1 or not rebuild["differenceRefs"]:
                reasons.add("projection_difference_evidence_incomplete")
            if not rebuild["promotionBlocked"]:
                reasons.add("projection_difference_not_blocked")
    return reasons


def validate_objects_and_interfaces(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    for item in document["worldObjects"]:
        if item["validUntil"] is not None and parse_time(item["validFrom"]) >= parse_time(item["validUntil"]):
            reasons.add("object_validity_reversed")
        for history in item["identityHistory"]:
            if history["changeType"] in {"merge", "split"} and (
                not history["priorAssetRefs"] or not history["approvedByRef"] or not history["auditRef"]
            ):
                reasons.add("identity_change_audit_incomplete")

    interfaces = [item["interfaceType"] for item in document["domainInterfaces"]]
    if len(interfaces) != len(set(interfaces)):
        reasons.add("domain_interface_duplicate")
    if len(interfaces) != len(EXPECTED_INTERFACES) or set(interfaces) != EXPECTED_INTERFACES:
        reasons.add("domain_interfaces_incomplete")
    return reasons


def validate_events(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    grouped: dict[str, list[dict[str, Any]]] = {}
    for event in document["reliableEvents"]:
        grouped.setdefault(event["idempotencyKey"], []).append(event)
        if not event["outboxPersisted"]:
            reasons.add("event_outbox_missing")
        if event["deliveryState"] == "dead_letter":
            if event["attempts"] < event["maxRetries"]:
                reasons.add("premature_dead_letter")
            if not event["compensationRef"]:
                reasons.add("dead_letter_compensation_missing")
        if event["deliveryState"] == "compensated" and not event["compensationRef"]:
            reasons.add("compensation_receipt_missing")
    for events in grouped.values():
        if len(events) <= 1:
            continue
        if sum(item["sideEffectCount"] for item in events) != 1:
            reasons.add("idempotency_side_effect_duplicated")
        if sum(1 for item in events if not item["inboxDeduplicated"]) != 1:
            reasons.add("inbox_deduplication_broken")
        if len({item["commandId"] for item in events}) != 1:
            reasons.add("idempotency_command_mismatch")
    return reasons


def validate_security_metrics_and_phases(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    security = document["securityControls"]
    if not security["tenantIsolation"]:
        reasons.add("tenant_isolation_disabled")
    if not all([
        security["leastPrivilege"], security["transportEncryption"], security["atRestEncryption"],
        security["auditEnabled"], security["promptInjectionDefense"], bool(security["connectorWhitelist"]),
    ]):
        reasons.add("security_control_incomplete")
    if security["secretHandling"] != "reference_only" or security["secretPlaintextLocations"]:
        reasons.add("plaintext_secret_propagation")

    metric_types = [item["metricType"] for item in document["observabilityMetrics"]]
    if len(metric_types) != len(set(metric_types)):
        reasons.add("observability_metric_duplicate")
    if len(metric_types) != len(EXPECTED_METRICS) or set(metric_types) != EXPECTED_METRICS:
        reasons.add("observability_metrics_incomplete")
    metric_ids = {item["metricId"] for item in document["observabilityMetrics"]}

    phases = document["deliveryPhases"]
    phase_ids = [item["phaseId"] for item in phases]
    if phase_ids != EXPECTED_PHASES:
        reasons.add("delivery_phases_incomplete")
    for index, phase in enumerate(phases):
        expected_prerequisite = None if index == 0 else EXPECTED_PHASES[index - 1]
        if phase["prerequisitePhase"] != expected_prerequisite:
            reasons.add("phase_prerequisite_skipped")
        if not set(phase["exitMetricRefs"]).issubset(metric_ids):
            reasons.add("phase_metric_ref_missing")
        if phase["authorizationGranted"] and not phase["independentAuthorizationRef"]:
            reasons.add("phase_independent_authorization_missing")
        if phase["nextPhaseAuthorized"] and not (
            phase["exitCriteriaMet"]
            and phase["riskReviewed"]
            and phase["authorizationGranted"]
            and phase["independentAuthorizationRef"]
        ):
            reasons.add("phase_authorization_bypassed")
    return reasons


def validate_acceptance(document: dict[str, Any]) -> set[str]:
    evidence = document["acceptanceEvidence"]
    reasons: set[str] = set()
    if evidence["evidenceType"] in {"fixture", "demonstration"} and evidence["claimedStatus"] != "structural_compliance":
        reasons.add("evidence_status_overclaimed")
    if evidence["claimedStatus"] == "complete" and not (
        evidence["independentValidation"] and evidence["humanConfirmation"] and evidence["realRuntimeEvidence"]
    ):
        reasons.add("evidence_status_overclaimed")
    return reasons


def validate_semantics(document: dict[str, Any]) -> set[str]:
    reasons = validate_unique_ids(document)
    reasons |= validate_layers_and_promotions(document)
    reasons |= validate_storages_and_rebuilds(document)
    reasons |= validate_objects_and_interfaces(document)
    reasons |= validate_events(document)
    reasons |= validate_security_metrics_and_phases(document)
    reasons |= validate_acceptance(document)
    return reasons


def validate_manifest() -> None:
    payload = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("gcworld_engineering_governance=fail reason=manifest_invalid")
    for item in payload.get("artifacts", []):
        path = ROOT / item["path"]
        if not path.is_file():
            raise SystemExit(f"gcworld_engineering_governance=fail reason=manifest_file_missing path={item['path']}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            raise SystemExit(f"gcworld_engineering_governance=fail reason=manifest_hash_mismatch path={item['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--determinism-runs", type=int, default=3)
    args = parser.parse_args()
    if args.determinism_runs < 1:
        raise SystemExit("gcworld_engineering_governance=fail reason=invalid_determinism_runs")

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
            raise SystemExit(f"gcworld_engineering_governance=fail case={case['name']} reasons={','.join(sorted(reasons))}")
        digest = semantic_digest(document)
        for _ in range(args.determinism_runs):
            if semantic_digest(document) != digest:
                raise SystemExit(f"gcworld_engineering_governance=fail case={case['name']} reason=nondeterministic_digest")
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
            raise SystemExit(f"gcworld_engineering_governance=fail case={case['name']} missing={missing} actual={actual}")
        negative += 1

    validate_manifest()
    matrix_digest = hashlib.sha256("".join(sorted(digests)).encode("utf-8")).hexdigest()
    print(
        "gcworld_engineering_governance=pass "
        f"positive={positive} negative={negative} data_layers={len(EXPECTED_LAYERS)} "
        f"storage_roles={len(EXPECTED_STORAGES)} domain_interfaces={len(EXPECTED_INTERFACES)} "
        f"observability_metrics={len(EXPECTED_METRICS)} delivery_phases={len(EXPECTED_PHASES)} "
        f"determinism_runs={args.determinism_runs} matrix_sha256={matrix_digest} "
        "real_events=0 kds_writes=0 business_writes=0 external_writes=0 deployments=0 status_promotions=0"
    )


if __name__ == "__main__":
    main()
