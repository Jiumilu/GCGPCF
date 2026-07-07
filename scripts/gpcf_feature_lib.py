#!/usr/bin/env python3
"""Shared helpers for GPCF 2.0 Feature Workspace scripts."""

from __future__ import annotations

import re
import shutil
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEATURE_ROOT = ROOT / "features"
ACTIVE = FEATURE_ROOT / "active"
DONE = FEATURE_ROOT / "done"
ARCHIVED = FEATURE_ROOT / "archived"
RUNTIME = ROOT / "runtime"
QUEUE_FILE = RUNTIME / "queue.json"
STATE_FILE = RUNTIME / "state.json"
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
PASSING_EVIDENCE = {"pass", "waived"}
FEATURE_ID_RE = re.compile(r"^F-(\d{3})")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "feature"


def ensure_base_dirs() -> None:
    for path in [ACTIVE, DONE, ARCHIVED]:
        path.mkdir(parents=True, exist_ok=True)
    (RUNTIME / "logs").mkdir(parents=True, exist_ok=True)
    if not QUEUE_FILE.exists():
        write_json(QUEUE_FILE, {"schema_version": "2.0", "queue": []})
    if not STATE_FILE.exists():
        write_json(
            STATE_FILE,
            {
                "schema_version": "2.0",
                "mode": "feature_delivery",
                "current_feature": None,
                "roles": ["Dispatcher", "Planner", "Builder", "Evaluator", "Repair", "Recorder"],
            },
        )


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def enqueue_feature(data: dict[str, Any], feature_dir: Path) -> None:
    ensure_base_dirs()
    queue = read_json(QUEUE_FILE, {"schema_version": "2.0", "queue": []})
    entries = [entry for entry in queue.get("queue", []) if entry.get("id") != data["id"]]
    entries.append(
        {
            "id": data["id"],
            "name": data["name"],
            "project": data["project"],
            "priority": data["priority"],
            "status": "queued",
            "current_role": "Dispatcher",
            "workspace": feature_dir.relative_to(ROOT).as_posix(),
            "created_at": data["created_at"],
            "updated_at": now(),
        }
    )
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    entries.sort(key=lambda item: (priority_order.get(str(item.get("priority")), 9), str(item.get("id"))))
    queue["schema_version"] = "2.0"
    queue["queue"] = entries
    write_json(QUEUE_FILE, queue)
    refresh_runtime_state()


def update_queue_entry(feature_id: str, *, status: str | None = None, role: str | None = None) -> None:
    ensure_base_dirs()
    queue = read_json(QUEUE_FILE, {"schema_version": "2.0", "queue": []})
    for entry in queue.get("queue", []):
        if entry.get("id") == feature_id:
            if status:
                entry["status"] = status
            if role:
                entry["current_role"] = role
            entry["updated_at"] = now()
            break
    write_json(QUEUE_FILE, queue)
    refresh_runtime_state()


def refresh_runtime_state() -> None:
    queue = read_json(QUEUE_FILE, {"schema_version": "2.0", "queue": []})
    active_entries = [
        entry
        for entry in queue.get("queue", [])
        if entry.get("status") not in {"closed", "archived"}
    ]
    state = read_json(
        STATE_FILE,
        {
            "schema_version": "2.0",
            "mode": "feature_delivery",
            "current_feature": None,
            "roles": ["Dispatcher", "Planner", "Builder", "Evaluator", "Repair", "Recorder"],
        },
    )
    state.update(
        {
            "schema_version": "2.0",
            "mode": "feature_delivery",
            "current_feature": active_entries[0]["id"] if active_entries else None,
            "active_feature_count": len(active_entries),
            "queue_length": len(queue.get("queue", [])),
            "updated_at": now(),
        }
    )
    state.setdefault("roles", ["Dispatcher", "Planner", "Builder", "Evaluator", "Repair", "Recorder"])
    write_json(STATE_FILE, state)


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
            if item.strip().startswith("- ") and nested_list:
                data[current][nested_list].append(unquote(item.strip()[2:]))
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
            "## LOOP 日志",
            "",
            "### Iteration 0",
            "",
            "1. 这轮做什么？",
            "   - 创建 Feature Workspace。",
            "2. 改了什么？",
            "   - 初始化 feature.yaml、journal.md、evidence/、artifacts/。",
            "3. 怎么验证？",
            "   - 关闭前运行 gpcf_check_evidence.py。",
            "4. 发现什么问题？",
            "   - none",
            "5. 是否可以提交？",
            "   - 否，Evidence Gate 仍待验证。",
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
