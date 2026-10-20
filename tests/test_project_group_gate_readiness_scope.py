"""The project-group readiness check must cover the registered scope."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/kds-sync/validate_loop_project_group_gate_readiness.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("project_group_gate_readiness_scope", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPT.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def test_readiness_repos_match_current_registry():
    module = load_validator()
    registry = yaml.safe_load((ROOT / "config/project-group-projects.yaml").read_text(encoding="utf-8"))
    expected = [item["repo"] for item in registry["projects"]]
    assert len(expected) == registry["current_project_count"]
    assert [label for label, _ in module.REPOS] == expected
    assert all(path == module.PROJECT_GROUP_ROOT / label for label, path in module.REPOS)


def test_readiness_uses_primary_checkout_for_linked_worktrees():
    module = load_validator()
    common_dir = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"], cwd=ROOT, text=True,
    ).strip()
    common_path = Path(common_dir)
    if not common_path.is_absolute():
        common_path = ROOT / common_path
    assert module.PROJECT_GROUP_ROOT == common_path.resolve().parent.parent


def test_missing_project_gate_fails_instead_of_being_omitted(tmp_path):
    module = load_validator()
    ok, reason = module.run_gate(tmp_path / "missing-project", "Missing Project")
    assert not ok
    assert "Missing Project missing tools/kds-sync/loop_document_gate.py" == reason


def test_readiness_checks_real_checkout_from_linked_worktree(monkeypatch):
    module = load_validator()
    checked_roots = []
    monkeypatch.setattr(module, "REPOS", [])
    monkeypatch.setattr(
        module, "require_gfis_real_fact_entry",
        lambda root: checked_roots.append(root) or {"status_ceiling": "partial"},
    )
    assert module.main() == 0
    assert checked_roots == [module.PROJECT_GROUP_ROOT / "GlobalCoud GPCF"]


def test_readiness_checks_every_registered_project(monkeypatch, capsys):
    module = load_validator()
    checked = []
    monkeypatch.setattr(module, "require_gfis_real_fact_entry", lambda root: {"status_ceiling": "partial"})
    monkeypatch.setattr(module, "gate_invocation_key", lambda path: str(path))
    monkeypatch.setattr(module, "run_gate", lambda path, label: (checked.append(label) or True, ""))
    assert module.main() == 0
    assert checked == [item[0] for item in module.REPOS]
    assert f"checked_repos={len(module.REPOS)}" in capsys.readouterr().out
