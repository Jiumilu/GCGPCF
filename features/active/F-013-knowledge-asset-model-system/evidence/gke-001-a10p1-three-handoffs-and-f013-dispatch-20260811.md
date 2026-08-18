---
doc_id: GPCF-EVIDENCE-GKE-001-A10P1-HANDOFFS-F013-DISPATCH-20260811
title: GKE-001 A10P1 Three Handoffs and F-013 Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p1-three-handoffs-and-f013-dispatch-20260811.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p1-three-handoffs-and-f013-dispatch-20260811.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

# GKE-001 A10P1 Three Handoffs and F-013 Dispatch

## Control

- ID: `GKE-001-COORDINATION-20260811-006-A10P1`.
- SHA-256: `264a50bb1020a97777761371fb331f6a6c05e6ed3698875d27107b0c79bfd1bb`.
- Status: `active / partial / not_complete`.

## Studio/MMC Handoff

- Repositories remained clean, ahead/behind `0/0`, with no OpsX lock and no file or runtime change.
- Proposed server-trusted chain: authenticated user -> owned project session -> `SessionBindingContext` -> authoritative `targetObjectRef` -> KDS project verification.
- Proposed no-leak boundary uses 401 for missing login, bounded 403 for missing business identity, and uniform 404 for unavailable project context.
- Proposed Studio adapter uses session-scoped routes and derives project context server-side.
- Proposed MMC policy has two operations, with current/restore fingerprint `40a674577b73422c98936a69efd1b3a317d1999d5a44dfd0b4635842067c0a5e` and isolated fingerprint `7cda2ae47668fa0bcdf6e085034a91cafb33ee0e4078e742a5072456a1413074`.
- No live KDS/MMC request, policy change, binding write or credential action occurred.

## KDS Handoff

- Repository remained at `f28edb5113e0493ed60fec423cb6c7e1a6252de8`, ordinary dirty count `166`, staged `0`, ahead/behind `0/0`, lock absent.
- Proposed contract: `globalcloud.kds.canonical-read`, revision `release0.v1`, with search, graph and wiki-preview operations.
- Proposed projections preserve singular canonical identity and derive graph nodes/edges only from existing KnowledgeObject, asset, version, extraction, block and EvidenceLink identities.
- Proposed Release 0 authorization requires exact tenant/org, project scope, `session_ref`, `session_scopes` and authoritative target binding before rows/rank/count.
- Proposed audit matrix covers success/denied/not_found for all three reads and fails closed when audit persistence is unavailable.
- No repository, database, API, network, fixture, registry or role-view change occurred.

## Brain Handoff

- Exactly six allowed product/test files changed; all nine A7 baseline entries were preserved.
- Focused Vitest: `29/29` passed.
- Read-model alignment passed; OpenSpec strict `1/1` passed without OpenSpec writes; CodeGraph synchronized; diff-check passed.
- Full typecheck improved from `86` errors in `25` files to `49` errors in `19` later files; the six-file tranche has zero remaining errors.
- Machine summary: typecheck from 86 errors/25 files to 49 errors/19 files.
- A standard run-scoped OpsX handoff, evidence index, acceptance matrix, six-file patch, agent receipt and final verification were created under the authorized run directory.
- The execution-only lock was released and is absent.
- No browser, network, KDS/MMC, LLM or prompt-send action occurred; no commit, push, deployment or promotion occurred.

## Contract Conflict Requiring F-013 Decision

- KDS proposes three `POST` operations under `/api/v1/knowledge-read/release-0/{search|graph|wiki-preview}`.
- Studio/MMC proposes two operations under `/api/v1/release-0/projects/{projectId}/{search|read}` with `POST` search and `GET` read.
- Request bounds and content identity also differ: KDS uses canonical target/project/session refs and asset/extraction/block/cell/evidence projections; Studio/MMC still describes a project/path/max_chars adapter shape.
- Neither proposal is frozen, implemented or authorized for live use. F-013 must choose one canonical contract or return rework.
- Machine summary: two facade proposals conflict on method, path and request identity.

## F-013 Review Request

Independently verify:

1. all three handoffs and repository/lock preservation;
2. Brain exact six-file scope, evidence package and `86 -> 49` typecheck claim;
3. whether either API proposal can be frozen without rework;
4. the exact canonical method/path/request/response identity for Search, Graph and WikiPreview;
5. server-side session ownership and authoritative project binding;
6. session-scope ACL, complete persistent per-read audit and MMC two-operation isolation;
7. the next minimum implementation tranche, while keeping live-read and real E2E unauthorized.

## Boundary and Rollback

- All three A10P1 lanes are frozen after handoff.
- No live KDS/MMC read/write, real E2E, Studio/MMC/KDS implementation, commit, push, restart, deployment or status promotion is authorized.
- Report rollback is withdrawal; Brain rollback is the uncommitted six-file patch back to the A7 baseline.
- No external data rollback applies.
