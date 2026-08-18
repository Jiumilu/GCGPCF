---
doc_id: GPCF-DOC-F013-GKE001-STUDIO-A10I1G1-DISPATCH-20260812
title: GKE-001 Studio A10I1G1 Post-commit CodeGraph Reconciliation Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-studio-postcommit-codegraph-reconciliation-dispatch-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-studio-postcommit-codegraph-reconciliation-dispatch-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 Studio A10I1G1 Post-commit CodeGraph Reconciliation Dispatch

## Current Fact

Studio is clean at `HEAD == origin/main == 953d4d1baea201cc0fc822074bc74cad9299d0dd`; its direct parent is the LR-876 pre-commit baseline `88769078f5c230ae9ed973815de4861cc6317a5c`. The current Studio LOOP validator fails only with `committed scope content differs from precommit evidence`.

LR-876 schema v3 declared `.harness/opsx.lock` in `scopeFiles`, excluded it from `changedFilesAfter`, and sealed only one aggregate `scopeContentHashAfter`. The lock was execution-only and is now correctly absent. Because the old evidence has no per-file hash map, simply filtering the lock from the current calculation cannot prove that the committed persistent files equal the pre-commit state. A waiver or silent rewrite of LR-876 would weaken drift detection and is forbidden.

## Controlled Action

`GKE-001-COORDINATION-20260812-004-A10I1G1` authorizes one Studio governance lane with exactly three product/test paths:

- `tools/codegraph_loop_evidence.py`
- `tools/kds-sync/validate_studio_loop_control.py`
- `tests/server/studio-loop-control.test.ts`

The lane must add a backward-compatible schema v4 persistent-scope protocol and an immutable LR-877 post-commit reconciliation. The receipt must validate the LR-876 evidence hash, the exact direct parent relation, the exact commit path set, current persistent per-file SHA-256 values, and the existing F-013 A10I1R1 review reference. It must state that the old aggregate is not reconstructably comparable; it may not claim an invented match.

## Boundary

LR-876 files are immutable. Studio application source, KDS, MMC, Brain, credentials, network calls, commit, push, restart, deployment, live E2E and status promotion are not authorized. The lane remains `authorized_dispatch_pending_receipt`; after its standard OpsX handoff it freezes for F-013 independent review.

Overall status remains `active / partial / not_complete`.
