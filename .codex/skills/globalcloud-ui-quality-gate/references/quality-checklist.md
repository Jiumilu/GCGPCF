---
doc_id: GPCF-DOC-1F2E3D4C5B
title: quality-checklist
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-ui-quality-gate/references/quality-checklist.md
source_path: .codex/skills/globalcloud-ui-quality-gate/references/quality-checklist.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Quality Checklist

Score each required gate as `pass`, `partial`, `fail`, or `not_applicable`. Attach evidence for every `pass` and remediation for every `partial` or `fail`.

## G1 Surface Structure

- Surface type is declared: list, detail, edit/config, operation workbench, exception handling, evidence/audit, AI chat, AI sidebar, brand/marketing, mobile/desktop shell.
- Required zones from the GlobalCloud experience skeleton are present.
- Navigation, back path, primary action, secondary action, and danger action positions are predictable.

## G2 Design Tokens

- Colors use shared semantic tokens: brand, background, text, success, warning, danger, info, muted.
- Governance status colors distinguish running, blocked, partial, review, complete.
- AI suggestion color does not equal business completion color.
- Typography levels, spacing, radius, borders, shadows, and component states follow local design-token rules.

## G3 Component Consistency

- Buttons, inputs, forms, tables, status tags, cards, modals, drawers, toasts, empty/loading/error states share one vocabulary.
- Tables use consistent header, row height, sorting, filtering, action-column, and status-column behavior.
- Dangerous table actions are demoted to menus or require confirmation.
- Icon buttons have tooltips and accessible names.

## G4 Evidence And Governance

- Core object pages expose source record, event chain, evidence list, audit record, current status, confirmer, and confirmation time when applicable.
- Evidence/audit pages show source backlink, timeline, status, risk, and audit log.
- Governance-blocked state is visually distinct from ordinary explanatory text.

## G5 AI Fact Separation

- AI suggestions are separate from business facts.
- AI suggestions cite sources or evidence.
- AI suggestions can be rejected.
- AI prohibited actions are visible.
- No AI output is presented as final business confirmation.

## G6 Accessibility

- Text contrast meets WCAG AA unless explicitly exempted.
- Keyboard focus is visible and logical.
- Forms have labels, errors, required indicators, and recovery guidance.
- Meaningful images have alt text.
- Touch targets are at least 44px where touch interaction is expected.
- Reduced-motion alternatives exist for animation.

## G7 Responsive And Text Robustness

- Check at desktop, tablet, and mobile viewports.
- No horizontal overflow unless the component intentionally scrolls.
- Chinese, English, long identifiers, long organization names, and long status labels do not overlap.
- Tables and cards define responsive behavior.
- Empty, loading, error, permission, and blocked states are implemented.

## G8 Runtime Verification

- Run build/test/lint if appropriate and available.
- Use browser or Playwright screenshots for at least one desktop and one mobile viewport when UI changed.
- Verify keyboard path for forms, modals, drawers, menus, and primary flows.
- Record commands, URLs, screenshots, and failures.

## G9 Scope Control

- Changes are limited to the requested surface and required shared tokens/components.
- Existing local style and framework are preserved unless they violate a gate.
- No unrelated refactor, dependency installation, hook enablement, or generated churn.

## Product-first Human Operability Extension

For every human-facing or human-assisted surface, also record:

- `multi_user_usability_gate`: cover first-time/low-frequency users, frequent professional users, governance/audit users, and any explicitly applicable mobile or accessibility users.
- `human_operable_gate`: a person can discover the entry, understand state and consequences, complete the primary task, and recover from an error without knowing internal API, script, test-selector, or state-machine names.
- `functional_completeness`: required behavior works before usability is marked ready.
- `quality_baseline`: relevant build, test, data-integrity, security, and error-handling checks pass before usability is marked ready.
- Machine interfaces remain available through API/CLI/developer or governance details, but raw payloads, hashes, idempotency keys, and internal state are not default product copy.
