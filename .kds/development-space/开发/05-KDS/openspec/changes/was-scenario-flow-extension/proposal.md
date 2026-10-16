---
doc_id: GPCF-DOC-25EB2F876F
title: proposal
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/was-scenario-flow-extension/proposal.md
source_path: openspec/changes/was-scenario-flow-extension/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

## 变更原因

GCWORLD 总体架构 V1.0.1（KDS，2026-10-16）已按老卢 2026-10-16 裁定，把「场景流 ScenarioFlow」确立为第九流；而 WAS 契约层当前仍为 8+8 基线——存在「文档已用、体系未承接」的未闭合项。《WAS 总体方案 v1.3.0》U16 条款明确：理论层采纳「资产维度／资产流为开放集合」，契约层保留 8+8 基线，**扩展走版本化**。本变更按该版本化路径把场景流正式承接进 WAS 体系。

本变更不改变八流基线语义、不重命名任何既有术语、不替 WAS 私定内部映射；所有下游影响按 WAS 仓《AGENTS.md》跨项目变更协议以六项声明给出（见 design.md §3）。

## 变更内容

- 登记「场景流 ScenarioFlow」为 WAS 流集合的受控兼容扩展（candidate）：产出《场景流扩展登记草案》（含定义单源、与八流/八维关系、六项兼容性声明、未决项与引用口径）。
- 建立 capability 规范 `was-scenario-flow-extension`：规定扩展登记、兼容性声明、版本化纳入路径与提前引用防护要求。
- 完成文档登记与镜像（`document_control.py` 增量 scope 运行）。
- （后续 tasks 跟踪）WAS 主方案扩展记录、XWAIL `flowType` 影响评估流转、WAME 登记位确认、KDS GCWORLD V1.0.1 注记回填。

## 能力范围

### 新增能力

- `was-scenario-flow-extension`：场景流的受控扩展登记、兼容性声明与版本化纳入路径规范。

### 修改能力

无。八流基线、八维、三层资产与生命周期定义均不变。

## 影响范围

- **项目群与发布阶段：** WAS 体系（v1.3.x 候选扩展）；不绑定 GKE-001 或其他 Release 状态变化。
- **功能包：** F-022 `was-scenario-flow-extension`（新建，2026-10-16）；不改变任何既有 Feature 状态。
- **仓库与责任方：** WAS（承接主体）／GPCF（治理登记与证据）／KDS（事实来源，只读）。
- **当前基线：** WAS v1.3.0（2026-10-12 转正）；GCWORLD V1.0.1（2026-10-16）。
- **允许范围：** 本 OpenSpec 变更、登记草案、文档登记与镜像、术语一致性验证证据。
- **禁止范围：** 修改八流/八维/三层资产/生命周期定义；XWAIL 契约与 WAME 登记的实际改写（仅声明与建议流转）；任何 accepted / integrated / production_ready / customer_accepted 声明。
- **依赖关系：** WAS 治理复核（承接方式确认）；XWAIL 侧 `flowType` 影响评估。
- **非目标（Non-goals）：** 八流旧名→V1.2 迁移表（仍为 WAS 独立交付物）；场景流的实现与运行时代码；GCWORLD 运行时变更。
- **CodeGraph 影响：** 不改变源码关系。
- **回滚边界：** 登记件可标记 superseded 或撤回（不删除）；镜像与登记可逆向同步；无运行时影响。
