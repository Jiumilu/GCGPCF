#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
from datetime import datetime
import hashlib
import importlib.util
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable


CONTROL_ID = "GKE-001-COORDINATION-20260821-003-A10R34P17R15"
RUN_ID = "gke001-a10r34p17r15-quiescent-session-read"
CHANGE_ID = "read-kds-session-aggregate-during-sealed-autopilot-quiescence-a10r34p17r15"
GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
ARTIFACTS = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts"
R5_PATH = ARTIFACTS / "gke-001-kds-local-schema-diagnostic-controller-a10r34p17r5.py"
R5_SHA256 = "7e2299ef2f057d43b6c66bad1e1b4fc7608cc2fb44ecef33ef23ade673d856f2"
R8_PATH = ARTIFACTS / "gke-001-kds-local-session-aggregate-controller-a10r34p17r8.py"
R8_SHA256 = "9246748605d46f90260d685ee001f44bb842f4dabc0799bfec6958492b97f3c4"
R10_PATH = ARTIFACTS / "gke-001-kds-local-session-aggregate-controller-a10r34p17r10.py"
R10_SHA256 = "98a0bdedeafa31686e35d98872d3ea49f41ae512160b8ff47f112b4c0283cdd6"
OFFICIAL_ACQUIRE = Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/acquire-lock.sh")
OFFICIAL_RELEASE = Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/release-lock.sh")
OFFICIAL_HELPERS = {
    OFFICIAL_ACQUIRE: "fb6d2133e2f5b8402439ef6df2151cfb915803fe0eb327d79c98a4cae0786f36",
    OFFICIAL_RELEASE: "26c1256057df419f8212093fdec8483481dba6d04a89112129c077f5bbb8aa8c",
}
SERVICE_UID = 501
LAUNCHD_DOMAIN = "gui/501"
LABEL = "com.gbrain.autopilot"
PLIST = Path("/Users/lujunxiang/Library/LaunchAgents/com.gbrain.autopilot.plist")
PLIST_SHA256 = "d2b92752345e157592b2e1fb6e7b1e1c9f81896f1949e79d4528d757628f60e1"
AUTOPILOT_MARKER = b"gbrain autopilot --repo /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"
WORKER_MARKER = b"gbrain jobs work --max-rss"
QUIET_SECONDS = 20
TIMEOUT_SECONDS = 30
KDS_AUDIT_PREFIX = b"concepts/\xe5\xbc\x80\xe5\x8f\x91/kds/tenants/gehua/orgs/gehua/governance/audits_\xe5\xae\xa1\xe8\xae\xa1/kds-audit-read-view-"
KDS_AUDIT_SUFFIX = re.compile(rb"^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\.md$")
KDS_AUDIT_EXPECTED_COUNT = 17
KDS_AUDIT_MANIFEST_SHA256 = "ad10f211f02d8cd3e629165156d942bcaa0ffbb112d038b90d450b8bbfaaea53"
KDS_RETAINED_GOVERNANCE_REPORT = Path("_governance/distributed-knowledge-runs/distributed-knowledge-governance-20260821-073153/report.md")
KDS_RETAINED_GOVERNANCE_REPORT_SHA256 = "6bb9acef6d234d542133106c74cdafc7b8d663aadb2e247e31bf37da1d24c330"
KDS_RETAINED_GOVERNANCE_REPORT_SIZE = 15946

SEALED_BASELINES: dict[str, dict[str, Any]] = {
    "gpcf": {
        "head": "9e580d5aedb83e8f4fd4d941a88fc31dedba35d5",
        "origin": "9e580d5aedb83e8f4fd4d941a88fc31dedba35d5",
        "ordinary_count": 38,
        "ordinary_sha256": "2bdb226540a3d2ed5b68fc42f95c9d2108d9a662f7c9fd4c45259d7725474408",
        "expanded_count": 38,
        "expanded_sha256": "2bdb226540a3d2ed5b68fc42f95c9d2108d9a662f7c9fd4c45259d7725474408",
    },
    "kds": {
        "head": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "ordinary_count": 376,
        "ordinary_sha256": "74e6c11e778363b2e050aad0eb9a2257d6d275548e6e4b72f6d11ddeb2027dbc",
        "expanded_count": 706,
        "expanded_sha256": "4ff7681a41bd675aa49d8935b1d98caef5e60bfc9cded886ed115d232443caa3",
    },
    "mmc": {
        "head": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7",
        "origin": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7",
        "ordinary_count": 0,
        "ordinary_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "expanded_count": 0,
        "expanded_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
}

Runner = Callable[..., Any]

# Dynamic imports are confined to sealed artifacts and must never create a
# repository bytecode side effect during either preflight or execution.
sys.dont_write_bytecode = True


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def terminal(status: str, code: str, **extra: Any) -> dict[str, Any]:
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


def load_module(path: Path, expected: str, name: str) -> Any:
    if digest(path) != expected:
        raise RuntimeError(f"{name}_sha256")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name}_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def assert_no_artifact_bytecode() -> None:
    if any(ARTIFACTS.rglob("__pycache__")):
        raise RuntimeError("artifact_bytecode_present")


def load_base() -> Any:
    r5 = load_module(R5_PATH, R5_SHA256, "r15_r5")
    base = r5.load_base()
    base.CONTROL_ID, base.RUN_ID, base.CHANGE_ID = CONTROL_ID, RUN_ID, CHANGE_ID
    base.BASELINES = tuple(
        base.RepoBaseline(root, values["head"], values["origin"], values["ordinary_count"], values["ordinary_sha256"], values["expanded_count"], values["expanded_sha256"])
        for name, root in (("gpcf", GPCF_ROOT), ("kds", KDS_ROOT), ("mmc", MMC_ROOT))
        for values in (SEALED_BASELINES[name],)
    )
    return base


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


def active(runner: Runner = subprocess.run) -> int | None:
    state = command(("/bin/launchctl", "print", target()), runner)
    autopilots, workers = process_tree(runner)
    if state.returncode == 0 and b"state = running" in state.stdout and len(autopilots) == 1 and workers.get(autopilots[0], 0) >= 1:
        return autopilots[0]
    return None


def absent(previous_pid: int, runner: Runner = subprocess.run) -> bool:
    state = command(("/bin/launchctl", "print", target()), runner)
    text = (state.stdout + state.stderr).lower()
    autopilots, workers = process_tree(runner)
    return state.returncode != 0 and b"could not find service" in text and not autopilots and workers.get(previous_pid, 0) == 0


def eventually(predicate: Callable[[], bool], seconds: int, *, clock: Callable[[], float] = time.monotonic, sleeper: Callable[[float], None] = time.sleep) -> bool:
    deadline = clock() + seconds
    while clock() < deadline:
        if predicate():
            return True
        sleeper(1)
    return predicate()


def stable_for(predicate: Callable[[], bool], seconds: int, *, clock: Callable[[], float] = time.monotonic, sleeper: Callable[[float], None] = time.sleep) -> bool:
    deadline = clock() + seconds
    while clock() < deadline:
        if not predicate():
            return False
        sleeper(1)
    return predicate()


def checked_static_inputs() -> None:
    if os.getuid() != SERVICE_UID:
        raise RuntimeError("service_uid")
    metadata = PLIST.lstat()
    if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o644 or digest(PLIST) != PLIST_SHA256:
        raise RuntimeError("plist_contract")
    for path, expected in OFFICIAL_HELPERS.items():
        if digest(path) != expected:
            raise RuntimeError(f"{path.name}_sha256")
    if any(not values for values in SEALED_BASELINES.values()):
        raise RuntimeError("baseline_unsealed")


def filter_kds_status(data: bytes) -> bytes:
    retained, excluded = [], []
    for record in data.split(b"\0"):
        if not record:
            continue
        if record.startswith(b"?? ") and record[3:].startswith(KDS_AUDIT_PREFIX):
            relative = record[3:]
            if KDS_AUDIT_SUFFIX.fullmatch(relative[len(KDS_AUDIT_PREFIX):]) is None:
                raise RuntimeError("audit_name")
            entry = KDS_ROOT / os.fsdecode(relative)
            mode = entry.lstat().st_mode
            if not stat.S_ISREG(mode) or stat.S_ISLNK(mode):
                raise RuntimeError("audit_type")
            excluded.append(record)
        else:
            retained.append(record)
    manifest = hashlib.sha256(b"".join(record + b"\0" for record in excluded)).hexdigest()
    if len(excluded) != KDS_AUDIT_EXPECTED_COUNT or manifest != KDS_AUDIT_MANIFEST_SHA256:
        raise RuntimeError("audit_manifest")
    return b"".join(record + b"\0" for record in retained)


def filtered_kds_status(base: Any, expanded: bool) -> tuple[int, str]:
    args = ["/usr/bin/git", "status", "--porcelain=v1", "-z"]
    if expanded:
        args.append("--untracked-files=all")
    data = filter_kds_status(base.run(tuple(args), cwd=KDS_ROOT).stdout)
    return sum(bool(record) for record in data.split(b"\0")), hashlib.sha256(data).hexdigest()


def check_retained_kds_governance_report() -> None:
    report = KDS_ROOT / KDS_RETAINED_GOVERNANCE_REPORT
    metadata = report.lstat()
    if not stat.S_ISREG(metadata.st_mode) or report.is_symlink() or stat.S_IMODE(metadata.st_mode) != 0o644 or metadata.st_uid != os.getuid() or metadata.st_nlink != 1 or metadata.st_size != KDS_RETAINED_GOVERNANCE_REPORT_SIZE:
        raise RuntimeError("retained_governance_report_type")
    if digest(report) != KDS_RETAINED_GOVERNANCE_REPORT_SHA256:
        raise RuntimeError("retained_governance_report_content")


def check_kds(base: Any, r10: Any) -> None:
    expected = SEALED_BASELINES["kds"]
    if base.run(("/usr/bin/git", "branch", "--show-current"), cwd=KDS_ROOT).stdout.strip() != b"main":
        base.fail("baseline", "kds_branch")
    for ref, value in (("HEAD", expected["head"]), ("origin/main", expected["origin"])):
        if base.run(("/usr/bin/git", "rev-parse", ref), cwd=KDS_ROOT).stdout.decode().strip() != value:
            base.fail("baseline", f"kds_{ref}")
    if base.run(("/usr/bin/git", "rev-list", "--left-right", "--count", "HEAD...origin/main"), cwd=KDS_ROOT).stdout.split() != [b"0", b"0"]:
        base.fail("baseline", "kds_divergence")
    if base.run(("/usr/bin/git", "diff", "--cached", "--name-only"), cwd=KDS_ROOT).stdout:
        base.fail("baseline", "kds_staged")
    if filtered_kds_status(base, False) != (expected["ordinary_count"], expected["ordinary_sha256"]):
        base.fail("baseline", "kds_filtered_ordinary")
    if filtered_kds_status(base, True) != (expected["expanded_count"], expected["expanded_sha256"]):
        base.fail("baseline", "kds_filtered_expanded")
    check_retained_kds_governance_report()
    r10.check_external_files(base)


def check_official_lock(root: Path = GPCF_ROOT, *, after_read: Callable[[Path], None] | None = None) -> None:
    lock = root / ".harness/opsx.lock"
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(lock, flags)
    except OSError as error:
        raise RuntimeError("official_lock_open") from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o600 or metadata.st_uid != os.getuid() or metadata.st_nlink != 1:
            raise RuntimeError("official_lock_metadata")
        content = os.read(descriptor, metadata.st_size + 1)
        if len(content) != metadata.st_size:
            raise RuntimeError("official_lock_read")
        if after_read is not None:
            after_read(lock)
        current = lock.lstat()
        if (current.st_dev, current.st_ino, current.st_mode, current.st_size, current.st_uid, current.st_nlink) != (metadata.st_dev, metadata.st_ino, metadata.st_mode, metadata.st_size, metadata.st_uid, metadata.st_nlink):
            raise RuntimeError("official_lock_replaced")
    finally:
        os.close(descriptor)
    try:
        values = dict(line.split(": ", 1) for line in content.decode("utf-8", "strict").splitlines())
        datetime.strptime(values["locked_at"], "%Y-%m-%dT%H:%M:%SZ")
    except (KeyError, ValueError, UnicodeError):
        raise RuntimeError("official_lock_content") from None
    if values != {"run_id": RUN_ID, "change_id": CHANGE_ID, "branch": "main", "locked_at": values["locked_at"], "ttl_hours": "4"}:
        raise RuntimeError("official_lock_content")


def check_gpcf(base: Any, *, own_lock: bool) -> None:
    expected = SEALED_BASELINES["gpcf"]
    if base.run(("/usr/bin/git", "branch", "--show-current"), cwd=GPCF_ROOT).stdout.strip() != b"main":
        base.fail("baseline", "gpcf_branch")
    for ref, value in (("HEAD", expected["head"]), ("origin/main", expected["origin"])):
        if base.run(("/usr/bin/git", "rev-parse", ref), cwd=GPCF_ROOT).stdout.decode().strip() != value:
            base.fail("baseline", f"gpcf_{ref}")
    if base.run(("/usr/bin/git", "rev-list", "--left-right", "--count", "HEAD...origin/main"), cwd=GPCF_ROOT).stdout.split() != [b"0", b"0"]:
        base.fail("baseline", "gpcf_divergence")
    if base.run(("/usr/bin/git", "diff", "--cached", "--name-only"), cwd=GPCF_ROOT).stdout:
        base.fail("baseline", "gpcf_staged")
    for expanded, count_key, sha_key in ((False, "ordinary_count", "ordinary_sha256"), (True, "expanded_count", "expanded_sha256")):
        args = ["/usr/bin/git", "status", "--porcelain=v1", "-z"]
        if expanded:
            args.append("--untracked-files=all")
        records = [record for record in base.run(tuple(args), cwd=GPCF_ROOT).stdout.split(b"\0") if record and record != b"?? .harness/opsx.lock"]
        data = b"".join(record + b"\0" for record in records)
        if (sum(bool(record) for record in records), hashlib.sha256(data).hexdigest()) != (expected[count_key], expected[sha_key]):
            base.fail("baseline", f"gpcf_{'expanded' if expanded else 'ordinary'}_dirty")
    if own_lock:
        check_official_lock()
    elif (GPCF_ROOT / ".harness/opsx.lock").exists():
        base.fail("baseline", "gpcf_opsx_lock")


def read_kds_dsn(base: Any) -> str:
    # One bounded in-memory read of the sealed 0600 local config; only this
    # loopback gbrain DSN is retained, and no config value is emitted.
    content = base.secure_read(base.KDS_ENV, 742)
    dsn = ""
    for raw in content.decode("utf-8", "strict").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[7:]
        if line.startswith("KDS_INTAKE_DATABASE_URL="):
            values = shlex.split(line.split("=", 1)[1], posix=True)
            if len(values) == 1:
                dsn = values[0]
            break
    parsed = urllib.parse.urlparse(dsn)
    if parsed.scheme not in ("postgres", "postgresql") or parsed.hostname not in ("localhost", "127.0.0.1", "::1") or parsed.port not in (None, 5432) or parsed.path.lstrip("/") != "gbrain":
        raise RuntimeError("database_target")
    return dsn


def preflight(base: Any, r10: Any, *, own_lock: bool, read_dsn: bool = False) -> str | None:
    mmc = next(item for item in base.BASELINES if item.root == MMC_ROOT)
    check_gpcf(base, own_lock=own_lock)
    base.check_repo(mmc)
    check_kds(base, r10)
    return read_kds_dsn(base) if read_dsn else None


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__)) != sealed_sha:
        raise RuntimeError("sealed_sha")
    checked_static_inputs()
    if Path.cwd().resolve() != GPCF_ROOT:
        raise RuntimeError("gpcf_root")
    base: Any | None = None
    acquired = booted_out = False
    response = terminal("stopped_no_change", "not_started")
    try:
        assert_no_artifact_bytecode()
        base, r10 = load_base(), load_module(R10_PATH, R10_SHA256, "r15_r10")
        assert_no_artifact_bytecode()
        dsn = preflight(base, r10, own_lock=False, read_dsn=True)
        if dsn is None:
            return terminal("stopped_no_change", "database_target")
        if active() is None:
            return terminal("stopped_no_change", "autopilot_precondition_not_active")
        acquired = command(("/bin/bash", str(OFFICIAL_ACQUIRE), RUN_ID, CHANGE_ID, str(GPCF_ROOT))).returncode == 0
        if not acquired:
            return terminal("stopped_no_change", "opsx_lock_not_acquired")
        preflight(base, r10, own_lock=True)
        previous_pid = active()
        if previous_pid is None:
            return terminal("stopped_no_change", "autopilot_changed_before_bootout")
        booted_out = True
        if command(("/bin/launchctl", "bootout", target())).returncode != 0:
            return terminal("stopped_no_change", "autopilot_bootout_failed")
        if not eventually(lambda: absent(previous_pid), TIMEOUT_SECONDS) or not stable_for(lambda: absent(previous_pid), QUIET_SECONDS):
            return terminal("failed_recovered", "autopilot_quiet_window_failed")
        preflight(base, r10, own_lock=True)
        r8 = load_module(R8_PATH, R8_SHA256, "r15_r8")
        assert_no_artifact_bytecode()
        response = r8.aggregate_sessions(dsn, base) | {"control": CONTROL_ID, "quiescent_read": True}
    except Exception as error:
        response = terminal("stopped_no_change", type(error).__name__)
    finally:
        restored = True
        try:
            if booted_out:
                restored = command(("/bin/launchctl", "bootstrap", LAUNCHD_DOMAIN, str(PLIST))).returncode == 0 and eventually(lambda: active() is not None, TIMEOUT_SECONDS)
        except Exception:
            restored = False
        finally:
            if acquired:
                released = False
                try:
                    released = command(("/bin/bash", str(OFFICIAL_RELEASE), RUN_ID, CHANGE_ID, str(GPCF_ROOT))).returncode == 0
                except BaseException as error:
                    response["opsx_lock_release_error_class"] = type(error).__name__
                response["opsx_lock_released"] = released
                if not released:
                    response["status"], response["code"] = "failed_fail_closed", "opsx_lock_release_unresolved"
        if not restored:
            response["status"], response["code"] = "failed_fail_closed", "autopilot_restore_failed"
    return response


def self_test() -> dict[str, Any]:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = {alias.name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)) for alias in node.names}
    assert not {name.split(".")[0] for name in imports} & {"requests", "httpx", "sqlalchemy"}
    assert "urllib.request" not in imports
    assert target() == "gui/501/com.gbrain.autopilot"
    with tempfile.TemporaryDirectory(prefix="gke001-r15-lock-") as temporary:
        root = Path(temporary)
        harness = root / ".harness"
        harness.mkdir(mode=0o700)
        lock = harness / "opsx.lock"
        valid_lock = f"run_id: {RUN_ID}\nchange_id: {CHANGE_ID}\nbranch: main\nlocked_at: 2026-08-21T00:00:00Z\nttl_hours: 4\n".encode("utf-8")

        def write_lock(content: bytes = valid_lock, mode: int = 0o600) -> None:
            lock.unlink(missing_ok=True)
            lock.write_bytes(content)
            lock.chmod(mode)

        write_lock()
        check_official_lock(root)
        write_lock(valid_lock.replace(CHANGE_ID.encode(), b"wrong-change"))
        try:
            check_official_lock(root)
            raise AssertionError("official_lock_owner")
        except RuntimeError as error:
            assert str(error) == "official_lock_content"
        write_lock(mode=0o644)
        try:
            check_official_lock(root)
            raise AssertionError("official_lock_mode")
        except RuntimeError as error:
            assert str(error) == "official_lock_metadata"
        write_lock()
        hardlink = harness / "opsx.lock.hardlink"
        os.link(lock, hardlink)
        try:
            check_official_lock(root)
            raise AssertionError("official_lock_links")
        except RuntimeError as error:
            assert str(error) == "official_lock_metadata"
        hardlink.unlink()
        write_lock()

        def replace_lock(path: Path) -> None:
            replacement = path.with_name("replacement")
            replacement.write_bytes(valid_lock)
            replacement.chmod(0o600)
            os.replace(replacement, path)

        try:
            check_official_lock(root, after_read=replace_lock)
            raise AssertionError("official_lock_replacement")
        except RuntimeError as error:
            assert str(error) == "official_lock_replaced"
    ticks, attempts = [0.0], [False, False, True]
    def clock() -> float:
        return ticks[0]
    def sleeper(_seconds: float) -> None:
        ticks[0] += 1
    assert eventually(lambda: attempts.pop(0), 3, clock=clock, sleeper=sleeper)
    calls = [True, False]
    assert not stable_for(lambda: calls.pop(0), 3, clock=clock, sleeper=sleeper)
    assert terminal("x", "y")["database_connections"] == 0
    originals = {name: globals()[name] for name in ("load_base", "load_module", "check_gpcf", "check_kds", "read_kds_dsn", "active", "absent", "command", "eventually", "stable_for")}
    events: list[str] = []
    module_calls = [0]
    def fake_module(_path: Path, _expected: str, _name: str) -> Any:
        module_calls[0] += 1
        if module_calls[0] % 2:
            return SimpleNamespace(check_external_files=lambda _base: None)
        return SimpleNamespace(aggregate_sessions=lambda _dsn, _base: events.append("aggregate") or {"status": "completed_read_only", "code": "session_ownership_aggregate_complete", "database_connections": 1, "api_requests": 0, "fixture_created": False})
    def fake_command(args: tuple[str, ...], **_kwargs: Any) -> SimpleNamespace:
        if args[0] == "/bin/launchctl":
            events.append(args[1])
        elif args[0] == "/bin/bash" and "release-lock.sh" in args[1]:
            events.append("release")
        elif args[0] == "/bin/bash":
            events.append("acquire")
        return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")
    wait_calls = [0]
    def fake_eventually(predicate: Callable[[], bool], _seconds: int) -> bool:
        wait_calls[0] += 1
        events.append("wait_absent" if wait_calls[0] == 1 else "wait_active")
        return predicate()
    try:
        fake_base = SimpleNamespace(
            BASELINES=(SimpleNamespace(root=MMC_ROOT),),
            check_repo=lambda _baseline: events.append("mmc"),
        )
        globals()["load_base"] = lambda: fake_base
        globals()["load_module"] = fake_module
        globals()["check_gpcf"] = lambda _base, *, own_lock: events.append(f"gpcf:{own_lock}")
        globals()["check_kds"] = lambda _base, _r10: events.append("kds")
        globals()["read_kds_dsn"] = lambda _base: events.append("dsn") or "sealed-dsn"
        globals()["active"] = lambda: 101
        globals()["absent"] = lambda _pid: True
        globals()["command"] = fake_command
        globals()["eventually"] = fake_eventually
        globals()["stable_for"] = lambda predicate, _seconds: events.append("stable_quiet") or predicate()
        receipt = execute(digest(Path(__file__)))
        expected_preflight = ["gpcf:False", "mmc", "kds", "dsn"]
        expected_locked_preflight = ["gpcf:True", "mmc", "kds"]
        assert receipt["status"] == "completed_read_only" and receipt["opsx_lock_released"] and events == expected_preflight + ["acquire"] + expected_locked_preflight + ["bootout", "wait_absent", "stable_quiet"] + expected_locked_preflight + ["aggregate", "bootstrap", "wait_active", "release"]

        def release_timeout(args: tuple[str, ...], **kwargs: Any) -> SimpleNamespace:
            if args[0] == "/bin/bash" and "release-lock.sh" in args[1]:
                raise subprocess.TimeoutExpired(args, kwargs.get("timeout", TIMEOUT_SECONDS))
            return fake_command(args, **kwargs)

        globals()["command"] = release_timeout
        receipt = execute(digest(Path(__file__)))
        assert receipt["status"] == "failed_fail_closed" and receipt["code"] == "opsx_lock_release_unresolved" and not receipt["opsx_lock_released"] and receipt["opsx_lock_release_error_class"] == "TimeoutExpired"
    finally:
        globals().update(originals)
    return {"status": "pass", "control": CONTROL_ID, "execution_authorized": False, "database_connections": 0, "api_requests": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--sealed-sha", default="")
    args = parser.parse_args()
    if args.self_test == args.execute:
        raise SystemExit("choose exactly one mode")
    try:
        response = self_test() if args.self_test else execute(args.sealed_sha)
    except Exception as error:
        response = terminal("failed_fail_closed", type(error).__name__)
    print(json.dumps(response, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if response["status"] in {"pass", "completed_read_only", "stopped_no_change"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
