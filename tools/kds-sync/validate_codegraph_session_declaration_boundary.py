#!/usr/bin/env python3
"""Validate CodeGraph session declaration boundary evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-session-declaration-boundary-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-session-declaration-boundary-20260622.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)

    require(evidence["evidence_id"] == "CODEGRAPH-SESSION-DECLARATION-BOUNDARY-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-SESSION-DECLARATION-BOUNDARY-001", "invalid scope")
    require(evidence["status"] == "declaration_boundary_established", "invalid status")

    required_rounds = {
        "GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001",
        "GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002",
    }
    require(set(evidence["latest_rounds"]) == required_rounds, "latest rounds mismatch")

    for key, value in evidence["declaration_boundaries"].items():
        require(value is False, f"declaration boundary must remain false: {key}")

    for phrase in [
        "不是进入各项目业务开发",
        "允许声明",
        "禁止声明",
        "不得声明业务功能已完成",
        "不得声明任何项目已 `accepted` 或 `integrated`",
        "不得声明 CodeGraph 可替代 WAES、Harness 或人工验收裁决",
        "GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "业务功能已完成",
        "项目已 accepted 或 integrated",
        "生产环境已就绪",
        "CodeGraph 可替代 WAES/Harness/人工验收裁决",
    ]:
        require(phrase in evidence["forbidden_claims"], f"forbidden claim missing: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_session_declaration_boundary=pass "
        "allowed_claims=5 "
        "forbidden_claims=6 "
        "status_boundaries=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
