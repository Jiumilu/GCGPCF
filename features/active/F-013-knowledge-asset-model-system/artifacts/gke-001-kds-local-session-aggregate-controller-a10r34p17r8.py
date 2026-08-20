#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any
from unittest import mock

import psycopg


CONTROL_ID = "GKE-001-COORDINATION-20260820-002-A10R34P17R8"
RUN_ID = "gke001-a10r34p17r8-kds-session-aggregate"
CHANGE_ID = "classify-kds-local-session-ownership-a10r34p17r8"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
R5_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-schema-diagnostic-controller-a10r34p17r5.py"
R5_CONTROLLER_SHA256 = "7e2299ef2f057d43b6c66bad1e1b4fc7608cc2fb44ecef33ef23ade673d856f2"

# This query deliberately emits only closed categories and their counts. It never
# selects identifiers, credentials, query text, raw application names, or addresses.
SESSION_AGGREGATE_SQL = """
SELECT
  CASE
    WHEN application_name = '' THEN 'unspecified'
    WHEN lower(application_name) LIKE '%kds%' THEN 'kds'
    WHEN lower(application_name) LIKE '%gbrain%' THEN 'gbrain'
    WHEN lower(application_name) LIKE '%brain%' THEN 'brain'
    WHEN lower(application_name) LIKE '%studio%' THEN 'studio'
    WHEN lower(application_name) LIKE '%mmc%' THEN 'mmc'
    WHEN lower(application_name) LIKE '%psql%' THEN 'psql'
    WHEN lower(application_name) LIKE '%psycopg%' THEN 'psycopg'
    ELSE 'unclassified'
  END AS application_class,
  CASE
    WHEN client_addr IS NULL THEN 'local_socket'
    WHEN client_addr = inet '127.0.0.1' THEN 'loopback_ipv4'
    WHEN client_addr = inet '::1' THEN 'loopback_ipv6'
    ELSE 'non_loopback'
  END AS client_location,
  CASE
    WHEN state IN ('active', 'idle', 'idle in transaction', 'idle in transaction (aborted)') THEN state
    ELSE 'other'
  END AS state_class,
  count(*)::bigint AS session_count
FROM pg_stat_activity
WHERE datname = current_database()
  AND backend_type = 'client backend'
  AND pid <> pg_backend_pid()
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3
""".strip()

SEALED_BASELINES = {
    "gpcf": {
        "head": "a317eeaab451920bc4bbbea904ca1c2bc774a497",
        "origin": "8deda915579b915d7496f20b2e4ecb5475491c40",
        "ordinary_count": 9,
        "ordinary_sha256": "2d391e7e4498d64b094a654adba48264d59369f62f14ebcbf1ac49a7b58125da",
        "expanded_count": 9,
        "expanded_sha256": "2d391e7e4498d64b094a654adba48264d59369f62f14ebcbf1ac49a7b58125da",
    },
    "kds": {
        "head": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "ordinary_count": 373,
        "ordinary_sha256": "4677fcccdf92696d134e276bc19692403f57f5151c3026670950b8f2ded7760b",
        "expanded_count": 703,
        "expanded_sha256": "5a7325cd54c9eed1c89fcc9e5540065b68cc61ed7c2399fdddbe761534b46f77",
    },
    "mmc": {
        "head": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7",
        "origin": "2dd7954fa4826120d68d42bd8f3c30e8d9ead99b",
        "ordinary_count": 0,
        "ordinary_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "expanded_count": 0,
        "expanded_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
        "transaction_count": 1,
        "transaction_mode": "repeatable_read_read_only",
        "fixture_created": False,
        "api_requests": 0,
        **extra,
    }


def safe_error_code(error: BaseException) -> str:
    return str(getattr(error, "sqlstate", None) or type(error).__name__)


def safe_groups(rows: list[tuple[Any, ...]]) -> tuple[list[dict[str, Any]], bool]:
    groups: list[dict[str, Any]] = []
    accepted = True
    for application_class, location, state, count in rows:
        app = str(application_class)
        client_location = str(location)
        if app == "unclassified" or client_location == "non_loopback":
            accepted = False
        groups.append(
            {
                "application_class": app,
                "client_location": client_location,
                "state_class": str(state),
                "session_count": int(count),
            }
        )
    return groups, accepted


def aggregate_sessions(dsn: str, base: Any) -> dict[str, Any]:
    connection: psycopg.Connection[Any] | None = None
    transaction_started = False
    rollback_confirmed = False
    close_confirmed = False
    status = "failed_no_change"
    code = "session_aggregate_failed"
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
            return terminal("failed_no_change", "database_connection_failed", error_class=safe_error_code(error), rollback_confirmed=False, connection_close_confirmed=True)

        connection.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        transaction_started = True
        database_name, transaction_read_only, xid_before = connection.execute(
            "SELECT current_database(), current_setting('transaction_read_only'), txid_current_if_assigned()"
        ).fetchone()
        if database_name != "gbrain" or transaction_read_only != "on":
            status = "stopped_no_change"
            code = "read_only_identity_mismatch"
        else:
            groups, accepted = safe_groups([tuple(row) for row in connection.execute(SESSION_AGGREGATE_SQL).fetchall()])
            xid_after = connection.execute("SELECT txid_current_if_assigned()").fetchone()[0]
            if not accepted:
                status = "stopped_no_change"
                code = "session_ownership_unclassified"
                extra = {
                    "aggregate_group_count": len(groups),
                    "xid_before_is_null": xid_before is None,
                    "xid_after_is_null": xid_after is None,
                }
            else:
                status = "completed_read_only"
                code = "session_ownership_aggregate_complete"
                extra = {
                    "aggregate_groups": groups,
                    "xid_before_is_null": xid_before is None,
                    "xid_after_is_null": xid_after is None,
                }
    except Exception as error:
        status = "failed_no_change"
        code = "session_aggregate_failed"
        extra = {"error_class": safe_error_code(error)}

    cleanup_errors: list[str] = []
    if connection is not None:
        if transaction_started:
            try:
                connection.execute("ROLLBACK")
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
        status = "failed_fail_closed"
        code = "session_aggregate_cleanup_unresolved"
        extra = {"cleanup_error_classes": cleanup_errors}
    return terminal(status, code, rollback_confirmed=rollback_confirmed, connection_close_confirmed=close_confirmed, **extra)


def preflight(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r5 = load_r5()
    base = load_base(r5)
    dsn, _ = base.hard_baseline()
    del dsn
    return {
        "status": "eligible_for_separate_aggregate_read_only_authorization",
        "control": CONTROL_ID,
        "controller_sha256": sealed_sha,
        "aggregate_only": True,
        "raw_application_name_output": False,
        "raw_network_address_output": False,
        "pid_output": False,
        "query_text_read": False,
        "api_requests": 0,
    }


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r5 = load_r5()
    base = load_base(r5)
    acquired = False
    result: dict[str, Any] = terminal("stopped_no_change", "not_started")
    try:
        _, _ = base.hard_baseline()
        acquired_result = base.lock_helper_acquire()
        if not acquired_result.get("acquired"):
            result = terminal("stopped_no_change", "lock_not_acquired")
        else:
            acquired = True
            dsn, _ = base.hard_baseline(own_lock_expected=True)
            result = aggregate_sessions(dsn, base)
    except base.ControlledFailure as error:
        result = terminal("stopped_no_change", error.code, step=error.step)
    finally:
        if acquired:
            released = base.lock_helper_release()
            result["opsx_lock_released"] = bool(released.get("released"))
            if not result["opsx_lock_released"]:
                result["status"] = "failed_fail_closed"
                result["code"] = "lock_release_unresolved"
        else:
            result["opsx_lock_released"] = not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists()
    return result


def self_test() -> dict[str, Any]:
    upper_sql = SESSION_AGGREGATE_SQL.upper()
    assert "PG_STAT_ACTIVITY" in upper_sql and "GROUP BY" in upper_sql
    for forbidden in ("SELECT PID", "USENAME", "QUERY", "CLIENT_HOSTNAME", "CLIENT_PORT", "INSERT ", "UPDATE ", "DELETE ", "CREATE ", "ALTER ", "DROP ", "COMMIT"):
        assert forbidden not in upper_sql
    assert "APPLICATION_NAME" in upper_sql and "CLIENT_ADDR" in upper_sql

    r5 = load_r5()
    base = load_base(r5)

    class FakeRows:
        def __init__(self, rows: list[tuple[Any, ...]]): self.rows = rows
        def fetchone(self) -> tuple[Any, ...]: return self.rows[0]
        def fetchall(self) -> list[tuple[Any, ...]]: return self.rows

    class FakeConnection:
        def __init__(self, rows: list[tuple[Any, ...]], fail_cleanup: bool = False, fail_close: bool = False):
            self.rows, self.fail_cleanup, self.fail_close, self.closed, self.rolled_back = rows, fail_cleanup, fail_close, False, False
        def execute(self, statement: str) -> FakeRows:
            if statement.startswith("BEGIN TRANSACTION") or statement == "ROLLBACK":
                if statement == "ROLLBACK":
                    if self.fail_cleanup: raise RuntimeError("rollback")
                    self.rolled_back = True
                return FakeRows([])
            if statement.startswith("SELECT current_database()"): return FakeRows([("gbrain", "on", None)])
            if statement == SESSION_AGGREGATE_SQL: return FakeRows(self.rows)
            if statement == "SELECT txid_current_if_assigned()": return FakeRows([(None,)])
            raise AssertionError(statement)
        def close(self) -> None:
            if self.fail_close:
                raise RuntimeError("close")
            self.closed = True

    normal = FakeConnection([("kds", "loopback_ipv4", "idle", 1), ("psycopg", "local_socket", "active", 1)])
    with mock.patch.object(psycopg, "connect", return_value=normal):
        normal_result = aggregate_sessions("redacted", base)
    assert normal_result["status"] == "completed_read_only"
    assert normal_result["aggregate_groups"][0]["application_class"] == "kds"
    assert normal.rolled_back and normal.closed

    rejected = FakeConnection([("unclassified", "loopback_ipv4", "idle", 13)])
    with mock.patch.object(psycopg, "connect", return_value=rejected):
        rejected_result = aggregate_sessions("redacted", base)
    assert rejected_result["status"] == "stopped_no_change"
    assert rejected_result["code"] == "session_ownership_unclassified"
    assert "aggregate_groups" not in rejected_result

    non_loopback = FakeConnection([("kds", "non_loopback", "idle", 1)])
    with mock.patch.object(psycopg, "connect", return_value=non_loopback):
        non_loopback_result = aggregate_sessions("redacted", base)
    assert non_loopback_result["status"] == "stopped_no_change"
    assert non_loopback_result["code"] == "session_ownership_unclassified"
    assert "aggregate_groups" not in non_loopback_result

    cleanup_failure = FakeConnection([("kds", "loopback_ipv4", "idle", 1)], fail_cleanup=True)
    with mock.patch.object(psycopg, "connect", return_value=cleanup_failure):
        cleanup_result = aggregate_sessions("redacted", base)
    assert cleanup_result["status"] == "failed_fail_closed"

    close_failure = FakeConnection([("kds", "loopback_ipv4", "idle", 1)], fail_close=True)
    with mock.patch.object(psycopg, "connect", return_value=close_failure):
        close_result = aggregate_sessions("redacted", base)
    assert close_result["status"] == "failed_fail_closed"
    return {"status": "pass", "control": CONTROL_ID, "aggregate_only": True, "single_connection": True, "single_read_only_transaction": True, "unclassified_fail_closed": True, "non_loopback_fail_closed": True, "mandatory_rollback": True, "close_failure_fail_closed": True, "api_requests": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--sealed-sha", default="")
    arguments = parser.parse_args()
    try:
        result = self_test() if arguments.self_test else preflight(arguments.sealed_sha) if arguments.preflight else execute(arguments.sealed_sha)
    except Exception as error:
        result = terminal("stopped_no_change", safe_error_code(error), connection_count=0)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] in {"pass", "eligible_for_separate_aggregate_read_only_authorization", "completed_read_only"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
