#!/usr/bin/env python3
"""Validate the post-scheme-recognition dirty repository disposition queue."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
LIVE_SNAPSHOT = ROOT / "docs/harness/evidence/globalcloud-project-group-live-status-snapshot-20260626.md"
CURRENT_JSON = ROOT / "docs/harness/evidence/project_group_live_status_current.json"
TZ = timezone(timedelta(hours=8))
FRESHNESS_HOURS = 12

CORE_DOC_TOKENS = [
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "project_group_dirty_disposition_queue_post_scheme_recognition_20260626 = controlled",
    "dirty_disposition_queue_post_scheme_recognition_ready",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "project_group_git_clean = blocked",
]

REFERENCE_TOKENS = [
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md",
    "validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py",
    "project_group_dirty_disposition_queue_post_scheme_recognition_20260626 = controlled",
    "dirty_disposition_queue_post_scheme_recognition_ready",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "review_allowed | `true`",
    "stage_allowed | `true`",
    "commit_allowed | `true`",
    "push_allowed | `true`",
    "delete_allowed | `true`",
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def load_current_snapshot(failures: list[str]) -> dict:
    if not CURRENT_JSON.exists():
        failures.append(f"missing current snapshot: {CURRENT_JSON}")
        return {}
    try:
        return json.loads(CURRENT_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"failed to parse current snapshot: {exc}")
        return {}


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(LIVE_SNAPSHOT, failures)])
    current = load_current_snapshot(failures)

    for token in CORE_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in post-scheme dirty queue: {token}")
    for token in REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")
    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive claim: {token}")

    generated_at_raw = str(current.get("generated_at") or "")
    if generated_at_raw:
        try:
            generated_at = datetime.fromisoformat(generated_at_raw)
            if datetime.now(TZ) - generated_at > timedelta(hours=FRESHNESS_HOURS):
                failures.append("current snapshot is stale for post-scheme dirty queue")
        except ValueError:
            failures.append("current snapshot generated_at is invalid")

    if not isinstance(current.get("review_boundary"), list):
        failures.append("current snapshot review_boundary missing")
    if not isinstance(current.get("observed_dirty"), list):
        failures.append("current snapshot observed_dirty missing")

    result = {
        "gate": "project_group_dirty_disposition_queue_post_scheme_recognition_20260626",
        "status": "pass" if not failures else "fail",
        "review_boundary": current.get("review_boundary", []),
        "observed_dirty": current.get("observed_dirty", []),
        "observed_ahead": current.get("observed_ahead", []),
        "failures": failures,
        "warnings": [
            "This validates the post-scheme-recognition dirty repository disposition queue only; it does not delete files, stage, commit, push, sync KDS API, deploy, or grant accepted/integrated/customer acceptance status."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
