---
doc_id: GPCF-DRC-STATUS-20261021
title: GlobalCloud DRC 状态
project: GPCF
related_projects: [GPCF, DRC]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/drc/STATUS.md
source_path: projects/drc/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-21
supersedes: []
superseded_by: []
---

# GlobalCloud DRC 状态

- 定位：项目群级数据库管理与数据资源管理；不替代各项目业务主账、KDS 知识主存或 WAME 治理裁决。
- Git：独立本地 `main` 与私有远端 [Jiumilu/GCDRC](https://github.com/Jiumilu/GCDRC) 已建立；`git ls-remote --heads origin main` 返回 `0fc24478a1146754f3f9b710ae37547939281b58`，与本地 HEAD 一致。
- 项目群：第 28 个项目，`project_status=registered`，`overall_status=partial/rework`。
- 项目级总体方案和实施方案仅为候选；数据库连接、资源目录、权限模型和真实运行均未实现或验证。
- 门禁：本轮前置检查为 `loop_document_gate=rework_required`、`project_group_gate_readiness=fail`；不声明纳管后通过。
- authorization：用户授权纳管及建立本地与远端 Git。
- confirmation：生产数据接入、权限变更、正式集成、发布及客户验收待独立确认。
- 回退：撤回中央登记不删除独立仓或其他项目数据。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/drc-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project drc`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`
