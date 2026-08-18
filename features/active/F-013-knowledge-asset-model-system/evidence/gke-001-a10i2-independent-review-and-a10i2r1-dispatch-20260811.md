---
doc_id: GPCF-DOC-F013-GKE001-A10I2-REVIEW-A10I2R1-DISPATCH-20260811
title: GKE-001 A10I2 Independent Review and A10I2R1 Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2-independent-review-and-a10i2r1-dispatch-20260811.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2-independent-review-and-a10i2r1-dispatch-20260811.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

# GKE-001 A10I2 Independent Review and A10I2R1 Dispatch

## Decision

F-013 classified A10I2 as:

`technical_rework_required / handoff_not_accepted / active_partial_not_complete`

## Findings

1. MMC emitted `aud=kds` plus `knowledge_read=true` but omitted frozen KDS `permissions`, `project_scopes` and `session_scopes`; current KDS DelegationVerifier rejects the claim.
2. MMC OpenAPI composed a closed authority object with `allOf`, so valid search/read instances fail; graph/wiki options, cursor/header bounds and success response fields do not match the frozen schema.
3. Existing reachable tests exercise search only; read, graph and wiki-preview plus real KDS verifier compatibility are not proven.
4. Release 0 bypass denial returns before the bounded MMC denied audit path.

The review separately confirmed scope/hash integrity, Studio signature-before-scope ordering, exact scope equality, nonce/lifetime/signature, caller KDS header stripping, registry-before-upstream, bounded error projection, generic invoke/rate/circuit behavior and no second ledger.

## Rework Control

- ID: `GKE-001-COORDINATION-20260811-014-A10I2R1`.
- SHA-256: `ef4065c374f5f2be480c170b3a4e60bef54a72b0d8ee40c3bd3c7fb5e12cbd2e`.
- Product/test limit: the original exact six paths.
- `runtime/scripts/contract_test.py`, seed/state, core delegation modules and every policy/runtime file remain forbidden.

## Boundary

A10I2R1 must prove a KDS-verifier-compatible signed claim, field-level frozen OpenAPI valid/invalid instances, separate search/graph/wiki-preview reachable tests and bounded bypass denied audit. It must preserve all previously accepted behavior and return a new standard OpsX package. High-risk policy configuration, live-read, Brain, Studio, real E2E, credentials, commit, push, restart, deploy and promotion remain unauthorized.

Overall status remains `active / partial / not_complete`.
