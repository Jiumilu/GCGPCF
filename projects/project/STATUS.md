---
doc_id: GPCF-PROJECT-STATUS-20261018
title: GlobalCloud PMC 状态
project: GPCF
related_projects: [GPCF, Project]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/project/STATUS.md
source_path: projects/project/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# GlobalCloud PMC 状态

- 路径：`../GlobalCloud PMC`；独立本地 Git 仓库，基于 Plane 社区版上游提交 `879ce8b5c6b4fe21efff4789a7062747f46d6383`，许可证为 AGPL-3.0。
- 主职责：团队研发协作；只读投影 GPCF Feature 与 Evidence 状态，不承担 GPCF 交付、验收或生产状态裁决。
- 项目级总体方案与实施方案：独立仓根目录沿用旧文件名 `GlobalCloud Project 总体方案.md`、`GlobalCloud Project 实施方案.md`，继承项目群双主控。
- Feature：F-028 已关闭；`overall_status=partial`。本机 Plane API 同步队列中 28 个 Feature（涉及 12 个已有 Feature 的项目），27 项创建、1 项更新；重复同步 F-028 更新同一工作项，GPCF 源文件哈希不变。证据见 `features/done/F-028-plane-gpcf-feature-evidence-integration/evidence/live-plane-api.json` 与 `evidence/live-plane-full-sync.json`；Plane 用户界面未验证。
- 本机验证实例已停机，临时容器卷和本次生成的凭据文件已清理；保留可重建的源码与验证结果。
- authorization：用户于 2026-10-18 授权本地立项、定制开发及仅本机开发环境凭据。
- confirmation：共享/生产实例写入、对外发布、`accepted`、`integrated`、`production_ready`、`customer_accepted` 尚未获得人工确认。
- 回滚：停用定制适配器与项目登记；GPCF 原始队列、Feature 和 Evidence 保持不变。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/project-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project project`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`
