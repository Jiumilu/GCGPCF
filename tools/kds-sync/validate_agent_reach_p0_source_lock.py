#!/usr/bin/env python3
"""Validate Agent-Reach P0 source lock artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p0-source-lock-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p0-source-lock-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P0-SOURCE-LOCK-001.md"
THIRD_PARTY = ROOT / "third_party/agent-reach"
REQUIRED_REVIEW_FILES = [
    "README.md",
    "SOURCE.md",
    "VERSION.lock",
    "OSS_REVIEW.md",
    "SECURITY_REVIEW.md",
    "MODIFICATIONS.md",
]
REQUIRED_CHANNELS = {
    "web",
    "exa_search",
    "github",
    "youtube",
    "rss",
    "bilibili",
    "v2ex",
    "xueqiu",
    "twitter",
    "reddit",
    "xiaohongshu",
    "linkedin",
    "xiaoyuzhou",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p0_source_lock=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    data = json.loads(read_text(EVIDENCE_JSON))
    evidence = read_text(EVIDENCE_MD)
    loop = read_text(LOOP_MD)
    version_lock = read_text(THIRD_PARTY / "VERSION.lock")

    for name in REQUIRED_REVIEW_FILES:
        path = THIRD_PARTY / name
        if not path.exists():
            fail(f"missing_review_file:{name}")
    for name in ["README.md", "SOURCE.md", "OSS_REVIEW.md", "SECURITY_REVIEW.md", "MODIFICATIONS.md"]:
        text = read_text(THIRD_PARTY / name)
        for marker in ["doc_id:", "status: controlled", "kds_space: 开发", f"source_path: third_party/agent-reach/{name}"]:
            if marker not in text:
                fail(f"missing_frontmatter:{name}:{marker}")

    upstream = data.get("upstream", {})
    if data.get("status") != "source_lock_ready":
        fail("unexpected_status")
    if data.get("current_admission") != "limited_candidate_only":
        fail("current_admission_not_limited")
    if data.get("phase") != "P0 Source Lock":
        fail("phase_mismatch")
    if upstream.get("head") != "22d7f03a59401b5740b380c3ad43e3ff7a9dc373":
        fail("head_mismatch")
    if upstream.get("version") != "1.5.0":
        fail("version_mismatch")
    if upstream.get("license") != "MIT":
        fail("license_mismatch")
    if upstream.get("source_file_count") != 89:
        fail("source_file_count_mismatch")
    if set(data.get("capability_domains", [])) != REQUIRED_CHANNELS:
        fail("capability_domains_mismatch")
    controls = data.get("security_controls", {})
    for field in [
        "source_archive_copied",
        "upstream_source_modified",
        "package_installed",
        "live_external_search_invoked",
        "agent_reach_runtime_invoked",
        "credential_written",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "production_config_write_allowed",
        "global_mcp_config_write_allowed",
        "production_integration_allowed",
    ]:
        if controls.get(field) is not False:
            fail(f"{field}_not_false")
    for phrase in [
        "verified_head=22d7f03a59401b5740b380c3ad43e3ff7a9dc373",
        "package_version=1.5.0",
        "license=MIT",
        "admission=limited_candidate_only",
        "production_integration_allowed=false",
    ]:
        if phrase not in version_lock:
            fail(f"version_lock_missing:{phrase}")
    for phrase in [
        "不声明 Agent-Reach 已安装",
        "不声明 live external search 已调用",
        "不声明 accepted / integrated / production_ready",
    ]:
        if phrase not in evidence:
            fail(f"evidence_missing:{phrase}")
    for section in ["输入", "动作", "输出", "检查", "反馈", "下一轮"]:
        if f"## {section}" not in loop:
            fail(f"loop_missing_section:{section}")
    if data.get("next_round") != "GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001":
        fail("next_round_mismatch")

    print(
        "agent_reach_p0_source_lock=pass "
        f"review_file_count={len(REQUIRED_REVIEW_FILES)} "
        f"capability_domain_count={len(REQUIRED_CHANNELS)} "
        f"source_file_count={upstream['source_file_count']} "
        "current_admission=limited_candidate_only "
        "package_installed=false "
        "production_integration_allowed=false "
        f"next={data['next_round']}"
    )


if __name__ == "__main__":
    main()
