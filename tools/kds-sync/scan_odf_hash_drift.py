#!/usr/bin/env python3
"""Scan ODF ledgers for source, Markdown, and envelope hash drift.

This tool is read-only. It reports drift without updating ledgers, creating
ODF samples, writing to KDS, or changing rollout status.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGERS = [
    ROOT / "docs/harness/evidence/odf-pilot-sample-ledger-20260617.json",
    ROOT / "docs/harness/evidence/odf-phase2-sample-ledger-20260617.json",
    ROOT / "docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.json",
    ROOT / "docs/harness/evidence/odf-phase7-small-batch-ledger-20260619.json",
]
DYNAMIC_SOURCE_POLICIES = {
    "09-status/gpcf-project-status-matrix.md": "reference_only",
    "09-status/kds-development-space-sync-register.md": "reference_only",
    "docs/harness/evidence/evidence-index.md": "reference_only",
    "docs/harness/evidence/loop-governance-dashboard-20260617.md": "reference_only",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"odf_hash_drift=blocked reason=missing_ledger:{rel(path)}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"odf_hash_drift=blocked reason=invalid_json:{rel(path)}:{exc}")


def scan() -> dict:
    strict_drift: list[dict] = []
    dynamic_reference_drift: list[dict] = []
    samples = 0
    dynamic_sources = 0
    ledgers = []
    for ledger_path in LEDGERS:
        ledger = load_json(ledger_path)
        ledgers.append(rel(ledger_path))
        for sample in ledger.get("samples", []):
            samples += 1
            sample_id = sample.get("sample_id", "<missing>")
            source_path = sample.get("source_path")
            odf_path = sample.get("odf_path")
            dynamic_policy = DYNAMIC_SOURCE_POLICIES.get(str(source_path))
            if dynamic_policy:
                dynamic_sources += 1
            source = ROOT / str(source_path)
            odf = ROOT / str(odf_path)
            if not source.exists():
                strict_drift.append({"sample_id": sample_id, "field": "source_path", "expected": source_path, "actual": "missing"})
                continue
            if not odf.exists():
                strict_drift.append({"sample_id": sample_id, "field": "odf_path", "expected": odf_path, "actual": "missing"})
                continue
            source_hash = sha256_file(source)
            odf_hash = sha256_file(odf)
            if source_hash != sample.get("source_hash"):
                target = dynamic_reference_drift if dynamic_policy == "reference_only" else strict_drift
                target.append({"sample_id": sample_id, "field": "source_hash", "expected": sample.get("source_hash"), "actual": source_hash, "policy": dynamic_policy or "strict"})
            if source_hash != sample.get("markdown_hash"):
                target = dynamic_reference_drift if dynamic_policy == "reference_only" else strict_drift
                target.append({"sample_id": sample_id, "field": "markdown_hash", "expected": sample.get("markdown_hash"), "actual": source_hash, "policy": dynamic_policy or "strict"})
            if odf_hash != sample.get("odf_hash"):
                strict_drift.append({"sample_id": sample_id, "field": "odf_hash", "expected": sample.get("odf_hash"), "actual": odf_hash})
    return {
        "status": "pass" if not strict_drift else "strict_drift_detected",
        "ledgers": ledgers,
        "samples": samples,
        "dynamic_sources": dynamic_sources,
        "strict_drift_count": len(strict_drift),
        "dynamic_reference_drift_count": len(dynamic_reference_drift),
        "strict_drift": strict_drift,
        "dynamic_reference_drift": dynamic_reference_drift,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-drift", action="store_true")
    args = parser.parse_args()

    result = scan()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            "odf_hash_drift="
            + ("pass" if result["strict_drift_count"] == 0 else "strict_drift_detected")
            + f" ledgers={len(result['ledgers'])}"
            + f" samples={result['samples']}"
            + f" dynamic_sources={result['dynamic_sources']}"
            + f" strict_drift={result['strict_drift_count']}"
            + f" dynamic_reference_drift={result['dynamic_reference_drift_count']}"
        )
        for item in result["strict_drift"][:50]:
            print(
                f"{item['sample_id']} {item['field']} "
                f"expected={item['expected']} actual={item['actual']}"
            )
    return 1 if args.fail_on_drift and result["strict_drift_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
