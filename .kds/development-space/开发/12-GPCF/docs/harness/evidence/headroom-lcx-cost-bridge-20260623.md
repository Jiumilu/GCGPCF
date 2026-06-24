---
doc_id: GPCF-DOC-HEADROOM-LCX-COST-BRIDGE-20260623
title: Headroom LCX Cost Bridge Evidence
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-cost-bridge-20260623.md
source_path: docs/harness/evidence/headroom-lcx-cost-bridge-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Cost Bridge Evidence

## Evidence ID

`HEADROOM-LCX-COST-BRIDGE-20260623`

## 结论

本证据只把 cost model、三窗口 loop cost observation series、independent replay 和 metadata replay 连接成 replay only 成本桥接层。
它不产生真实生产 token 结论，也不打开 production branch。
status: cost_bridge_defined_replay_only

## 支撑证据

- `cost_sensitivity_model`: `HEADROOM-COST-SENSITIVITY-MODEL-20260621`
- `loop_cost_observation_series`: `HEADROOM-LOOP-COST-OBSERVATION-SERIES-20260621`
- `independent_replay`: `HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-20260621`
- `metadata_replay_check`: `HEADROOM-LCX-METADATA-REPLAY-CHECK-20260622`

## 当前状态

| bridge_mode | `replay_only` |
| cost_sensitivity_gate | `true` |
| series_gate | `true` |
| independent_round_gate | `true` |
| metadata_replay_gate | `true` |
| production_token_measurement_allowed | `false` |
| measured_production_tokens | `false` |
| production_admission_gate | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 非声明

- 本证据不表示真实测量已执行。
- 本证据不表示真实业务等价性已证明。
- 本证据不表示生产代理或生产 SDK 已启用。
- 本证据不表示 accepted、integrated 或 production_ready。
