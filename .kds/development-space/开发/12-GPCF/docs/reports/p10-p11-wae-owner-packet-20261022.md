---
doc_id: GPCF-DOC-E31E79A62B
title: P10 / P11 · 界面分层与双角色权限一致性 · WAE 属主执行包
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p10-p11-wae-owner-packet-20261022.md
source_path: docs/reports/p10-p11-wae-owner-packet-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P10 / P11 · 界面分层与双角色权限一致性 · WAE 属主执行包

- 日期：2026-10-22｜依据：计划 P10/P11；UI 硬规则 `LOOP_UI_PRODUCT_FIRST_CONTROL.md`
- 边界：WAE 仓改动由 WAE 属主执行；GPCF 只出动作与判据（纪律⑤）
- 现状：`ui_plane` 仅在 `apps/wame/src/app/apps/AppsShell.dom.test.tsx` 有测试侧引用，`placement.city.yaml` 尚无该字段

## 1. P10 普通用户界面 vs 治理审计界面分层

| # | 动作 | 判据 |
|---|---|---|
| 1 | `docs/assembly-spec/placement.city.yaml` 每个 service 条目加 `ui_plane: user|governance` | `grep -c "ui_plane" placement.city.yaml` == service 条目数 |
| 2 | 治理审计页统一 `/governance/*` 前缀 + 独立权限位 | 路由清单可枚举；无治理页出现在用户导航 |
| 3 | 29 项目审计视图从用户侧导航移除 | 用户导航项数（DOM 断言）与改动前基线一致或更少 |
| 4 | viewer 访问 `/governance/*` 断言 403/重定向 | 新增 DOM 用例 pass（`pnpm vitest run apps/shell`） |

## 2. P11 管理员与 viewer 双角色权限一致性测试

| # | 动作 | 判据 |
|---|---|---|
| 1 | 建 29 service entries × {admin, viewer} 角色矩阵测试 | 矩阵覆盖 29/29，缺一即失败 |
| 2 | 差异必须显式声明（`diff_declared: true`），未声明的差异即失败 | `jq '[.matrix[]|select(.admin!=.viewer and (.diff_declared!=true))]|length'` == 0 |
| 3 | 治理审计界面 + 部分授权精确收敛补充用例 | `pnpm vitest run apps/shell/src/AppsShell.dom.test.tsx` pass |
| 4 | 令牌一律 mock，禁读生产凭据 | 测试内无真实 token 文件读取 |

## 3. 非声明

- 通过 ≠ 产品验收；不得声明 accepted/integrated/production_ready；
- 移动端与完整无障碍仍属 P16-3 范围。
