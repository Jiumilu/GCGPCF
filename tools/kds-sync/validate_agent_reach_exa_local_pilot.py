#!/usr/bin/env python3
"""Validate Agent-Reach Exa local pilot evidence."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION = ROOT / "docs/harness/evidence/agent-reach-exa-local-pilot-authorization.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-exa-local-pilot-20260620.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-exa-local-pilot-20260620.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001.md"


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


def main() -> int:
    authorization = load_json(AUTHORIZATION)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/agent-reach-exa-local-pilot-20260620.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001.md",
    )

    require(authorization.get("authorized_mode") == "agent-reach-exa-local-pilot", "invalid authorization")
    require(authorization.get("allow_global_npm_install") is False, "global npm install must be false")
    require(authorization.get("allow_project_dependency_change") is False, "project dependency change must be false")
    require(authorization.get("allow_cookie_or_login_state") is False, "cookies/login state must be false")
    require(authorization.get("allow_production_write") is False, "production write must be false")
    require(authorization.get("allow_kds_canonical_write") is False, "KDS canonical write must be false")
    require(authorization.get("rollback_required") is True, "rollback must be required")

    require(evidence.get("evidence_id") == "AGENT-REACH-EXA-LOCAL-PILOT-20260620", "invalid evidence id")
    require(evidence.get("status") == "pass", "pilot must pass")
    require(evidence.get("authorization_file_present") is True, "authorization file must be present")
    require(evidence.get("installation_performed") is True, "temporary installation must be recorded")
    require(evidence.get("global_npm_install_performed") is False, "global npm install must be false")
    require(evidence.get("project_dependency_changed") is False, "project dependency change must be false")
    require(evidence.get("mcp_configuration_changed") is True, "temporary MCP config must be changed")
    require(evidence.get("mcp_configuration_scope") == "temporary_home_only", "MCP config scope must be temporary")
    require(evidence.get("exa_mcp_registered") is True, "Exa MCP must be registered in temp config")
    require(evidence.get("agent_reach_doctor_exa_status") == "ok", "Agent-Reach exa doctor must be ok")
    require(evidence.get("agent_reach_doctor_exa_backend") == "Exa via mcporter", "invalid exa backend")
    require(evidence.get("exa_schema_status") == "ok", "Exa schema must be ok")
    require("web_search_exa" in evidence.get("exa_tools", []), "web_search_exa missing")
    require("web_fetch_exa" in evidence.get("exa_tools", []), "web_fetch_exa missing")
    require(evidence.get("exa_search_test_success_rate") == 1.0, "Exa search test must pass")
    require(evidence.get("source_provenance_rate") == 1.0, "source provenance must be complete")
    require(evidence.get("cookies_configured") is False, "cookies must remain false")
    require(evidence.get("production_write_count") == 0, "production write count must be zero")
    require(evidence.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")
    require(evidence.get("external_platform_write_count") == 0, "external platform write count must be zero")
    require(evidence.get("credential_leakage_count") == 0, "credential leakage count must be zero")
    require(evidence.get("rollback_verified") is True, "rollback must be verified")
    require(evidence.get("mcporter_still_available_after_rollback") is False, "mcporter must not remain available")
    require(evidence.get("temporary_npm_prefix_exists_after_rollback") is False, "temporary npm prefix must be removed")
    require(evidence.get("temporary_home_exists_after_rollback") is False, "temporary home must be removed")
    require(evidence.get("status_upgrade_allowed") is False, "status upgrade must be false")

    for phrase in [
        "结论为 `pass`，但只证明 Exa local pilot 在临时隔离范围内可用",
        "未执行全局 npm 安装",
        "未写 KDS canonical",
        "回滚结果",
        "不升级",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "rollback_verified | true",
        "stop_type | authorization_boundary",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    require(shutil.which("mcporter") is None, "mcporter must not remain available after rollback")

    print(
        "agent_reach_exa_local_pilot=pass "
        "exa_search_test_success_rate=1.0 "
        "global_npm_install_performed=false project_dependency_changed=false "
        "mcp_configuration_scope=temporary_home_only rollback_verified=true "
        "status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
