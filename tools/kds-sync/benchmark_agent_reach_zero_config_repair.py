#!/usr/bin/env python3
"""Run Agent-Reach zero-config fallback benchmark.

This benchmark intentionally avoids cookies, login-state platforms, MCP
configuration changes, production writes, and KDS canonical writes.
"""

from __future__ import annotations

import gzip
import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime, timezone


def fetch(url: str) -> tuple[str, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "identity",
            "Accept": "text/plain,text/html,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read(4096)
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        text = raw.decode("utf-8", "replace")
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text, resp.geturl()


def run_case(name: str, channel: str, fn) -> dict[str, object]:
    start = time.perf_counter()
    case: dict[str, object] = {
        "name": name,
        "channel": channel,
        "success": False,
        "latency_seconds": None,
        "error": None,
        "source_provenance": None,
        "rag_admission": "repair_required",
    }
    try:
        summary, provenance = fn()
        case.update(
            success=True,
            result_summary=summary[:300],
            source_provenance=provenance,
            rag_admission="limited",
        )
    except Exception as exc:  # noqa: BLE001 - benchmark evidence needs failure detail
        case["error"] = f"{type(exc).__name__}: {exc}"
    case["latency_seconds"] = round(time.perf_counter() - start, 3)
    return case


def main() -> int:
    cases = [
        run_case(
            "web_jina_example_domain",
            "web",
            lambda: fetch("https://r.jina.ai/http://example.com"),
        ),
        run_case(
            "web_jina_raw_agent_reach_readme",
            "web",
            lambda: fetch("https://r.jina.ai/https://raw.githubusercontent.com/Panniantong/Agent-Reach/main/README.md"),
        ),
        run_case(
            "github_api_agent_reach_readme",
            "github",
            lambda: (
                subprocess.run(
                    ["gh", "api", "repos/Panniantong/Agent-Reach/readme", "--jq", ".content"],
                    capture_output=True,
                    text=True,
                    timeout=20,
                    check=True,
                ).stdout[:300],
                "gh api repos/Panniantong/Agent-Reach/readme",
            ),
        ),
        run_case(
            "rss_python_peps_feed",
            "rss",
            lambda: fetch("https://peps.python.org/peps.rss"),
        ),
    ]

    success_count = sum(1 for case in cases if case["success"])
    latencies = sorted(float(case["latency_seconds"]) for case in cases)
    report = {
        "evidence_id": "AGENT-REACH-ZERO-CONFIG-REPAIR-20260620",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if success_count == len(cases) else "partial",
        "mode": "L2_zero_config_repair",
        "benchmark_case_count": len(cases),
        "benchmark_success_count": success_count,
        "zero_config_success_rate": round(success_count / len(cases), 4),
        "latency_p50_seconds": latencies[len(latencies) // 2],
        "latency_p95_seconds": latencies[-1],
        "cookies_configured": False,
        "mcp_configuration_changed": False,
        "production_write_count": 0,
        "kds_canonical_write_count": 0,
        "external_platform_write_count": 0,
        "credential_leakage_count": 0,
        "cases": cases,
        "non_claims": [
            "does not prove Agent-Reach production integration",
            "does not configure cookies or login-state platforms",
            "does not configure mcporter or Exa MCP",
            "does not write KDS canonical Markdown",
            "does not create GFIS source-of-record",
            "does not upgrade GPCF accepted/integrated/production_ready status",
        ],
        "next_gate": "mcporter_exa_requires_explicit_authorization",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if success_count == len(cases) else 2


if __name__ == "__main__":
    raise SystemExit(main())
