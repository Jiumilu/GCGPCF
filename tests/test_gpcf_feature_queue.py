"""F-002: Feature creation must enter the Runtime queue."""

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_new_feature_updates_queue_state_and_dispatch_log(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import gpcf_feature_lib as lib
    import gpcf_new_feature

    active = tmp_path / "features" / "active"
    runtime = tmp_path / "runtime"
    for name, value in {
        "ROOT": tmp_path,
        "ACTIVE": active,
        "DONE": tmp_path / "features" / "done",
        "ARCHIVED": tmp_path / "features" / "archived",
        "RUNTIME": runtime,
        "QUEUE_FILE": runtime / "queue.json",
        "STATE_FILE": runtime / "state.json",
    }.items():
        monkeypatch.setattr(lib, name, value)
    monkeypatch.setattr(gpcf_new_feature, "ACTIVE", active)
    monkeypatch.setattr(sys, "argv", [
        "gpcf_new_feature.py", "--project", "gpcf", "--name", "Queue Sample",
        "--priority", "P1", "--goal", "Verify queue creation",
    ])

    assert gpcf_new_feature.main() == 0
    feature = active / "F-001-queue-sample"
    assert yaml.safe_load((feature / "feature.yaml").read_text())["status"] == "active"
    assert (feature / "journal.md").is_file()
    queue = json.loads((runtime / "queue.json").read_text())["queue"]
    assert [(item["id"], item["status"], item["current_role"], item["workspace"]) for item in queue] == [
        ("F-001", "queued", "Dispatcher", "features/active/F-001-queue-sample")
    ]
    state = json.loads((runtime / "state.json").read_text())
    assert (state["mode"], state["active_feature_count"], state["queue_length"], state["current_feature"]) == (
        "feature_delivery", 1, 1, "F-001"
    )
    log = json.loads((runtime / "logs" / "F-001.jsonl").read_text().splitlines()[0])
    assert (log["role"], log["status"]) == ("Dispatcher", "queued")


def test_runtime_current_feature_skips_blocked_and_recorded_entries(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import gpcf_feature_lib as lib

    runtime = tmp_path / "runtime"
    runtime.mkdir()
    queue_file = runtime / "queue.json"
    state_file = runtime / "state.json"
    queue_file.write_text(json.dumps({"schema_version": "2.0", "queue": [
        {"id": "F-024", "status": "queued", "current_role": "Dispatcher", "updated_at": "2026-10-16T00:00:00+00:00"},
        {"id": "F-025", "status": "blocked", "current_role": "Dispatcher", "updated_at": "2026-10-18T00:00:00+00:00"},
        {"id": "F-005", "status": "commit", "current_role": "Recorder", "updated_at": "2026-10-18T01:00:00+00:00"},
    ]}))
    monkeypatch.setattr(lib, "QUEUE_FILE", queue_file)
    monkeypatch.setattr(lib, "STATE_FILE", state_file)

    lib.refresh_runtime_state()

    state = json.loads(state_file.read_text())
    assert state["current_feature"] == "F-024"
    assert state["active_feature_count"] == 3
