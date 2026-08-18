---
doc_id: GPCF-DOC-F013-GKE001-A10I3H1R2R2-20260812
title: GKE-001 A10I3H1R2 Secondary Review Scope Correction
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-secondary-review-scope-correction-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-secondary-review-scope-correction-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 A10I3H1R2 Secondary Review Scope Correction

## Result

A second independent technical read-only review confirmed the coordinator's P0 alias-lock finding and P1 startup-count finding. It also found that the proposed four-file H1R3 scope was incomplete. This result is technical evidence only; it is not the canonical F-013 decision and does not authorize implementation.

## Confirmed Evidence

```text
resolved_state_equal=True
lock_path_equal=False
recovery_path_equal=False
child=acquired
recovery_pending=True
published_counts={'apis': 1, 'llms': 1}
```

- `registry_state._state_lock()` resolves the state identity, while lock, recovery and state I/O still derive from the unresolved caller path.
- An independent process using a symlink alias can acquire a second advisory lock while the canonical-path holder is active.
- `runtime/app/db/session.py` reads `runtime/state.json` without the shared recovery boundary, so startup health counts may reflect target or stale state.
- `scripts/dry_run_mmc_dependencies.py` is an additional operational reader outside the shared boundary. It and `runtime/tests/test_dependency_dry_run.py` were missing from the four-file proposal.
- The current spec says every writer uses the lock while `runtime/scripts/seed.sh` is explicitly forbidden. H1R3 must narrow this statement to online runtime and the operational dry-run, leaving seed convergence for H2.

All reproduction work used auto-removed temporary directories. MMC remained at `HEAD=origin/main=b06f58a78ac7713197deed47d1125bec7a260e8c`, 10 dirty entries, staged 0 and no OpsX lock.

## Corrected Review Request

Control: `GKE-001-COORDINATION-20260812-003-A10I3H1R2R2`.

Control SHA-256: `588691af5c5866a481fcc46886df0e9c3cd200a191bcca89295397f7cd0838c3`.

The future H1R3 request is now six product/test paths plus three existing OpenSpec paths, nine total. It covers canonical state/lock/recovery identity, startup health hydration, dependency dry-run recovery, corresponding regressions, and exact online-consumer wording. `runtime/scripts/seed.sh`, `runtime/state.json`, H2/H3, live access and every publication action remain forbidden.

## State Boundary

Classification: `technical_rework_required_scope_corrected_pending_f013_confirmation`.

Brain tranche 3 remains separately `authorized_dispatch_pending_receipt`; neither lane is counted as active implementation. Overall status remains `active / partial / not_complete`.

Rollback is not applicable to MMC because this review made no MMC change. The GPCF correction may be withdrawn without changing product state.
