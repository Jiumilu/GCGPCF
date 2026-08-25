#!/usr/bin/env python3
"""确定性校验 GCWORLD 世界原生权限、责任链与失效治理契约。"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import unicodedata
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
SCHEMA_PATH = ARTIFACTS / "gcworld-world-auth.schema.json"
FIXTURES_PATH = ARTIFACTS / "gcworld-world-auth-fixtures.json"
MANIFEST_PATH = ARTIFACTS / "gcworld-world-auth-contract-manifest.yaml"
ID_FIELDS = {
    "worldSnapshots": ("snapshotId", "world-snapshot"),
    "identities": ("identityId", "identity"),
    "roleDefinitions": ("roleDefinitionId", "role-definition"),
    "roleAssignments": ("roleAssignmentId", "role-assignment"),
    "authorizationGrants": ("grantId", "authorization-grant"),
    "delegations": ("delegationId", "delegation"),
    "runtimeDecisions": ("decisionId", "decision"),
    "executionReceipts": ("receiptId", "execution-receipt"),
    "revocations": ("revocationId", "revocation"),
    "derivedArtifacts": ("artifactId", "derived-artifact"),
}
ALLOW_DECISIONS = {"allow", "allow_with_obligations"}
RISK_RANK = {f"R{number}": number for number in range(5)}
CLASSIFICATION_RANK = {f"S{number}": number for number in range(4)}
HIGH_RISK_ACTIONS = {
    "external_communication",
    "funds",
    "contract",
    "identity_change",
    "permission_change",
    "government_communication",
    "business_state_change",
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
        "projectRefs",
        "responsibilityScope",
        "allowedActions",
        "prohibitedActions",
        "resourceScope",
        "actionScope",
        "purposeScope",
        "projectScope",
        "approvalRequirements",
        "evidenceRequirements",
        "grantRefs",
        "delegationRefs",
        "effectiveActionScope",
        "reasonCodes",
        "sourceAuthorizationRefs",
        "sourceClassifications",
        "sourceRestrictions",
        "effectiveRestrictions",
        "cascadeTargets",
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


def validate_references_and_time(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    identities = {item["identityId"]: item for item in document["identities"]}
    roles = {item["roleDefinitionId"]: item for item in document["roleDefinitions"]}
    assignments = {item["roleAssignmentId"]: item for item in document["roleAssignments"]}
    grants = {item["grantId"]: item for item in document["authorizationGrants"]}
    delegations = {item["delegationId"]: item for item in document["delegations"]}
    snapshots = {item["snapshotId"]: item for item in document["worldSnapshots"]}
    decisions = {item["decisionId"]: item for item in document["runtimeDecisions"]}

    for snapshot in snapshots.values():
        if parse_time(snapshot["expiresAt"]) <= parse_time(snapshot["issuedAt"]):
            reasons.add("snapshot_time_reversed")
    for assignment in assignments.values():
        if assignment["subjectIdentityId"] not in identities or assignment["roleDefinitionId"] not in roles:
            reasons.add("dangling_role_assignment_ref")
        if parse_time(assignment["expiresAt"]) <= parse_time(assignment["validFrom"]):
            reasons.add("role_assignment_time_reversed")
    for grant in grants.values():
        required_ids = {grant["grantorIdentityId"], grant["granteeIdentityId"], *grant["approvalRequirements"]}
        if not required_ids.issubset(identities) or grant["roleAssignmentId"] not in assignments:
            reasons.add("dangling_grant_ref")
        if parse_time(grant["expiresAt"]) <= parse_time(grant["validFrom"]):
            reasons.add("grant_time_reversed")
    for delegation in delegations.values():
        if (
            delegation["parentGrantId"] not in grants
            or delegation["delegatorIdentityId"] not in identities
            or delegation["delegateeIdentityId"] not in identities
        ):
            reasons.add("dangling_delegation_ref")
        if parse_time(delegation["expiresAt"]) <= parse_time(delegation["validFrom"]):
            reasons.add("delegation_time_reversed")
    for decision in decisions.values():
        refs_present = (
            decision["principalIdentityId"] in identities
            and decision["actorIdentityId"] in identities
            and decision["roleAssignmentId"] in assignments
            and decision["worldSnapshotId"] in snapshots
            and set(decision["grantRefs"]).issubset(grants)
            and set(decision["delegationRefs"]).issubset(delegations)
        )
        if decision.get("actingAgentIdentityId") and decision["actingAgentIdentityId"] not in identities:
            refs_present = False
        if not refs_present:
            reasons.add("dangling_decision_ref")
        if parse_time(decision["expiresAt"]) <= parse_time(decision["issuedAt"]):
            reasons.add("decision_time_reversed")
    for receipt in document["executionReceipts"]:
        if receipt["decisionId"] not in decisions or receipt["executorIdentityId"] not in identities:
            reasons.add("dangling_receipt_ref")
    return reasons


def validate_decisions(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    identities = {item["identityId"]: item for item in document["identities"]}
    roles = {item["roleDefinitionId"]: item for item in document["roleDefinitions"]}
    assignments = {item["roleAssignmentId"]: item for item in document["roleAssignments"]}
    grants = {item["grantId"]: item for item in document["authorizationGrants"]}
    delegations = {item["delegationId"]: item for item in document["delegations"]}
    snapshots = {item["snapshotId"]: item for item in document["worldSnapshots"]}
    state = document["systemState"]

    for decision in document["runtimeDecisions"]:
        assignment = assignments.get(decision["roleAssignmentId"])
        snapshot = snapshots.get(decision["worldSnapshotId"])
        selected_grants = [grants[item] for item in decision["grantRefs"] if item in grants]
        selected_delegations = [delegations[item] for item in decision["delegationRefs"] if item in delegations]
        principal = identities.get(decision["principalIdentityId"])
        actor = identities.get(decision["actorIdentityId"])
        agent = identities.get(decision.get("actingAgentIdentityId", ""))
        allowed = decision["decision"] in ALLOW_DECISIONS

        identity_chain = [item for item in (principal, actor, agent) if item is not None]
        if allowed and any(item["status"] != "confirmed" for item in identity_chain):
            reasons.add("identity_not_confirmed")
        if allowed and assignment is not None and assignment["status"] != "active":
            reasons.add("inactive_role_allowed")
        if allowed and assignment is not None and assignment["worldType"] != "fact":
            reasons.add("non_fact_authority_expansion")
        if allowed and any(grant["status"] != "active" or grant["worldType"] != "fact" for grant in selected_grants):
            reasons.add("inactive_grant_allowed")
        if allowed and any(item["status"] != "active" for item in selected_delegations):
            reasons.add("inactive_delegation_allowed")

        if snapshot is not None:
            if decision["evaluatedVersions"] != snapshot["versions"]:
                reasons.add("snapshot_version_mismatch")
            if parse_time(snapshot["expiresAt"]) <= parse_time(decision["issuedAt"]):
                reasons.add("snapshot_expired")

        if allowed and (not state["contextComplete"] or not state["factVersionsVerified"]):
            reasons.add("default_deny_broken")
        if not state["waesAvailable"]:
            if allowed or decision["requestedAction"] in HIGH_RISK_ACTIONS or RISK_RANK[decision["riskLevel"]] >= 3:
                reasons.add("degraded_high_risk_allowed")
            elif decision["decision"] != "degraded_readonly" or set(decision["effectiveActionScope"]) != {"observation"}:
                reasons.add("degraded_readonly_boundary_broken")

        if assignment is not None and assignment["roleDefinitionId"] in roles:
            role = roles[assignment["roleDefinitionId"]]
            effective = set(role["allowedActions"])
            prohibited = set(role["prohibitedActions"])
            risk_ceiling = RISK_RANK[role["riskCeiling"]]
            for grant in selected_grants:
                effective &= set(grant["actionScope"])
                prohibited |= set(grant["prohibitedActions"])
                risk_ceiling = min(risk_ceiling, RISK_RANK[grant["riskCeiling"]])
            for delegation in selected_delegations:
                effective &= set(delegation["actionScope"])
            if agent is not None:
                effective &= set(agent.get("agentActionScope", []))
            effective -= prohibited
            if set(decision["effectiveActionScope"]) != effective and allowed:
                reasons.add("effective_scope_mismatch")
            if allowed and decision["requestedAction"] not in effective:
                reasons.add("intersection_principle_broken")
            if allowed and RISK_RANK[decision["riskLevel"]] > risk_ceiling:
                reasons.add("risk_ceiling_exceeded")
            if agent is not None and allowed and decision["requestedAction"] not in set(agent.get("agentActionScope", [])):
                reasons.add("agent_scope_exceeded")

        controllers_by_stage: dict[str, set[str]] = {}
        for stage in decision["controlChain"]:
            controllers_by_stage.setdefault(stage["stage"], set()).add(stage["ultimateControllerAssetId"])
            identity = identities.get(stage["actorIdentityId"])
            if identity is not None and identity["ultimateControllerAssetId"] != stage["ultimateControllerAssetId"]:
                reasons.add("control_chain_identity_mismatch")
        if controllers_by_stage.get("propose", set()) & controllers_by_stage.get("approve", set()):
            reasons.add("separation_of_duties_broken")
    return reasons


def validate_delegations_and_emergency(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    grants = {item["grantId"]: item for item in document["authorizationGrants"]}
    for delegation in document["delegations"]:
        grant = grants.get(delegation["parentGrantId"])
        if grant is None:
            continue
        if not set(delegation["actionScope"]).issubset(grant["actionScope"]):
            reasons.add("delegation_scope_exceeded")
        if not grant["canRedelegate"] or delegation["depth"] > grant["maxDelegationDepth"]:
            reasons.add("delegation_depth_exceeded")
        if parse_time(delegation["expiresAt"]) > parse_time(grant["expiresAt"]):
            reasons.add("delegation_time_exceeded")

    for grant in grants.values():
        if not grant["emergency"]:
            continue
        valid_window = parse_time(grant["expiresAt"]) - parse_time(grant["validFrom"])
        valid = (
            valid_window <= timedelta(hours=8)
            and len(set(grant["approvalRequirements"])) >= 2
            and not grant["canRedelegate"]
            and grant["maxDelegationDepth"] == 0
            and grant.get("postReviewRequired") is True
            and bool(grant.get("emergencyJustification"))
        )
        if not valid:
            reasons.add("emergency_grant_invalid")
    return reasons


def validate_receipts(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    decisions = {item["decisionId"]: item for item in document["runtimeDecisions"]}
    for receipt in document["executionReceipts"]:
        decision = decisions.get(receipt["decisionId"])
        if decision is None:
            continue
        if receipt["externalSideEffect"]:
            reasons.add("real_side_effect_forbidden")
        if receipt["result"] == "succeeded":
            if decision["precommitRevalidationRequired"] and not receipt["precommitRevalidated"]:
                reasons.add("precommit_revalidation_missing")
            if receipt["revalidatedVersions"] != decision["evaluatedVersions"]:
                reasons.add("precommit_version_mismatch")
            if receipt["performedAction"] != decision["requestedAction"]:
                reasons.add("receipt_action_mismatch")
            required = {item["obligationId"] for item in decision["obligations"]}
            evidenced = {item["obligationId"] for item in receipt["obligationEvidence"]}
            if not required.issubset(evidenced):
                reasons.add("obligation_evidence_missing")
    return reasons


def validate_revocations_and_derivations(document: dict[str, Any]) -> set[str]:
    reasons: set[str] = set()
    grants = {item["grantId"]: item for item in document["authorizationGrants"]}
    delegations = {item["delegationId"]: item for item in document["delegations"]}
    derived = {item["artifactId"]: item for item in document["derivedArtifacts"]}

    for revocation in document["revocations"]:
        if revocation["targetType"] != "role_assignment":
            continue
        dependent_grants = {
            grant["grantId"] for grant in grants.values() if grant["roleAssignmentId"] == revocation["targetId"]
        }
        dependent_delegations = {
            item["delegationId"] for item in delegations.values() if item["parentGrantId"] in dependent_grants
        }
        dependent_artifacts = {
            item["artifactId"]
            for item in derived.values()
            if set(item["sourceAuthorizationRefs"]) & dependent_grants
        }
        expected = dependent_grants | dependent_delegations | dependent_artifacts
        status_applied = (
            all(grants[item]["status"] in {"revoked", "frozen"} for item in dependent_grants)
            and all(delegations[item]["status"] in {"revoked", "frozen"} for item in dependent_delegations)
            and all(derived[item]["revocationStatus"] in {"frozen", "deleted"} for item in dependent_artifacts)
        )
        if not expected.issubset(revocation["cascadeTargets"]) or not status_applied:
            reasons.add("cascade_revocation_incomplete")

    for artifact in derived.values():
        strongest = max(CLASSIFICATION_RANK[item] for item in artifact["sourceClassifications"])
        restrictions_preserved = set(artifact["sourceRestrictions"]).issubset(artifact["effectiveRestrictions"])
        memory_preserved = "no_long_term_memory" not in artifact["effectiveRestrictions"] or not artifact["memoryAllowed"]
        if CLASSIFICATION_RANK[artifact["classification"]] < strongest or not restrictions_preserved or not memory_preserved:
            reasons.add("derived_restriction_downgrade")
    return reasons


def validate_semantics(document: dict[str, Any]) -> set[str]:
    reasons = validate_stable_ids(document)
    reasons |= validate_references_and_time(document)
    reasons |= validate_decisions(document)
    reasons |= validate_delegations_and_emergency(document)
    reasons |= validate_receipts(document)
    reasons |= validate_revocations_and_derivations(document)
    return reasons


def validate_manifest() -> None:
    payload = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("gcworld_world_auth=fail reason=manifest_invalid")
    for item in payload.get("artifacts", []):
        path = ROOT / item["path"]
        if not path.is_file():
            raise SystemExit(f"gcworld_world_auth=fail reason=manifest_file_missing path={item['path']}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            raise SystemExit(f"gcworld_world_auth=fail reason=manifest_hash_mismatch path={item['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--determinism-runs", type=int, default=3)
    args = parser.parse_args()
    if args.determinism_runs < 1:
        raise SystemExit("gcworld_world_auth=fail reason=invalid_determinism_runs")

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
            joined = ",".join(sorted(reasons))
            raise SystemExit(f"gcworld_world_auth=fail case={case['name']} reasons={joined}")
        digest = semantic_digest(document)
        for _ in range(args.determinism_runs):
            if semantic_digest(document) != digest:
                raise SystemExit(f"gcworld_world_auth=fail case={case['name']} reason=nondeterministic_digest")
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
            raise SystemExit(f"gcworld_world_auth=fail case={case['name']} missing={missing} actual={actual}")
        negative += 1

    validate_manifest()
    matrix_digest = hashlib.sha256("".join(sorted(digests)).encode("utf-8")).hexdigest()
    print(
        "gcworld_world_auth=pass "
        f"positive={positive} negative={negative} object_types={len(ID_FIELDS)} "
        f"determinism_runs={args.determinism_runs} matrix_sha256={matrix_digest} "
        "real_authorizations=0 kds_writes=0 business_writes=0 external_writes=0 status_promotions=0"
    )


if __name__ == "__main__":
    main()
