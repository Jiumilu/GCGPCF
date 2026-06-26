---
doc_id: GPCF-DOC-C3B9DFCB0C
title: LOOP_ROUND_TEMPLATE
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/LOOP_ROUND_TEMPLATE.md
source_path: templates/LOOP_ROUND_TEMPLATE.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

 Loop Round Template

复制到：`docs/harness/loops/loop-round-{ROUND_ID}.md`

## 1. 基本信息

| 字段 | 值 |
|---|---|
| Round ID |  |
| 触发来源 |  |
| Loop 模式 | L0 / L1 / L2 / L3 / L3.5 / L4 / L5 |
| 本轮状态 | planned / running / blocked / completed / needs-human-review |
| 开始时间 |  |
| 完成时间 |  |

## 1.1 连续运行计数器

| 字段 | 值 |
|---|---|
| continuous session | active / stopped / not_applicable |
| continuous mode | L3 / L3.5 / L4 / L5 / not_applicable |
| declared_rounds | n/上限 |
| substantive_rounds | n/上限 |
| generated_items |  |
| batch_generated | true / false |
| substance_gate | pass / partial / fail / not_applicable |
| substance_evidence |  |
| 剩余轮次 | 上限-n |
| 已用时间 | x/时间上限 |
| 停止类型 | none / hard_stop / user_stop / budget_exhausted / time_exhausted / task_queue_empty / authorization_boundary / production_safety |
| 停止证据 |  |
| 是否符合停止规则 | yes / no / not_applicable |
| 未停止时下一轮 |  |

## 1.2 轮次真实性检查

L3、L3.5、L4、L5 必填。每轮至少满足 4/5，才可计为 `substantive_round=1`。同一脚本、同一时间窗口、同一模板批量生成多个文档时，整批默认最多计 1 个实质轮次。

| 项 | 判定 | 证据 |
|---|---|---|
| 独立输入 | yes / no |  |
| 独立判断 | yes / no |  |
| 独立输出 | yes / no |  |
| 独立验证 | yes / no |  |
| 独立反馈 | yes / no |  |

| 字段 | 值 |
|---|---|
| generated_item | true / false |
| substantive_round | true / false |
| counted_as_continuous_round | true / false |
| batch_generated | true / false |
| batch_id |  |
| similarity_with_previous | low / medium / high |
| substance_score | 0-5 |
| l4_score | 0-100 / not_applicable |
| counted_as_l4_substantive_round | true / false / not_applicable |
| correction_required | yes / no |
| corrected_stop_type | none / hard_stop / user_stop / budget_exhausted / time_exhausted / task_queue_empty / authorization_boundary / production_safety |

## 2. 本轮目标

- 最小目标：
- 不处理范围：
- 成功判定：

## 3. 输入文档

| 文档 | 路径 | 用途 |
|---|---|---|
|  |  |  |

## 3.1 KDS 关联数据检索

涉及真实开发、契约、mock、dry-run 或 evidence 时必填。KDS 只提供受控语义、字段口径、SOP、案例和 evidence 回指，不替代 GPC/GFIS/WAES/PVAOS 的当前业务事实。

| 字段 | 值 |
|---|---|
| required | true / false |
| status | planned / completed / skipped_with_reason / blocked |
| retrieval_mode | local_mirror / kds_api_readonly / kds_api_dry_run |
| business_node |  |
| target_projects |  |

| query_terms | 说明 |
|---|---|
|  |  |

| source_document | doc_id | source_path / kds_path | status | relevance |
|---|---|---|---|---|
|  |  |  | controlled/draft/archive |  |

| retrieved_object | owner_project | fields | source |
|---|---|---|---|
|  |  |  |  |

| retrieved_status | allowed_transitions | blocked_transitions | source |
|---|---|---|---|
|  |  |  |  |

| retrieved_sop | summary | source |
|---|---|---|
|  |  |  |

| retrieved_evidence_rule | required_fields | source |
|---|---|---|
|  |  |  |

| development_data_need | producer_project | consumer_project | verification_method |
|---|---|---|---|
|  |  |  |  |

| mock_data_need | fields | boundary_cases |
|---|---|---|
|  |  |  |

| unresolved_question | owner | stop_required |
|---|---|---|
|  |  | true/false |

| kds_followup_update | target_doc | reason |
|---|---|---|
|  |  |  |

## 3.2 L4 100 分评分

Loop 模式为 L4 时必填。评分标准来源：`01-architecture/GlobalCloud项目群最小闭环L4实施方案.md` 的 `L4 100 分评分模型`。

| 指标 | 分值 | 得分 | 扣分原因 |
|---|---:|---:|---|
| 职责边界准确性 | 15 |  |  |
| KDS 关联数据检索质量 | 10 |  |  |
| 真实仓实质变更 | 15 |  |  |
| 测试与验证 | 15 |  |  |
| Evidence 完整性 | 15 |  |  |
| 最小闭环贡献度 | 10 |  |  |
| Git 与工作区可审计性 | 10 |  |  |
| 下一轮可执行性 | 10 |  |  |
| 合计 | 100 |  |  |

| 字段 | 值 |
|---|---|
| l4_status | L4 Ready / L4 Conditional / L3 Repair / Blocked / Invalid / not_applicable |
| counted_as_l4_substantive_round | true / false / not_applicable |
| project_group_cumulative_score | 0-100 / not_calculated |
| next_round_score_target |  |
| score_gate_result | pass / conditional / downgrade_to_l3 / blocked / invalid / not_applicable |

评分门禁：

- 90-100：`L4 Ready`，可计为高质量 L4 实质轮。
- 80-89：`L4 Conditional`，可计为 L4 实质轮，但必须登记改进项。
- 70-79：`L3 Repair`，不得计为 L4 实质轮，必须降级补齐。
- 60-69：`Blocked`，本轮停止，修复关键缺口后再继续。
- 0-59：`Invalid`，本轮无效，不得进入下一轮 L4。

## 4. 影响范围

| 项目/模块 | 影响 | 风险等级 |
|---|---|---|
|  |  | P0/P1/P2/P3 |

## 5. 授权边界

### 允许动作

- 

### 禁止动作

- Git push / 合并主分支，除非用户明确授权。
- 删除文件或大规模迁移，除非用户明确授权。
- 真实 API 写入、生产写入、部署、权限变更，除非当前模式为 L3.5/L4/L5 且专项政策与显式授权均允许。
- KDS TOKEN 写入或真实 KDS API 同步声明。
- 标记 `accepted` / `integrated`。

### L3.5 / L4 / L5 专项授权字段

| 字段 | 值 |
|---|---|
| 授权项目 |  |
| 授权环境 |  |
| 授权分支/API |  |
| 授权时间窗 |  |
| 最大轮次 |  |
| 允许真实动作 |  |
| 禁止动作 |  |
| 回滚策略 |  |
| 验收指标 |  |
| 监控指标 |  |

## 6. 执行步骤

| 步骤 | 动作 | 结果 |
|---|---|---|
| 1 |  |  |

## 7. 验证命令

| 命令 | 结果 | 证据 |
|---|---|---|
|  | pass/partial/fail |  |

## 7.1 UI 质量门禁（涉及 UI 时必填）

仅当本轮涉及产品界面、控制塔、工作台、证据页、异常页、AI 对话页、配置页、移动端、桌面端、前端回归或可视化交互验收时填写。若 `UI scope=true`，则必须按 `.codex/skills/globalcloud-ui-quality-gate/` 输出完整 UI gate 记录。

| 字段 | 值 |
|---|---|
| UI scope | true / false |
| Tool route | `@product-design -> WAES -> ui-ux-pro-max -> Figma -> Storybook -> impeccable -> Playwright/browser -> axe-core/Lighthouse -> GPCF UI Gate` / project-specific route / not_applicable |
| Context package | completed / partial / missing / not_applicable |
| Prompt profile | functional-accuracy / visual-quality / usability-experience / governance-evidence / scope-control / mixed / not_applicable |
| Design options | 3 / 1_with_existing_selected_direction / not_applicable |
| Selected option | 1 / 2 / 3 / existing / not_applicable |
| WAES baseline reuse | shell / page-skeleton / core-components / full-stack / exception-approved / not_applicable |
| Surface | list / detail / edit-config / operation-workbench / exception-handling / evidence-audit / ai-chat / ai-sidebar / brand-marketing / mobile-desktop-shell / not_applicable |
| Repository/path |  |
| Scope |  |
| Tools used | `@product-design` / WAES / Impeccable / ui-ux-pro-max / Playwright / browser / Figma / Storybook / axe-core / Lighthouse / manual / not_applicable |
| Tools unavailable |  |
| Verification |  |
| Status ceiling | ui_evidence_candidate / partial / blocked / rework_required / not_applicable |

```text
UI gate status: ui_ready | ui_partial | ui_blocked | ui_rework_required | not_applicable
Tool route:
Context package:
Prompt profile:
Design options:
Selected option:
WAES baseline reuse:
Surface:
Repository/path:
Scope:
Tools used:
Tools unavailable:
Verification:
Status ceiling:
```

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass/partial/fail/not_applicable |  |  |
| G2 Design Tokens | pass/partial/fail/not_applicable |  |  |
| G3 Component Consistency | pass/partial/fail/not_applicable |  |  |
| G4 Evidence And Governance | pass/partial/fail/not_applicable |  |  |
| G5 AI Fact Separation | pass/partial/fail/not_applicable |  |  |
| G6 Accessibility | pass/partial/fail/not_applicable |  |  |
| G7 Responsive And Text Robustness | pass/partial/fail/not_applicable |  |  |
| G8 Runtime Verification | pass/partial/fail/not_applicable |  |  |
| G9 Scope Control | pass/partial/fail/not_applicable |  |  |

UI caveats：

- runtime_not_verified / mobile_not_verified / a11y_manual_only / figma_not_verified / not_applicable（运行未验证 / 移动端未验证 / 仅做无障碍人工检查 / Figma 未验证 / 不适用）

## 8. 产出文件

| 文件 | 类型 | 说明 |
|---|---|---|
|  | 新增/修改 |  |

## 9. Evidence 清单

| evidence | 路径 | 是否完整 |
|---|---|---|
|  |  | yes/no |

## 10. 风险与回滚

| 风险 | 等级 | 处置 | 回滚/撤销路径 |
|---|---|---|---|
|  | P0/P1/P2/P3 |  |  |

## 11. 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | planned / running / blocked / completed / needs-human-review |
| 门禁结果 | pass / partial / fail |
| 是否需要人工确认 | yes / no |
| 是否可进入下一轮 | yes / no |
| 连续运行是否必须继续 | yes / no / not_applicable |

## 12. 下一轮建议

- 下一轮 Round ID：
- 下一轮目标：
- 下一轮仍禁止：
