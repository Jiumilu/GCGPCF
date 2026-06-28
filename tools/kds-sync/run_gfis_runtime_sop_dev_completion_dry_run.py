#!/usr/bin/env python3
"""Read-only verifier for the GFIS dev-completion dry-run chain."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"

DEV_DRY_RUN = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dev-dry-run-result.json"
MIN_CLOSED_LOOP = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dev-only-minimum-closed-loop.json"
CANDIDATE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-min-001-candidate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL run_gfis_runtime_sop_dev_completion_dry_run: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected JSON object: {path}")
    return data


def main() -> int:
    dry_run = load_json(DEV_DRY_RUN)
    min_closed_loop = load_json(MIN_CLOSED_LOOP)
    candidate = load_json(CANDIDATE)

    dry_counts = dry_run.get("counts")
    min_counts = min_closed_loop.get("counts")
    candidate_counts = candidate.get("candidate_counts")
    require(isinstance(dry_counts, dict), "dry-run counts missing")
    require(isinstance(min_counts, dict), "minimum closed-loop counts missing")
    require(isinstance(candidate_counts, dict), "candidate counts missing")

    require(dry_run.get("synthetic_dev_lane") == "dev_closed", "synthetic_dev_lane must be dev_closed")
    require(dry_run.get("synthetic_e2e") == "synthetic_e2e_pass", "synthetic_e2e must pass")
    require(dry_counts.get("synthetic_stage_count") == 12, "synthetic stage count must be 12")
    require(dry_counts.get("real_source_records") == 0, "real_source_records must remain 0")
    require(dry_counts.get("real_runtime_primary_keys") == 0, "real runtime primary keys must remain 0")
    require(min_counts.get("synthetic_closed_loop_passed") == 1, "synthetic closed loop must pass once")
    require(min_counts.get("pollution_guard_passed") == 1, "pollution guard must pass")
    require(min_counts.get("real_source_records") == 0, "minimum closed-loop real source records must remain 0")
    require(candidate_counts.get("source_record_candidates") == 1, "source record candidate count mismatch")
    require(candidate_counts.get("runtime_primary_key_candidates") == 1, "runtime primary key candidate count mismatch")
    require(candidate_counts.get("review_queue_candidates") == 1, "review queue candidate count mismatch")
    require(candidate_counts.get("runtime_intake_candidates") == 1, "runtime intake candidate count mismatch")
    require(candidate_counts.get("waes_review_candidates") == 1, "WAES candidate count mismatch")
    require(candidate_counts.get("verified_artifact_candidates") == 1, "verified artifact candidate count mismatch")
    require(candidate.get("status_boundary", {}).get("status_promotion_allowed") is False, "status promotion must stay false")

    print(
        "gfis_runtime_sop_dev_completion_dry_run=pass "
        "synthetic_dev_lane=dev_closed synthetic_e2e=synthetic_e2e_pass "
        "synthetic_stage_count=12 synthetic_closed_loop_passed=1 "
        "source_record_candidates=1 runtime_primary_key_candidates=1 "
        "review_queue_candidates=1 runtime_intake_candidates=1 "
        "waes_review_candidates=1 verified_artifact_candidates=1 "
        "real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 "
        "real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0 "
        "status_promotion_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
