#!/usr/bin/env python3
"""Validate Agent-Reach P9 web-provider fallback parsing without live network reads."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-web-provider-fallback-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-web-provider-fallback-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_web_provider_fallback=fail reason={message}")


def load_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_bing_parser(runner) -> None:
    html = """
    <html><body>
      <li class="b_algo">
        <h2><a href="https://mee.gov.cn/ywdt/standard.html">磷石膏污染控制标准</a></h2>
        <p>磷石膏综合利用、无害化贮存和污染控制要求。</p>
      </li>
    </body></html>
    """
    rows = runner.parse_bing_rows(html, 5)
    if rows != [("磷石膏污染控制标准", "https://mee.gov.cn/ywdt/standard.html", "磷石膏综合利用、无害化贮存和污染控制要求。")]:
        fail("bing_parser_rows_mismatch")


def validate_duckduckgo_parser(runner) -> None:
    html = """
    <html><body>
      <div class="result results_links_deep web-result">
        <a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fmiit.gov.cn%2Fgreen%2Fsolid-waste.html">工业固废综合利用</a>
        <div class="result__snippet">工业固废、磷石膏和资源综合利用政策。</div>
      </div>
      </div>
    </body></html>
    """
    rows = runner.parse_duckduckgo_rows(html, 5)
    if rows != [("工业固废综合利用", "https://miit.gov.cn/green/solid-waste.html", "工业固废、磷石膏和资源综合利用政策。")]:
        fail("duckduckgo_parser_rows_mismatch")


def validate_block_detection(runner) -> None:
    if runner.provider_blocked("<html>please complete captcha verification</html>") is not True:
        fail("captcha_block_not_detected")
    if runner.provider_blocked("<html><li class='b_algo'>normal result</li></html>") is not False:
        fail("normal_html_marked_blocked")


def validate_candidate_building(runner) -> None:
    query = {
        "query_id": "p9-pg-q01",
        "project": "GFIS",
        "channel": "web",
        "query": "site:mee.gov.cn 磷石膏 利用 无害化 贮存 污染控制",
    }
    rows = [("磷石膏污染控制标准", "https://mee.gov.cn/ywdt/standard.html", "磷石膏综合利用、无害化贮存和污染控制要求。")]
    candidates = runner.build_candidates(query, rows)
    if len(candidates) != 1:
        fail("candidate_building_expected_one")
    candidate = candidates[0]
    if candidate["source_domain"] != "mee.gov.cn":
        fail("candidate_source_domain_mismatch")
    if "candidate_only" not in candidate["non_claims"]:
        fail("candidate_non_claim_missing")
    if candidate["overall_score"] < 0.5:
        fail("candidate_score_below_threshold")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_markdown(report: dict) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-WEB-PROVIDER-FALLBACK-20260626",
            "title: Agent-Reach P9 Web Provider Fallback 离线验证 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-web-provider-fallback-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-web-provider-fallback-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9 Web Provider Fallback 离线验证 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- live_external_search_invoked: `{report['live_external_search_invoked']}`",
            f"- bing_parser: `{report['checks']['bing_parser']}`",
            f"- duckduckgo_parser: `{report['checks']['duckduckgo_parser']}`",
            f"- provider_block_detection: `{report['checks']['provider_block_detection']}`",
            f"- candidate_building: `{report['checks']['candidate_building']}`",
            "",
            "## 边界",
            "",
            "- 本证据只使用离线 HTML fixture。",
            "- 本证据不执行真实搜索，不消耗 P9 live query 额度。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "",
        ]
    )


def main() -> None:
    runner = load_runner()
    validate_bing_parser(runner)
    validate_duckduckgo_parser(runner)
    validate_block_detection(runner)
    validate_candidate_building(runner)
    report = {
        "id": "agent-reach-p9-web-provider-fallback-20260626",
        "date": "2026-06-26",
        "status": "p9_web_provider_fallback_offline_validated",
        "current_admission": "limited_candidate_only",
        "live_external_search_invoked": False,
        "checks": {
            "bing_parser": "pass",
            "duckduckgo_parser": "pass",
            "provider_block_detection": "pass",
            "candidate_building": "pass",
        },
        "non_claims": [
            "offline_fixture_only",
            "not_live_search_invoked",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_web_provider_fallback=pass "
        "bing_parser=pass duckduckgo_parser=pass provider_block_detection=pass "
        "live_external_search_invoked=false"
    )


if __name__ == "__main__":
    main()
