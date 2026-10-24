---
doc_id: GPCF-DOC-F023-FLOW-MAPPING-REQUEST-20261024
title: F-023 流命名映射决策请求（场景矩阵批 1）
project: GPCF
related_projects: [WAS, XWAIL]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-023-was-flow-naming-migration/evidence/flow-mapping-decision-request-20261024.md
source_path: features/done/F-023-was-flow-naming-migration/evidence/flow-mapping-decision-request-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# 流命名映射决策请求

## 现状

`validate_was_scenario_profile_matrix.py` 与 evidence/fixture 仍用旧八流名；WAS v1.2 已发布九流命名。

## 建议映射

| 旧名 | V1.2 |
|---|---|
| material_flow | LogisticsFlow |
| information_flow | InformationFlow |
| capital_flow | FinancialFlow |
| energy_flow | EnergyFlow |
| commerce_flow | ServiceFlow |
| rule_flow | ControlFlow |
| knowledge_flow | InformationFlow（合并） |
| spacetime_flow | ScenarioFlow（运行层） |

## 需 WAS 属主确认

1. 场景矩阵是否升为 **9 流**（补 `ValueFlow`、`CreditFlow`）？
2. `spacetime_flow` 是否映射 `ScenarioFlow`，还是保留为维度 `SpaceTimeDimension` 不进入流集合？
3. `knowledge_flow` 合并后，场景矩阵的 `required_flows` 是否允许重复/去重？

## 影响面（确认后执行）

- `tools/kds-sync/validate_was_scenario_profile_matrix.py` 的 `FLOWS`
- `docs/harness/evidence/was-scenario-profile-matrix-20260621.json`（required_flows + profiles）
- `docs/harness/evidence/was-scenario-profile-matrix-20260621.md`
- `docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-SCENARIO-PROFILE-MATRIX-001.md`
- `fixtures/was/scenario-profile-matrix-positive.json` + 3 negative

## 非声明

- 不声明映射已批准；本轮不改文件。
