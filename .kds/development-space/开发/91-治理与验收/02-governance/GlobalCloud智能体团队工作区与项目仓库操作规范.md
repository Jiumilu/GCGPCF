---
doc_id: GPCF-DOC-39A8CE7FE1
title: GlobalCloud智能体团队工作区与项目仓库操作规范
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, Brain, XiaoC, XGD, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud智能体团队工作区与项目仓库操作规范.md
source_path: 02-governance/GlobalCloud智能体团队工作区与项目仓库操作规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud智能体团队工作区与项目仓库操作规范

日期：2026-06-08
状态：工作区与仓库操作规范 v1

## 1. 目的

本规范用于明确：

1. 哪些工作在总控工作区做
2. 哪些工作必须进真实项目仓库做
3. 什么时候允许从总控层切到项目层
4. 进入项目仓库后必须执行什么 preflight
5. 离开项目仓库后必须回写什么台账

## 2. 双层工作机制

### 2.1 总控工作区

位置：

- `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`

主责：

1. 总体架构
2. 文档基线
3. 控制塔
4. PMBOK 台账
5. 周报
6. 风险、阻塞、状态控制
7. Linear 汇总

### 2.2 项目仓库层

典型仓库：

1. `WAES`
2. `PVAOS`
3. `GFIS`
4. `GPC`
5. `Brain`
6. `XiaoC`
7. `Hermes`
8. `XGD`

主责：

1. 仓库预检
2. 实现落点确认
3. 代码/配置修改
4. 本地运行与仓库级验证

## 3. 总控工作区允许事项

1. 方案设计
2. 专项汇总
3. 控制台账维护
4. 目标、计划、风险、阻塞管理
5. 评估与审计

禁止事项：

1. 用总控文档替代真实仓库证据
2. 在未进仓库时声称实现已经确认

## 4. 项目仓库允许事项

### 4.1 默认允许

1. `pwd`
2. `git status --short --branch`
3. `git remote -v`
4. `git branch --show-current`
5. 目录与实现落点只读检查
6. 运行入口与脚本只读检查

### 4.2 明确批准后允许

1. 最小代码修改
2. 配置修改
3. 本地运行
4. 验证脚本执行

## 5. 进入项目仓库前置条件

进入真实项目仓库前，必须满足：

1. 专项责任域已明确
2. 仓库路径已明确
3. 本轮目标已明确
4. 已知禁止事项已明确

## 6. 进入项目仓库后的固定 preflight

每次进入真实仓库，至少执行：

```bash
pwd
git status --short --branch
git remote -v
git branch --show-current
```

必要时补：

```bash
git diff --stat
rg --files
```

## 7. 仓库层状态纪律

1. 仓库 dirty state 必须保留
2. 未明确批准前默认只读
3. 不得覆盖既有改动
4. 不得把只读预检直接写成联调完成

## 8. 从仓库层回写总控层要求

每次仓库动作完成后，必须至少回写：

1. 仓库路径
2. 当前分支
3. remote
4. dirty state 摘要
5. 已确认实现落点
6. 未确认事项
7. 当前状态建议
8. 下一步动作

## 9. 当前适用判断

当前阶段已经从：

- “实施前准备收口”

进入：

- “6 个专项正式只读预检完成”
- “首轮实施前验证准备”

因此当前主要求是：

1. 继续在仓库层补运行前样本入口
2. 持续回写总控层
3. 不得跳过环境门和状态门
