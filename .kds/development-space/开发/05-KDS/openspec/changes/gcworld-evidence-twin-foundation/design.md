---
doc_id: GPCF-DOC-CACBA085BD
title: design
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, MMC, GPCF, Studio]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/gcworld-evidence-twin-foundation/design.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/design.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## Context

GCWORLD is a future operating workbench built from GlobalCloud's organizational and project reality. KDS is the knowledge source of truth; WAS-Ontology defines the types and semantics of the world; GCWORLD maintains derived world instances; XWAIL provides agent cognition and coordination; WAES supplies permission and risk gates; MMC supplies capability connections; GFIS/ERP/CRM and other business systems perform real-world actions; LOOP/Harness records and validates results. A world model must make identity uncertainty, relationship timing, simulation assumptions, and agent authority explicit.

This design is bound to GKE-001 `release_0` and F-013. The current authorization permits GPCF-local planning and deterministic local read-only assessment only. It does not permit real KDS/MMC writes, runtime integration, or product-repository changes. OpenSpec artifacts remain planning evidence, not a production world model.

## Goals / Non-Goals

**Goals:**

- Establish a minimal model that preserves KDS provenance while representing organization assets and time-bounded relationships.
- Make source coverage, unresolved references, and data-quality gaps measurable before any visual workbench or autonomous workflow is built.
- Make role agents explicitly bounded by evidence, permission, action mode, and human confirmation.
- Produce deterministic, reviewable artifacts that can later guide KDS, Brain, Studio, and business-system handoffs without creating a second source of truth.

**Non-Goals:**

- No KDS data import, API use, mutation, identity merge, relationship write-back, or raw-record reclassification.
- No live CRM replacement, external communication, business decision, deployment, customer pilot, or status promotion.
- No 3D visualization, simulated prediction engine, LLM extraction claim, or assertion that all KDS people and organizations have been resolved.

## Decisions

### 1. KDS remains the source of truth; GCWORLD is an evidence-linked projection

A world asset holds stable identifiers, type, lifecycle state, and evidence references, but it does not duplicate or replace the source record. A source mention can remain unresolved and cannot become a canonical identity merely because a model proposes a match.

Alternative considered: materialize all KDS content into a new world database first. Rejected because it would create a competing primary ledger before data-quality and authorization gates exist.

### 2. Use four explicitly disjoint world states; keep evidence classification separate

Every world-state record is exactly one of `fact`, `operational`, `target`, or `simulation`. Evidence layer and candidate status are separate classifications: a KDS source may support a fact, a candidate may await review, and a source link never turns a target or simulation into a fact. Operational records represent current collaboration or task state; targets represent plans, budgets, and expected outcomes; simulations represent versioned hypotheses.

Alternative considered: a single `status` field on every node. Rejected because it allows plans, inferred data, or simulations to be displayed as facts.

### 3. Model people and organizations as assets; model functions as roles, not duplicate persons

One asset can hold multiple roles across organizations and time ranges. A functional agent attaches to an approved role and can never claim to be the natural person. This supports employees, customers, partners, government contacts, teams, platforms, and physical assets without forcing an inaccurate one-to-one agent model.

Alternative considered: one agent per human. Rejected because the requested unit of execution is function and authority, while people can hold multiple changing functions.

### 4. Make coverage a deterministic read-only gate before product presentation

The initial assessment consumes an explicit local file manifest and produces an asset/reference ledger, unresolved-reference queue, source-to-asset coverage metrics, relationship-evidence metrics, and exclusions. It must preserve source paths and hashes, and it must not change a KDS file.

Alternative considered: start with graph visualization and clean data later. Rejected because omissions and false identity merges would be visually persuasive but operationally unsafe.

### 5. Use four agent operating modes and require an action envelope beyond observation

An agent registration carries agent ID, role binding, source scope, operating mode, owner, risk level, evidence requirement, and confirmation requirement. The modes are `mirror`, `assist`, `delegated`, and `autonomous`; autonomous operation remains limited to approved scenarios. Any external, financial, contractual, identity-changing, government-facing, permission-changing, or business-state action remains blocked until separately authorized and confirmed.

Alternative considered: reuse a generic chat-agent permission switch. Rejected because it cannot show which organizational role is acting on which evidence and with what real-world boundary.

## Risks / Trade-offs

- [Unresolved aliases and low-quality transcripts] → retain candidate nodes and evidence links; never auto-merge or elevate them.
- [Large and changing KDS corpus] → use a versioned manifest, deterministic ordering, hashes, and incremental comparison rather than an unbounded ad hoc scan.
- [Sensitive personal and commercial material] → begin with metadata, pseudonymous identifiers where required, least-privilege source scopes, and no public-facing projection.
- [Agent overreach] → enforce action envelopes, mandatory confirmation, immutable execution ledger, and a deny-by-default external-action policy.
- [Second system of record] → retain only references and derived assessment outputs; KDS remains authoritative for knowledge facts.

## Migration Plan

1. Create and review the GCWORLD contract and read-only assessment specification in GPCF.
2. After F-013 admission constraints are cleared, run the bounded local assessment against an approved KDS manifest and store results as evidence only.
3. Obtain separate authorization before any KDS-side schema, UI, integration, or write-back work.
4. Roll back the first phase by removing only its uncommitted GPCF artifacts; no KDS or business data is altered.

## Open Questions

- Who is the designated human owner for canonical identity merges and relationship disputes?
- Which KDS spaces and retention classes are permitted in the first read-only manifest?
- What minimum data should be redacted before a future shared or customer-facing workbench?
- Which system will become the authorized operational ledger after the read-only pilot proves coverage?
