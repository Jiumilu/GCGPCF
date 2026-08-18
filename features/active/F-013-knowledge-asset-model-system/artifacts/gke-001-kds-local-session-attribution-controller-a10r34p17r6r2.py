#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from unittest import mock


CONTROL_ID = "GKE-001-COORDINATION-20260817-055-A10R34P17R6R2"
RUN_ID = "gke001-a10r34p17r6r2-kds-session-attribution"
CHANGE_ID = "attribute-kds-local-schema-sessions-a10r34p17r6r2"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
R6R1_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-session-attribution-controller-a10r34p17r6.py"
R6R1_CONTROLLER_SHA256 = "8e3ec95cb9e61b33b02dd1ee671a8d2739e71f35423b975093b05cd07a61a5d0"

# Filled after the R6R2 artifacts exist. Untracked content changes do not alter these status records.
SEALED_BASELINES = {
    "gpcf": {
        "head": "11d022b818332d2271a78b427c326eb454507a5a",
        "origin": "11d022b818332d2271a78b427c326eb454507a5a",
        "ordinary_count": 745,
        "ordinary_sha256": "e3f428f94a02fefd6902aaa7659040ac4dcbb626f24f0deabf5cb3db677f7639",
        "expanded_count": 762,
        "expanded_sha256": "4622037b9a06f4d02c95918d44f7b7a5dcafedc1c93524133100e2b4759a3ed8",
    },
    "kds": {
        "head": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "ordinary_count": 280,
        "ordinary_sha256": "5673e55d796a4affe1aa33c077e4b758a2da71362afd2946fcc86616c2c0b770",
        "expanded_count": 570,
        "expanded_sha256": "171aa1df9eb9558b1c1dcd296609bf9d3267704846ca72243371826ee2be13b9",
    },
    "mmc": {
        "head": "c93463ff5ee40ce66d8e1a09995ca8c66a24c86d",
        "origin": "c93463ff5ee40ce66d8e1a09995ca8c66a24c86d",
        "ordinary_count": 10,
        "ordinary_sha256": "300ef303a5a647e54931171ff5ebf309192671fbf9f52f027acedf40d7ab8ad9",
        "expanded_count": 98,
        "expanded_sha256": "2fd6e7fe5409ed79e410ea20e722a84eecb1d141d969153b27c969b3ebf6a451",
    },
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_r6r1() -> Any:
    if digest(R6R1_CONTROLLER.read_bytes()) != R6R1_CONTROLLER_SHA256:
        raise RuntimeError("r6r1_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r6r1_base", R6R1_CONTROLLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("r6r1_controller_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_base(r6r1: Any) -> Any:
    base = r6r1.load_base(r6r1.load_r5())
    base.CONTROL_ID = CONTROL_ID
    base.RUN_ID = RUN_ID
    base.CHANGE_ID = CHANGE_ID
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
        for name, root in (("gpcf", GPCF_ROOT), ("kds", KDS_ROOT), ("mmc", MMC_ROOT))
    )
    return base


def terminal(status: str, code: str, **extra: Any) -> dict[str, Any]:
    return {
        "status": status,
        "code": code,
        "control": CONTROL_ID,
        "database": "gbrain",
        "host": "loopback",
        "connection_count": 0,
        "transaction_count": 0,
        "transaction_mode": "not_started",
        "fixture_created": False,
        "api_requests": 0,
        **extra,
    }


def database_terminal(status: str, code: str, **extra: Any) -> dict[str, Any]:
    return terminal(
        status,
        code,
        connection_count=1,
        transaction_count=1,
        transaction_mode="repeatable_read_read_only",
        **extra,
    )


def safe_error_code(error: BaseException) -> str:
    return str(getattr(error, "sqlstate", None) or type(error).__name__)


def preflight(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r6r1 = load_r6r1()
    base = load_base(r6r1)
    dsn, _ = base.hard_baseline()
    del dsn
    return terminal(
        "eligible_for_separate_read_only_session_attribution_authorization",
        "preflight_passed",
        controller_sha256=sealed_sha,
        authorized_connection_count=1,
        authorized_transaction_count=1,
        authorized_transaction_mode="repeatable_read_read_only",
        expected_session_count=r6r1.EXPECTED_SESSION_COUNT,
        raw_application_name_output=False,
        query_text_read=False,
    )


def lock_helper_action(action: str, sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    base = load_base(load_r6r1())
    if action == "acquire":
        return base.lock_helper_acquire()
    if action == "release":
        return base.lock_helper_release()
    if action == "cleanup":
        return base.lock_helper_cleanup()
    raise RuntimeError("lock_helper_action")


def run_lock_helper(base: Any, action: str, sealed_sha: str) -> tuple[bool, bool, str]:
    environment = {
        "HOME": str(Path.home()),
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "PYTHONDONTWRITEBYTECODE": "1",
    }

    def invoke(helper_action: str) -> tuple[str, int, str]:
        try:
            result = subprocess.run(
                (
                    "/usr/bin/python3",
                    str(Path(__file__)),
                    "--lock-helper",
                    "--helper-action",
                    helper_action,
                    "--sealed-sha",
                    sealed_sha,
                ),
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=base.LOCK_HELPER_TIMEOUT_SECONDS,
                env=environment,
            )
            helper_code = "unparseable"
            try:
                helper_code = str(json.loads(result.stdout.decode("utf-8"))["code"])
            except (KeyError, TypeError, ValueError, UnicodeError):
                pass
            return "completed", result.returncode, helper_code
        except subprocess.TimeoutExpired:
            return "timeout", -1, "timeout"
        except OSError:
            return "spawn_failed", -1, "spawn_failed"

    outcome, returncode, helper_code = invoke(action)
    if action == "acquire":
        if outcome == "completed" and returncode == 0 and base.owned_lock_state():
            return True, True, "acquired"
        failure = f"acquire_{outcome}_{helper_code}" if outcome != "completed" else f"acquire_failed_{helper_code}"
        if base.partial_owned_state():
            cleanup_outcome, cleanup_returncode, cleanup_code = invoke("cleanup")
            if (
                cleanup_outcome == "completed"
                and cleanup_returncode == 0
                and not base.OPSX_LOCK.exists()
                and not base.ATOMIC_GUARD.exists()
            ):
                return False, False, f"{failure}_recovered"
            return False, False, f"{failure}_cleanup_{cleanup_code}_lock_unresolved"
        if base.OPSX_LOCK.exists() or base.ATOMIC_GUARD.exists():
            return False, False, f"{failure}_lock_unresolved"
        return False, False, f"{failure}_no_lock"
    released = outcome == "completed" and returncode == 0 and not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists()
    return released, False, "released" if released else f"release_{outcome}_{helper_code}_lock_unresolved"


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r6r1 = load_r6r1()
    base = load_base(r6r1)
    prelock_dsn, _ = base.hard_baseline()
    prelock_dsn = ""
    acquired = False
    result: dict[str, Any] = terminal("stopped_no_change", "not_started")
    try:
        lock_success, acquired, lock_code = run_lock_helper(base, "acquire", sealed_sha)
        if not lock_success:
            result = terminal(
                "failed_fail_closed" if "lock_unresolved" in lock_code else "stopped_no_change",
                lock_code,
            )
        else:
            dsn, _ = base.hard_baseline(own_lock_expected=True)
            r6r1.terminal = database_terminal
            result = r6r1.attribute_sessions(dsn, base)
            dsn = ""
    except base.ControlledFailure as error:
        result = terminal("stopped_no_change", error.code, step=error.step)
    finally:
        prelock_dsn = ""
        if acquired:
            released, _, release_code = run_lock_helper(base, "release", sealed_sha)
            result["opsx_lock_released"] = released
            if not released:
                result["prior_code"] = result.get("code")
                result["status"] = "failed_fail_closed"
                result["code"] = release_code
        else:
            result.setdefault("opsx_lock_released", not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists())
    return result


def self_test() -> dict[str, Any]:
    r6r1 = load_r6r1()
    base = load_base(r6r1)
    assert terminal("stopped_no_change", "before_lock")["connection_count"] == 0
    assert terminal("stopped_no_change", "before_lock")["transaction_count"] == 0
    assert database_terminal("completed_read_only", "complete")["connection_count"] == 1
    assert database_terminal("completed_read_only", "complete")["transaction_count"] == 1

    success = subprocess.CompletedProcess(
        args=(),
        returncode=0,
        stdout=b'{"status":"success","code":"atomic_opsx_lock_acquired"}',
        stderr=b"",
    )
    with mock.patch.object(subprocess, "run", return_value=success), mock.patch.object(base, "owned_lock_state", return_value=True):
        acquired, owned, code = run_lock_helper(base, "acquire", "sealed")
    assert acquired and owned and code == "acquired"

    failure = subprocess.CompletedProcess(
        args=(),
        returncode=3,
        stdout=b'{"status":"stopped_no_change","code":"identity_metadata"}',
        stderr=b"",
    )
    with mock.patch.object(subprocess, "run", return_value=failure), mock.patch.object(base, "partial_owned_state", return_value=False):
        acquired, owned, code = run_lock_helper(base, "acquire", "sealed")
    assert not acquired and not owned and code == "acquire_failed_identity_metadata_no_lock"
    return terminal(
        "pass",
        "self_test_passed",
        helper_success_exit_recognized=True,
        helper_failure_code_preserved=True,
        preconnection_count_zero=True,
        authorized_connection_count=1,
        authorized_transaction_count=1,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--lock-helper", action="store_true")
    parser.add_argument("--sealed-sha", default="")
    parser.add_argument("--helper-action", choices=("acquire", "release", "cleanup"))
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            result = self_test()
        elif arguments.preflight:
            result = preflight(arguments.sealed_sha)
        elif arguments.lock_helper:
            if not arguments.helper_action:
                raise RuntimeError("helper_action")
            result = lock_helper_action(arguments.helper_action, arguments.sealed_sha)
        else:
            result = execute(arguments.sealed_sha)
    except Exception as error:
        result = terminal("stopped_no_change", safe_error_code(error))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] in {
        "success",
        "pass",
        "eligible_for_separate_read_only_session_attribution_authorization",
        "completed_read_only",
    } else 3


if __name__ == "__main__":
    raise SystemExit(main())
