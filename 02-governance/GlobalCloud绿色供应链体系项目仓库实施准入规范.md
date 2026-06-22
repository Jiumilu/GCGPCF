---
doc_id: GPCF-DOC-94AA31880F
title: GlobalCloud 绿色供应链体系项目仓库实施准入规范
project: WAES
related_projects: [GFIS, GPC, WAES, XiaoC]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系项目仓库实施准入规范.md
source_path: 02-governance/GlobalCloud绿色供应链体系项目仓库实施准入规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系项目仓库实施准入规范

日期：2026-06-08
状态：项目仓库实施准入规范 v1
用途：定义各专项何时允许进入真实项目仓库实施，以及进入后的最小控制要求。

## 1. 准入原则

进入真实仓库实施前，必须同时满足：

1. 专项边界已明确
2. 对应仓库路径已明确
3. 已完成只读预检
4. 已识别既有 dirty state
5. 已明确本轮允许写入范围

缺一项，不得开工实施。

## 2. 仓库实施前必做检查

必须记录：

1. `pwd`
2. `git status --short --branch`
3. `git remote -v`
4. `git branch --show-current`
5. 主要入口文件或实现落点

## 3. dirty state 规则

1. 既有 dirty state 默认视为用户或前序会话工作。
2. 不得覆盖、回滚、格式化或清理既有未授权改动。
3. 新改动必须与本次目标严格相关。

## 4. 分支与写入边界

1. 真实仓库实施必须在当前明确分支上进行，除非用户另行指定。
2. 一个专项不得无理由同时改多个仓库核心主段。
3. 跨仓库实施必须由小即统一收口。

## 5. 仓库实施后必须回写

1. 对应专项状态报告
2. 设计-实现追踪项
3. 交付物完成证据
4. 测试与验证结果
5. 阻塞项与风险项

## 6. 禁止事项

1. 不得未预检直接进入实施
2. 不得无准入结论直接改代码
3. 不得跨专项改动非本域核心边界
4. 不得把 Odoo 原型直接写成 GPC 已实现
5. 不得把 Edge 当作业务主账仓库
