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

import psycopg


CONTROL_ID = "GKE-001-COORDINATION-20260817-056-A10R34P17R6R3"
RUN_ID = "gke001-a10r34p17r6r3-kds-session-attribution"
CHANGE_ID = "attribute-kds-local-schema-sessions-a10r34p17r6r3"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
R6R2_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-session-attribution-controller-a10r34p17r6r2.py"
R6R2_CONTROLLER_SHA256 = "1de418bd65b05feaa74f6441ea6b7887e0ba9a697beda60aa278ae5575979b74"

# Filled after the R6R3 artifacts exist. Untracked content changes do not alter these status records.
SEALED_BASELINES = {
    "gpcf": {
        "head": "11d022b818332d2271a78b427c326eb454507a5a",
        "origin": "11d022b818332d2271a78b427c326eb454507a5a",
        "ordinary_count": 747,
        "ordinary_sha256": "1e27b8b31f1b54f7b69b38d3b498acc648cb855bbaaa3fc48c07d1f5fc60dcca",
        "expanded_count": 764,
        "expanded_sha256": "368f0bcf21251f6d3bdb29658fd6e3148a9ac2677a5ff4a36ce0b67d99c5713e",
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


def load_r6r2() -> Any:
    if digest(R6R2_CONTROLLER.read_bytes()) != R6R2_CONTROLLER_SHA256:
        raise RuntimeError("r6r2_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r6r2_base", R6R2_CONTROLLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("r6r2_controller_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_base(r6r2: Any) -> tuple[Any, Any]:
    r6r1 = r6r2.load_r6r1()
    base = r6r2.load_base(r6r1)
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
    return r6r1, base


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


def safe_error_code(error: BaseException) -> str:
    return str(getattr(error, "sqlstate", None) or type(error).__name__)


def attribute_sessions(dsn: str, r6r1: Any, base: Any) -> dict[str, Any]:
    connection: psycopg.Connection[Any] | None = None
    connection_count = 0
    transaction_count = 0
    rollback_confirmed = False
    close_confirmed = False
    status = "failed_no_change"
    code = "session_attribution_failed"
    extra: dict[str, Any] = {}
    cleanup_errors: list[str] = []
    try:
        connection = psycopg.connect(
            dsn,
            autocommit=True,
            connect_timeout=base.DATABASE_CONNECT_TIMEOUT_SECONDS,
            options=(
                f"-c lock_timeout={base.DATABASE_LOCK_TIMEOUT_MILLISECONDS} "
                f"-c statement_timeout={base.DATABASE_STATEMENT_TIMEOUT_MILLISECONDS} "
                f"-c idle_in_transaction_session_timeout={base.DATABASE_IDLE_TRANSACTION_TIMEOUT_MILLISECONDS}"
            ),
        )
        connection_count = 1
        connection.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        transaction_count = 1
        database_name, transaction_read_only, xid_before = connection.execute(
            "SELECT current_database(), current_setting('transaction_read_only'), txid_current_if_assigned()"
        ).fetchone()
        if database_name != "gbrain" or transaction_read_only != "on":
            status = "stopped_no_change"
            code = "read_only_identity_mismatch"
        else:
            observed_count = int(connection.execute(r6r1.SESSION_COUNT_SQL).fetchone()[0])
            xid_after = connection.execute("SELECT txid_current_if_assigned()").fetchone()[0]
            if observed_count != r6r1.EXPECTED_SESSION_COUNT:
                status = "stopped_no_change"
                code = "session_count_drift"
                extra = {
                    "observed_session_count": observed_count,
                    "expected_session_count": r6r1.EXPECTED_SESSION_COUNT,
                    "xid_before_is_null": xid_before is None,
                    "xid_after_is_null": xid_after is None,
                }
            else:
                rows = connection.execute(r6r1.SESSION_SQL).fetchall()
                if len(rows) != r6r1.EXPECTED_SESSION_COUNT:
                    raise RuntimeError("session_projection_count")
                sessions = [r6r1.session_projection(tuple(row)) for row in rows]
                if any(item["client_location"] == "non_loopback" for item in sessions):
                    status = "stopped_no_change"
                    code = "non_loopback_session_observed"
                    extra = {
                        "session_count": len(sessions),
                        "xid_before_is_null": xid_before is None,
                        "xid_after_is_null": xid_after is None,
                    }
                else:
                    status = "completed_read_only"
                    code = "session_attribution_complete"
                    extra = {
                        "session_count": len(sessions),
                        "sessions": sessions,
                        "xid_before_is_null": xid_before is None,
                        "xid_after_is_null": xid_after is None,
                    }
    except BaseException as error:
        status = "failed_no_change"
        code = "session_attribution_interrupted" if isinstance(error, (KeyboardInterrupt, SystemExit)) else "session_attribution_failed"
        extra = {"error_class": safe_error_code(error)}
    finally:
        if connection is not None:
            if transaction_count:
                try:
                    connection.execute("ROLLBACK")
                    rollback_confirmed = True
                except BaseException as error:
                    cleanup_errors.append(f"rollback:{safe_error_code(error)}")
            try:
                connection.close()
                close_confirmed = bool(getattr(connection, "closed", True))
                if not close_confirmed:
                    cleanup_errors.append("close:not_confirmed")
            except BaseException as error:
                cleanup_errors.append(f"close:{safe_error_code(error)}")

    if cleanup_errors:
        extra = {"prior_code": code, "cleanup_error_classes": cleanup_errors}
        status = "failed_fail_closed"
        code = "session_attribution_cleanup_unresolved"
    return terminal(
        status,
        code,
        connection_count=connection_count,
        transaction_count=transaction_count,
        transaction_mode="repeatable_read_read_only" if transaction_count else "not_started",
        rollback_confirmed=rollback_confirmed,
        connection_close_confirmed=close_confirmed,
        **extra,
    )


def preflight(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r6r1, base = load_base(load_r6r2())
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
    _, base = load_base(load_r6r2())
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
            if cleanup_outcome == "completed" and cleanup_returncode == 0 and not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists():
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
    r6r1, base = load_base(load_r6r2())
    prelock_dsn, _ = base.hard_baseline()
    prelock_dsn = ""
    acquired = False
    result: dict[str, Any] = terminal("stopped_no_change", "not_started")
    try:
        lock_success, acquired, lock_code = run_lock_helper(base, "acquire", sealed_sha)
        if not lock_success:
            result = terminal("failed_fail_closed" if "lock_unresolved" in lock_code else "stopped_no_change", lock_code)
        else:
            dsn, _ = base.hard_baseline(own_lock_expected=True)
            result = attribute_sessions(dsn, r6r1, base)
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


class FakeRows:
    def __init__(self, rows: list[tuple[Any, ...]]):
        self.rows = rows

    def fetchone(self) -> tuple[Any, ...]:
        return self.rows[0]

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self.rows


class FakeConnection:
    def __init__(self, *, fail_begin: bool = False, interrupt_on_count: bool = False):
        self.fail_begin = fail_begin
        self.interrupt_on_count = interrupt_on_count
        self.closed = False
        self.rolled_back = False

    def execute(self, statement: str) -> FakeRows:
        if statement.startswith("BEGIN TRANSACTION"):
            if self.fail_begin:
                raise RuntimeError("begin")
            return FakeRows([])
        if statement.startswith("SELECT current_database()"):
            return FakeRows([("gbrain", "on", None)])
        if "PG_STAT_ACTIVITY" in statement.upper() and "COUNT" in statement.upper():
            if self.interrupt_on_count:
                raise KeyboardInterrupt()
            return FakeRows([(2,)])
        if statement == "SELECT txid_current_if_assigned()":
            return FakeRows([(None,)])
        if "ORDER BY pid" in statement:
            return FakeRows([
                (101, "kds", "client backend", "idle", "Client", "ClientRead", "loopback_ipv4", 52001),
                (102, "gbrain", "client backend", "idle", "Client", "ClientRead", "loopback_ipv4", 52002),
            ])
        if statement == "ROLLBACK":
            self.rolled_back = True
            return FakeRows([])
        raise AssertionError(statement)

    def close(self) -> None:
        self.closed = True


def self_test() -> dict[str, Any]:
    r6r1, base = load_base(load_r6r2())

    with mock.patch.object(psycopg, "connect", side_effect=RuntimeError("connect")):
        connection_failure = attribute_sessions("redacted", r6r1, base)
    assert connection_failure["connection_count"] == 0
    assert connection_failure["transaction_count"] == 0

    begin_failure_connection = FakeConnection(fail_begin=True)
    with mock.patch.object(psycopg, "connect", return_value=begin_failure_connection):
        begin_failure = attribute_sessions("redacted", r6r1, base)
    assert begin_failure["connection_count"] == 1
    assert begin_failure["transaction_count"] == 0
    assert begin_failure_connection.closed

    interrupted_connection = FakeConnection(interrupt_on_count=True)
    with mock.patch.object(psycopg, "connect", return_value=interrupted_connection):
        interrupted = attribute_sessions("redacted", r6r1, base)
    assert interrupted["code"] == "session_attribution_interrupted"
    assert interrupted["connection_count"] == 1
    assert interrupted["transaction_count"] == 1
    assert interrupted["rollback_confirmed"] is True
    assert interrupted["connection_close_confirmed"] is True
    assert interrupted_connection.rolled_back and interrupted_connection.closed

    success = subprocess.CompletedProcess(
        args=(),
        returncode=0,
        stdout=b'{"status":"success","code":"atomic_opsx_lock_acquired"}',
        stderr=b"",
    )
    with mock.patch.object(subprocess, "run", return_value=success), mock.patch.object(base, "owned_lock_state", return_value=True):
        acquired, owned, code = run_lock_helper(base, "acquire", "sealed")
    assert acquired and owned and code == "acquired"
    return terminal(
        "pass",
        "self_test_passed",
        connection_failure_accounting=True,
        begin_failure_accounting=True,
        base_exception_cleanup=True,
        helper_success_exit_recognized=True,
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
    except BaseException as error:
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
