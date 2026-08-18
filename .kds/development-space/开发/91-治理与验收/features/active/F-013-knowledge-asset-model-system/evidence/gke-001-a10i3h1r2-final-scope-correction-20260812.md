---
doc_id: GPCF-DOC-F013-GKE001-A10I3H1R2R3-20260812
title: GKE-001 A10I3H1R2 Final Scope Correction
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-final-scope-correction-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-final-scope-correction-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 A10I3H1R2 Final Scope Correction

## Result

A Harness `audit_only` replay independently confirmed the H1R2 resolved-path, startup-count, operational dry-run and specification findings. It also found that the nine-path H1R3 proposal remained incomplete because its OpenSpec allowlist omitted `proposal.md`.

Control `GKE-001-COORDINATION-20260812-006-A10I3H1R2R3` corrects the future request to six product/test paths plus four OpenSpec paths, ten total. Control SHA-256: `06a34a9b05078fe26897c15070315e919886b132e02c8006fcf50fce8f32e0ff`.

This is a scope correction, not the canonical F-013 decision. H1R3 implementation remains unauthorized.

## Independent Findings

1. `registry_state._state_lock()` resolves only the in-process lock key. OS lock, recovery and atomic replacement still derive from the caller path. A file symlink can acquire a different advisory lock and alias save can replace the symlink instead of updating the canonical target.
2. `runtime/app/db/session.py` reads the target directly during startup count hydration and can publish uncommitted or stale counts while recovery is pending.
3. `scripts/dry_run_mmc_dependencies.py` directly reads `runtime/state.json` and can validate an uncommitted target during pending recovery.
4. The current `Every writer` requirement conflicts with the explicit deferral of `runtime/scripts/seed.sh` to H2. H1R3 must say online runtime readers/writers plus the operational dry-run.
5. The H1R2 evidence package is structurally present, but its evidence rows lack explicit freshness and trust-level metadata; replay claims must become machine-replayable in H1R3.

## Corrected Future Scope

Product/test paths, six:

- `runtime/app/gateway/registry_state.py`
- `runtime/app/db/session.py`
- `scripts/dry_run_mmc_dependencies.py`
- `runtime/tests/test_registry_policy_audit.py`
- `runtime/tests/test_api.py`
- `runtime/tests/test_dependency_dry_run.py`

OpenSpec paths, four:

- `openspec/changes/rework-mmc-shared-registry-state-a10i3h1r2/proposal.md`
- `openspec/changes/rework-mmc-shared-registry-state-a10i3h1r2/design.md`
- `openspec/changes/rework-mmc-shared-registry-state-a10i3h1r2/specs/shared-registry-state/spec.md`
- `openspec/changes/rework-mmc-shared-registry-state-a10i3h1r2/tasks.md`

The earlier nine-path request is superseded and must not be implemented.

## Boundaries

MMC remained at `HEAD=origin/main=b06f58a78ac7713197deed47d1125bec7a260e8c`, 10 dirty entries, staged/ahead/behind `0/0/0`, with no OpsX lock. Temporary test state was removed.

`runtime/scripts/seed.sh`, `runtime/state.json`, H2, H3, live-read, real E2E, credentials, commit, push, restart, deployment and status promotion remain forbidden.

Status remains `active / partial / not_complete`. Rollback for this review is withdrawal of the GPCF correction only; no MMC mutation exists to reverse.
