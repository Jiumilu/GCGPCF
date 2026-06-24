---
doc_id: GPCF-DOC-8C7F2F5003
title: Cognee P4 真实写入前置预检 Evidence（修复复测 20260624）
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md
source_path: docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Cognee P4 真实写入前置预检 Evidence（修复复测 20260624）

## 1. 运行方式

```bash
authority_file=fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json
python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-precheck.py \
  --input "$authority_file" \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.json

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-precheck.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.json
```

> 说明：本文件用于 P4 真实写回前置矩阵，仍属于预检/受控预演，不构成生产写入闭环。

## 1.1 P4 预检结果（更新于 2026-06-24）

- evidence status: `pass`
- status reason: `pass`
- record_count: `5`
- requested_write_count: `5`
- precheck_pass_rate: `1.0`
- owner_authorization_presence_rate: `1.0`
- waes_pass_rate: `1.0`
- runtime_dependency_ok_rate: `1.0`
- rollback_readiness_rate: `1.0`
- authorization_token_source_coverage: `1.0`
- expected_blocked_reason_rate: `1.0`
- marker_coverage: `1.0`
- mean_saving_rate: `0.051312`
- pilot_gate_pass: `true`
- pilot_rule: `precheck_pass_rate_min=0.8, owner_authorization_presence_min=0.8, waes_pass_rate_min=0.8, runtime_dependency_ok_rate_min=0.8, rollback_readiness_rate_min=0.8, authorization_token_source_coverage_min=0.8, marker_pass_rate_min=0.95, expected_blocked_reason_rate_min=1.0`

> 该轮判定说明：目前 P4 预检可闭合真实写入前置门禁基线，该轮阻断样例已复测修复：`runtime_dependency_ok` 与 `owner_authorization_present` 已全部为 true；本轮保留受控预检语义，未进入生产写入闭环。

## 2. 结果字段（摘要）

- schema: `globalcloud.cognee_p4_real_writeback_precheck_result.v1`
- status: `pass | hold`
- status_reason:
  - `pass`
  - `precheck_gate_not_reached`
- records: 与 `fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json` 的对齐结果
- summary:
  - `record_count`
  - `requested_write_count`
  - `precheck_pass_rate`
  - `owner_authorization_presence_rate`
  - `waes_pass_rate`
  - `runtime_dependency_ok_rate`
  - `rollback_readiness_rate`
  - `authorization_token_source_coverage`
  - `expected_blocked_reason_rate`
  - `marker_coverage`
  - `mean_saving_rate`
  - `pilot_gate_pass`

## 3. 字段校验命令

```bash
python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-precheck.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.json
```

## 4. 输出示例

`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.json`
