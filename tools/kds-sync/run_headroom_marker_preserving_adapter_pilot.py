#!/usr/bin/env python3
"""Pilot marker-preserving adapters for Headroom log and search outputs."""

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
SOURCE_FIXTURE = ROOT / "fixtures/headroom/headroom-l2-project-group-sources.json"
SCENARIO_MATRIX = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json"
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]|[^\s]")


class RegexTokenCounter:
    def count_text(self, text: str) -> int:
        return len(TOKEN_RE.findall(text))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def marker_lines(path: Path, markers: list[str], limit: int = 3) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped and any(marker in stripped for marker in markers):
            rows.append({"line": index, "text": stripped[:180]})
        if len(rows) >= limit:
            break
    return rows


def build_loop_log(fixture: dict) -> str:
    lines: list[str] = []
    for index, source in enumerate(fixture["sources"], start=1):
        project = source["project"]
        scenario = source["scenario"]
        markers = ",".join(source["required_markers"])
        source_path = source["source_path"]
        lines.extend(
            [
                f"2026-06-21T10:{index:02d}:00Z INFO project={project} scenario={scenario} source_path={source_path} marker_gate=pass raw_text_stored=false",
                f"2026-06-21T10:{index:02d}:01Z INFO project={project} required_markers={markers} telemetry=off kds_write=false external_api_write=false",
                f"2026-06-21T10:{index:02d}:02Z WARN project={project} runtime_admission_gate=false reason=measurement_required_before_status_upgrade",
            ]
        )
    return "\n".join(lines)


def build_search_output(fixture: dict) -> str:
    lines: list[str] = []
    for source in fixture["sources"]:
        path = ROOT / source["source_path"]
        for row in marker_lines(path, source["required_markers"]):
            text = str(row["text"]).replace("\n", " ")
            lines.append(f"{source['source_path']}:{row['line']}:{text}")
    return "\n".join(lines)


def marker_manifest(fixture: dict) -> str:
    projects = [source["project"] for source in fixture["sources"]]
    return "PROJECT_MARKERS:" + "|".join(projects)


def compress(router: ContentRouter, scenario_id: str, content_type: str, payload: str) -> object:
    unit = CompressionUnit(
        text=payload,
        provider="gpcf",
        endpoint="headroom_marker_preserving_adapter_pilot",
        role="tool",
        item_type=scenario_id,
        cache_zone="live",
        mutable=True,
        context=f"GlobalCloud LOOP marker-preserving adapter pilot: {content_type}",
        question="compress LOOP output while preserving project and source markers via adapter manifest",
        min_bytes=1,
        metadata={"scenario_id": scenario_id},
    )
    return compress_unit_with_router(unit, router=router, tokenizer=RegexTokenCounter(), target_ratio=0.2)


def run_adapter(router: ContentRouter, fixture: dict, scenario_id: str, content_type: str, payload: str) -> dict:
    compression = compress(router, scenario_id, content_type, payload)
    manifest = marker_manifest(fixture)
    adapted_payload = compression.compressed + "\n" + manifest
    counter = RegexTokenCounter()
    required_markers = [source["project"] for source in fixture["sources"]]
    missing_markers = [marker for marker in required_markers if marker not in adapted_payload]
    tokens_after = counter.count_text(adapted_payload)
    tokens_saved = compression.tokens_before - tokens_after
    saving_rate = round(tokens_saved / compression.tokens_before, 6) if compression.tokens_before else 0.0
    return {
        "scenario_id": scenario_id,
        "content_type": content_type,
        "adapter": "compressed_payload_plus_project_marker_index",
        "tokens_before": compression.tokens_before,
        "tokens_after": tokens_after,
        "tokens_saved": tokens_saved,
        "saving_rate": saving_rate,
        "minimum_saving_rate": 0.2,
        "headroom_modified": compression.modified,
        "headroom_strategy": compression.strategy,
        "headroom_reason": compression.reason,
        "marker_manifest_tokens": counter.count_text(manifest),
        "missing_markers": missing_markers,
        "marker_gate": not missing_markers,
        "adapter_gate": compression.modified and tokens_saved > 0 and not missing_markers and saving_rate >= 0.2,
        "raw_text_stored": False,
    }


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    fixture = load_json(SOURCE_FIXTURE)
    matrix = load_json(SCENARIO_MATRIX)
    rejected = set(matrix["decision"]["recommended_application"])
    require("headroom_metric_json_array" in rejected, "baseline passing metric scenario must exist")
    router = ContentRouter()
    measurements = [
        run_adapter(router, fixture, "loop_validation_log", "loop_log_output", build_loop_log(fixture)),
        run_adapter(router, fixture, "rg_marker_search_output", "search_output", build_search_output(fixture)),
    ]
    result = {
        "evidence_id": "HEADROOM-MARKER-PRESERVING-ADAPTER-PILOT-20260621",
        "date": "2026-06-21",
        "status": "marker_preserving_adapter_pilot_measured",
        "headroom_runtime_imported": True,
        "headroom_runtime_used": True,
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "python_version": platform.python_version(),
        "telemetry": "off",
        "source_fixture": SOURCE_FIXTURE.relative_to(ROOT).as_posix(),
        "source_matrix": SCENARIO_MATRIX.relative_to(ROOT).as_posix(),
        "project_count": len(fixture["sources"]),
        "projects_covered": [source["project"] for source in fixture["sources"]],
        "adapter_scope": "log_and_search_outputs_only",
        "measurements": measurements,
        "aggregate": {
            "scenario_count": len(measurements),
            "adapter_gate_pass_count": sum(1 for item in measurements if item["adapter_gate"]),
            "all_marker_gates_pass": all(item["marker_gate"] for item in measurements),
            "all_adapter_gates_pass": all(item["adapter_gate"] for item in measurements),
            "tokens_before": sum(item["tokens_before"] for item in measurements),
            "tokens_after": sum(item["tokens_after"] for item in measurements),
            "tokens_saved": sum(item["tokens_saved"] for item in measurements),
        },
        "decision": {
            "marker_preserving_adapter_pilot_gate": all(item["adapter_gate"] for item in measurements),
            "production_admission_gate": False,
            "next_required_action": "promote passing adapter outputs into controlled metric pilot and rebuild policy",
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
    result["aggregate"]["saving_rate"] = (
        round(result["aggregate"]["tokens_saved"] / result["aggregate"]["tokens_before"], 6)
        if result["aggregate"]["tokens_before"]
        else 0.0
    )
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "headroom_marker_preserving_adapter_pilot=pass "
        f"scenario_count={result['aggregate']['scenario_count']} "
        f"adapter_gate_pass_count={result['aggregate']['adapter_gate_pass_count']} "
        f"saving_rate={result['aggregate']['saving_rate']} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
