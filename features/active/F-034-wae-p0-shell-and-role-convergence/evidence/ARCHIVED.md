---
doc_id: GPCF-DOC-CACA881C1E
title: 归档说明（F-034 WAE 侧证据包，v6 · 2026-10-25 刷新）
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

# 归档说明（F-034 WAE 侧证据包，v6 · 2026-10-25 刷新）

| 项 | 内容 |
|---|---|
| 来源仓 | `GlobalCloud WAE`（分支 `refactor/ui-spec-wae`，提交 `c558dda`） |
| 源路径 | `docs/evidence/F-034/`（**20 项：20 pass / 0 expected_diff / 0 fail**） |
| 归档时间 | 2026-10-25（v6；v1 12 / v2 15 / v3 17 / v4 19 / v5 19） |
| 授权 | 老卢 2026-10-24 跨仓解除阻塞授权延续 |
| 范围 | 仅复制/更新证据文件；未改 Feature 状态（本次归档前状态已按老卢 2026-10-25 确认置为 ready_for_review） |
| 重放 | 回 WAE 仓：`bash docs/evidence/F-034/collect.sh` → `pnpm evidence:collect` |

**v6 变化**：新增第 20 项 **M3 三线 B5 视觉基线**（PKC 3 / Brain 4 / PVAOS 3 共 10 张，pageerror=0，`visual/m3-lines/` 含 index.json）；O2 两项保持 pass；日志/截图/基线全部刷新至 WAE 提交 `c558dda`。

**口径**：被嵌应用由 iframe 承载，WAE 接入不改变其视觉 ⇒ B5 基线为「后置基线」，「前」取各仓 git 历史；Brain 截图含模型/KDS 不可用的如实降级态。

**同期跨仓记录**：PKC（`6cf8bdce`/`708aa959`/`831ebf0b`/`baeaec11`/`f1849aad`）、Brain（`7c3d72b1`/`6ffe85be`）、PVAOS（`1c03704`）、Studio（`bed04bdc`）、本仓（`9d7191eb4`/`1a67aa746`）。

**日志说明**：本仓 `.gitignore` 含 `*.log` ⇒ 只跟踪 `logs/*.exit`；完整日志回 WAE 仓取。

> 非声明：不声明 F-034 done/accepted/生产就绪；不声明三条线已生产接入。
