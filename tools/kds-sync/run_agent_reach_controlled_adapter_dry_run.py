#!/usr/bin/env python3
"""Run Agent-Reach controlled adapter skeleton in dry-run mode."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/agent-reach/controlled-adapter-dry-run.json"

ALLOWED_COMMANDS = [
    {"kind": "diagnostic", "command": "agent-reach --help", "decision": "allow_dry_run"},
    {"kind": "diagnostic", "command": "agent-reach --version", "decision": "allow_dry_run"},
    {"kind": "health_probe", "command": "agent-reach doctor --json", "decision": "allow_with_probe_record"},
]

BLOCKED_COMMANDS = [
    {"kind": "configuration", "command": "agent-reach configure --from-browser chrome", "block_reason": "credential_required_channel"},
    {"kind": "installer", "command": "agent-reach install --channels opencli", "block_reason": "credential_required_channel"},
    {"kind": "update", "command": "agent-reach check-update", "block_reason": "live_external_search_without_authorization"},
    {"kind": "watch", "command": "agent-reach watch", "block_reason": "live_external_search_without_authorization"},
    {"kind": "transcribe", "command": "agent-reach transcribe <url-or-file>", "block_reason": "credential_required_channel"},
    {"kind": "live_search", "command": "agent-reach <live search/read action>", "block_reason": "live_external_search_without_authorization"},
]

REQUIRED_CANDIDATE_FIELDS = {
    "candidate_id",
    "channel",
    "title",
    "source_url",
    "snippet",
    "evidence_tier",
    "admission_status",
}


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def build_report() -> dict:
    fixture = load_fixture()
    candidates = fixture["candidate_results"]
    expected_blocks = fixture["expected_blocks"]
    schema_valid = all(REQUIRED_CANDIDATE_FIELDS <= set(candidate) for candidate in candidates)
    candidate_only = all(candidate.get("admission_status") == "candidate_only" for candidate in candidates)
    fixture_only = all(candidate.get("evidence_tier") == "fixture_only" for candidate in candidates)

    return {
        "id": "agent-reach-controlled-adapter-dry-run-20260622",
        "round": "GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "controlled_adapter_skeleton_ready",
        "current_admission": "limited_candidate_only",
        "mode": fixture["mode"],
        "query": fixture["query"],
        "requested_channels": fixture["requested_channels"],
        "allowed_commands": ALLOWED_COMMANDS,
        "blocked_commands": BLOCKED_COMMANDS,
        "command_block_reasons": sorted({item["block_reason"] for item in BLOCKED_COMMANDS}),
        "policy_block_reasons": expected_blocks,
        "candidate_result_schema": sorted(REQUIRED_CANDIDATE_FIELDS),
        "candidate_results": candidates,
        "checks": {
            "fixture_loaded": True,
            "candidate_schema_valid": schema_valid,
            "candidate_only": candidate_only,
            "fixture_only": fixture_only,
            "allowed_command_count": len(ALLOWED_COMMANDS),
            "blocked_command_count": len(BLOCKED_COMMANDS),
            "candidate_count": len(candidates),
        },
        "security_controls": {
            "agent_reach_binary_invoked": False,
            "live_external_search_invoked": False,
            "doctor_health_probe_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "next_round": "GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001",
    }


def main() -> None:
    print(json.dumps(build_report(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
