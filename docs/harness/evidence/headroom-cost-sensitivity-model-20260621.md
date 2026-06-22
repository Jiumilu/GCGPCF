---
doc_id: GPCF-DOC-7EC36CDCAD
title: Headroom Cost Sensitivity Model
project: GPCF
related_projects: [GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md
source_path: docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom Cost Sensitivity Model

## Evidence ID

`HEADROOM-COST-SENSITIVITY-MODEL-20260621`

## 结论

本模型使用 15 项目 dry-run token 计数，在三组价格 profile 下复算 Headroom 成本节省稳定性。

`cost_sensitivity_gate | true`，`profile_count | 3`，`production_admission_gate | false`，`measured_production_tokens | false`。

## Profile 汇总

| profile_id | baseline_cost | headroom_cost | gross_saving | saving_rate | admission_gate |
|---|---:|---:|---:|---:|---|
| low_input_high_cache_discount | 125865.01 | 1320.93 | 124544.08 | 0.989505 | true |
| base_model | 292186.55 | 3066.15 | 289120.4 | 0.989506 | true |
| high_input_low_cache_discount | 584373.1 | 6132.3 | 578240.8 | 0.989506 | true |

## 边界

- 不写入供应商真实价格。
- 不使用真实生产 token 台账。
- 不声明 production token saving。
- 不升级 accepted、integrated 或 production_ready。
