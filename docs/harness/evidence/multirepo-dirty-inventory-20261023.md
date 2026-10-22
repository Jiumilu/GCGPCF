---
doc_id: GPCF-DOC-MULTIREPO-DIRTY-INVENTORY-20261023
title: 多仓未提交改动盘点（2026-10-23）
project: GPCF
related_projects: [GPCF, WAE, WAME, PKC, XWAIL, KDS, GFIS, AAAS, XiaoC, FireQuote]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/multirepo-dirty-inventory-20261023.md
source_path: docs/harness/evidence/multirepo-dirty-inventory-20261023.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# 多仓未提交改动盘点（2026-10-23）

> 性质：只读盘点；不 commit / 不 stash / 不清理。
> 目的：为后续分批提交提供范围依据，避免 `git add -A` 误纳入并发改动。

## 1. 总表

| 仓 | 当前分支 | dirty | ahead/behind | 说明 |
|---|---|---:|---|---|
| GlobalCloud GPCF | `ci/gpcf-gates` | **1118** | — | 含 536 `.kds` 镜像、225 features、78 openspec、72 docs、54 harness、31 projects、25 runtime、23 tools、16 09-status |
| GlobalCloud WAE | `refactor/ui-spec-wae` | **0** | ahead 12 | 本会话 import/a11y 已推送 |
| GlobalCloud WAME | `wame/pm-governance` | 6 | — | 含本会话已提交后的少量残留 |
| GlobalCloud PKC | `codex/pkc-l4-task-notification` | 14 | — | P4/P5 令牌/状态改动未提交 |
| GlobalCloud XWAIL | `main` | 1 | — | 总体方案脏改（他人） |
| GlobalCloud KDS | `main` | 3 | — | 并发改动 |
| GlobalCloud GFIS | `chore/rename-gpcf-path` | 1 | — | 总体方案脏改（他人） |
| GlobalCloud AAAS | `main` | 19 | — | 并发改动 |
| GlobalCloud XiaoC | `main` | 209 | ahead 2 | 并发/候选件 |
| GlobalCloud FireQuote | `main` | 38 | — | 并发改动 |

## 2. 本会话产生的未提交改动（建议优先分批提交）

| 仓 | 范围 | 风险 |
|---|---|---|
| GPCF | `tools/kds-sync/validate_*.py`（vu/asset/drift/packageRef）、CI workflow、`runtime/plan-20261022/*`、`docs/harness/evidence/*`、`projects/{wae,pkc,wame}/STATUS.md`、`runtime/vu-ledger.yaml`、`runtime/asset-registry/usage-report.yaml` | 低（治理产物；按路径暂存） |
| PKC | `src/styles/gc-tokens.css`、`theme.css`、`status-badge.tsx`、页面迁移、测试、evidence | 中（业务前端；需 PKC 分支/评审） |
| WAME | `server/xap-intake` 残留 | 中（已提交主体；残留需确认） |

## 3. 风险与建议

1. **GPCF 1118 条**：`.kds` 镜像与并发会话改动占多数；**禁止 `git add -A`**，按显式路径分批提交。
2. GPCF 分支 `ci/gpcf-gates` 与远端关系需先 `git fetch` 确认，避免再次 behind。
3. PKC 改动在 `codex/pkc-l4-task-notification` 分支，需 PKC 属主/评审后再提交。
4. XiaoC/AAAS/FireQuote 等仓的 dirty 属并发会话，不由本会话接管。
5. WAE 已 0 dirty；无需处理。

## 4. 非声明

- 不声明任何改动已提交；
- 不声明任何项目状态提升；
- 不清理、不 stash、不删除任何改动。
