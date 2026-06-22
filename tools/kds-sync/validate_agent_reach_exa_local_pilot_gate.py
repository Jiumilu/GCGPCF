#!/usr/bin/env python3
"""Validate Agent-Reach Exa local pilot authorization gate."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION = ROOT / "docs/harness/evidence/agent-reach-exa-local-pilot-authorization.json"
AUTH_TEMPLATE = ROOT / "docs/harness/evidence/agent-reach-exa-local-pilot-authorization.template.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-exa-local-pilot-gate-20260620.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-exa-local-pilot-gate-20260620.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-LOCAL-PILOT-GATE-001.md"

REQUIRED_AUTH_FIELDS = [
    "authorized_mode",
    "authorized_scope",
    "authorized_projects",
    "allow_network_download",
    "allow_npm_package_install",
    "allow_global_npm_install",
    "allow_project_dependency_change",
    "allow_mcp_configuration_change",
    "allow_exa_mcp_registration",
    "allow_cookie_or_login_state",
    "allow_production_write",
    "allow_kds_canonical_write",
    "rollback_required",
    "rollback_deadline_minutes",
    "acceptance_required",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str, source_path: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    metadata = text[:end]
    for key in [
        "doc_id:",
        "title:",
        "project:",
        "related_projects:",
        "domain:",
        "status:",
        "version:",
        "owner:",
        "kds_space:",
        "kds_path:",
        "source_path:",
        "sync_direction:",
        "last_reviewed:",
        "supersedes:",
        "superseded_by:",
    ]:
        require(key in metadata, f"{path.relative_to(ROOT)} missing front matter key {key}")
    require(f"source_path: {source_path}" in metadata, f"{path.relative_to(ROOT)} source_path mismatch")


def validate_authorization(auth: dict) -> None:
    for field in REQUIRED_AUTH_FIELDS:
        require(field in auth, f"authorization missing field: {field}")
    require(auth["authorized_mode"] == "agent-reach-exa-local-pilot", "invalid authorized_mode")
    require(auth["allow_network_download"] is True, "network download must be explicit true")
    require(auth["allow_npm_package_install"] is True, "npm package install must be explicit true")
    require(auth["allow_global_npm_install"] is False, "global npm install must remain false")
    require(auth["allow_project_dependency_change"] is False, "project dependency change must remain false")
    require(auth["allow_mcp_configuration_change"] is True, "MCP configuration change must be explicit true")
    require(auth["allow_exa_mcp_registration"] is True, "Exa MCP registration must be explicit true")
    require(auth["allow_cookie_or_login_state"] is False, "cookies/login state must remain false")
    require(auth["allow_production_write"] is False, "production write must remain false")
    require(auth["allow_kds_canonical_write"] is False, "KDS canonical write must remain false")
    require(auth["rollback_required"] is True, "rollback_required must be true")
    require(auth["acceptance_required"] is True, "acceptance_required must be true")


def main() -> int:
    template = load_json(AUTH_TEMPLATE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/agent-reach-exa-local-pilot-gate-20260620.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-LOCAL-PILOT-GATE-001.md",
    )

    for field in REQUIRED_AUTH_FIELDS:
        require(field in template, f"authorization template missing field: {field}")

    require(evidence.get("evidence_id") == "AGENT-REACH-EXA-LOCAL-PILOT-GATE-20260620", "invalid evidence id")
    require(evidence.get("status") == "authorization_required", "gate must remain authorization_required")
    authorization_present = AUTHORIZATION.exists()
    if not authorization_present:
        require(evidence.get("authorization_file_present") is False, "evidence must record absent authorization")
        require(evidence.get("execution_allowed") is False, "execution must not be allowed")
    require(evidence.get("installation_performed") is False, "installation must be false")
    require(evidence.get("mcp_configuration_changed") is False, "MCP config must remain unchanged")
    require(evidence.get("exa_mcp_registered") is False, "Exa MCP registration must be false")
    require(evidence.get("exa_search_verified") is False, "Exa search verification must be false")
    require(evidence.get("cookies_configured") is False, "cookies must remain false")
    require(evidence.get("production_write_count") == 0, "production write count must be zero")
    require(evidence.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")
    require(evidence.get("credential_leakage_count") == 0, "credential leakage count must be zero")
    require(evidence.get("status_upgrade_allowed") is False, "status upgrade must be false")

    if authorization_present:
        validate_authorization(load_json(AUTHORIZATION))
    else:
        require("authorization_file_present | false" in evidence_md, "markdown must record missing authorization")
        require("status=authorization_required" in loop_round, "loop round must record authorization_required")

    require(shutil.which("mcporter") is None, "gate expects no mcporter install before explicit authorization")

    print(
        "agent_reach_exa_local_pilot_gate=pass "
        f"status=authorization_required authorization_file_present={str(authorization_present).lower()} "
        "execution_allowed=false installation_performed=false "
        "mcp_configuration_changed=false exa_search_verified=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
