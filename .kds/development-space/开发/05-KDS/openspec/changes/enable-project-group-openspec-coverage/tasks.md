---
doc_id: GPCF-OS-OPEN-SPEC-COVERAGE-TASKS-20260712
title: tasks
project: KDS
related_projects: [WAES, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/enable-project-group-openspec-coverage/tasks.md
source_path: openspec/changes/enable-project-group-openspec-coverage/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

## 1. 当前项目事实源与覆盖矩阵

- [x] 1.1 建立包含 18 个当前项目的单一项目事实源，并区分历史 17 项目基线。
- [x] 1.2 建立逐项目 OpenSpec required/conditional/waived 矩阵及中央入口或豁免字段。
- [x] 1.3 为 18 个项目登记 Feature、Loop、Evidence 和 Harness 映射。

## 2. 项目入口与 Loop 路由

- [x] 2.1 在每个 `projects/<project>/STATUS.md` 登记 OpenSpec 策略和中央入口。
- [x] 2.2 更新 GlobalCloud OpenSpec 治理技能和 Loop 编排器，引用 18 项目矩阵与专用验证器。

## 3. 门禁修复与测试

- [x] 3.1 修复当前项目元数据覆盖 validator，使全部当前控制文档使用 18 项目事实源。
- [x] 3.2 修复 Loop 工程主方案 validator 的 17 项目硬编码口径。
- [x] 3.3 新增并运行 18 项目 OpenSpec 覆盖 validator，验证唯一性、入口/豁免和 Feature/Loop 映射。
- [x] 3.4 运行相关 Python 编译、回归门禁和 `git diff --check`。

## 4. Evidence 与文档治理

- [x] 4.1 更新 F-009 journal、evidence 和 Evidence Gate 回放结果。
- [x] 4.2 运行文档台账、KDS 本地镜像、污染、TOKEN 与 Loop 文档门禁。
- [x] 4.3 记录回滚边界和 Harness 人工确认边界；不执行状态提升、提交、推送或部署。
