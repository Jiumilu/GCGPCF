---
doc_id: GPCF-DOC-A4F29144C7
title: proposal
project: KDS
related_projects: [GPC, WAES, KDS, MMC, GPCF]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/gcworld-evidence-twin-foundation/proposal.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## Why

GlobalCloud KDS contains the factual materials required to represent people, organizations, projects, systems, and their changing relationships, but it does not yet provide a governed, coverage-measurable world model. A GCWORLD foundation is needed so that a future workbench and role agents can operate from evidence rather than from untraceable summaries or inferred identities.

This is a GKE-001 `release_0` planning and read-only assessment change. It does not authorize real KDS/MMC writes, external actions, deployment, or any status promotion.

## What Changes

- Define a GCWORLD system-boundary contract: KDS records evidence and facts; WAS-Ontology defines world structure; GCWORLD hosts world instances and workbench views; XWAIL plans and coordinates agents; WAES governs permissions; MMC connects capabilities; business systems execute real-world actions; LOOP/Harness records and validates results.
- Define a GCWORLD evidence-twin contract that separates evidence/candidate classifications from four world states: fact, operational, target, and simulation.
- Define the organization-asset model for people, organizations, teams, projects, systems, physical assets, functional roles, and their time-bounded relationships.
- Define a deterministic, read-only coverage assessment for KDS source references, identity resolution, provenance, unresolved mentions, and relationship evidence.
- Define a governed role-agent model: functional agents are bound to asset roles, permissions, evidence scope, action boundaries, and an auditable execution ledger; they are not replicas of real persons.
- Define the first GCWORLD workbench views and explicit non-goals for the future product implementation.

## Capabilities

### New Capabilities

- `gcworld-evidence-twin`: Evidence-linked organization-asset world model with distinct fact, operational, target, and simulation states.
- `gcworld-coverage-assessment`: Deterministic, read-only assessment of source-to-asset coverage, unresolved identities, and relationship evidence gaps.
- `gcworld-role-agent-governance`: Bounded functional-agent registration and action controls for organization assets.
- `gcworld-runtime-boundary`: System boundaries, first workbench centers, and staged progression from KDS census to controlled execution.

### Modified Capabilities

None.

## Impact

- **Program / release:** GKE-001 / `release_0` (`customer_readonly_pilot`).
- **Feature:** F-013 `knowledge-asset-model-system`; this change adds no successor feature and does not alter F-013's blocked state.
- **Repository / owner:** GPCF / GPCF; KDS is a read-only evidence source only.
- **Thread:** current GCWORLD task; canonical GKE-001 coordinator remains the thread recorded in `governance/openspec/gke001-program-binding.yaml`.
- **Baseline:** current GPCF document gate pass; runtime `F-013` remains blocked and `F-014` remains separately scoped to the meeting-to-project-control loop.
- **Allowed scope:** this OpenSpec change and a future bounded, read-only assessment artifact under F-013 after its admission constraints are met.
- **Forbidden scope:** KDS/MMC writes, KDS API use, identity or relationship write-back, business-ledger writes, credentials, permissions, deployment, external communications, and acceptance/integration/production status claims.
- **CodeGraph:** no source-code relationship changes; only a declared future domain relationship from GKE-001/KDS evidence to a GCWORLD read-only model.
- **Rollback:** delete only this uncommitted OpenSpec change; no source records or operational state are modified.
