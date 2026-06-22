#!/usr/bin/env python3
"""Validate WAS project-group admission evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WAS_ROOT = ROOT.parent / "WAS世界资产体系"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-project-group-admission-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-project-group-admission-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-WAS-ADMISSION-001.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
CODEGRAPH_COVERAGE = ROOT / "02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md"


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
        f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stdout}\n{completed.stderr}",
    )
    return completed.stdout.strip()


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed:",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    control_board = read(CONTROL_BOARD)
    status_matrix = read(STATUS_MATRIX)
    coverage = read(CODEGRAPH_COVERAGE)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(WAS_ROOT.exists(), f"WAS root missing: {WAS_ROOT}")
    require((WAS_ROOT / ".git").exists(), "WAS must be a Git repository")
    for path in [
        "AGENTS.md",
        "PROJECT_HARNESS_MANIFEST.md",
        "docs/harness/loop-state.md",
        "docs/harness/evidence/evidence-index.md",
        "docs/harness/loops/loop-round-WAS-LR-001.md",
        "okf/validators/validate_all.py",
    ]:
        require((WAS_ROOT / path).exists(), f"WAS missing required file: {path}")

    require(evidence.get("evidence_id") == "WAS-PROJECT-GROUP-ADMISSION-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_project_group_admitted_as_semantic_foundation_candidate", "invalid evidence status")
    project = evidence.get("project", {})
    require(project.get("key") == "WAS", "WAS key missing")
    require(project.get("role") == "semantic_foundation_project", "WAS role mismatch")
    require(project.get("project_group_position") == 14, "WAS must be project group position 14")
    require(project.get("remote") == "https://github.com/Jiumilu/GCWAS.git", "WAS remote mismatch")
    require(project.get("remote_visibility") == "PRIVATE", "WAS remote visibility mismatch")
    require(project.get("default_branch") == "main", "WAS default branch mismatch")

    governance = evidence.get("governance", {})
    for key in ["agents_md", "project_harness_manifest", "loop_state", "evidence_index", "loop_round", "remote_push_completed"]:
        require(governance.get(key) is True, f"governance marker must be true: {key}")
    for key in ["accepted", "integrated", "production_ready"]:
        require(governance.get(key) is False, f"governance marker must be false: {key}")

    codegraph = evidence.get("codegraph", {})
    require(codegraph.get("version") == "1.0.1", "CodeGraph version mismatch")
    require(codegraph.get("files") == 30, "WAS CodeGraph files mismatch")
    require(codegraph.get("nodes") == 70, "WAS CodeGraph nodes mismatch")
    require(codegraph.get("edges") == 209, "WAS CodeGraph edges mismatch")
    require(codegraph.get("git_tracking_entries_for_codegraph") == 0, "CodeGraph must not be tracked")

    boundaries = evidence.get("boundaries", {})
    require(boundaries.get("semantic_contract_source") is True, "WAS must be semantic contract source")
    for key in ["kds_source_of_record", "gfis_runtime", "waes_gate_authority", "production_write", "external_api_write", "kds_write", "waes_write"]:
        require(boundaries.get(key) is False, f"boundary must remain false: {key}")

    git_status = run(["git", "-C", str(WAS_ROOT), "status", "--short", "--branch", "--ignored"])
    require("## main...origin/main" in git_status, "WAS must track origin/main")
    require("!! .codegraph/" in git_status, "WAS .codegraph must be ignored")
    require(run(["git", "-C", str(WAS_ROOT), "remote", "get-url", "origin"]) == "https://github.com/Jiumilu/GCWAS.git", "WAS origin mismatch")
    head = run(["git", "-C", str(WAS_ROOT), "rev-parse", "HEAD"])
    require(head == project.get("head_commit"), "WAS head commit mismatch")

    was_validation = run(["python3", "okf/validators/validate_all.py"], cwd=WAS_ROOT)
    require("PASS validate_was_dimensions" in was_validation, "WAS validator output missing dimensions pass")
    require("PASS validate_no_stale_bundle" in was_validation, "WAS validator output missing stale bundle pass")

    codegraph_status = run(["codegraph", "status", str(WAS_ROOT)])
    for phrase in ["Files:     30", "Nodes:     70", "Edges:     209", "DB Size:   0.27 MB"]:
        require(phrase in codegraph_status, f"CodeGraph status missing phrase: {phrase}")

    for text_name, text in [
        ("control board", control_board),
        ("status matrix", status_matrix),
        ("codegraph coverage", coverage),
        ("evidence md", evidence_md),
        ("loop round", loop_round),
    ]:
        for phrase in ["WAS", "semantic_foundation_project", "GCWAS"]:
            require(phrase in text, f"{text_name} missing phrase: {phrase}")

    print(
        "was_project_group_admission=pass "
        "project_group_position=14 role=semantic_foundation_project "
        "remote=Jiumilu/GCWAS visibility=PRIVATE codegraph=pass "
        "was_validators=pass accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
