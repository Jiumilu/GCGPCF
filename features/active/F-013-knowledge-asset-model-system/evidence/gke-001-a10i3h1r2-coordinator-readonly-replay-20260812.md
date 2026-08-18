---
doc_id: GPCF-DOC-4FABA57E57
title: GKE-001 A10I3H1R2 Coordinator Read-Only Replay
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-coordinator-readonly-replay-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-coordinator-readonly-replay-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 A10I3H1R2 Coordinator Read-Only Replay

## Scope

- control: `GKE-001-COORDINATION-20260812-001-A10I3H1R2R1`
- parent implementation: `GKE-001-COORDINATION-20260811-019-A10I3H1R2`
- MMC baseline: `HEAD=origin/main=b06f58a78ac7713197deed47d1125bec7a260e8c`
- mode: disposable temporary files and independent local processes only
- repository write allowlist: empty

## P0 Reproduction

The frozen H1R2 specification requires independent processes addressing the same resolved state path to share one advisory lock identity.

Observed output:

```text
resolved_state_equal=True
lock_path_equal=False
second_process_acquired_while_first_held=True
second_stdout=acquired
holder_rc=0 waiter_rc=0
```

The first process held `registry_state.locked_state(real_state)`. The second process addressed the same file through a file symlink and acquired `registry_state.locked_state(alias_state)` before the first released. No shared/runtime repository file was read or written by the reproduction.

Root cause:

- `registry_state._state_lock()` keys the process-local lock by `path.resolve()`.
- `registry_state.lock_path()` and `registry_state.recovery_path()` derive sidecars from the unresolved caller path.
- Independent processes therefore open different sidecar files for two aliases of the same resolved state file.

Impact:

- H1R2 does not satisfy its exact resolved-path advisory-lock requirement.
- Alias-based independent writers can bypass serialization; atomic replacement through an alias can also split the alias from the canonical state path.
- The H1R2 handoff cannot be accepted on current evidence.

## P1 All-Consumer Gap

`runtime/app/db/session.py` still directly reads `runtime/state.json` during file-mode startup count hydration. H1R2 disclosed this path but its OpenSpec states that all file-mode registry consumers share one state transaction. F-013 must decide whether to include it in H1R3 or narrow the contract with an explicit, evidence-backed exception.

## Proposed H1R3 Scope Sufficiency

A second static call-site audit found no additional runtime product path that directly reads `runtime/state.json` outside the shared registry module except `runtime/app/db/session.py`. API registry, LLM registry, connector and readiness callers already enter through `registry_state`; their product files do not need another edit for this finding.

The proposed four paths are sufficient for a bounded repair:

- `runtime/app/gateway/registry_state.py`: canonicalize the state path once, then derive state, recovery and advisory-lock I/O from that canonical path.
- `runtime/app/db/session.py`: hydrate file-mode startup counts through the shared fail-closed load boundary.
- `runtime/tests/test_registry_policy_audit.py`: prove aliases share one advisory identity, an independent alias writer waits, and all state/recovery I/O targets the canonical path.
- `runtime/tests/test_api.py`: prove startup count hydration uses the shared boundary and does not publish stale counts when recovery is unresolved.

This confirms scope sufficiency only. It does not authorize H1R3 implementation or modify the required F-013 independent-review gate.

## Concurrent Baseline Facts

- Studio is clean at `HEAD=origin/main=953d4d1baea201cc0fc822074bc74cad9299d0dd`, external daily clean sync, 23-file commit.
- Brain is clean at `HEAD=origin/main=925659b0144a5fb858a78cf32c1d8ddf6967c19b`, external daily clean sync, 18-file commit.
- Studio's 23 committed paths equal the prior A10I1/A10I1R1 product, test and governance-package scope; Brain's 18 committed paths equal the preserved A7 seven-file delta, its existing evidence/OpenSpec scope and the A10P1 six-file tranche. This establishes path continuity only.
- These Git actions were not authorized or ratified by this coordinator; no new Studio or Brain execution is authorized by observing them.

## Review Dispatch Receipt

- The coordinator attempted to send this read-only blocker control to the F-013 reviewer task, but the task interface returned no delivery receipt before timeout.
- F-013 confirmation is therefore still unverified; the proposed H1R3 scope remains unauthorized.
- A separate read-only check of the previously closed KDS A10I1R1 package confirmed its CodeGraph index at `632 files / 5326 nodes / 13240 edges`, all 12 product/test hashes and four shared/excluded hashes unchanged. The current KDS ordinary dirty count is `190`, so the historical A10I1R1 count of `180` is not treated as a current repository-state assertion.

## Decision

Classification: `technical_rework_required_pending_f013_confirmation / active / partial / not_complete`.

No MMC product/test/OpenSpec/handoff file was modified. No KDS/MMC API, shared data, credential, commit, push, restart, deployment or status promotion occurred. A proposed four-file H1R3 scope is recorded in the control artifact but remains unauthorized until F-013 independent confirmation.
