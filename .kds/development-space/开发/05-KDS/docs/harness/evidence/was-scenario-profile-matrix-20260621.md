---
doc_id: GPCF-DOC-1F7DEFD3F1
title: WAS Scenario Profile Matrix Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-scenario-profile-matrix-20260621.md
source_path: docs/harness/evidence/was-scenario-profile-matrix-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# WAS Scenario Profile Matrix Evidence

## 结论

`GPCF-ONTOLOGY-WAS-SCENARIO-PROFILE-MATRIX-001` 已建立覆盖整个 GlobalCloud 项目群和绿色供应链全链路的 WAS scenario profile matrix。

本轮只建立语义剖面矩阵、正负夹具和 validator，不创建真实 source-of-record，不写 GFIS/KWE runtime，不创建 WAES review，不升级 accepted、integrated 或 production_ready。

## 覆盖指标

| 指标 | 当前值 |
|---|---:|
| project_group_scope | `14/14` |
| scenario_profiles | `10` |
| asset_dimensions | `8/8` |
| flows | `8/8` |
| green_supply_chain_links | `10/10` |
| positive_fixtures | `1` |
| negative_fixtures | `3` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| waes_review | `0` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 项目群范围

GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC、XGD、XiaoG、MMC、GPCF、Studio、WAS。

## 绿色供应链链路

- customer_order
- supplier_procurement
- production_work_order
- quality_inspection
- logistics_delivery
- energy_consumption
- carbon_footprint
- settlement_profit
- knowledge_reference
- recycling_circular

## Scenario Profiles

| profile_id | 作用 |
|---|---|
| GFIS-RUNTIME-SOP-E2E | GFIS runtime SOP E2E 语义剖面 |
| KDS-CANDIDATE-PROMOTION | KDS candidate promotion 语义剖面 |
| WAES-LOOP-CLOSURE | WAES gate 与 Loop closure 语义剖面 |
| RAG-STRONG-REFERENCE-ADMISSION | RAG strong reference admission 语义剖面 |
| GFIS-KWE-WRITEBACK-PRECHECK | GFIS/KWE writeback precheck 语义剖面 |
| ELEVEN-POOLS-LINKAGE | 11 Pools semantic linkage 语义剖面 |
| GREEN-SUPPLY-CHAIN-ORDER-TO-DELIVERY | 订单到交付链路 |
| ENERGY-CARBON-ACCOUNTING | 能源与碳核算链路 |
| SETTLEMENT-PROFIT-GOVERNANCE | 结算与收益治理链路 |
| RECYCLING-CIRCULAR-GOVERNANCE | 回收与循环治理链路 |

## 验证命令

```bash
python3 tools/kds-sync/validate_was_scenario_profile_matrix.py
```

## 下一轮

推荐下一轮：`GPCF-ONTOLOGY-WAS-WAES-KDS-RAG-WRITEBACK-GATE-PACK-001`。

该下一轮应建立 WAES gate input、KDS binding、RAG strong reference、GFIS/KWE writeback 和 11 Pools pool_link 的分阶段门禁包；仍不得声明业务上线。
