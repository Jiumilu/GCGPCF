---
doc_id: GPCF-DOC-C1476319CB
title: 双角色收敛 E2E 报告（F-034 / F-010 基线复跑）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/reports/双角色收敛E2E报告.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/reports/双角色收敛E2E报告.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 双角色收敛 E2E 报告（F-034 / F-010 基线复跑）

- 时间：2026-10-22T13:30:09.740Z
- 结论：通过

| 判据 | 结果 | 详情 |
|---|---|---|
| A1 system-admin 服务控制台可见 | ✓ | 服务控制台二级 7 项（期望 7） |
| A2 system-admin /api/idp/users = 200 | ✓ | status=200 |
| A5a system-admin 无 pageerror | ✓ | 0 条 |
| A3 viewer 服务控制台不可见 | ✓ | 一级=0，二级=0 |
| A4 viewer /api/idp/users = 403 | ✓ | status=403 |
| A5b viewer 无 pageerror | ✓ | 0 条 |

> 口径：F-010 `wae-multi-user.spec.ts`（system-admin 16 menus / viewer 4 menus；users API 200 vs 403）。
> 非声明：本报告不提升任何 Feature/项目状态。
