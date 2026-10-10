---
doc_id: GPCF-SPACEAI-STATUS-20261010
title: SpaceAI 状态
project: GPCF
related_projects:
- SpaceAI
- GPCF
domain: governance
status: controlled
version: v1.0
owner: 老卢
kds_space: 开发
kds_path: 开发/SpaceAI/projects/spaceai/STATUS.md
source_path: projects/spaceai/STATUS.md
sync_direction: local_only
last_reviewed: '2026-10-10'
supersedes: []
superseded_by: []
---

# SpaceAI 状态

- 路径：`../GlobalCloud SpaceAI`；角色 external；Windows/.NET 桌面工程，入口 MB3000.sln。
- 私有仓库：`https://github.com/Jiumilu/GCSpaceAI`，main。
- project_status: registered；overall_status: partial。
- authorization: user_authorized_onboarding_and_git_2026-10-10。
- confirmation：业务验收、生产发布未确认。
- Git 基线仅纳管文件；历史源码存在疑似凭据，保留本地且未提交/上传。
- 当前 macOS 缺 Windows/.NET 构建工具，未声明构建、运行、集成或生产通过。
- 证据：`../GlobalCloud SpaceAI/docs/harness/onboarding-2026-10-10.md`。
- 下一步：凭据清理后源码入库，在 Windows 上构建并核验产品业务与设备依赖。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/spaceai-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project spaceai`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## Git 回读

- 私有 origin 已创建，main 已推送；初始提交 `480c59bb172afc68236edc2299d1998bfc27807e`。
- 初始提交仅 6 个纳管文件；原源码因疑似凭据保留本地、未上传。
- 技能链和 OpenSpec 覆盖按并行新增后的 21 项目通过；Loop 文档门禁 pass。
- 默认 frontmatter 检查发现健康报告受保护 related_projects 变更，主权工具收口待完成；overall_status 仍为 partial。
