---
doc_id: GPCF-DOC-8C7F2F4F01
title: Cognee P3 写入预览回滚演练 Evidence
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.md
source_path: docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Cognee P3 写入预览回滚演练 Evidence

## 1. 运行方式

```bash
python3 loop/context/cognee/scripts/run-cognee-p3-write-preview-rollback.py \
  --input fixtures/cognee/cognee-p3-write-preview-rollback-template.json \
  --output-json docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.json

python3 loop/context/cognee/scripts/validate-cognee-p3-write-preview-rollback.py \
  --input docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.json
```

> 说明：本文件只用于 P3 反例与回滚演练，不表示生产能力闭环。

## 1.1 P3 回滚演练结果（更新于 2026-06-23）

- evidence status: `pass`
- status reason: `pass`
- record_count: `4`
- requested_write_count: `4`
- rollback_block_rate: `1.0`
- owner_authorization_absence_rate: `0.5`
- waes_block_rate: `0.5`
- preview_tier_rate: `1.0`
- expected_blocked_reason_rate: `1.0`
- marker_coverage: `1.0`
- mean_saving_rate: `0.056332`
- pilot_gate_pass: `true`
- pilot_rule: `rollback_block_rate_min=1.0, owner_authorization_absence_min=0.4, waes_block_rate_min=0.4, preview_tier_rate_min=1.0`

> 该轮判定说明：回滚演练通过，authorization 缺失与 WAES 拒绝场景均被稳定拦截，且全部被归类为预期阻断原因。

## 2. 结果字段（摘要）

- schema: `globalcloud.cognee_p3_write_preview_rollback_result.v1`
- status: `pass | hold`
- status_reason:
  - `pass`
  - `rollback_gate_not_reached`
- records: 与 `fixtures/cognee/cognee-p3-write-preview-rollback-template.json` 的对齐结果
- summary:
  - `record_count`
  - `requested_write_count`
  - `rollback_block_rate`
  - `owner_authorization_absence_rate`
  - `waes_block_rate`
  - `preview_tier_rate`
  - `expected_blocked_reason_rate`
  - `marker_coverage`
  - `mean_saving_rate`
  - `pilot_gate_pass`

## 3. 字段校验命令

```bash
python3 loop/context/cognee/scripts/validate-cognee-p3-write-preview-rollback.py \
  --input docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.json
```

## 4. 输出示例

`docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.json`
