---
doc_id: GPCF-DOC-9A8B7C6D5E
title: evidence-output
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-ui-quality-gate/references/evidence-output.md
source_path: .codex/skills/globalcloud-ui-quality-gate/references/evidence-output.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Evidence Output

Use this structure for UI quality reports and evidence candidate documents.

## Required Summary

```text
UI gate status: ui_ready | ui_partial | ui_blocked | ui_rework_required
Surface:
Repository/path:
Scope:
Tools used:
Tools unavailable:
Verification:
Status ceiling:
```

`Status ceiling` is always UI-specific. It cannot exceed `ui_evidence_candidate` unless a separate Harness/WAES/GPCF process upgrades the broader project status.

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass/partial/fail/na | file, screenshot, command, or observation | action |
| G2 Design Tokens | | | |
| G3 Component Consistency | | | |
| G4 Evidence And Governance | | | |
| G5 AI Fact Separation | | | |
| G6 Accessibility | | | |
| G7 Responsive And Text Robustness | | | |
| G8 Runtime Verification | | | |
| G9 Scope Control | | | |

## Required Caveats

- If no browser/runtime was launched, say `runtime_not_verified`.
- If no mobile viewport was checked, say `mobile_not_verified`.
- If accessibility was only inspected manually, say `a11y_manual_only`.
- If Impeccable or accessibility tools were unavailable, say which checks were substituted.
- If Figma exists but was not consulted, say `figma_not_verified`.

## Evidence Writing Rules

- Write Chinese reports by default for GlobalCloud project documentation.
- Keep facts, inference, and pending confirmation separate.
- Do not write external-tool recommendations as accepted project facts.
- Do not write secrets, tokens, API keys, or private URLs into evidence.
- Do not update KDS or controlled status records unless the user explicitly requests document governance work.
