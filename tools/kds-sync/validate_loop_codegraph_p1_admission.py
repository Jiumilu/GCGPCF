#!/usr/bin/env python3
"""Validate CodeGraph P1 pilot admission package."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "02-governance/loop/LOOP_CODEGRAPH_P1_PILOT_ADMISSION.md"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-p1-pilot-admission-20260620.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-p1-pilot-admission-20260620.json"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-P1-ADMISSION-001.md"

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
    "authorized_repos",
    "allow_global_npm_install",
    "allow_agent_mcp_install",
    "allow_codegraph_init",
    "allow_network_download",
    "rollback_required",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def frontmatter(path: Path, text: str) -> str:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    return text[:end]


def validate_controlled(path: Path, text: str, source_path: str) -> None:
    metadata = frontmatter(path, text)
    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in metadata, f"{path.relative_to(ROOT)} missing front matter key {key}")
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    plan = read(PLAN)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    evidence = load_json(EVIDENCE_JSON)

    validate_controlled(PLAN, plan, "02-governance/loop/LOOP_CODEGRAPH_P1_PILOT_ADMISSION.md")
    validate_controlled(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/loop-codegraph-p1-pilot-admission-20260620.md",
    )
    validate_controlled(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-CODEGRAPH-P1-ADMISSION-001.md",
    )

    for phrase in [
        "authorization_required",
        "codegraph_cli_available",
        "@colbymchenry/codegraph@1.0.1",
        "npm i -g @colbymchenry/codegraph",
        "codegraph install",
        "codegraph init",
        "npm uninstall -g @colbymchenry/codegraph",
        "GFIS",
        "GPCF",
        "不证明 CodeGraph 已安装",
        "不授权生产写入",
    ]:
        require(phrase in plan, f"admission plan missing phrase: {phrase}")

    for field in AUTH_FIELDS:
        require(field in plan, f"admission plan missing authorization field: {field}")
        require(field in evidence_md, f"evidence markdown missing authorization field: {field}")

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-P1-ADMISSION-20260620", "invalid evidence id")
    require(evidence.get("status") == "authorization_required", "P1 admission must remain authorization_required")
    state = evidence.get("current_state", {})
    require(state.get("codegraph_cli_available") is False, "evidence must record CLI unavailable before authorization")
    require(state.get("npm_visible_version") == "1.0.1", "evidence must record npm visible version")
    require(state.get("mcp_configuration_changed") is False, "MCP config must remain unchanged")
    require(state.get("codegraph_index_created") is False, "CodeGraph index must not be created")
    require(state.get("production_write") is False, "production write must be false")
    require(state.get("external_api_write") is False, "external API write must be false")
    require(state.get("status_upgrade_allowed") is False, "status upgrade must not be allowed")

    evidence_fields = evidence.get("required_authorization_fields", [])
    require(isinstance(evidence_fields, list), "required_authorization_fields must be a list")
    for field in AUTH_FIELDS:
        require(field in evidence_fields, f"evidence JSON missing authorization field: {field}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "authorization_required",
        "本轮不安装 CodeGraph",
        "本轮不修改 MCP 配置",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    non_claims = "\n".join(evidence.get("non_claims", []))
    for phrase in [
        "does not prove CodeGraph installed",
        "does not prove GFIS runtime SOP E2E passed",
        "does not create source-of-record",
        "does not authorize production write",
    ]:
        require(phrase in non_claims, f"evidence non-claims missing phrase: {phrase}")

    codegraph_available = shutil.which("codegraph") is not None
    require(codegraph_available is False, "P1 admission validator expects no CodeGraph install before authorization")

    print(
        "loop_codegraph_p1_admission=pass "
        "evidence=LOOP-CODEGRAPH-P1-ADMISSION-20260620 "
        "status=authorization_required "
        "codegraph_cli_available=false npm_visible_version=1.0.1 "
        "installation_performed=false mcp_configuration_changed=false "
        "codegraph_index_created=false status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
