---
doc_id: GPCF-DOC-44D11B1ED6
title: GKE-001 A10I3H1R1 Coordinator Replay And A10I3H1R2 Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r1-coordinator-replay-and-a10i3h1r2-dispatch-20260811.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r1-coordinator-replay-and-a10i3h1r2-dispatch-20260811.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

# GKE-001 A10I3H1R1 Coordinator Replay And A10I3H1R2 Dispatch

## Decision

`A10I3H1R1` remains `technical_rework_required`. The coordinator reproduced two reachable shared-state failures outside the four-file H1R1 boundary. The H1 technical gate is not closed.

## Exact Reproductions

The coordinator used only a temporary directory and local in-process calls. No repository file, real registry, API, database, credential or external state was changed.

```text
unresolved_recovery_registry_api=blocked_503
unresolved_recovery_connector_exposes_target=true
guarded_status=200
concurrent_llm_patch_reported_rpm=2
final_llm_rpm=1
llm_update_lost=true
```

The first result proves that `registry_apis` fails closed while `connectors._load()` still reads the same target `runtime/state.json` during unresolved recovery. The second proves that `registry_llms.patch_llm()` can report success while a guarded API policy mutation later overwrites the LLM field with its older full-state snapshot.

## Root Cause

The stable lock and durable recovery implementation is local to `registry_apis.py`, but the same `runtime/state.json` is also read or written directly by:

- `runtime/app/api/v1/registry_llms.py`
- `runtime/app/api/v1/connectors.py`
- `runtime/app/api/v1/health.py`

This violates the H1R1 requirements that unresolved recovery must prevent target-policy publication and that all writers sharing the state file must serialize without lost updates.

## A10I3H1R2 Dispatch

Control: `GKE-001-COORDINATION-20260811-019-A10I3H1R2`.

The minimal repair is limited to eight product/test files. It introduces one shared state transaction primitive and binds API registry, LLM registry, connector reads and readiness reads to the same resolved-path lock/recovery boundary. The policy, seed, runtime registry, credentials and external services remain unchanged.

H2 seed mutation, H3 runtime policy application, live read, Brain expansion and authenticated E2E remain unauthorized.

## Current Status

```text
engineering=active
cross_project=partial
completion=not_complete
H1=technical_rework_required
H2=false
H3=false
```

Rollback is limited to the future H1R2 local delta and its governance package. No external rollback exists because no external state was changed.
