---
doc_id: GPCF-DOC-F013-GKE001-A10P0-HANDOFFS-20260811
title: GKE-001 A10P0 Three Handoffs And F-013 Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p0-three-handoffs-and-f013-dispatch-20260811.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p0-three-handoffs-and-f013-dispatch-20260811.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

# GKE-001 A10P0 Three Handoffs And F-013 Dispatch

- Control SHA-256: `b9d4acdef872289afd5a2194a1430daf977bab028f9fc76ce6e937f39e8ecc96`.
- Studio/MMC: 3/3 focused tests; both repos clean/0/0/unlocked; authoritative project and KDS persistent audit are not enforced; policy fingerprint `40a674577b73422c98936a69efd1b3a317d1999d5a44dfd0b4635842067c0a5e`.
- Brain: 84/84 focused tests and static alignment pass; typecheck remains 86 errors in 25 files; A7 nine-entry delta unchanged; no prompt auto-send.
- KDS: A9 evidence hashes unchanged; 166 dirty entries, staged 0, unlocked; Stage B and legacy project reads are incompatible; legacy routes lack delegation, ACL, authoritative project binding and KDS audit.
- Common zero-access statement: no live KDS/MMC, database, prompt/LLM, credential, write, commit, push, restart, deployment or status promotion.
- Common rollback: withdraw the report scope; no repository/runtime/data restore applies.
- F-013 request: independently review the exact endpoint, identity, project-binding, ACL/count, audit, policy, rollback and next-tranche boundaries.
- Status: `active / partial / not_complete`; A10 live-read and real E2E remain unauthorized.
