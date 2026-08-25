#!/usr/bin/env python3
"""确定性校验 GCWORLD 工作中心、资产档案、权限裁剪和多租户共享契约。"""

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
SCHEMA_PATH = ARTIFACTS / "gcworld-workbench.schema.json"
FIXTURES_PATH = ARTIFACTS / "gcworld-workbench-fixtures.json"
MANIFEST_PATH = ARTIFACTS / "gcworld-workbench-contract-manifest.yaml"

EXPECTED_CENTERS = {
    "world_overview", "organization_assets", "relation_network", "project_world",
    "time_events", "agents", "actions_collaboration", "permissions_identity",
    "simulation_lab", "fact_governance", "governance_audit", "development_operations",
}
PROFILE_SECTIONS = {
    "facts", "history", "aliases", "relationships", "roles", "capabilities",
    "permissions", "tasks", "actions", "results", "feedback", "evidence", "conflicts",
}
PROJECTION_SURFACES = {
    "field", "paragraph", "graph", "search", "timeline", "aggregate", "export", "agent_answer",
}
COLLECTION_IDS = {
    "workCenters": "centerId",
    "navigationTransitions": "transitionId",
    "assetProfiles": "profileId",
    "projectionPolicies": "policyId",
    "collaborationSpaces": "spaceId",
    "sharingContracts": "shareId",
    "shareAccessChecks": "checkId",
    "explanationRecords": "explanationId",
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
        "evidenceRefs", "sourceEvidenceRefs", "receiptRefs", "sections",
        "mergedCandidateRefs", "organizationRefs", "projectRefs", "memberTenantIds",
        "objectRefs", "fieldScope", "purposeScope", "usageEvidenceRefs",
    }

    def normalize(value: Any, field: str | None = None) -> Any:
        if isinstance(value, dict):
            return {key: normalize(item, key) for key, item in sorted(value.items())}
        if isinstance(value, list):
            items = [normalize(item) for item in value]
            if field in unordered_fields:
                return sorted(items, key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True))
            if field == "decisions":
                return sorted(items, key=lambda item: item["surface"])
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


def validate_centers_and_navigation(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    centers = document["workCenters"]
    center_types = [item["centerType"] for item in centers]
    center_ids = {item["centerId"] for item in centers}
    if len(center_types) != len(set(center_types)):
        reasons.add("work_center_duplicate")
    if len(center_types) != len(EXPECTED_CENTERS) or set(center_types) != EXPECTED_CENTERS:
        reasons.add("work_centers_incomplete")
    snapshots = {item["worldSnapshotRef"] for item in centers}
    permissions = {item["permissionContextRef"] for item in centers}
    semantics = {item["assetIdSemantics"] for item in centers}
    if len(snapshots) != 1 or len(permissions) != 1 or semantics != {"worldAssetId"}:
        reasons.add("work_center_context_inconsistent")

    for transition in document["navigationTransitions"]:
        if transition["fromCenter"] not in center_ids or transition["toCenter"] not in center_ids:
            reasons.add("navigation_center_missing")
        if transition["assetIdBefore"] != transition["assetIdAfter"]:
            reasons.add("navigation_asset_context_changed")
        if transition["worldSnapshotBefore"] != transition["worldSnapshotAfter"]:
            reasons.add("navigation_snapshot_context_changed")
        if transition["permissionContextBefore"] != transition["permissionContextAfter"]:
            reasons.add("navigation_permission_context_changed")
    return reasons


def validate_profiles(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    asset_ids: set[str] = set()
    for profile in document["assetProfiles"]:
        if profile["worldAssetId"] in asset_ids:
            reasons.add("multiple_profiles_for_asset")
        asset_ids.add(profile["worldAssetId"])
        sections = profile["sections"]
        if len(sections) != len(set(sections)) or set(sections) != PROFILE_SECTIONS:
            reasons.add("profile_sections_incomplete")
        unresolved = {item["candidateRef"] for item in profile["unresolvedIdentityCandidates"]}
        if unresolved.intersection(profile["mergedCandidateRefs"]):
            reasons.add("unresolved_identity_silently_merged")
    return reasons


def validate_projections(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    for policy in document["projectionPolicies"]:
        decisions = policy["decisions"]
        surfaces = [item["surface"] for item in decisions]
        if len(surfaces) != len(set(surfaces)) or set(surfaces) != PROJECTION_SURFACES:
            reasons.add("projection_surfaces_incomplete")
        expected = policy["expectedDecision"]
        for decision in decisions:
            surface = decision["surface"]
            if decision["decision"] != expected:
                reasons.add("projection_decision_inconsistent")
                if expected in {"deny", "redact"} and decision["decision"] == "allow":
                    reasons.add(f"{surface}_projection_leak")
            if expected == "deny" and decision["dataVisible"]:
                reasons.add(f"{surface}_projection_leak")
            if expected in {"deny", "redact"} and decision["countDisclosed"]:
                if surface == "aggregate":
                    reasons.add("aggregate_inference_leak")
                else:
                    reasons.add(f"{surface}_projection_leak")
        if policy["classification"] in {"S2", "S3"} and expected == "allow" and policy["shareContractRef"] is None:
            reasons.add("sensitive_projection_without_share")
    return reasons


def validate_sharing(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    spaces = {item["spaceId"]: item for item in document["collaborationSpaces"]}
    shares = {item["shareId"]: item for item in document["sharingContracts"]}

    for space in spaces.values():
        if not space["isolationEnforced"]:
            reasons.add("collaboration_space_isolation_disabled")
    for share in shares.values():
        space = spaces.get(share["spaceId"])
        if space is None:
            reasons.add("sharing_space_missing")
        elif not {share["sourceTenantId"], share["targetTenantId"]}.issubset(set(space["memberTenantIds"])):
            reasons.add("sharing_tenant_outside_space")
        if share["sourceTenantId"] != share["targetTenantId"] and (
            not share["objectRefs"]
            or not share["fieldScope"]
            or not share["purposeScope"]
            or not share["revocationMethod"]
        ):
            reasons.add("sharing_contract_scope_incomplete")
        if parse_time(share["validFrom"]) >= parse_time(share["validUntil"]):
            reasons.add("sharing_validity_reversed")
        if share["status"] == "active" and share["revokedAt"] is not None:
            reasons.add("active_share_has_revocation_time")
        if share["status"] == "revoked":
            if share["revokedAt"] is None:
                reasons.add("revoked_share_time_missing")
            if not share["usageEvidenceRefs"]:
                reasons.add("revoked_share_usage_evidence_missing")

    for check in document["shareAccessChecks"]:
        share = shares.get(check["shareId"])
        if share is None:
            reasons.add("share_access_contract_missing")
            continue
        checked_at = parse_time(check["checkedAt"])
        revoked_at = parse_time(share["revokedAt"]) if share["revokedAt"] else None
        if share["status"] == "revoked" and revoked_at is not None and checked_at >= revoked_at:
            if check["decision"] != "deny" or check["dataReturned"] or check["aggregateDisclosed"]:
                reasons.add("revoked_share_access_continues")
        if checked_at < parse_time(share["validFrom"]) or checked_at >= parse_time(share["validUntil"]):
            if check["decision"] != "deny" or check["dataReturned"] or check["aggregateDisclosed"]:
                reasons.add("share_access_outside_validity")
    return reasons


def validate_semantics(document: dict[str, Any]) -> set[str]:
    reasons = validate_unique_ids(document)
    reasons |= validate_centers_and_navigation(document)
    reasons |= validate_profiles(document)
    reasons |= validate_projections(document)
    reasons |= validate_sharing(document)
    return reasons


def validate_manifest() -> None:
    payload = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("gcworld_workbench=fail reason=manifest_invalid")
    for item in payload.get("artifacts", []):
        path = ROOT / item["path"]
        if not path.is_file():
            raise SystemExit(f"gcworld_workbench=fail reason=manifest_file_missing path={item['path']}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            raise SystemExit(f"gcworld_workbench=fail reason=manifest_hash_mismatch path={item['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--determinism-runs", type=int, default=3)
    args = parser.parse_args()
    if args.determinism_runs < 1:
        raise SystemExit("gcworld_workbench=fail reason=invalid_determinism_runs")

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
            raise SystemExit(f"gcworld_workbench=fail case={case['name']} reasons={','.join(sorted(reasons))}")
        digest = semantic_digest(document)
        for _ in range(args.determinism_runs):
            if semantic_digest(document) != digest:
                raise SystemExit(f"gcworld_workbench=fail case={case['name']} reason=nondeterministic_digest")
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
            raise SystemExit(f"gcworld_workbench=fail case={case['name']} missing={missing} actual={actual}")
        negative += 1

    validate_manifest()
    matrix_digest = hashlib.sha256("".join(sorted(digests)).encode("utf-8")).hexdigest()
    print(
        "gcworld_workbench=pass "
        f"positive={positive} negative={negative} work_centers={len(EXPECTED_CENTERS)} "
        f"profile_sections={len(PROFILE_SECTIONS)} projection_surfaces={len(PROJECTION_SURFACES)} "
        f"determinism_runs={args.determinism_runs} matrix_sha256={matrix_digest} "
        "real_cross_tenant_shares=0 kds_writes=0 business_writes=0 "
        "external_writes=0 deployments=0 status_promotions=0"
    )


if __name__ == "__main__":
    main()
