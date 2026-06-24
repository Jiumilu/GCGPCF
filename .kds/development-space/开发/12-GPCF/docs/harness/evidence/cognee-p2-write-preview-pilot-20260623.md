---
doc_id: GPCF-DOC-8C7F2D6F01
title: Cognee P2 写入预览 Evidence
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.md
source_path: docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Cognee P2 写入预览 Evidence

## 1. 运行方式

```bash
python3 loop/context/cognee/scripts/run-cognee-p2-write-preview.py \
  --input fixtures/cognee/cognee-p2-write-preview-template.json \
  --output-json docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.json

python3 loop/context/cognee/scripts/validate-cognee-p2-write-preview-output.py \
  --input docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.json
```

> 说明：本文件只用于 P2 受控 preview 写入对照，不表示生产能力闭环。

## 1.1 P2 复测结果（更新于 2026-06-23）

- evidence status: `pass`
- status reason: `pass`
- record_count: `5`
- requested_write_count: `5`
- preview_block_rate: `1.0`
- owner_authorization_presence_rate: `1.0`
- waes_pass_rate: `1.0`
- preview_tier_rate: `1.0`
- marker_coverage: `1.0`
- mean_saving_rate: `0.049075`
- pilot_gate_pass: `false`
- pilot_rule: `preview_block_rate_min=1.0, owner_authorization_presence_min=1.0, waes_pass_rate_min=1.0, payload_tier_preview_min=1.0`

> 该轮判定说明：当前 P2 阈值通过，授权与 WAES 放行覆盖达到门禁要求。

## 2. 结果字段（摘要）

- schema: `globalcloud.cognee_p2_write_preview_result.v1`
- status: `pass | hold`
- status_reason:
  - `pass`
  - `pilot_threshold_not_reached`
- records: 与 `fixtures/cognee/cognee-p2-write-preview-template.json` 的对齐结果
- summary:
  - `record_count`
  - `requested_write_count`
  - `preview_block_rate`
  - `owner_authorization_presence_rate`
  - `waes_pass_rate`
  - `preview_tier_rate`
  - `marker_coverage`
  - `mean_saving_rate`
  - `pilot_gate_pass`

## 3. 字段校验命令

```bash
python3 loop/context/cognee/scripts/validate-cognee-p2-write-preview-output.py \
  --input docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.json
```

## 4. 输出示例

`docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.json`
