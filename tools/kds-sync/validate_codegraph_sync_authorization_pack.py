#!/usr/bin/env python3
"""Validate CodeGraph sync authorization pack evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-sync-authorization-pack-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-sync-authorization-pack-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009.md"
THRESHOLDS = ROOT / "docs/harness/evidence/codegraph-drift-alert-thresholds-20260621.json"
TARGET = "tools/kds-sync/validate_codegraph_drift_alert_thresholds.py"

REPOS = {
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
    "GlobalCloud GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
    "GlobalCoud GPCF": ROOT,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def pending_total(pending: dict) -> int:
    return sum(int(pending.get(key, 0)) for key in ("added", "modified", "removed"))


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    thresholds = json.loads(read(THRESHOLDS))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-SYNC-AUTHORIZATION-PACK-20260621", "invalid evidence id")
    require(evidence["status"] == "sync_authorization_pack_ready", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009", "invalid scope")
    require(thresholds["status"] == "drift_alert_thresholds_ready", "threshold source mismatch")
    require(evidence["authorization_request"]["not_authorized_in_this_round"] is True, "this round must not be authorized")
    require(evidence["authorization_request"]["approval_phrase"] == "授权执行 Brain/Studio CodeGraph sync-only closure", "approval phrase mismatch")

    targets = {item["repo"]: item for item in evidence["authorization_request"]["target_repos"]}
    require(set(targets) == {"GlobalCloud Brain", "GlobalCloud Studio"}, "authorization targets mismatch")

    for repo_name in ["GlobalCloud Brain", "GlobalCloud Studio"]:
        target = targets[repo_name]
        require(target["threshold_result"] == "action_required", f"{repo_name} must be action_required")
        require("codegraph sync" in target["allowed_command_after_authorization"], f"{repo_name} allowed command missing")
        for forbidden in ["business code edits", "git add", "git commit", "git push", "deploy"]:
            require(forbidden in target["forbidden_actions"], f"{repo_name} missing forbidden action: {forbidden}")

        path = REPOS[repo_name]
        status = run(["codegraph", "status", "--json", "."], cwd=path)
        require(status.returncode == 0, f"codegraph status failed for {repo_name}: {status.stderr}")
        live = json.loads(status.stdout)
        require(live.get("initialized") is True, f"{repo_name} codegraph must be initialized")
        require(pending_total(live.get("pendingChanges") or {}) >= 6, f"{repo_name} must still meet action threshold")
        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path)
        require(git_status.returncode == 0, f"git status failed for {repo_name}")
        require(git_status.stdout.strip() == "", f"{repo_name} .codegraph must remain git-isolated")

    gfis_status = run(["codegraph", "status", "--json", "."], cwd=REPOS["GlobalCloud GFIS"])
    require(gfis_status.returncode == 0, "GFIS codegraph status failed")
    gfis = json.loads(gfis_status.stdout)
    require((gfis.get("pendingChanges") or {}).get("added", 0) >= 1, "GFIS policy exception must remain readable")

    query = run(["codegraph", "query", "codegraph_drift_alert_thresholds", "--json"])
    require(query.returncode == 0, f"codegraph query failed: {query.stderr}")
    results = json.loads(query.stdout)
    require(len(results) >= 4, "query should return at least 4 results")
    require(results[0]["node"]["filePath"] == TARGET, "top query result must be drift threshold validator")

    node = run(["codegraph", "node", TARGET])
    require(node.returncode == 0, f"codegraph node failed: {node.stderr}")
    require("160 lines" in node.stdout, "line count must be reported")
    require("12 symbols" in node.stdout, "symbol count must be reported")
    require("no other indexed file depends on it" in node.stdout, "target should have no indexed dependents")

    affected = run(["codegraph", "affected", TARGET, "--json"])
    require(affected.returncode == 0, f"codegraph affected failed: {affected.stderr}")
    affected_json = json.loads(affected.stdout)
    require(affected_json["affectedTests"] == [], "affected tests must be empty")
    require(affected_json["totalDependentsTraversed"] == 0, "dependents traversed must be zero")

    rg = run([
        "rg",
        "-n",
        "validate_codegraph_drift_alert_thresholds|CODEGRAPH-DRIFT-ALERT-THRESHOLDS-20260621|GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008|GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009",
        "docs",
        "tools",
        "governance",
        "harness",
        "loop",
        "09-status",
    ])
    require(rg.returncode == 0, "rg authorization pack should find references")
    require(len(rg.stdout.splitlines()) >= evidence["impact_gate_sample"]["text_scan"]["matched_lines"], "rg line count regressed")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundary must remain false")

    for phrase in ["sync_authorization_pack_ready", "授权执行 Brain/Studio CodeGraph sync-only closure", "not execute", "GPCF-CODEGRAPH-SYNC-ONLY-CLOSURE-010"]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-SYNC-ONLY-CLOSURE-010"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_sync_authorization_pack=pass "
        "brain=action_required studio=action_required authorized=false "
        "next=GPCF-CODEGRAPH-SYNC-ONLY-CLOSURE-010"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
