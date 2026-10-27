---
doc_id: GPCF-DOC-F022-OWNER-PACK-20261024
title: F-022 WAS 属主动作包
project: GPCF
related_projects: [WAS]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-022-was-scenario-flow-extension/evidence/owner-action-pack-20261024.md
source_path: features/active/F-022-was-scenario-flow-extension/evidence/owner-action-pack-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-022 WAS 属主动作包

## 你需要决定（3 项）

1. 场景矩阵是否升为 WAS v1.2 **9 流**（补 `ValueFlow`、`CreditFlow`）？
2. `spacetime_flow` 映射 `ScenarioFlow`，还是保留为 `SpaceTimeDimension` 维度、不进入流集合？
3. `knowledge_flow` 并入 `InformationFlow` 后，矩阵 `required_flows` 是否允许去重？

## 你需要签署（1 项）

- 六项兼容声明（WAS 基线 v1.3.0 / Ontology 新增术语 / XWAIL 已支持 / AaaS 无变更 / WAME 登记位 / compatible）。

## 证据

- 映射请求：`features/done/F-023.../evidence/flow-mapping-decision-request-20261024.md`
- 复核请求：`evidence/was-review-request-20261024.md`
- XWAIL 评估：`evidence/xwail-impact-assessment-20261024.md`
- D 当前状态：场景流为 candidate；XWAIL ALLOWED_FLOWS 已含 ScenarioFlow。

## 签完后 GPCF 动作

1. 更新 F-022 blockers 为空并留 resolved 证据；
2. `python3 scripts/gpcf_check_evidence.py --check-only F-022`；
3. `python3 scripts/gpcf_close_feature.py F-022`（需授权）；
4. 不声明 accepted/integrated/production_ready。

## 风险

- 若选 9 流，需评估 Value/Credit 在场景矩阵中的语义覆盖；
- 若保留 SpaceTimeDimension 独立，需更新 F-023 映射表与 loop context。
