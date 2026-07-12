---
doc_id: GPCF-OS-OPEN-SPEC-COVERAGE-DESIGN-20260712
title: design
project: GPCF
related_projects: [GPC, WAES, GPCF, ICP]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/enable-project-group-openspec-coverage/design.md
source_path: openspec/changes/enable-project-group-openspec-coverage/design.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

## Context

GPCF 已有 repo-local OpenSpec 规划空间和项目群包装技能，但项目覆盖信息分散，当前校验器混用了历史 17 项目基线与当前 18 项目集合。F-009 负责建立可机读覆盖事实源并将其接入 Feature、Loop、Evidence 与 Harness。

## Goals / Non-Goals

**Goals:**

- 以单一清单逐项描述 18 项目的 OpenSpec 策略。
- 为每个项目提供 GPCF 中央 OpenSpec 入口或显式豁免；本轮选择 6 个 required、12 个 conditional、0 个 waived。
- 让 validator 从当前项目事实源读取集合，不再硬编码 17。
- 生成可回放 Evidence 并由 Harness 保留最终裁决权。

**Non-Goals:**

- 不自动修改 18 个独立代码仓的业务代码。
- 不要求每个项目复制一套 OpenSpec 技能或配置。
- 不把历史 17 项目证据改写成 18 项目。
- 不执行提交、推送、部署、真实外部写入或状态提升。

## Decisions

1. 新增 `config/project-group-projects.yaml` 作为当前项目集合与稳定标识事实源。相比继续在多个 validator 中复制列表，该方式可消除集合漂移；历史证据仍保留自己的 17 项目口径。
2. 新增中央适用性矩阵，所有项目通过 GPCF `openspec/` 入口发起项目级或跨项目 change。相比向未知状态的 18 个独立仓批量落文件，中央入口可在当前授权范围内验证且避免污染用户仓库。
3. `required` 用于当前跨项目控制、事实、证据和主交付链项目；其余项目使用 `conditional`，在出现需求/架构/契约/安全/迁移类变更时启用。`conditional` 不是豁免。
4. 每行映射 `feature_project`、默认 Loop、Evidence Gate 与 Harness handoff；具体开发仍必须用 `gpcf_new_feature.py` 创建独立 Feature。
5. 新增专用 validator，并让既有当前覆盖 validator 读取同一事实源；历史命名含 `_17_scope` 的校验器仅在其确为历史证据时保留 17。

## Risks / Trade-offs

- [中央入口被误解为已修改全部项目仓] → 矩阵显式区分 `central_entry` 与 `project_repo_installation`，后者保持未执行。
- [conditional 被误写成 waived] → validator 要求 `required/conditional/waived` 枚举并要求 waived 提供理由和复核条件。
- [历史证据被当前口径污染] → 只修改当前状态/控制面 validator，不批量改写带日期的历史 evidence 正文。
- [OpenSpec 完成被误当验收完成] → 映射固定 `harness_handoff=required`，并禁止自动状态提升。

## Migration Plan

1. 建立 18 项目事实源和适用性矩阵。
2. 更新当前控制面 validator 读取 18 项目集合。
3. 运行专用 validator、既有门禁、Feature Evidence Gate 和文档治理。
4. 若失败，仅回滚 F-009 新增文件及本 change 对 validator 的修改；保留 ICP 第 18 项目登记事实。

## Open Questions

无。独立项目仓是否安装 repo-local OpenSpec 由后续项目 Feature 按需决定，不影响本轮中央入口覆盖。
