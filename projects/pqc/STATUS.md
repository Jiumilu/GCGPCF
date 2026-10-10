---
doc_id: GPCF-PQC-STATUS-20261010
title: PQC 状态
project: GPCF
related_projects: [PQC, GPCF, PVAOS, KDS]
domain: governance
status: controlled
version: v1.0
owner: 老卢
kds_space: 开发
kds_path: 开发/PQC/projects/pqc/STATUS.md
source_path: projects/pqc/STATUS.md
sync_direction: local_only
last_reviewed: 2026-10-10
supersedes: []
superseded_by: []
---

# PQC 状态

- 路径：`../GlobalCloud PQC`
- 仓库：`https://github.com/Jiumilu/GCPQC`（private，main）
- 业务：包装项目成本、报价审批、订单回款；PVA-PACKAGING-SYSTEM。
- project_status: registered；overall_status: partial。
- authorization: user_authorized_onboarding_and_git_2026-10-10。
- confirmation：业务验收与生产发布尚未确认。
- 基线验证：后端 261 passed；前端 tsc --noEmit 通过。
- 生产/真实业务/跨系统验收：本轮未执行，不提升 integrated/production_ready。
- 证据：`../GlobalCloud PQC/docs/harness/onboarding-2026-10-10.md`。
- 下一步：依据本项目实际业务需求新建 Feature，完成真实业务与权限验收；历史门禁覆盖不代表新项目完成。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/pqc-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project pqc`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`
