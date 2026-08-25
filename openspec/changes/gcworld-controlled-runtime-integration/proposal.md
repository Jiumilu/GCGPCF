---
doc_id: GPCF-DOC-GCWORLD-040
title: GCWORLD受控运行时集成变更提案
project: GPCF
related_projects: [XWAIL, WAES, KWE, MMC, KDS, GFIS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-controlled-runtime-integration/proposal.md
source_path: openspec/changes/gcworld-controlled-runtime-integration/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## 变更原因

GCWORLD世界运行闭环目前只有结构Schema与固定样例，尚无真实服务、授权裁决、人工确认、连接器执行和回执链。需要先规划一个默认无外部副作用、可从镜像模式逐级授权的运行时集成，确保任何真实行动都能被阻断、追溯和撤销。

## 变更内容

- 定义世界注册、身份解析、投影、上下文、事件、智能体、裁决、确认、行动、证据和查询服务的集成边界。
- 定义观察、解析、快照、推理、裁决、确认、执行、取证、提升和学习的不可跳步运行协议。
- 要求所有写命令具备幂等、因果、关联、版本、重试、死信、补偿和不可变回执。
- 建立R0—R4风险门禁、人工确认、职责分离、紧急冻结、撤销传播和降级只读策略。
- 采用阶段开关：首先仅允许本地镜像与建议，真实内部写入、外部执行和重大行动分别需要新的独立授权。
- 当前不启动运行服务，不调用KDS、MMC、GFIS或其他外部系统，不产生真实授权或业务动作。

## 能力范围

### 新增能力

- `gcworld-controlled-runtime-integration`：定义GCWORLD多服务运行闭环、风险分级、裁决确认、可靠执行、回执补偿和分阶段授权集成。

### 修改能力

无。

## 影响范围

- **Program / Release：** GKE‑001；`release_0`后续规划候选，运行实现必须进入独立批准的Release阶段。
- **Feature：** 暂由F‑013承载规划追踪；真实运行时实施前必须建立或确认后继Feature。
- **当前目标仓库与责任方：** GPCF / GPCF，仅限本OpenSpec目录。
- **未来依赖：** XWAIL、WAES、KWE、MMC、KDS、GFIS及业务系统；接口和责任人待独立授权。
- **基线：** 继承GCWORLD世界运行时结构契约；真实执行、授权和外部写入证据均为0。
- **CodeGraph：** 仅声明未来服务调用与事件关系，不修改现有GKE‑001域绑定。
- **非目标：** 不直接实现有限自治，不绕过WAES或业务系统，不把GCWORLD建设为业务主账。
- **回滚：** 删除本次未提交的规划目录即可，不影响任何运行服务或业务状态。
