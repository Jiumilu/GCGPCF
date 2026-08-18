---
doc_id: GPCF-DOC-82B83BA05C
title: design
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/integrate-gke001-openspec-codegraph/design.md
source_path: openspec/changes/integrate-gke001-openspec-codegraph/design.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

## Context

GKE-001 是项目群一级工程域，不是一个独立 Git 仓库。它已经由 GPCF/F-013 控制 canonical，KDS 持有知识事实，MMC 提供身份授权，Studio 提供客户工作台，Brain 提供受控分析，并通过应用路线图管理 Release 0 至 Release 3。当前 OpenSpec 入口只包含通用 Feature 规则，CodeGraph registry 只表达 14 个真实仓库，无法直接查询 GKE-001 的 Program、Feature、Release、仓库职责和证据依赖。

受影响 stakeholder 包括 GPCF/F-013、KDS、MMC、Studio、Brain、业务权威系统、能力消费项目、OpsX 和 Harness。实现必须保持 KDS 单一知识主存、MMC 授权边界、F-013 独立验收以及 `active / partial / not_complete` 状态上限。

## Goals / Non-Goals

**Goals:**

- 为 GKE-001 建立 OpenSpec Program 级机器绑定，并连接 F-013、canonical hash、应用路线图、Release 和 handoff。
- 为 GKE-001 建立 CodeGraph engineering-domain binding，并连接现有 14 仓 registry、18 项目职责、关键文档、契约、能力和证据。
- 提供确定性 validator 和本地 CodeGraph evidence，证明纳管结构可解析、可查询且没有状态越权。
- 将新文档纳入文控、本地 KDS 开发空间镜像、Feature evidence 和 Harness handoff 边界。

**Non-Goals:**

- 不把 GKE-001 伪装成第 15 个 Git 仓库，也不修改 14 仓覆盖基线。
- 不修改 KDS、MMC、Studio、Brain 或业务系统产品源码。
- 不执行真实 KDS/MMC 调用、客户 E2E、部署、发布或状态提升。
- 不在本 change 内归档主规格或声明 accepted/integrated/production_ready/customer_accepted。

## Decisions

### 1. GKE-001 使用 engineering-domain binding，不新增 repository entry

在 `governance/codegraph/gke001-engineering-domain-binding.yaml` 中表达 GKE-001 节点、仓库职责、Program/Feature/Release、契约和 evidence edges，并在 repo registry 增加 `engineering_domains` 引用。

选择原因：CodeGraph registry 的 `repo_count: 14` 表示真实 Git 仓库覆盖。把 GKE-001 加成仓库会破坏既有证据和 live status 语义。

替代方案：新增虚拟仓库。拒绝，因为它没有独立 `.git`、`.codegraph` 和产品运行时。

### 2. OpenSpec 使用独立 Program binding 并增强全局 context

新增 `governance/openspec/gke001-program-binding.yaml`，固定 coordinator、F-013、manifest、路线图、Release、项目范围、OpsX/Harness 和授权边界；同时在 `openspec/config.yaml` 中增加 GKE-001 变更必须引用该 binding 的规则。

选择原因：OpenSpec change 仍按仓库和 Feature 工作，Program binding 提供跨 change 的稳定上位关系，不要求把所有实现塞入一个长期 change。

替代方案：仅依赖 F-013 `feature.yaml`。拒绝，因为它不能直接表达每个 OpenSpec change 的 Program/Release/CodeGraph 影响关系。

### 3. Validator 验证结构，不把索引存在当成运行完成

新增确定性 validator，检查两个 binding、registry、实施方案、路线图 hash、OpenSpec change/spec/tasks、18 项目范围、14 仓引用和所有状态提升授权为 false。CodeGraph evidence 只记录 `sync/status/query` 的本地结果。

选择原因：图谱节点存在只能证明代码智能纳管，不能证明 API、客户任务或生产状态。

### 4. Feature 和 evidence 继续绑定 F-013

本 change 的文档、validator 和 evidence 进入 F-013 evidence gate；最终验收仍由 Harness/F-013 执行。OpenSpec strict 通过只代表 apply-ready 或规格有效。

## Risks / Trade-offs

- [Risk] 工程域 binding 与 14 仓 live registry 被误认为同一计数 → 保持 `repo_count: 14`，将 GKE-001 放入独立 `engineering_domains`。
- [Risk] CodeGraph 可查询被误报为产品集成 → evidence 固定 `simulated_only / governance_only / not_complete`，禁止真实运行状态提升。
- [Risk] 路线图或 canonical hash 漂移 → validator 每次读取并重新计算 SHA-256。
- [Risk] 18 项目职责与实际仓库覆盖不同 → binding 分开记录 `project_scope` 和 `indexed_repositories`。
- [Risk] 并发工作树污染本 change → validator 使用精确路径，handoff 记录外部 dirty scope，不回滚或混入。

## Migration Plan

1. 建立 OpenSpec change、两个 capability specs 和任务清单。
2. 新增 GKE-001 OpenSpec Program binding。
3. 新增 CodeGraph engineering-domain binding，并在 14 仓 registry 中登记引用。
4. 新增 validator 和正负 fixture/证据要求。
5. 执行 OpenSpec strict、validator、CodeGraph sync/status/query、文控和 Feature Evidence Gate。
6. 形成 Harness handoff；不自动 archive 或提升状态。

回滚时仅删除本 change、两个 binding、registry 工程域引用、validator 和本轮 evidence；保留现有 14 仓 registry、`.codegraph` 数据和产品代码。

## Open Questions

- 后续是否把 GKE-001 binding 同步到各产品仓的本地 OpenSpec config，由对应 Release Feature 单独决策，不在本 change 自动扩张。
- CodeGraph 跨仓联邦查询能力升级后，是否将当前静态 repository edges 替换为统一跨仓 node IDs，由后续独立 change 处理。
