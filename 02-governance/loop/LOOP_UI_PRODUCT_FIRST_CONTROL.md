---
doc_id: GPCF-DOC-LOOP-UI-PRODUCT-FIRST-CONTROL
title: LOOP UI Product First Control
project: WAES
related_projects: [GPC, WAES, KDS, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md
source_path: 02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md
sync_direction: bidirectional
last_reviewed: 2026-07-05
supersedes: []
superseded_by: []
---

# LOOP UI Product First Control

本文是项目群 LOOP 对 Studio 及其它产品界面开发的产品优先控制规则。它不接管 Studio 当前开发目标，不替代 Studio 本地 LOOP；它只定义 GPCF 项目群治理如何防止 LOOP 证据驱动反噬产品设计，并让 Studio 在受控边界内继续快速开发。

GPCF 只控制 LOOP 防偏、项目群 UI 门禁和跨会话治理边界，不隐式接管 Studio 本地开发会话。

涉及 UI 的开发态 LOOP 还必须同时遵守 `LOOP_DELIVERY_EFFICIENCY_CONTROL.md`，确保 UI 降噪和治理证据收敛能转化为 `product_delta`、`user_visible_delta` 和 `delivery_efficiency_gate`，避免 `high_compliance_low_product_progress`。

## 1. 最高裁决

```text
LOOP success must not reduce product usability.
UI evidence is not UI structure.
Governance evidence must be traceable, not dominant.
Debug details must not become default product copy.
A test-visible element is not automatically user-visible.
```

## 2. 控制范围

本控制适用于：

- Studio 当前运营工作台、AI 会话工作区、KDS 对象工作区和项目会话流。
- GPCF 项目群 UI Quality Gate。
- 所有涉及 UI 的 LOOP 轮次、E2E、测试策略和 evidence 输出。
- 多会话或多智能体在 Studio UI 上并行推进时的主线防偏。

本控制不授权：

- 接管 Studio 开发会话。
- deploy、真实外部 API、真实 KDS API、生产写入。
- `accepted`、`integrated`、`production_ready`、`customer_accepted` 状态提升。
- 删除业务能力或绕过 Studio 本地验证。

## 3. 产品优先门禁

Studio 或其它项目继续 UI 快速开发时，每轮必须通过以下 5 项：

| Gate | 要求 | 失败后状态 |
|---|---|---|
| `product_first_ui_gate` | 本轮推进用户可识别任务流，而不是只增加治理证明 | `ui_rework_required` |
| `evidence_overexposure_gate` | 默认界面不得新增常驻 receipt、preflight、dry-run、boundary、readiness 或 audit 条 | `ui_rework_required` |
| `debug_details_visibility` | `createObject`、`writeToKds`、`idempotency`、`rollback`、`package hash` 等技术细节默认隐藏，只能进入调试或治理详情 | `ui_rework_required` |
| `task_flow_e2e_status` | E2E 必须以用户任务流完成为主，不得只验证治理条存在 | `ui_rework_required` |
| `audit_traceability_gate` | 审计、权限、回执、边界仍必须可追溯，但默认折叠或进入治理详情 | `ui_partial` 或 `ui_rework_required` |

## 4. Studio 快速开发控制

允许 Studio 当前目标继续快速开发：

- 调整信息架构和主工作区密度。
- 折叠治理、审计、回执和技术详情。
- 把 receipt 改为 toast + 审计时间线。
- 把 E2E 从证据存在改为用户流程完成。
- 保留所有必要 evidence 的追溯入口。

禁止 Studio LOOP 继续执行：

- 新增常驻 `receipt`、`preflight`、`dry-run`、`boundary`、`readiness`、`controlled-write` 条。
- 用 `data-testid` 或测试可见性反推用户默认可见 UI。
- 把 `createObject`、`writeToKds`、`idempotency`、`rollback`、`package hash` 放到默认主界面。
- 用治理文案替代用户任务入口。
- 在 UI gate 失败时继续叠加证明型 UI。

## 5. Studio 会话受控提示词

```text
继续 Studio 当前目标开发，但必须受 GPCF LOOP_UI_PRODUCT_FIRST_CONTROL 约束。

本轮目标不是继续增加治理证据 UI，而是让 Studio 快速回到产品工作台主线：
- 用户任务流优先；
- 治理证据可追溯但默认折叠；
- 技术细节进入调试/治理详情入口；
- E2E 以用户流程完成为主；
- 不得新增常驻 receipt/preflight/dry-run/boundary/readiness 条；
- 不得状态提升、deploy、真实外部 API、真实 KDS API。

每轮结束必须报告：
goal / changed / verified / risk / next
并明确：
product_first_ui_gate
evidence_overexposure_gate
debug_details_visibility
task_flow_e2e_status
audit_traceability_gate
```

## 6. 回到 GPCF 治理的条件

出现以下任一情况，Studio 开发会话必须回到 GPCF 治理确认：

- UI 继续出现治理证据堆叠。
- E2E 继续以证明条存在作为主要验收。
- 默认界面出现技术内部词汇主导用户任务。
- 需要 deploy、真实外部 API、真实 KDS API、生产写入或状态提升。
- 多会话输出触碰重叠 scope 或出现主线漂移。

## 7. Validator

本控制由以下脚本检查：

```bash
python3 tools/kds-sync/validate_loop_ui_product_first_control.py
```

该 validator 必须接入 `loop_document_gate.py`，并作为 UI Quality Gate 的项目群级硬门禁。
