#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any
from unittest import mock


CONTROL_ID = "GKE-001-COORDINATION-20260820-003-A10R34P17R9"
RUN_ID = "gke001-a10r34p17r9-kds-session-aggregate"
CHANGE_ID = "repair-kds-session-aggregate-baseline-contract-a10r34p17r9"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
R5_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-schema-diagnostic-controller-a10r34p17r5.py"
R5_CONTROLLER_SHA256 = "7e2299ef2f057d43b6c66bad1e1b4fc7608cc2fb44ecef33ef23ade673d856f2"
R8_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-session-aggregate-controller-a10r34p17r8.py"
R8_CONTROLLER_SHA256 = "9246748605d46f90260d685ee001f44bb842f4dabc0799bfec6958492b97f3c4"

SEALED_BASELINES = {
    "gpcf": {"head": "a317eeaab451920bc4bbbea904ca1c2bc774a497", "origin": "8deda915579b915d7496f20b2e4ecb5475491c40", "ahead": 1, "behind": 0, "ordinary_count": 11, "ordinary_sha256": "3db8f38e40ff5681009459c83f5d9e6f6b0502ecad093b142e9d06d64f455a0f", "expanded_count": 11, "expanded_sha256": "3db8f38e40ff5681009459c83f5d9e6f6b0502ecad093b142e9d06d64f455a0f"},
    "kds": {"head": "2ac85c55163b7acf0ede699184ac360579ccefaa", "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa", "ahead": 0, "behind": 0, "ordinary_count": 373, "ordinary_sha256": "4677fcccdf92696d134e276bc19692403f57f5151c3026670950b8f2ded7760b", "expanded_count": 703, "expanded_sha256": "5a7325cd54c9eed1c89fcc9e5540065b68cc61ed7c2399fdddbe761534b46f77"},
    "mmc": {"head": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7", "origin": "2dd7954fa4826120d68d42bd8f3c30e8d9ead99b", "ahead": 3, "behind": 0, "ordinary_count": 0, "ordinary_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "expanded_count": 0, "expanded_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
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
    r5 = load_module(R5_CONTROLLER, R5_CONTROLLER_SHA256, "gke001_r9_r5")
    base = r5.load_base()
    base.CONTROL_ID, base.RUN_ID, base.CHANGE_ID = CONTROL_ID, RUN_ID, CHANGE_ID
    base.BASELINES = tuple(
        base.RepoBaseline(root, SEALED_BASELINES[name]["head"], SEALED_BASELINES[name]["origin"], SEALED_BASELINES[name]["ordinary_count"], SEALED_BASELINES[name]["ordinary_sha256"], SEALED_BASELINES[name]["expanded_count"], SEALED_BASELINES[name]["expanded_sha256"])
        for name, root in (("gpcf", GPCF_ROOT), ("kds", KDS_ROOT), ("mmc", MMC_ROOT))
    )
    return base


def load_r8() -> Any:
    return load_module(R8_CONTROLLER, R8_CONTROLLER_SHA256, "gke001_r9_r8")


def fail(base: Any, code: str) -> None:
    base.fail("baseline", code)


def exact_divergence(base: Any, root: Path, expected: tuple[int, int]) -> None:
    actual = tuple(int(value) for value in base.run(("/usr/bin/git", "rev-list", "--left-right", "--count", "HEAD...origin/main"), cwd=root).stdout.split())
    if actual != expected:
        fail(base, f"{root.name}_divergence")


def check_exact_repo(base: Any, name: str, root: Path) -> None:
    values = SEALED_BASELINES[name]
    if base.run(("/usr/bin/git", "branch", "--show-current"), cwd=root).stdout.strip() != b"main":
        fail(base, f"{root.name}_branch")
    for ref, expected in (("HEAD", values["head"]), ("origin/main", values["origin"])):
        if base.run(("/usr/bin/git", "rev-parse", ref), cwd=root).stdout.decode().strip() != expected:
            fail(base, f"{root.name}_{ref}")
    exact_divergence(base, root, (values["ahead"], values["behind"]))
    if base.run(("/usr/bin/git", "diff", "--cached", "--name-only"), cwd=root).stdout:
        fail(base, f"{root.name}_staged")
    if base.git_status(root, False) != (values["ordinary_count"], values["ordinary_sha256"]):
        fail(base, f"{root.name}_ordinary_dirty")
    if base.git_status(root, True) != (values["expanded_count"], values["expanded_sha256"]):
        fail(base, f"{root.name}_expanded_dirty")
    if (root / ".harness/opsx.lock").exists():
        fail(base, f"{root.name}_opsx_lock")


def check_gpcf(base: Any) -> None:
    check_exact_repo(base, "gpcf", GPCF_ROOT)
    if base.ATOMIC_GUARD.exists():
        fail(base, "GlobalCoud GPCF_opsx_guard")


def hard_baseline(base: Any) -> str:
    check_gpcf(base)
    for baseline in base.BASELINES:
        if baseline.root == KDS_ROOT:
            base.check_repo(baseline)
    check_exact_repo(base, "mmc", MMC_ROOT)
    base.validate_runtime()
    for name, path in base.OFFICIAL_LOCK_HELPERS.items():
        if digest(path.read_bytes()) != base.SEALED_OFFICIAL_LOCK_HELPERS[name]:
            base.fail("lock", f"official_{name}_helper_drift")
    return base.read_secure_environment()


def terminal(status: str, code: str, **extra: Any) -> dict[str, Any]:
    return {"status": status, "code": code, "control": CONTROL_ID, "database": "gbrain", "host": "loopback", "connection_count": 1, "transaction_count": 1, "transaction_mode": "repeatable_read_read_only", "fixture_created": False, "api_requests": 0, **extra}


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    base, r8, acquired = load_base(), load_r8(), False
    result: dict[str, Any] = terminal("stopped_no_change", "not_started")
    try:
        dsn = hard_baseline(base)
        outcome = base.lock_helper_acquire()
        if not outcome.get("acquired"):
            result = terminal("stopped_no_change", "lock_not_acquired")
        else:
            acquired = True
            dsn = hard_baseline(base)
            result = r8.aggregate_sessions(dsn, base)
    except base.ControlledFailure as error:
        result = terminal("stopped_no_change", error.code, step=error.step)
    finally:
        if acquired:
            released = base.lock_helper_release()
            result["opsx_lock_released"] = bool(released.get("released"))
            if not result["opsx_lock_released"]:
                result["status"], result["code"] = "failed_fail_closed", "lock_release_unresolved"
        else:
            result["opsx_lock_released"] = not base.OPSX_LOCK.exists() and not base.ATOMIC_GUARD.exists()
    return result


def self_test() -> dict[str, Any]:
    r8 = load_r8()
    assert SEALED_BASELINES["gpcf"]["ahead"] == 1 and SEALED_BASELINES["gpcf"]["behind"] == 0
    assert SEALED_BASELINES["kds"]["ahead"] == 0 and SEALED_BASELINES["mmc"]["ahead"] == 3
    class FakeResult:
        def __init__(self, output: bytes): self.stdout = output
    class FakeBase:
        def __init__(self, output: bytes): self.output = output
        def run(self, _args: Any, **_kwargs: Any) -> FakeResult: return FakeResult(self.output)
        def fail(self, _step: str, code: str) -> None: raise RuntimeError(code)
    exact_divergence(FakeBase(b"1 0\n"), GPCF_ROOT, (1, 0))
    exact_divergence(FakeBase(b"3 0\n"), MMC_ROOT, (3, 0))
    try:
        exact_divergence(FakeBase(b"1 0\n"), GPCF_ROOT, (0, 0))
    except RuntimeError as error:
        assert str(error).endswith("_divergence")
    else:
        raise AssertionError("divergence mismatch accepted")
    with mock.patch.object(r8.psycopg, "connect"):
        assert r8.self_test()["status"] == "pass"
    return {"status": "pass", "control": CONTROL_ID, "explicit_gpcf_ahead_baseline": True, "explicit_mmc_ahead_baseline": True, "divergence_mismatch_fail_closed": True, "r8_aggregate_selftest": True, "api_requests": 0}


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
        result = terminal("stopped_no_change", type(error).__name__, connection_count=0)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] in {"pass", "completed_read_only"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
