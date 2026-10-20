"""Repository-only checks reject missing project register rows."""

import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_validator(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools/kds-sync" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def register_without_wae(source, target):
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    removed = [line for line in lines if line.startswith("| GlobalCloud WAE |")]
    assert len(removed) == 1
    target.write_text("".join(line for line in lines if line not in removed), encoding="utf-8")


def test_master_register_repository_check_rejects_missing_wae(tmp_path, monkeypatch, capsys):
    validator = load_validator("validate_project_master_plan_register")
    register = tmp_path / "master.md"
    register_without_wae(validator.REGISTER, register)
    monkeypatch.setattr(validator, "REGISTER", register)
    monkeypatch.setattr(sys, "argv", ["validate_project_master_plan_register.py", "--repository-only"])

    assert validator.main() == 1
    assert "expected exactly one project row in register: GlobalCloud WAE" in capsys.readouterr().out


def test_implementation_register_rejects_missing_wae(tmp_path, monkeypatch, capsys):
    validator = load_validator("validate_project_implementation_register")
    register = tmp_path / "implementation.md"
    register_without_wae(validator.REGISTER, register)
    monkeypatch.setattr(validator, "REGISTER", register)

    assert validator.main() == 1
    assert "expected exactly one project row in implementation register: GlobalCloud WAE" in capsys.readouterr().out


@pytest.mark.parametrize("project", ["World", "PDC", "SLC"])
def test_project_group_master_rejects_missing_project_responsibility(project, tmp_path, monkeypatch, capsys):
    validator = load_validator("validate_project_master_plan_register")
    source = validator.GROUP_MASTER.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    removed = [line for line in lines if line.startswith(f"| {project} |")]
    assert len(removed) == 1
    group_master = tmp_path / "group-master.md"
    group_master.write_text("".join(line for line in lines if line not in removed), encoding="utf-8")
    monkeypatch.setattr(validator, "GROUP_MASTER", group_master)
    monkeypatch.setattr(sys, "argv", ["validate_project_master_plan_register.py", "--repository-only"])

    assert validator.main() == 1
    assert f"expected exactly one project responsibility row: {project}" in capsys.readouterr().out
