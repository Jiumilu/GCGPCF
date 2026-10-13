#!/usr/bin/env python3
"""Validate the MMC intake readonly capability registration request package.

双态范式（先例：validate_cwme_space_domain_extension_registration_request.py）：
- pending：相关门全 false + md 短语 pending_governance_review；
- accepted：decision_record(date/authority/decision) + governance_reviewed/accepted=true。
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/MMC/evidence/mmc-intake-readonly-capability-registration-request-20261014.json"
EVIDENCE_MD = ROOT / "docs/harness/MMC/evidence/mmc-intake-readonly-capability-registration-request-20261014.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-MMC-INTAKE-REG-001.md"


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
        "last_reviewed: 2026-10-14",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "MMC-INTAKE-READONLY-CAPABILITY-REGISTRATION-REQUEST-20261014", "invalid evidence id")
    require(evidence.get("status") in ("request_submitted_pending_governance_review", "request_accepted"), "invalid status")
    require(evidence.get("scope") == "mmc_intake_readonly_capability_registration_request_only", "invalid scope")
    require(evidence.get("requested_decision") == "admit_intake_readonly_capabilities_into_mmc_catalog", "requested decision mismatch")
    require(evidence.get("current_decision") in ("pending_governance_review", "accepted"), "current decision invalid")

    subject = evidence.get("subject", {})
    caps = subject.get("capabilities_readonly", [])
    require(len(caps) == 6, f"expect 6 readonly capabilities, got {len(caps)}")
    cids = [c.get("capability_id", "") for c in caps]
    for expected in ["intake.xap.health", "intake.xap.requests_list", "intake.xap.request_get",
                     "intake.xap.receipt_get", "intake.xap.publication_get", "intake.xap.projects_list"]:
        require(expected in cids, f"missing capability: {expected}")
    for c in caps:
        require(c.get("method") == "GET", f"readonly capability must be GET: {c.get('capability_id')}")
    require(subject.get("readonly_only") is True, "readonly_only must be true")
    excluded = subject.get("excluded_write_surface", [])
    for w in ["/intake/submit", "/intake/decide", "/intake/publish"]:
        require(w in excluded, f"write surface must be excluded: {w}")

    pre = evidence.get("admission_preconditions", {})
    for key in [
        "source_file_reviewed",
        "readonly_surface_identified",
        "health_endpoint_probed_200",
        "no_waes_repo_modification",
        "no_intake_write_surface_touched",
        "candidate_boundary_retained",
    ]:
        require(pre.get(key) is True, f"precondition must be true: {key}")

    gates = evidence.get("gates", {})
    require(gates.get("request_package_generated") is True, "request package gate must be true")
    require(gates.get("submitted") is True, "submitted gate must be true")
    decision = evidence.get("current_decision")
    if decision == "accepted":
        record = evidence.get("decision_record", {})
        require(record.get("decision") == "accepted" and record.get("date") and record.get("authority"),
                "accepted 状态需 decision_record（decision/date/authority）")
        require(gates.get("governance_reviewed") is True, "accepted 状态 governance_reviewed 必须为 true")
        require(gates.get("accepted") is True, "accepted 状态 accepted 门必须为 true")
        require(gates.get("registry_entry_added") is True or gates.get("registry_entry_added") is False,
                "registry_entry_added 须为布尔")
        for key in ["integrated", "production_ready"]:
            require(gates.get(key) is False, f"gate must be false: {key}")
    else:
        for key in ["registry_entry_added", "governance_reviewed", "wame_authorized", "accepted",
                    "integrated", "production_ready"]:
            require(gates.get(key) is False, f"gate must be false: {key}")

        for phrase in [
            "MMC-INTAKE-READONLY-CAPABILITY-REGISTRATION-REQUEST-20261014",
            "request_package_generated | true",
            "submitted | true",
            "registry_entry_added | false",
            "governance_reviewed | false",
            "wame_authorized | false",
            "accepted | false",
            "production_ready | false",
            "pending_governance_review",
        ]:
            require(phrase in md, f"md missing phrase: {phrase}")

    print(f"PASS: MMC intake readonly capability registration request | status={evidence.get('status')} | decision={decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
