---
doc_id: GPCF-DOC-CACA881C1E
title: 归档说明（F-034 WAE 侧证据包，v4 · 2026-10-23 刷新）
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

# 归档说明（F-034 WAE 侧证据包，v4 · 2026-10-23 刷新）

| 项 | 内容 |
|---|---|
| 来源仓 | `GlobalCloud WAE`（分支 `refactor/ui-spec-wae`，提交 `307a948`） |
| 源路径 | `docs/evidence/F-034/`（**19 项：17 pass / 2 expected_diff**） |
| 归档时间 | 2026-10-23（v4 刷新；v1 12 项 / v2 15 项 / v3 17 项） |
| 授权 | 老卢 2026-10-23 授权（问答 + 决策模型 `archive_refresh` 0.864，供参考；纯证据同步） |
| 范围 | 仅复制/更新证据文件；未建 Feature、未改 F-034/F-036 定义、未提升任何状态 |
| 重放 | 回 WAE 仓：`bash docs/evidence/F-034/collect.sh` → `pnpm evidence:collect` |

**v4 变更**：并入第 18 项（像素级基线 4 页 ≤0.02%）、第 19 项（B3 面板布局 E2E 10/10，默认 off）；日志/截图/visual 基线刷新至 WAE 提交 `307a948`。

**两条 expected_diff 说明**：均因 **PKC 快照仍过期**（11 跨仓比对 + 17 登记表判定）；Brain 与登记一致、待书面确认。两轮请求/提醒已投递（PKC `8ce25526`/`ed724d11`，Brain `3f8cbb75`/`8edd9b2e`）。

**残留证据历史处置（2026-10-22）**：`o1-shell-decoupling.md`/`o3-sidebar-unification.md` 已标 `status: superseded`（其引用的 `packages/app-shell` 已随 A2 删除、命令 exit 1）；`kds_path` 已修正为 `features/active`；`summary-active-residue-20261022.md` 已注明"历史残留，以 summary.md 为准"。

> **日志说明（与 WAE 源的差异）**：GPCF 仓 `.gitignore` 含 `*.log`，因此本仓**只跟踪 `logs/*.exit`（退出码）**，不跟踪 `logs/*.log`（完整输出）。
> 需要完整输出时请回 WAE 仓按 `bash docs/evidence/F-034/collect.sh` 重跑，或从 WAE 仓对应提交的 `docs/evidence/F-034/logs/` 取。

> 非声明：本归档不声明 F-034 完成或 ready_for_review；F-034 状态仍 `active`（`loop.current_step: evaluate`, iteration 2）。
