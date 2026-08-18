---
doc_id: GPCF-EVIDENCE-GKE-001-A10P3-REPORTS-A10P3R1-DISPATCH-20260811
title: GKE-001 A10P3 Reports and A10P3R1 Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p3-two-reports-and-a10p3r1-dispatch-20260811.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p3-two-reports-and-a10p3r1-dispatch-20260811.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

# GKE-001 A10P3 Reports and A10P3R1 Dispatch

## A10P3 Result

- Both report-only lanes preserved their repository baselines, staged state and lock boundaries and performed zero live or write action.
- KDS proved `SearchRequest` rejects a valid instance because `CommonAuthority` used `additionalProperties:false` under `allOf`.
- KDS also identified Stage B mapping gaps for lifecycle `parsing`, digest prefix, OCR kind, confidence normalization, bounded text and lossless PDF/DOCX/XLSX/image/text locators.
- Studio/MMC provided exact clean future paths: Studio 10 and MMC 8. It also confirmed the current Studio bridge lacks session binding and the MMC connector wraps KDS 4xx in an incompatible 200 envelope.
- Studio/MMC used an alternative matrix extraction and demonstrated the A10P3 prose did not itself provide one executable normalizer. A10P3 therefore remains `rework_required` and is not sent for freeze acceptance.

## A10P3R1 Correction

- Corrected schema raw SHA: `74b51affabf79d2ba4a908d2d9397671bdd0b07bc80814a0c36dd8d83faa7e14`.
- Canonical JSON: 34526 bytes, SHA `766ca647e894c09520bcb8ce0e70386aa233bcf727fcaf140e521f6127b1a09b`.
- Executable normalizer SHA: `d820e8103b2af74aab06381fe4034c9cec525acc8c7e1efdb074bd8a4a3aa4e4`.
- Authoritative matrix SHA: `2a80d362fe0d25d078874f919b911150122ca4f3c2faa3d9a25401f6e792a65c`.
- OpenAPI validation, Search/Graph/Wiki valid instances and six EvidenceLocator valid instances passed locally.
- The corrected candidate freezes proposed mappings only after two reports and independent F-013 review; it remains not frozen and not implemented.

## Control and Dispatch

- Control: `GKE-001-COORDINATION-20260811-009-A10P3R1`.
- Control SHA: `c8b76dcde4ffdee835fe426edbd44c33c975b6bcbd25dd60ad0dd827134f6060`.
- Studio/MMC receipt: `019ee242-2575-73f1-b5bb-d43e7e49468e`.
- KDS receipt: `019fc4e3-bce5-7541-85e3-8885c7e78aea`.
- Both repositories retain empty allowlists; Brain remains frozen after A10P1 tranche 2.

## Boundary

- No implementation, lane repository write, policy/configuration change, database/API/runtime access, live read, credential action, real E2E, commit, push, restart, deployment or status promotion is authorized.
- Rollback is withdrawal of A10P3R1 while retaining the A10P2 operation/identity decision baseline.
- Status remains `active / partial / not_complete`.
