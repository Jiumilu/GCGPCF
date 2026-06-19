---
doc_id: GPCF-DOC-3F160ABA27
title: L4 Minimum Closed Loop Object Contracts
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/minimum-closed-loop/object-contracts.md
source_path: docs/harness/minimum-closed-loop/object-contracts.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# L4 Minimum Closed Loop Object Contracts

## Core Objects

| Object | Owner | Contract Role |
|---|---|---|
| PlatformOrder | GPC | Platform order intent and customer demand anchor |
| SampleRequest | GPC / GFIS | Sample or sample-box request before production release |
| SampleWorkOrder | GFIS | Factory runtime sample work order |
| SampleApproval | GPC / WAES | Customer signoff or waiver gate |
| ProductionRelease | WAES | Controlled release decision before factory order |
| OrderMapping | GPCF | Cross-project traceability between platform and runtime records |
| FactoryOrder | GFIS | Factory runtime order after release gate |
| ProofOfDelivery | GFIS / GPC | Delivery and customer receipt evidence |
| ExternalException | WAES | Exception and escalation record |
| EvidenceRecord | WAES | Evidence metadata and review state |
| KnowledgeBacklink | KDS | Controlled knowledge backlink to source material |

## Gate Rules

- PlatformOrder cannot create FactoryOrder directly.
- FactoryOrder requires one of: approved SampleApproval, approved waiver, or approved ProductionRelease.
- SampleApproval.status in ["approved", "waived"].
- ProductionRelease.status == "approved".
- WAES.gate == "confirmed".

## Current Boundary

- These contracts define L4 control-plane rules only.
- GFIS runtime SOP E2E remains `repair_required`.
- This document does not create customer orders, platform orders, runtime primary keys, production write, real external API write, or accepted/integrated status.
