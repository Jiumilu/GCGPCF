#!/usr/bin/env python3
"""Run a Headroom runtime adapter dry-run on structured project evidence."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
from pathlib import Path

from headroom.transforms.compression_units import CompressionUnit, compress_unit_with_router
from headroom.transforms.content_router import ContentRouter


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FIXTURE = ROOT / "fixtures/headroom/headroom-l2-project-group-sources.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json"
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]|[^\s]")


class RegexTokenCounter:
    def count_text(self, text: str) -> int:
        return len(TOKEN_RE.findall(text))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def extract_marker_lines(text: str, markers: list[str]) -> list[str]:
    selected: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(marker in stripped for marker in markers):
            selected.append(stripped)
    return selected[:12]


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    fixture = json.loads(SOURCE_FIXTURE.read_text(encoding="utf-8"))
    records: list[dict] = []
    for source in fixture["sources"]:
        path = ROOT / source["source_path"]
        require(path.exists(), f"missing source: {source['source_path']}")
        text = path.read_text(encoding="utf-8")
        markers = source["required_markers"]
        marker_lines = extract_marker_lines(text, markers)
        records.append(
            {
                "project": source["project"],
                "scenario": source["scenario"],
                "source_path": source["source_path"],
                "required_markers": markers,
                "evidence_lines": marker_lines,
                "raw_text_stored": False,
            }
        )

    adapter_payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    input_hash = hashlib.sha256(adapter_payload.encode("utf-8")).hexdigest()
    router = ContentRouter()
    unit = CompressionUnit(
        text=adapter_payload,
        provider="gpcf",
        endpoint="headroom_runtime_adapter",
        role="tool",
        item_type="project_group_evidence_json",
        cache_zone="live",
        mutable=True,
        context="GlobalCloud project-group Loop evidence adapter dry-run",
        question="compress project group evidence while preserving project names and required gate markers",
        min_bytes=1,
        metadata={"adapter": "project_group_evidence_json"},
    )
    compression = compress_unit_with_router(
        unit,
        router=router,
        tokenizer=RegexTokenCounter(),
        target_ratio=0.2,
    )
    compressed = compression.compressed
    gate_markers = sorted(
        {
            marker
            for record in records
            for marker in [record["project"], *record["required_markers"]]
        }
    )
    missing_markers = [marker for marker in gate_markers if marker not in compressed]
    saving_rate = (
        round(compression.tokens_saved / compression.tokens_before, 6)
        if compression.tokens_before
        else 0.0
    )
    minimum_saving_rate = fixture["minimum_saving_rate"]
    runtime_adapter_admission_gate = (
        compression.modified
        and compression.tokens_saved > 0
        and not missing_markers
        and saving_rate >= minimum_saving_rate
    )
    result = {
        "evidence_id": "HEADROOM-RUNTIME-ADAPTER-DRY-RUN-20260621",
        "date": "2026-06-21",
        "status": "runtime_adapter_dry_run_measured_below_l2_threshold",
        "headroom_runtime_imported": True,
        "headroom_runtime_used": True,
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "python_version": platform.python_version(),
        "telemetry": "off",
        "source_fixture": SOURCE_FIXTURE.relative_to(ROOT).as_posix(),
        "adapter": {
            "name": "project_group_evidence_json",
            "role": "tool",
            "endpoint": "headroom_runtime_adapter",
            "cache_zone": "live",
            "raw_text_stored": False,
            "input_sha256": input_hash,
        },
        "project_count": len(records),
        "projects_covered": [record["project"] for record in records],
        "aggregate": {
            "tokens_before": compression.tokens_before,
            "tokens_after": compression.tokens_after,
            "tokens_saved": compression.tokens_saved,
            "runtime_adapter_saving_rate": saving_rate,
            "minimum_saving_rate": minimum_saving_rate,
            "modified": compression.modified,
            "strategy": compression.strategy,
            "reason": compression.reason,
            "reason_category": compression.reason_category,
            "transforms_applied": compression.transforms_applied,
            "all_marker_gates_pass": not missing_markers,
            "missing_markers": missing_markers,
        },
        "decision": {
            "runtime_adapter_admission_gate": runtime_adapter_admission_gate,
            "reason": "real headroom-ai runtime compressed the structured tool adapter payload, but saving_rate remains below the L2 threshold"
            if not runtime_adapter_admission_gate
            else "real headroom-ai runtime adapter met the dry-run saving and marker gates",
            "next_required_action": "measure larger real tool-output payloads and compare against structured surrogate before L3.5/L4 runtime use",
        },
        "records": [
            {
                "project": record["project"],
                "scenario": record["scenario"],
                "source_path": record["source_path"],
                "required_markers": record["required_markers"],
                "evidence_line_count": len(record["evidence_lines"]),
                "raw_text_stored": False,
            }
            for record in records
        ],
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_cross_project_memory": True,
            "no_runtime_admission": not runtime_adapter_admission_gate,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "headroom_runtime_adapter_dry_run=pass "
        "runtime_imported=true version="
        f"{result['headroom_version']} project_count={result['project_count']} "
        f"tokens_before={compression.tokens_before} tokens_after={compression.tokens_after} "
        f"runtime_adapter_saving_rate={saving_rate} "
        f"runtime_adapter_admission_gate={str(runtime_adapter_admission_gate).lower()} "
        "measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
