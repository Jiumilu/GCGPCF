---
doc_id: GPCF-DOC-D63AEEB17D
title: Loop Governance Operating Boundary
project: WAES
related_projects: [GFIS, WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md
source_path: 02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Governance Operating Boundary

This document defines the boundary between the implementation main process and
the governance process.

## Process Split

| Process | Responsibility | Boundary |
|---|---|---|
| implementation main process | Produces real GFIS source records, runtime primary keys, review queue entries, runtime intake records, WAES reviews, verified artifacts, and any accepted/integrated evidence. | Must provide real business evidence before business status can advance. |
| governance process | Checks Loop quality, document control, debt visibility, validation coverage, and self-improvement gates. | Must not create or substitute real business facts. |

## Governance Rules

1. The governance process may add validators, review plans, evidence indexes,
   and status ceilings.
2. The governance process may mark missing evidence, historical debt, or review
   required states.
3. The governance process must not create source-of-record, runtime primary key,
   review queue, runtime intake, WAES review, verified artifact, accepted, or
   integrated status.
4. The governance process must not use synthetic, demo, mock, fixture, KDS
   candidate-only, Loop document-only, or oral-only material as a replacement for
   real business evidence.
