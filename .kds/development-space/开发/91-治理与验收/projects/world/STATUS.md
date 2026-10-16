---
doc_id: GPCF-WORLD-PROJECTS-WORLD-STATUS-MD-20261016
title: World 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/world/STATUS.md
source_path: projects/world/STATUS.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

# World 状态

- 路径：`../GlobalCloud World`；角色 external；工程初始化，技术栈和业务边界待定。
- 私有远端目标：`https://github.com/Jiumilu/GCWorld`，main。
- project_status: registered；overall_status: partial。
- authorization：用户于 2026-10-16 授权纳管、本地建仓和私有远端初始同步。
- confirmation：业务验收、生产发布未确认。
- 本次 Feature：F-021，独立建仓不迁移 Studio F-015 或 KDS 主账。
- 既有相关成果：F-015（Studio，blocked）；gcworld-evidence-twin-foundation；gcworld-kds-authoritative-integration。
- 纳管前中央文档门禁：rework_required；6 项 missing_metadata 与既有检查失败。历史 18 项运行快照不改写为 22 项实测。
- 证据：`features/active/F-021-world-project-onboarding/evidence/`；World `.harness/onboarding-20261016.json`。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/world-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project world`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## Git 回读

私有远端已创建，main 本地与远端一致：`021a6d536ad47476c057c9d170e2484c54defcae`；工作树干净。22 项 OpenSpec 覆盖与 F-021 Evidence 检查通过；技能链总检查因既有 wae 目录未登记失败。中央门禁仍为 rework_required，保持 partial。
