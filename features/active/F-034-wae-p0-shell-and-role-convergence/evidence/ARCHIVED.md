---
doc_id: GPCF-DOC-CACA881C1E
title: 归档说明（F-034 WAE 侧证据包，v7 · 2026-10-25 刷新）
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

# 归档说明（F-034 WAE 侧证据包，v7 · 2026-10-25 刷新）

| 项 | 内容 |
|---|---|
| 来源仓 | `GlobalCloud WAE`（分支 `refactor/ui-spec-wae`，提交 `ac7e5c7`） |
| 源路径 | `docs/evidence/F-034/`（**21 项：21 pass / 0 expected_diff / 0 fail**） |
| 归档时间 | 2026-10-25（v7；v1 12 / v2 15 / v3 17 / v4 19 / v5 19 / v6 20） |
| 授权 | 老卢 2026-10-24 跨仓解除阻塞授权延续 |
| 范围 | 仅复制/更新证据文件；Feature 状态仍 `ready_for_review`（老卢 2026-10-25 确认，`1a67aa746`） |
| 重放 | 回 WAE 仓：`bash docs/evidence/F-034/collect.sh` → `pnpm evidence:collect` |

**v7 变化**：新增第 21 项 **端到端任务流**（真实 dev + 临时身份：登录→统一工作台→PKC 候选页→服务控制台→回 PKC 页，**8/8 步**，pageerror=0）——同时作为 `task_flow_e2e_status` 的运行时证据；`evidence_overexposure_gate` 以第 15 项（5 页 0 命中 + 金丝雀 6/6）为运行时证据（见 `evidence/runtime-evidence-20261025.md`，`c50d9a14e`）。

**B5 基线**（v6 起）：`visual/m3-lines/` 10 张（PKC 3 / Brain 4 / PVAOS 3，pageerror=0）；iframe 隔离下为「后置基线」，「前」取各仓 git 历史；Brain 截图含 KDS/模型不可用如实降级态。

**同期跨仓记录**：PKC（`6cf8bdce`/`708aa959`/`831ebf0b`/`baeaec11`/`f1849aad`）、Brain（`7c3d72b1`/`6ffe85be`）、PVAOS（`1c03704`）、Studio（`bed04bdc`）、本仓（`9d7191eb4`/`1a67aa746`/`c50d9a14e`）。

**日志说明**：本仓 `.gitignore` 含 `*.log` ⇒ 只跟踪 `logs/*.exit`；完整日志回 WAE 仓取。

> 非声明：不声明 F-034 done/accepted/生产就绪；不声明三条线已生产接入。
