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


CONTROL_ID = "GKE-001-COORDINATION-20260817-052-A10R34P17R5R1"
RUN_ID = "gke001-a10r34p17r5r1-kds-schema-diagnostic"
CHANGE_ID = "diagnose-kds-local-schema-stop-a10r34p17r5r1"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
BASE_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-schema-migration-controller-a10r34p17r4.py"
BASE_CONTROLLER_SHA256 = "756d7d88e3959cd1b8eea1d0f62c7f8e9bc682a817c414c18c418867e38c4d51"
NEW_EXTERNAL_FILE = (
    "_governance/sync-runs/macmini-workwiki-20260817-064211/remote-identity.txt",
    "04b9ee8d7ce159e1b00cda33283633c5281323b484acea470855a181a88227de",
)
SEALED_EXTERNAL_MANIFEST_SHA256 = "13cdc6cb4348d1700311084b680caac89fd82d47830526744717b643b45733ec"

RELATIONS = (
    "schema_versions",
    "knowledge_objects",
    "knowledge_assets",
    "knowledge_asset_versions",
    "upload_intents",
    "knowledge_intake_jobs",
    "job_attempts",
    "audit_events",
    "outbox_events",
    "extraction_runs",
    "extracted_contents",
    "extracted_table_cells",
    "evidence_links",
    "extraction_active_selections",
)

RELATION_SQL = (
    "SELECT relation_name, to_regclass('knowledge_intake.' || relation_name)::text "
    "FROM (VALUES "
    + ",".join(f"('{name}',{ordinal})" for ordinal, name in enumerate(RELATIONS, start=1))
    + ") AS sealed(relation_name, ordinal) ORDER BY ordinal"
)
SESSION_SQL = (
    "SELECT count(*) FROM pg_stat_activity "
    "WHERE datname = current_database() AND backend_type = 'client backend' AND pid <> pg_backend_pid()"
)

# Filled from the post-artifact Git status. Untracked-file content edits do not alter these status records.
SEALED_BASELINES = {
    "gpcf": {
        "head": "11d022b818332d2271a78b427c326eb454507a5a",
        "origin": "11d022b818332d2271a78b427c326eb454507a5a",
        "ordinary_count": 741,
        "ordinary_sha256": "0df976d5b7ada5c40e4046ecd0af99c057ce6915477b9e85ba0abceed693f7e0",
        "expanded_count": 758,
        "expanded_sha256": "715b56d816b392270d80b53a8c82638c1936620413f22313aa6a616c452d9bd5",
    },
    "kds": {
        "head": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "ordinary_count": 278,
        "ordinary_sha256": "c4fd8c5602363bde8328e05301b9a38085b7bc22418fca55e4975deb8a5761b7",
        "expanded_count": 568,
        "expanded_sha256": "5c2b90cb8ec51975795a524bcd55c72fe81e9110671ceb75d709d7948c7040b3",
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


def load_base() -> Any:
    if digest(BASE_CONTROLLER.read_bytes()) != BASE_CONTROLLER_SHA256:
        raise RuntimeError("base_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r4r1_base", BASE_CONTROLLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("base_controller_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.CONTROL_ID = CONTROL_ID
    module.RUN_ID = RUN_ID
    module.CHANGE_ID = CHANGE_ID
    module.SEALED_EXTERNAL_FILES = tuple(module.SEALED_EXTERNAL_FILES) + (NEW_EXTERNAL_FILE,)
    module.SEALED_EXTERNAL_MANIFEST_SHA256 = SEALED_EXTERNAL_MANIFEST_SHA256
    module.BASELINES = tuple(
        module.RepoBaseline(
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
    return module


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


def diagnose(dsn: str, base: Any) -> dict[str, Any]:
    connection: psycopg.Connection[Any] | None = None
    transaction_started = False
    rollback_confirmed = False
    close_confirmed = False
    status = "failed_no_change"
    code = "diagnostic_failed"
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
            relation_rows = connection.execute(RELATION_SQL).fetchall()
            if [row[0] for row in relation_rows] != list(RELATIONS):
                status = "stopped_no_change"
                code = "relation_projection_mismatch"
            else:
                relation_presence = {name: qualified is not None for name, qualified in relation_rows}
                other_client_sessions = int(connection.execute(SESSION_SQL).fetchone()[0])
                xid_after = connection.execute("SELECT txid_current_if_assigned()").fetchone()[0]
                status = "completed_read_only"
                code = "diagnostic_complete"
                extra = {
                    "relation_presence": relation_presence,
                    "xid_before_is_null": xid_before is None,
                    "xid_after_is_null": xid_after is None,
                    "other_client_sessions": other_client_sessions,
                }
    except Exception as error:
        status = "failed_no_change"
        code = "diagnostic_failed"
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
        extra = {
            "prior_code": code,
            "cleanup_error_classes": cleanup_errors,
        }
        status = "failed_fail_closed"
        code = "diagnostic_cleanup_unresolved"
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
    base = load_base()
    dsn, _ = base.hard_baseline()
    del dsn
    return {
        "status": "eligible_for_separate_read_only_diagnostic_authorization",
        "control": CONTROL_ID,
        "controller_sha256": sealed_sha,
        "database": "gbrain",
        "host": "loopback",
        "connection_count": 1,
        "transaction_count": 1,
        "transaction_mode": "repeatable_read_read_only",
        "relation_count": len(RELATIONS),
        "api_requests": 0,
        "fixture_created": False,
    }


def lock_helper_action(action: str, sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    base = load_base()
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
    base = load_base()
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
            result = diagnose(dsn, base)
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
    assert len(RELATIONS) == 14
    assert len(set(RELATIONS)) == 14
    assert "ORDER BY ordinal" in RELATION_SQL
    assert "pg_stat_activity" in SESSION_SQL
    forbidden = ("INSERT ", "UPDATE ", "DELETE ", "CREATE ", "ALTER ", "DROP ", "COMMIT")
    for statement in (RELATION_SQL, SESSION_SQL):
        assert not any(token in statement.upper() for token in forbidden)
    base = load_base()
    assert tuple(base.RELATIONS) == RELATIONS

    class FakeRows:
        def __init__(self, rows: list[tuple[Any, ...]]):
            self.rows = rows

        def fetchone(self) -> tuple[Any, ...]:
            return self.rows[0]

        def fetchall(self) -> list[tuple[Any, ...]]:
            return self.rows

    class FakeConnection:
        def __init__(self, *, fail_rollback: bool = False, fail_close: bool = False):
            self.fail_rollback = fail_rollback
            self.fail_close = fail_close
            self.closed = False
            self.rolled_back = False

        def execute(self, statement: str) -> FakeRows:
            if statement.startswith("BEGIN TRANSACTION"):
                return FakeRows([])
            if statement.startswith("SELECT current_database()"):
                return FakeRows([("gbrain", "on", None)])
            if statement == RELATION_SQL:
                return FakeRows([(name, None) for name in RELATIONS])
            if statement == SESSION_SQL:
                return FakeRows([(0,)])
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
        normal_result = diagnose("redacted", base)
    assert normal_result["status"] == "completed_read_only"
    assert normal_result["rollback_confirmed"] is True
    assert normal_result["connection_close_confirmed"] is True
    assert normal.rolled_back and normal.closed

    rollback_failure = FakeConnection(fail_rollback=True)
    with mock.patch.object(psycopg, "connect", return_value=rollback_failure):
        rollback_result = diagnose("redacted", base)
    assert rollback_result["status"] == "failed_fail_closed"
    assert rollback_result["code"] == "diagnostic_cleanup_unresolved"

    close_failure = FakeConnection(fail_close=True)
    with mock.patch.object(psycopg, "connect", return_value=close_failure):
        close_result = diagnose("redacted", base)
    assert close_result["status"] == "failed_fail_closed"
    assert close_result["code"] == "diagnostic_cleanup_unresolved"

    completed = subprocess.CompletedProcess(args=(), returncode=1, stdout=b"", stderr=b"")
    with mock.patch.object(subprocess, "run", return_value=completed) as run_mock:
        acquired, owned, lock_code = run_lock_helper(base, "acquire", "sealed")
    assert not acquired and not owned and lock_code == "acquire_failed_no_lock"
    assert run_mock.call_args.kwargs["timeout"] == base.LOCK_HELPER_TIMEOUT_SECONDS
    return {
        "status": "pass",
        "control": CONTROL_ID,
        "relations": len(RELATIONS),
        "single_connection": True,
        "single_read_only_transaction": True,
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
    return 0 if result["status"] in {"pass", "success", "eligible_for_separate_read_only_diagnostic_authorization", "completed_read_only"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
