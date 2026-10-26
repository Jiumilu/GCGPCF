"""Stage 1 console export: drift classification and deterministic JSON output."""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_export_module():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("console_export", SCRIPTS / "console_export.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def feature(fid, step, status="active", project="gpcf", priority="P1"):
    return {
        "id": fid,
        "step": step,
        "status": status,
        "project": project,
        "priority": priority,
    }


def entry(fid, status, role, project="gpcf", priority="P1"):
    return {
        "id": fid,
        "status": status,
        "current_role": role,
        "project": project,
        "priority": priority,
    }


def kinds(drifts, fid):
    return sorted(item["kind"] for item in drifts if item["feature"] == fid)


def test_classify_drift_separates_truth_from_mapping_gaps():
    module = load_export_module()
    features = [
        feature("F-001", "plan"),
        feature("F-002", "plan"),
        feature("F-003", "evaluate"),
        feature("F-004", "commit"),
        feature("F-005", "evaluate"),
    ]
    queue = {
        "F-002": entry("F-002", "queued", "Dispatcher"),
        "F-003": entry("F-003", "queued", "Dispatcher"),
        "F-004": entry("F-004", "commit", "Recorder"),
        "F-005": entry("F-005", "evaluated", "Evaluator"),
        "F-009": entry("F-009", "queued", "Dispatcher"),
    }
    drifts = module.classify_drift(features, queue)

    # initial plan state -> mapping gap, not drift
    assert kinds(drifts, "F-002") == ["mapping_gap", "mapping_gap"]
    # stale derived view far from the initial state -> drift
    assert kinds(drifts, "F-003") == ["drift", "drift"]
    # consistent entry -> nothing
    assert kinds(drifts, "F-004") == []
    assert kinds(drifts, "F-005") == []
    # workspace without queue entry / queue entry without workspace
    assert kinds(drifts, "F-001") == ["missing_in_queue"]
    assert kinds(drifts, "F-009") == ["orphan_in_queue"]
    # every record carries the truth and derived side
    for item in drifts:
        assert set(item) == {"feature", "kind", "field", "truth", "derived"}


def test_classify_drift_reports_project_and_priority_mismatch():
    module = load_export_module()
    features = [feature("F-010", "commit")]
    queue = {"F-010": entry("F-010", "commit", "Recorder", project="wae", priority="P0")}
    drifts = module.classify_drift(features, queue)
    fields = sorted(item["field"] for item in drifts)
    assert fields == ["queue.priority", "queue.project"]


def test_export_is_deterministic_except_timestamp(tmp_path):
    module = load_export_module()
    first = tmp_path / "one"
    second = tmp_path / "two"
    module.export(first)
    module.export(second)

    names = ["features.json", "projects.json", "gates.json", "docs.json", "meta.json"]
    for name in names:
        assert (first / name).is_file(), name
        left = json.loads((first / name).read_text(encoding="utf-8"))
        right = json.loads((second / name).read_text(encoding="utf-8"))
        if name == "meta.json":
            left.pop("generated_at")
            right.pop("generated_at")
        assert left == right, name

    meta = json.loads((first / "meta.json").read_text(encoding="utf-8"))
    assert meta["counts"]["features"] >= 1
    assert meta["drift"]["total"] == len(meta["drift"]["items"])
    assert set(meta["drift"]["by_kind"]) <= {
        "drift",
        "mapping_gap",
        "missing_in_queue",
        "orphan_in_queue",
    }
    features = json.loads((first / "features.json").read_text(encoding="utf-8"))
    assert features["count"] == len(features["items"])


def test_check_mode_flags_stale_and_missing(tmp_path):
    module = load_export_module()
    out = tmp_path / "data"
    assert module.main(["--out", str(out), "--quiet"]) == 0
    assert module.main(["--out", str(out), "--check", "--quiet"]) == 0

    before = (out / "features.json").read_text(encoding="utf-8")
    assert module.main(["--out", str(out), "--check", "--quiet"]) == 0
    assert (out / "features.json").read_text(encoding="utf-8") == before, "check must not rewrite"

    tampered = out / "projects.json"
    payload = json.loads(tampered.read_text(encoding="utf-8"))
    payload["count"] = payload["count"] + 1
    tampered.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    assert module.main(["--out", str(out), "--check", "--quiet"]) == 1

    (out / "docs.json").unlink()
    assert module.main(["--out", str(out), "--check", "--quiet"]) == 1
