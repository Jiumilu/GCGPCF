---
doc_id: GPCF-DOC-DOMAIN-SLICE-REGISTRY-GREENCHAIN-GRAPH-20261011
title: 业务域切片登记（GreenChainGraphBusinessDomain）· 2026-10-11
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/business-domain-slice-registry-greenchain-graph-20261011.md
source_path: docs/harness/evidence/business-domain-slice-registry-greenchain-graph-20261011.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# 业务域切片登记（GreenChainGraphBusinessDomain）· 2026-10-11

## 1. 登记定位

本文登记 `GPCF-DOMAIN-SLICE-REGISTRY-GREENCHAIN-GRAPH-20261011`：按 WAS 项目群 registry `future_project_policy`（admission_required／scope binding／六类目映射／不绕 KDS-WAES loop），将**工业绿链业务域（图谱只读投影）**登记为域切片条目（候选），与 F-015（GCWORLD 组织域只读切片）并列。

- 上游：`industrial-green-chain-graph-domain-registration-request-20261011`（**已受理 accepted，2026-10-11**）。
- 基础 registry：`was-project-group-ontology-registry-20260621.json`（**既有 43 条一字未动**）。
- 登记状态：`business_domain_slice_registered_candidate`（候选：零写回、零运行状态提升）。

## 2. 域切片条目

| 项 | 值 |
|---|---|
| 名称 | `GreenChainGraphBusinessDomain`（工业绿链业务域 · 图谱只读投影） |
| 载体 | `工业绿链/图谱/`（快照＋回执＋校验＋XWAIL 导出物） |
| scope 绑定 | 工业绿链（IGL）＋ KDS（F-016） |
| 六类目映射 | object=快照 objects｜relationship=claims｜event=event 类｜evidence=source_refs+回执+导出包｜state=生命周期映射表｜interface=快照契约+导出物 |
| 并列 | F-015（GCWORLD 组织域只读切片） |

## 3. 随附请求（缺口登记）

- `state-request:rejected`（registry state 词表扩展，待评审）
- `term-request` ×8：Project／Person／Equipment／BusinessEvent／Risk／Decision／DependsOn／Blocks

## 4. 边界（候选保持）

| 项 | 值 |
|---|---|
| real_source_records | 0 |
| runtime_primary_key_ready | 0 |
| waes_review | 0 |
| accepted | false |
| integrated | false |
| production_ready | false |
| runtime_write | false |
| kds_api_write | false |

## 5. 非声明

- 本登记为**域切片注册条目（候选）**：不是运行授权、不是知识库、不替代 KDS source-of-record。
- 不修改 `20260621` registry 既有 43 条；不改写任何来源台账；零写回、零运行状态提升。

## 6. 复核

```bash
python3 tools/kds-sync/validate_business_domain_slice_registry_greenchain_graph.py
```
