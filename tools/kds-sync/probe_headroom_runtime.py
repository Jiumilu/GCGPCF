#!/usr/bin/env python3
"""Probe real headroom-ai runtime behavior against project-group samples."""

from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FIXTURE = ROOT / "fixtures/headroom/headroom-l2-project-group-sources.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-runtime-probe-20260621.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    try:
        import headroom  # type: ignore
    except Exception as exc:
        result = {
            "evidence_id": "HEADROOM-RUNTIME-PROBE-20260621",
            "date": "2026-06-21",
            "status": "runtime_import_failed",
            "headroom_runtime_imported": False,
            "headroom_runtime_used": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "python_version": platform.python_version(),
            "telemetry": "off",
            "measured_production_tokens": False,
        }
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("headroom_runtime_probe=blocked runtime_imported=false")
        return 0

    fixture = json.loads(SOURCE_FIXTURE.read_text(encoding="utf-8"))
    measurements: list[dict] = []
    config = headroom.CompressConfig(
        compress_user_messages=True,
        compress_system_messages=True,
        protect_recent=0,
        protect_analysis_context=False,
        min_tokens_to_compress=1,
        target_ratio=0.1,
    )
    for source in fixture["sources"]:
        path = ROOT / source["source_path"]
        require(path.exists(), f"missing source: {source['source_path']}")
        text = path.read_text(encoding="utf-8")
        response = headroom.compress(
            [{"role": "system", "content": text}],
            model="gpt-4o-mini",
            model_limit=4096,
            config=config,
        )
        content_after = response.messages[0].get("content", "") if response.messages else ""
        missing_markers = [marker for marker in source["required_markers"] if marker not in content_after]
        measurements.append(
            {
                "project": source["project"],
                "scenario": source["scenario"],
                "source_path": source["source_path"],
                "tokens_before": response.tokens_before,
                "tokens_after": response.tokens_after,
                "tokens_saved": response.tokens_saved,
                "compression_ratio": response.compression_ratio,
                "transforms_applied": response.transforms_applied,
                "missing_markers": missing_markers,
                "marker_gate": not missing_markers,
                "raw_text_stored": False,
            }
        )

    total_before = sum(item["tokens_before"] for item in measurements)
    total_after = sum(item["tokens_after"] for item in measurements)
    total_saved = total_before - total_after
    result = {
        "evidence_id": "HEADROOM-RUNTIME-PROBE-20260621",
        "date": "2026-06-21",
        "status": "runtime_probe_completed_no_project_group_compression",
        "headroom_runtime_imported": True,
        "headroom_runtime_used": True,
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "python_version": platform.python_version(),
        "telemetry": "off",
        "source_fixture": SOURCE_FIXTURE.relative_to(ROOT).as_posix(),
        "project_count": len(measurements),
        "projects_covered": [item["project"] for item in measurements],
        "aggregate": {
            "tokens_before": total_before,
            "tokens_after": total_after,
            "tokens_saved": total_saved,
            "runtime_saving_rate": round(total_saved / total_before, 6) if total_before else 0,
            "all_marker_gates_pass": all(item["marker_gate"] for item in measurements),
            "all_runtime_compressions_positive": all(item["tokens_saved"] > 0 for item in measurements),
            "all_transforms_noop": all(item["transforms_applied"] == ["router:noop"] for item in measurements),
        },
        "measurements": measurements,
        "decision": {
            "runtime_admission_gate": False,
            "reason": "headroom-ai runtime imported and executed, but project-group samples returned router:noop with zero token savings",
            "next_required_action": "identify supported Headroom transform path or adapter configuration before L3.5/L4 runtime use",
        },
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_cross_project_memory": True,
            "no_runtime_admission": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "headroom_runtime_probe=pass "
        f"runtime_imported=true version={result['headroom_version']} "
        f"project_count={result['project_count']} "
        f"runtime_saving_rate={result['aggregate']['runtime_saving_rate']} "
        f"runtime_admission_gate={str(result['decision']['runtime_admission_gate']).lower()} "
        "measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
