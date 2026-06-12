---
doc_id: GPCF-DOC-670FDF1C79
title: GlobalCloud 绿色供应链体系测试与验证规范
project: WAES
related_projects: [GPC, WAES]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系测试与验证规范.md
source_path: 02-governance/GlobalCloud绿色供应链体系测试与验证规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系测试与验证规范

日期：2026-06-08
状态：测试与验证规范 v1
用途：定义从实现到联调前必须经过的验证层级，避免只有设计审计没有工程验证。

## 1. 验证分层

统一分为五层：

1. 单元验证
2. 模块验证
3. 仓库级验证
4. 跨系统联调验证
5. 运行前验证

## 2. 当前阶段要求

当前阶段是“首轮实施前验证准备”，因此至少必须补齐：

1. 仓库级验证入口
2. 运行前验证清单
3. 样本与证据要求

## 3. 运行前验证最小清单

当前体系重点验证项：

1. 连接器与接口可达性
2. 数据库权限与只读隔离
3. Event Bus / DLQ / Replay / 补偿
4. 知识发布、ingest、引用回指、失效拦截
5. AI 越权拦截与业务主账无写入

## 4. 验证结果要求

每条验证必须记录：

1. 验证目标
2. 环境
3. 输入样本
4. 执行方式
5. 结果
6. 证据位置
7. 是否阻塞状态升级

## 5. 禁止事项

1. 不得把“验证计划已写”当成“验证已通过”
2. 不得把 mock 结果写成真实运行结果
3. 不得把 isolated smoke 写成完整业务闭环通过
