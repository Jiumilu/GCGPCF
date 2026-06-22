#!/usr/bin/env python3
"""Validate GFIS CodeGraph residual notice evidence."""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GFIS = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-gfis-residual-notice-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-gfis-residual-notice-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-RESIDUAL-NOTICE-001.md"
CANDIDATE = GFIS / "scripts/validate_gfis_runtime_sop_e2e.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stderr}",
    )
    return completed.stdout


def parse_count(label: str, output: str) -> int:
    match = re.search(rf"{re.escape(label)}:\s+([0-9,.]+)", output)
    require(match is not None, f"CodeGraph status missing {label}")
    return int(match.group(1).replace(",", ""))


def indexed_path_exists(path: str) -> bool:
    db_path = GFIS / ".codegraph/codegraph.db"
    require(db_path.exists(), "GFIS CodeGraph DB missing")
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("select 1 from files where path = ?", (path,)).fetchone()
    return row is not None


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    require(run(["codegraph", "--version"]).strip() == "1.0.1", "codegraph version must be 1.0.1")

    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-GFIS-RESIDUAL-NOTICE-20260621", "invalid evidence id")
    require(evidence.get("status") == "gfis_residual_notice_explained", "invalid evidence status")
    require(evidence.get("codegraph", {}).get("gfis_sync_executed_this_round") is False, "this round must not execute GFIS sync")
    require(
        evidence.get("codegraph", {}).get("gpcf_evidence_sync_executed_this_round") is True,
        "this round must record GPCF evidence sync",
    )
    require(evidence.get("classification", {}).get("integration_layer_notice") is True, "must classify as integration notice")
    require(evidence.get("classification", {}).get("project_internal_development_required") is False, "must not require project development")

    require(GFIS.exists() and (GFIS / ".git").exists(), "GFIS Git repo missing")
    require((GFIS / ".codegraph").exists(), "GFIS .codegraph missing")
    exclude = GFIS / ".git/info/exclude"
    require(exclude.exists() and ".codegraph/" in exclude.read_text(encoding="utf-8"), "GFIS .codegraph exclude missing")
    require(run(["git", "status", "--short", "--", ".codegraph"], cwd=GFIS).strip() == "", "GFIS .codegraph appears in git status")

    status = run(["codegraph", "status", str(GFIS)])
    gfis = evidence["gfis"]
    require(parse_count("Files", status) == int(gfis["files"]), "GFIS file count drift")
    require(parse_count("Nodes", status) == int(gfis["nodes"]), "GFIS node count drift")
    require(parse_count("Edges", status) == int(gfis["edges"]), "GFIS edge count drift")
    require("Pending Changes:" in status and "Added:" in status, "GFIS pending notice missing")

    candidate = evidence["residual_candidate"]
    require(candidate["path"] == "scripts/validate_gfis_runtime_sop_e2e.py", "unexpected candidate path")
    require(CANDIDATE.exists(), "candidate file missing")
    require(run(["git", "ls-files", "--", candidate["path"]], cwd=GFIS).strip() == candidate["path"], "candidate must be tracked")
    require(run(["git", "status", "--short", "--", candidate["path"]], cwd=GFIS).strip().startswith("M "), "candidate must remain modified")
    require(not indexed_path_exists(candidate["path"]), "candidate must not be in CodeGraph files table")
    require(CANDIDATE.stat().st_size == int(candidate["size_bytes"]), "candidate size drift")
    require(sum(1 for _ in CANDIDATE.open("r", encoding="utf-8")) == int(candidate["line_count"]), "candidate line count drift")

    for phrase in [
        "scripts/validate_gfis_runtime_sop_e2e.py",
        "residual_pending_notice",
        "未进入 GFIS 业务开发",
        "未对 GFIS 执行 `codegraph sync`",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-GFIS-LARGE-FILE-POLICY-001"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for key, value in evidence.get("status_boundaries", {}).items():
        require(value is False, f"status boundary must be false: {key}")

    print(
        "loop_codegraph_gfis_residual_notice=pass "
        "evidence=LOOP-CODEGRAPH-GFIS-RESIDUAL-NOTICE-20260621 "
        "candidate=scripts/validate_gfis_runtime_sop_e2e.py "
        "classification=integration_layer_notice "
        "codegraph_git_status_entries=0 "
        "project_internal_development=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
