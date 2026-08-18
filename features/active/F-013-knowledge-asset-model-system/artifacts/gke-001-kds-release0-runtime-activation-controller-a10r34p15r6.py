#!/usr/bin/env python3
"""Sealed fail-stop controller for the GKE-001 KDS Release 0 runtime activation.

The default mode is inert. ``--self-test`` uses synthetic data and a temporary
directory only. Real execution requires ``--execute`` plus the externally
sealed SHA-256 of this file. Any failure consumes the execution attempt: this
program performs bounded recovery and exits; it never hot-fixes or continues.
"""
from __future__ import annotations

import argparse
import base64
import ctypes
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import signal
import socket
import stat
import struct
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


CONTROL_ID = "GKE-001-COORDINATION-20260816-040-A10R34P15R6R5R2"
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ENV = Path("/Users/lujunxiang/.globalcloud/kds.env")
KDS_LEGACY_SECRET = Path("/Users/lujunxiang/.globalcloud/kds-delegation-secret")
KDS_RUNNER = Path("/Users/lujunxiang/.globalcloud/run-kds-api-18080.sh")
KDS_PLIST = Path("/Users/lujunxiang/Library/LaunchAgents/com.globalcloud.kds-api-18080.plist")
KDS_LABEL = "com.globalcloud.kds-api-18080"
KDS_PID = 81015
MMC_PID = 80610
KDS_PORT = 18080
SHADOW_PORT = 18081
EXPECTED_KDS_HEAD = "2ac85c55163b7acf0ede699184ac360579ccefaa"
EXPECTED_MMC_HEAD = "c93463ff5ee40ce66d8e1a09995ca8c66a24c86d"
EXPECTED_GPCF_HEAD = "11d022b818332d2271a78b427c326eb454507a5a"
EXPECTED_KDS_STATUS = (
    264,
    "a0174d93cf2407f274f3806a50caa99444981c9918061c5619f3ef8cc2dab299",
    554,
    "1528fb303c7112f05ac2a7d7ee05d156f3e55bed7cf9c4f2a38117c220240dd2",
)
EXPECTED_MMC_STATUS = (
    10,
    "300ef303a5a647e54931171ff5ebf309192671fbf9f52f027acedf40d7ab8ad9",
    98,
    "2fd6e7fe5409ed79e410ea20e722a84eecb1d141d969153b27c969b3ebf6a451",
)
EXPECTED_GPCF_STATUS = (
    734,
    "95b32308a0f567107dbe575e5a0bf5433230c4a7e8c69ececb1e0dab9e0095f3",
    751,
    "9a3dcd09e97bd212a1e7f5331e0010bc6a9304ee2a262c35849f66ed5d0eba77",
)
EXPECTED_CONTROLLED_ENTRY_SHA256 = (
    ("03-data-ai-knowledge/GlobalCloud项目群知识工程规范.md", "01018556e7bdd83f432537fdd866dfe836d6c29e0695810261968a32780b2746"),
    ("03-data-ai-knowledge/GlobalCloud知识工程应用体系实施方案.md", "990b2db334928e821dd796d44703cf6efce9d3558add5001f164188c2072edd8"),
    ("governance/openspec/gke001-program-binding.yaml", "796306ca8aef8247c8d74dbcf5a85c18bf2ad9e7a99ebc04b94724c267ce306b"),
    ("governance/codegraph/gke001-engineering-domain-binding.yaml", "1aac07c78deff8d42dda05226ca57cb79a5adaf98b51a4205576dc1d1825272f"),
    ("governance/codegraph/repo-codegraph-registry.yaml", "d0dcf156af58df8c0047797b46661b5b4a562a542f30e5cf2bb963714977d190"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/.openspec.yaml", "1e29e84341de33c4849e79cac1189edb575e45fb593636616d4ffb1103293bc8"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/README.md", "0fea6a15d663b3feb22bb6c0b18548f69671baba65e47bf98511bdc2ee471217"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/design.md", "c7d4d9fbf84baa31d28c868bd2337bf57311818cd1805f1401bc99d0ecebaa05"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/proposal.md", "f5c5aa2fee56d463a7babb25cf4b398780f50b37ffaf7f0b8470fe46d8bd7d0b"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/tasks.md", "bb04d0af10b97b194a92c62186d4712bbb552f79a186ae4b813a1c7c3ce2f4be"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/specs/README.md", "9e49ed8bb6bad41aca1350d2ced4738c8b5c559e25f8432e5a5b264a7c417e95"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/specs/gke001-codegraph-binding/README.md", "24761310c4b1d870dcc0a47228148c00673a54ba8a5f052b52f73c60188102c0"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/specs/gke001-codegraph-binding/spec.md", "1f629b4c9472e2b14bb759554d6ea99b02ab6947d25e53bcbc610a7ffad95c90"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/specs/gke001-program-governance/README.md", "4b59f2b0828a9463c4dc6c31420bab01b5242c809cd1a9dca9e5d6044a406e28"),
    ("openspec/changes/integrate-gke001-openspec-codegraph/specs/gke001-program-governance/spec.md", "020de9a3000e9072fd87945bee69661ba89ee56bec070a54a1629adb06c3b843"),
    ("features/active/F-013-knowledge-asset-model-system/feature.yaml", "a1dbe356d8032ba58803bfd3123c6f79677208109528c4f1998ea82a4d0e9e46"),
    ("features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-application-program-roadmap-v1.yaml", "32f00e131b0dab667fa7403dbd6d6a79c865f517959c5d6b227f82340534ad9f"),
    ("02-governance/loop/LOOP_CONTROL_BOARD.md", "1b4d26854984e7962c3bd54fb89ff3e6ae7744edf41f997392c8b705c91257c2"),
    ("02-governance/loop/LOOP_SESSION_REGISTRY.md", "02e390fd78950ad42ee6a4401db44a754cc66b2ec8a1996c3978b9fe1c2e1499"),
)
EXPECTED_KDS_START = "Sun Aug 16 20:26:45 2026"
EXPECTED_MMC_START = "Fri Aug 14 07:20:14 2026"
EXPECTED_KDS_ARGV = (
    "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python",
    "api_server.py",
    "--host",
    "127.0.0.1",
    "--port",
    "18080",
    "--data-dir",
    "concepts",
)
EXPECTED_RUNNER_ARGV = ("/bin/zsh", str(KDS_RUNNER))
EXPECTED_SHADOW_ARGV = (
    "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python",
    "api_server.py",
    "--host",
    "127.0.0.1",
    "--port",
    "18081",
    "--data-dir",
    "concepts",
)
EXPECTED_MMC_ARGV = (
    "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python",
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
)
EXPECTED_RUNNER_SHA = "544fa07436cabaaa7dc86b1c98ce0183cf5b9862fdde4d7b77518ebe6f95f959"
EXPECTED_PLIST_SHA = "e26365b304a13ea34389455ad3427264ba35ac4eeee9b3daad147c541ede5ad0"
EXPECTED_ENV_SIZE = 407
EXPECTED_ENV_MODE = 0o600
EXPECTED_ENV_UID = 501
EXPECTED_ENV_GID = 20
EXPECTED_ENV_XATTRS = ("com.apple.lastuseddate#PS", "com.apple.provenance")
EXPECTED_LEGACY_SECRET_SIZE = 65
HMAC_KEY_ID = "studio"
TARGET_ENV_KEYS = (
    "PYTHONDONTWRITEBYTECODE",
    "KDS_INTAKE_DATABASE_URL",
    "KDS_INTAKE_HMAC_KEYS_JSON",
    "KDS_KNOWLEDGE_READ_CURSOR_SECRET",
)
MISSPELLED_ENV_KEY = "PYTHONDWRITEBYTECODE"
KERN_PROCARGS2 = 49
CTL_KERN = 1


class GateFailure(RuntimeError):
    def __init__(self, step: str, code: str) -> None:
        super().__init__(code)
        self.step = step
        self.code = code


def fail(step: str, code: str) -> None:
    raise GateFailure(step, code)


def bounded_result(status: str, step: str, code: str, **facts: object) -> None:
    payload = {"control_id": CONTROL_ID, "status": status, "step": step, "code": code}
    payload.update(facts)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


def run(command: Sequence[str], *, cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        list(command),
        cwd=str(cwd) if cwd else None,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        fail("command", "subprocess_failed")
    return result


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_controlled_entry_hashes(
    root: Path,
    expected_entries: Sequence[Tuple[str, str]],
) -> None:
    for relative_path, expected_sha in expected_entries:
        path = root / relative_path
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(str(path), flags)
        except FileNotFoundError:
            fail("baseline", "controlled_entry_missing")
        except OSError:
            fail("baseline", "controlled_entry_type_mismatch")
        try:
            info = os.fstat(descriptor)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                fail("baseline", "controlled_entry_type_mismatch")
            digest = hashlib.sha256()
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
            try:
                after = path.lstat()
            except OSError:
                fail("baseline", "controlled_entry_replaced")
            if stat.S_ISLNK(after.st_mode) or (after.st_dev, after.st_ino) != (info.st_dev, info.st_ino):
                fail("baseline", "controlled_entry_replaced")
            if digest.hexdigest() != expected_sha:
                fail("baseline", "controlled_entry_hash_mismatch")
        finally:
            os.close(descriptor)


def status_record_count(raw: bytes) -> int:
    records = raw.split(b"\0")
    count = 0
    index = 0
    while index < len(records) and records[index]:
        record = records[index]
        count += 1
        index += 1
        if len(record) >= 2 and (record[0:1] in (b"R", b"C") or record[1:2] in (b"R", b"C")):
            index += 1
    return count


def git_snapshot(root: Path) -> Tuple[str, str, int, int, int, int, str, int, str]:
    head = run(("/usr/bin/git", "rev-parse", "HEAD"), cwd=root).stdout.decode().strip()
    origin = run(("/usr/bin/git", "rev-parse", "origin/main"), cwd=root).stdout.decode().strip()
    counts = run(("/usr/bin/git", "rev-list", "--left-right", "--count", "HEAD...origin/main"), cwd=root).stdout.decode().split()
    if len(counts) != 2:
        fail("git", "ahead_behind_unavailable")
    staged_raw = run(("/usr/bin/git", "diff", "--cached", "--name-only", "-z"), cwd=root).stdout
    ordinary = run(("/usr/bin/git", "status", "--porcelain=v1", "-z"), cwd=root).stdout
    expanded = run(("/usr/bin/git", "status", "--porcelain=v1", "-z", "--untracked-files=all"), cwd=root).stdout
    return (
        head,
        origin,
        int(counts[0]),
        int(counts[1]),
        len([value for value in staged_raw.split(b"\0") if value]),
        status_record_count(ordinary),
        hashlib.sha256(ordinary).hexdigest(),
        status_record_count(expanded),
        hashlib.sha256(expanded).hexdigest(),
    )


def parse_procargs_blob(
    raw: bytes,
    selected_keys: Optional[Iterable[str]] = None,
) -> Tuple[Tuple[str, ...], Dict[str, bytes]]:
    if len(raw) < struct.calcsize("=i"):
        fail("procargs", "blob_too_short")
    argc = struct.unpack_from("=i", raw, 0)[0]
    if argc <= 0 or argc > 4096:
        fail("procargs", "argc_invalid")
    cursor = struct.calcsize("=i")

    def take_c_string(position: int) -> Tuple[bytes, int]:
        end = raw.find(b"\0", position)
        if end < 0:
            fail("procargs", "unterminated_field")
        return raw[position:end], end + 1

    _, cursor = take_c_string(cursor)
    while cursor < len(raw) and raw[cursor] == 0:
        cursor += 1
    argv: List[str] = []
    for _ in range(argc):
        value, cursor = take_c_string(cursor)
        argv.append(value.decode("utf-8", "strict"))
    environment: Dict[str, bytes] = {}
    selected = set(selected_keys) if selected_keys is not None else None
    while cursor < len(raw):
        if raw[cursor] == 0:
            cursor += 1
            continue
        value, cursor = take_c_string(cursor)
        if b"=" not in value:
            continue
        key, item = value.split(b"=", 1)
        try:
            key_text = key.decode("ascii", "strict")
        except UnicodeDecodeError:
            continue
        if selected is None or key_text in selected:
            environment[key_text] = item
    return tuple(argv), environment


def procargs_blob(pid: int) -> bytes:
    libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib", use_errno=True)
    sysctl = libc.sysctl
    sysctl.argtypes = (
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_uint,
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.c_void_p,
        ctypes.c_size_t,
    )
    sysctl.restype = ctypes.c_int
    mib = (ctypes.c_int * 3)(CTL_KERN, KERN_PROCARGS2, pid)
    size = ctypes.c_size_t(0)
    if sysctl(mib, 3, None, ctypes.byref(size), None, 0) != 0 or size.value <= 0:
        fail("procargs", "size_query_failed")
    buffer = ctypes.create_string_buffer(size.value)
    if sysctl(mib, 3, buffer, ctypes.byref(size), None, 0) != 0:
        fail("procargs", "read_failed")
    return ctypes.string_at(buffer, size.value)


def process_cwd_matches(pid: int, expected_cwd: Path) -> bool:
    result = run(("/usr/sbin/lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"), check=False)
    if result.returncode not in (0, 1):
        fail("process", "cwd_query_failed")
    cwd_values = [line[1:] for line in result.stdout.decode().splitlines() if line.startswith("n")]
    return cwd_values == [str(expected_cwd)]


def process_snapshot(
    pid: int,
    expected_cwd: Path,
    selected_keys: Iterable[str] = (),
) -> Tuple[Tuple[str, ...], Dict[str, bytes], int, str]:
    argv, environment = parse_procargs_blob(procargs_blob(pid), selected_keys)
    ppid_text = run(("/bin/ps", "-p", str(pid), "-o", "ppid="), check=False).stdout.decode().strip()
    start_text = run(("/bin/ps", "-p", str(pid), "-o", "lstart="), check=False).stdout.decode().strip()
    if not ppid_text or not start_text:
        fail("process", "process_missing")
    if not process_cwd_matches(pid, expected_cwd):
        fail("process", "cwd_mismatch")
    return argv, environment, int(ppid_text), " ".join(start_text.split())


def stable_process_snapshot(
    identity: "ProcessIdentity",
    expected_cwd: Path,
    selected_keys: Iterable[str],
    *,
    deadline: float,
    error_step: str,
    timeout_code: str,
    validate_attempt: Callable[[], None],
    monotonic: Callable[[], float] = time.monotonic,
    pause: Callable[[float], None] = time.sleep,
    snapshot: Callable[
        [int, Path, Iterable[str]],
        Tuple[Tuple[str, ...], Dict[str, bytes], int, str],
    ] = process_snapshot,
) -> Tuple[Tuple[str, ...], Dict[str, bytes], int, str]:
    while monotonic() < deadline:
        validate_attempt()
        try:
            sample = snapshot(identity.pid, expected_cwd, selected_keys)
        except GateFailure as exc:
            if exc.step != "procargs" or exc.code not in ("size_query_failed", "read_failed"):
                raise
            validate_attempt()
            pause(0.05)
            continue
        validate_attempt()
        return sample
    fail(error_step, timeout_code)
    raise AssertionError


def listener_pids(port: int) -> Tuple[int, ...]:
    result = run(("/usr/sbin/lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-Fpn"), check=False)
    if result.returncode not in (0, 1):
        fail("listener", "lsof_failed")
    pids = []
    names = []
    for line in result.stdout.decode().splitlines():
        if line.startswith("p") and line[1:].isdigit():
            pids.append(int(line[1:]))
        elif line.startswith("n"):
            names.append(line[1:])
    if pids and not all(name == f"127.0.0.1:{port}" for name in names):
        fail("listener", "non_loopback_listener")
    return tuple(sorted(set(pids)))


def postgres_connection_count(pid: int) -> int:
    result = run(
        ("/usr/sbin/lsof", "-a", "-p", str(pid), "-nP", "-iTCP:5432", "-sTCP:ESTABLISHED", "-Fp"),
        check=False,
    )
    if result.returncode not in (0, 1):
        fail("database", "lsof_failed")
    return len({line[1:] for line in result.stdout.decode().splitlines() if line.startswith("p")})


def launchagent_output() -> Optional[str]:
    target = f"gui/{os.getuid()}/{KDS_LABEL}"
    result = run(("/bin/launchctl", "print", target), check=False)
    if result.returncode == 0:
        return result.stdout.decode("utf-8", "replace")
    if result.returncode == 113:
        return None
    fail("launchagent", "print_failed")
    return None


def require_port_free(port: int) -> None:
    if listener_pids(port):
        fail("listener", "port_not_free")
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        probe.bind(("127.0.0.1", port))
    except OSError:
        fail("listener", "port_bind_failed")
    finally:
        probe.close()


def list_xattrs(path: Path) -> Tuple[str, ...]:
    result = run(("/usr/bin/xattr", str(path)), check=False)
    if result.returncode not in (0, 1):
        fail("xattr", "list_failed")
    return tuple(sorted(line for line in result.stdout.decode().splitlines() if line))


def read_xattrs(path: Path) -> Dict[str, bytes]:
    values: Dict[str, bytes] = {}
    for name in list_xattrs(path):
        result = run(("/usr/bin/xattr", "-px", name, str(path)))
        try:
            values[name] = bytes.fromhex(result.stdout.decode())
        except ValueError:
            fail("xattr", "hex_decode_failed")
    return values


def write_xattrs(path: Path, values: Mapping[str, bytes]) -> None:
    for name, value in values.items():
        run(("/usr/bin/xattr", "-wx", name, value.hex(), str(path)))


def has_acl(path: Path) -> bool:
    result = run(("/bin/ls", "-lde", str(path)))
    return len(result.stdout.decode("utf-8", "replace").splitlines()) > 1


@dataclass(frozen=True)
class FileImage:
    content: bytes
    mode: int
    uid: int
    gid: int
    device: int
    inode: int
    atime_ns: int
    mtime_ns: int
    xattrs: Mapping[str, bytes]


def capture_file(path: Path) -> FileImage:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(str(path), flags)
    except OSError:
        fail("config", "same_fd_open_failed")
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            fail("config", "unsafe_file_type")
        chunks = []
        total = 0
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            total += len(chunk)
            if total > 1024 * 1024:
                fail("config", "file_too_large")
            chunks.append(chunk)
        content = b"".join(chunks)
        xattrs = read_xattrs(path)
        if has_acl(path):
            fail("config", "acl_present")
        after = path.lstat()
        if stat.S_ISLNK(after.st_mode) or (after.st_dev, after.st_ino) != (info.st_dev, info.st_ino):
            fail("config", "same_fd_identity_changed")
        return FileImage(
            content,
            stat.S_IMODE(info.st_mode),
            info.st_uid,
            info.st_gid,
            info.st_dev,
            info.st_ino,
            info.st_atime_ns,
            info.st_mtime_ns,
            xattrs,
        )
    finally:
        os.close(descriptor)


def atomic_write_image(
    path: Path,
    content: bytes,
    image: FileImage,
    *,
    expected_current: Optional[FileImage] = None,
) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.gke001-", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(str(temporary), image.mode)
        os.chown(str(temporary), image.uid, image.gid)
        write_xattrs(temporary, image.xattrs)
        os.utime(str(temporary), ns=(image.atime_ns, image.mtime_ns))
        if expected_current is not None:
            current = path.lstat()
            if stat.S_ISLNK(current.st_mode) or (current.st_dev, current.st_ino) != (
                expected_current.device,
                expected_current.inode,
            ):
                fail("config", "pre_replace_identity_changed")
        os.replace(str(temporary), str(path))
        directory_fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def restore_file_image(path: Path, image: FileImage, candidate: bytes) -> None:
    current = capture_file(path)
    if current.content == image.content:
        if (
            current.mode != image.mode
            or current.uid != image.uid
            or current.gid != image.gid
            or current.xattrs != image.xattrs
        ):
            fail("recovery", "preimage_metadata_mismatch")
        return
    if current.content != candidate:
        fail("recovery", "config_current_bytes_unknown")
    atomic_write_image(path, image.content, image, expected_current=current)
    restored = capture_file(path)
    if (
        restored.content != image.content
        or restored.mode != image.mode
        or restored.uid != image.uid
        or restored.gid != image.gid
        or restored.xattrs != image.xattrs
    ):
        fail("recovery", "config_restore_mismatch")


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def hmac_json_bytes(signer_secret: bytes) -> bytes:
    try:
        secret_text = signer_secret.decode("utf-8", "strict")
    except UnicodeDecodeError:
        fail("render", "value_encoding_invalid")
    return json.dumps(
        {HMAC_KEY_ID: secret_text},
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def render_config(preimage: bytes, dsn: bytes, signer_secret: bytes, cursor: bytes) -> bytes:
    if any(key.encode() + b"=" in preimage for key in TARGET_ENV_KEYS) or MISSPELLED_ENV_KEY.encode() + b"=" in preimage:
        fail("render", "target_key_preexists")
    try:
        dsn_text = dsn.decode("utf-8", "strict")
        cursor_text = cursor.decode("ascii", "strict")
    except UnicodeDecodeError:
        fail("render", "value_encoding_invalid")
    hmac_keys = hmac_json_bytes(signer_secret).decode("ascii")
    lines = (
        "export PYTHONDONTWRITEBYTECODE=1",
        f"export KDS_INTAKE_DATABASE_URL={shell_quote(dsn_text)}",
        f"export KDS_INTAKE_HMAC_KEYS_JSON={shell_quote(hmac_keys)}",
        f"export KDS_KNOWLEDGE_READ_CURSOR_SECRET={shell_quote(cursor_text)}",
    )
    return preimage.rstrip(b"\n") + b"\n" + ("\n".join(lines) + "\n").encode("utf-8")


def validate_rendered_config(candidate: bytes, preimage: bytes) -> None:
    if not candidate.startswith(preimage.rstrip(b"\n") + b"\n"):
        fail("render", "preimage_not_preserved")
    if MISSPELLED_ENV_KEY.encode() + b"=" in candidate:
        fail("render", "misspelled_key_present")
    for key in TARGET_ENV_KEYS:
        pattern = re.compile(rb"(?m)^export " + re.escape(key.encode()) + rb"=")
        if len(pattern.findall(candidate)) != 1:
            fail("render", "exact_key_count_failed")


def validate_dsn(raw: bytes) -> None:
    try:
        parsed = urllib.parse.urlparse(raw.decode("utf-8", "strict"))
    except UnicodeDecodeError:
        fail("database", "dsn_encoding_invalid")
    database = parsed.path.lstrip("/")
    if parsed.scheme not in ("postgres", "postgresql"):
        fail("database", "scheme_not_postgresql")
    if parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
        fail("database", "host_not_loopback")
    if parsed.port not in (None, 5432):
        fail("database", "port_not_local_postgresql")
    if database != "gbrain":
        fail("database", "database_not_proven_nonproduction")


def normalize_secret(raw: bytes) -> bytes:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError:
        fail("runtime_values", "signer_secret_encoding_invalid")
    if "\x00" in text:
        fail("runtime_values", "signer_secret_nul_invalid")
    normalized = text.strip()
    if len(normalized.encode("utf-8")) < 32:
        fail("runtime_values", "signer_secret_too_short")
    return normalized.encode("utf-8")


def select_signer_secret(
    legacy_process_raw: Optional[bytes],
    active_process_raw: Optional[bytes],
    legacy_file_raw: bytes,
) -> bytes:
    active_secret = normalize_secret(active_process_raw or b"")
    legacy_file_secret = normalize_secret(legacy_file_raw)
    if not hmac.compare_digest(legacy_file_secret, active_secret):
        fail("runtime_values", "signer_secret_mismatch")
    if legacy_process_raw is not None:
        legacy_process_secret = normalize_secret(legacy_process_raw)
        if not hmac.compare_digest(legacy_process_secret, active_secret):
            fail("runtime_values", "signer_secret_mismatch")
    return active_secret


def offline_verifier_roundtrip(secret: bytes, cursor: bytes) -> None:
    sys.path.insert(0, str(KDS_ROOT))
    try:
        from knowledge_intake.authorization import DelegationVerifier, StaticHmacKeyResolver
        from knowledge_intake.read_authorization import ReadAuthorityVerifier
        from knowledge_intake.read_contract import CursorCodec, CursorContext
    finally:
        if sys.path and sys.path[0] == str(KDS_ROOT):
            sys.path.pop(0)
    now = int(time.time())
    payload = {
        "version": 1,
        "kid": HMAC_KEY_ID,
        "iss": "mmc",
        "aud": "kds-knowledge-intake",
        "subject": "studio-user:1",
        "tenant_id": "personal",
        "org_id": "gehua",
        "permissions": ["knowledge:read"],
        "project_scopes": ["project:synthetic:read"],
        "session_scopes": ["session:synthetic@project:synthetic"],
        "read_authority": {
            "binding_revision": "release0.v1",
            "target_object_ref": "knowledge-object:synthetic",
            "project_ref": "project:synthetic",
            "session_ref": "session:synthetic",
        },
        "issued_at": now - 1,
        "expires_at": now + 30,
        "nonce": str(uuid.uuid4()),
    }
    encoded = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    signature = base64.urlsafe_b64encode(hmac.new(secret, encoded.encode(), hashlib.sha256).digest()).decode().rstrip("=")
    verifier = ReadAuthorityVerifier(
        DelegationVerifier(StaticHmacKeyResolver({HMAC_KEY_ID: secret}), issuer="mmc", audience="kds-knowledge-intake")
    )
    authority = verifier.verify(
        encoded,
        signature,
        target_object_ref="knowledge-object:synthetic",
        project_ref="project:synthetic",
        session_ref="session:synthetic",
        now=now,
    )
    if authority.identity.tenant_id != "personal":
        fail("offline", "authority_roundtrip_failed")
    codec = CursorCodec(cursor)
    context = CursorContext(
        "search",
        "search",
        "personal",
        "gehua",
        "knowledge-object:synthetic",
        "project:synthetic",
        "session:synthetic",
        "synthetic-filter",
    )
    encoded_cursor = codec.encode(context, [1, "asset:synthetic"])
    if codec.decode(encoded_cursor, context) != [1, "asset:synthetic"]:
        fail("offline", "cursor_roundtrip_failed")


@dataclass(frozen=True)
class RuntimeExpectation:
    mode: str
    dsn: bytes
    hmac_json: bytes = b""
    cursor: bytes = b""


def verify_runtime_environment(
    identity: ProcessIdentity,
    port: int,
    expectation: RuntimeExpectation,
    expected_argv: Tuple[str, ...],
    *,
    phase: str,
    job_bound: bool = False,
    timeout: float = 3,
    monotonic: Callable[[], float] = time.monotonic,
    pause: Callable[[float], None] = time.sleep,
    snapshot: Callable[
        [int, Path, Iterable[str]],
        Tuple[Tuple[str, ...], Dict[str, bytes], int, str],
    ] = process_snapshot,
    identity_check: Optional[Callable[[], bool]] = None,
    cwd_check: Optional[Callable[[], bool]] = None,
    owners_snapshot: Optional[Callable[[], Tuple[int, ...]]] = None,
    job_snapshot: Optional[Callable[[], Tuple[int, Optional[int]]]] = None,
) -> None:
    selected = (
        "PYTHONDONTWRITEBYTECODE",
        "DATABASE_URL",
        "KDS_INTAKE_DATABASE_URL",
        "KDS_INTAKE_HMAC_KEYS_JSON",
        "KDS_KNOWLEDGE_READ_CURSOR_SECRET",
        "KDS_INTAKE_DELEGATION_ISSUER",
        "KDS_INTAKE_DELEGATION_AUDIENCE",
    )
    if identity_check is None:
        identity_check = lambda: identity_alive(identity)
    if cwd_check is None:
        cwd_check = lambda: process_cwd_matches(identity.pid, KDS_ROOT)
    if owners_snapshot is None:
        owners_snapshot = lambda: listener_pids(port)
    if job_snapshot is None:
        job_snapshot = launch_job_snapshot

    def validate_attempt() -> None:
        if not identity_check():
            fail("readiness", f"{phase}_identity_changed")
        if not cwd_check():
            fail("readiness", f"{phase}_cwd_changed")
        if job_bound:
            runs_count, job_pid = job_snapshot()
            if runs_count != 1 or job_pid != identity.pid:
                fail("readiness", f"{phase}_job_identity_changed")
        if owners_snapshot() != (identity.pid,):
            fail("readiness", f"{phase}_listener_owner_mismatch")

    argv, environment, _, _ = stable_process_snapshot(
        identity,
        KDS_ROOT,
        selected,
        deadline=monotonic() + timeout,
        error_step="readiness",
        timeout_code=f"{phase}_procargs_timeout",
        validate_attempt=validate_attempt,
        monotonic=monotonic,
        pause=pause,
        snapshot=snapshot,
    )
    if argv != expected_argv:
        fail("readiness", f"{phase}_argv_mismatch")
    validate_runtime_environment_mapping(environment, expectation)
    validate_attempt()


def validate_runtime_environment_mapping(
    environment: Mapping[str, bytes],
    expectation: RuntimeExpectation,
) -> None:
    if expectation.mode == "release0":
        if (
            environment.get("PYTHONDONTWRITEBYTECODE") != b"1"
            or environment.get("KDS_INTAKE_DATABASE_URL") != expectation.dsn
            or environment.get("KDS_INTAKE_HMAC_KEYS_JSON") != expectation.hmac_json
            or environment.get("KDS_KNOWLEDGE_READ_CURSOR_SECRET") != expectation.cursor
            or environment.get("KDS_INTAKE_DELEGATION_ISSUER", b"mmc") != b"mmc"
            or environment.get("KDS_INTAKE_DELEGATION_AUDIENCE", b"kds-knowledge-intake") != b"kds-knowledge-intake"
        ):
            fail("readiness", "release0_environment_mismatch")
    elif expectation.mode == "legacy":
        if (
            environment.get("DATABASE_URL") != expectation.dsn
            or environment.get("KDS_INTAKE_DATABASE_URL")
            or environment.get("KDS_INTAKE_HMAC_KEYS_JSON")
            or environment.get("KDS_KNOWLEDGE_READ_CURSOR_SECRET")
        ):
            fail("readiness", "legacy_environment_mismatch")
    else:
        fail("readiness", "runtime_expectation_invalid")


def http_json(port: int, path: str) -> object:
    request = urllib.request.Request(f"http://127.0.0.1:{port}{path}", method="GET")
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            if response.status != 200:
                fail("http", "status_not_200")
            return json.loads(response.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        fail("http", "request_failed")


def readiness_sample(
    identity: ProcessIdentity,
    port: int,
    expectation: RuntimeExpectation,
    expected_argv: Tuple[str, ...],
    *,
    phase: str,
    job_bound: bool = False,
    attest: Optional[Callable[[], None]] = None,
    owners_snapshot: Optional[Callable[[], Tuple[int, ...]]] = None,
    http_get: Callable[[int, str], object] = http_json,
    database_connections: Callable[[int], int] = postgres_connection_count,
) -> None:
    if owners_snapshot is None:
        owners_snapshot = lambda: listener_pids(port)
    if owners_snapshot() != (identity.pid,):
        fail("readiness", "listener_owner_mismatch")
    if attest is None:
        attest = lambda: verify_runtime_environment(
            identity,
            port,
            expectation,
            expected_argv,
            phase=phase,
            job_bound=job_bound,
        )
    attest()
    health = http_get(port, "/api/v1/health")
    if not isinstance(health, dict):
        fail("readiness", "health_shape_invalid")
    schema = http_get(port, "/openapi.json")
    if not isinstance(schema, dict):
        fail("readiness", "openapi_shape_invalid")
    paths = schema.get("paths")
    expected_routes = {
        "/api/v1/knowledge-read/release-0/search": "kdsCanonicalKnowledgeSearch",
        "/api/v1/knowledge-read/release-0/read": "kdsCanonicalKnowledgeRead",
    }
    if not isinstance(paths, dict):
        fail("readiness", "openapi_paths_missing")
    for path, operation_id in expected_routes.items():
        operation = paths.get(path, {}).get("post") if isinstance(paths.get(path), dict) else None
        if not isinstance(operation, dict) or operation.get("operationId") != operation_id:
            fail("readiness", "release0_route_missing")
    if database_connections(identity.pid) != 0:
        fail("readiness", "database_connection_observed")
    attest()


def wait_listener(port: int, timeout: float) -> int:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        pids = listener_pids(port)
        if len(pids) == 1:
            return pids[0]
        if len(pids) > 1:
            fail("listener", "multiple_owners")
        time.sleep(0.25)
    fail("listener", "readiness_timeout")
    return 0


def process_exists(pid: int) -> bool:
    result = run(("/bin/ps", "-p", str(pid), "-o", "stat="), check=False)
    status = result.stdout.decode().strip()
    return bool(status) and not status.startswith("Z")


@dataclass(frozen=True)
class ProcessIdentity:
    pid: int
    start: str


def capture_process_identity(pid: int) -> ProcessIdentity:
    result = run(("/bin/ps", "-p", str(pid), "-o", "lstart="), check=False)
    start = " ".join(result.stdout.decode().split())
    if not start:
        fail("process", "identity_missing")
    return ProcessIdentity(pid, start)


def identity_alive(identity: ProcessIdentity) -> bool:
    if not process_exists(identity.pid):
        return False
    result = run(("/bin/ps", "-p", str(identity.pid), "-o", "lstart="), check=False)
    return " ".join(result.stdout.decode().split()) == identity.start


def stop_known_process(
    identity: ProcessIdentity,
    term_timeout: float,
    kill_timeout: float,
    process_kind: str,
) -> bool:
    if process_kind != "fresh":
        fail("process", "signal_target_kind_forbidden")
    if not identity_alive(identity):
        return True
    try:
        os.kill(identity.pid, signal.SIGTERM)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    deadline = time.monotonic() + term_timeout
    while time.monotonic() < deadline:
        if not identity_alive(identity):
            return True
        time.sleep(0.25)
    try:
        os.kill(identity.pid, signal.SIGKILL)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    deadline = time.monotonic() + kill_timeout
    while time.monotonic() < deadline:
        if not identity_alive(identity):
            return True
        time.sleep(0.25)
    return not identity_alive(identity)


def stop_created_child(
    process: subprocess.Popen,
    term_timeout: float,
    kill_timeout: float,
    process_kind: str,
) -> bool:
    if process_kind not in {"shadow", "manual"}:
        fail("process", "created_child_kind_forbidden")
    if process.poll() is not None:
        process.wait(timeout=1)
        return True
    try:
        process.terminate()
        process.wait(timeout=term_timeout)
        return True
    except subprocess.TimeoutExpired:
        pass
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    try:
        process.kill()
        process.wait(timeout=kill_timeout)
        return True
    except (subprocess.TimeoutExpired, ProcessLookupError):
        return process.poll() is not None
    except PermissionError:
        return False


def stop_old_process(identity: ProcessIdentity) -> str:
    if not identity_alive(identity) or listener_pids(KDS_PORT) != (identity.pid,):
        return "ambiguous"
    try:
        os.kill(identity.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return "ambiguous"
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        alive = identity_alive(identity)
        owners = listener_pids(KDS_PORT)
        if not alive and not owners:
            return "exited"
        if owners and owners != (identity.pid,):
            return "ambiguous"
        time.sleep(0.25)
    if identity_alive(identity) and listener_pids(KDS_PORT) == (identity.pid,):
        return "preserved"
    return "ambiguous"


@dataclass(frozen=True)
class RecoveryState:
    config_mutated: bool
    shadow_started: bool
    old_cutover_started: bool
    old_identity_available: bool
    old_transition: str
    bootstrap_attempted: bool
    known_fresh_available: bool
    dsn_available: bool


@dataclass(frozen=True)
class RecoveryHooks:
    restore_config: Callable[[], None]
    stop_shadow: Callable[[], bool]
    bootout_if_present: Callable[[], None]
    verify_old_owner: Callable[[], bool]
    bootout_fresh: Callable[[], bool]
    stop_fresh: Callable[[], bool]
    owners: Callable[[], Tuple[int, ...]]
    manual_recovery: Callable[[], Tuple[str, Optional[int]]]


@dataclass(frozen=True)
class RecoveryOutcome:
    status: str
    recovery: str
    recovery_pid: Optional[int] = None
    observed_owner_count: Optional[int] = None


def perform_recovery(state: RecoveryState, hooks: RecoveryHooks) -> RecoveryOutcome:
    restore_ok = True
    cleanup_ok = True
    if state.config_mutated:
        try:
            hooks.restore_config()
        except BaseException:
            restore_ok = False
    if state.shadow_started:
        try:
            cleanup_ok = hooks.stop_shadow() and cleanup_ok
        except BaseException:
            cleanup_ok = False
    if not state.old_cutover_started:
        if not state.old_identity_available:
            if not restore_ok:
                return RecoveryOutcome("failed_fail_closed", "config_restore_unresolved")
            if not cleanup_ok:
                return RecoveryOutcome("failed_fail_closed", "precutover_cleanup_unresolved")
            return RecoveryOutcome("failed_fail_closed", "hard_baseline_stopped_before_mutation")
        try:
            hooks.bootout_if_present()
        except BaseException:
            cleanup_ok = False
        old_ok = False
        if state.old_identity_available:
            try:
                old_ok = hooks.verify_old_owner()
            except BaseException:
                old_ok = False
        if not restore_ok:
            return RecoveryOutcome("failed_fail_closed", "config_restore_unresolved_old_owner_preserved" if old_ok else "config_restore_unresolved")
        if not cleanup_ok:
            return RecoveryOutcome("failed_fail_closed", "precutover_cleanup_unresolved")
        if old_ok:
            return RecoveryOutcome("failed_recovered", "old_owner_preserved_launchagent_booted_out")
        return RecoveryOutcome("failed_fail_closed", "precutover_owner_ambiguous_launchagent_booted_out")
    if state.old_transition == "preserved" and state.old_identity_available:
        try:
            old_ok = hooks.verify_old_owner()
        except BaseException:
            old_ok = False
        if not restore_ok:
            return RecoveryOutcome("failed_fail_closed", "config_restore_unresolved_old_owner_preserved" if old_ok else "config_restore_unresolved")
        if not cleanup_ok:
            return RecoveryOutcome("failed_fail_closed", "old_owner_preservation_cleanup_unresolved")
        if old_ok:
            return RecoveryOutcome("failed_recovered", "old_owner_preserved_after_single_sigterm_launchagent_booted_out")
        return RecoveryOutcome("failed_fail_closed", "old_owner_preservation_gate_failed")
    if state.bootstrap_attempted:
        try:
            cleanup_ok = hooks.bootout_fresh() and cleanup_ok
        except BaseException:
            cleanup_ok = False
        if state.known_fresh_available:
            try:
                cleanup_ok = hooks.stop_fresh() and cleanup_ok
            except BaseException:
                cleanup_ok = False
    else:
        try:
            hooks.bootout_if_present()
        except BaseException:
            cleanup_ok = False
    try:
        owners = hooks.owners()
    except BaseException:
        return RecoveryOutcome("failed_fail_closed", "listener_ownership_unresolved")
    if owners:
        return RecoveryOutcome("failed_fail_closed", "unknown_owner_remains_no_second_owner", observed_owner_count=len(owners))
    if not restore_ok:
        return RecoveryOutcome("failed_fail_closed", "config_restore_unresolved_no_manual_recovery")
    if not cleanup_ok:
        return RecoveryOutcome("failed_fail_closed", "known_process_cleanup_unresolved_no_manual_recovery")
    if not state.dsn_available:
        return RecoveryOutcome("failed_fail_closed", "original_dsn_unavailable_no_manual_recovery")
    try:
        recovery, recovery_pid = hooks.manual_recovery()
    except BaseException:
        return RecoveryOutcome("failed_fail_closed", "manual_recovery_exception_no_retry")
    status = "failed_recovered" if recovery == "manual_single_owner_restored_launchagent_booted_out" else "failed_fail_closed"
    return RecoveryOutcome(status, recovery, recovery_pid=recovery_pid)


def verify_old_owner_preserved(identity: ProcessIdentity) -> bool:
    for sample in range(2):
        if not identity_alive(identity) or listener_pids(KDS_PORT) != (identity.pid,):
            return False
        if postgres_connection_count(identity.pid) != 0:
            return False
        if sample == 0:
            time.sleep(5)
    return True


def launch_job_snapshot() -> Tuple[int, Optional[int]]:
    output = launchagent_output()
    if output is None:
        fail("launchagent", "job_absent")
    runs_match = re.search(r"\bruns = ([0-9]+)\b", output)
    pid_match = re.search(r"\bpid = ([0-9]+)\b", output)
    if runs_match is None:
        fail("launchagent", "runs_missing")
    return int(runs_match.group(1)), int(pid_match.group(1)) if pid_match else None


def wait_fresh_job(
    captured: List[ProcessIdentity],
    *,
    timeout: float = 30,
    monotonic: Callable[[], float] = time.monotonic,
    pause: Callable[[float], None] = time.sleep,
    job_snapshot: Callable[[], Tuple[int, Optional[int]]] = launch_job_snapshot,
    identity_snapshot: Callable[[int], ProcessIdentity] = capture_process_identity,
    argv_snapshot: Optional[Callable[[int], Tuple[str, ...]]] = None,
    cwd_check: Optional[Callable[[int], bool]] = None,
    owners_snapshot: Optional[Callable[[], Tuple[int, ...]]] = None,
) -> ProcessIdentity:
    if argv_snapshot is None:
        argv_snapshot = lambda pid: process_snapshot(pid, KDS_ROOT)[0]
    if owners_snapshot is None:
        owners_snapshot = lambda: listener_pids(KDS_PORT)
    if cwd_check is None:
        cwd_check = lambda pid: process_cwd_matches(pid, KDS_ROOT)
    deadline = monotonic() + timeout
    first: Optional[ProcessIdentity] = captured[0] if captured else None
    final_argv_seen = False
    while monotonic() < deadline:
        runs_count, pid = job_snapshot()
        if runs_count != 1:
            fail("cutover", "fresh_job_runs_mismatch")
        if pid is not None:
            observed = identity_snapshot(pid)
            if first is None:
                first = observed
                captured.append(first)
            elif observed != first:
                fail("cutover", "fresh_process_identity_changed")
            latest_owners: Tuple[int, ...] = ()

            def validate_attempt() -> None:
                nonlocal latest_owners
                current_runs, current_pid = job_snapshot()
                if current_runs != 1:
                    fail("cutover", "fresh_job_runs_mismatch")
                if current_pid is None:
                    fail("cutover", "fresh_process_disappeared")
                if current_pid != first.pid or identity_snapshot(current_pid) != first:
                    fail("cutover", "fresh_process_identity_changed")
                if not cwd_check(current_pid):
                    fail("cutover", "fresh_process_cwd_changed")
                latest_owners = owners_snapshot()
                if latest_owners and latest_owners != (first.pid,):
                    fail("cutover", "unknown_listener_owner")

            def sample_argv() -> Tuple[Tuple[str, ...], Tuple[int, ...]]:
                sample = stable_process_snapshot(
                    first,
                    KDS_ROOT,
                    (),
                    deadline=deadline,
                    error_step="cutover",
                    timeout_code="fresh_wait_procargs_timeout",
                    validate_attempt=validate_attempt,
                    monotonic=monotonic,
                    pause=pause,
                    snapshot=lambda sample_pid, expected_cwd, selected: (
                        argv_snapshot(sample_pid),
                        {},
                        1,
                        first.start,
                    ),
                )
                return sample[0], latest_owners

            argv, owners = sample_argv()
            if argv == EXPECTED_RUNNER_ARGV:
                if final_argv_seen:
                    fail("cutover", "fresh_process_argv_regressed")
                if owners:
                    confirmed_argv, confirmed_owners = sample_argv()
                    if confirmed_owners != (first.pid,):
                        fail("cutover", "fresh_listener_owner_changed")
                    if confirmed_argv == EXPECTED_RUNNER_ARGV:
                        fail("cutover", "runner_bound_listener")
                    if confirmed_argv != EXPECTED_KDS_ARGV:
                        fail("cutover", "fresh_process_argv_mismatch")
                    final_argv_seen = True
                    return first
            elif argv == EXPECTED_KDS_ARGV:
                final_argv_seen = True
                if owners == (first.pid,):
                    confirmed_argv, confirmed_owners = sample_argv()
                    if confirmed_owners != (first.pid,):
                        fail("cutover", "fresh_listener_owner_changed")
                    if confirmed_argv != EXPECTED_KDS_ARGV:
                        fail("cutover", "fresh_process_argv_regressed")
                    return first
            else:
                fail("cutover", "fresh_process_argv_mismatch")
        elif first is not None:
            fail("cutover", "fresh_process_disappeared")
        pause(0.25)
    fail("cutover", "fresh_job_start_timeout")
    raise AssertionError


def verify_fresh_sample(identity: ProcessIdentity, expectation: RuntimeExpectation) -> None:
    runs_count, pid = launch_job_snapshot()
    if runs_count != 1 or pid != identity.pid or not identity_alive(identity):
        fail("cutover", "fresh_job_identity_changed")
    readiness_sample(
        identity,
        KDS_PORT,
        expectation,
        EXPECTED_KDS_ARGV,
        phase="fresh_readiness",
        job_bound=True,
    )


def bootout_fresh_job() -> bool:
    target = f"gui/{os.getuid()}/{KDS_LABEL}"
    if launchagent_output() is not None:
        result = run(("/bin/launchctl", "bootout", target), check=False)
        if result.returncode != 0:
            return False
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if launchagent_output() is None:
            return True
        time.sleep(0.25)
    return False


def start_shadow() -> subprocess.Popen:
    command = (
        "set -eu; set -a; source /Users/lujunxiang/.globalcloud/kds.env; set +a; "
        "export KDS_DELEGATION_SECRET=\"$(< /Users/lujunxiang/.globalcloud/kds-delegation-secret)\"; "
        "cd '/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS'; "
        "exec /usr/bin/python3 api_server.py --host 127.0.0.1 --port 18081 --data-dir concepts"
    )
    return subprocess.Popen(
        ("/bin/zsh", "-lc", command),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def bootout_if_present() -> None:
    if launchagent_output() is None:
        return
    target = f"gui/{os.getuid()}/{KDS_LABEL}"
    result = run(("/bin/launchctl", "bootout", target), check=False)
    if result.returncode != 0:
        fail("recovery", "bootout_failed")


def manual_recovery_environment(base: Mapping[str, str], original_dsn: bytes) -> Dict[str, str]:
    recovery_environment = dict(base)
    for name in (
        "KDS_INTAKE_DATABASE_URL",
        "KDS_INTAKE_HMAC_KEYS_JSON",
        "KDS_KNOWLEDGE_READ_CURSOR_SECRET",
    ):
        recovery_environment.pop(name, None)
    recovery_environment["DATABASE_URL"] = original_dsn.decode("utf-8", "strict")
    return recovery_environment


def start_manual_recovery(original_dsn: bytes) -> Tuple[str, Optional[int]]:
    try:
        recovery_environment = manual_recovery_environment(os.environ, original_dsn)
    except UnicodeDecodeError:
        return "service_unavailable_after_bounded_recovery", None
    process = subprocess.Popen(
        (str(KDS_RUNNER),),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env=recovery_environment,
    )
    try:
        identity = capture_process_identity(process.pid)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            owners = listener_pids(KDS_PORT)
            if owners:
                if owners != (identity.pid,):
                    fail("recovery", "unknown_listener_owner")
                break
            if process.poll() is not None:
                fail("recovery", "manual_process_exited")
            time.sleep(0.25)
        else:
            fail("recovery", "manual_start_timeout")
        if launchagent_output() is not None:
            fail("recovery", "manual_identity_invalid")
        legacy_expectation = RuntimeExpectation("legacy", original_dsn)
        readiness_sample(
            identity,
            KDS_PORT,
            legacy_expectation,
            EXPECTED_KDS_ARGV,
            phase="manual_recovery",
        )
        time.sleep(5)
        if not identity_alive(identity) or listener_pids(KDS_PORT) != (identity.pid,):
            fail("recovery", "manual_identity_changed")
        readiness_sample(
            identity,
            KDS_PORT,
            legacy_expectation,
            EXPECTED_KDS_ARGV,
            phase="manual_recovery",
        )
        return "manual_single_owner_restored_launchagent_booted_out", identity.pid
    except BaseException:
        if not stop_created_child(process, 10, 5, "manual"):
            return "known_failed_recovery_remains_no_second_owner", process.pid
        owners = listener_pids(KDS_PORT)
        if owners:
            return "unknown_owner_remains_no_second_owner", owners[0] if len(owners) == 1 else None
        return "service_unavailable_after_bounded_recovery", None


def hard_baseline(sealed_sha: str) -> Tuple[Dict[str, bytes], Dict[str, bytes], FileImage]:
    if not re.fullmatch(r"[0-9a-f]{64}", sealed_sha) or sha256_file(Path(__file__).resolve()) != sealed_sha:
        fail("baseline", "controller_sha_mismatch")
    validate_controlled_entry_hashes(GPCF_ROOT, EXPECTED_CONTROLLED_ENTRY_SHA256)
    if git_snapshot(KDS_ROOT) != (
        EXPECTED_KDS_HEAD,
        EXPECTED_KDS_HEAD,
        0,
        0,
        0,
        *EXPECTED_KDS_STATUS,
    ):
        fail("baseline", "kds_git_mismatch")
    if git_snapshot(MMC_ROOT) != (
        EXPECTED_MMC_HEAD,
        EXPECTED_MMC_HEAD,
        0,
        0,
        0,
        *EXPECTED_MMC_STATUS,
    ):
        fail("baseline", "mmc_git_mismatch")
    if git_snapshot(GPCF_ROOT) != (
        EXPECTED_GPCF_HEAD,
        EXPECTED_GPCF_HEAD,
        0,
        0,
        0,
        *EXPECTED_GPCF_STATUS,
    ):
        fail("baseline", "gpcf_git_mismatch")
    if any((root / ".harness/opsx.lock").exists() for root in (GPCF_ROOT, KDS_ROOT, MMC_ROOT)):
        fail("baseline", "opsx_lock_present")
    if sha256_file(KDS_RUNNER) != EXPECTED_RUNNER_SHA or sha256_file(KDS_PLIST) != EXPECTED_PLIST_SHA:
        fail("baseline", "launcher_hash_mismatch")
    if launchagent_output() is not None:
        fail("baseline", "launchagent_not_booted_out")
    if listener_pids(KDS_PORT) != (KDS_PID,):
        fail("baseline", "kds_listener_mismatch")
    require_port_free(SHADOW_PORT)
    kds_argv, kds_environment, kds_ppid, kds_start = process_snapshot(
        KDS_PID,
        KDS_ROOT,
        ("KDS_INTAKE_DATABASE_URL", "DATABASE_URL", "KDS_DELEGATION_SECRET"),
    )
    mmc_argv, mmc_environment, mmc_ppid, mmc_start = process_snapshot(
        MMC_PID,
        MMC_ROOT,
        ("KDS_DELEGATION_SECRET",),
    )
    if kds_argv != EXPECTED_KDS_ARGV or kds_ppid != 1 or kds_start != EXPECTED_KDS_START:
        fail("baseline", "kds_process_mismatch")
    if mmc_argv != EXPECTED_MMC_ARGV or mmc_ppid != 1 or mmc_start != EXPECTED_MMC_START:
        fail("baseline", "mmc_process_mismatch")
    if postgres_connection_count(KDS_PID) != 0:
        fail("baseline", "database_connection_observed")
    image = capture_file(KDS_ENV)
    if (
        len(image.content) != EXPECTED_ENV_SIZE
        or image.mode != EXPECTED_ENV_MODE
        or image.uid != EXPECTED_ENV_UID
        or image.gid != EXPECTED_ENV_GID
        or tuple(sorted(image.xattrs)) != EXPECTED_ENV_XATTRS
    ):
        fail("baseline", "config_metadata_mismatch")
    if any(key.encode() + b"=" in image.content for key in TARGET_ENV_KEYS) or MISSPELLED_ENV_KEY.encode() + b"=" in image.content:
        fail("baseline", "config_target_key_present")
    secret_info = KDS_LEGACY_SECRET.lstat()
    if (
        stat.S_ISLNK(secret_info.st_mode)
        or not stat.S_ISREG(secret_info.st_mode)
        or secret_info.st_nlink != 1
        or stat.S_IMODE(secret_info.st_mode) != 0o600
        or secret_info.st_uid != EXPECTED_ENV_UID
        or secret_info.st_gid != EXPECTED_ENV_GID
        or secret_info.st_size != EXPECTED_LEGACY_SECRET_SIZE
        or has_acl(KDS_LEGACY_SECRET)
    ):
        fail("baseline", "legacy_secret_metadata_mismatch")
    return kds_environment, mmc_environment, image


def select_runtime_values(kds_environment: Mapping[str, bytes], mmc_environment: Mapping[str, bytes]) -> Tuple[bytes, bytes]:
    dsn_values = [kds_environment[name] for name in ("KDS_INTAKE_DATABASE_URL", "DATABASE_URL") if kds_environment.get(name)]
    if not dsn_values or any(value != dsn_values[0] for value in dsn_values[1:]):
        fail("runtime_values", "dsn_missing_or_ambiguous")
    validate_dsn(dsn_values[0])
    legacy_file = capture_file(KDS_LEGACY_SECRET)
    if (
        len(legacy_file.content) != EXPECTED_LEGACY_SECRET_SIZE
        or legacy_file.mode != 0o600
        or legacy_file.uid != EXPECTED_ENV_UID
        or legacy_file.gid != EXPECTED_ENV_GID
    ):
        fail("runtime_values", "legacy_secret_metadata_mismatch")
    active_secret = select_signer_secret(
        kds_environment.get("KDS_DELEGATION_SECRET"),
        mmc_environment.get("KDS_DELEGATION_SECRET"),
        legacy_file.content,
    )
    return dsn_values[0], active_secret


def execute(sealed_sha: str) -> bool:
    image: Optional[FileImage] = None
    config_mutation_started = False
    candidate = b""
    dsn = b""
    old_cutover_started = False
    old_identity: Optional[ProcessIdentity] = None
    old_transition = "not_started"
    bootstrap_attempted = False
    fresh_identity: Optional[ProcessIdentity] = None
    captured_fresh: List[ProcessIdentity] = []
    shadow: Optional[subprocess.Popen] = None
    shadow_identity: Optional[ProcessIdentity] = None
    cursor = bytearray()
    try:
        kds_environment, mmc_environment, image = hard_baseline(sealed_sha)
        old_identity = capture_process_identity(KDS_PID)
        dsn, signer_secret = select_runtime_values(kds_environment, mmc_environment)
        cursor.extend(secrets.token_urlsafe(48).encode("ascii"))
        candidate = render_config(image.content, dsn, signer_secret, bytes(cursor))
        validate_rendered_config(candidate, image.content)
        release0_expectation = RuntimeExpectation(
            "release0",
            dsn,
            hmac_json_bytes(signer_secret),
            bytes(cursor),
        )
        config_mutation_started = True
        atomic_write_image(KDS_ENV, candidate, image, expected_current=image)
        candidate_image = capture_file(KDS_ENV)
        if (
            candidate_image.content != candidate
            or candidate_image.mode != image.mode
            or candidate_image.uid != image.uid
            or candidate_image.gid != image.gid
            or candidate_image.xattrs != image.xattrs
        ):
            fail("config", "candidate_postwrite_mismatch")
        offline_verifier_roundtrip(signer_secret, bytes(cursor))
        shadow = start_shadow()
        shadow_identity = capture_process_identity(shadow.pid)
        shadow_pid = wait_listener(SHADOW_PORT, 15)
        if shadow_pid != shadow.pid:
            fail("shadow", "owner_mismatch")
        if not identity_alive(shadow_identity):
            fail("shadow", "identity_changed")
        readiness_sample(
            shadow_identity,
            SHADOW_PORT,
            release0_expectation,
            EXPECTED_SHADOW_ARGV,
            phase="shadow_readiness",
        )
        if not stop_created_child(shadow, 10, 5, "shadow"):
            fail("shadow", "known_shadow_process_remains")
        shadow.wait(timeout=1)
        require_port_free(SHADOW_PORT)
        shadow = None
        shadow_identity = None
        if listener_pids(KDS_PORT) != (KDS_PID,):
            fail("cutover", "old_owner_drift")
        old_cutover_started = True
        old_transition = stop_old_process(old_identity)
        if old_transition == "preserved":
            fail("cutover", "old_owner_preserved_after_sigterm")
        if old_transition != "exited":
            fail("cutover", "old_owner_transition_ambiguous")
        target = f"gui/{os.getuid()}"
        bootstrap_attempted = True
        result = run(("/bin/launchctl", "bootstrap", target, str(KDS_PLIST)), check=False)
        if result.returncode != 0:
            fail("cutover", "bootstrap_failed")
        fresh_identity = wait_fresh_job(captured_fresh)
        verify_fresh_sample(fresh_identity, release0_expectation)
        time.sleep(5)
        verify_fresh_sample(fresh_identity, release0_expectation)
        if git_snapshot(KDS_ROOT) != (
            EXPECTED_KDS_HEAD,
            EXPECTED_KDS_HEAD,
            0,
            0,
            0,
            *EXPECTED_KDS_STATUS,
        ) or git_snapshot(MMC_ROOT) != (
            EXPECTED_MMC_HEAD,
            EXPECTED_MMC_HEAD,
            0,
            0,
            0,
            *EXPECTED_MMC_STATUS,
        ):
            fail("final", "git_state_changed")
        bounded_result(
            "success",
            "complete",
            "release0_runtime_activated",
            fresh_pid=fresh_identity.pid,
            launchagent="active",
            readiness_samples=2,
            database_connections=0,
        )
        return True
    except BaseException as caught:
        exc = caught if isinstance(caught, GateFailure) else GateFailure("controller", "unexpected_failure")
        known_fresh = fresh_identity or (captured_fresh[0] if captured_fresh else None)

        def restore_config_hook() -> None:
            if image is None:
                fail("recovery", "config_preimage_unavailable")
            restore_file_image(KDS_ENV, image, candidate)

        def stop_shadow_hook() -> bool:
            if shadow is None:
                return True
            if not stop_created_child(shadow, 10, 5, "shadow"):
                return False
            return not listener_pids(SHADOW_PORT)

        def verify_old_hook() -> bool:
            return old_identity is not None and verify_old_owner_preserved(old_identity)

        def stop_fresh_hook() -> bool:
            return known_fresh is None or not identity_alive(known_fresh) or stop_known_process(known_fresh, 10, 5, "fresh")

        try:
            outcome = perform_recovery(
                RecoveryState(
                    config_mutated=config_mutation_started,
                    shadow_started=shadow is not None,
                    old_cutover_started=old_cutover_started,
                    old_identity_available=old_identity is not None,
                    old_transition=old_transition,
                    bootstrap_attempted=bootstrap_attempted,
                    known_fresh_available=known_fresh is not None,
                    dsn_available=bool(dsn),
                ),
                RecoveryHooks(
                    restore_config=restore_config_hook,
                    stop_shadow=stop_shadow_hook,
                    bootout_if_present=bootout_if_present,
                    verify_old_owner=verify_old_hook,
                    bootout_fresh=bootout_fresh_job,
                    stop_fresh=stop_fresh_hook,
                    owners=lambda: listener_pids(KDS_PORT),
                    manual_recovery=lambda: start_manual_recovery(dsn),
                ),
            )
        except BaseException:
            outcome = RecoveryOutcome("failed_fail_closed", "unresolved_fail_closed")
        facts: Dict[str, object] = {"recovery": outcome.recovery}
        recovery_pid = outcome.recovery_pid
        if recovery_pid is None and outcome.recovery.startswith("old_owner_") and old_identity is not None:
            recovery_pid = old_identity.pid
        if recovery_pid is not None:
            facts["recovery_pid"] = recovery_pid
        if outcome.observed_owner_count is not None:
            facts["observed_owner_count"] = outcome.observed_owner_count
        bounded_result(outcome.status, exc.step, exc.code, **facts)
        return False
    finally:
        for index in range(len(cursor)):
            cursor[index] = 0


def synthetic_procargs(argv: Sequence[str], environment: Mapping[str, bytes]) -> bytes:
    executable = argv[0].encode()
    return (
        struct.pack("=i", len(argv))
        + executable
        + b"\0\0"
        + b"\0".join(value.encode() for value in argv)
        + b"\0"
        + b"\0".join(key.encode() + b"=" + value for key, value in environment.items())
        + b"\0\0"
    )


def self_test() -> None:
    root = Path(tempfile.mkdtemp(prefix="gke001-p15r6-selftest-"))
    try:
        argv = ("/usr/bin/python3", "synthetic.py", "--flag")
        expected_environment = {"ONE": b"alpha", "TWO": b"beta=gamma"}
        blob = synthetic_procargs(argv, {**expected_environment, "UNSELECTED_SECRET": b"must-not-be-retained"})
        parsed_argv, parsed_environment = parse_procargs_blob(blob, expected_environment)
        if parsed_argv != argv or parsed_environment != expected_environment:
            fail("self_test", "procargs_parser_failed")

        def sequence(values: Sequence[object]) -> Callable[..., object]:
            iterator = iter(values)
            return lambda *args: next(iterator)

        synthetic_identity = ProcessIdentity(4242, "synthetic-start")
        transition_captured: List[ProcessIdentity] = []
        transition_argv_calls = 0

        def transition_argv(pid: int) -> Tuple[str, ...]:
            nonlocal transition_argv_calls
            transition_argv_calls += 1
            return EXPECTED_RUNNER_ARGV if transition_argv_calls == 1 else EXPECTED_KDS_ARGV

        transitioned = wait_fresh_job(
            transition_captured,
            timeout=1,
            monotonic=lambda: 0.0,
            pause=lambda delay: None,
            job_snapshot=lambda: (1, 4242),
            identity_snapshot=lambda pid: synthetic_identity,
            argv_snapshot=transition_argv,
            cwd_check=lambda pid: True,
            owners_snapshot=lambda: () if transition_argv_calls < 2 else (4242,),
        )
        if transitioned != synthetic_identity or transition_captured != [synthetic_identity]:
            fail("self_test", "fresh_exec_transition_failed")
        bind_transition_captured: List[ProcessIdentity] = []
        bind_transitioned = wait_fresh_job(
            bind_transition_captured,
            timeout=1,
            monotonic=lambda: 0.0,
            pause=lambda delay: None,
            job_snapshot=lambda: (1, 4242),
            identity_snapshot=lambda pid: synthetic_identity,
            argv_snapshot=sequence((EXPECTED_RUNNER_ARGV, EXPECTED_KDS_ARGV)),
            cwd_check=lambda pid: True,
            owners_snapshot=lambda: (4242,),
        )
        if bind_transitioned != synthetic_identity or bind_transition_captured != [synthetic_identity]:
            fail("self_test", "fresh_exec_bind_transition_failed")

        def expect_fresh_gate(code: str, callback: Callable[[], object]) -> None:
            try:
                callback()
            except GateFailure as exc:
                if exc.code != code:
                    fail("self_test", "fresh_exec_wrong_failure")
            else:
                fail("self_test", "fresh_exec_gate_not_enforced")

        expect_fresh_gate(
            "fresh_job_start_timeout",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=sequence((0.0, 2.0)),
                pause=lambda delay: None,
            ),
        )
        expect_fresh_gate(
            "fresh_process_identity_changed",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=sequence(((1, 4242), (1, 4243))),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=lambda pid: EXPECTED_RUNNER_ARGV,
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (),
            ),
        )
        expect_fresh_gate(
            "fresh_process_identity_changed",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=sequence(
                    (
                        synthetic_identity,
                        synthetic_identity,
                        ProcessIdentity(4242, "replacement-start"),
                    )
                ),
                argv_snapshot=lambda pid: EXPECTED_KDS_ARGV,
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (4242,),
            ),
        )
        expect_fresh_gate(
            "fresh_process_argv_regressed",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=sequence((EXPECTED_KDS_ARGV, EXPECTED_RUNNER_ARGV)),
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (),
            ),
        )
        expect_fresh_gate(
            "fresh_process_argv_mismatch",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=lambda pid: ("/bin/zsh", "/tmp/unsealed-runner.sh"),
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (),
            ),
        )
        expect_fresh_gate(
            "runner_bound_listener",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=lambda pid: EXPECTED_RUNNER_ARGV,
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (4242,),
            ),
        )

        def argv_with_transient(
            transient_code: str,
        ) -> Tuple[Callable[[int], Tuple[str, ...]], List[str]]:
            values: List[object] = [
                GateFailure("procargs", transient_code),
                EXPECTED_KDS_ARGV,
                EXPECTED_KDS_ARGV,
            ]
            calls: List[str] = []

            def sample(pid: int) -> Tuple[str, ...]:
                calls.append(transient_code)
                value = values.pop(0)
                if isinstance(value, BaseException):
                    raise value
                return value

            return sample, calls

        size_transient_argv, size_transient_calls = argv_with_transient("size_query_failed")
        if wait_fresh_job(
            [],
            timeout=1,
            monotonic=lambda: 0.0,
            pause=lambda delay: None,
            job_snapshot=lambda: (1, 4242),
            identity_snapshot=lambda pid: synthetic_identity,
            argv_snapshot=size_transient_argv,
            cwd_check=lambda pid: True,
            owners_snapshot=lambda: (4242,),
        ) != synthetic_identity or len(size_transient_calls) != 3:
            fail("self_test", "fresh_size_query_transition_failed")

        read_transient_argv, read_transient_calls = argv_with_transient("read_failed")
        if wait_fresh_job(
            [],
            timeout=1,
            monotonic=lambda: 0.0,
            pause=lambda delay: None,
            job_snapshot=lambda: (1, 4242),
            identity_snapshot=lambda pid: synthetic_identity,
            argv_snapshot=read_transient_argv,
            cwd_check=lambda pid: True,
            owners_snapshot=lambda: (4242,),
        ) != synthetic_identity or len(read_transient_calls) != 3:
            fail("self_test", "fresh_read_query_transition_failed")

        expect_fresh_gate(
            "fresh_wait_procargs_timeout",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=sequence((0.0, 0.0, 0.0, 2.0)),
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=lambda pid: (_ for _ in ()).throw(
                    GateFailure("procargs", "size_query_failed")
                ),
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (4242,),
            ),
        )
        expect_fresh_gate(
            "fresh_process_identity_changed",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=sequence(
                    (
                        synthetic_identity,
                        synthetic_identity,
                        ProcessIdentity(4242, "replacement-start"),
                    )
                ),
                argv_snapshot=lambda pid: (_ for _ in ()).throw(
                    GateFailure("procargs", "read_failed")
                ),
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (4242,),
            ),
        )
        expect_fresh_gate(
            "unknown_listener_owner",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=lambda pid: (_ for _ in ()).throw(
                    GateFailure("procargs", "size_query_failed")
                ),
                cwd_check=lambda pid: True,
                owners_snapshot=sequence(((), (9999,))),
            ),
        )
        expect_fresh_gate(
            "fresh_process_cwd_changed",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=lambda pid: (_ for _ in ()).throw(
                    GateFailure("procargs", "read_failed")
                ),
                cwd_check=sequence((True, False)),
                owners_snapshot=lambda: (4242,),
            ),
        )
        non_procargs_calls: List[str] = []

        def non_procargs_failure(pid: int) -> Tuple[str, ...]:
            non_procargs_calls.append("called")
            fail("cutover", "non_procargs_gate_failure")
            raise AssertionError

        expect_fresh_gate(
            "non_procargs_gate_failure",
            lambda: wait_fresh_job(
                [],
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                job_snapshot=lambda: (1, 4242),
                identity_snapshot=lambda pid: synthetic_identity,
                argv_snapshot=non_procargs_failure,
                cwd_check=lambda pid: True,
                owners_snapshot=lambda: (4242,),
            ),
        )
        if non_procargs_calls != ["called"]:
            fail("self_test", "non_procargs_gate_retried")
        controlled_entry = root / "controlled-entry.txt"
        controlled_entry.write_bytes(b"sealed-controlled-entry\n")
        controlled_manifest = (
            (
                "controlled-entry.txt",
                hashlib.sha256(controlled_entry.read_bytes()).hexdigest(),
            ),
        )
        validate_controlled_entry_hashes(root, controlled_manifest)

        def expect_controlled_gate(code: str, manifest: Sequence[Tuple[str, str]]) -> None:
            try:
                validate_controlled_entry_hashes(root, manifest)
            except GateFailure as exc:
                if exc.code != code:
                    fail("self_test", "controlled_entry_wrong_failure")
            else:
                fail("self_test", "controlled_entry_gate_not_enforced")

        controlled_entry.write_bytes(b"drifted-controlled-entry\n")
        expect_controlled_gate("controlled_entry_hash_mismatch", controlled_manifest)
        expect_controlled_gate(
            "controlled_entry_missing",
            (("missing-controlled-entry.txt", hashlib.sha256(b"missing").hexdigest()),),
        )
        controlled_symlink = root / "controlled-entry-link"
        controlled_symlink.symlink_to(controlled_entry)
        expect_controlled_gate(
            "controlled_entry_type_mismatch",
            ((controlled_symlink.name, hashlib.sha256(controlled_entry.read_bytes()).hexdigest()),),
        )
        hardlink_source = root / "controlled-hardlink-source"
        hardlink_target = root / "controlled-hardlink-target"
        hardlink_source.write_bytes(b"hardlinked-controlled-entry\n")
        os.link(str(hardlink_source), str(hardlink_target))
        expect_controlled_gate(
            "controlled_entry_type_mismatch",
            ((hardlink_target.name, hashlib.sha256(hardlink_target.read_bytes()).hexdigest()),),
        )
        controlled_directory = root / "controlled-entry-directory"
        controlled_directory.mkdir()
        expect_controlled_gate(
            "controlled_entry_type_mismatch",
            ((controlled_directory.name, hashlib.sha256(b"directory").hexdigest()),),
        )
        config = root / "synthetic.env"
        config.write_bytes(b"BASE=synthetic\n")
        os.chmod(str(config), 0o600)
        synthetic_xattr = "com.globalcloud.gke001.synthetic"
        synthetic_value = b"synthetic-xattr-value"
        write_xattrs(config, {synthetic_xattr: synthetic_value})
        image = capture_file(config)
        if image.xattrs.get(synthetic_xattr) != synthetic_value:
            fail("self_test", "xattr_px_failed")
        candidate = render_config(
            image.content,
            b"postgresql://synthetic@127.0.0.1:5432/gke001_synthetic_local",
            b"synthetic-signer-secret-at-least-thirty-two-bytes",
            b"synthetic-cursor-secret-at-least-thirty-two-bytes",
        )
        validate_rendered_config(candidate, image.content)
        if b"PYTHONDONTWRITEBYTECODE=1" not in candidate or b"PYTHONDWRITEBYTECODE=" in candidate:
            fail("self_test", "render_key_failed")
        rejected = candidate.replace(b"PYTHONDONTWRITEBYTECODE", b"PYTHONDWRITEBYTECODE", 1)
        try:
            validate_rendered_config(rejected, image.content)
        except GateFailure:
            pass
        else:
            fail("self_test", "typo_not_rejected")
        atomic_write_image(config, candidate, image, expected_current=image)
        if config.read_bytes() != candidate or read_xattrs(config) != image.xattrs:
            fail("self_test", "atomic_replace_failed")
        restore_file_image(config, image, candidate)
        restored = capture_file(config)
        if restored.content != image.content or restored.mode != image.mode or restored.xattrs != image.xattrs:
            fail("self_test", "atomic_restore_failed")
        symlink = root / "synthetic-secret-link"
        symlink.symlink_to(config)
        try:
            capture_file(symlink)
        except GateFailure:
            pass
        else:
            fail("self_test", "same_fd_nofollow_failed")
        if normalize_secret(b"  synthetic-secret-at-least-thirty-two-bytes\n") != b"synthetic-secret-at-least-thirty-two-bytes":
            fail("self_test", "secret_normalization_failed")
        synthetic_signer = b"synthetic-secret-at-least-thirty-two-bytes"
        if select_signer_secret(None, synthetic_signer, synthetic_signer + b"\n") != synthetic_signer:
            fail("self_test", "missing_legacy_process_secret_not_accepted")
        if select_signer_secret(synthetic_signer, synthetic_signer, synthetic_signer + b"\n") != synthetic_signer:
            fail("self_test", "matching_legacy_process_secret_not_accepted")
        for legacy_process_raw, active_process_raw, legacy_file_raw in (
            (None, synthetic_signer, b"different-synthetic-secret-at-least-thirty-two-bytes\n"),
            (b"different-synthetic-secret-at-least-thirty-two-bytes", synthetic_signer, synthetic_signer + b"\n"),
        ):
            try:
                select_signer_secret(legacy_process_raw, active_process_raw, legacy_file_raw)
            except GateFailure as exc:
                if exc.code != "signer_secret_mismatch":
                    fail("self_test", "signer_secret_mismatch_wrong_failure")
            else:
                fail("self_test", "signer_secret_mismatch_not_rejected")
        release0_environment = {
            "PYTHONDONTWRITEBYTECODE": b"1",
            "KDS_INTAKE_DATABASE_URL": b"postgresql://synthetic@127.0.0.1:5432/gbrain",
            "KDS_INTAKE_HMAC_KEYS_JSON": b'{"studio":"synthetic-secret-at-least-thirty-two-bytes"}',
            "KDS_KNOWLEDGE_READ_CURSOR_SECRET": b"synthetic-cursor-secret-at-least-thirty-two-bytes",
            "KDS_INTAKE_DELEGATION_ISSUER": b"mmc",
            "KDS_INTAKE_DELEGATION_AUDIENCE": b"kds-knowledge-intake",
        }
        release0_expectation = RuntimeExpectation(
            "release0",
            release0_environment["KDS_INTAKE_DATABASE_URL"],
            release0_environment["KDS_INTAKE_HMAC_KEYS_JSON"],
            release0_environment["KDS_KNOWLEDGE_READ_CURSOR_SECRET"],
        )
        validate_runtime_environment_mapping(release0_environment, release0_expectation)
        incomplete_environment = dict(release0_environment)
        del incomplete_environment["KDS_KNOWLEDGE_READ_CURSOR_SECRET"]
        try:
            validate_runtime_environment_mapping(incomplete_environment, release0_expectation)
        except GateFailure:
            pass
        else:
            fail("self_test", "release0_environment_gap_not_rejected")
        validate_runtime_environment_mapping(
            {"DATABASE_URL": release0_environment["KDS_INTAKE_DATABASE_URL"]},
            RuntimeExpectation("legacy", release0_environment["KDS_INTAKE_DATABASE_URL"]),
        )

        def transient_environment_snapshot(
            transient_code: str,
            environment: Mapping[str, bytes],
        ) -> Tuple[
            Callable[[int, Path, Iterable[str]], Tuple[Tuple[str, ...], Dict[str, bytes], int, str]],
            List[str],
        ]:
            values: List[object] = [
                GateFailure("procargs", transient_code),
                (EXPECTED_KDS_ARGV, dict(environment), 1, synthetic_identity.start),
            ]
            calls: List[str] = []

            def sample(
                pid: int,
                expected_cwd: Path,
                selected_keys: Iterable[str],
            ) -> Tuple[Tuple[str, ...], Dict[str, bytes], int, str]:
                calls.append(transient_code)
                value = values.pop(0)
                if isinstance(value, BaseException):
                    raise value
                return value

            return sample, calls

        fresh_environment_snapshot, fresh_environment_calls = transient_environment_snapshot(
            "read_failed",
            release0_environment,
        )
        verify_runtime_environment(
            synthetic_identity,
            KDS_PORT,
            release0_expectation,
            EXPECTED_KDS_ARGV,
            phase="fresh_readiness",
            job_bound=True,
            timeout=1,
            monotonic=lambda: 0.0,
            pause=lambda delay: None,
            snapshot=fresh_environment_snapshot,
            identity_check=lambda: True,
            cwd_check=lambda: True,
            owners_snapshot=lambda: (synthetic_identity.pid,),
            job_snapshot=lambda: (1, synthetic_identity.pid),
        )
        if len(fresh_environment_calls) != 2:
            fail("self_test", "fresh_readiness_procargs_retry_failed")

        legacy_environment = {
            "DATABASE_URL": release0_environment["KDS_INTAKE_DATABASE_URL"],
        }
        legacy_expectation = RuntimeExpectation("legacy", legacy_environment["DATABASE_URL"])
        manual_environment_snapshot, manual_environment_calls = transient_environment_snapshot(
            "size_query_failed",
            legacy_environment,
        )
        verify_runtime_environment(
            synthetic_identity,
            KDS_PORT,
            legacy_expectation,
            EXPECTED_KDS_ARGV,
            phase="manual_recovery",
            timeout=1,
            monotonic=lambda: 0.0,
            pause=lambda delay: None,
            snapshot=manual_environment_snapshot,
            identity_check=lambda: True,
            cwd_check=lambda: True,
            owners_snapshot=lambda: (synthetic_identity.pid,),
        )
        if len(manual_environment_calls) != 2:
            fail("self_test", "manual_recovery_procargs_retry_failed")

        expect_fresh_gate(
            "manual_recovery_procargs_timeout",
            lambda: verify_runtime_environment(
                synthetic_identity,
                KDS_PORT,
                legacy_expectation,
                EXPECTED_KDS_ARGV,
                phase="manual_recovery",
                timeout=1,
                monotonic=sequence((0.0, 0.0, 2.0)),
                pause=lambda delay: None,
                snapshot=lambda pid, expected_cwd, selected: (_ for _ in ()).throw(
                    GateFailure("procargs", "read_failed")
                ),
                identity_check=lambda: True,
                cwd_check=lambda: True,
                owners_snapshot=lambda: (synthetic_identity.pid,),
            ),
        )
        expect_fresh_gate(
            "fresh_readiness_argv_mismatch",
            lambda: verify_runtime_environment(
                synthetic_identity,
                KDS_PORT,
                release0_expectation,
                EXPECTED_KDS_ARGV,
                phase="fresh_readiness",
                job_bound=True,
                timeout=1,
                monotonic=lambda: 0.0,
                pause=lambda delay: None,
                snapshot=lambda pid, expected_cwd, selected: (
                    EXPECTED_RUNNER_ARGV,
                    dict(release0_environment),
                    1,
                    synthetic_identity.start,
                ),
                identity_check=lambda: True,
                cwd_check=lambda: True,
                owners_snapshot=lambda: (synthetic_identity.pid,),
                job_snapshot=lambda: (1, synthetic_identity.pid),
            ),
        )

        valid_schema = {
            "paths": {
                "/api/v1/knowledge-read/release-0/search": {
                    "post": {"operationId": "kdsCanonicalKnowledgeSearch"}
                },
                "/api/v1/knowledge-read/release-0/read": {
                    "post": {"operationId": "kdsCanonicalKnowledgeRead"}
                },
            }
        }

        def terminal_readiness_fixture(
            terminal_argv: Tuple[str, ...] = EXPECTED_KDS_ARGV,
            terminal_owners: Tuple[int, ...] = (synthetic_identity.pid,),
            terminal_transient: Optional[GateFailure] = None,
        ) -> Tuple[Callable[[], None], Callable[[int, str], object], Callable[[], Tuple[int, ...]], List[str]]:
            state: Dict[str, object] = {
                "argv": EXPECTED_KDS_ARGV,
                "owners": (synthetic_identity.pid,),
                "transient": None,
            }
            events: List[str] = []

            def snapshot(
                pid: int,
                expected_cwd: Path,
                selected_keys: Iterable[str],
            ) -> Tuple[Tuple[str, ...], Dict[str, bytes], int, str]:
                transient = state["transient"]
                if isinstance(transient, GateFailure):
                    state["transient"] = None
                    raise transient
                return (
                    state["argv"],
                    dict(release0_environment),
                    1,
                    synthetic_identity.start,
                )

            def owners() -> Tuple[int, ...]:
                return state["owners"]

            def attestation() -> None:
                events.append("attest")
                verify_runtime_environment(
                    synthetic_identity,
                    KDS_PORT,
                    release0_expectation,
                    EXPECTED_KDS_ARGV,
                    phase="fresh_readiness",
                    job_bound=True,
                    timeout=1,
                    monotonic=lambda: 0.0,
                    pause=lambda delay: None,
                    snapshot=snapshot,
                    identity_check=lambda: True,
                    cwd_check=lambda: True,
                    owners_snapshot=owners,
                    job_snapshot=lambda: (1, synthetic_identity.pid),
                )

            def http_get(port: int, path: str) -> object:
                events.append(path)
                if path == "/api/v1/health":
                    return {"status": "ok"}
                if path == "/openapi.json":
                    state["argv"] = terminal_argv
                    state["owners"] = terminal_owners
                    state["transient"] = terminal_transient
                    return valid_schema
                fail("self_test", "terminal_readiness_unexpected_path")
                raise AssertionError

            return attestation, http_get, owners, events

        for terminal_argv in (
            EXPECTED_RUNNER_ARGV,
            ("/bin/zsh", "/tmp/unsealed-runner.sh"),
        ):
            attestation, http_get, owners, events = terminal_readiness_fixture(
                terminal_argv=terminal_argv,
            )
            expect_fresh_gate(
                "fresh_readiness_argv_mismatch",
                lambda attestation=attestation, http_get=http_get, owners=owners: readiness_sample(
                    synthetic_identity,
                    KDS_PORT,
                    release0_expectation,
                    EXPECTED_KDS_ARGV,
                    phase="fresh_readiness",
                    job_bound=True,
                    attest=attestation,
                    owners_snapshot=owners,
                    http_get=http_get,
                    database_connections=lambda pid, events=events: (events.append("db") or 0),
                ),
            )
            if events != ["attest", "/api/v1/health", "/openapi.json", "db", "attest"]:
                fail("self_test", "terminal_argv_attestation_order_failed")

        attestation, http_get, owners, events = terminal_readiness_fixture(
            terminal_owners=(9999,),
        )
        expect_fresh_gate(
            "fresh_readiness_listener_owner_mismatch",
            lambda: readiness_sample(
                synthetic_identity,
                KDS_PORT,
                release0_expectation,
                EXPECTED_KDS_ARGV,
                phase="fresh_readiness",
                job_bound=True,
                attest=attestation,
                owners_snapshot=owners,
                http_get=http_get,
                database_connections=lambda pid: (events.append("db") or 0),
            ),
        )
        if events != ["attest", "/api/v1/health", "/openapi.json", "db", "attest"]:
            fail("self_test", "terminal_listener_attestation_order_failed")

        attestation, http_get, owners, events = terminal_readiness_fixture(
            terminal_transient=GateFailure("procargs", "read_failed"),
        )
        readiness_sample(
            synthetic_identity,
            KDS_PORT,
            release0_expectation,
            EXPECTED_KDS_ARGV,
            phase="fresh_readiness",
            job_bound=True,
            attest=attestation,
            owners_snapshot=owners,
            http_get=http_get,
            database_connections=lambda pid: (events.append("db") or 0),
        )
        if events != ["attest", "/api/v1/health", "/openapi.json", "db", "attest"]:
            fail("self_test", "terminal_procargs_recovery_order_failed")
        manual_environment = manual_recovery_environment(
            {
                "KDS_INTAKE_DATABASE_URL": "poisoned",
                "KDS_INTAKE_HMAC_KEYS_JSON": "poisoned",
                "KDS_KNOWLEDGE_READ_CURSOR_SECRET": "poisoned",
                "UNCHANGED": "synthetic",
            },
            release0_environment["KDS_INTAKE_DATABASE_URL"],
        )
        if (
            any(name in manual_environment for name in TARGET_ENV_KEYS[1:])
            or manual_environment.get("DATABASE_URL") != release0_environment["KDS_INTAKE_DATABASE_URL"].decode()
            or manual_environment.get("UNCHANGED") != "synthetic"
        ):
            fail("self_test", "manual_environment_sanitization_failed")
        for forbidden_kind in ("old", "unknown"):
            try:
                stop_known_process(ProcessIdentity(-1, "synthetic"), 0, 0, forbidden_kind)
            except GateFailure:
                pass
            else:
                fail("self_test", "forbidden_signal_target_accepted")
        def injected_recovery(
            state: RecoveryState,
            *,
            owners: Tuple[int, ...] = (),
            restore_failure: bool = False,
            manual_failure: bool = False,
        ) -> Tuple[RecoveryOutcome, List[str]]:
            actions: List[str] = []

            def record(name: str, result: bool = True) -> bool:
                actions.append(name)
                return result

            def restore() -> None:
                actions.append("restore_config")
                if restore_failure:
                    raise RuntimeError("synthetic_restore_failure")

            def manual() -> Tuple[str, Optional[int]]:
                actions.append("manual_recovery")
                if manual_failure:
                    raise RuntimeError("synthetic_manual_failure")
                return "manual_single_owner_restored_launchagent_booted_out", 4242

            outcome = perform_recovery(
                state,
                RecoveryHooks(
                    restore_config=restore,
                    stop_shadow=lambda: record("stop_shadow"),
                    bootout_if_present=lambda: record("bootout_if_present") and None,
                    verify_old_owner=lambda: record("verify_old_owner"),
                    bootout_fresh=lambda: record("bootout_fresh"),
                    stop_fresh=lambda: record("stop_fresh"),
                    owners=lambda: (actions.append("owners") or owners),
                    manual_recovery=manual,
                ),
            )
            return outcome, actions

        baseline_stop, baseline_actions = injected_recovery(
            RecoveryState(False, False, False, False, "not_started", False, False, False)
        )
        if baseline_stop.recovery != "hard_baseline_stopped_before_mutation" or baseline_actions:
            fail("self_test", "hard_baseline_fail_stop_injection_failed")
        config_fault, config_actions = injected_recovery(
            RecoveryState(True, False, False, True, "not_started", False, False, True)
        )
        if config_fault.status != "failed_recovered" or config_actions[:2] != ["restore_config", "bootout_if_present"]:
            fail("self_test", "config_write_fault_injection_failed")
        old_timeout, old_actions = injected_recovery(
            RecoveryState(True, False, True, True, "preserved", False, False, True)
        )
        if old_timeout.status != "failed_recovered" or old_actions != ["restore_config", "verify_old_owner"]:
            fail("self_test", "old_timeout_fault_injection_failed")
        unknown_owner, unknown_actions = injected_recovery(
            RecoveryState(True, False, True, True, "exited", False, False, True),
            owners=(99999,),
        )
        if (
            unknown_owner.recovery != "unknown_owner_remains_no_second_owner"
            or "manual_recovery" in unknown_actions
            or "stop_fresh" in unknown_actions
        ):
            fail("self_test", "unknown_owner_fault_injection_failed")
        replacement, replacement_actions = injected_recovery(
            RecoveryState(True, False, True, True, "exited", True, True, True)
        )
        if (
            replacement.status != "failed_recovered"
            or replacement_actions != ["restore_config", "bootout_fresh", "stop_fresh", "owners", "manual_recovery"]
        ):
            fail("self_test", "replacement_restart_fault_injection_failed")
        manual_failure, manual_actions = injected_recovery(
            RecoveryState(False, False, True, True, "exited", False, False, True),
            manual_failure=True,
        )
        if (
            manual_failure.recovery != "manual_recovery_exception_no_retry"
            or manual_actions.count("manual_recovery") != 1
        ):
            fail("self_test", "manual_failure_fault_injection_failed")
        restore_failure, restore_actions = injected_recovery(
            RecoveryState(True, True, True, True, "exited", True, True, True),
            restore_failure=True,
        )
        if (
            restore_failure.recovery != "config_restore_unresolved_no_manual_recovery"
            or restore_actions[:3] != ["restore_config", "stop_shadow", "bootout_fresh"]
            or "stop_fresh" not in restore_actions
            or "manual_recovery" in restore_actions
        ):
            fail("self_test", "restore_failure_cleanup_injection_failed")
        for process_kind in ("shadow", "manual"):
            child = subprocess.Popen(
                (sys.executable, "-c", "import time; time.sleep(60)"),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if not stop_created_child(child, 1, 1, process_kind) or child.poll() is None:
                fail("self_test", "created_child_cleanup_failed")
        bounded_result(
            "pass",
            "self_test",
            "synthetic_controller_self_test_passed",
            procargs_parser=True,
            selected_environment_filter=True,
            fresh_exec_transition=True,
            fresh_exec_bind_transition=True,
            fresh_exec_timeout=True,
            fresh_exec_restart_rejection=True,
            fresh_exec_final_identity_recheck=True,
            fresh_exec_regression_rejection=True,
            fresh_exec_wrong_argv_rejection=True,
            runner_listener_rejection=True,
            fresh_procargs_size_retry=True,
            fresh_procargs_read_retry=True,
            fresh_procargs_timeout=True,
            fresh_procargs_identity_replacement_rejection=True,
            fresh_procargs_unknown_listener_rejection=True,
            fresh_procargs_cwd_replacement_rejection=True,
            non_procargs_gate_not_retried=True,
            fresh_readiness_procargs_retry=True,
            readiness_exact_argv=True,
            readiness_terminal_argv_rejection=True,
            readiness_terminal_listener_rejection=True,
            readiness_terminal_procargs_recovery=True,
            readiness_terminal_attestation_order=True,
            manual_recovery_procargs_retry=True,
            manual_recovery_procargs_timeout=True,
            controlled_entry_hash_gate=True,
            controlled_entry_missing_rejection=True,
            controlled_entry_symlink_rejection=True,
            controlled_entry_hardlink_rejection=True,
            controlled_entry_nonregular_rejection=True,
            four_key_render=True,
            typo_rejection=True,
            xattr_px_wx=True,
            atomic_replace_restore=True,
            same_fd_nofollow=True,
            strict_secret_normalization=True,
            missing_legacy_process_secret=True,
            signer_secret_continuity=True,
            runtime_environment_readiness=True,
            manual_environment_sanitization=True,
            forbidden_signal_targets=True,
            state_machine_fault_injection=True,
            created_child_lifecycle=True,
            restore_failure_cleanup=True,
            hard_baseline_fail_stop=True,
        )
    finally:
        shutil.rmtree(str(root), ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--sealed-sha", default="")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            self_test()
            return 0
        if not arguments.sealed_sha:
            fail("authorization", "sealed_sha_required")
        return 0 if execute(arguments.sealed_sha) else 1
    except GateFailure as exc:
        bounded_result("failed_fail_closed", exc.step, exc.code, recovery="not_started_or_synthetic_cleanup")
        return 1
    except BaseException:
        bounded_result("failed_fail_closed", "controller", "unexpected_failure", recovery="no_hotfix_no_continuation")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
