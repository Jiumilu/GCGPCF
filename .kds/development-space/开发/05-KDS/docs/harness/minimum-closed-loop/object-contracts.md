---
doc_id: GPCF-DOC-3F160ABA27
title: L4 Minimum Closed Loop Object Contracts
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XGD, XiaoG, MMC, GPCF]
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

## Contract Rules

- PlatformOrder cannot create FactoryOrder directly.
- FactoryOrder requires one of: approved SampleApproval, approved waiver, or approved ProductionRelease.
- GPC owns customer-facing sample approval and production release.
- GFIS owns formula R&D, sample work order, sample inspection and factory execution facts.
- WAES confirms evidence gates and blocks unauthorized transition.

## Core Object Contracts

| Object | Producer | Consumers | Input | Output | Forbidden actions | Verification |
|---|---|---|---|---|---|---|
| ProjectInitialization | PVAOS | GPC, WAES, GPCF | tenant, organization, partner, project template | project space, permission boundary | creating production facts | L4-006 dry-run |
| PlatformOrder | GPC | WAES, GFIS, PKC, Brain | customer order, partner, product intent | order state, sample request candidate | direct FactoryOrder creation | L4-007 contract validator |
| QuoteReviewContract | GPC | WAES, PKC | platform order, pricing, delivery constraint | reviewed quote, contract status | bypassing sample gate for sample-required products | L4-007 contract validator |
| SampleRequest | GPC | GFIS, WAES, KDS, Brain, PKC | PlatformOrder, sample spec, customer requirement | sample request, evidence refs | starting production order | L4-007 and L4-008 dry-run |
| SampleWorkOrder | GFIS | GPC, WAES, KDS, XiaoG | SampleRequest, formula requirement, test rule | formula draft, sample batch, inspection result | claiming customer approval | L4-008 readonly sample |
| SampleApproval | GPC | WAES, GFIS, KDS, PKC | sample result, customer signoff, waiver flag | approved/rejected/waived decision | silent approval without evidence | L4-009 evidence gate |
| ProductionRelease | GPC / WAES | GFIS, MMC, GPCF | approved SampleApproval or waiver, WAES evidence gate | production release decision | releasing without signed sample, waiver, or WAES gate | L4-009 evidence gate |
| OrderMapping | GPC / GFIS | WAES, GPCF | ProductionRelease, PlatformOrder, GFIS factory capacity | platform-to-factory mapping | mapping unsigned PlatformOrder to FactoryOrder | L4-007/L4-008 dry-run |
| FactoryOrder | GFIS | WAES, GPC, XiaoG | ProductionRelease, OrderMapping | factory order state | accepting unsigned or unreleased order | L4-008 readonly sample |
| WorkOrder | GFIS | WAES, Brain, PKC, XiaoG | FactoryOrder, BOM, resource plan | work order state, operator, timing | changing release gate | L4-008 readonly sample |
| QualityInventoryBatch | GFIS | WAES, Brain, KDS | WorkOrder, inspection rule, batch movement | quality status, inventory state, batch trace | hiding rejected inspection | L4-008 readonly sample |
| Shipment | GFIS | GPC, WAES | completed order, outbound plan | shipment and outbound evidence | shipping unreleased or blocked goods | L4-008/L4-007 dry-run |
| ProofOfDelivery | GPC | WAES, PKC, Brain | shipment, carrier, receiver evidence | POD/signoff state | marking delivered without evidence | L4-007 UI/contract smoke |
| ExternalException | GPC / GFIS / WAES | Brain, PKC, XGD, GPCF | exception event, source record, evidence refs | exception state, owner, closure path | closing without WAES evidence | L4-009 and L4-011 dry-run |
| EvidenceRecord | WAES | GPCF, KDS, Brain, PKC | source event, trace id, evidence refs | evidence chain, gate decision | editing business facts | L4-009 evidence validator |
| KnowledgeBacklink | KDS | Brain, GPCF, PKC | SOP, sample spec, signoff material, evidence refs | knowledge entry and backlink | storing raw token or uncontrolled secret | L4-003 KDS safety check |

## Blocking Rule

FactoryOrder creation is blocked unless:

```text
SampleApproval.status in ["approved", "waived"]
AND ProductionRelease.status == "approved"
AND WAES.gate == "confirmed"
```

Allowed validation levels:

- real read-only API
- local fixture dry-run
- mock transport
- static contract validator

Forbidden validation shortcuts:

- claiming accepted or integrated
- production write
- real external API write
- permission change
- deployment
- token disclosure
