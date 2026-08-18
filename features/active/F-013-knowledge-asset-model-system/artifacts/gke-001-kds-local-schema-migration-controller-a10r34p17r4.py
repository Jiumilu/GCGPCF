#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import shlex
import socket
import stat
import subprocess
import sys
import tempfile
import urllib.parse
from unittest import mock
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import psycopg


CONTROL_ID = "GKE-001-COORDINATION-20260817-050-A10R34P17R4R1"
RUN_ID = "gke001-a10r34p17r4r1-kds-local-schema-migration"
CHANGE_ID = "migrate-kds-local-release0-schema-a10r34p17r4r1"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
KDS_ENV = Path("/Users/lujunxiang/.globalcloud/kds.env")
OPSX_LOCK = GPCF_ROOT / ".harness/opsx.lock"
ATOMIC_GUARD = GPCF_ROOT / ".harness/opsx.atomic-guard"
GUARD_OWNER = ATOMIC_GUARD / "owner"
LOCK_HELPER_TIMEOUT_SECONDS = 5
DATABASE_CONNECT_TIMEOUT_SECONDS = 5
DATABASE_LOCK_TIMEOUT_MILLISECONDS = 5000
DATABASE_STATEMENT_TIMEOUT_MILLISECONDS = 30000
DATABASE_IDLE_TRANSACTION_TIMEOUT_MILLISECONDS = 30000
SEALED_OFFICIAL_LOCK_HELPERS = {
    "acquire": "d0678fc5f261b1bf9363e945dc96a478c4b5e0483acffacc0854ed0a28ce1fe6",
    "release": "4310529f86ec4e0e899c986751a531454e6a1c751253dd7d34bf4e9d747a4191",
}
OFFICIAL_LOCK_HELPERS = {
    "acquire": Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/acquire-lock.sh"),
    "release": Path("/Users/lujunxiang/.codex/skills/opsx-full-cycle/scripts/release-lock.sh"),
}

MIGRATIONS = (
    (
        KDS_ROOT / "knowledge_intake/sql/001_knowledge_intake.sql",
        "539b19dd563812aae6ac2c047f98c49a8c2bf55eb80bced8fa6b41b9d138c77c",
    ),
    (
        KDS_ROOT / "knowledge_intake/sql/002_document_extraction.sql",
        "f4673975ae385680571cb2db9f81bf80a6e9ad6731988f7e41b774ea6b2ad2d5",
    ),
)

SEALED_EXTERNAL_FILES = (
    ("工业绿链/reports/Hermes质量周报.md", "241016b0cca22b64c1cb69cf51902a6695d739712a9901b45a5df58c86508e4c"),
    ("工业绿链/reports/项目复盘知识归档报告.md", "b062727cd3bc294e2e0ad11b75c44eab94a1e07003446afd632fc2abe5fd36a0"),
    ("工业绿链/reports/项目监控仪表盘.md", "977848b6fed3e953a31d6e065e27f70ae809f4cae231ef3881ac2755e460868b"),
    ("工业绿链/体系/W01-W20第二阶段任务清单.md", "08040c809ced18708e349a626cb295840f3369192125cc287f49b36f21f63812"),
    ("工业绿链/体系/W01-W20覆盖率报告.md", "8b5931029aee668b70ed2efc95706069021593c23ac6c82f585de1008d91f69a"),
    ("工业绿链/体系/meeting-quality-gate_2026-08-16.json", "900fafe508c27804d531077afba34f132b667ed5edff024b2eec591687521391"),
    ("工业绿链/体系/会议质量门禁阻断清单_2026-08-16.md", "8f5c47d808f9d72e5bfeb8d4e4c2c44057060ce969cdb5711d025870f0344ec2"),
    ("工业绿链/体系/老卢工作体系健康检查_2026-08-16.md", "2a9dc8a937436696f1de7a8c0b53b65a78bd223ebac547bab0167b1eca4036fa"),
    ("工业绿链/变更告警_2026-08-16.md", "e7127e492342d34ebacd5686bfe5b7d089db9c60bf1d9d10e1a226e2ac557b3a"),
    ("工业绿链/周报/周报_2026W33.md", "40aa36b89767043f9482f7c081518fd26d1a629d514993326b09d49fdcd28409"),
    ("工业绿链/日报/晨报-2026-08-16.md", "17878591de8bf528d422fbeb49bc59129f2d75661c908d3d3fe1df2187d3b63e"),
    ("工业绿链/月报/月报_2026-08.md", "df7ed71bc783111da72f2c84f8da6923f841ec1965d0f8122b22db08fe47daff"),
)
SEALED_EXTERNAL_MANIFEST_SHA256 = "bd054bbee318a385c00fa723022eca6c299ae563073ce167c36ea683d916b3db"

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

BUSINESS_TABLES = tuple(name for name in RELATIONS if name != "schema_versions")


@dataclass(frozen=True)
class RepoBaseline:
    root: Path
    head: str
    origin: str
    ordinary_count: int
    ordinary_sha256: str
    expanded_count: int
    expanded_sha256: str


BASELINES = (
    RepoBaseline(
        GPCF_ROOT,
        "11d022b818332d2271a78b427c326eb454507a5a",
        "11d022b818332d2271a78b427c326eb454507a5a",
        739,
        "b0920d526ec802b0f78c5542b83b50b4f64ee79c6c40f049ea22de3f950bdb64",
        756,
        "f2dc7d9b8219096f1c3809a925140d4669b322b175d0069525242f4b065b891b",
    ),
    RepoBaseline(
        KDS_ROOT,
        "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "2ac85c55163b7acf0ede699184ac360579ccefaa",
        277,
        "449b5bb746c6584a49d103c576841e502671ec3b59d6320b4f6f978583195f8e",
        567,
        "a20dcf7dfcadf972725364227d71269a48d0c2acb6517e5f26628015ec53ad99",
    ),
    RepoBaseline(
        MMC_ROOT,
        "c93463ff5ee40ce66d8e1a09995ca8c66a24c86d",
        "c93463ff5ee40ce66d8e1a09995ca8c66a24c86d",
        10,
        "300ef303a5a647e54931171ff5ebf309192671fbf9f52f027acedf40d7ab8ad9",
        98,
        "2fd6e7fe5409ed79e410ea20e722a84eecb1d141d969153b27c969b3ebf6a451",
    ),
)


class ControlledFailure(RuntimeError):
    def __init__(self, step: str, code: str):
        super().__init__(code)
        self.step = step
        self.code = code


def fail(step: str, code: str) -> None:
    raise ControlledFailure(step, code)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: Iterable[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        tuple(command),
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def normalized_status(data: bytes, allow_own_lock: bool) -> bytes:
    if not allow_own_lock:
        return data
    records = [record for record in data.split(b"\0") if record]
    own_records = {
        b"?? .harness/opsx.lock",
        b"?? .harness/opsx.atomic-guard/",
        b"?? .harness/opsx.atomic-guard/owner",
    }
    records = [record for record in records if record not in own_records]
    return b"".join(record + b"\0" for record in records)


def git_status(root: Path, expanded: bool, *, allow_own_lock: bool = False) -> tuple[int, str]:
    command = ["/usr/bin/git", "status", "--porcelain=v1", "-z"]
    if expanded:
        command.append("--untracked-files=all")
    data = normalized_status(run(command, cwd=root).stdout, allow_own_lock)
    return sum(bool(item) for item in data.split(b"\0")), digest(data)


def attest_directory(path: Path, expected_mode: int) -> os.stat_result:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        fail("lock", "directory_open_failed")
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISDIR(metadata.st_mode)
            or stat.S_IMODE(metadata.st_mode) != expected_mode
            or metadata.st_uid != os.getuid()
        ):
            fail("lock", "directory_metadata")
        path_metadata = os.lstat(path)
        if path_metadata.st_dev != metadata.st_dev or path_metadata.st_ino != metadata.st_ino:
            fail("lock", "directory_replaced")
        return metadata
    finally:
        os.close(descriptor)


def attest_identity_file(
    path: Path,
    expected_content: bytes | None,
    *,
    expected_mode: int = 0o400,
    immutable: bool | None = None,
) -> tuple[os.stat_result, bytes]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        fail("lock", "identity_open_failed")
    try:
        metadata = os.fstat(descriptor)
        immutable_set = bool(metadata.st_flags & stat.UF_IMMUTABLE)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or stat.S_IMODE(metadata.st_mode) != expected_mode
            or metadata.st_uid != os.getuid()
            or metadata.st_nlink != 1
            or (immutable is not None and immutable_set != immutable)
            or metadata.st_size > 1024
        ):
            fail("lock", "identity_metadata")
        chunks: list[bytes] = []
        remaining = metadata.st_size + 1
        while remaining:
            chunk = os.read(descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        content = b"".join(chunks)
        if expected_content is not None and content != expected_content:
            fail("lock", "identity_content")
        path_metadata = os.lstat(path)
        if (
            path_metadata.st_dev != metadata.st_dev
            or path_metadata.st_ino != metadata.st_ino
            or path_metadata.st_uid != metadata.st_uid
            or path_metadata.st_nlink != metadata.st_nlink
            or stat.S_IMODE(path_metadata.st_mode) != expected_mode
        ):
            fail("lock", "identity_replaced")
        return metadata, content
    finally:
        os.close(descriptor)


def lock_payload() -> bytes:
    return (
        f"run_id: {RUN_ID}\n"
        f"change_id: {CHANGE_ID}\n"
        "branch: main\n"
        f"locked_at: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        "ttl_hours: 4\n"
        f"control_id: {CONTROL_ID}\n"
    ).encode("utf-8")


def validate_lock_payload(content: bytes) -> None:
    try:
        values = dict(line.split(": ", 1) for line in content.decode("utf-8", "strict").splitlines())
        datetime.strptime(values["locked_at"], "%Y-%m-%dT%H:%M:%SZ")
    except (KeyError, ValueError, UnicodeError):
        fail("lock", "identity_content")
    if values != {
        "run_id": RUN_ID,
        "change_id": CHANGE_ID,
        "branch": "main",
        "locked_at": values["locked_at"],
        "ttl_hours": "4",
        "control_id": CONTROL_ID,
    }:
        fail("lock", "identity_content")


def check_own_lock() -> None:
    attest_directory(ATOMIC_GUARD, 0o700)
    _, owner_content = attest_identity_file(GUARD_OWNER, None, immutable=False)
    validate_lock_payload(owner_content)
    metadata, _ = attest_identity_file(OPSX_LOCK, owner_content, immutable=True)
    if (
        not (metadata.st_flags & stat.UF_IMMUTABLE)
        or OPSX_LOCK.is_symlink()
        or GUARD_OWNER.is_symlink()
    ):
        fail("lock", "own_lock_type")


def check_repo(baseline: RepoBaseline, *, own_lock_expected: bool = False) -> None:
    if run(("/usr/bin/git", "branch", "--show-current"), cwd=baseline.root).stdout.strip() != b"main":
        fail("baseline", f"{baseline.root.name}_branch")
    if run(("/usr/bin/git", "rev-parse", "HEAD"), cwd=baseline.root).stdout.decode().strip() != baseline.head:
        fail("baseline", f"{baseline.root.name}_head")
    if run(("/usr/bin/git", "rev-parse", "origin/main"), cwd=baseline.root).stdout.decode().strip() != baseline.origin:
        fail("baseline", f"{baseline.root.name}_origin")
    divergence = run(("/usr/bin/git", "rev-list", "--left-right", "--count", "HEAD...origin/main"), cwd=baseline.root).stdout.split()
    if divergence != [b"0", b"0"]:
        fail("baseline", f"{baseline.root.name}_divergence")
    if run(("/usr/bin/git", "diff", "--cached", "--name-only"), cwd=baseline.root).stdout:
        fail("baseline", f"{baseline.root.name}_staged")
    allow_own_lock = own_lock_expected and baseline.root == GPCF_ROOT
    if git_status(baseline.root, False, allow_own_lock=allow_own_lock) != (baseline.ordinary_count, baseline.ordinary_sha256):
        fail("baseline", f"{baseline.root.name}_ordinary_dirty")
    if git_status(baseline.root, True, allow_own_lock=allow_own_lock) != (baseline.expanded_count, baseline.expanded_sha256):
        fail("baseline", f"{baseline.root.name}_expanded_dirty")
    lock_exists = (baseline.root / ".harness/opsx.lock").exists()
    if allow_own_lock:
        check_own_lock()
    elif lock_exists:
        fail("baseline", f"{baseline.root.name}_opsx_lock")
    if baseline.root == KDS_ROOT:
        records = bytearray()
        for relative_path, expected_sha256 in SEALED_EXTERNAL_FILES:
            path = KDS_ROOT / relative_path
            metadata = path.lstat()
            if not stat.S_ISREG(metadata.st_mode) or path.is_symlink():
                fail("baseline", "sealed_external_file_type")
            actual_sha256 = digest(path.read_bytes())
            if actual_sha256 != expected_sha256:
                fail("baseline", "sealed_external_file_content")
            records.extend(f"{actual_sha256}  {relative_path}\n".encode("utf-8"))
        if digest(bytes(records)) != SEALED_EXTERNAL_MANIFEST_SHA256:
            fail("baseline", "sealed_external_content_manifest")


def validate_runtime() -> None:
    ps = run(("/bin/ps", "-p", "90660", "-o", "pid=,ppid=,command=")).stdout.decode()
    if "90660" not in ps or " 1 " not in f" {ps} " or "api_server.py --host 127.0.0.1 --port 18080 --data-dir concepts" not in ps:
        fail("runtime", "pid_identity")
    owners = [
        line
        for line in run(("/usr/sbin/lsof", "-nP", "-iTCP:18080", "-sTCP:LISTEN", "-Fp")).stdout.decode().splitlines()
        if line.startswith("p")
    ]
    if owners != ["p90660"]:
        fail("runtime", "listener_18080")
    shadow = subprocess.run(
        ("/usr/sbin/lsof", "-nP", "-iTCP:18081", "-sTCP:LISTEN", "-Fp"),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if shadow.stdout:
        fail("runtime", "listener_18081")
    established = subprocess.run(
        ("/usr/sbin/lsof", "-a", "-p", "90660", "-iTCP:5432", "-sTCP:ESTABLISHED", "-Fp"),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if established.stdout:
        fail("runtime", "database_connection_present")
    launch = run(("/bin/launchctl", "print", f"gui/{os.getuid()}/com.globalcloud.kds-api-18080")).stdout.decode()
    for expected in ("state = running", "runs = 1", "pid = 90660"):
        if expected not in launch:
            fail("runtime", "launchagent_identity")


def secure_read(path: Path, expected_size: int) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        fail("environment", "open_failed")
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o600:
            fail("environment", "mode_or_type")
        if metadata.st_uid != os.getuid() or metadata.st_size != expected_size or metadata.st_nlink != 1:
            fail("environment", "owner_size_or_link_count")
        chunks: list[bytes] = []
        remaining = metadata.st_size + 1
        while remaining:
            chunk = os.read(descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        content = b"".join(chunks)
        if len(content) != metadata.st_size:
            fail("environment", "read_size")
        try:
            path_metadata = os.lstat(path)
        except OSError:
            fail("environment", "path_replaced")
        if (
            path_metadata.st_dev != metadata.st_dev
            or path_metadata.st_ino != metadata.st_ino
            or path_metadata.st_nlink != 1
            or stat.S_IMODE(path_metadata.st_mode) != 0o600
        ):
            fail("environment", "path_replaced")
    finally:
        os.close(descriptor)
    if b"\0" in content:
        fail("environment", "nul_byte")
    return content


def read_secure_environment() -> str:
    content = secure_read(KDS_ENV, 742)
    values: dict[str, str] = {}
    for raw in content.decode("utf-8", "strict").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:]
        if "=" not in line:
            fail("environment", "assignment_shape")
        name, value = line.split("=", 1)
        parsed = shlex.split(value, posix=True)
        if len(parsed) != 1:
            fail("environment", "value_shape")
        values[name] = parsed[0]
    dsn = values.get("KDS_INTAKE_DATABASE_URL", "")
    parsed = urllib.parse.urlparse(dsn)
    if parsed.scheme not in ("postgres", "postgresql"):
        fail("environment", "database_scheme")
    if parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
        fail("environment", "database_host")
    if parsed.port not in (None, 5432) or parsed.path.lstrip("/") != "gbrain":
        fail("environment", "database_target")
    return dsn


def migration_body(path: Path, expected_sha256: str) -> str:
    raw = path.read_bytes()
    if digest(raw) != expected_sha256:
        fail("migration_source", path.name)
    text = raw.decode("utf-8", "strict")
    if not text.startswith("BEGIN;\n") or not text.endswith("COMMIT;\n"):
        fail("migration_source", f"{path.name}_transaction_envelope")
    body = text[len("BEGIN;\n") : -len("COMMIT;\n")]
    if "\nCOMMIT;" in body or "\nBEGIN;" in body:
        fail("migration_source", f"{path.name}_nested_transaction")
    return body


def relation_presence(connection: psycopg.Connection[Any]) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for name in RELATIONS:
        row = connection.execute("SELECT to_regclass(%s)::text", (f"knowledge_intake.{name}",)).fetchone()
        result[name] = bool(row and row[0])
    return result


def verify_empty_schema(connection: psycopg.Connection[Any]) -> tuple[list[int], dict[str, int]]:
    presence = relation_presence(connection)
    if not all(presence.values()):
        fail("verification", "relation_missing")
    versions = [row[0] for row in connection.execute("SELECT version FROM knowledge_intake.schema_versions ORDER BY version").fetchall()]
    if versions != [1, 2]:
        fail("verification", "schema_versions")
    counts: dict[str, int] = {}
    for table in BUSINESS_TABLES:
        counts[table] = connection.execute(f"SELECT count(*) FROM knowledge_intake.{table}").fetchone()[0]
    if any(counts.values()):
        fail("verification", "business_rows_present")
    return versions, counts


def other_client_sessions(connection: psycopg.Connection[Any]) -> int:
    row = connection.execute(
        "SELECT count(*) FROM pg_stat_activity "
        "WHERE datname = current_database() AND backend_type = 'client backend' AND pid <> pg_backend_pid()"
    ).fetchone()
    return int(row[0])


def owned_lock_state() -> bool:
    try:
        check_own_lock()
        return True
    except ControlledFailure:
        return False


def partial_owned_state() -> bool:
    try:
        attest_directory(ATOMIC_GUARD, 0o700)
        _, owner_content = attest_identity_file(GUARD_OWNER, None, immutable=False)
        validate_lock_payload(owner_content)
        if OPSX_LOCK.exists():
            attest_identity_file(OPSX_LOCK, owner_content, immutable=None)
        return True
    except ControlledFailure:
        return False


def cleanup_partial_owned_lock() -> bool:
    if not partial_owned_state():
        return False
    try:
        _, owner_content = attest_identity_file(GUARD_OWNER, None, immutable=False)
        validate_lock_payload(owner_content)
        if OPSX_LOCK.exists():
            attest_identity_file(OPSX_LOCK, owner_content, immutable=None)
            os.chflags(OPSX_LOCK, 0)
            OPSX_LOCK.unlink()
        attest_identity_file(GUARD_OWNER, owner_content, immutable=False)
        GUARD_OWNER.unlink()
        ATOMIC_GUARD.rmdir()
        return not OPSX_LOCK.exists() and not ATOMIC_GUARD.exists()
    except (ControlledFailure, OSError):
        return False


def lock_helper_acquire() -> dict[str, Any]:
    if not ATOMIC_GUARD.parent.is_dir():
        fail("lock", "harness_directory_missing")
    try:
        os.mkdir(ATOMIC_GUARD, 0o700)
    except FileExistsError:
        fail("lock", "atomic_guard_exists")
    try:
        payload = lock_payload()
        owner_fd = os.open(
            GUARD_OWNER,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
            0o400,
        )
        try:
            os.write(owner_fd, payload)
            os.fsync(owner_fd)
        finally:
            os.close(owner_fd)
        if OPSX_LOCK.exists():
            fail("lock", "official_lock_exists")
        lock_fd = os.open(
            OPSX_LOCK,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
            0o400,
        )
        try:
            os.write(lock_fd, payload)
            os.fsync(lock_fd)
        finally:
            os.close(lock_fd)
        os.chflags(OPSX_LOCK, stat.UF_IMMUTABLE)
        check_own_lock()
        return {"status": "success", "code": "atomic_opsx_lock_acquired", "control": CONTROL_ID}
    except Exception:
        cleanup_partial_owned_lock()
        raise


def lock_helper_release() -> dict[str, Any]:
    if not owned_lock_state():
        fail("lock", "owned_lock_not_releasable")
    os.chflags(OPSX_LOCK, 0)
    OPSX_LOCK.unlink()
    GUARD_OWNER.unlink()
    ATOMIC_GUARD.rmdir()
    if OPSX_LOCK.exists() or ATOMIC_GUARD.exists():
        fail("lock", "release_incomplete")
    return {"status": "success", "code": "atomic_opsx_lock_released", "control": CONTROL_ID}


def lock_helper_cleanup() -> dict[str, Any]:
    if not cleanup_partial_owned_lock():
        fail("lock", "partial_cleanup_unresolved")
    return {"status": "success", "code": "partial_opsx_lock_cleaned", "control": CONTROL_ID}


def run_lock_helper(action: str, sealed_sha: str) -> tuple[bool, bool, str]:
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
                    helper_action,
                    "--sealed-sha",
                    sealed_sha,
                ),
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=LOCK_HELPER_TIMEOUT_SECONDS,
                env=environment,
            )
            return "completed", result.returncode
        except subprocess.TimeoutExpired:
            return "timeout", -1
        except OSError:
            return "spawn_failed", -1

    outcome, returncode = invoke(action)
    if action == "acquire":
        if outcome == "completed" and returncode == 0 and owned_lock_state():
            return True, True, "acquired"
        failure = f"acquire_{outcome}" if outcome != "completed" else "acquire_failed"
        if partial_owned_state():
            cleanup_outcome, cleanup_returncode = invoke("cleanup")
            if cleanup_outcome == "completed" and cleanup_returncode == 0 and not OPSX_LOCK.exists() and not ATOMIC_GUARD.exists():
                return False, False, f"{failure}_recovered"
            return False, False, f"{failure}_lock_unresolved"
        if OPSX_LOCK.exists() or ATOMIC_GUARD.exists():
            return False, False, f"{failure}_lock_unresolved"
        return False, False, f"{failure}_no_lock"
    released = outcome == "completed" and returncode == 0 and not OPSX_LOCK.exists() and not ATOMIC_GUARD.exists()
    return released, False, "released" if released else f"release_{outcome}_lock_unresolved"


def hard_baseline(*, own_lock_expected: bool = False) -> tuple[str, tuple[str, str]]:
    for baseline in BASELINES:
        check_repo(baseline, own_lock_expected=own_lock_expected)
    validate_runtime()
    for name, path in OFFICIAL_LOCK_HELPERS.items():
        if digest(path.read_bytes()) != SEALED_OFFICIAL_LOCK_HELPERS[name]:
            fail("lock", f"official_{name}_helper_drift")
    dsn = read_secure_environment()
    bodies = tuple(migration_body(path, expected) for path, expected in MIGRATIONS)
    return dsn, bodies  # type: ignore[return-value]


def terminal_result(status: str, code: str, **extra: Any) -> dict[str, Any]:
    return {
        "status": status,
        "code": code,
        "control": CONTROL_ID,
        "database": "gbrain",
        "host": "loopback",
        "connection_count": 1,
        "fixture_created": False,
        "api_requests": 0,
        **extra,
    }


def safe_error_code(error: BaseException) -> str:
    sqlstate = getattr(error, "sqlstate", None)
    return str(sqlstate or type(error).__name__)


def verify_schema_absent(connection: psycopg.Connection[Any]) -> bool:
    try:
        connection.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        absent = not any(relation_presence(connection).values())
        xid = connection.execute("SELECT txid_current_if_assigned()").fetchone()[0]
        connection.execute("ROLLBACK")
        return absent and xid is None
    except Exception:
        try:
            connection.execute("ROLLBACK")
        except Exception:
            pass
        return False


def execute_migration(dsn: str, bodies: tuple[str, str]) -> dict[str, Any]:
    connection: psycopg.Connection[Any] | None = None
    commit_attempted = False
    commit_confirmed = False
    postverify_confirmed = False
    try:
        try:
            connection = psycopg.connect(
                dsn,
                autocommit=True,
                connect_timeout=DATABASE_CONNECT_TIMEOUT_SECONDS,
                options=(
                    f"-c lock_timeout={DATABASE_LOCK_TIMEOUT_MILLISECONDS} "
                    f"-c statement_timeout={DATABASE_STATEMENT_TIMEOUT_MILLISECONDS} "
                    f"-c idle_in_transaction_session_timeout={DATABASE_IDLE_TRANSACTION_TIMEOUT_MILLISECONDS}"
                ),
            )
        except Exception as error:
            return terminal_result(
                "failed_no_change",
                "database_connection_failed",
                commit_attempted=False,
                commit_confirmed=False,
                postverify_confirmed=False,
                error_class=safe_error_code(error),
            )
        timeout_settings = connection.execute(
            "SELECT "
            "(extract(epoch FROM current_setting('lock_timeout')::interval) * 1000)::bigint, "
            "(extract(epoch FROM current_setting('statement_timeout')::interval) * 1000)::bigint, "
            "(extract(epoch FROM current_setting('idle_in_transaction_session_timeout')::interval) * 1000)::bigint"
        ).fetchone()
        if timeout_settings != (
            DATABASE_LOCK_TIMEOUT_MILLISECONDS,
            DATABASE_STATEMENT_TIMEOUT_MILLISECONDS,
            DATABASE_IDLE_TRANSACTION_TIMEOUT_MILLISECONDS,
        ):
            return terminal_result(
                "stopped_no_change",
                "database_timeout_settings_mismatch",
                commit_attempted=False,
                commit_confirmed=False,
                postverify_confirmed=False,
            )
        connection.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        pre = relation_presence(connection)
        xid_before = connection.execute("SELECT txid_current_if_assigned()").fetchone()[0]
        pre_sessions = other_client_sessions(connection)
        connection.execute("ROLLBACK")
        if any(pre.values()) or xid_before is not None or pre_sessions != 0:
            return terminal_result(
                "stopped_no_change",
                "schema_not_absent_or_xid_assigned",
                commit_attempted=False,
                commit_confirmed=False,
                postverify_confirmed=False,
            )

        try:
            connection.execute("BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE")
            connection.execute(bodies[0])
            connection.execute(bodies[1])
            versions, counts = verify_empty_schema(connection)
            validate_runtime()
            if other_client_sessions(connection) != 0:
                fail("database_precommit", "other_client_session_present")
        except Exception as error:
            try:
                connection.execute("ROLLBACK")
            except Exception:
                pass
            recovered = verify_schema_absent(connection)
            return terminal_result(
                "failed_recovered" if recovered else "failed_fail_closed",
                "precommit_migration_rolled_back" if recovered else "precommit_rollback_unverified",
                commit_attempted=False,
                commit_confirmed=False,
                postverify_confirmed=False,
                error_class=safe_error_code(error),
            )

        commit_attempted = True
        try:
            connection.execute("COMMIT")
        except Exception as error:
            return terminal_result(
                "failed_fail_closed",
                "commit_outcome_ambiguous_reconciliation_required",
                commit_attempted=True,
                commit_confirmed=False,
                postverify_confirmed=False,
                error_class=safe_error_code(error),
            )
        commit_confirmed = True

        try:
            connection.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            post_versions, post_counts = verify_empty_schema(connection)
            xid_after = connection.execute("SELECT txid_current_if_assigned()").fetchone()[0]
            post_sessions = other_client_sessions(connection)
            connection.execute("ROLLBACK")
            validate_runtime()
            if xid_after is not None or post_versions != versions or post_counts != counts or post_sessions != 0:
                fail("database_postimage", "verification_mismatch")
        except Exception as error:
            try:
                connection.execute("ROLLBACK")
            except Exception:
                pass
            return terminal_result(
                "failed_fail_closed",
                "schema_committed_postverify_failed_reconciliation_required",
                commit_attempted=True,
                commit_confirmed=True,
                postverify_confirmed=False,
                error_class=safe_error_code(error),
            )
        postverify_confirmed = True
        return terminal_result(
            "success",
            "local_release0_schema_migrated",
            migration_transaction_count=1,
            schema_versions=versions,
            relations_present=len(RELATIONS),
            business_rows=sum(counts.values()),
            audit_rows=counts["audit_events"],
            outbox_rows=counts["outbox_events"],
            row_count_semantics="postcommit_snapshot",
            other_client_sessions_snapshot=0,
            lock_timeout_ms=DATABASE_LOCK_TIMEOUT_MILLISECONDS,
            statement_timeout_ms=DATABASE_STATEMENT_TIMEOUT_MILLISECONDS,
            idle_transaction_timeout_ms=DATABASE_IDLE_TRANSACTION_TIMEOUT_MILLISECONDS,
            commit_attempted=commit_attempted,
            commit_confirmed=commit_confirmed,
            postverify_confirmed=postverify_confirmed,
        )
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass


def preflight(sealed_sha: str) -> dict[str, Any]:
    source = Path(__file__).read_bytes()
    if digest(source) != sealed_sha:
        fail("controller", "sealed_sha")
    dsn, bodies = hard_baseline()
    del dsn
    return {
        "status": "eligible_for_separate_migration_authorization",
        "control": CONTROL_ID,
        "controller_sha256": sealed_sha,
        "migration_count": len(bodies),
        "migration_sha256": [expected for _, expected in MIGRATIONS],
        "target": {"scheme": "postgresql", "host": "loopback", "port": 5432, "database": "gbrain"},
        "fixture_created": False,
        "api_requests": 0,
    }


def combine_lock_outcome(result: dict[str, Any], released: bool) -> dict[str, Any]:
    combined = dict(result)
    combined["opsx_lock_released"] = released
    if released:
        return combined
    combined["prior_code"] = result.get("code")
    combined["status"] = "failed_fail_closed"
    if result.get("commit_confirmed"):
        combined["code"] = "schema_committed_lock_unresolved"
    elif result.get("commit_attempted"):
        combined["code"] = "commit_outcome_ambiguous_and_lock_unresolved"
    else:
        combined["code"] = "no_commit_lock_unresolved"
    return combined


def execute(sealed_sha: str) -> dict[str, Any]:
    source = Path(__file__).read_bytes()
    if digest(source) != sealed_sha:
        fail("controller", "sealed_sha")
    prelock_dsn, _ = hard_baseline()
    prelock_dsn = ""
    acquired = False
    result: dict[str, Any] | None = None
    dsn = ""
    try:
        lock_success, acquired, lock_code = run_lock_helper("acquire", sealed_sha)
        if not lock_success:
            result = {
                "status": "failed_fail_closed" if "lock_unresolved" in lock_code else "stopped_no_change",
                "code": lock_code,
                "step": "lock",
                "control": CONTROL_ID,
                "commit_attempted": False,
                "commit_confirmed": False,
                "postverify_confirmed": False,
            }
        else:
            dsn, bodies = hard_baseline(own_lock_expected=True)
            result = execute_migration(dsn, bodies)
    except ControlledFailure as error:
        result = {
            "status": "stopped_no_change",
            "code": error.code,
            "step": error.step,
            "control": CONTROL_ID,
            "commit_attempted": False,
            "commit_confirmed": False,
            "postverify_confirmed": False,
        }
    except Exception as error:
        result = {
            "status": "stopped_no_change",
            "code": "controller_internal_error",
            "error_class": type(error).__name__,
            "control": CONTROL_ID,
            "commit_attempted": False,
            "commit_confirmed": False,
            "postverify_confirmed": False,
        }
    finally:
        dsn = ""
    if not acquired or result is None:
        return result
    released, _, _ = run_lock_helper("release", sealed_sha)
    return combine_lock_outcome(result, released)


def self_test() -> dict[str, Any]:
    for path, expected in MIGRATIONS:
        body = migration_body(path, expected)
        if not body.strip() or body.lstrip().startswith("BEGIN") or body.rstrip().endswith("COMMIT;"):
            fail("self_test", "migration_body")
    sample = b"a\0b\0"
    if digest(sample) != hashlib.sha256(sample).hexdigest():
        fail("self_test", "digest")
    status_sample = (
        b"?? artifact\0"
        b"?? .harness/opsx.lock\0"
        b"?? .harness/opsx.atomic-guard/\0"
        b"?? .harness/opsx.atomic-guard/owner\0"
    )
    if normalized_status(status_sample, True) != b"?? artifact\0":
        fail("self_test", "lock_status_normalization")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        secure = root / "secure.env"
        secure.write_bytes(b"A=1\n")
        secure.chmod(0o600)
        if secure_read(secure, 4) != b"A=1\n":
            fail("self_test", "secure_read")
        hardlink = root / "hardlink.env"
        os.link(secure, hardlink)
        try:
            secure_read(secure, 4)
            fail("self_test", "hardlink_accepted")
        except ControlledFailure as error:
            if error.code != "owner_size_or_link_count":
                raise
        hardlink.unlink()
        replacement = os.lstat(secure)

        class ReplacedPath:
            st_dev = replacement.st_dev
            st_ino = replacement.st_ino + 1
            st_nlink = 1
            st_mode = replacement.st_mode

        with mock.patch("os.lstat", return_value=ReplacedPath()):
            try:
                secure_read(secure, 4)
                fail("self_test", "replacement_accepted")
            except ControlledFailure as error:
                if error.code != "path_replaced":
                    raise
        symlink = root / "symlink.env"
        symlink.symlink_to(secure)
        try:
            secure_read(symlink, 4)
            fail("self_test", "symlink_accepted")
        except ControlledFailure as error:
            if error.code != "open_failed":
                raise
        identity = root / "identity"
        identity_payload = lock_payload()
        identity.write_bytes(identity_payload)
        identity.chmod(0o400)
        attest_identity_file(identity, identity_payload, immutable=False)
        identity_metadata = os.lstat(identity)

        class ReplacedIdentity:
            st_dev = identity_metadata.st_dev
            st_ino = identity_metadata.st_ino + 1
            st_uid = identity_metadata.st_uid
            st_nlink = identity_metadata.st_nlink
            st_mode = identity_metadata.st_mode

        with mock.patch("os.lstat", return_value=ReplacedIdentity()):
            try:
                attest_identity_file(identity, identity_payload, immutable=False)
                fail("self_test", "identity_replacement_accepted")
            except ControlledFailure as error:
                if error.code != "identity_replaced":
                    raise
        guard = root / "guard"
        owner = guard / "owner"
        partial_lock = root / "opsx.lock"
        guard.mkdir(mode=0o700)
        owner.write_bytes(identity_payload)
        owner.chmod(0o400)
        partial_lock.write_bytes(identity_payload)
        partial_lock.chmod(0o400)
        with mock.patch(f"{__name__}.ATOMIC_GUARD", guard), mock.patch(
            f"{__name__}.GUARD_OWNER", owner
        ), mock.patch(f"{__name__}.OPSX_LOCK", partial_lock):
            helper_calls = 0

            def helper_timeout_then_cleanup(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
                nonlocal helper_calls
                helper_calls += 1
                if helper_calls == 1:
                    raise subprocess.TimeoutExpired(("lock-helper",), 5)
                if not cleanup_partial_owned_lock():
                    fail("self_test", "partial_lock_cleanup")
                return subprocess.CompletedProcess(args[0], 0, b"", b"")

            with mock.patch("subprocess.run", side_effect=helper_timeout_then_cleanup):
                lock_success, owned, code = run_lock_helper("acquire", "sealed")
            if lock_success or owned or code != "acquire_timeout_recovered":
                fail("self_test", "partial_timeout_cleanup_terminal")
            if guard.exists() or partial_lock.exists():
                fail("self_test", "partial_lock_residue")
    success = terminal_result(
        "success",
        "local_release0_schema_migrated",
        commit_attempted=True,
        commit_confirmed=True,
        postverify_confirmed=True,
    )
    if combine_lock_outcome(success, False)["code"] != "schema_committed_lock_unresolved":
        fail("self_test", "committed_lock_terminal")
    ambiguous = terminal_result(
        "failed_fail_closed",
        "commit_outcome_ambiguous_reconciliation_required",
        commit_attempted=True,
        commit_confirmed=False,
        postverify_confirmed=False,
    )
    if combine_lock_outcome(ambiguous, False)["code"] != "commit_outcome_ambiguous_and_lock_unresolved":
        fail("self_test", "ambiguous_lock_terminal")
    with mock.patch("subprocess.run", side_effect=subprocess.TimeoutExpired(("lock-helper",), 5)):
        lock_success, owned, code = run_lock_helper("acquire", "sealed")
    if lock_success or owned or code != "acquire_timeout_no_lock":
        fail("self_test", "acquire_timeout_terminal")

    class FakeRows:
        def __init__(self, *, one: tuple[Any, ...] | None = None, many: list[tuple[Any, ...]] | None = None):
            self.one = one
            self.many = many or []

        def fetchone(self) -> tuple[Any, ...] | None:
            return self.one

        def fetchall(self) -> list[tuple[Any, ...]]:
            return self.many

    class FakeConnection:
        def __init__(self, mode: str):
            self.mode = mode
            self.phase = "initial"
            self.body_calls = 0

        def execute(self, statement: str, parameters: tuple[str, ...] | None = None) -> FakeRows:
            if statement.startswith("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY"):
                if self.phase == "committed" and self.mode == "postverify_failure":
                    raise RuntimeError("synthetic postverify failure")
                self.phase = "post" if self.phase == "committed" else "pre"
                return FakeRows()
            if statement.startswith("BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE"):
                self.phase = "migration"
                return FakeRows()
            if statement == "ROLLBACK":
                self.phase = "rolled_back"
                return FakeRows()
            if statement == "COMMIT":
                if self.mode == "commit_response_loss":
                    raise RuntimeError("synthetic commit response loss")
                self.phase = "committed"
                return FakeRows()
            if statement.startswith("SELECT to_regclass"):
                relation = parameters[0] if parameters else ""
                present = self.phase in ("migration", "post")
                return FakeRows(one=(relation if present else None,))
            if statement == "SELECT txid_current_if_assigned()":
                return FakeRows(one=(None,))
            if "current_setting('lock_timeout')" in statement:
                return FakeRows(
                    one=(
                        DATABASE_LOCK_TIMEOUT_MILLISECONDS,
                        DATABASE_STATEMENT_TIMEOUT_MILLISECONDS,
                        DATABASE_IDLE_TRANSACTION_TIMEOUT_MILLISECONDS,
                    )
                )
            if statement.startswith("SELECT version FROM"):
                return FakeRows(many=[(1,), (2,)])
            if statement.startswith("SELECT count(*) FROM"):
                return FakeRows(one=(0,))
            self.body_calls += 1
            if self.mode == "precommit_failure" and self.body_calls == 2:
                raise RuntimeError("synthetic precommit failure")
            return FakeRows()

        def close(self) -> None:
            return None

    for mode, expected_status, expected_code in (
        ("precommit_failure", "failed_recovered", "precommit_migration_rolled_back"),
        ("commit_response_loss", "failed_fail_closed", "commit_outcome_ambiguous_reconciliation_required"),
        ("postverify_failure", "failed_fail_closed", "schema_committed_postverify_failed_reconciliation_required"),
    ):
        fake = FakeConnection(mode)
        with mock.patch("psycopg.connect", return_value=fake) as connect_mock, mock.patch(
            f"{__name__}.validate_runtime", return_value=None
        ):
            terminal = execute_migration("redacted", ("body-one", "body-two"))
        options = connect_mock.call_args.kwargs.get("options", "")
        for expected in ("lock_timeout=5000", "statement_timeout=30000", "idle_in_transaction_session_timeout=30000"):
            if expected not in options:
                fail("self_test", "database_timeout_options")
        if terminal["status"] != expected_status or terminal["code"] != expected_code:
            fail("self_test", f"{mode}_terminal")
    return {
        "status": "pass",
        "control": CONTROL_ID,
        "migration_envelopes": 2,
        "relations": len(RELATIONS),
        "single_combined_transaction": True,
        "lock_inside_baseline": True,
        "commit_terminal_states": True,
        "commit_fault_injection": True,
        "secure_environment_faults": True,
        "same_fd_lock_attestation": True,
        "partial_lock_cleanup": True,
        "lock_helper_timeout": True,
        "database_statement_timeouts": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--lock-helper", choices=("acquire", "release", "cleanup"))
    parser.add_argument("--sealed-sha", default="")
    arguments = parser.parse_args()
    try:
        if arguments.lock_helper:
            source = Path(__file__).read_bytes()
            if digest(source) != arguments.sealed_sha:
                fail("controller", "sealed_sha")
            if arguments.lock_helper == "acquire":
                result = lock_helper_acquire()
            elif arguments.lock_helper == "release":
                result = lock_helper_release()
            else:
                result = lock_helper_cleanup()
        elif arguments.self_test:
            result = self_test()
        elif arguments.preflight:
            result = preflight(arguments.sealed_sha)
        else:
            result = execute(arguments.sealed_sha)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        return 0 if result.get("status") in ("pass", "success", "eligible_for_separate_migration_authorization") else 3
    except ControlledFailure as error:
        print(
            json.dumps(
                {"status": "stopped", "control": CONTROL_ID, "step": error.step, "code": error.code},
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2
    except Exception as error:
        print(
            json.dumps(
                {
                    "status": "stopped",
                    "control": CONTROL_ID,
                    "step": "controller",
                    "code": "internal_error",
                    "error_class": type(error).__name__,
                },
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 4


if __name__ == "__main__":
    sys.exit(main())
