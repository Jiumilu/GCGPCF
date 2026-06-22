#!/usr/bin/env python3
"""Validate Agent-Reach full implementation goal artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-full-implementation-goal-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-full-implementation-goal-20260622.md"
PROMPT_MD = ROOT / "02-governance/GlobalCloud项目群Agent-Reach全量实施方案与执行提示词.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-FULL-IMPLEMENTATION-GOAL-001.md"

FORBIDDEN_CLAIMS = [
    "production_integration_allowed\": true",
    "kds_canonical_write_allowed\": true",
    "gfis_source_of_record_write_allowed\": true",
    "live_external_search_invoked\": true",
    "agent_reach_runtime_invoked\": true",
]

REQUIRED_PHASES = [
    "P0 Source Lock",
    "P1 Isolated Install",
    "P2 Channel Doctor",
    "P3 Fixed Query Benchmark",
    "P4 Candidate Ingestion",
    "P5 Project Group Routing",
    "P6 Authorized Read-Only Live",
    "P7 Human Review",
    "P8 Controlled Production Admission",
]

REQUIRED_PROMPT_PHRASES = [
    "完整实施提示词",
    "limited_candidate_only",
    "agent-reach doctor --json",
    "source_provenance_rate == 1.0",
    "canonical_write_count = 0",
    "production_admission",
    "GPCF-AGENT-REACH-P0-SOURCE-LOCK-001",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_full_implementation_goal=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    data = json.loads(read_text(EVIDENCE_JSON))
    evidence_text = read_text(EVIDENCE_MD)
    prompt_text = read_text(PROMPT_MD)
    loop_text = read_text(LOOP_MD)

    if data.get("status") != "full_implementation_prompt_ready":
        fail("unexpected_status")
    if data.get("current_admission") != "limited_candidate_only":
        fail("current_admission_not_limited")
    for field in [
        "production_integration_allowed",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "live_external_search_invoked",
        "agent_reach_runtime_invoked",
    ]:
        if data.get(field) is not False:
            fail(f"{field}_not_false")
    if data.get("upstream", {}).get("head") != "22d7f03a59401b5740b380c3ad43e3ff7a9dc373":
        fail("upstream_head_mismatch")
    if data.get("upstream", {}).get("version") != "1.5.0":
        fail("upstream_version_mismatch")
    if data.get("upstream", {}).get("license") != "MIT":
        fail("license_mismatch")
    if len(data.get("capability_domains", [])) < 17:
        fail("capability_domain_count_too_low")
    if len(data.get("project_scope", [])) != 14:
        fail("project_scope_count_mismatch")
    if data.get("phases") != REQUIRED_PHASES:
        fail("phase_sequence_mismatch")
    if data.get("next_round") != "GPCF-AGENT-REACH-P0-SOURCE-LOCK-001":
        fail("next_round_mismatch")

    combined_json = EVIDENCE_JSON.read_text(encoding="utf-8")
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined_json:
            fail(f"forbidden_claim:{claim}")
    for phrase in REQUIRED_PROMPT_PHRASES:
        if phrase not in prompt_text:
            fail(f"missing_prompt_phrase:{phrase}")
    for phrase in ["非声明", "不声明 accepted / integrated / production_ready"]:
        if phrase not in evidence_text:
            fail(f"missing_evidence_phrase:{phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "下一轮"]:
        if f"## {phrase}" not in loop_text:
            fail(f"missing_loop_section:{phrase}")

    print(
        "agent_reach_full_implementation_goal=pass "
        f"phase_count={len(data['phases'])} "
        f"capability_domain_count={len(data['capability_domains'])} "
        f"project_scope_count={len(data['project_scope'])} "
        "current_admission=limited_candidate_only "
        "production_integration_allowed=false "
        f"next={data['next_round']}"
    )


if __name__ == "__main__":
    main()
