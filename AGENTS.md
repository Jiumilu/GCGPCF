---
doc_id: GPCF-DOC-37DD68363F
title: AGENTS
project: WAES
related_projects: [WAES, GPCF]
domain: general
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/04-WAES/AGENTS.md
source_path: AGENTS.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

## GlobalCloud 项目群总控体系识别规则

GlobalCloud 项目群存在两个必须识别的总控体系：

1. GlobalCloud 项目群总体方案体系
主文件：`GlobalCloud 项目群总体方案.md`
定位：项目群最高层总体控制性方案，负责项目群架构、术语、版本、兼容矩阵、方案传导、项目边界与协同控制。

2. GlobalCloud 项目群实施方案体系
主文件：`GlobalCloud 项目群实施方案.md`
定位：项目群唯一实施控制性方案，负责真实进度、真实研发、真实运行、真实集成、真实交付、客户验收、任务包、命令、证据、门禁、回滚和 LOOP 闭环。

所有项目级总体方案必须继承项目群总体方案。
所有项目级实施方案必须继承项目群实施方案。
项目级方案变化必须回传项目群主方案，并按影响范围传导到关联项目。
未经人工确认，不得声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

## LOOP 输出克制规则

整个项目群及 LOOP 运行必须严格遵守：

```text
DO NOT send optional commentary
```

除必要的结论、阻塞项、授权确认请求、执行结果和验证证据外，不得输出可选过程性说明。需要授权或确认的事项必须以明确确认请求呈现，不得用可选 commentary 替代。
