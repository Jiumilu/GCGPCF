#!/usr/bin/env python3
"""Validate Agent-Reach P7 runtime dependency precheck evidence."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "tools/kds-sync/check_agent_reach_p7_runtime_dependencies.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-runtime-dependency-precheck-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p7-runtime-dependency-precheck-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-RUNTIME-DEPENDENCY-PRECHECK-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p7_runtime_dependency_precheck=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def load_checker_module():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_dependency_checker", CHECKER)
    if spec is None or spec.loader is None:
        fail("checker_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    checker = load_checker_module()
    current = checker.build_dependency_report()
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    if evidence.get("status") != current.get("status"):
        fail("evidence_status_stale")
    if evidence.get("checked_queries") != current.get("checked_queries"):
        fail("checked_queries_mismatch")
    if evidence.get("missing_binaries") != current.get("missing_binaries"):
        fail("missing_binaries_mismatch")
    evidence_checks = {
        (item["query_id"], item["binary"]): item["available"]
        for item in evidence.get("dependency_checks", [])
    }
    for item in current.get("dependency_checks", []):
        key = (item["query_id"], item["binary"])
        if evidence_checks.get(key) is not item["available"]:
            fail(f"dependency_check_stale:{item['query_id']}:{item['binary']}")
    if evidence.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("live_external_search_not_false")
    status_marker = current["status"]
    for marker in [
        status_marker,
        "不声明真实搜索已调用",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    if current["missing_binaries"] and "missing" not in evidence_md:
        fail("evidence_md_missing:missing")
    if not current["missing_binaries"] and "available" not in evidence_md:
        fail("evidence_md_missing:available")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p7_runtime_dependency_precheck=pass "
        f"status={current['status']} "
        f"missing_binaries={','.join(current['missing_binaries']) or 'none'} "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
