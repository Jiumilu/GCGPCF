---
doc_id: GPCF-DOC-F013-GKE001-KDS-STAGEB-RELEASE0-ORDER-20260812
title: GKE-001 KDS Stage B Release 0 Dependency Order And Review Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-release0-dependency-order-and-review-dispatch-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-release0-dependency-order-and-review-dispatch-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 KDS Stage B Release 0 Dependency Order And Review Dispatch

## Control

- ID: `GKE-001-COORDINATION-20260812-011-A10I1D2`.
- Control SHA-256: `a226a75e1d839678b79ea941def964b69e0e2876b7c49510b256882017ac6e5d`.
- Change: `verify-kds-stageb-release0-dependency-order-a10i1d2`.
- Mode: report-only source inspection and disposable clean-baseline replay.
- KDS repository allowlist: empty.
- Status ceiling: `active / partial / not_complete`.

## Dependency Finding

A10I1 and Stage B are disjoint ownership sets but not independent runtime sets. `read_contract`, `read_repository` and `read_postgres` consume Stage B extraction types and repository behavior. A clean `f28edb51` baseline with only the 12 A10I1 product/test paths fails during collection because `knowledge_intake.extraction` is absent.

The existing `api_server.py` also imports the repository-sibling `shared.python_utils` package through the tracked `shared -> ../shared` link. A disposable archive must preserve that pre-existing runtime dependency to evaluate the two Release 0 entry tests; its absence caused two infrastructure-only failures in the first combined replay and did not indicate a Stage B/A10I1 contract conflict.

## Disposable Replay Matrix

| baseline overlay | result | interpretation |
|---|---|---|
| clean HEAD + A10I1 12 paths | 4 collection errors, missing `knowledge_intake.extraction` | A10I1 cannot land before Stage B |
| clean HEAD + Stage B 14 paths | 66 passed | Stage B is independently replayable |
| clean HEAD + Stage B 14 + A10I1 12 + existing `shared` runtime dependency | 107 tests: 101 passed, 6 skipped, 0 failed/errors | Stage B then A10I1 is technically coherent |

All final disposable roots were removed and verified absent. One root left by an earlier interrupted command was explicitly removed before the sealed replay. No repository file, database, API, process, network endpoint, credential, corpus or external fact was changed.

## Coordinator Decision

The technical sets remain separate. The required order is:

```text
Stage B owner-specific disposition
-> clean Stage B baseline and independent replay
-> A10I1 rebase/replay on that baseline
-> F-013 joint revalidation
-> separately authorized Git/integration decision
```

The 26 product/test paths must not be combined into one commit or handoff. External role-view files and the remaining operational/governance dirty scopes remain excluded. KDS admission stays `blocked_dirty_worktree`.

## Review Request

F-013 is requested to independently verify the import dependency, the three replay outcomes, disposable cleanup, zero KDS mutation and the serial order. This review does not authorize staging, commit, push, cleanup, deployment, live read, real E2E or status promotion.

## Rollback

Withdraw only this GPCF control/evidence and its Feature/LOOP references. KDS and external data rollback are not applicable because the KDS working tree and runtime were not mutated.

## F-013 Independent Review

F-013 independently confirmed the control hash, static import dependency, sealed replay records, current KDS Git/status hashes and absence of every named disposable root. It found no KDS repository, runtime, database, API, network or credential mutation.

Independent classification: `dependency_order_verified_owner_sets_must_remain_separate`.

The verified order is Stage B owner-specific disposition, clean Stage B baseline replay, A10I1 rebase/replay on that baseline, F-013 joint revalidation, then a separately authorized Git/integration decision. The 26 product/test paths remain two ownership sets and must not be combined into one commit or handoff. KDS admission remains `blocked_dirty_worktree`; overall remains `active / partial / not_complete`.
