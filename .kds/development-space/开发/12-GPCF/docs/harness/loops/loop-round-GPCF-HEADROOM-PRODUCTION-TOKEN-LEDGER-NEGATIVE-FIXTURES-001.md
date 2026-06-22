---
doc_id: GPCF-DOC-FFE428F629
title: LOOP Round GPCF Headroom Production Token Ledger Negative Fixtures 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-PRODUCTION-TOKEN-LEDGER-NEGATIVE-FIXTURES-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-PRODUCTION-TOKEN-LEDGER-NEGATIVE-FIXTURES-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Production Token Ledger Negative Fixtures 001

## 输入

- `fixtures/headroom/headroom-production-token-ledger-template.json`
- `docs/harness/evidence/headroom-production-token-intake-gate-20260621.json`

## 动作

1. 新增 `tools/kds-sync/evaluate_headroom_production_token_ledger.py`。
2. 新增 `fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json`。
3. 新增 `tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py`。
4. 验证 telemetry on、raw prompt、缺授权窗口、缺回滚和 marker gate 失败均被拒绝。

## 输出

- `tools/kds-sync/evaluate_headroom_production_token_ledger.py`
- `fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json`
- `tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py`

## 检查

| 检查项 | 结果 |
|---|---|
| case_count | 5 |
| rejected | 5 |
| production_admission_gate | false |

## 反馈

Headroom 已具备面向真实脱敏生产 token 台账的通用评估器和负向 fixture。当前仍无授权窗口和真实脱敏生产 token 台账，不升级 accepted、integrated 或 production_ready。
