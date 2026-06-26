#!/usr/bin/env python3
"""Validate CodeGraph KDS mirror scope review authorization recheck evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
KDS = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-kds-mirror-scope-review-authorization-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-kds-mirror-scope-review-authorization-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def extract_json(stdout: str) -> dict[str, Any]:
    start = stdout.find("{")
    end = stdout.rfind("}")
    require(start >= 0 and end >= start, f"no JSON object in command output: {stdout}")
    return json.loads(stdout[start : end + 1])


def git_dirty_total(repo: Path) -> int:
    result = run(["git", "status", "--short"], cwd=repo)
    require(result.returncode == 0, f"git status failed: {result.stderr}")
    return len([line for line in result.stdout.splitlines() if line.strip()])


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017", "invalid scope")
    require(evidence["status"] == "authorization_required_current_state_dirty", "invalid status")
    require(evidence["previous_round"] == "GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016", "invalid previous round")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018", "invalid next round")

    current = evidence["current_kds"]
    status_result = run(["codegraph", "status", "--json", "."], cwd=KDS)
    require(status_result.returncode == 0, f"KDS codegraph status failed: {status_result.stderr}")
    status = json.loads(status_result.stdout)
    require(status["initialized"] is True, "KDS CodeGraph not initialized")
    require(status["pendingChanges"] == current["codegraph"]["pendingChanges"], "KDS CodeGraph pending must match evidence")
    require(status["worktreeMismatch"] is None, "KDS worktree mismatch must be null")
    require(status["index"]["reindexRecommended"] is False, "KDS reindex must not be recommended")

    require(git_dirty_total(KDS) == current["git_dirty"]["total"], "KDS Git dirty must match evidence")
    git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=KDS)
    require(git_status.returncode == 0, f"KDS .codegraph git status failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", "KDS .codegraph must remain git-isolated")

    decision = evidence["authorization_decision"]
    require(decision["kds_mirror_scope_review_required_now"] is True, "KDS scope review must be required now")
    require(decision["kds_codegraph_sync_required_now"] is False, "KDS sync must not be required now")
    require(decision["kds_clean_reindex_required_now"] is False, "KDS clean reindex must not be required now")

    governance = evidence["governance"]
    require(governance["mode"] == "kds_scope_review_authorization_required_by_dirty_state", "invalid governance mode")
    for key, value in governance.items():
        if key == "mode":
            continue
        require(value is False, f"governance action must be false: {key}")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        require(section in evidence["five_direction"], f"missing five_direction section: {section}")
        require(f"## {section}" in loop_round, f"loop round missing section: {section}")

    localization = run(["python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json"])
    require(localization.returncode == 0, f"localization gate failed: {localization.stdout}{localization.stderr}")
    localization_json = extract_json(localization.stdout)
    require(localization_json["localization_gate"] == "pass", "localization gate must pass")
    require(localization_json["findings"] == 0, "localization findings must be zero")

    loop_gate = run(["python3", "tools/kds-sync/loop_document_gate.py", "--check-only"])
    require(loop_gate.returncode == 0, f"Loop document gate failed: {loop_gate.stdout}{loop_gate.stderr}")
    loop_json = extract_json(loop_gate.stdout)
    require(loop_json["gate"] == "pass", "Loop document gate must pass")
    require(loop_json["localization_debt"] is False, "localization_debt must be false")

    pollution = run(["python3", "tools/kds-sync/check_document_pollution.py"])
    require(pollution.returncode == 0 and "document_pollution=pass" in pollution.stdout, "document pollution must pass")

    token = run(["python3", "tools/kds-sync/validate_kds_token.py"])
    require(token.returncode == 0 and "kds_token=pass" in token.stdout, "KDS token must pass")

    for phrase in [
        "authorization_required_current_state_dirty",
        "KDS Git dirty：`1`",
        "KDS CodeGraph pending：`added=0, modified=0, removed=0`",
        "保留 KDS scope review 授权边界",
        "GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    print(
        "codegraph_kds_mirror_scope_review_authorization=required_current_state_dirty "
        f"kds_git_dirty={git_dirty_total(KDS)} "
        "kds_pending=0 "
        "kds_scope_review_required=true "
        "kds_sync_performed=false "
        "real_kds_api_write=false "
        "mirror_overwrite=false "
        "clean_reindex=false "
        "business_development=false commit=false push=false deploy=false "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
