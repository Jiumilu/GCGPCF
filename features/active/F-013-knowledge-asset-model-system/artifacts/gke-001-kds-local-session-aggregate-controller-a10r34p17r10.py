#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


CONTROL_ID = "GKE-001-COORDINATION-20260820-004-A10R34P17R10"
RUN_ID = "gke001-a10r34p17r10-kds-session-aggregate"
CHANGE_ID = "repair-kds-session-aggregate-external-lock-contract-a10r34p17r10"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
R9_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-session-aggregate-controller-a10r34p17r9.py"
R9_CONTROLLER_SHA256 = "2ee3c779cd4e55571ed091e2180f7374e8cc71ae17e916808e6a985a9c9761fa"

SEALED_BASELINES = {
    "gpcf": {"head": "a317eeaab451920bc4bbbea904ca1c2bc774a497", "origin": "8deda915579b915d7496f20b2e4ecb5475491c40", "ahead": 1, "behind": 0, "ordinary_count": 13, "ordinary_sha256": "c55927f86f0e7effe6de03428631b02713c09a1329035a890a47f355f98e61e9", "expanded_count": 13, "expanded_sha256": "c55927f86f0e7effe6de03428631b02713c09a1329035a890a47f355f98e61e9"},
    "kds": {"head": "2ac85c55163b7acf0ede699184ac360579ccefaa", "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa", "ahead": 0, "behind": 0, "ordinary_count": 373, "ordinary_sha256": "4677fcccdf92696d134e276bc19692403f57f5151c3026670950b8f2ded7760b", "expanded_count": 703, "expanded_sha256": "5a7325cd54c9eed1c89fcc9e5540065b68cc61ed7c2399fdddbe761534b46f77"},
    "mmc": {"head": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7", "origin": "2dd7954fa4826120d68d42bd8f3c30e8d9ead99b", "ahead": 3, "behind": 0, "ordinary_count": 0, "ordinary_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "expanded_count": 0, "expanded_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
}

SEALED_EXTERNAL_FILES = (
    ("工业绿链/reports/Hermes质量周报.md", "068f95eaef8d1bd96c9060a679cd8fc1a9e9d16098d57b73cd1f9815f300d362"),
    ("工业绿链/reports/项目复盘知识归档报告.md", "b062727cd3bc294e2e0ad11b75c44eab94a1e07003446afd632fc2abe5fd36a0"),
    ("工业绿链/reports/项目监控仪表盘.md", "ef33ce6cbd1dacf391985bb88b31f22b238d9ec27fa4a3c61790399b5df5e3d9"),
    ("工业绿链/体系/W01-W20第二阶段任务清单.md", "08040c809ced18708e349a626cb295840f3369192125cc287f49b36f21f63812"),
    ("工业绿链/体系/W01-W20覆盖率报告.md", "7bcee42c2316eed4adab01e9962e36556c29bc11dcf263eb1e50e0154a591552"),
    ("工业绿链/体系/meeting-quality-gate_2026-08-16.json", "900fafe508c27804d531077afba34f132b667ed5edff024b2eec591687521391"),
    ("工业绿链/体系/会议质量门禁阻断清单_2026-08-16.md", "8f5c47d808f9d72e5bfeb8d4e4c2c44057060ce969cdb5711d025870f0344ec2"),
    ("工业绿链/体系/老卢工作体系健康检查_2026-08-16.md", "2a9dc8a937436696f1de7a8c0b53b65a78bd223ebac547bab0167b1eca4036fa"),
    ("工业绿链/变更告警_2026-08-16.md", "e7127e492342d34ebacd5686bfe5b7d089db9c60bf1d9d10e1a226e2ac557b3a"),
    ("工业绿链/周报/周报_2026W33.md", "40aa36b89767043f9482f7c081518fd26d1a629d514993326b09d49fdcd28409"),
    ("工业绿链/日报/晨报-2026-08-16.md", "17878591de8bf528d422fbeb49bc59129f2d75661c908d3d3fe1df2187d3b63e"),
    ("工业绿链/月报/月报_2026-08.md", "10ef0a8f7f887481911535fe1794bd6af7885e61d17392e8e422dd3f0cabcd46"),
)
SEALED_EXTERNAL_MANIFEST_SHA256 = "c00c3c96320bb78f0ca626ea92a5f14b50d6028cbcef6d545a5456ea03ca148b"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_r9() -> Any:
    if digest(R9_CONTROLLER.read_bytes()) != R9_CONTROLLER_SHA256:
        raise RuntimeError("r9_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r10_r9", R9_CONTROLLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("r9_controller_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.SEALED_BASELINES = SEALED_BASELINES
    return module


def fail(base: Any, code: str) -> None:
    base.fail("baseline", code)


def check_exact_repo(r9: Any, base: Any, name: str, root: Path, *, own_lock_expected: bool = False) -> None:
    values = SEALED_BASELINES[name]
    if base.run(("/usr/bin/git", "branch", "--show-current"), cwd=root).stdout.strip() != b"main":
        fail(base, f"{root.name}_branch")
    for ref, expected in (("HEAD", values["head"]), ("origin/main", values["origin"])):
        if base.run(("/usr/bin/git", "rev-parse", ref), cwd=root).stdout.decode().strip() != expected:
            fail(base, f"{root.name}_{ref}")
    r9.exact_divergence(base, root, (values["ahead"], values["behind"]))
    if base.run(("/usr/bin/git", "diff", "--cached", "--name-only"), cwd=root).stdout:
        fail(base, f"{root.name}_staged")
    allow_own_lock = own_lock_expected and root == GPCF_ROOT
    if base.git_status(root, False, allow_own_lock=allow_own_lock) != (values["ordinary_count"], values["ordinary_sha256"]):
        fail(base, f"{root.name}_ordinary_dirty")
    if base.git_status(root, True, allow_own_lock=allow_own_lock) != (values["expanded_count"], values["expanded_sha256"]):
        fail(base, f"{root.name}_expanded_dirty")
    if allow_own_lock:
        base.check_own_lock()
    elif (root / ".harness/opsx.lock").exists() or (root == GPCF_ROOT and base.ATOMIC_GUARD.exists()):
        fail(base, f"{root.name}_opsx_lock")


def check_external_files(base: Any) -> None:
    records = bytearray()
    for relative_path, expected_sha256 in SEALED_EXTERNAL_FILES:
        path = KDS_ROOT / relative_path
        descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                fail(base, "sealed_external_file_type")
            hasher = hashlib.sha256()
            while chunk := os.read(descriptor, 1024 * 1024):
                hasher.update(chunk)
            completed = os.fstat(descriptor)
            opening_identity = (opened.st_mode, opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns)
            completed_identity = (completed.st_mode, completed.st_dev, completed.st_ino, completed.st_size, completed.st_mtime_ns, completed.st_ctime_ns)
            if opening_identity != completed_identity:
                fail(base, "sealed_external_file_mutated")
            current = path.lstat()
            current_identity = (current.st_mode, current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns, current.st_ctime_ns)
            if not stat.S_ISREG(current.st_mode) or completed_identity != current_identity:
                fail(base, "sealed_external_file_replaced")
            actual_sha256 = hasher.hexdigest()
        finally:
            os.close(descriptor)
        if actual_sha256 != expected_sha256:
            fail(base, "sealed_external_file_content")
        records.extend(f"{actual_sha256}  {relative_path}\n".encode("utf-8"))
    if digest(bytes(records)) != SEALED_EXTERNAL_MANIFEST_SHA256:
        fail(base, "sealed_external_content_manifest")


def hard_baseline(r9: Any, base: Any, *, own_lock_expected: bool = False) -> str:
    check_exact_repo(r9, base, "gpcf", GPCF_ROOT, own_lock_expected=own_lock_expected)
    check_exact_repo(r9, base, "kds", KDS_ROOT)
    check_external_files(base)
    check_exact_repo(r9, base, "mmc", MMC_ROOT)
    base.validate_runtime()
    for name, path in base.OFFICIAL_LOCK_HELPERS.items():
        if digest(path.read_bytes()) != base.SEALED_OFFICIAL_LOCK_HELPERS[name]:
            base.fail("lock", f"official_{name}_helper_drift")
    return base.read_secure_environment()


def terminal(r9: Any, status: str, code: str, **extra: Any) -> dict[str, Any]:
    return r9.terminal(status, code, **extra) | {"control": CONTROL_ID}


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r9, base, acquired = load_r9(), None, False
    result: dict[str, Any] = {"status": "stopped_no_change", "code": "not_started", "control": CONTROL_ID}
    try:
        base = r9.load_base()
        base.CONTROL_ID, base.RUN_ID, base.CHANGE_ID = CONTROL_ID, RUN_ID, CHANGE_ID
        dsn = hard_baseline(r9, base)
        outcome = base.lock_helper_acquire()
        if not outcome.get("acquired"):
            result = terminal(r9, "stopped_no_change", "lock_not_acquired")
        else:
            acquired = True
            dsn = hard_baseline(r9, base, own_lock_expected=True)
            result = r9.load_r8().aggregate_sessions(dsn, base) | {"control": CONTROL_ID}
    except Exception as error:
        if base is not None and isinstance(error, base.ControlledFailure):
            result = terminal(r9, "stopped_no_change", error.code, step=error.step)
        else:
            result = terminal(r9, "stopped_no_change", type(error).__name__)
    finally:
        if base is not None and acquired:
            released = base.lock_helper_release()
            result["opsx_lock_released"] = bool(released.get("released"))
            if not result["opsx_lock_released"]:
                result["status"], result["code"] = "failed_fail_closed", "lock_release_unresolved"
        elif base is not None:
            result["opsx_lock_released"] = not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists()
    return result


def self_test() -> dict[str, Any]:
    r9 = load_r9()
    assert digest("".join(f"{digest_value}  {path}\n" for path, digest_value in SEALED_EXTERNAL_FILES).encode()) == SEALED_EXTERNAL_MANIFEST_SHA256
    source = Path(__file__).read_text(encoding="utf-8")
    assert "O_NOFOLLOW" in source
    fstat_call = "os.fstat" + "(descriptor)"
    assert source.count(fstat_call) == 2
    assert "st_mtime_ns" in source and "st_ctime_ns" in source
    assert SEALED_BASELINES["gpcf"]["ahead"] == 1 and SEALED_BASELINES["mmc"]["ahead"] == 3
    class FakeResult:
        def __init__(self, output: bytes): self.stdout = output
    class FakeBase:
        def __init__(self): self.own_lock_checked = False
        def run(self, args: tuple[str, ...], **_kwargs: Any) -> FakeResult:
            if args[1:2] == ("branch",): return FakeResult(b"main\n")
            if args[1:2] == ("rev-parse",): return FakeResult((SEALED_BASELINES["gpcf"]["head"] if args[-1] == "HEAD" else SEALED_BASELINES["gpcf"]["origin"]).encode() + b"\n")
            if args[1:2] == ("rev-list",): return FakeResult(b"1 0\n")
            if args[1:2] == ("diff",): return FakeResult(b"")
            raise AssertionError(args)
        def git_status(self, _root: Path, expanded: bool, *, allow_own_lock: bool = False) -> tuple[int, str]:
            assert allow_own_lock
            key = "expanded" if expanded else "ordinary"
            return SEALED_BASELINES["gpcf"][f"{key}_count"], SEALED_BASELINES["gpcf"][f"{key}_sha256"]
        def check_own_lock(self) -> None: self.own_lock_checked = True
        def fail(self, _step: str, code: str) -> None: raise RuntimeError(code)
    fake = FakeBase()
    check_exact_repo(r9, fake, "gpcf", GPCF_ROOT, own_lock_expected=True)
    assert fake.own_lock_checked
    receipt = r9.self_test()
    assert receipt["status"] == "pass" and receipt["explicit_mmc_ahead_baseline"]
    return {"status": "pass", "control": CONTROL_ID, "external_manifest_sealed": True, "own_lock_baseline_path": True, "r9_divergence_selftest": True, "api_requests": 0}


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
        result = {"status": "stopped_no_change", "code": type(error).__name__, "control": CONTROL_ID, "connection_count": 0, "api_requests": 0}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] in {"pass", "completed_read_only"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
