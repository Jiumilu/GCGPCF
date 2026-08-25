#!/usr/bin/env python3
"""确定性校验 GCWORLD 职能智能体注册、行动信封和执行账本。"""

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
SCHEMA_PATH = ARTIFACTS / "gcworld-role-agent-governance.schema.json"
FIXTURES_PATH = ARTIFACTS / "gcworld-role-agent-governance-fixtures.json"
MANIFEST_PATH = ARTIFACTS / "gcworld-role-agent-governance-contract-manifest.yaml"
ID_FIELDS = {
    "registrations": ("agentId", "agent"),
    "actionEnvelopes": ("envelopeId", "envelope"),
    "executionLedger": ("ledgerEntryId", "ledger"),
}
RISK_RANK = {f"R{number}": number for number in range(5)}
HIGH_IMPACT_ACTIONS = {
    "external_communication",
    "funds",
    "contract",
    "identity_change",
    "permission_change",
    "government_communication",
    "business_state_change",
}
MINIMUM_RISK = {
    "external_communication": 3,
    "funds": 4,
    "contract": 3,
    "identity_change": 3,
    "permission_change": 4,
    "government_communication": 4,
    "business_state_change": 3,
}
MODE_ALLOWED = {
    "mirror": {"observation"},
    "assist": {"observation", "advice", "draft"},
    "delegated": None,
    "autonomous": {"observation", "advice", "draft", "internal_write"},
}
EXPECTED_MODES = {"mirror", "assist", "delegated", "autonomous"}
EXPECTED_LEDGER_OUTCOMES = {
    "advised",
    "drafted",
    "approved_executed",
    "rejected",
    "failed",
    "blocked",
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
        for item in canonical[collection]:
            for field in (
                "contextRefs",
                "sourceScopeRefs",
                "capabilities",
                "knowledgeScopeRefs",
                "toolScope",
                "connectorScope",
                "authorizationRefs",
                "allowedActions",
                "prohibitedActions",
                "evidenceRefs",
                "reasonCodes",
            ):
                if isinstance(item.get(field), list):
                    item[field].sort()
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def validate_semantics(document: dict[str, Any]) -> set[str]:
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

    agents = {item["agentId"]: item for item in document["registrations"]}
    envelopes = {item["envelopeId"]: item for item in document["actionEnvelopes"]}

    for agent in document["registrations"]:
        if parse_time(agent["expiresAt"]) <= parse_time(agent["validFrom"]):
            reasons.add("registration_time_reversed")
        if set(agent["allowedActions"]) & set(agent["prohibitedActions"]):
            reasons.add("action_policy_overlap")
        if agent["mode"] == "mirror" and (
            agent["riskCeiling"] != "R0" or set(agent["allowedActions"]) != {"observation"}
        ):
            reasons.add("mode_registration_invalid")
        if agent["mode"] == "assist" and RISK_RANK[agent["riskCeiling"]] > 1:
            reasons.add("mode_registration_invalid")
        if agent["mode"] == "autonomous" and RISK_RANK[agent["riskCeiling"]] > 2:
            reasons.add("mode_registration_invalid")

    for envelope in document["actionEnvelopes"]:
        agent = agents.get(envelope["agentId"])
        if agent is None:
            reasons.add("dangling_agent_ref")
            continue
        action = envelope["actionType"]
        allowed = envelope["decision"] == "allowed"
        risk = RISK_RANK[envelope["riskLevel"]]

        minimum_risk = MINIMUM_RISK.get(action)
        if minimum_risk is not None and risk < minimum_risk:
            reasons.add("high_impact_risk_too_low")

        if allowed and risk > RISK_RANK[agent["riskCeiling"]]:
            reasons.add("risk_ceiling_exceeded")
        if allowed and (action not in agent["allowedActions"] or action in agent["prohibitedActions"]):
            reasons.add("prohibited_action_requested")

        mode_allowed = MODE_ALLOWED[agent["mode"]]
        if allowed and mode_allowed is not None and action not in mode_allowed:
            reasons.add("mode_boundary_broken")
        if allowed and agent["mode"] == "autonomous" and (risk > 2 or action in HIGH_IMPACT_ACTIONS):
            reasons.add("autonomous_high_risk_action")

        if allowed and action in HIGH_IMPACT_ACTIONS:
            authorization_ready = (
                envelope["authorizationStatus"] == "granted"
                and bool(envelope.get("authorizationDecisionRef"))
            )
            confirmation_ready = (
                envelope["confirmationStatus"] == "confirmed"
                and bool(envelope.get("humanConfirmationRef"))
            )
            if not authorization_ready or not confirmation_ready:
                reasons.add("high_impact_default_deny_broken")

        if action in {"observation", "advice", "draft"} and envelope["zeroWrite"] is not True:
            reasons.add("zero_write_boundary_broken")
        if envelope["decision"] == "blocked" and envelope["zeroWrite"] is not True:
            reasons.add("blocked_side_effect")

    for entry in document["executionLedger"]:
        envelope = envelopes.get(entry["envelopeId"])
        if envelope is None:
            reasons.add("dangling_envelope_ref")
            continue
        if entry["agentId"] != envelope["agentId"]:
            reasons.add("ledger_agent_mismatch")
        if entry["outcome"] in {"blocked", "rejected"} and entry["externalSideEffect"]:
            reasons.add("blocked_side_effect")
        if entry["outcome"] in {"advised", "drafted"} and entry["externalSideEffect"]:
            reasons.add("advisory_side_effect")
        if entry["outcome"] == "approved_executed" and envelope["decision"] != "allowed":
            reasons.add("execution_without_allow")
        if entry["outcome"] == "failed" and envelope["decision"] != "allowed":
            reasons.add("failure_without_execution_attempt")

    return reasons


def schema_reasons(validator: Draft202012Validator, document: dict[str, Any]) -> set[str]:
    return {"schema_error"} if list(validator.iter_errors(document)) else set()


def validate_manifest() -> None:
    payload = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("gcworld_role_agent_governance=fail reason=manifest_invalid")
    for item in payload.get("artifacts", []):
        path = ROOT / item["path"]
        if not path.is_file():
            raise SystemExit(f"gcworld_role_agent_governance=fail reason=manifest_file_missing path={item['path']}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            raise SystemExit(f"gcworld_role_agent_governance=fail reason=manifest_hash_mismatch path={item['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--determinism-runs", type=int, default=3)
    args = parser.parse_args()
    if args.determinism_runs < 1:
        raise SystemExit("gcworld_role_agent_governance=fail reason=invalid_determinism_runs")

    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    fixtures = load_json(FIXTURES_PATH)
    base = fixtures["baseDocument"]

    positive = 0
    digests: list[str] = []
    observed_modes: set[str] = set()
    observed_outcomes: set[str] = set()
    for case in fixtures["positiveCases"]:
        document = render_case(base, case)
        reasons = schema_reasons(validator, document) | validate_semantics(document)
        if reasons:
            joined = ",".join(sorted(reasons))
            raise SystemExit(f"gcworld_role_agent_governance=fail case={case['name']} reasons={joined}")
        digest = semantic_digest(document)
        for _ in range(args.determinism_runs):
            if semantic_digest(document) != digest:
                raise SystemExit(
                    f"gcworld_role_agent_governance=fail case={case['name']} reason=nondeterministic_digest"
                )
        digests.append(digest)
        observed_modes.update(item["mode"] for item in document["registrations"])
        observed_outcomes.update(item["outcome"] for item in document["executionLedger"])
        positive += 1

    if observed_modes != EXPECTED_MODES:
        raise SystemExit("gcworld_role_agent_governance=fail reason=mode_coverage_incomplete")
    if observed_outcomes != EXPECTED_LEDGER_OUTCOMES:
        raise SystemExit("gcworld_role_agent_governance=fail reason=ledger_outcome_coverage_incomplete")

    negative = 0
    for case in fixtures["negativeCases"]:
        document = render_case(base, case)
        reasons = schema_reasons(validator, document) | validate_semantics(document)
        expected = set(case["expectedReasons"])
        if not expected.issubset(reasons):
            actual = ",".join(sorted(reasons)) or "none"
            missing = ",".join(sorted(expected - reasons))
            raise SystemExit(
                f"gcworld_role_agent_governance=fail case={case['name']} missing={missing} actual={actual}"
            )
        negative += 1

    validate_manifest()
    matrix_digest = hashlib.sha256("".join(sorted(digests)).encode("utf-8")).hexdigest()
    print(
        "gcworld_role_agent_governance=pass "
        f"positive={positive} negative={negative} modes={len(observed_modes)} "
        f"ledger_outcomes={len(observed_outcomes)} determinism_runs={args.determinism_runs} "
        f"matrix_sha256={matrix_digest} kds_writes=0 mmc_writes=0 "
        "business_writes=0 external_writes=0 status_promotions=0"
    )


if __name__ == "__main__":
    main()
