---
doc_id: GPCF-DOC-F013-GKE001-KDS-DIRTY-ISOLATION-20260812
title: GKE-001 KDS Dirty Ownership Isolation And Review Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-dirty-ownership-isolation-and-review-dispatch-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-dirty-ownership-isolation-and-review-dispatch-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 KDS Dirty Ownership Isolation And Review Dispatch

## Control

- ID: `GKE-001-COORDINATION-20260812-010-A10I1D1`.
- Control SHA-256: `d14ef30b401284c833e16bc1f1add845fba7e34cb2f31a29cf85c52e6eec2840`.
- Change: `audit-kds-dirty-ownership-isolation-a10i1d1`.
- Mode: coordinator read-only inspection followed by F-013 independent read-only replay.
- KDS repository allowlist: empty.
- Status ceiling: `active / partial / not_complete`.

## Repository Facts

- KDS `HEAD == origin/main == f28edb5113e0493ed60fec423cb6c7e1a6252de8`; ahead/behind `0/0`; staged `0`; OpsX lock absent.
- Ordinary porcelain: `190` entries (`47` tracked modifications and `143` untracked roots), SHA-256 `51c8985e3eba86cc115cd58fd6cfb1f809857198a8d4ed2b822afb9a31afc905`.
- Expanded porcelain: `462` file entries (`47` tracked modifications and `415` untracked files), SHA-256 `0055f30e91654a23252292f956f665a97242962aff6442964755519c7e7a1b9b`.
- `git diff --check` passed before dispatch.

## Ownership Partition

| owner scope | ordinary | expanded | disposition |
|---|---:|---:|---|
| Release 0 A10I1 implementation/OpenSpec/run | 14 | 35 | Frozen technical change; do not mix with Stage B or runtime facts |
| Stage B extraction implementation/OpenSpec/run | 16 | 36 | Frozen technical change; independent handoff boundary |
| Green supply-chain role view and registry | 2 | 2 | External owner scope; excluded from both technical lanes |
| Business projection content | 59 | 61 | Operational knowledge content; not a code change set |
| Feishu runtime facts | 60 | 171 | Runtime/source facts; owner-specific disposition required |
| KDS governance-generated outputs | 30 | 30 | Governance/sync owner scope |
| KDS audit read views | 5 | 5 | Append-only read-audit projections |
| Disposable local outputs | 3 | 121 | Local output roots; no deletion authorized |
| Automation memory | 1 | 1 | Automation-owned state |
| Unclassified | 0 | 0 | No unknown path remained |

The ordinary total is `190`; the expanded total is `462`. The two totals describe different Git untracked display modes and must not be compared as drift.

## Hash Isolation

- A10I1 12 product/test manifest: `2a551b9c66a37ca15372ffd0046e74fe03dd26cc602be83fe85483b97b18d969`; all `12/12` individual hashes match the sealed run `evidence/source-hashes.txt`.
- A10I1 OpenSpec directory manifest: `badda1fffe8c677a9319b09f91abdfdfa94ddcfa1087fdc3b1bdb419b0ebda48`.
- A10I1 run directory manifest: `3410b7ff0bf576c8613a6d49060e1ab05a67c19ad93b43b1470c63d4703ccb6d`.
- Stage B 14 product/test manifest: `139238548b83a92d4244f300f31fdee127b19960434cc987b67e39f77a3bc370`.
- Stage B OpenSpec directory manifest: `7acdd640e47a6892af715d57038b57de5747f84061cbf3f0034d5bef52dfdeed`.
- Stage B run directory manifest: `9505cf98726d0148b0124022f4dca502837b82ec74e10a262daed29f15881e47`.
- Role-view two-file manifest: `ff43f17a16e82969fc0c93cd0724423872e94fb82b6e15212ba324cb37b0c5b5`.
- Role-view files remain `_registries/global-object-registry.yaml` `76709ef4...1322f` and `entities/green-supply-chain-role-view-entity.md` `ce44a121...8b590`, matching the A10I1 exclusion evidence.

Directory manifests are computed from sorted `shasum -a 256` records for every file below the named directory. Product/test manifests are computed from ordered `shasum -a 256` records in the control's frozen path order.

## Decision And Handoff

Coordinator classification: `ownership_partition_complete_independent_review_pending`.

`dirty=190` is not one coherent patch. It contains two separately reviewed technical changes, one external role-view change, operational knowledge/source facts, governance outputs, audit projections and disposable local outputs. It must not be staged, committed, cleaned, reset, reverted or promoted as one unit.

F-013 is requested to replay the counts, hashes and zero-unclassified result, confirm the two technical manifests and role-view exclusion, and decide whether the partition is sufficient for later owner-specific disposition controls. No KDS file, database, API, process, network, credential or external fact was read or written beyond local Git/file hashing.

## Boundaries

- KDS admission remains `blocked_dirty_worktree`.
- Stage B and A10I1 technical verification remain unchanged; this report does not re-accept either implementation.
- No clean-up, commit, push, deployment, production/shared access, migration, live read, real E2E or status promotion is authorized.
- Rollback is limited to withdrawing this GPCF control/evidence and its Feature/LOOP references. KDS rollback is not applicable because KDS was not mutated.

## F-013 Independent Review

F-013 independently replayed the raw NUL-delimited ordinary and expanded status hashes, every ownership count, all three product-scope manifests and all four OpenSpec/run directory manifests. It confirmed:

- `190 = 47 modified + 143 untracked roots` and `462 = 47 modified + 415 untracked files` with the recorded hashes.
- `unclassified=0` in both views.
- A10I1, Stage B and role-view product path sets are mutually disjoint.
- A10I1 `12/12` source hashes still match the sealed run.
- No KDS file, lock, database, API, network, credential or Git write occurred.

Independent classification: `ownership_partition_verified_for_owner_specific_disposition_controls` with no blocking finding.

This closes only the partition-review gate. The partition is a routing basis, not an execution allowlist. Every later owner-specific disposition must freeze exact paths, actions, pre/post hashes, rollback and exclusions. KDS admission remains `blocked_dirty_worktree`; overall remains `active / partial / not_complete`.
