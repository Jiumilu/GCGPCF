---
doc_id: GPCF-LOOP-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001
title: Loop Round GPCF-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001.md
source_path: docs/harness/loops/loop-round-GPCF-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001

## 输入

- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`
- `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`
- `templates/LOOP_ROUND_TEMPLATE.md`
- `.codex/skills/globalcloud-ui-quality-gate/SKILL.md`
- `.codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md`
- `tools/kds-sync/validate_loop_ui_quality_baseline.py`
- 用户要求：界面工程所使用的工具必须真正具备界面设计、界面质量、界面体验等真实能力；总界面、页面类和重要组件至少给出三种界面设计；统一框架与风格样式保持一致；`@product-design` 必须纳入并真实发挥作用；除上下文外还要建立提示词能力。

## run

1. 复核项目群现有 UI 总控方案、统一规范、UI Quality Gate 技能、Loop 模板和校验器，确认此前已落地 UI gate，但尚未把 `@product-design`、工具上下文包、提示词能力、三方案机制和 `WAES` 母框架复用写成强制字段。
2. 采用最小必要改动策略，不新建平行总控文件，直接增强现有总控文件与统一规范。
3. 将项目群界面工程标准工具链固定为：`@product-design -> WAES -> ui-ux-pro-max -> Figma -> Storybook -> impeccable -> Playwright/browser -> axe-core/Lighthouse -> GPCF UI Gate`。
4. 把 `工具上下文包`、`提示词能力`、`三方案机制`、`WAES baseline reuse` 写入总控方案、统一规范和 Loop 模板。
5. 同步增强 `globalcloud-ui-quality-gate` 技能与 `tool-routing`，使其把 `@product-design` 和 `WAES` 复用路由写成未来 UI 轮次的真实前置。
6. 更新 `validate_loop_ui_quality_baseline.py`，把新增字段与路由纳入机检。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | UI 工具链、上下文包、提示词能力与三方案机制已从原则要求落为受控文档、Loop 模板和校验器约束 |

## verify

本轮执行并通过：

```bash
python3 tools/kds-sync/validate_loop_ui_quality_baseline.py
git diff --check -- 04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md 04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md templates/LOOP_ROUND_TEMPLATE.md .codex/skills/globalcloud-ui-quality-gate/SKILL.md .codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md tools/kds-sync/validate_loop_ui_quality_baseline.py docs/harness/loops/loop-round-GPCF-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001.md
```

关键验证结论：

1. `validate_loop_ui_quality_baseline.py` 现在同时检查 `@product-design`、工具上下文包、提示词能力、三方案机制和 `WAES` 复用字段。
2. `LOOP_ROUND_TEMPLATE.md` 已新增 `Tool route`、`Context package`、`Prompt profile`、`Design options`、`Selected option`、`WAES baseline reuse`。
3. `globalcloud-ui-quality-gate` 技能已把 `@product-design` 设为设计型 UI 工作的前置层，`tool-routing` 已定义其与 `WAES` 的强制路由。

## recover

1. 后续任何 UI 轮次都可以直接复用新增模板字段，不需要再重复定义这套治理结构。
2. 如某项目暂时不具备 `Storybook`、`Figma`、`axe-core` 或 `Lighthouse`，允许保留为 unavailable，但必须显式登记。

## debug

当前仍未关闭的边界：

1. 本轮只完成项目群 UI 工具治理与门禁增强，没有对任一具体界面产出新的三张设计图。
2. `@product-design` 已被纳入强制路由，但其“真实三方案产出”要在后续具体页面/组件设计轮次中执行并留证。
3. 本轮不提升任何项目到 `accepted`、`integrated` 或 `production_ready`。

## 输出

- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`
- `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`
- `templates/LOOP_ROUND_TEMPLATE.md`
- `.codex/skills/globalcloud-ui-quality-gate/SKILL.md`
- `.codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md`
- `tools/kds-sync/validate_loop_ui_quality_baseline.py`
- `docs/harness/loops/loop-round-GPCF-UI-TOOLCHAIN-PROMPT-GOVERNANCE-001.md`

## 连续运行真实性记录

| 字段 | 值 |
|---|---|
| declared_rounds | 1/1 |
| substantive_rounds | 1/1 |
| generated_items | 7 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | evidence_candidate_ready |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | pass |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 下一轮 Round ID：`GPCF-UI-STUDIO-WORKBENCH-023` 或同等级具体页面/组件设计轮次
- 下一轮目标：在真实页面或关键组件上按新机制执行一次 `@product-design` 三方案产出，并记录 `Selected option`
- 下一轮仍禁止：不得把治理增强直接写成具体产品界面已完成
