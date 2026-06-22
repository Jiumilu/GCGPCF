#!/usr/bin/env python3
"""Validate Agent-Reach P7 web backend runtime repair artifacts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-web-backend-runtime-repair-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p7-web-backend-runtime-repair-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-WEB-BACKEND-RUNTIME-REPAIR-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p7_web_backend_runtime_repair=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def load_runner_module():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner_module()
    plan = runner.load_json(runner.PLAN_PATH)
    execution_plan = runner.build_execution_plan(plan)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    web_items = [item for item in execution_plan if item["channel"] == "web"]
    if len(web_items) != 3:
        fail("web_query_count_mismatch")
    for item in web_items:
        if item.get("backend") != "duckduckgo_html_via_python_stdlib":
            fail(f"web_backend_mismatch:{item['query_id']}")
        if item.get("planned_command", [None])[0] != "python3":
            fail(f"web_binary_mismatch:{item['query_id']}")
    if evidence.get("status") != "web_backend_runtime_dependency_repaired":
        fail("evidence_status_mismatch")
    if evidence.get("repair", {}).get("new_backend") != "duckduckgo_html_via_python_stdlib":
        fail("evidence_new_backend_mismatch")
    if evidence.get("post_repair_dependency_status", {}).get("missing_binaries") != []:
        fail("evidence_missing_binaries_not_empty")
    if evidence.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("live_external_search_not_false")
    for marker in [
        "web_backend_runtime_dependency_repaired",
        "duckduckgo_html_via_python_stdlib",
        "不声明真实搜索已调用",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p7_web_backend_runtime_repair=pass "
        "status=web_backend_runtime_dependency_repaired "
        "backend=duckduckgo_html_via_python_stdlib"
    )


if __name__ == "__main__":
    main()
