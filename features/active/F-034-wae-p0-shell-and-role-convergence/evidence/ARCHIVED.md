---
doc_id: GPCF-DOC-CACA881C1E
title: 归档说明（F-034 WAE 侧证据包，v5 · 2026-10-24 刷新）
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

# 归档说明（F-034 WAE 侧证据包，v5 · 2026-10-24 刷新）

| 项 | 内容 |
|---|---|
| 来源仓 | `GlobalCloud WAE`（分支 `refactor/ui-spec-wae`，提交 `e066c4c`） |
| 源路径 | `docs/evidence/F-034/`（**19 项：19 pass / 0 expected_diff / 0 fail**） |
| 归档时间 | 2026-10-24（v5；v1 12 / v2 15 / v3 17 / v4 19） |
| 授权 | 老卢 2026-10-24 授权跨仓解除阻塞（纯证据同步） |
| 范围 | 仅复制/更新证据文件；未建 Feature、未改 F-034/F-036 定义、未提升任何状态 |
| 重放 | 回 WAE 仓：`bash docs/evidence/F-034/collect.sh` → `pnpm evidence:collect` |

**v5 变化**：O2 闭环——第 11 项（跨仓比对）与第 17 项（登记表判定）由 expected_diff 转 **pass**（PKC 快照与 WAE 逐字节相同；Brain 偏离 5/28 与登记一致）；新增 M2 真实第二插件与 B3 面板布局 E2E（第 19 项 13/13）；日志/截图/visual 基线全部刷新。

**同期跨仓记录**：
- PKC：令牌快照入库 + WAE 复核回执（`6cf8bdce`）；P5 状态语义接入 B7 + 截图（`708aa959`，tsc 0 / 151 例）
- Brain：自有主题声明 + WAE 复核回执（`7c3d72b1`）
- Studio：标记 `retired` + 例外回执（`bed04bdc`）
- 本仓：Studio 例外三方记录（`9d7191eb4`）

**日志说明**：本仓 `.gitignore` 含 `*.log` ⇒ 只跟踪 `logs/*.exit`；完整日志回 WAE 仓取（其 `.gitignore` 已对本目录开例外）。

> 非声明：本归档不声明 F-034 完成或 ready_for_review；F-034 状态仍 `active`（`loop.current_step: evaluate`, iteration 2）。
