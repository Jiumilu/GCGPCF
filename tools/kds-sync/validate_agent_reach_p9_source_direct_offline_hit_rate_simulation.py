#!/usr/bin/env python3
"""Validate P9S source-direct hit-rate logic with an offline fetch simulation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_p9_source_direct_hit_rate.py"
PRECHECK = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-offline-hit-rate-simulation-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-offline-hit-rate-simulation-20260626.md"

TOPIC_FIXTURE_TEXT = {
    "green_supply_chain": "绿色供应链 供应商 ESG 碳足迹 scope 3 carbon traceability",
    "phosphogypsum": "磷石膏 综合利用 污染控制 无害化 贮存 phosphogypsum",
    "industrial_solid_waste": "工业固废 工业固体废物 大宗固废 资源综合利用 solid waste",
    "zero_waste_city": "无废城市 指标体系 试点 工业固废综合利用率 zero-waste",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_offline_hit_rate_simulation=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p9s_runner_offline", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_html_for(target: dict[str, Any], url: str) -> tuple[int, str, str, str, str, str]:
    topic_text = " ".join(TOPIC_FIXTURE_TEXT[topic] for topic in target["topics"])
    link = f"https://www.{target['domain']}/agent-reach-fixture/{target['target_id']}.html"
    if "agent-reach-fixture" in url:
        raw = f"<html><title>{target['target_id']} detail</title><body>{topic_text}</body></html>"
    else:
        raw = f"<html><title>{target['target_id']} entry</title><body>{topic_text}<a href=\"{link}\">detail</a></body></html>"
    title, body = raw.split("<body>", 1)
    return 200, target["target_id"], body.replace("</body></html>", ""), raw, url, "text/html"


def build_report() -> dict[str, Any]:
    precheck = read_json(PRECHECK)
    if precheck.get("status") != "p9_source_direct_hit_rate_precheck_ready":
        fail("precheck_status_mismatch")
    runner = load_runner()
    url_to_target: dict[str, dict[str, Any]] = {}
    for target in precheck["source_direct_targets"]:
        for entrypoint in target["entrypoints"]:
            url_to_target[entrypoint["url"]] = target
            url_to_target[f"https://www.{target['domain']}/agent-reach-fixture/{target['target_id']}.html"] = target

    def fake_fetch_url(url: str):
        target = url_to_target.get(url)
        if target is None:
            fail(f"unexpected_offline_url:{url}")
        return fake_html_for(target, url)

    runner.fetch_url = fake_fetch_url
    runner.fetch_url_with_retry = lambda url: (*fake_fetch_url(url), 0)
    candidates, errors = runner.execute_live(precheck)
    hit_rate = runner.hit_rate_report(precheck, candidates, errors)
    if errors:
        fail(f"offline_errors_present:{len(errors)}")
    if hit_rate.get("threshold_pass") is not True:
        fail("offline_hit_rate_threshold_not_passed")
    if hit_rate.get("topic_coverage") != 1.0:
        fail("offline_topic_coverage_not_one")
    for topic_id, topic_report in hit_rate.get("topic_reports", {}).items():
        if topic_report.get("p0_domain_hit_count", 0) < 1:
            fail(f"offline_p0_hit_missing:{topic_id}")
        if topic_report.get("keyword_hit_candidate_count", 0) < 1:
            fail(f"offline_keyword_hit_missing:{topic_id}")
    return {
        "id": "agent-reach-p9-source-direct-offline-hit-rate-simulation-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_offline_hit_rate_simulation_pass",
        "current_admission": "limited_candidate_only",
        "mode": "offline_fixture_no_external_network",
        "runner": "tools/kds-sync/run_agent_reach_p9_source_direct_hit_rate.py",
        "candidate_count": len(candidates),
        "fetch_error_count": len(errors),
        "critical_fetch_error_count": hit_rate["critical_fetch_error_count"],
        "noncritical_fetch_error_count": hit_rate["noncritical_fetch_error_count"],
        "topic_coverage": hit_rate["topic_coverage"],
        "threshold_pass": hit_rate["threshold_pass"],
        "topic_reports": hit_rate["topic_reports"],
        "live_external_fetch_invoked": False,
        "completion_claim_allowed": False,
        "non_claims": [
            "offline_simulation_only",
            "not_live_fetch_invoked",
            "not_live_run_completed",
            "not_source_of_record",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-OFFLINE-HIT-RATE-SIMULATION-20260626",
            "title: Agent-Reach P9S Source Direct Offline Hit-Rate Simulation 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-offline-hit-rate-simulation-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-offline-hit-rate-simulation-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Offline Hit-Rate Simulation 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- mode: `{report['mode']}`",
            f"- candidate_count: `{report['candidate_count']}`",
            f"- topic_coverage: `{report['topic_coverage']}`",
            f"- threshold_pass: `{report['threshold_pass']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence is offline simulation only.",
            "- This evidence does not invoke live target-site fetch.",
            "- This evidence does not prove real site hit-rate completion.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_offline_hit_rate_simulation=pass "
        f"candidate_count={report['candidate_count']} topic_coverage={report['topic_coverage']} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
