---
doc_id: GPCF-DOC-F013-GKE001-A10I1R1M1-MATRIX-RECONCILIATION-20260812
title: GKE-001 KDS A10I1R1 Acceptance Matrix Reconciliation
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-a10i1r1-matrix-reconciliation-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-a10i1r1-matrix-reconciliation-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 KDS A10I1R1 Acceptance Matrix Reconciliation

## Control

- ID: `GKE-001-COORDINATION-20260812-005-A10I1R1M1`.
- SHA-256: `283dbea9d56fc095cf2cdf775de2cebc5e668eed16d4d027577c418416b608dc`.
- Parent: `GKE-001-COORDINATION-20260811-012-A10I1R1`.
- Repository scope: three persistent governance files in the existing KDS run plus one execution-only lock.
- Product/test/OpenSpec scope: empty.

## Finding And Change

The A10I1R1 CodeGraph replay, handoff and status audit all recorded a passing, up-to-date index, but the run-scoped `acceptance-matrix.md` still contained the pre-replay statements `CodeGraph not run` and `unrun CodeGraph gate`. This was an internal evidence conflict under the Harness handoff protocol.

The bounded correction changed only:

- `.harness/runs/20260811-193752-implement-release0-canonical-read-facade/acceptance-matrix.md`;
- `.harness/runs/20260811-193752-implement-release0-canonical-read-facade/evidence-index.yaml`;
- `.harness/runs/20260811-193752-implement-release0-canonical-read-facade/evidence/acceptance-matrix-a10i1r1m1.txt`.

Final SHA-256 values:

- acceptance matrix: `bb94c7ca6194361811b9046de96956c840bf8e670b4502a784aa62e36b221e38`;
- evidence index: `4b96cca6acb17c7ddcb4d79ccf5b4963512261e0060039bbdf9d0ba27bc00357`;
- reconciliation evidence: `b5b25676735326622a8aa5bba7d32c6cb45eb6c3dc1a38a4dc636c76a2289bf7`.

## Verification

- KDS CodeGraph: `632 files / 5,326 nodes / 13,240 edges`, index up to date.
- Bounded queries: both route builders and five isolated read modules are queryable; the non-symbol coordination label remains an expected empty query.
- Hash boundary: 12/12 A10I1 product/test files and 4/4 shared/excluded files unchanged.
- Matrix text: no `CodeGraph not run` or `unrun CodeGraph` remains.
- KDS Git: `HEAD == origin/main == f28edb5113e0493ed60fec423cb6c7e1a6252de8`, ahead/behind `0/0`, staged `0`, default dirty count `190` before and after, OpsX lock released and absent, diff-check pass.
- GPCF OpenSpec strict and GKE-001 OpenSpec/CodeGraph binding self-test: pass.
- F-013 model, workspace, admission validator and Evidence Gate: pass; admission remains `blocked_dirty_worktree`, Evidence Gate has 12 governance blockers and no close candidate.
- GKE-001 coordination, session registry, pollution and TOKEN: pass after preserving the historical targeted-review marker and recording the matrix re-review separately.
- Project-group readiness: `0/17`, rework required for localization debt and the existing Studio loop failure.
- Loop document gate: `rework_required` for project-group readiness and localization debt; metadata and README coverage remain complete.

## Decision Boundary

The independent byte, CodeGraph and Git-boundary replay is recorded in `gke-001-kds-a10i1r1-matrix-independent-review-closure-20260812.md`. Classification is now `technical_governance_reconciliation_verified_f013_independent_review_passed`; the matrix consistency gate is closed. This correction does not reopen or promote the KDS/Studio implementation batch, does not authorize MMC policy application, and does not establish live authenticated Release 0 integration.

No real/shared KDS or MMC access, database action, product/test/OpenSpec change, credential, commit, push, restart, deployment or status promotion occurred.

Rollback is limited to restoring the three KDS governance files to their pre-A10I1R1M1 bytes. No external-data rollback applies.
