#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


CONTROL_ID = "GKE-001-COORDINATION-20260820-005-A10R34P17R11"
GPCF_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")
KDS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
R10_PATH = GPCF_ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-local-session-aggregate-controller-a10r34p17r10.py"
R10_SHA256 = "98a0bdedeafa31686e35d98872d3ea49f41ae512160b8ff47f112b4c0283cdd6"

KDS_BASELINE = {
    "head": "2ac85c55163b7acf0ede699184ac360579ccefaa",
    "origin": "2ac85c55163b7acf0ede699184ac360579ccefaa",
    "ordinary": (381, "7545feb29bc340c848751b9f6c01733ce08f62c3d1f6edb7d36b7100ed75e3e1"),
    "expanded": (711, "2dcda5a6d957e2ded61fb72d1b156861f7fb74604d76b3a787d7dd56d58b6b8f"),
}


class VerificationFailure(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(*args: str) -> bytes:
    return subprocess.run(("/usr/bin/git",) + args, cwd=KDS_ROOT, check=True, stdout=subprocess.PIPE).stdout


def status(expanded: bool) -> tuple[int, str]:
    args = ["status", "--porcelain=v1", "-z"]
    if expanded:
        args.append("--untracked-files=all")
    payload = run_git(*args)
    return payload.count(b"\0"), sha256(payload)


def load_r10() -> Any:
    if sha256(R10_PATH.read_bytes()) != R10_SHA256:
        raise VerificationFailure("r10_controller_sha256")
    spec = importlib.util.spec_from_file_location("gke001_r11_r10", R10_PATH)
    if spec is None or spec.loader is None:
        raise VerificationFailure("r10_controller_import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def verify() -> dict[str, Any]:
    if run_git("branch", "--show-current").strip() != b"main":
        raise VerificationFailure("kds_branch")
    if run_git("rev-parse", "HEAD").decode().strip() != KDS_BASELINE["head"]:
        raise VerificationFailure("kds_head")
    if run_git("rev-parse", "origin/main").decode().strip() != KDS_BASELINE["origin"]:
        raise VerificationFailure("kds_origin")
    if run_git("rev-list", "--left-right", "--count", "HEAD...origin/main").strip() != b"0\t0":
        raise VerificationFailure("kds_divergence")
    if run_git("diff", "--cached", "--name-only"):
        raise VerificationFailure("kds_staged")
    if (KDS_ROOT / ".harness/opsx.lock").exists():
        raise VerificationFailure("kds_opsx_lock")
    for label, expanded in (("ordinary", False), ("expanded", True)):
        if status(expanded) != KDS_BASELINE[label]:
            raise VerificationFailure(f"kds_{label}_dirty")

    r10 = load_r10()
    class ReadOnlyBase:
        def fail(self, _step: str, code: str) -> None:
            raise VerificationFailure(code)
    r10.check_external_files(ReadOnlyBase())
    return {
        "status": "pass",
        "control": CONTROL_ID,
        "execution_authorized": False,
        "database_connections": 0,
        "api_requests": 0,
        "external_manifest_verified": True,
    }


def main() -> int:
    try:
        result = verify()
    except Exception as error:
        result = {
            "status": "stopped_no_change",
            "control": CONTROL_ID,
            "code": str(error),
            "execution_authorized": False,
            "database_connections": 0,
            "api_requests": 0,
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] == "pass" else 3


if __name__ == "__main__":
    raise SystemExit(main())
