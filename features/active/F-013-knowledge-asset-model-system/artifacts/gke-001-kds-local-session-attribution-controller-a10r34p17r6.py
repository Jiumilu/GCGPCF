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


CONTROL_ID = "GKE-001-COORDINATION-20260817-054-A10R34P17R6R1"
RUN_ID = "gke001-a10r34p17r6r1-kds-session-attribution"
CHANGE_ID = "attribute-kds-local-schema-sessions-a10r34p17r6r1"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
R5_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-schema-diagnostic-controller-a10r34p17r5.py"
R5_CONTROLLER_SHA256 = "7e2299ef2f057d43b6c66bad1e1b4fc7608cc2fb44ecef33ef23ade673d856f2"
EXPECTED_SESSION_COUNT = 2

SESSION_COUNT_SQL = (
    "SELECT count(*) FROM pg_stat_activity "
    "WHERE datname = current_database() AND backend_type = 'client backend' AND pid <> pg_backend_pid()"
)

SESSION_SQL = """
SELECT
  pid,
  CASE
    WHEN application_name = '' THEN 'unspecified'
    WHEN lower(application_name) LIKE '%kds%' THEN 'kds'
    WHEN lower(application_name) LIKE '%gbrain%' THEN 'gbrain'
    WHEN lower(application_name) LIKE '%brain%' THEN 'brain'
    WHEN lower(application_name) LIKE '%studio%' THEN 'studio'
    WHEN lower(application_name) LIKE '%mmc%' THEN 'mmc'
    WHEN lower(application_name) LIKE '%psql%' THEN 'psql'
    WHEN lower(application_name) LIKE '%psycopg%' THEN 'psycopg'
    ELSE 'other'
  END AS application_class,
  backend_type,
  COALESCE(state, 'unknown') AS state,
  COALESCE(wait_event_type, 'none') AS wait_event_type,
  COALESCE(wait_event, 'none') AS wait_event,
  CASE
    WHEN client_addr IS NULL THEN 'local_socket'
    WHEN client_addr = inet '127.0.0.1' THEN 'loopback_ipv4'
    WHEN client_addr = inet '::1' THEN 'loopback_ipv6'
    ELSE 'non_loopback'
  END AS client_location,
  COALESCE(client_port, -1) AS client_port
FROM pg_stat_activity
WHERE datname = current_database()
  AND backend_type = 'client backend'
  AND pid <> pg_backend_pid()
ORDER BY pid
LIMIT 2
""".strip()

# Filled after both R6 artifacts are present. Their content may change without changing Git status records.
SEALED_BASELINES = {
    "gpcf": {
        "head": "11d022b818332d2271a78b427c326eb454507a5a",
        "origin": "11d022b818332d2271a78b427c326eb454507a5a",
        "ordinary_count": 743,
        "ordinary_sha256": "498e897531c830e40df6ba5d4e55579f6dc776233ff93b09d986c2b976560c3e",
        "expanded_count": 760,
        "expanded_sha256": "a4e89ee4c0134769dce240cc7ced7baa444cebc3f91aa5cb8f1356294679fae5",
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


def load_r5() -> Any:
    if digest(R5_CONTROLLER.read_bytes()) != R5_CONTROLLER_SHA256:
        raise RuntimeError("r5_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r5_base", R5_CONTROLLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("r5_controller_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_base(r5: Any) -> Any:
    base = r5.load_base()
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
        "connection_count": 1,
        "transaction_mode": "repeatable_read_read_only",
        "fixture_created": False,
        "api_requests": 0,
        **extra,
    }


def safe_error_code(error: BaseException) -> str:
    return str(getattr(error, "sqlstate", None) or type(error).__name__)


def session_projection(row: tuple[Any, ...]) -> dict[str, Any]:
    pid, application_class, backend_type, state, wait_type, wait_event, location, port = row
    return {
        "pid": int(pid),
        "application_class": str(application_class),
        "backend_type": str(backend_type),
        "state": str(state),
        "wait_event_type": str(wait_type),
        "wait_event": str(wait_event),
        "client_location": str(location),
        "client_port": int(port),
    }


def attribute_sessions(dsn: str, base: Any) -> dict[str, Any]:
    connection: psycopg.Connection[Any] | None = None
    transaction_started = False
    rollback_confirmed = False
    close_confirmed = False
    status = "failed_no_change"
    code = "session_attribution_failed"
    extra: dict[str, Any] = {}
    try:
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
        except Exception as error:
            return terminal(
                "failed_no_change",
                "database_connection_failed",
                error_class=safe_error_code(error),
                rollback_confirmed=False,
                connection_close_confirmed=True,
            )

        connection.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        transaction_started = True
        database_name, transaction_read_only, xid_before = connection.execute(
            "SELECT current_database(), current_setting('transaction_read_only'), txid_current_if_assigned()"
        ).fetchone()
        if database_name != "gbrain" or transaction_read_only != "on":
            status = "stopped_no_change"
            code = "read_only_identity_mismatch"
        else:
            observed_count = int(connection.execute(SESSION_COUNT_SQL).fetchone()[0])
            xid_after = connection.execute("SELECT txid_current_if_assigned()").fetchone()[0]
            if observed_count != EXPECTED_SESSION_COUNT:
                status = "stopped_no_change"
                code = "session_count_drift"
                extra = {
                    "observed_session_count": observed_count,
                    "expected_session_count": EXPECTED_SESSION_COUNT,
                    "xid_before_is_null": xid_before is None,
                    "xid_after_is_null": xid_after is None,
                }
            else:
                rows = connection.execute(SESSION_SQL).fetchall()
                if len(rows) != EXPECTED_SESSION_COUNT:
                    raise RuntimeError("session_projection_count")
                sessions = [session_projection(tuple(row)) for row in rows]
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
    except Exception as error:
        status = "failed_no_change"
        code = "session_attribution_failed"
        extra = {"error_class": safe_error_code(error)}

    cleanup_errors: list[str] = []
    if connection is not None:
        if transaction_started:
            try:
                connection.execute("ROLLBACK")
                transaction_started = False
                rollback_confirmed = True
            except Exception as error:
                cleanup_errors.append(f"rollback:{safe_error_code(error)}")
        try:
            connection.close()
            close_confirmed = bool(getattr(connection, "closed", True))
            if not close_confirmed:
                cleanup_errors.append("close:not_confirmed")
        except Exception as error:
            cleanup_errors.append(f"close:{safe_error_code(error)}")

    if cleanup_errors:
        extra = {"prior_code": code, "cleanup_error_classes": cleanup_errors}
        status = "failed_fail_closed"
        code = "session_attribution_cleanup_unresolved"
    return terminal(
        status,
        code,
        rollback_confirmed=rollback_confirmed,
        connection_close_confirmed=close_confirmed,
        **extra,
    )


def preflight(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r5 = load_r5()
    base = load_base(r5)
    dsn, _ = base.hard_baseline()
    del dsn
    return {
        "status": "eligible_for_separate_read_only_session_attribution_authorization",
        "control": CONTROL_ID,
        "controller_sha256": sealed_sha,
        "database": "gbrain",
        "host": "loopback",
        "connection_count": 1,
        "transaction_count": 1,
        "transaction_mode": "repeatable_read_read_only",
        "expected_session_count": EXPECTED_SESSION_COUNT,
        "raw_application_name_output": False,
        "query_text_read": False,
        "api_requests": 0,
        "fixture_created": False,
    }


def lock_helper_action(action: str, sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    base = load_base(load_r5())
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

    def invoke(helper_action: str) -> tuple[str, int]:
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
            return "completed", result.returncode
        except subprocess.TimeoutExpired:
            return "timeout", -1
        except OSError:
            return "spawn_failed", -1

    outcome, returncode = invoke(action)
    if action == "acquire":
        if outcome == "completed" and returncode == 0 and base.owned_lock_state():
            return True, True, "acquired"
        failure = f"acquire_{outcome}" if outcome != "completed" else "acquire_failed"
        if base.partial_owned_state():
            cleanup_outcome, cleanup_returncode = invoke("cleanup")
            if (
                cleanup_outcome == "completed"
                and cleanup_returncode == 0
                and not base.OPSX_LOCK.exists()
                and not base.ATOMIC_GUARD.exists()
            ):
                return False, False, f"{failure}_recovered"
            return False, False, f"{failure}_lock_unresolved"
        if base.OPSX_LOCK.exists() or base.ATOMIC_GUARD.exists():
            return False, False, f"{failure}_lock_unresolved"
        return False, False, f"{failure}_no_lock"
    released = (
        outcome == "completed"
        and returncode == 0
        and not base.OPSX_LOCK.exists()
        and not base.ATOMIC_GUARD.exists()
    )
    return released, False, "released" if released else f"release_{outcome}_lock_unresolved"


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r5 = load_r5()
    base = load_base(r5)
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
            result = attribute_sessions(dsn, base)
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
            result.setdefault(
                "opsx_lock_released",
                not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists(),
            )
    return result


def self_test() -> dict[str, Any]:
    upper_sql = SESSION_SQL.upper()
    upper_count_sql = SESSION_COUNT_SQL.upper()
    assert "PG_STAT_ACTIVITY" in upper_sql
    assert "ORDER BY PID" in upper_sql
    assert "LIMIT 2" in upper_sql
    for forbidden in (" QUERY", "USENAME", "CLIENT_HOSTNAME", "INSERT ", "UPDATE ", "DELETE ", "CREATE ", "ALTER ", "DROP ", "COMMIT"):
        assert forbidden not in upper_sql
        assert forbidden not in upper_count_sql
    assert "application_name" in SESSION_SQL
    assert "application_class" in SESSION_SQL

    r5 = load_r5()
    base = load_base(r5)

    class FakeRows:
        def __init__(self, rows: list[tuple[Any, ...]]):
            self.rows = rows

        def fetchone(self) -> tuple[Any, ...]:
            return self.rows[0]

        def fetchall(self) -> list[tuple[Any, ...]]:
            return self.rows

    class FakeConnection:
        def __init__(self, *, rows: list[tuple[Any, ...]] | None = None, fail_rollback: bool = False, fail_close: bool = False):
            self.rows = rows or [
                (101, "kds", "client backend", "idle", "Client", "ClientRead", "loopback_ipv4", 52001),
                (102, "psycopg", "client backend", "idle", "Client", "ClientRead", "local_socket", -1),
            ]
            self.fail_rollback = fail_rollback
            self.fail_close = fail_close
            self.closed = False
            self.rolled_back = False
            self.executed_statements: list[str] = []

        def execute(self, statement: str) -> FakeRows:
            self.executed_statements.append(statement)
            if statement.startswith("BEGIN TRANSACTION"):
                return FakeRows([])
            if statement.startswith("SELECT current_database()"):
                return FakeRows([("gbrain", "on", None)])
            if statement == SESSION_COUNT_SQL:
                return FakeRows([(len(self.rows),)])
            if statement == SESSION_SQL:
                return FakeRows(self.rows)
            if statement == "SELECT txid_current_if_assigned()":
                return FakeRows([(None,)])
            if statement == "ROLLBACK":
                if self.fail_rollback:
                    raise RuntimeError("rollback")
                self.rolled_back = True
                return FakeRows([])
            raise AssertionError(statement)

        def close(self) -> None:
            if self.fail_close:
                raise RuntimeError("close")
            self.closed = True

    normal = FakeConnection()
    with mock.patch.object(psycopg, "connect", return_value=normal):
        normal_result = attribute_sessions("redacted", base)
    assert normal_result["status"] == "completed_read_only"
    assert normal_result["session_count"] == EXPECTED_SESSION_COUNT
    assert normal_result["sessions"][0]["application_class"] == "kds"
    assert normal_result["rollback_confirmed"] is True
    assert normal_result["connection_close_confirmed"] is True
    assert normal.rolled_back and normal.closed

    drift = FakeConnection(rows=[*normal.rows, (103, "other", "client backend", "idle", "Client", "ClientRead", "loopback_ipv4", 52003)])
    with mock.patch.object(psycopg, "connect", return_value=drift):
        drift_result = attribute_sessions("redacted", base)
    assert drift_result["status"] == "stopped_no_change"
    assert drift_result["code"] == "session_count_drift"
    assert "sessions" not in drift_result
    assert SESSION_SQL not in drift.executed_statements

    non_loopback_rows = list(normal.rows)
    non_loopback_rows[1] = (*non_loopback_rows[1][:-2], "non_loopback", 52002)
    non_loopback = FakeConnection(rows=non_loopback_rows)
    with mock.patch.object(psycopg, "connect", return_value=non_loopback):
        non_loopback_result = attribute_sessions("redacted", base)
    assert non_loopback_result["status"] == "stopped_no_change"
    assert non_loopback_result["code"] == "non_loopback_session_observed"
    assert "sessions" not in non_loopback_result

    rollback_failure = FakeConnection(fail_rollback=True)
    with mock.patch.object(psycopg, "connect", return_value=rollback_failure):
        rollback_result = attribute_sessions("redacted", base)
    assert rollback_result["status"] == "failed_fail_closed"
    assert rollback_result["code"] == "session_attribution_cleanup_unresolved"

    close_failure = FakeConnection(fail_close=True)
    with mock.patch.object(psycopg, "connect", return_value=close_failure):
        close_result = attribute_sessions("redacted", base)
    assert close_result["status"] == "failed_fail_closed"
    assert close_result["code"] == "session_attribution_cleanup_unresolved"

    completed = subprocess.CompletedProcess(args=(), returncode=1, stdout=b"", stderr=b"")
    with mock.patch.object(subprocess, "run", return_value=completed) as run_mock:
        acquired, owned, lock_code = run_lock_helper(base, "acquire", "sealed")
    assert not acquired and not owned and lock_code == "acquire_failed_no_lock"
    assert run_mock.call_args.kwargs["timeout"] == base.LOCK_HELPER_TIMEOUT_SECONDS
    return {
        "status": "pass",
        "control": CONTROL_ID,
        "expected_session_count": EXPECTED_SESSION_COUNT,
        "single_connection": True,
        "single_read_only_transaction": True,
        "raw_application_name_output": False,
        "query_text_read": False,
        "session_count_drift_fail_closed": True,
        "non_loopback_fail_closed": True,
        "mandatory_rollback": True,
        "rollback_failure_fail_closed": True,
        "close_failure_fail_closed": True,
        "bounded_lock_helper": True,
        "api_requests": 0,
        "fixture_created": False,
    }


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
        result = terminal("stopped_no_change", safe_error_code(error), connection_count=0)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    success = {
        "pass",
        "eligible_for_separate_read_only_session_attribution_authorization",
        "completed_read_only",
    }
    return 0 if result["status"] in success else 3


if __name__ == "__main__":
    raise SystemExit(main())
