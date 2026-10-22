---
doc_id: GPCF-DOC-CACA881C1E
title: 归档说明（F-034 WAE 侧证据包，v2 · 2026-10-22 刷新）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/ARCHIVED.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/ARCHIVED.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 归档说明（F-034 WAE 侧证据包，v2 · 2026-10-22 刷新）

| 项 | 内容 |
|---|---|
| 来源仓 | `GlobalCloud WAE`（分支 `refactor/ui-spec-wae`，提交 `0f4ba74`） |
| 源路径 | `docs/evidence/F-034/`（**15 项：14 pass / 1 expected_diff**） |
| 归档时间 | 2026-10-22（**v2 刷新**；v1 为同日 12 项版本） |
| 授权 | 老卢 2026-10-22 授权（问答 + 决策模型 `approve_copy` 0.743；v2 刷新经 `gpcf_cleanup` 0.957） |
| 范围 | 仅复制/更新证据文件；未建 Feature、未改 F-034/F-036 定义、未提升任何状态 |
| 重放 | 回 WAE 仓：`bash docs/evidence/F-034/collect.sh` → `pnpm evidence:collect` |

**v2 变更**：并入 G8 无障碍矩阵（13）、G1 逐页视觉基线（14，含 `visual/` 目录）、无机器字段扫描（15）；manifest 更新至 commit `0f4ba74`。

**残留证据处置（同日，授权 `gpcf_cleanup`）**：`o1-shell-decoupling.md`/`o3-sidebar-unification.md` 已标 `status: superseded`（其引用的 `packages/app-shell` 已随 A2 删除、命令 exit 1）；`kds_path` 由 `features/done` 修正为 `features/active`；`summary-active-residue-20261022.md` 已注明"历史残留，以 summary.md 为准"。

> 非声明：本归档不声明 F-034 完成或 ready_for_review；F-034 状态仍 `active`（`loop.current_step: evaluate`, iteration 2）。
