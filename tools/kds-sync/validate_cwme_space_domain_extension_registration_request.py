#!/usr/bin/env python3
"""Validate the CWME city space domain extension registration request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CWME-SPACE-DOMAIN-EXTENSION-REGISTRATION-REQUEST-001.md"
KDS_ROOT = ROOT.parent / "GlobalCloud KDS"
ATTACHMENTS = [
    KDS_ROOT / "世界资产/世界模型引擎/ontology/cwme-ext.ttl",
    KDS_ROOT / "世界资产/世界模型引擎/ontology/cwme-mapping-v1.yaml",
    KDS_ROOT / "世界资产/世界模型引擎/ontology/cwme-shapes-min.ttl",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path} must contain JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-10-11",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "CWME-SPACE-DOMAIN-EXTENSION-REGISTRATION-REQUEST-20261011", "invalid evidence id")
    require(evidence.get("status") == "request_submitted_pending_governance_review", "invalid status")
    require(evidence.get("scope") == "cwme_city_space_domain_extension_registration_request_only", "invalid scope")
    require(evidence.get("requested_decision") == "register_cwme_city_space_domain_extension_pack", "requested decision mismatch")
    require(evidence.get("current_decision") == "pending_governance_review", "current decision must stay pending")

    pack = evidence.get("extension_pack", {})
    require("cwme-ext.ttl" in str(pack.get("ontology_file", "")), "ontology file ref missing")
    require("cwme-mapping-v1.yaml" in str(pack.get("mapping_file", "")), "mapping file ref missing")
    verified = pack.get("verified", {})
    require(verified.get("triples", 0) >= 150, "verified triples too low")
    require(verified.get("classes", 0) >= 25, "verified class count too low")
    require(verified.get("positive_sample_conforms") is True, "positive sample must conform")
    require(verified.get("negative_sample_violations", 0) >= 5, "negative sample violations too low")

    for attachment in ATTACHMENTS:
        require(attachment.exists(), f"attachment missing: {attachment}")

    pre = evidence.get("admission_preconditions", {})
    for key in [
        "cwme_ext_ttl_initial_exists",
        "mapping_v1_exists",
        "local_verification_pass",
        "no_was_repo_modification",
        "no_xwail_repo_modification",
        "candidate_boundary_retained",
    ]:
        require(pre.get(key) is True, f"precondition must be true: {key}")

    gates = evidence.get("gates", {})
    require(gates.get("request_package_generated") is True, "request package gate must be true")
    require(gates.get("submitted") is True, "submitted gate must be true")
    for key in ["registry_entry_added", "governance_reviewed", "waes_authorized", "accepted", "integrated", "production_ready"]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "CWME-SPACE-DOMAIN-EXTENSION-REGISTRATION-REQUEST-20261011",
        "request_package_generated | true",
        "submitted | true",
        "registry_entry_added | false",
        "governance_reviewed | false",
        "waes_authorized | false",
        "accepted | false",
        "production_ready | false",
        "pending_governance_review",
        "cwme-ext.ttl",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_cwme_space_domain_extension_registration_request.py" in loop_round, "loop round missing validator")
    print(
        "cwme_space_domain_extension_registration_request=pass "
        "requested_decision=register_cwme_city_space_domain_extension_pack "
        "current_decision=pending_governance_review submitted=true registry_entry_added=false "
        "attachments=3/3 verified triples>=150 classes>=25 "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
