#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import stat
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable


CONTROL_ID = "GKE-001-COORDINATION-20260821-002-A10R34P17R14"
RUN_ID = "gke001-a10r34p17r14-autopilot-quiescence"
CHANGE_ID = "verify-kds-autopilot-quiescence-and-restore-a10r34p17r14"
GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
PLIST = Path("/Users/lujunxiang/Library/LaunchAgents/com.gbrain.autopilot.plist")
PLIST_SHA256 = "d2b92752345e157592b2e1fb6e7b1e1c9f81896f1949e79d4528d757628f60e1"
OFFICIAL_ACQUIRE = Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/acquire-lock.sh")
OFFICIAL_RELEASE = Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/release-lock.sh")
OFFICIAL_HELPERS = {
    OFFICIAL_ACQUIRE: "fb6d2133e2f5b8402439ef6df2151cfb915803fe0eb327d79c98a4cae0786f36",
    OFFICIAL_RELEASE: "26c1256057df419f8212093fdec8483481dba6d04a89112129c077f5bbb8aa8c",
}
LABEL = "com.gbrain.autopilot"
SERVICE_UID = 501
LAUNCHD_DOMAIN = f"gui/{SERVICE_UID}"
KDS_ROOT = "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"
AUTOPILOT_MARKER = f"gbrain autopilot --repo {KDS_ROOT}".encode()
WORKER_MARKER = b"gbrain jobs work --max-rss"
QUIET_SECONDS = 20
TIMEOUT_SECONDS = 30

Runner = Callable[..., Any]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result(status: str, code: str, **extra: Any) -> dict[str, Any]:
    return {
        "status": status,
        "code": code,
        "control": CONTROL_ID,
        "database_connections": 0,
        "api_requests": 0,
        "fixture_created": False,
        **extra,
    }


def target() -> str:
    return f"{LAUNCHD_DOMAIN}/{LABEL}"


def checked_plist() -> None:
    metadata = PLIST.lstat()
    if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o644:
        raise RuntimeError("plist_type_or_mode")
    if digest(PLIST) != PLIST_SHA256:
        raise RuntimeError("plist_sha256")


def checked_helpers() -> None:
    for path, expected in OFFICIAL_HELPERS.items():
        if digest(path) != expected:
            raise RuntimeError(f"{path.name}_sha256")


def command(args: tuple[str, ...], runner: Runner = subprocess.run) -> Any:
    return runner(args, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=TIMEOUT_SECONDS)


def process_tree(runner: Runner = subprocess.run) -> tuple[list[int], dict[int, int]]:
    output = runner(("/bin/ps", "-axo", "pid=,ppid=,command="), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=TIMEOUT_SECONDS).stdout
    autopilots: list[int] = []
    workers: dict[int, int] = {}
    for line in output.splitlines():
        fields = line.split(maxsplit=2)
        if len(fields) != 3 or not fields[0].isdigit() or not fields[1].isdigit():
            continue
        pid, parent, command_line = int(fields[0]), int(fields[1]), fields[2]
        if AUTOPILOT_MARKER in command_line:
            autopilots.append(pid)
        elif WORKER_MARKER in command_line:
            workers[parent] = workers.get(parent, 0) + 1
    return autopilots, workers


def absent(previous_autopilot_pid: int, runner: Runner = subprocess.run) -> bool:
    current = command(("/bin/launchctl", "print", target()), runner)
    text = (current.stdout + current.stderr).lower()
    autopilots, workers = process_tree(runner)
    return current.returncode != 0 and b"could not find service" in text and not autopilots and workers.get(previous_autopilot_pid, 0) == 0


def active(runner: Runner = subprocess.run) -> int | None:
    current = command(("/bin/launchctl", "print", target()), runner)
    autopilots, workers = process_tree(runner)
    if current.returncode == 0 and b"state = running" in current.stdout and len(autopilots) == 1 and workers.get(autopilots[0], 0) >= 1:
        return autopilots[0]
    return None


def stable_for(predicate: Callable[[], bool], seconds: int, *, clock: Callable[[], float] = time.monotonic, sleeper: Callable[[float], None] = time.sleep) -> bool:
    deadline = clock() + seconds
    while clock() < deadline:
        if not predicate():
            return False
        sleeper(1)
    return predicate()


def eventually(predicate: Callable[[], bool], seconds: int, *, clock: Callable[[], float] = time.monotonic, sleeper: Callable[[float], None] = time.sleep) -> bool:
    deadline = clock() + seconds
    while clock() < deadline:
        if predicate():
            return True
        sleeper(1)
    return predicate()


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__)) != sealed_sha:
        raise RuntimeError("sealed_sha")
    if Path.cwd().resolve() != GPCF_ROOT:
        raise RuntimeError("gpcf_root")
    if os.getuid() != SERVICE_UID:
        raise RuntimeError("service_uid")
    checked_plist()
    checked_helpers()
    previous_pid = active()
    if previous_pid is None:
        return result("stopped_no_change", "autopilot_precondition_not_active")
    booted_out = False
    acquired = False
    response = result("stopped_no_change", "not_started")
    try:
        acquired = command(("/bin/bash", str(OFFICIAL_ACQUIRE), RUN_ID, CHANGE_ID, str(GPCF_ROOT))).returncode == 0
        if not acquired:
            response = result("stopped_no_change", "opsx_lock_not_acquired")
            return response
        booted_out = True
        stopped = command(("/bin/launchctl", "bootout", target()))
        if stopped.returncode != 0:
            response = result("stopped_no_change", "autopilot_bootout_failed")
            return response
        quiet_started = eventually(lambda: absent(previous_pid), TIMEOUT_SECONDS)
        quiet = quiet_started and stable_for(lambda: absent(previous_pid), QUIET_SECONDS)
        if not quiet:
            response = result("failed_recovered", "autopilot_quiet_window_failed")
            return response
        response = result("completed_quiescence_restored", "autopilot_quiet_window_passed", quiet_seconds=QUIET_SECONDS)
        return response
    except Exception as error:
        response = result("failed_recovered", type(error).__name__)
    finally:
        restoration_ok = True
        try:
            if booted_out:
                restored = command(("/bin/launchctl", "bootstrap", LAUNCHD_DOMAIN, str(PLIST))).returncode == 0
                restoration_ok = restored and eventually(lambda: active() is not None, TIMEOUT_SECONDS)
        except Exception:
            restoration_ok = False
        finally:
            if acquired:
                try:
                    released = command(("/bin/bash", str(OFFICIAL_RELEASE), RUN_ID, CHANGE_ID, str(GPCF_ROOT))).returncode == 0
                except Exception:
                    released = False
                response["opsx_lock_released"] = released
                if not released:
                    response["status"], response["code"] = "failed_recovered", "opsx_lock_release_failed"
        if not restoration_ok:
            response["status"], response["code"] = "failed_recovered", "autopilot_restore_failed"
    return response


def self_test() -> dict[str, Any]:
    assert result("x", "y")["database_connections"] == 0
    assert LAUNCHD_DOMAIN == "gui/501" and target() == "gui/501/com.gbrain.autopilot"
    assert AUTOPILOT_MARKER.endswith(KDS_ROOT.encode())
    assert WORKER_MARKER == b"gbrain jobs work --max-rss"
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imports = {alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)) for alias in node.names}
    assert not imports & {"psycopg", "requests", "urllib", "httpx", "sqlalchemy"}
    ticks = [0.0]
    def clock() -> float:
        return ticks[0]
    def sleeper(_seconds: float) -> None:
        ticks[0] += 1
    assert stable_for(lambda: True, 3, clock=clock, sleeper=sleeper)
    ticks[0] = 0.0
    calls = [True, False]
    assert not stable_for(lambda: calls.pop(0), 3, clock=clock, sleeper=sleeper)
    ticks[0] = 0.0
    attempts = [False, False, True]
    assert eventually(lambda: attempts.pop(0), 3, clock=clock, sleeper=sleeper)
    ps = b"101 1 bun gbrain autopilot --repo /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS\n102 101 bun gbrain jobs work --max-rss 8192\n103 1 bun gbrain jobs work --max-rss 8192\n"
    fake = lambda *_args, **_kwargs: type("Result", (), {"stdout": ps})()
    assert process_tree(fake) == ([101], {101: 1, 1: 1})
    replacement = b"201 1 bun gbrain autopilot --repo /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS\n202 201 bun gbrain jobs work --max-rss 8192\n"
    def replacement_runner(args: tuple[str, ...], **_kwargs: Any) -> SimpleNamespace:
        if args[1] == "launchctl":
            return SimpleNamespace(returncode=113, stdout=b"", stderr=b"Could not find service")
        return SimpleNamespace(returncode=0, stdout=replacement, stderr=b"")
    assert not absent(101, replacement_runner)
    original_command, original_active, original_absent, original_eventually, original_stable_for, original_timeout = command, active, absent, eventually, stable_for, TIMEOUT_SECONDS
    events: list[str] = []
    def timeout_runner(args: tuple[str, ...], **_kwargs: Any) -> SimpleNamespace:
        if args[0] == "/bin/launchctl" and args[1] == "bootout":
            events.append("bootout")
            raise subprocess.TimeoutExpired(args, TIMEOUT_SECONDS)
        if args[0] == "/bin/launchctl" and args[1] == "bootstrap":
            events.append("bootstrap")
        elif args[0] == "/bin/bash" and "release-lock.sh" in args[1]:
            events.append("release")
        elif args[0] == "/bin/bash":
            events.append("acquire")
        return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")
    try:
        globals()["command"] = timeout_runner
        globals()["active"] = lambda: 101
        globals()["TIMEOUT_SECONDS"] = 0
        receipt = execute(digest(Path(__file__)))
        assert receipt["status"] == "failed_recovered" and receipt["opsx_lock_released"] and events == ["acquire", "bootout", "bootstrap", "release"]
    finally:
        globals()["command"], globals()["active"], globals()["absent"], globals()["eventually"], globals()["stable_for"], globals()["TIMEOUT_SECONDS"] = original_command, original_active, original_absent, original_eventually, original_stable_for, original_timeout
    events.clear()
    def success_runner(args: tuple[str, ...], **_kwargs: Any) -> SimpleNamespace:
        if args[0] == "/bin/launchctl":
            events.append(args[1])
        elif args[0] == "/bin/bash" and "release-lock.sh" in args[1]:
            events.append("release")
        elif args[0] == "/bin/bash":
            events.append("acquire")
        return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")
    wait_calls = [0]
    def traced_eventually(predicate: Callable[[], bool], _seconds: int) -> bool:
        wait_calls[0] += 1
        events.append("wait_absent" if wait_calls[0] == 1 else "wait_active")
        return predicate()
    def traced_stable(predicate: Callable[[], bool], _seconds: int) -> bool:
        events.append("stable_quiet")
        return predicate()
    try:
        globals()["command"] = success_runner
        globals()["active"] = lambda: 101
        globals()["absent"] = lambda _pid: True
        globals()["eventually"] = traced_eventually
        globals()["stable_for"] = traced_stable
        receipt = execute(digest(Path(__file__)))
        assert receipt["status"] == "completed_quiescence_restored" and receipt["opsx_lock_released"] and events == ["acquire", "bootout", "wait_absent", "stable_quiet", "bootstrap", "wait_active", "release"]
    finally:
        globals()["command"], globals()["active"], globals()["absent"], globals()["eventually"], globals()["stable_for"], globals()["TIMEOUT_SECONDS"] = original_command, original_active, original_absent, original_eventually, original_stable_for, original_timeout
    return {"status": "pass", "control": CONTROL_ID, "service_only": True, "database_connections": 0, "api_requests": 0, "execution_authorized": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--sealed-sha", default="")
    args = parser.parse_args()
    try:
        response = self_test() if args.self_test else execute(args.sealed_sha)
    except Exception as error:
        response = result("failed_recovered", type(error).__name__)
    print(json.dumps(response, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if response["status"] in {"pass", "completed_quiescence_restored", "stopped_no_change"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
