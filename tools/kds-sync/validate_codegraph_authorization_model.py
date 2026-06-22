#!/usr/bin/env python3
"""Validate CodeGraph authorization model artifacts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PERMISSIONS = ROOT / "governance/codegraph/agent-codegraph-permissions.yaml"
DOC = ROOT / "docs/codegraph/codegraph-authorization-model.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    permissions = read(PERMISSIONS)
    doc = read(DOC)

    required_sections = [
        "tool_authorization:",
        "repo_authorization:",
        "agent_authorization:",
        "loop_codegraph_permissions:",
        "kds_authorization:",
        "human_roles:",
    ]
    for section in required_sections:
        require(section in permissions, f"permissions missing section: {section}")

    required_denials = [
        "modify_source_files",
        "commit_code",
        "push_code",
        "access_secrets",
        "promote_kds_accepted_fact",
        "approve_waes_gate",
        "accepted_status_upgrade",
        "integrated_status_upgrade",
        "production_ready_status_upgrade",
    ]
    for denial in required_denials:
        require(denial in permissions, f"permissions missing denial: {denial}")

    for agent in ["codex_agent", "review_agent", "test_agent", "doc_agent", "waes_agent", "loop_agent"]:
        require(f"  {agent}:" in permissions, f"permissions missing agent: {agent}")

    for role in ["project_owner", "tech_lead", "security_owner", "waes_admin", "kds_curator", "developer", "ai_agent"]:
        require(f"  {role}:" in permissions, f"permissions missing human role: {role}")

    require("default_status: candidate" in permissions, "KDS default status must be candidate")
    require("codegraph_may_promote_to_accepted" not in permissions, "accepted promotion belongs in KDS mapping policy")

    for phrase in ["六层授权", "工具级", "仓库级", "Agent 级", "Loop 阶段级", "KDS/OKF 级", "WAES/人员级"]:
        require(phrase in doc, f"authorization doc missing phrase: {phrase}")

    print("codegraph_authorization_model=pass layers=6 agents=6 candidate_only=true ai_final_approval=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
