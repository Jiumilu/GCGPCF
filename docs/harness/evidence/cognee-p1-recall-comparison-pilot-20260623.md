---
doc_id: GPCF-DOC-8C7F2F4D5A
title: Cognee P1 召回对照 Evidence
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.md
source_path: docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Cognee P1 召回对照 Evidence

## 1. 运行方式

```bash
python3 loop/context/cognee/scripts/run-cognee-p1-recall-comparison.py \
  --input fixtures/cognee/cognee-p1-recall-comparison-template.json \
  --output-json docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.json

python3 loop/context/cognee/scripts/validate-cognee-p1-recall-output.py \
  --input docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.json
```

> 说明：本文件使用 P1 试点对照输入模板，不表示业务结论，仅用于 pilot evidence 归档。

## 1.1 P1 复测结果（更新于 2026-06-23）

- evidence status: `hold`
- status reason: `pilot_threshold_not_reached`
- record_count: `5`
- mean_retrieval_precision: `0.736190`
- marker_coverage: `1.0`
- unauthorized_write_block_rate: `1.0`
- mean_saving_rate: `0.059804`
- pilot_gate_pass: `false`
- pilot_rule: `recall_precision_min=0.85, marker_coverage_min=0.95, write_block_rate_min=1.0`

> 该轮判定说明：当前 precision 未达到门槛，且仍建议继续补充场景并复测。

## 2. 结果字段（摘要）

- schema: `globalcloud.cognee_p1_pilot_result.v1`
- status: `pass | hold`
- status_reason:
  - `pass`
  - `pilot_threshold_not_reached`
- records: 与 `fixtures/cognee/cognee-p1-recall-comparison-template.json` 的对齐结果
- summary:
  - `mean_retrieval_precision`
  - `marker_coverage`
  - `unauthorized_write_block_rate`
  - `mean_saving_rate`
  - `pilot_gate_pass`

## 3. 字段校验命令

```bash
python3 loop/context/cognee/scripts/validate-cognee-p1-recall-output.py \
  --input docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.json
```

## 4. 输出示例

`docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.json`
