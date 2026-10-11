---
doc_id: GPCF-DOC-LOOP-UI-PRODUCT-FIRST-CONTROL
title: LOOP UI Product First Control
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md
source_path: 02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md
sync_direction: bidirectional
last_reviewed: 2026-07-16
supersedes: []
superseded_by: []
---

# LOOP UI Product First Control

本文是整个 GlobalCloud 项目群 LOOP 对产品界面、操作工作台、人机协同入口及其运行目标的产品优先控制规则。它不接管各项目当前开发目标，不替代项目本地 LOOP；它定义 GPCF 项目群治理如何在功能完整和质量基线不下降的前提下，防止 LOOP 证据或机器接口反噬产品设计，并保证不同用户能够理解、完成、纠错和复现自己的任务。

GPCF 只控制 LOOP 防偏、项目群 UI 门禁和跨会话治理边界，不隐式接管 Studio 本地开发会话。

涉及 UI 的开发态 LOOP 还必须同时遵守 `LOOP_DELIVERY_EFFICIENCY_CONTROL.md`，确保 UI 降噪和治理证据收敛能转化为 `product_delta`、`user_visible_delta` 和 `delivery_efficiency_gate`，避免 `high_compliance_low_product_progress`。

## 1. 最高裁决

```text
LOOP success must not reduce product usability.
UI evidence is not UI structure.
Governance evidence must be traceable, not dominant.
Debug details must not become default product copy.
A test-visible element is not automatically user-visible.
Human-operable is required; machine-operable alone is not product-ready.
Functional completeness and quality are prerequisites, not substitutes for usability.
```

## 2. 控制范围

本控制适用于项目登记表中的全部 18 个项目：`AAAS`、`Brain`、`WAS`、`XiaoC`、`WAES`、`GPC`、`Studio`、`GPCF`、`XWAIL`、`GFIS`、`MMC`、`KDS`、`XiaoG`、`PVAOS`、`SOP`、`PKC`、`XGD`、`ICP`，以及后续经项目群登记表纳管的新增项目。

覆盖对象包括：

- Studio 当前运营工作台、AI 会话工作区、KDS 对象工作区和项目会话流。
- GPCF 项目群 UI Quality Gate。
- 所有涉及 UI 的 LOOP 轮次、E2E、测试策略和 evidence 输出。
- 多会话或多智能体在 Studio UI 上并行推进时的主线防偏。
- `features/active/`、`runtime/queue.json` 中所有正在执行、排队、评估、修复或待记录的 Feature/目标；不因目标当前不是前端开发而免除人类使用边界判断。
- CLI、API、自动化、Evidence、治理脚本产生的所有人类查看、确认、配置、排障、恢复和交接入口。

本控制不授权：

- 接管 Studio 开发会话。
- deploy、真实外部 API、真实 KDS API、生产写入。
- `accepted`、`integrated`、`production_ready`、`customer_accepted` 状态提升。
- 删除业务能力或绕过 Studio 本地验证。

## 3. 产品优先门禁

Studio 或其它项目继续 UI 快速开发时，每轮必须通过以下 7 项：

| Gate | 要求 | 失败后状态 |
|---|---|---|
| `product_first_ui_gate` | 本轮推进用户可识别任务流，而不是只增加治理证明 | `ui_rework_required` |
| `evidence_overexposure_gate` | 默认界面不得新增常驻 receipt、preflight、dry-run、boundary、readiness 或 audit 条 | `ui_rework_required` |
| `debug_details_visibility` | `createObject`、`writeToKds`、`idempotency`、`rollback`、`package hash` 等技术细节默认隐藏，只能进入调试或治理详情 | `ui_rework_required` |
| `task_flow_e2e_status` | E2E 必须以用户任务流完成为主，不得只验证治理条存在 | `ui_rework_required` |
| `audit_traceability_gate` | 审计、权限、回执、边界仍必须可追溯，但默认折叠或进入治理详情 | `ui_partial` 或 `ui_rework_required` |
| `multi_user_usability_gate` | 至少覆盖首次/低频用户、高频专业用户、治理/审计用户，以及目标明确需要的移动端或无障碍用户 | `ui_partial` 或 `ui_rework_required` |
| `human_operable_gate` | 人类用户必须能发现入口、理解状态、完成任务、识别后果并从错误中恢复；只有机器、脚本或测试可操作不算通过 | `ui_rework_required` |

功能完整、构建/测试通过和既有质量门是进入易用性评估的前置条件。任何一项未通过时不得用“易用”掩盖功能或质量缺口；全部通过后仍必须独立验证易用性，不得把机器接口成功、选择器存在或截图生成当作人类可用证据。

## 4. 多用户易用性基线

每个直接或间接面向人的目标必须先声明用户群和主任务，至少按以下角色检查适用性：

1. 首次或低频用户：入口可发现，术语可理解，有下一步和恢复指引。
2. 高频专业用户：核心路径短，支持键盘/批量/筛选等高效操作，重复确认不过载。
3. 管理、治理或审计用户：状态、来源、权限、影响范围和审计链可追溯，但默认不挤占主任务。
4. 移动端、触控或无障碍用户：仅在目标场景适用时纳入；必须明确适用或豁免理由，不得静默忽略。

共同通过标准：

- 可发现：用户无需了解内部对象名、脚本名或测试选择器即可找到入口。
- 可理解：使用业务语言，状态、风险、权限和操作后果清晰；技术细节按需展开。
- 可完成：主任务具有清晰起点、单一主操作、进度反馈和完成反馈。
- 可纠错：输入校验、撤销/回滚、错误解释和恢复路径与风险等级匹配。
- 高效率：高频路径不被治理证明、重复确认或机器字段阻塞。
- 可访问与自适应：键盘焦点、语义标签、对比度、触控目标、长文本和目标视口通过适用检查。

机器接口必须与人类操作面分层：API/CLI/agent contract 可以保留完整机器字段，但默认产品界面只展示完成任务所需的业务信息；原始载荷、哈希、幂等键、内部状态机和调试日志进入开发者或治理详情。

## 5. 运行中 Feature 与目标的强制继承

所有 `features/active/*/feature.yaml` 必须声明 `ui_product_first_control`，至少包含：

```yaml
ui_product_first_control:
  version: v1.1
  applicability: direct | indirect | not_applicable
  user_groups: []
  primary_human_task: ""
  machine_interface_boundary: ""
  gates:
    functional_completeness: pass | pending | fail | waived
    quality_baseline: pass | pending | fail | waived
    multi_user_usability: pass | pending | fail | waived
    task_flow_e2e_status: pass | pending | fail | waived
    accessibility_status: pass | pending | fail | waived
    evidence_overexposure_gate: pass | pending | fail | waived
  status_ceiling: partial | ui_evidence_candidate
```

规则：

- `direct`：目标直接改变 UI/交互，必须给出真实用户任务流、桌面与适用移动视口、键盘/焦点、错误恢复证据。
- `indirect`：目标产生人类查看、确认、配置、排障或交接入口，必须至少验证可理解、状态反馈和恢复路径。
- `not_applicable`：必须写明可审计理由；仅“这是后端/脚本/机器任务”不是有效豁免理由。
- 任一必需 gate 为 `pending` 或 `fail` 时，状态上限为 `partial`；全部必需 gate 有可回放证据后，最高也只能形成 `ui_evidence_candidate`。
- 新 Feature 在进入 Builder 前完成声明；本控制生效时已运行的 Feature 必须在下一次角色流转或 evidence 更新前补齐。

## 6. Studio 快速开发控制

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

## 7. Studio 会话受控提示词

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
multi_user_usability_gate
human_operable_gate
```

## 8. 回到 GPCF 治理的条件

出现以下任一情况，Studio 开发会话必须回到 GPCF 治理确认：

- UI 继续出现治理证据堆叠。
- E2E 继续以证明条存在作为主要验收。
- 默认界面出现技术内部词汇主导用户任务。
- 需要 deploy、真实外部 API、真实 KDS API、生产写入或状态提升。
- 多会话输出触碰重叠 scope 或出现主线漂移。
- 仅机器接口、测试选择器或治理脚本成功，但目标用户无法独立完成主任务。
- 功能或质量门未通过，却试图用易用性结论提升状态。

## 9. Validator

本控制由以下脚本检查：

```bash
python3 tools/kds-sync/validate_loop_ui_product_first_control.py
```

该 validator 必须接入 `loop_document_gate.py`，并作为 UI Quality Gate 的项目群级硬门禁。
