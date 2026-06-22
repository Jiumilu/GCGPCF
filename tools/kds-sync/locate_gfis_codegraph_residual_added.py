#!/usr/bin/env python3
"""Read-only locator for GFIS CodeGraph residual added state."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"
SCANNABLE_EXTENSIONS = (".py", ".js", ".ts", ".yaml", ".yml", ".liquid")


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def require_ok(result: subprocess.CompletedProcess[str], label: str) -> str:
    if result.returncode != 0:
        raise SystemExit(f"FAIL: {label}: {result.stderr or result.stdout}")
    return result.stdout


def main() -> int:
    status = json.loads(require_ok(run(["codegraph", "status", "--json", "."], GFIS_ROOT), "codegraph status"))
    files = json.loads(require_ok(run(["codegraph", "files", "--json"], GFIS_ROOT), "codegraph files"))
    indexed_paths = {str(item["path"]) for item in files if isinstance(item, dict) and item.get("path")}
    untracked = require_ok(run(["git", "ls-files", "--others", "--exclude-standard"], GFIS_ROOT), "git untracked").splitlines()
    untracked_scannable = [path for path in untracked if path.endswith(SCANNABLE_EXTENSIONS)]
    untracked_scannable_not_indexed = [path for path in untracked_scannable if path not in indexed_paths]

    sync_probe = require_ok(run(["codegraph", "sync"], GFIS_ROOT), "codegraph sync")
    post_status = json.loads(require_ok(run(["codegraph", "status", "--json", "."], GFIS_ROOT), "post-sync codegraph status"))

    payload: dict[str, Any] = {
        "locator_id": "GFIS-CODEGRAPH-RESIDUAL-ADDED-LOCATOR-20260622",
        "gfis_root": str(GFIS_ROOT),
        "pre_sync_pending_changes": status.get("pendingChanges"),
        "post_sync_pending_changes": post_status.get("pendingChanges"),
        "indexed_file_count": len(indexed_paths),
        "untracked_files_total": len(untracked),
        "untracked_codegraph_scannable_files": len(untracked_scannable),
        "untracked_codegraph_scannable_not_indexed_count": len(untracked_scannable_not_indexed),
        "untracked_codegraph_scannable_not_indexed": untracked_scannable_not_indexed,
        "sync_probe_contains_added_one_zero_nodes": "Added: 1" in sync_probe and "0 nodes" in sync_probe,
        "exact_pending_file_identified": len(untracked_scannable_not_indexed) == 1,
        "locator_conclusion": "pending_added_not_mapped_to_untracked_scannable_file"
        if not untracked_scannable_not_indexed
        else "pending_added_has_untracked_scannable_candidates",
        "cleanup_performed": False,
        "git_write_performed": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
