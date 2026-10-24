from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/kds-sync/validate_owner_receipts.py"
RECORDER = ROOT / "tools/kds-sync/record_owner_receipt.py"
REGISTRY = ROOT / "runtime/owner-receipts.yaml"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, check=False)


def test_owner_receipts_registry_passes() -> None:
    result = run(str(VALIDATOR))
    assert result.returncode == 0, result.stderr
    assert "owner_receipts=pass" in result.stdout


def test_dry_run_does_not_modify_registry() -> None:
    before = REGISTRY.read_bytes()
    result = run(str(RECORDER), "--ref", "GC-357", "--status", "pending", "--dry-run")
    assert result.returncode == 0, result.stderr
    assert REGISTRY.read_bytes() == before


def test_approved_requires_signer() -> None:
    result = run(str(RECORDER), "--ref", "GC-357", "--status", "approved")
    assert result.returncode != 0
    assert "approved requires" in (result.stderr + result.stdout)
