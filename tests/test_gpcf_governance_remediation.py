"""Regression checks for the governance repairs that protect existing evidence."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_document_control():
    path = ROOT / "tools/kds-sync/document_control.py"
    spec = importlib.util.spec_from_file_location("document_control_safety", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_project_registry_matches_current_24_project_scope():
    registry = yaml.safe_load((ROOT / "config/project-group-projects.yaml").read_text(encoding="utf-8"))
    assert registry["current_project_count"] == len(registry["projects"]) == 24
    assert {project["slug"] for project in registry["projects"]} == {
        path.name for path in (ROOT / "projects").iterdir() if path.is_dir()
    }
    assert len({project["repo"] for project in registry["projects"]}) == 24


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
