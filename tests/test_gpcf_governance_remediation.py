"""Regression checks for the governance repairs that protect existing evidence."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml
import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_document_control():
    path = ROOT / "tools/kds-sync/document_control.py"
    spec = importlib.util.spec_from_file_location("document_control_safety", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_health_report_generation_preserves_review_date(tmp_path, monkeypatch):
    path = ROOT / "tools/kds-sync/loop_document_gate.py"
    spec = importlib.util.spec_from_file_location("loop_document_gate_review_date", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = tmp_path / "health.md"
    mirror = tmp_path / "mirror.md"
    report.write_text("---\nlast_reviewed: 2026-10-01\n---\n\n# Previous\n", encoding="utf-8")
    monkeypatch.setattr(module, "REPORT", report)
    monkeypatch.setattr(module, "MIRROR_REPORT", mirror)
    summary = {
        "gate": "pass", "status_ceiling": "partial", "gate_reasons": [],
        "status_counts": {}, "project_counts": {},
        "repo_md": 0, "kds_md": 0, "local_mirror_ledger_lines": 0,
        "local_mirror_unique_docs": 0, "api_sync_ledger_lines": 0,
        "missing_metadata": 0, "missing_readme_dirs": 0,
        "localization_debt": False, "fixed_doc_id_drift": False,
        "review_overdue_90d": 0, "review_date_unverified": 0,
    }
    module.write_report(summary, {})
    assert "last_reviewed: 2026-10-01" in report.read_text(encoding="utf-8")
    assert mirror.read_text(encoding="utf-8") == report.read_text(encoding="utf-8")


def test_live_snapshot_ignores_only_local_worktree_churn():
    path = ROOT / "tools/kds-sync/build_project_group_live_status_current.py"
    spec = importlib.util.spec_from_file_location("live_status_safety", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    previous = {key: [] for key in module.SEMANTIC_KEYS}
    previous["dirty_details"] = {
        "GlobalCoud GPCF": {"dirty_count": 2},
        "GlobalCloud WAE": {"dirty_count": 1},
    }
    current = {**previous, "dirty_details": {
        "GlobalCoud GPCF": {"dirty_count": 3},
        "GlobalCloud WAE": {"dirty_count": 1},
    }}
    assert module.semantically_same(previous, current)
    current["dirty_details"]["GlobalCloud WAE"]["dirty_count"] = 2
    assert not module.semantically_same(previous, current)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_generated_readme_keeps_review_date_and_custom_frontmatter(tmp_path):
    control = load_document_control()
    readme = tmp_path / "README.md"
    readme.write_text(
        "---\nlast_reviewed: 2026-06-12\nsuperseded_by: [GPCF-DOC-NEW]\n"
        "custom_control:\n  owner_decision: pending\n---\n\n# Old\n",
        encoding="utf-8",
    )
    control.write_text(readme, "# Generated\n")
    text = readme.read_text(encoding="utf-8")
    assert "last_reviewed: 2026-06-12" in text
    assert "superseded_by: [GPCF-DOC-NEW]" in text
    assert "custom_control:\n  owner_decision: pending" in text
    assert text.endswith("# Generated\n")


def test_document_control_dry_run_does_not_change_control_files():
    paths = [
        ROOT / "09-status/globalcloud-document-control-register.md",
        ROOT / ".kds/local-mirror-ledger.jsonl",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "tools/kds-sync/document_control.py", "--dry-run"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "changed_count" in json.loads(result.stdout)
    assert before == [digest(path) for path in paths]


def test_closed_feature_replay_does_not_change_queue_or_evidence():
    paths = [
        ROOT / "runtime/queue.json",
        ROOT / "features/done/F-020-aaas-service-console/feature.yaml",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_check_evidence.py", "F-020"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert "close_candidate=false" in result.stdout
    assert before == [digest(path) for path in paths]


def test_historical_done_feature_with_active_acceptance_is_not_a_close_candidate():
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_check_evidence.py", "F-008", "--check-only"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "acceptance requires this Feature to remain active" in result.stdout


def test_explicit_active_acceptance_blocks_close_without_mutation():
    paths = [
        ROOT / "runtime/queue.json",
        ROOT / "features/active/F-005-factory-exception-intake-dry-run/feature.yaml",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_close_feature.py", "F-005"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "remain active" in result.stderr
    assert before == [digest(path) for path in paths]


def test_explicit_active_acceptance_is_not_an_evidence_close_candidate():
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_check_evidence.py", "F-005", "--check-only"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "acceptance requires this Feature to remain active" in result.stdout


def test_dispatch_dry_run_keeps_runtime_and_feature_unchanged():
    paths = [
        ROOT / "runtime/queue.json",
        ROOT / "features/done/F-020-aaas-service-console/feature.yaml",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_dispatch.py", "F-020", "--dry-run"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "gpcf_dispatch_dry_run" in result.stdout
    assert before == [digest(path) for path in paths]


def test_dispatch_does_not_advance_feature_with_unresolved_blockers(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import gpcf_dispatch

    active = tmp_path / "active"
    feature_dir = active / "F-010-sample"
    feature_dir.mkdir(parents=True)
    monkeypatch.setattr(gpcf_dispatch, "ACTIVE", active)
    monkeypatch.setattr(gpcf_dispatch, "select_feature", lambda _: "F-010")
    monkeypatch.setattr(gpcf_dispatch, "queue_entry", lambda _: {"current_role": "Planner", "status": "implement"})
    monkeypatch.setattr(gpcf_dispatch, "find_feature", lambda _: feature_dir)
    monkeypatch.setattr(gpcf_dispatch, "feature_file", lambda _: feature_dir / "feature.yaml")
    monkeypatch.setattr(gpcf_dispatch, "read_feature", lambda _: {"status": "active", "blockers": ["验收未完成"], "loop": {"iteration": 1}})
    for name in ("write_feature", "update_queue_entry", "append_runtime_log", "append_journal"):
        monkeypatch.setattr(gpcf_dispatch, name, lambda *args, **kwargs: pytest.fail("blocked dispatch wrote state"))
    monkeypatch.setattr(sys, "argv", ["gpcf_dispatch.py", "F-010"])

    with pytest.raises(SystemExit, match="unresolved blockers"):
        gpcf_dispatch.main()


@pytest.mark.parametrize(
    "scope_in,acceptance,role,missing",
    [
        ([], ["验收完成"], [], "scope.in"),
        (["交付范围"], [], [], "acceptance"),
        ([], [], ["--role", "Dispatcher"], "scope.in, acceptance"),
    ],
)
def test_dispatch_requires_planning_before_implementation(tmp_path, monkeypatch, scope_in, acceptance, role, missing):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import gpcf_dispatch

    active = tmp_path / "active"
    feature_dir = active / "F-012-sample"
    feature_dir.mkdir(parents=True)
    monkeypatch.setattr(gpcf_dispatch, "ACTIVE", active)
    monkeypatch.setattr(gpcf_dispatch, "select_feature", lambda _: "F-012")
    monkeypatch.setattr(gpcf_dispatch, "queue_entry", lambda _: {"current_role": "Planner", "status": "plan"})
    monkeypatch.setattr(gpcf_dispatch, "find_feature", lambda _: feature_dir)
    monkeypatch.setattr(gpcf_dispatch, "feature_file", lambda _: feature_dir / "feature.yaml")
    monkeypatch.setattr(gpcf_dispatch, "read_feature", lambda _: {
        "status": "active", "blockers": [], "scope": {"in": scope_in},
        "acceptance": acceptance, "loop": {"iteration": 1},
    })
    for name in ("write_feature", "update_queue_entry", "append_runtime_log", "append_journal"):
        monkeypatch.setattr(gpcf_dispatch, name, lambda *args, **kwargs: pytest.fail("incomplete planning wrote state"))
    monkeypatch.setattr(sys, "argv", ["gpcf_dispatch.py", "F-012", *role, "--dry-run"])

    with pytest.raises(SystemExit, match=missing):
        gpcf_dispatch.main()


def test_project_registry_matches_current_project_scope():
    registry = yaml.safe_load((ROOT / "config/project-group-projects.yaml").read_text(encoding="utf-8"))
    projects = registry["projects"]
    assert registry["current_project_count"] == len(projects)
    assert "wae" in {project["slug"] for project in projects}
    assert {project["slug"] for project in projects} == {
        path.name for path in (ROOT / "projects").iterdir() if path.is_dir()
    }
    assert len({project["repo"] for project in projects}) == len(projects)


def test_bytecode_check_handles_long_names_and_reports_syntax_errors(tmp_path):
    long_source = tmp_path / ("x" * 237 + ".py")
    long_source.write_text("value = 1\n", encoding="utf-8")
    command = [sys.executable, "tools/kds-sync/check_python_bytecode.py", str(tmp_path)]
    passing = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    assert "python_bytecode=pass files=1 failures=0" in passing.stdout

    (tmp_path / "invalid.py").write_text("if (:\n", encoding="utf-8")
    failing = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert failing.returncode != 0
    assert "python_bytecode=fail files=2 failures=1" in failing.stdout
