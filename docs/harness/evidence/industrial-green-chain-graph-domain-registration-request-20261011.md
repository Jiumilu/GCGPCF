---
doc_id: GPCF-DOC-IGL-GRAPH-DOMAIN-REGISTRATION-REQUEST-20261011
title: 工业绿链业务域（图谱只读投影）注册请求 2026-10-11
project: KDS
related_projects: [PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/industrial-green-chain-graph-domain-registration-request-20261011.md
source_path: docs/harness/evidence/industrial-green-chain-graph-domain-registration-request-20261011.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# 工业绿链业务域（图谱只读投影）注册请求 2026-10-11

## 1. 证据定位

本文登记 `IGL-GRAPH-DOMAIN-REGISTRATION-REQUEST-20261011`：**向项目群 registry 申报新增域切片注册条目**——工业绿链业务域（图谱只读投影），与 F-015（GCWORLD 组织域只读切片）并列。

本文只提交注册请求：不改 registry 本体、不声明受理/通过；不声明 WAES 授权或发布；不声明生产就绪或客户验收。

## 2. 请求内容

| 项 | 值 |
|---|---|
| requested_decision | admit_readonly_business_domain_slice_candidate |
| current_decision | accepted（2026-10-11 受理；见 §8） |
| 域名称（建议） | `GreenChainGraphBusinessDomain`（工业绿链业务域 · 图谱只读投影） |
| 载体 | `工业绿链/图谱/`（F-016 工作区：快照＋回执＋校验＋XWAIL 导出物） |
| 并列对象 | F-015（GCWORLD 组织域只读切片） |
| 源材料 | KDS《业务域注册请求草案 v0.1》《世界快照与只读消费接口契约 v0.1》《状态生命周期映射表 v0.1》 |

## 3. 绑定与政策遵循（registry `future_project_policy`）

| 政策项 | 声明 |
|---|---|
| admission_required | 遵循（本请求即 admission 输入） |
| must_bind_project_group_scope | 工业绿链（IGL）＋ KDS（F-016） |
| must_map_to_registry_categories | 六类目映射见 §4 |
| must_not_bypass_kds_waes_loop | 遵循；只读派生、零写回、`Trusted` 永不自行产生 |

## 4. 六类目映射（首期）

| 类目 | 图谱承载 |
|---|---|
| object | 快照 `objects.yaml`（85 对象/10 类型；术语回指 `sc:*`/`was_registry:*`） |
| relationship | 声明快照 `claims.yaml`（51 条；claim-rules-0.1；inference 显式候选） |
| event | `event` 类对象（`term-request:BusinessEvent` 另行登记） |
| evidence | `source_refs`＋revision；快照回执；导出包（manifest+receipt+digest，实跑核验） |
| state | 《状态生命周期映射表 v0.1》（4 态映射；`state-request:rejected` 缺口） |
| interface | 《世界快照与只读消费接口契约 v0.1》《查询与导出契约 v0.1》；XWAIL 导出物（O-2） |

## 5. 随附缺口请求

- `state-request:rejected`（registry state 词表扩展）。
- `term-request` ×8：Project / Person / Equipment / BusinessEvent / Risk / Decision / DependsOn / Blocks。

## 6. 门禁

| 项 | 值 |
|---|---|
| request_package_generated | true |
| submitted | true |
| registry_entry_added | true（登记件见 §8） |
| governance_reviewed | true |
| waes_authorized | false |
| accepted | true |
| integrated | false |
| production_ready | false |

## 7. 下一步

registry admission 流程裁定；受理后按六类目登记（不修改既有条目、不触碰 registry 既有 43 项）。

## 8. 受理记录（2026-10-11）

- **已受理（accepted）**：授权来源＝老卢「按推荐执行」（2026-10-11）；材料复核通过（六类目映射/政策遵循齐备）。
- 后续动作：登记动作**已完成**（2026-10-11）——域切片登记件 `business-domain-slice-registry-greenchain-graph-20261011`（候选边界保持；不修改 registry 既有条目）。
