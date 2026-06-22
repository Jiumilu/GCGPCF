---
doc_id: GPCF-DOC-68EE4EAB95
title: LOOP Round GPCF Headroom Cost Sensitivity Model 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-COST-SENSITIVITY-MODEL-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-COST-SENSITIVITY-MODEL-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Cost Sensitivity Model 001

## 输入

- `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json`
- `docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.json`

## 动作

1. 新增 `tools/kds-sync/build_headroom_cost_sensitivity_model.py`。
2. 新增 `tools/kds-sync/validate_headroom_cost_sensitivity_model.py`。
3. 用 low/base/high 三组价格 profile 复算 15 项目 token 成本。
4. 校验所有 profile 的 saving_rate 均满足 L2 阈值，同时保持 production gate false。

## 输出

- `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json`
- `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md`
- `tools/kds-sync/build_headroom_cost_sensitivity_model.py`
- `tools/kds-sync/validate_headroom_cost_sensitivity_model.py`

## 检查

| 检查项 | 结果 |
|---|---|
| profile_count | 3 |
| project_count | 15 |
| all_profiles_admission_gate | true |
| cost_sensitivity_gate | true |
| production_admission_gate | false |
| measured_production_tokens | false |

## 反馈

Headroom 成本模型已具备价格敏感性复算证据。当前仍不写入供应商真实价格、不使用真实生产 token 台账、不声明 production token saving。
