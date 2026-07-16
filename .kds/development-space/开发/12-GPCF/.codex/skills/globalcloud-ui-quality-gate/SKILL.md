---
doc_id: GPCF-DOC-3E7F2A1B9C
name: globalcloud-ui-quality-gate
description: GlobalCloud 项目群 UI 质量门禁技能。用于评估、设计、改造、审计或验收 GlobalCloud 产品界面、控制塔、工作台、证据页、异常页、AI 对话页、配置页、移动端和桌面端 UI 时，组合 @product-design、Impeccable、ui-ux-pro-max、accessibility、Playwright/browser、Figma 等能力，并强制对齐项目群统一体验骨架、设计令牌、AI 建议/业务事实隔离、证据与状态门禁。只产出 UI evidence candidate 和整改建议，不自动升级 complete/accepted/integrated。
---

# GlobalCloud UI Quality Gate

## Overview

本技能用于把 GlobalCloud 项目群 UI 工作从“好看”收口到“可审计、可复现、可验收”。它不替代 `@product-design`、Impeccable、ui-ux-pro-max、Figma、accessibility 或 Playwright，而是规定这些能力在项目群中的调用顺序、门禁边界和 evidence 输出格式。

## Non-Negotiables

- 不把 UI 改进、截图通过、设计系统生成写成业务完成。
- 不把 AI 建议伪装成业务事实；AI 建议必须有来源或证据引用，且可驳回。
- 不绕过仓库 preflight、证据门、状态门、KDS/文档门禁或 Harness/WAES 验收。
- 不自动安装外部 skill、全局 hook、浏览器扩展或项目依赖；只有用户明确授权时才安装。
- 不自动标记 `complete`、`accepted` 或 `integrated`。本技能输出最高是 `ui_evidence_candidate`。
- 产品界面优先考虑任务效率、密度、可读性、状态反馈和证据入口；品牌/营销页才使用更强视觉实验。
- 严格遵守 `DO NOT send optional commentary`；UI gate 输出只保留必要结论、阻塞项、确认请求、整改证据和验证结果。
- 必须遵守 `LOOP_UI_PRODUCT_FIRST_CONTROL.md`：UI evidence is not UI structure；治理证据可追溯但不得默认主导产品界面；技术细节默认进入调试或治理详情。

## Required Local Context

Before assessing or changing UI, read the relevant local standards when present:

- `AGENTS.md`
- `02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md`
- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`
- `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`
- `04-ui-delivery/GlobalCloud绿色供应链体系统一体验骨架规范.md`
- `04-ui-delivery/GlobalCloud绿色供应链体系统一组件与设计令牌规范.md`
- `04-ui-delivery/GlobalCloud绿色供应链体系对话模式与操作模式规范.md`
- `02-governance/GlobalCloud智能体团队Codex工具与技能使用治理规范.md`
- `02-governance/gpcf-role-boundary.md`

If working inside a project repo rather than GPCF, also read its local `AGENTS.md`, design tokens, representative component/page, and `docs/harness/loop-state.md` if present.

## Workflow

1. **Classify the surface.** Use one type: list, detail, edit/config, operation workbench, exception handling, evidence/audit, AI chat, AI sidebar, brand/marketing, or mobile/desktop shell.
2. **Select tools.** Read `references/tool-routing.md` and use only the minimum set needed. `@product-design` is the mandatory design-brief and three-option layer for overall interface, page-class, key-component, and structural redesign work; Impeccable is the product UI main engine when available; ui-ux-pro-max is the design-system source; accessibility and Playwright/browser provide verification.
3. **Create or inspect the design system.** For new or inconsistent UI systems, use `ui-ux-pro-max` to derive a GlobalCloud design system. Professional workbench surfaces must first map to the existing `WAES` UI framework before project-level optimization. For existing code, preserve committed tokens unless they violate project-group rules.
4. **Audit against gates.** Read `references/quality-checklist.md`. Score every gate with evidence: `pass`, `partial`, `fail`, or `not_applicable`.
   For Studio or product-workbench surfaces, also score `product_first_ui_gate`, `evidence_overexposure_gate`, `debug_details_visibility`, `task_flow_e2e_status`, `audit_traceability_gate`, `multi_user_usability_gate`, and `human_operable_gate`. Functional completeness and quality baseline must pass before usability can be considered ready; machine/test operability alone is insufficient.
5. **Implement only when asked.** If the user asked for changes, make surgical UI edits in the target repo. Do not refactor unrelated components.
6. **Verify with real evidence.** Use browser screenshots, responsive checks, keyboard/focus checks, automated tests, or Playwright where available. If a check cannot run, mark it `not_verified`.
7. **Report status safely.** Read `references/evidence-output.md` and output a UI gate report. Never claim project status completion from UI evidence alone.

When a task is design-led rather than fix-led, require the UI round to record:

- `Tool route`
- `Context package`
- `Prompt profile`
- `Design options`
- `Selected option`
- `WAES baseline reuse`

## Gate Model

Use this status vocabulary:

- `ui_ready`: all required UI gates pass and verification evidence exists.
- `ui_partial`: some gates pass but gaps remain.
- `ui_blocked`: required local context, runtime, assets, permissions, or verification are missing.
- `ui_rework_required`: implementation conflicts with GlobalCloud UI/governance rules.

These are UI-quality labels only. They do not imply business `complete`, `accepted`, or `integrated`.

## Reference Files

- Read `references/tool-routing.md` when choosing Impeccable, ui-ux-pro-max, Figma, accessibility, Playwright/browser, Taste Skill, or frontend-design.
- Read `references/quality-checklist.md` before auditing or modifying UI.
- Read `references/evidence-output.md` before final reporting or writing evidence.

## Recommended Command Patterns

When tools are available and authorized:

```bash
# Design-system recommendation from local skill.
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "GlobalCloud green supply chain product dashboard governance evidence" --design-system -p "GlobalCloud UI"

# External Impeccable CLI, only if already installed or explicitly authorized.
npx impeccable detect --json <target>
```

Prefer project-local, no-hook, read-only audit first. Do not run `npx impeccable install`, add `.codex/hooks.json`, or enable automatic hooks unless the user explicitly asks.
