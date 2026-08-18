#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


CONTROL_ID = "GKE-001-COORDINATION-20260817-057-A10R34P17R6R4"
RUN_ID = "gke001-a10r34p17r6r4-kds-session-attribution"
CHANGE_ID = "attribute-kds-local-schema-sessions-a10r34p17r6r4"

GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
MMC_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
R6R3_CONTROLLER = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-session-attribution-controller-a10r34p17r6r3.py"
R6R3_CONTROLLER_SHA256 = "7344d8ef21c36da6fa1dc2730a64144a0d44d374200f3b40d6a89a9d6ae440ca"
SEALED_EXTERNAL_OVERRIDES = {
    "工业绿链/reports/Hermes质量周报.md": "1c241db81a98765106c2b6bd838d0a1085a07ef70e125c95d2549ca68e567ebd",
    "工业绿链/reports/项目监控仪表盘.md": "0fd7841204c24f5a0408a327f02b12506225faa94ab4b623c5c62b4f000280e2",
    "工业绿链/体系/W01-W20覆盖率报告.md": "7bcee42c2316eed4adab01e9962e36556c29bc11dcf263eb1e50e0154a591552",
    "工业绿链/月报/月报_2026-08.md": "10ef0a8f7f887481911535fe1794bd6af7885e61d17392e8e422dd3f0cabcd46",
}
SEALED_EXTERNAL_MANIFEST_SHA256 = "33608acef60d121106cadad941254256055bfae4950f52d2eb770bf89ab2cfa9"

SEALED_BASELINES = {
    "gpcf": {
        "head": "11d022b818332d2271a78b427c326eb454507a5a",
        "origin": "11d022b818332d2271a78b427c326eb454507a5a",
        "ordinary_count": 749,
        "ordinary_sha256": "d96982fe7f45c6d3835a15fbf125956755dfb75d0a966033200fba0afb048132",
        "expanded_count": 766,
        "expanded_sha256": "0423da61addd089fa1f20eca99d87e0ac351935d50e0a603099edcee96384aab",
    },
    "kds": {
        "head": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa",
        "ordinary_count": 287,
        "ordinary_sha256": "8b06b9c3777d8ccc7940e229bc93f674d38ff5b81011b1562ab07776ae1098c7",
        "expanded_count": 577,
        "expanded_sha256": "322d38cb205db114c0c0954ecb3c602320db13b862c5c9522c4188582986020c",
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


def load_stack() -> tuple[Any, Any, Any]:
    if digest(R6R3_CONTROLLER.read_bytes()) != R6R3_CONTROLLER_SHA256:
        raise RuntimeError("r6r3_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r6r3_base", R6R3_CONTROLLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("r6r3_controller_import")
    r6r3 = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = r6r3
    spec.loader.exec_module(r6r3)
    r6r3.CONTROL_ID = CONTROL_ID
    r6r3.RUN_ID = RUN_ID
    r6r3.CHANGE_ID = CHANGE_ID
    r6r3.__file__ = str(Path(__file__))
    r6r3.SEALED_BASELINES = SEALED_BASELINES
    r6r3.terminal = terminal
    original_load_base = r6r3.load_base

    def resealed_load_base(r6r2: Any) -> tuple[Any, Any]:
        r6r1, base = original_load_base(r6r2)
        base.CONTROL_ID = CONTROL_ID
        base.RUN_ID = RUN_ID
        base.CHANGE_ID = CHANGE_ID
        base.SEALED_EXTERNAL_FILES = tuple(
            (path, SEALED_EXTERNAL_OVERRIDES.get(path, expected))
            for path, expected in base.SEALED_EXTERNAL_FILES
        )
        base.SEALED_EXTERNAL_MANIFEST_SHA256 = SEALED_EXTERNAL_MANIFEST_SHA256
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

    r6r3.load_base = resealed_load_base
    r6r1, base = r6r3.load_base(r6r3.load_r6r2())
    return r6r3, r6r1, base


def lock_helper_action(action: str, sealed_sha: str) -> dict[str, Any]:
    if digest(Path(__file__).read_bytes()) != sealed_sha:
        raise RuntimeError("sealed_sha")
    _, _, base = load_stack()
    if action == "acquire":
        return base.lock_helper_acquire()
    if action == "release":
        return base.lock_helper_release()
    if action == "cleanup":
        return base.lock_helper_cleanup()
    raise RuntimeError("lock_helper_action")


def preflight(sealed_sha: str) -> dict[str, Any]:
    r6r3, _, _ = load_stack()
    return r6r3.preflight(sealed_sha)


def execute(sealed_sha: str) -> dict[str, Any]:
    r6r3, _, _ = load_stack()
    return r6r3.execute(sealed_sha)


def self_test() -> dict[str, Any]:
    r6r3, _, _ = load_stack()
    result = r6r3.self_test()
    result["control"] = CONTROL_ID
    result["resealed_kds_dirty"] = "287/577"
    return result


def safe_error_code(error: BaseException) -> str:
    return str(getattr(error, "sqlstate", None) or type(error).__name__)


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
