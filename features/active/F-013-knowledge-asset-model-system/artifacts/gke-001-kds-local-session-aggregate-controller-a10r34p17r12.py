#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


CONTROL_ID = "GKE-001-COORDINATION-20260820-006-A10R34P17R12"
RUN_ID = "gke001-a10r34p17r12-kds-session-aggregate"
CHANGE_ID = "execute-kds-session-aggregate-from-owner-stable-baseline-a10r34p17r12"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
R10_PATH = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-session-aggregate-controller-a10r34p17r10.py"
R10_SHA256 = "98a0bdedeafa31686e35d98872d3ea49f41ae512160b8ff47f112b4c0283cdd6"

# This is the post-quiescence state, including this controller and its envelope.
SEALED_BASELINES = {
    "gpcf": {
        "head": "a317eeaab451920bc4bbbea904ca1c2bc774a497",
        "origin": "8deda915579b915d7496f20b2e4ecb5475491c40",
        "ahead": 1,
        "behind": 0,
        "ordinary_count": 17,
        "ordinary_sha256": "f0f54e4a96bd2c9338c532349215097ff0ebe0c6f5dd18e4c08ff8c0f87e06da",
        "expanded_count": 17,
        "expanded_sha256": "f0f54e4a96bd2c9338c532349215097ff0ebe0c6f5dd18e4c08ff8c0f87e06da",
    },
    "kds": {
        "head": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "ahead": 0,
        "behind": 0,
        "ordinary_count": 384,
        "ordinary_sha256": "20e3118b5cccd7ab1b7f00dd3a142aee36e319e1bb3c0e89e898fdc45ed17809",
        "expanded_count": 714,
        "expanded_sha256": "5ad716a5a9cb636475d9f319b6e098d79e821e218ef8f0462e938d7bc2fa0b72",
    },
    "mmc": {
        "head": "8f1e7cba20bada78fbc2e4c922f53be7b38606d7",
        "origin": "2dd7954fa4826120d68d42bd8f3c30e8d9ead99b",
        "ahead": 3,
        "behind": 0,
        "ordinary_count": 0,
        "ordinary_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "expanded_count": 0,
        "expanded_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_r10() -> Any:
    if digest(R10_PATH.read_bytes()) != R10_SHA256:
        raise RuntimeError("r10_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r12_r10", R10_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("r10_controller_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.SEALED_BASELINES = SEALED_BASELINES
    return module


def terminal(r10: Any, status: str, code: str, **extra: Any) -> dict[str, Any]:
    return r10.terminal(status, code, **extra) | {"control": CONTROL_ID}


def execute(sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    r10, base, acquired = load_r10(), None, False
    result: dict[str, Any] = {"status": "stopped_no_change", "code": "not_started", "control": CONTROL_ID}
    try:
        r9 = r10.load_r9()
        base = r9.load_base()
        base.CONTROL_ID, base.RUN_ID, base.CHANGE_ID = CONTROL_ID, RUN_ID, CHANGE_ID
        dsn = r10.hard_baseline(r9, base)
        outcome = base.lock_helper_acquire()
        if not outcome.get("acquired"):
            result = terminal(r10, "stopped_no_change", "lock_not_acquired")
        else:
            acquired = True
            dsn = r10.hard_baseline(r9, base, own_lock_expected=True)
            result = r9.load_r8().aggregate_sessions(dsn, base) | {"control": CONTROL_ID}
    except Exception as error:
        if base is not None and isinstance(error, base.ControlledFailure):
            result = terminal(r10, "stopped_no_change", error.code, step=error.step)
        else:
            result = terminal(r10, "stopped_no_change", type(error).__name__)
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
    r10 = load_r10()
    assert SEALED_BASELINES["kds"]["ordinary_count"] == 384
    assert SEALED_BASELINES["kds"]["expanded_count"] == 714
    assert SEALED_BASELINES["gpcf"]["ahead"] == 1
    assert SEALED_BASELINES["mmc"]["ahead"] == 3
    source = Path(__file__).read_text(encoding="utf-8")
    assert "--execute" in source and "sealed_sha" in source
    assert "module.SEALED_BASELINES = SEALED_BASELINES" in source
    return {
        "status": "pass",
        "control": CONTROL_ID,
        "execution_authorized": False,
        "database_connections": 0,
        "api_requests": 0,
        "r10_dependency_sha256": R10_SHA256,
    }


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
        result = {"status": "stopped_no_change", "control": CONTROL_ID, "code": type(error).__name__, "database_connections": 0, "api_requests": 0}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] in {"pass", "completed_read_only"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
