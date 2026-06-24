---
doc_id: GPCF-DOC-16DD6DC90F
title: GPCF 项目 Harness Manifest
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, Brain, XiaoC, XGD, XiaoG, GPCF]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/PROJECT_HARNESS_MANIFEST.md
source_path: PROJECT_HARNESS_MANIFEST.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF 项目 Harness Manifest

## 1. 项目基本信息

- 项目名称：GlobalCoud GPCF（绿色供应链体系文档工作区）
- 项目路径：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF`
- 仓库远端：`https://github.com/Jiumilu/GCGPCF.git`
- 当前分支：`main`
- 运行方式：纯 Markdown 文档体系
- 负责人：老卢 + Codex 智能体团队
- 当前状态：`not_started`
- 最近更新时间：2026-06-12

## 2. 项目目标

- 集中管理 GlobalCloud 绿色供应链体系的架构、治理、数据/AI、UI/交付、智能体团队、工作流等文档
- 作为体系级统一定义（0.0 节）的唯一基线来源
- 对项目群 12 个项目进行交叉分析、收口和治理状态跟踪

不属于本项目的内容：
- 不存放可执行代码（代码在各自项目仓库）
- 不直接修改其他项目文件（仅作为分析来源）

## 3. 边界声明

允许读取：
- 本项目内所有文件
- 项目群其他项目（只读分析）

允许写入：
- 本项目内所有 Markdown、配置、脚本
- `docs/harness/` 治理资产
- `openspec/` 规范定义

禁止访问或修改：
- 其他项目仓库的业务文件
- 生产配置、密钥

必须人工确认的动作：
- `git push`、合并
- 修改统一定义条款（0.0 节）

## 4. Harness 六层配置

### 4.1 运行环境层
- 工作目录：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF`
- 运行方式：纯文档（Markdown）
- 环境变量：无特殊要求

### 4.2 CLI 执行层
- 状态检查：`git status --short --branch`
- 结构验证：检查 00-index~08-evidence-samples 目录完整性
- 文档索引更新：手动维护 [00-index/README.md](00-index/README.md)

### 4.3 实时反馈层
- Git 状态：实时可用
- 项目群状态：通过交叉分析报告呈现

### 4.4 上下文管理层
- 统一定义基线：[00-index/README.md](00-index/README.md) 0.0 节
- 项目群分析：[01-architecture/GlobalCloud项目群交叉分析报告.md](01-architecture/GlobalCloud项目群交叉分析报告.md)
- 架构文档：[01-architecture/](01-architecture/)
- 治理规范：[02-governance/](02-governance/)
- 验收矩阵：[07-acceptance/](07-acceptance/)
- 证据样本：[08-evidence-samples/](08-evidence-samples/)
- 当前阻塞：项目群治理成熟度不均，仅 GFIS、XiaoC 有历史量化评分；状态升级仍需当前证据

### 4.5 工具集成层
- 文件系统：允许
- Git：允许
- 文档系统：本仓库 docs/

### 4.6 约束规则层
- 允许命令：`git status/diff/log/add/commit`
- 禁止命令：`git push --force`
- 安全规则：遵循 GlobalCloud Harness Engineering v1
- 合规规则：统一定义条款变更需要交叉影响分析

## 5. 完成定义

本项目标记为 `complete` 必须同时满足：
- 体系 0.0 统一定义条款与项目群实际状态一致
- 所有项目有完整的治理状态记录
- 交叉分析报告覆盖所有 12 个项目，并与项目主线对齐矩阵一致
- 人工确认点全部完成

## 6. 验收证据

证据存放位置：`docs/harness/evidence/`

## 7. 当前风险

| 风险 | 影响 | 处理方式 | 状态 |
| --- | --- | --- | --- |
| Brain/WIKI 冗余 | KDS 已为知识主存 | WIKI 已标注为镜像 | resolved |
| GPC docs 含 GFIS 文档 | 文档归属混淆 | GPC README 已标注 | resolved |
| XGD/XiaoG 无 Manifest | 治理缺口 | 已补充基础 Manifest | resolved |
| 项目群治理成熟度低 | 不可追踪交付进度 | 持续推进 | open |

## 8. 执行记录

| 日期 | 动作 | 证据 | 状态 |
| --- | --- | --- | --- |
| 2026-06-10 | 首轮 Harness 治理纳入 + 项目群交叉分析 | 交叉分析报告、各项目 Manifest | completed |
