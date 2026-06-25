---
doc_id: GPCF-DOC-8C7F2F6001
title: Cognee P4 真实写入 live 演练 Evidence（复测 20260624）
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md
source_path: docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Cognee P4 真实写入 live 演练 Evidence（复测 20260624）

## 1. 运行方式

```bash
authority_file=fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json

# 演练模式（默认 dry-run）
python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input "$authority_file" \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --dry-run-output-only

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json

# live-write 演练口径（本地证据生成）
python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input "$authority_file" \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --allow-live-write

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json
```

> 说明：`run-cognee-p4-real-writeback-live.py` 当前为受控运行链路脚本，`--allow-live-write` 用于演练口径标记，不代表已接入外部生产写入服务。

## 1.1 P4 live 演练结果（更新于 2026-06-25）

- evidence status: `pass`
- status reason: `pass`
- record_count: `5`
- requested_write_count: `5`
- execution_count: `5`
- production_write_count: `5`
- live_execution_ready_rate: `1.0`
- blocked_due_expected_reason_rate: `0.0`
- mean_saving_rate: `0.051312`
- pilot_gate_pass: `true`
- summary pilot rules:
  - `live_execution_ready_rate_min=1.0`
  - `blocked_due_expected_reason_rate_max=0.0`
  - `production_write_allowed=true`

> 该轮判定说明：live 演练口径已闭环，所有 `record` 均满足 `live_execution_ready=true`，写入执行标记均为 `executed`，可提交外部授权审批链进行生产执行切换决策。

## 2. 结果字段（摘要）

- schema: `globalcloud.cognee_p4_real_writeback_live_result.v1`
- status: `pass | hold`
- status_reason:
  - `dry_run_ready`
  - `live_execution_gate_not_reached`
  - `live_execution_blocked`
- records: 与 `fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json` 的对齐结果
- summary:
  - `record_count`
  - `requested_write_count`
  - `live_execution_ready_rate`
  - `live_execution_ready_count`
  - `execution_count`
  - `production_write_count`
  - `blocked_due_expected_reason_rate`
  - `mean_saving_rate`
  - `pilot_gate_pass`

## 3. 字段校验命令

```bash
python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json
```

## 4. 输出示例

`docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json`
