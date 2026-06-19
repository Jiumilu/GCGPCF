---
doc_id: GPCF-DOC-04BF76145B
title: LOOP_EXECUTION_RULES
project: WAES
related_projects: [WAES]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_EXECUTION_RULES.md
source_path: 02-governance/loop/LOOP_EXECUTION_RULES.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# LOOP_EXECUTION_RULES

## Mandatory Inputs

Every Loop governance or execution round must read the active repository
instructions and control state before changing files:

- `AGENTS.md`
- `02-governance/loop/LOOP_CONTROL_BOARD.md`
- `02-governance/loop/LOOP_AUTONOMY_POLICY.md`

If any of these documents are missing, empty, or internally inconsistent, the
round must stop at governance repair and must not upgrade project status.

## Definition of Done

A Loop round can be treated as complete only when all applicable items are true:

- Scope and authorization boundary are stated.
- Inputs, actions, outputs, checks, and feedback are recorded.
- Validation commands or evidence references are listed.
- `declared_rounds`, `substantive_rounds`, `generated_items`,
  `batch_generated`, `substance_gate`, and `stop_type` are recorded when the
  round belongs to a continuous mode.
- Non-claims are explicit when the round does not create source-of-record,
  runtime primary key, review queue, runtime intake, WAES review, verified
  artifact, accepted, or integrated status.

## Non-Bypass Rules

- A passing document or validator check does not prove business completion.
- No round may mark `accepted` or `integrated` without the required evidence and
  human authorization.
- No round may authorize production write, external API write, schema sync,
  bench migrate, deployment, permission change, commit, or push unless that
  action is explicitly authorized and separately evidenced.
