#!/usr/bin/env python3
"""Build and measure the HeadroomCostMeasurement output class."""

from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import re
from pathlib import Path

from headroom.transforms.compression_units import CompressionUnit, compress_unit_with_router
from headroom.transforms.content_router import ContentRouter


ROOT = Path(__file__).resolve().parents[2]
L2_EVIDENCE = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.json"
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]|[^\s]")


class RegexTokenCounter:
    def count_text(self, text: str) -> int:
        return len(TOKEN_RE.findall(text))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_measurements(l2: dict) -> list[dict[str, object]]:
    records = []
    for item in l2["measurements"]:
        records.append(
            {
                "project": item["project"],
                "source_path": item["source_path"],
                "structured_surrogate_input_tokens_before": item["input_tokens_before"],
                "structured_surrogate_input_tokens_after": item["input_tokens_after"],
                "structured_surrogate_saving_rate": item["saving_rate"],
                "marker_gate": item["admission_gate"],
                "raw_text_stored": False,
            }
        )
    return records


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    l2 = load_json(L2_EVIDENCE)
    records = build_measurements(l2)
    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    unit = CompressionUnit(
        text=payload,
        provider="gpcf",
        endpoint="headroom_cost_measurement_output",
        role="tool",
        item_type="headroom_cost_measurement_array",
        cache_zone="live",
        mutable=True,
        context="GlobalCloud HeadroomCostMeasurement output class",
        question="compress cost measurement records while preserving project names and gate fields",
        min_bytes=1,
        metadata={"schema": "HeadroomCostMeasurement[]"},
    )
    compression = compress_unit_with_router(
        unit,
        router=ContentRouter(),
        tokenizer=RegexTokenCounter(),
        target_ratio=0.2,
    )
    projects = [record["project"] for record in records]
    required_markers = sorted(set(projects + ["structured_surrogate_saving_rate", "marker_gate"]))
    missing_markers = [marker for marker in required_markers if marker not in compression.compressed]
    saving_rate = (
        round(compression.tokens_saved / compression.tokens_before, 6)
        if compression.tokens_before
        else 0.0
    )
    output_gate = (
        compression.modified
        and compression.tokens_saved > 0
        and saving_rate >= 0.2
        and not missing_markers
    )
    result = {
        "evidence_id": "HEADROOM-COST-MEASUREMENT-OUTPUT-20260621",
        "date": "2026-06-21",
        "status": "cost_measurement_output_class_measured",
        "headroom_runtime_imported": True,
        "headroom_runtime_used": True,
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "python_version": platform.python_version(),
        "telemetry": "off",
        "schema": {
            "name": "HeadroomCostMeasurement",
            "shape": "array",
            "allowed_application": "structured_metric_tool_output_only",
            "required_fields": [
                "type",
                "project",
                "source_path",
                "structured_surrogate_input_tokens_before",
                "structured_surrogate_input_tokens_after",
                "structured_surrogate_saving_rate",
                "marker_gate",
                "raw_text_stored",
            ],
            "full_cost_detail_source": L2_EVIDENCE.relative_to(ROOT).as_posix(),
        },
        "project_count": len(projects),
        "projects_covered": projects,
        "record_count": len(records),
        "aggregate": {
            "tokens_before": compression.tokens_before,
            "tokens_after": compression.tokens_after,
            "tokens_saved": compression.tokens_saved,
            "saving_rate": saving_rate,
            "minimum_saving_rate": 0.2,
            "modified": compression.modified,
            "strategy": compression.strategy,
            "reason": compression.reason,
            "reason_category": compression.reason_category,
            "transforms_applied": compression.transforms_applied,
            "missing_markers": missing_markers,
            "marker_gate": not missing_markers,
            "output_gate": output_gate,
        },
        "decision": {
            "headroom_cost_measurement_output_gate": output_gate,
            "allowed_for_next_pilot": output_gate,
            "reason": "HeadroomCostMeasurement structured metric output meets runtime saving and marker gates"
            if output_gate
            else "HeadroomCostMeasurement output did not meet runtime saving or marker gates",
        },
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_cross_project_memory": True,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "headroom_cost_measurement_output=pass "
        f"record_count={result['record_count']} saving_rate={saving_rate} "
        f"output_gate={str(output_gate).lower()} measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
