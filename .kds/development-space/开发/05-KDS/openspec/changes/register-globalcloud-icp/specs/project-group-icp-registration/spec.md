---
doc_id: GPCF-OS-ICP-REGISTRATION-SPEC-20260712
title: spec
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF, ICP]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/register-globalcloud-icp/specs/project-group-icp-registration/spec.md
source_path: openspec/changes/register-globalcloud-icp/specs/project-group-icp-registration/spec.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

## 新增需求

### 需求：GC-ICP 登记为第18个项目
项目群必须把 GlobalCloud ICP 登记为第18个独立项目，同时不得改写历史17项目基线。

#### 场景：检查当前项目范围
- **当** 审查人员读取项目群总体方案和实施方案。
- **则** GlobalCloud ICP 以项目代码 ICP 和 candidate 状态出现，历史17项目证据保持不变。

### 需求：GC-ICP 职责保持有界
项目群必须把 GC-ICP 定义为产业模型、资源投影、场景编排和决策候选的责任项目，并明确禁止其承担业务事实写入、治理批准和生产执行。

#### 场景：审查职责边界
- **当** 审查人员比较 ICP 与 WAES、KDS、GPC、GFIS、PVAOS 的职责。
- **则** 各系统保持唯一责任边界，ICP 不具备源系统写入权限。

### 需求：登记必须保持候选状态
项目群必须把 ICP 登记为 candidate/partial/human_required，不得从本地测试推断 accepted、integrated、production_ready 或 customer_accepted。

#### 场景：本地测试已通过
- **当** ICP 契约、接口和样例数据测试通过。
- **则** 实施台账只记录开发证据，集成和验收继续保持待确认。

### 需求：ICP 必须具备控制状态入口
项目群必须维护 ICP 的总体方案、实施方案、状态、风险和路线图入口。

#### 场景：审计项目治理覆盖
- **当** 项目登记 validator 运行。
- **则** 所需 ICP 控制入口均存在，并指向独立项目方案。
