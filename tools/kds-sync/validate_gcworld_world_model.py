#!/usr/bin/env python3
"""确定性校验 GCWORLD 证据数字孪生世界模型及其正反例。"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
SCHEMA_PATH = ARTIFACTS / "gcworld-world-model.schema.json"
FIXTURES_PATH = ARTIFACTS / "gcworld-world-model-fixtures.json"
ID_FIELDS = {
    "assets": ("assetId", "asset"),
    "aliases": ("aliasId", "alias"),
    "relationships": ("relationshipId", "relation"),
    "evidence": ("evidenceId", "evidence"),
    "worldStates": ("stateId", "state"),
}


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


def set_path(document: dict[str, Any], dotted_path: str, value: Any) -> None:
    parts = dotted_path.split(".")
    target: Any = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    last = parts[-1]
    if isinstance(target, list):
        target[int(last)] = deepcopy(value)
    else:
        target[last] = deepcopy(value)


def render_case(base: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    document = deepcopy(base)
    for collection, entries in case.get("append", {}).items():
        document[collection].extend(deepcopy(entries))
    for dotted_path, value in case.get("replace", {}).items():
        set_path(document, dotted_path, value)
    for collection in case.get("reverseArrays", []):
        document[collection].reverse()
    return document


def semantic_digest(document: dict[str, Any]) -> str:
    canonical = deepcopy(document)
    canonical.pop("expectedReasons", None)
    for collection, (id_field, _) in ID_FIELDS.items():
        canonical[collection] = sorted(canonical[collection], key=lambda item: item[id_field])
        for item in canonical[collection]:
            if isinstance(item.get("evidenceRefs"), list):
                item["evidenceRefs"].sort()
            if isinstance(item.get("candidateAssetRefs"), list):
                item["candidateAssetRefs"].sort()
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def validate_semantics(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    tenant_id = document["tenantId"]
    ids: set[str] = set()

    for collection, (id_field, kind) in ID_FIELDS.items():
        for item in document[collection]:
            item_id = item[id_field]
            if item_id in ids:
                reasons.add("duplicate_id")
            ids.add(item_id)
            if item_id != stable_id(kind, item["stableKey"]):
                reasons.add("stable_id_mismatch")

    evidence_by_id = {item["evidenceId"]: item for item in document["evidence"]}
    asset_by_id = {item["assetId"]: item for item in document["assets"]}
    relation_by_id = {item["relationshipId"]: item for item in document["relationships"]}

    for evidence in document["evidence"]:
        if evidence["tenantId"] != tenant_id:
            reasons.add("cross_tenant_evidence_ref")

    for collection in ("assets", "aliases", "relationships", "worldStates"):
        for item in document[collection]:
            for evidence_ref in item["evidenceRefs"]:
                evidence = evidence_by_id.get(evidence_ref)
                if evidence is None:
                    reasons.add("dangling_evidence_ref")
                elif evidence["tenantId"] != tenant_id:
                    reasons.add("cross_tenant_evidence_ref")

    for alias in document["aliases"]:
        target = alias.get("targetAssetId")
        candidates = alias.get("candidateAssetRefs", [])
        if target and target not in asset_by_id or any(item not in asset_by_id for item in candidates):
            reasons.add("dangling_asset_ref")
        if alias["resolutionStatus"] == "pending" and target:
            reasons.add("pending_alias_resolved")

    for relation in document["relationships"]:
        subject = asset_by_id.get(relation["subjectAssetId"])
        obj = asset_by_id.get(relation["objectAssetId"])
        if subject is None or obj is None:
            reasons.add("dangling_asset_ref")
        elif relation["worldType"] == "fact" and (
            subject["identityStatus"] == "pending" or obj["identityStatus"] == "pending"
        ):
            reasons.add("pending_identity_used_in_fact")
        validate_time_range(relation["validTime"], "valid_time_reversed", reasons)
        validate_time_range(relation["recordTime"], "record_time_reversed", reasons)

        prior_id = relation.get("supersedesRelationId")
        if prior_id:
            prior = relation_by_id.get(prior_id)
            if prior is None:
                reasons.add("dangling_relation_ref")
            else:
                prior_to = prior["validTime"].get("to")
                if prior_to is None or parse_time(relation["validTime"]["from"]) < parse_time(prior_to):
                    reasons.add("role_transition_not_closed")
        validate_simulation_boundary(relation, reasons)

    for state in document["worldStates"]:
        asset = asset_by_id.get(state["assetId"])
        if asset is None:
            reasons.add("dangling_asset_ref")
        elif state["worldType"] == "fact" and asset["identityStatus"] == "pending":
            reasons.add("pending_identity_used_in_fact")
        if state["worldType"] == "fact" and not state.get("factAuthorityRef"):
            reasons.add("fact_authority_missing")
        validate_simulation_boundary(state, reasons)

    return reasons


def validate_time_range(time_range: dict[str, str], reason: str, reasons: set[str]) -> None:
    if "to" in time_range and parse_time(time_range["to"]) < parse_time(time_range["from"]):
        reasons.add(reason)


def validate_simulation_boundary(item: dict[str, Any], reasons: set[str]) -> None:
    is_simulation = item["worldType"] == "simulation"
    if is_simulation and not item.get("simulationContext"):
        reasons.add("simulation_context_missing")
    if not is_simulation and item.get("simulationContext"):
        reasons.add("simulation_context_on_non_simulation")
    if is_simulation and (
        item.get("factAuthorityRef")
        or item.get("writebackRequested") is True
        or ("factPromotionCandidate" in item and item["factPromotionCandidate"] is not True)
    ):
        reasons.add("simulation_fact_isolation_broken")


def schema_reasons(validator: Draft202012Validator, document: dict[str, Any]) -> set[str]:
    return {"schema_error"} if list(validator.iter_errors(document)) else set()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--determinism-runs", type=int, default=3)
    args = parser.parse_args()
    if args.determinism_runs < 1:
        raise SystemExit("gcworld_world_model=fail reason=invalid_determinism_runs")

    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    fixtures = load_json(FIXTURES_PATH)
    base = fixtures["baseDocument"]

    positive = 0
    digests: list[str] = []
    for case in fixtures["positiveCases"]:
        document = render_case(base, case)
        reasons = schema_reasons(validator, document) | validate_semantics(document)
        if reasons:
            joined = ",".join(sorted(reasons))
            raise SystemExit(f"gcworld_world_model=fail case={case['name']} reasons={joined}")
        digest = semantic_digest(document)
        for _ in range(args.determinism_runs):
            if semantic_digest(document) != digest:
                raise SystemExit(f"gcworld_world_model=fail case={case['name']} reason=nondeterministic_digest")
        digests.append(digest)
        positive += 1

    negative = 0
    for case in fixtures["negativeCases"]:
        document = render_case(base, case)
        reasons = schema_reasons(validator, document) | validate_semantics(document)
        expected = set(case["expectedReasons"])
        if not expected.issubset(reasons):
            actual = ",".join(sorted(reasons)) or "none"
            missing = ",".join(sorted(expected - reasons))
            raise SystemExit(
                f"gcworld_world_model=fail case={case['name']} missing={missing} actual={actual}"
            )
        negative += 1

    matrix_digest = hashlib.sha256("".join(sorted(digests)).encode("utf-8")).hexdigest()
    print(
        "gcworld_world_model=pass "
        f"positive={positive} negative={negative} determinism_runs={args.determinism_runs} "
        f"matrix_sha256={matrix_digest} kds_writes=0 business_writes=0 status_promotions=0"
    )


if __name__ == "__main__":
    main()
