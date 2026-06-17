---
doc_id: GPCF-DOC-04BF76145B
title: Loop Execution Rules
project: WAES
related_projects: [GPC, WAES, GPCF]
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

# Loop Execution Rules

This document defines the minimum execution rules for GlobalCloud LOOP work in
the GPCF governance hub. It applies to governance rounds, document rounds,
validator rounds, and controlled repair rounds unless a more specific policy
sets a stricter boundary.

## Required Inputs

Every LOOP round must read or cite the current authoritative inputs:

- `AGENTS.md`
- `02-governance/loop/LOOP_CONTROL_BOARD.md`
- `02-governance/loop/LOOP_AUTONOMY_POLICY.md`
- The latest relevant `docs/harness/loops/loop-round-*.md`
- The current validator or evidence file used for the round decision

If any required input is missing, stale, or contradictory, the round must record
that fact and stop at `partial`, `blocked`, or `repair_required` as appropriate.

## Five-Part Round Contract

Each substantive round must contain five independently reviewable segments:

| Segment | Minimum Requirement |
|---|---|
| Input | What changed, what evidence triggered the round, and which boundary applies |
| Action | What was changed or inspected, including files and commands |
| Output | The produced document, evidence, validator output, or queue item |
| Check | The command, review, comparison, or gate used to verify the output |
| Feedback | The next controlled input, blocker, rollback note, or governance improvement |

Batch-generated artifacts do not automatically count as multiple substantive
rounds. They must satisfy the continuous-running substance rules in
`LOOP_AUTONOMY_POLICY.md`.

## Definition of Done

A LOOP governance round is done only when all applicable items are true:

- The scope and authorization boundary are explicit.
- The output is traceable to controlled evidence or a reproducible command.
- Validators pass, or failures are recorded as the next controlled work item.
- No business status is upgraded without the required evidence and human
  confirmation.
- No `accepted` or `integrated` status is claimed automatically.
- The round preserves dirty-worktree safety and does not overwrite unrelated
  user work.

## Forbidden Shortcuts

- Do not treat a dashboard, backlog, checklist, or validator pass as business
  completion.
- Do not turn missing source-of-record evidence into runtime primary keys,
  review queues, runtime intake, WAES review, verified artifacts, accepted, or
  integrated state.
- Do not perform production write, external API write, schema sync, bench
  migrate, deployment, permission change, commit, push, or merge without
  explicit authorization and rollback evidence.
- Do not bulk rewrite historical round records to make audits appear clean.

## Feedback Routing

Round feedback must become one of:

- A next-round candidate in `LOOP_CONTROL_BOARD.md`.
- A controlled evidence entry under `docs/harness/evidence/`.
- A governance backlog item such as `LEDB-*`.
- A validator improvement under `tools/kds-sync/`.
- An explicit authorization request when the next action exceeds the current
  boundary.
