---
doc_id: GPCF-DOC-6A7B8C9D0E
title: tool-routing
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md
source_path: .codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Tool Routing

Use the smallest tool set that can produce evidence.

## Primary Routes

| Scenario | Primary tool | Secondary tool | Notes |
|---|---|---|---|
| Overall interface, page-class, key-component, or structural redesign | `@product-design` | `ui-ux-pro-max` / `Figma` | Must run `get-context -> ideate -> select option`; produce exactly 3 design options before implementation unless the task is a small fix on an already selected direction. |
| Product UI, dashboard, control tower, admin, settings, forms | Impeccable | ui-ux-pro-max | Use Impeccable for audit, harden, polish, layout, clarify, adapt, optimize. |
| New GlobalCloud design system or inconsistent tokens | ui-ux-pro-max | Impeccable document/extract | Persist recommendations only after checking local controlled docs. |
| Figma design implementation or component mapping | Figma skills | Playwright/browser | Use Figma as source of visual truth when a Figma URL or node is provided. |
| Accessibility remediation | accessibility skill or Impeccable audit | Playwright/browser | WCAG, keyboard, focus, ARIA, contrast, form labels, screen-reader semantics. |
| Runtime visual verification | Playwright/browser | Impeccable detect | Use screenshots, viewport matrix, keyboard path, text overflow checks. |
| Brand, marketing, landing, visual identity | frontend-design or Taste Skill | ui-ux-pro-max | Do not apply high-experimentation rules to control towers or evidence pages. |

## Install Boundaries

- Impeccable may be used through `npx impeccable detect` without project install when possible.
- Do not run `npx impeccable install`, enable hooks, copy provider folders, or add submodules without explicit user authorization.
- Do not install accessibility or Playwright skills globally during a project-group UI audit.
- If a tool is unavailable, use local standards plus manual browser verification and mark the missing tool in evidence.

## Product vs Brand Default

GlobalCloud project-group UI defaults to product register:

- restrained color
- consistent components
- dense but readable layout
- evidence and state always visible
- motion for state feedback only
- no decorative motion in operational flows

Professional workbench UI defaults to `WAES` parent-frame reuse:

- shell first
- page skeleton second
- core high-risk components third
- local optimization only after reuse mapping is explicit

Use brand register only for public marketing, landing, portfolio, or presentation surfaces.
