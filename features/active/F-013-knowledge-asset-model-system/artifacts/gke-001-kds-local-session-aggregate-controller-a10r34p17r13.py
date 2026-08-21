#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable


CONTROL_ID = "GKE-001-COORDINATION-20260821-001-A10R34P17R13"
RUN_ID = "gke001-a10r34p17r13-kds-session-aggregate"
CHANGE_ID = "replace-r12-session-aggregate-lock-contract-a10r34p17r13"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
ARTIFACTS = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts"
R5_PATH = ARTIFACTS / "gke-001-kds-local-schema-diagnostic-controller-a10r34p17r5.py"
R5_SHA256 = "7e2299ef2f057d43b6c66bad1e1b4fc7608cc2fb44ecef33ef23ade673d856f2"
R8_PATH = ARTIFACTS / "gke-001-kds-local-session-aggregate-controller-a10r34p17r8.py"
R8_SHA256 = "9246748605d46f90260d685ee001f44bb842f4dabc0799bfec6958492b97f3c4"
R10_PATH = ARTIFACTS / "gke-001-kds-local-session-aggregate-controller-a10r34p17r10.py"
R10_SHA256 = "98a0bdedeafa31686e35d98872d3ea49f41ae512160b8ff47f112b4c0283cdd6"
OFFICIAL_ACQUIRE = Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/acquire-lock.sh")
OFFICIAL_RELEASE = Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/release-lock.sh")
SEALED_OFFICIAL_HELPERS = {
    OFFICIAL_ACQUIRE: "fb6d2133e2f5b8402439ef6df2151cfb915803fe0eb327d79c98a4cae0786f36",
    OFFICIAL_RELEASE: "26c1256057df419f8212093fdec8483481dba6d04a89112129c077f5bbb8aa8c",
}
KDS_AUDIT_PREFIX = b"concepts/\xe5\xbc\x80\xe5\x8f\x91/kds/tenants/gehua/orgs/gehua/governance/audits_\xe5\xae\xa1\xe8\xae\xa1/kds-audit-read-view-"
KDS_AUDIT_SUFFIX = re.compile(rb"^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\.md$")
KDS_AUDIT_EXPECTED_COUNT = 17
KDS_AUDIT_MANIFEST_SHA256 = "ad10f211f02d8cd3e629165156d942bcaa0ffbb112d038b90d450b8bbfaaea53"
AUTOPILOT_COMMAND = b"gbrain autopilot --repo /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"
AUTOPILOT_WORKER_COMMAND = b"gbrain jobs work --max-rss"

SEALED_BASELINES: dict[str, dict[str, Any]] = {
    "gpcf": {"head": "9e580d5aedb83e8f4fd4d941a88fc31dedba35d5", "origin": "9e580d5aedb83e8f4fd4d941a88fc31dedba35d5", "ahead": 0, "behind": 0, "ordinary_count": 4, "ordinary_sha256": "24dd1f9e5fd5ce80866b94b0cea78b311e4cbc9830fb8a676d6217e9718adf97", "expanded_count": 4, "expanded_sha256": "24dd1f9e5fd5ce80866b94b0cea78b311e4cbc9830fb8a676d6217e9718adf97"},
    "kds": {"head": "2ac85c55163b7acf0ede699184ac360579ccefaa", "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa", "ahead": 0, "behind": 0, "ordinary_count": 369, "ordinary_sha256": "bd251e57d313f46bcdd4cf8913cfa7e18f8da806286c99f46479bb0546d5e4e6", "expanded_count": 699, "expanded_sha256": "5f1a24800bbee248dc5301c4b6b75b6f9cc4f22f559c2c7a4b35aa34d5757739"},
    "mmc": {"head": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7", "origin": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7", "ahead": 0, "behind": 0, "ordinary_count": 0, "ordinary_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "expanded_count": 0, "expanded_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(path: Path, expected_sha256: str, name: str) -> Any:
    if digest(path.read_bytes()) != expected_sha256:
        raise RuntimeError(f"{name}_sha256")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name}_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_base() -> Any:
    r5 = load_module(R5_PATH, R5_SHA256, "gke001_r13_r5")
    base = r5.load_base()
    base.CONTROL_ID, base.RUN_ID, base.CHANGE_ID = CONTROL_ID, RUN_ID, CHANGE_ID
    base.BASELINES = tuple(
        base.RepoBaseline(
            root,
            SEALED_BASELINES[name]["head"],
            SEALED_BASELINES[name]["origin"],
            SEALED_BASELINES[name]["ordinary_count"],
            SEALED_BASELINES[name]["ordinary_sha256"],
            SEALED_BASELINES[name]["expanded_count"],
            SEALED_BASELINES[name]["expanded_sha256"],
        )
        for name, root in (("gpcf", base.GPCF_ROOT), ("kds", base.KDS_ROOT), ("mmc", base.MMC_ROOT))
    )
    return base


def load_r10() -> Any:
    return load_module(R10_PATH, R10_SHA256, "gke001_r13_r10")


def terminal(status: str, code: str, *, connections: int = 0, **extra: Any) -> dict[str, Any]:
    return {
        "status": status,
        "code": code,
        "control": CONTROL_ID,
        "database_connections": connections,
        "api_requests": 0,
        "fixture_created": False,
        **extra,
    }


def read_official_lock(root: Path) -> tuple[int, int, int, int, int, int] | None:
    lock = root / ".harness/opsx.lock"
    try:
        descriptor = os.open(lock, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    except OSError:
        return None
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or stat.S_IMODE(opened.st_mode) != 0o600:
            return None
        content = os.read(descriptor, opened.st_size + 1)
        completed = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = (opened.st_dev, opened.st_ino, opened.st_mode, opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns)
    if len(content) != opened.st_size or identity != (completed.st_dev, completed.st_ino, completed.st_mode, completed.st_size, completed.st_mtime_ns, completed.st_ctime_ns):
        return None
    try:
        current = lock.lstat()
    except OSError:
        return None
    if identity != (current.st_dev, current.st_ino, current.st_mode, current.st_size, current.st_mtime_ns, current.st_ctime_ns) or not stat.S_ISREG(current.st_mode):
        return None
    try:
        lines = content.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError:
        return None
    if len(lines) != 5:
        return None
    parsed: dict[str, str] = {}
    for line in lines:
        if ": " not in line:
            return None
        key, value = line.split(": ", 1)
        if key in parsed or not value:
            return None
        parsed[key] = value
    if not (
        parsed.get("run_id") == RUN_ID
        and parsed.get("change_id") == CHANGE_ID
        and parsed.get("branch") == "main"
        and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", parsed.get("locked_at", "")) is not None
        and parsed.get("ttl_hours") == "4"
    ):
        return None
    return identity


Runner = Callable[..., Any]


def lock_path_present(root: Path) -> bool:
    try:
        (root / ".harness/opsx.lock").lstat()
        return True
    except OSError:
        return False


def invoke_official(command: tuple[str, ...], timeout: int, runner: Runner) -> bool:
    try:
        result = runner(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def acquire_official_lock(root: Path, timeout: int, runner: Runner = subprocess.run) -> str:
    completed = invoke_official(("/bin/bash", str(OFFICIAL_ACQUIRE), RUN_ID, CHANGE_ID, str(root)), timeout, runner)
    if completed and read_official_lock(root) is not None:
        return "acquired"
    if read_official_lock(root) is not None:
        return "owned_after_acquire_failure"
    return "lock_unresolved" if lock_path_present(root) else "not_acquired"


def release_official_lock(root: Path, timeout: int, runner: Runner = subprocess.run) -> bool:
    if read_official_lock(root) is None:
        return False
    completed = invoke_official(("/bin/bash", str(OFFICIAL_RELEASE), RUN_ID, CHANGE_ID, str(root)), timeout, runner)
    return completed and not lock_path_present(root)


class AuditContractError(RuntimeError):
    pass


def filter_kds_status(data: bytes, root: Path, *, expected_count: int = KDS_AUDIT_EXPECTED_COUNT, expected_manifest: str = KDS_AUDIT_MANIFEST_SHA256) -> bytes:
    retained = []
    excluded = []
    for record in data.split(b"\0"):
        if not record:
            continue
        if record.startswith(b"?? ") and record[3:].startswith(KDS_AUDIT_PREFIX):
            relative, suffix = record[3:], record[3 + len(KDS_AUDIT_PREFIX):]
            if KDS_AUDIT_SUFFIX.fullmatch(suffix) is None:
                raise AuditContractError("audit_name")
            metadata = os.lstat(root / os.fsdecode(relative))
            if not stat.S_ISREG(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
                raise AuditContractError("audit_type")
            excluded.append(record)
            continue
        retained.append(record)
    manifest = digest(b"".join(record + b"\0" for record in excluded))
    if len(excluded) != expected_count or manifest != expected_manifest:
        raise AuditContractError("audit_manifest")
    return b"".join(record + b"\0" for record in retained)


def filtered_kds_status(base: Any, root: Path, expanded: bool) -> tuple[int, str]:
    command = ["/usr/bin/git", "status", "--porcelain=v1", "-z"]
    if expanded:
        command.append("--untracked-files=all")
    try:
        data = filter_kds_status(base.run(tuple(command), cwd=root).stdout, root)
    except (AuditContractError, OSError):
        base.fail("baseline", "GlobalCloud KDS_audit_dynamic_contract")
    return sum(bool(record) for record in data.split(b"\0")), digest(data)


def autopilot_quiescent(runner: Runner = subprocess.run, ps_runner: Runner = subprocess.run) -> bool:
    result = runner(
        ("/bin/launchctl", "print", f"gui/{__import__('os').getuid()}/com.gbrain.autopilot"),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    absence = (getattr(result, "stdout", b"") + getattr(result, "stderr", b"")).lower()
    if result.returncode == 0 or b"could not find service" not in absence:
        return False
    processes = ps_runner(("/bin/ps", "-axo", "pid=,command="), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    return AUTOPILOT_COMMAND not in processes and AUTOPILOT_WORKER_COMMAND not in processes


def check_kds(base: Any, r10: Any) -> None:
    kds = next(item for item in base.BASELINES if item.root == base.KDS_ROOT)
    if base.run(("/usr/bin/git", "branch", "--show-current"), cwd=kds.root).stdout.strip() != b"main":
        base.fail("baseline", "GlobalCloud KDS_branch")
    for ref, expected in (("HEAD", kds.head), ("origin/main", kds.origin)):
        if base.run(("/usr/bin/git", "rev-parse", ref), cwd=kds.root).stdout.decode().strip() != expected:
            base.fail("baseline", f"GlobalCloud KDS_{ref}")
    divergence = base.run(("/usr/bin/git", "rev-list", "--left-right", "--count", "HEAD...origin/main"), cwd=kds.root).stdout.split()
    if divergence != [str(kds.ahead).encode(), str(kds.behind).encode()]:
        base.fail("baseline", "GlobalCloud KDS_divergence")
    if base.run(("/usr/bin/git", "diff", "--cached", "--name-only"), cwd=kds.root).stdout:
        base.fail("baseline", "GlobalCloud KDS_staged")
    if filtered_kds_status(base, kds.root, False) != (kds.ordinary_count, kds.ordinary_sha256):
        base.fail("baseline", "GlobalCloud KDS_filtered_ordinary_dirty")
    if filtered_kds_status(base, kds.root, True) != (kds.expanded_count, kds.expanded_sha256):
        base.fail("baseline", "GlobalCloud KDS_filtered_expanded_dirty")
    if (kds.root / ".harness/opsx.lock").exists():
        base.fail("baseline", "GlobalCloud KDS_opsx_lock")
    r10.check_external_files(base)


def pre_lock_baseline(base: Any, r10: Any) -> str:
    if not autopilot_quiescent():
        base.fail("runtime", "autopilot_not_quiescent")
    for baseline in base.BASELINES:
        if baseline.root == base.KDS_ROOT:
            check_kds(base, r10)
        else:
            base.check_repo(baseline)
    base.validate_runtime()
    for path, expected in SEALED_OFFICIAL_HELPERS.items():
        if digest(path.read_bytes()) != expected:
            base.fail("lock", f"official_{path.name}_helper_drift")
    return base.read_secure_environment()


def post_lock_baseline(base: Any) -> None:
    if not autopilot_quiescent():
        base.fail("runtime", "autopilot_not_quiescent")
    gpcf = next(item for item in base.BASELINES if item.root == base.GPCF_ROOT)
    if base.run(("/usr/bin/git", "branch", "--show-current"), cwd=gpcf.root).stdout.strip() != b"main":
        base.fail("baseline", "GlobalCoud GPCF_branch")
    for ref, expected in (("HEAD", gpcf.head), ("origin/main", gpcf.origin)):
        if base.run(("/usr/bin/git", "rev-parse", ref), cwd=gpcf.root).stdout.decode().strip() != expected:
            base.fail("baseline", f"GlobalCoud GPCF_{ref}")
    divergence = base.run(("/usr/bin/git", "rev-list", "--left-right", "--count", "HEAD...origin/main"), cwd=gpcf.root).stdout.split()
    if divergence != [str(gpcf.ahead).encode(), str(gpcf.behind).encode()]:
        base.fail("baseline", "GlobalCoud GPCF_divergence")
    if base.run(("/usr/bin/git", "diff", "--cached", "--name-only"), cwd=gpcf.root).stdout:
        base.fail("baseline", "GlobalCoud GPCF_staged")
    if base.git_status(gpcf.root, False, allow_own_lock=True) != (gpcf.ordinary_count, gpcf.ordinary_sha256):
        base.fail("baseline", "GlobalCoud GPCF_ordinary_dirty")
    if base.git_status(gpcf.root, True, allow_own_lock=True) != (gpcf.expanded_count, gpcf.expanded_sha256):
        base.fail("baseline", "GlobalCoud GPCF_expanded_dirty")
    if read_official_lock(base.GPCF_ROOT) is None:
        base.fail("lock", "official_lock_contract")
    r10 = load_r10()
    for baseline in base.BASELINES:
        if baseline.root == base.KDS_ROOT:
            check_kds(base, r10)
        elif baseline.root != base.GPCF_ROOT:
            base.check_repo(baseline)
    base.validate_runtime()
    for path, expected in SEALED_OFFICIAL_HELPERS.items():
        if digest(path.read_bytes()) != expected:
            base.fail("lock", f"official_{path.name}_helper_drift")


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    base, acquired = None, False
    result = terminal("stopped_no_change", "not_started")
    try:
        base, r10 = load_base(), load_r10()
        dsn = pre_lock_baseline(base, r10)
        acquisition = acquire_official_lock(base.GPCF_ROOT, base.LOCK_HELPER_TIMEOUT_SECONDS)
        if acquisition == "acquired":
            acquired = True
        elif acquisition == "owned_after_acquire_failure":
            acquired = True
            result = terminal("stopped_no_change", "official_lock_acquire_attempt_failed_owned_lock_cleaned")
            return result
        else:
            return terminal("failed_fail_closed" if acquisition == "lock_unresolved" else "stopped_no_change", f"official_lock_{acquisition}")
        post_lock_baseline(base)
        r8 = load_module(R8_PATH, R8_SHA256, "gke001_r13_r8")
        result = r8.aggregate_sessions(dsn, base) | {"control": CONTROL_ID}
    except Exception as error:
        if base is not None and isinstance(error, base.ControlledFailure):
            result = terminal("stopped_no_change", error.code, step=error.step)
        else:
            result = terminal("stopped_no_change", type(error).__name__)
    finally:
        if acquired and base is not None:
            released = release_official_lock(base.GPCF_ROOT, base.LOCK_HELPER_TIMEOUT_SECONDS)
            result["opsx_lock_released"] = released
            if not released:
                result["status"], result["code"] = "failed_fail_closed", "official_lock_release_unresolved"
        elif base is not None:
            result["opsx_lock_released"] = not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists()
    return result


def self_test() -> dict[str, Any]:
    source = Path(__file__).read_text(encoding="utf-8")
    calls = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)]
    assert not any(node.func.attr in {"lock_helper_acquire", "lock_helper_release"} for node in calls)
    assert "acquire_official_lock(" in source and "release_official_lock(" in source
    assert terminal("stopped_no_change", "x")["database_connections"] == 0
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / ".harness").mkdir()

        def fake_runner(command: tuple[str, ...], **_kwargs: Any) -> SimpleNamespace:
            lock = root / ".harness/opsx.lock"
            if command[1] == str(OFFICIAL_ACQUIRE):
                lock.write_text(f"run_id: {RUN_ID}\nchange_id: {CHANGE_ID}\nbranch: main\nlocked_at: 2026-08-21T00:00:00Z\nttl_hours: 4\n", encoding="utf-8")
                lock.chmod(0o600)
                return SimpleNamespace(returncode=0)
            lock.unlink()
            return SimpleNamespace(returncode=0)

        assert acquire_official_lock(root, 1, fake_runner) == "acquired"
        assert release_official_lock(root, 1, fake_runner)
        assert acquire_official_lock(root, 1, lambda *_args, **_kwargs: SimpleNamespace(returncode=1)) == "not_acquired"

        def timeout_after_lock(command: tuple[str, ...], **_kwargs: Any) -> SimpleNamespace:
            lock = root / ".harness/opsx.lock"
            lock.write_text(f"run_id: {RUN_ID}\nchange_id: {CHANGE_ID}\nbranch: main\nlocked_at: 2026-08-21T00:00:00Z\nttl_hours: 4\n", encoding="utf-8")
            lock.chmod(0o600)
            raise subprocess.TimeoutExpired(command, 1)

        assert acquire_official_lock(root, 1, timeout_after_lock) == "owned_after_acquire_failure"
        assert release_official_lock(root, 1, fake_runner)

        relative = KDS_AUDIT_PREFIX + b"12345678-1234-1234-1234-123456789abc.md"
        audit = root / os.fsdecode(relative)
        audit.parent.mkdir(parents=True)
        audit.write_text("generated", encoding="utf-8")
        dynamic = b"?? " + relative + b"\0?? other.md\0"
        assert filter_kds_status(dynamic, root, expected_count=1, expected_manifest=digest(b"?? " + relative + b"\0")) == b"?? other.md\0"
        malformed = b"?? " + KDS_AUDIT_PREFIX + b"not-a-uuid.md\0"
        try:
            filter_kds_status(malformed, root, expected_count=1, expected_manifest=digest(malformed))
            raise AssertionError("malformed_audit_accepted")
        except AuditContractError:
            pass
        audit.unlink()
        audit.symlink_to(root / "other.md")
        try:
            filter_kds_status(b"?? " + relative + b"\0", root, expected_count=1, expected_manifest=digest(b"?? " + relative + b"\0"))
            raise AssertionError("audit_symlink_accepted")
        except AuditContractError:
            pass

    absent = lambda *_args, **_kwargs: SimpleNamespace(returncode=113, stdout=b"", stderr=b"Could not find service")
    empty_ps = lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout=b"", stderr=b"")
    assert autopilot_quiescent(absent, empty_ps)
    assert not autopilot_quiescent(lambda *_args, **_kwargs: SimpleNamespace(returncode=1, stdout=b"", stderr=b"other failure"), empty_ps)
    assert not autopilot_quiescent(absent, lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout=AUTOPILOT_WORKER_COMMAND, stderr=b""))
    return {"status": "pass", "control": CONTROL_ID, "official_lock_success_failure_release_covered": True, "official_lock_timeout_cleanup_covered": True, "audit_contract_covered": True, "autopilot_quiescence_covered": True, "terminal_adapter_covered": True, "database_connections": 0, "api_requests": 0, "execution_authorized": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--sealed-sha", default="")
    arguments = parser.parse_args()
    try:
        result = self_test() if arguments.self_test else execute(arguments.sealed_sha)
    except Exception as error:
        result = terminal("stopped_no_change", type(error).__name__)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] in {"pass", "completed_read_only"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
