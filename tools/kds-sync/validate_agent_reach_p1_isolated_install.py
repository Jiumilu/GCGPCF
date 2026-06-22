#!/usr/bin/env python3
"""Validate Agent-Reach P1 isolated install artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p1-isolated-install-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p1-isolated-install-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001.md"
INSTALL_REVIEW = ROOT / "third_party/agent-reach/ISOLATED_INSTALL_REVIEW.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p1_isolated_install=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    data = json.loads(read_text(EVIDENCE_JSON))
    evidence = read_text(EVIDENCE_MD)
    loop = read_text(LOOP_MD)
    review = read_text(INSTALL_REVIEW)

    if data.get("status") != "isolated_install_ready":
        fail("unexpected_status")
    if data.get("current_admission") != "limited_candidate_only":
        fail("current_admission_not_limited")
    if data.get("phase") != "P1 Isolated Install":
        fail("phase_mismatch")
    upstream = data.get("upstream", {})
    if upstream.get("head") != "22d7f03a59401b5740b380c3ad43e3ff7a9dc373":
        fail("head_mismatch")
    if upstream.get("version") != "1.5.0":
        fail("version_mismatch")
    env = data.get("environment", {})
    if env.get("default_python_result") != "blocked_by_python_requirement":
        fail("default_python_not_recorded_as_blocked")
    if env.get("isolated_python") != "3.12.13":
        fail("isolated_python_mismatch")
    install = data.get("installation", {})
    if install.get("isolated_venv_install") is not True:
        fail("isolated_install_not_true")
    for field in ["project_install", "global_install"]:
        if install.get(field) is not False:
            fail(f"{field}_not_false")
    checks = data.get("checks", {})
    for field in ["python_import_agent_reach", "python_import_core_agent_reach", "cli_help"]:
        if checks.get(field) != "pass":
            fail(f"{field}_not_pass")
    if checks.get("cli_version") != "Agent Reach v1.5.0":
        fail("cli_version_mismatch")
    if checks.get("doctor_json") != "pass_with_probe":
        fail("doctor_not_recorded_as_probe")
    if checks.get("temporary_config_file_absent") is not True:
        fail("temporary_config_file_not_absent")
    summary = data.get("doctor_summary", {})
    if set(summary.get("ok", [])) != {"web", "rss", "bilibili"}:
        fail("doctor_ok_mismatch")
    if set(summary.get("warn", [])) != {"github", "twitter", "youtube", "v2ex", "xueqiu"}:
        fail("doctor_warn_mismatch")
    if set(summary.get("off", [])) != {"reddit", "xiaohongshu", "linkedin", "xiaoyuzhou", "exa_search"}:
        fail("doctor_off_mismatch")
    controls = data.get("security_controls", {})
    expected_true = ["package_installed_in_isolated_venv", "doctor_health_probe_invoked", "temporary_config_directory_created"]
    for field in expected_true:
        if controls.get(field) is not True:
            fail(f"{field}_not_true")
    expected_false = [
        "package_installed_in_project",
        "package_installed_globally",
        "live_external_search_invoked",
        "agent_reach_search_command_invoked",
        "credential_written",
        "browser_cookie_extraction_invoked",
        "temporary_config_file_written",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "production_config_write_allowed",
        "global_mcp_config_write_allowed",
        "production_integration_allowed",
    ]
    for field in expected_false:
        if controls.get(field) is not False:
            fail(f"{field}_not_false")
    for marker in [
        "doc_id:",
        "status: controlled",
        "kds_space: 开发",
        "source_path: third_party/agent-reach/ISOLATED_INSTALL_REVIEW.md",
    ]:
        if marker not in review:
            fail(f"review_missing:{marker}")
    for phrase in [
        "不声明 live external search 已调用",
        "不声明任一搜索通道已通过业务质量验收",
        "不声明 accepted / integrated / production_ready",
    ]:
        if phrase not in evidence:
            fail(f"evidence_missing:{phrase}")
    for section in ["输入", "动作", "输出", "检查", "反馈", "下一轮"]:
        if f"## {section}" not in loop:
            fail(f"loop_missing_section:{section}")
    if data.get("next_round") != "GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001":
        fail("next_round_mismatch")

    print(
        "agent_reach_p1_isolated_install=pass "
        "status=isolated_install_ready "
        "current_admission=limited_candidate_only "
        "isolated_python=3.12.13 "
        "package_version=1.5.0 "
        "doctor_ok=3 doctor_warn=5 doctor_off=5 "
        "live_external_search_invoked=false "
        "credential_written=false "
        f"next={data['next_round']}"
    )


if __name__ == "__main__":
    main()
