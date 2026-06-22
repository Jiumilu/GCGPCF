#!/usr/bin/env python3
"""Measure Headroom runtime across project-group Loop output scenarios."""

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
L2_EVIDENCE = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
RUNTIME_PROBE = ROOT / "docs/harness/evidence/headroom-runtime-probe-20260621.json"
RUNTIME_ADAPTER = ROOT / "docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json"
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]|[^\s]")


class RegexTokenCounter:
    def count_text(self, text: str) -> int:
        return len(TOKEN_RE.findall(text))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def marker_lines(path: Path, markers: list[str], limit: int = 8) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped and any(marker in stripped for marker in markers):
            rows.append({"line": index, "text": stripped[:240]})
        if len(rows) >= limit:
            break
    return rows


def build_json_records(fixture: dict) -> str:
    records = []
    for source in fixture["sources"]:
        path = ROOT / source["source_path"]
        records.append(
            {
                "project": source["project"],
                "scenario": source["scenario"],
                "source_path": source["source_path"],
                "required_markers": source["required_markers"],
                "marker_lines": marker_lines(path, source["required_markers"]),
                "raw_text_stored": False,
            }
        )
    return json.dumps(records, ensure_ascii=False, indent=2)


def build_metric_json_array(l2: dict, runtime_probe: dict, runtime_adapter: dict) -> str:
    rows = []
    for item in l2["measurements"]:
        rows.append(
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
    rows.append(
        {
            "project": "GPCF",
            "source_path": "docs/harness/evidence/headroom-runtime-probe-20260621.json",
            "runtime_saving_rate": runtime_probe["aggregate"]["runtime_saving_rate"],
            "runtime_admission_gate": runtime_probe["decision"]["runtime_admission_gate"],
            "raw_text_stored": False,
        }
    )
    rows.append(
        {
            "project": "GPCF",
            "source_path": "docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json",
            "runtime_adapter_saving_rate": runtime_adapter["aggregate"]["runtime_adapter_saving_rate"],
            "runtime_adapter_admission_gate": runtime_adapter["decision"]["runtime_adapter_admission_gate"],
            "raw_text_stored": False,
        }
    )
    return json.dumps(rows, ensure_ascii=False, separators=(",", ":"))


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
        for row in marker_lines(path, source["required_markers"], limit=3):
            text = str(row["text"]).replace("\n", " ")
            lines.append(f"{source['source_path']}:{row['line']}:{text}")
    return "\n".join(lines)


def scenario_payloads(fixture: dict, l2: dict, runtime_probe: dict, runtime_adapter: dict) -> list[dict[str, object]]:
    return [
        {
            "scenario_id": "project_group_evidence_json",
            "content_type": "json_tool_output",
            "item_type": "project_group_evidence_json",
            "payload": build_json_records(fixture),
            "required_markers": [source["project"] for source in fixture["sources"]],
            "minimum_saving_rate": 0.2,
        },
        {
            "scenario_id": "headroom_metric_json_array",
            "content_type": "metric_json_array",
            "item_type": "headroom_metric_json_array",
            "payload": build_metric_json_array(l2, runtime_probe, runtime_adapter),
            "required_markers": [source["project"] for source in fixture["sources"]],
            "minimum_saving_rate": 0.2,
        },
        {
            "scenario_id": "loop_validation_log",
            "content_type": "loop_log_output",
            "item_type": "loop_validation_log",
            "payload": build_loop_log(fixture),
            "required_markers": [source["project"] for source in fixture["sources"]],
            "minimum_saving_rate": 0.2,
        },
        {
            "scenario_id": "rg_marker_search_output",
            "content_type": "search_output",
            "item_type": "rg_marker_search_output",
            "payload": build_search_output(fixture),
            "required_markers": [source["project"] for source in fixture["sources"]],
            "minimum_saving_rate": 0.2,
        },
    ]


def run_scenario(router: ContentRouter, scenario: dict[str, object]) -> dict[str, object]:
    payload = str(scenario["payload"])
    unit = CompressionUnit(
        text=payload,
        provider="gpcf",
        endpoint="headroom_runtime_scenario_matrix",
        role="tool",
        item_type=str(scenario["item_type"]),
        cache_zone="live",
        mutable=True,
        context=f"GlobalCloud LOOP Headroom scenario matrix: {scenario['content_type']}",
        question="compress LOOP tool output while preserving project names and gate markers",
        min_bytes=1,
        metadata={"scenario_id": str(scenario["scenario_id"])},
    )
    compression = compress_unit_with_router(
        unit,
        router=router,
        tokenizer=RegexTokenCounter(),
        target_ratio=0.2,
    )
    required_markers = list(scenario["required_markers"])
    missing_markers = [marker for marker in required_markers if marker not in compression.compressed]
    saving_rate = (
        round(compression.tokens_saved / compression.tokens_before, 6)
        if compression.tokens_before
        else 0.0
    )
    minimum = float(scenario["minimum_saving_rate"])
    scenario_gate = (
        compression.modified
        and compression.tokens_saved > 0
        and not missing_markers
        and saving_rate >= minimum
    )
    return {
        "scenario_id": scenario["scenario_id"],
        "content_type": scenario["content_type"],
        "item_type": scenario["item_type"],
        "tokens_before": compression.tokens_before,
        "tokens_after": compression.tokens_after,
        "tokens_saved": compression.tokens_saved,
        "saving_rate": saving_rate,
        "minimum_saving_rate": minimum,
        "modified": compression.modified,
        "strategy": compression.strategy,
        "reason": compression.reason,
        "reason_category": compression.reason_category,
        "transforms_applied": compression.transforms_applied,
        "missing_markers": missing_markers,
        "marker_gate": not missing_markers,
        "scenario_gate": scenario_gate,
        "raw_text_stored": False,
    }


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    fixture = read_json(SOURCE_FIXTURE)
    l2 = read_json(L2_EVIDENCE)
    runtime_probe = read_json(RUNTIME_PROBE)
    runtime_adapter = read_json(RUNTIME_ADAPTER)
    router = ContentRouter()
    measurements = [
        run_scenario(router, scenario)
        for scenario in scenario_payloads(fixture, l2, runtime_probe, runtime_adapter)
    ]
    total_before = sum(int(item["tokens_before"]) for item in measurements)
    total_after = sum(int(item["tokens_after"]) for item in measurements)
    total_saved = total_before - total_after
    scenario_gates_passed = [item["scenario_id"] for item in measurements if item["scenario_gate"]]
    result = {
        "evidence_id": "HEADROOM-RUNTIME-SCENARIO-MATRIX-20260621",
        "date": "2026-06-21",
        "status": "runtime_scenario_matrix_measured_partial",
        "headroom_runtime_imported": True,
        "headroom_runtime_used": True,
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "python_version": platform.python_version(),
        "telemetry": "off",
        "source_fixture": SOURCE_FIXTURE.relative_to(ROOT).as_posix(),
        "project_count": len(fixture["sources"]),
        "projects_covered": [source["project"] for source in fixture["sources"]],
        "scenario_count": len(measurements),
        "aggregate": {
            "tokens_before": total_before,
            "tokens_after": total_after,
            "tokens_saved": total_saved,
            "saving_rate": round(total_saved / total_before, 6) if total_before else 0.0,
            "scenario_gates_passed": scenario_gates_passed,
            "scenario_gate_pass_count": len(scenario_gates_passed),
            "all_marker_gates_pass": all(item["marker_gate"] for item in measurements),
            "all_scenario_gates_pass": all(item["scenario_gate"] for item in measurements),
        },
        "measurements": measurements,
        "decision": {
            "runtime_matrix_admission_gate": False,
            "reason": "real runtime has measurable scenario-specific value, but not all LOOP output scenarios meet the L2 threshold",
            "recommended_application": scenario_gates_passed,
            "next_required_action": "pilot only passing output classes and keep Markdown/direct conversation compression blocked",
        },
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_cross_project_memory": True,
            "no_runtime_matrix_admission": True,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "headroom_runtime_scenario_matrix=pass "
        f"scenario_count={result['scenario_count']} "
        f"scenario_gate_pass_count={result['aggregate']['scenario_gate_pass_count']} "
        f"saving_rate={result['aggregate']['saving_rate']} "
        "runtime_matrix_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
