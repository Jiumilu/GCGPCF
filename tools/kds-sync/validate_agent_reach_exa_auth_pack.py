#!/usr/bin/env python3
"""Validate Agent-Reach Exa authorization package."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "02-governance/loop/LOOP_AGENT_REACH_EXA_AUTH_PACK.md"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-exa-auth-pack-20260620.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-exa-auth-pack-20260620.json"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-AUTH-PACK-001.md"

REQUIRED_FRONTMATTER_KEYS = [
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
]

AUTH_FIELDS = [
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


def frontmatter(path: Path, text: str) -> str:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    return text[:end]


def validate_doc(path: Path, text: str, source_path: str) -> None:
    metadata = frontmatter(path, text)
    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in metadata, f"{path.relative_to(ROOT)} missing front matter key {key}")
    for phrase in [
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    plan = read(PLAN)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    evidence = load_json(EVIDENCE_JSON)

    validate_doc(PLAN, plan, "02-governance/loop/LOOP_AGENT_REACH_EXA_AUTH_PACK.md")
    validate_doc(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/agent-reach-exa-auth-pack-20260620.md",
    )
    validate_doc(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-AUTH-PACK-001.md",
    )

    for phrase in [
        "authorization_required",
        "mcporter_cli_available",
        "npm_visible_version",
        "0.12.0",
        "https://mcp.exa.ai/mcp",
        "npm install --prefix /tmp/agent-reach-mcporter mcporter",
        "mcporter config add exa https://mcp.exa.ai/mcp",
        "rm -rf /tmp/agent-reach-mcporter",
        "npm uninstall -g mcporter",
        "mcporter config remove exa",
        "不安装 `mcporter`",
        "不修改 MCP 配置",
    ]:
        require(phrase in plan, f"plan missing phrase: {phrase}")

    for field in AUTH_FIELDS:
        require(field in plan, f"plan missing authorization field: {field}")
        require(field in evidence_md, f"evidence markdown missing authorization field: {field}")

    require(evidence.get("evidence_id") == "AGENT-REACH-EXA-AUTH-PACK-20260620", "invalid evidence id")
    require(evidence.get("status") == "authorization_required", "status must remain authorization_required")
    require(evidence.get("mcporter_cli_available") is False, "mcporter must be unavailable before authorization")
    require(evidence.get("npm_visible_version") == "0.12.0", "invalid npm visible version")
    require(evidence.get("installation_performed") is False, "installation must be false")
    require(evidence.get("mcp_configuration_changed") is False, "MCP config must remain unchanged")
    require(evidence.get("exa_mcp_registered") is False, "Exa MCP registration must be false")
    require(evidence.get("exa_search_verified") is False, "Exa search verification must be false")
    require(evidence.get("cookies_configured") is False, "cookies must remain false")
    require(evidence.get("production_write_count") == 0, "production write count must be zero")
    require(evidence.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")
    require(evidence.get("credential_leakage_count") == 0, "credential leakage count must be zero")
    require(evidence.get("status_upgrade_allowed") is False, "status upgrade must be false")

    evidence_fields = evidence.get("required_authorization_fields", [])
    require(isinstance(evidence_fields, list), "required_authorization_fields must be a list")
    for field in AUTH_FIELDS:
        require(field in evidence_fields, f"evidence JSON missing authorization field: {field}")

    non_claims = "\n".join(evidence.get("non_claims", []))
    for phrase in [
        "does not prove mcporter installed",
        "does not prove Exa MCP configured",
        "does not prove Agent-Reach exa_search available",
        "does not write KDS canonical Markdown",
        "does not create GFIS source-of-record",
    ]:
        require(phrase in non_claims, f"non-claims missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "authorization_required",
        "本轮不安装 `mcporter`",
        "本轮不修改 MCP 配置",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    require(shutil.which("mcporter") is None, "validator expects no mcporter install before authorization")

    print(
        "agent_reach_exa_auth_pack=pass "
        "status=authorization_required mcporter_cli_available=false "
        "npm_visible_version=0.12.0 installation_performed=false "
        "mcp_configuration_changed=false exa_search_verified=false "
        "status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
