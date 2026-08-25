---
doc_id: GPCF-DOC-GCWORLD-034
title: GCWORLD工作台界面基础变更提案
project: GPCF
related_projects: [Studio, Brain, KDS, WAS, WAES, XWAIL]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-workbench-ui-foundation/proposal.md
source_path: openspec/changes/gcworld-workbench-ui-foundation/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## 变更原因

GCWORLD已经定义十二个工作中心和单一资产档案，但目前只有结构契约，没有真实产品界面。需要先形成以证据、世界状态和权限裁剪为核心的工作台界面提案，防止后续界面把候选、模拟或越权信息展示成事实。

## 变更内容

- 定义十二个工作中心的统一导航、页面层级和跨中心上下文保持要求。
- 定义单一资产档案、关系网络、项目世界、时间线、智能体、权限、模拟和审计的核心交互。
- 规定事实、运行、目标、模拟、候选、冲突和受限信息的中文视觉语义与解释路径。
- 将字段、段落、图节点与边、搜索、统计、导出和智能体回答统一纳入权限裁剪。
- 先以只读原型和固定契约数据验证信息架构；真实数据连接、跨租户共享和任何动作入口均需独立授权。
- 当前不修改Studio、Brain或其他产品仓库，不声称界面已实现、已集成或可上线。

## 能力范围

### 新增能力

- `gcworld-workbench-ui-foundation`：定义GCWORLD十二工作中心、单一资产档案、状态解释、权限裁剪和可访问性验证的工作台界面基础。

### 修改能力

无。

## 影响范围

- **Program / Release：** GKE‑001；`release_0`后续规划候选，实施前需获得新的产品实现授权。
- **Feature：** 暂由F‑013承载规划追踪；真实界面实施前必须建立或确认后继Feature。
- **当前目标仓库与责任方：** GPCF / GPCF，仅限本OpenSpec目录。
- **未来依赖：** Studio、Brain、KDS、WAS、WAES、XWAIL；产品仓库和责任人待独立授权。
- **基线：** 继承GCWORLD工作台结构契约，但无真实浏览器、搜索、API或数据链证据。
- **CodeGraph：** 仅声明未来 `GCWORLD视图模型→Studio工作台` 消费关系，不改变当前域关系。
- **非目标：** 不实现三维世界，不连接真实客户数据，不开放写操作，不建立新的人员或组织主账。
- **回滚：** 删除本次未提交的规划目录即可，不影响现有产品和数据。
