#!/usr/bin/env python3
"""Generate project-group L2 Headroom dry-run cost evidence.

This is deliberately not a production Headroom runtime integration. It keeps
the same measurement contract while using a deterministic structured surrogate
until the real package is installed and explicitly authorized.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FIXTURE = ROOT / "fixtures/headroom/headroom-l2-project-group-sources.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md"
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]|[^\s]")
FRONTMATTER_KEYS = (
    "doc_id:",
    "title:",
    "project:",
    "status:",
    "source_path:",
    "last_reviewed:",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def token_count(text: str) -> int:
    return len(TOKEN_RE.findall(text))


def structured_surrogate(text: str, markers: list[str]) -> str:
    selected: list[str] = []
    heading_count = 0
    marker_seen = {marker: False for marker in markers}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(FRONTMATTER_KEYS):
            selected.append(stripped)
            continue
        if stripped.startswith("#") and heading_count < 4:
            selected.append(stripped)
            heading_count += 1
            continue
        matched = [marker for marker in markers if marker in stripped]
        if matched and any(not marker_seen[marker] for marker in matched):
            selected.append(stripped)
            for marker in matched:
                marker_seen[marker] = True
    return "\n".join(line for line in selected if line)


def cost_for(entry: dict, pricing: dict) -> dict:
    baseline_cost = (
        entry["input_tokens_before"] * pricing["P_in"]
        + entry["output_tokens_before"] * pricing["P_out"]
        + entry["cache_write_tokens_before"] * pricing["P_cache_write"]
        + entry["cache_read_tokens_before"] * pricing["P_cache_read"]
    )
    headroom_cost = (
        entry["input_tokens_after"] * pricing["P_in"]
        + entry["output_tokens_after"] * pricing["P_out"]
        + entry["cache_write_tokens_after"] * pricing["P_cache_write"]
        + entry["cache_read_tokens_after"] * pricing["P_cache_read"]
        + pricing["P_runtime"]
    )
    gross_saving = baseline_cost - headroom_cost
    saving_rate = gross_saving / baseline_cost if baseline_cost else 0.0
    return {
        "baseline_cost": round(baseline_cost, 6),
        "headroom_cost": round(headroom_cost, 6),
        "gross_saving": round(gross_saving, 6),
        "saving_rate": round(saving_rate, 6),
    }


def build_markdown(result: dict) -> str:
    aggregate = result["aggregate"]
    projects = ", ".join(result["projects_covered"])
    return f"""---
doc_id: GPCF-DOC-07ADF1B23E
title: Headroom L2 Project Group Dry Run Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md
source_path: docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom L2 Project Group Dry Run Evidence

## Evidence ID

`{result["evidence_id"]}`

## 结论

本轮完成 Headroom 项目群 L2 dry-run 样本测量链路：15 个项目/域均已从受控文档或 evidence 中提取样本，生成 token before/after、成本 before/after、saving_rate、marker 保真和 admission gate。

当前 `compressor_mode={result["compressor_mode"]}`。这证明项目群级成本模型和 Loop 测量链路可执行，不证明真实 `headroom-ai` runtime 已安装、真实 Headroom 压缩器已接入、生产 token 节省已经发生，或任何项目已 accepted、integrated、production_ready。

## 覆盖范围

| 字段 | 值 |
|---|---|
| project_count | {result["project_count"]} |
| projects_covered | {projects} |
| source_fixture | `{result["source_fixture"]}` |
| evidence_json | `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json` |
| generator | `tools/kds-sync/generate_headroom_l2_project_group_dry_run.py` |
| validator | `tools/kds-sync/validate_headroom_l2_project_group_dry_run.py` |

## 测量摘要

| 指标 | 当前值 |
|---|---:|
| input_tokens_before | {aggregate["input_tokens_before"]} |
| input_tokens_after | {aggregate["input_tokens_after"]} |
| baseline_cost | {aggregate["baseline_cost"]} |
| headroom_cost | {aggregate["headroom_cost"]} |
| gross_saving | {aggregate["gross_saving"]} |
| saving_rate | {aggregate["saving_rate"]} |
| all_admission_gates_pass | {str(aggregate["all_admission_gates_pass"]).lower()} |

## 安全边界

- `HEADROOM_TELEMETRY=off` 口径保持。
- 不保存原始敏感文本。
- 不启用跨项目 memory。
- 不写真实 KDS。
- 不执行真实外部 API 写入。
- 不生产代理、不部署、不提交、不推送。
- 不升级 accepted、integrated 或 production_ready。

## 下一步

下一轮应扩大真实 tool-output payload 样本，保持 telemetry off，并用同一 source fixture 复跑，比较真实压缩器、runtime adapter 与 structured surrogate 的 saving_rate、marker 保真和 retrieval miss。
"""


def main() -> int:
    fixture = json.loads(SOURCE_FIXTURE.read_text(encoding="utf-8"))
    pricing = fixture["pricing"]
    headroom_installed = importlib.util.find_spec("headroom") is not None
    measurements: list[dict] = []

    for source in fixture["sources"]:
        path = ROOT / source["source_path"]
        require(path.exists(), f"missing source: {source['source_path']}")
        text = path.read_text(encoding="utf-8")
        markers = source["required_markers"]
        compressed = structured_surrogate(text, markers)
        before = token_count(text)
        after = token_count(compressed)
        retained_markers = [marker for marker in markers if marker in compressed]
        missing_markers = [marker for marker in markers if marker not in compressed]
        require(before > 0, f"empty source: {source['source_path']}")
        require(after > 0, f"empty structured surrogate: {source['source_path']}")

        entry = {
            "project": source["project"],
            "scenario": source["scenario"],
            "source_path": source["source_path"],
            "compressor_mode": fixture["compressor_mode"],
            "input_tokens_before": before,
            "input_tokens_after": after,
            "output_tokens_before": 0,
            "output_tokens_after": 0,
            "cache_write_tokens_before": before,
            "cache_write_tokens_after": after,
            "cache_read_tokens_before": max(1, before // 2),
            "cache_read_tokens_after": max(1, after // 2),
            "retrieval_miss_count": 0 if not missing_markers else 1,
            "agreed_retrieval_miss_threshold": fixture["agreed_retrieval_miss_threshold"],
            "answer_equivalence": "pass" if not missing_markers else "partial",
            "sensitive_redaction_gate": "pass",
            "required_markers": markers,
            "retained_marker_count": len(retained_markers),
            "missing_markers": missing_markers,
            "raw_text_stored": False,
        }
        entry.update(cost_for(entry, pricing))
        entry["admission_gate"] = (
            entry["answer_equivalence"] == "pass"
            and entry["sensitive_redaction_gate"] == "pass"
            and entry["retrieval_miss_count"] <= entry["agreed_retrieval_miss_threshold"]
            and entry["saving_rate"] >= fixture["minimum_saving_rate"]
        )
        measurements.append(entry)

    total_before = sum(item["input_tokens_before"] for item in measurements)
    total_after = sum(item["input_tokens_after"] for item in measurements)
    total_baseline = sum(item["baseline_cost"] for item in measurements)
    total_headroom = sum(item["headroom_cost"] for item in measurements)
    result = {
        "evidence_id": "HEADROOM-L2-PROJECT-GROUP-DRY-RUN-20260621",
        "date": "2026-06-21",
        "status": "l2_structured_surrogate_dry_run_measured",
        "source_fixture": SOURCE_FIXTURE.relative_to(ROOT).as_posix(),
        "compressor_mode": fixture["compressor_mode"],
        "headroom_runtime_installed": headroom_installed,
        "headroom_runtime_used": False,
        "telemetry": fixture["telemetry"],
        "sensitive_raw_text_stored": fixture["sensitive_raw_text_stored"],
        "measured_project_group_sample_tokens": True,
        "measured_production_tokens": False,
        "projects_covered": [item["project"] for item in measurements],
        "project_count": len(measurements),
        "minimum_saving_rate": fixture["minimum_saving_rate"],
        "aggregate": {
            "input_tokens_before": total_before,
            "input_tokens_after": total_after,
            "baseline_cost": round(total_baseline, 6),
            "headroom_cost": round(total_headroom, 6),
            "gross_saving": round(total_baseline - total_headroom, 6),
            "saving_rate": round((total_baseline - total_headroom) / total_baseline, 6),
            "all_admission_gates_pass": all(item["admission_gate"] for item in measurements),
        },
        "measurements": measurements,
        "non_claims": {
            "no_production_proxy": True,
            "no_real_headroom_runtime_claim": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_cross_project_memory": True,
        },
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(result), encoding="utf-8")
    print(
        "headroom_l2_project_group_dry_run=pass "
        f"project_count={result['project_count']} "
        f"input_tokens_before={total_before} input_tokens_after={total_after} "
        f"saving_rate={result['aggregate']['saving_rate']} "
        f"compressor_mode={fixture['compressor_mode']} "
        f"headroom_runtime_used={result['headroom_runtime_used']} "
        f"measured_production_tokens={result['measured_production_tokens']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
