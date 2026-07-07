#!/usr/bin/env python3
"""Shared helpers for GPCF 2.0 Feature Workspace scripts."""

from __future__ import annotations

import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEATURE_ROOT = ROOT / "features"
ACTIVE = FEATURE_ROOT / "active"
DONE = FEATURE_ROOT / "done"
ARCHIVED = FEATURE_ROOT / "archived"
PROJECTS = {
    "aaas",
    "brain",
    "was",
    "xiaoc",
    "waes",
    "gpc",
    "studio",
    "gpcf",
    "xwail",
    "gfis",
    "mmc",
    "kds",
    "xiaog",
    "pvaos",
    "sop",
    "pkc",
    "xgd",
}
PRIORITIES = {"P0", "P1", "P2", "P3"}
STEPS = ["plan", "implement", "evaluate", "repair", "commit"]
PASSING_EVIDENCE = {"pass", "not_required"}
FEATURE_ID_RE = re.compile(r"^F-(\d{3})")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "feature"


def ensure_base_dirs() -> None:
    for path in [ACTIVE, DONE, ARCHIVED]:
        path.mkdir(parents=True, exist_ok=True)


def feature_dirs() -> list[Path]:
    ensure_base_dirs()
    paths: list[Path] = []
    for base in [ACTIVE, DONE, ARCHIVED]:
        paths.extend(path for path in base.iterdir() if path.is_dir() and FEATURE_ID_RE.match(path.name))
    return sorted(paths)


def next_feature_id() -> str:
    used = []
    for path in feature_dirs():
        match = FEATURE_ID_RE.match(path.name)
        if match:
            used.append(int(match.group(1)))
    return f"F-{(max(used) + 1) if used else 1:03d}"


def find_feature(feature_id: str) -> Path:
    ensure_base_dirs()
    for base in [ACTIVE, DONE, ARCHIVED]:
        matches = sorted(path for path in base.iterdir() if path.is_dir() and path.name.startswith(feature_id))
        if matches:
            return matches[0]
    raise SystemExit(f"FAIL: feature not found: {feature_id}")


def feature_file(feature_dir: Path) -> Path:
    path = feature_dir / "feature.yaml"
    if not path.exists():
        raise SystemExit(f"FAIL: missing feature.yaml: {feature_dir.relative_to(ROOT)}")
    return path


def journal_file(feature_dir: Path) -> Path:
    path = feature_dir / "journal.md"
    if not path.exists():
        raise SystemExit(f"FAIL: missing journal.md: {feature_dir.relative_to(ROOT)}")
    return path


def default_feature(
    *,
    feature_id: str,
    name: str,
    project: str,
    goal: str,
    owner: str,
    priority: str,
) -> dict[str, Any]:
    timestamp = now()
    return {
        "id": feature_id,
        "name": slugify(name),
        "project": project,
        "status": "active",
        "goal": goal,
        "owner": owner,
        "priority": priority,
        "scope": {"in": [], "out": []},
        "acceptance": [],
        "loop": {"current_step": "plan", "iteration": 0},
        "evidence": {
            "tests": "pending",
            "build": "pending",
            "screenshots": "pending",
            "api": "pending",
            "summary": "pending",
        },
        "blockers": [],
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def quote_yaml(value: Any) -> str:
    text = str(value)
    if text == "":
        return '""'
    if re.search(r"[:#\[\]{}]|^\s|\s$", text):
        return '"' + text.replace('"', '\\"') + '"'
    return text


def render_feature(data: dict[str, Any]) -> str:
    lines = [
        f"id: {quote_yaml(data['id'])}",
        f"name: {quote_yaml(data['name'])}",
        f"project: {quote_yaml(data['project'])}",
        f"status: {quote_yaml(data['status'])}",
        f"goal: {quote_yaml(data['goal'])}",
        f"owner: {quote_yaml(data['owner'])}",
        f"priority: {quote_yaml(data['priority'])}",
        "scope:",
        "  in:",
    ]
    for item in data["scope"]["in"]:
        lines.append(f"    - {quote_yaml(item)}")
    lines.append("  out:")
    for item in data["scope"]["out"]:
        lines.append(f"    - {quote_yaml(item)}")
    lines.append("acceptance:")
    for item in data["acceptance"]:
        lines.append(f"  - {quote_yaml(item)}")
    lines.extend(
        [
            "loop:",
            f"  current_step: {quote_yaml(data['loop']['current_step'])}",
            f"  iteration: {data['loop']['iteration']}",
            "evidence:",
            f"  tests: {quote_yaml(data['evidence']['tests'])}",
            f"  build: {quote_yaml(data['evidence']['build'])}",
            f"  screenshots: {quote_yaml(data['evidence']['screenshots'])}",
            f"  api: {quote_yaml(data['evidence']['api'])}",
            f"  summary: {quote_yaml(data['evidence']['summary'])}",
            "blockers:",
        ]
    )
    for item in data["blockers"]:
        lines.append(f"  - {quote_yaml(item)}")
    lines.extend(
        [
            f"created_at: {quote_yaml(data['created_at'])}",
            f"updated_at: {quote_yaml(data['updated_at'])}",
            "",
        ]
    )
    return "\n".join(lines)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"')
    return value


def read_feature(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {
        "scope": {"in": [], "out": []},
        "acceptance": [],
        "loop": {},
        "evidence": {},
        "blockers": [],
    }
    current: str | None = None
    nested_list: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        if not raw.startswith(" "):
            key, _, value = raw.partition(":")
            current = key.strip()
            nested_list = None
            if value.strip():
                data[current] = unquote(value)
            elif current not in data:
                data[current] = []
            continue
        if current in {"acceptance", "blockers"} and raw.startswith("  - "):
            data[current].append(unquote(raw[4:]))
            continue
        if current in {"scope", "loop", "evidence"} and raw.startswith("  "):
            item = raw[2:]
            if item.startswith("- ") and nested_list:
                data[current][nested_list].append(unquote(item[2:]))
                continue
            key, _, value = item.partition(":")
            key = key.strip()
            if value.strip():
                data[current][key] = unquote(value)
                if key == "iteration":
                    data[current][key] = int(str(data[current][key]))
                nested_list = None
            else:
                data[current][key] = []
                nested_list = key
    return data


def write_feature(path: Path, data: dict[str, Any]) -> None:
    data["updated_at"] = now()
    path.write_text(render_feature(data), encoding="utf-8")


def render_journal(feature_id: str, name: str) -> str:
    return "\n".join(
        [
            f"# {feature_id} {name}",
            "",
            "## Loop Journal",
            "",
            "### Iteration 0",
            "",
            "1. 这轮做什么？",
            "   - Create Feature Workspace.",
            "2. 改了什么？",
            "   - Initialized feature.yaml, journal.md, evidence/, artifacts/.",
            "3. 怎么验证？",
            "   - Run gpcf_check_evidence.py before close.",
            "4. 发现什么问题？",
            "   - none",
            "5. 是否可以提交？",
            "   - no, evidence gate pending.",
            "",
        ]
    )


def append_journal(feature_dir: Path, *, iteration: int, answers: list[str]) -> None:
    path = journal_file(feature_dir)
    labels = [
        "1. 这轮做什么？",
        "2. 改了什么？",
        "3. 怎么验证？",
        "4. 发现什么问题？",
        "5. 是否可以提交？",
    ]
    lines = ["", f"### Iteration {iteration}", ""]
    for label, answer in zip(labels, answers):
        lines.append(label)
        lines.append(f"   - {answer}")
    lines.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def run_command(command: list[str]) -> tuple[str, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    output = (result.stdout + result.stderr).strip()
    status = "pass" if result.returncode == 0 else "fail"
    return status, output or "(no output)"


def evidence_complete(data: dict[str, Any]) -> bool:
    return all(str(value) in PASSING_EVIDENCE for value in data["evidence"].values())


def move_feature_to_done(feature_dir: Path) -> Path:
    target = DONE / feature_dir.name
    if target.exists():
        raise SystemExit(f"FAIL: done feature already exists: {target.relative_to(ROOT)}")
    shutil.move(str(feature_dir), str(target))
    return target
