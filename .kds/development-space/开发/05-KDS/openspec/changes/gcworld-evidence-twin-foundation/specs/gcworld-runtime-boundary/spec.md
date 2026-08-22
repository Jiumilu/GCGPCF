---
doc_id: GPCF-DOC-E9F567EAFF
title: spec
project: KDS
related_projects: [WAES, KDS, MMC]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-runtime-boundary/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-runtime-boundary/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: GCWORLD system boundaries
The system SHALL preserve distinct responsibilities: KDS for evidence and facts; WAS-Ontology for world semantics; GCWORLD for derived world instances and workbench views; XWAIL for agent cognition and coordination; WAES for rules, permissions, and gates; MMC for capability connections; business systems for real-world execution; and LOOP/Harness for result evidence and validation. GCWORLD MUST NOT bypass a responsible system's authorization boundary.

#### Scenario: An agent proposes a contract action
- **WHEN** an agent proposes a contract-related action in GCWORLD
- **THEN** GCWORLD records the proposal and required authorization but does not execute or write the action into a business system without the responsible system's gate

### Requirement: First-stage read-only workbench centers
The system SHALL define first-stage read-only views for world overview, organization assets, relationship network, project world, time and events, agent registry, action and collaboration, simulation laboratory, and governance and audit. Each view MUST expose evidence status and world-state type for displayed derived records.

#### Scenario: A user opens a relationship network view
- **WHEN** a user opens a relationship between two organization assets
- **THEN** the view displays relation type, direction, valid-time range, evidence references, confidence, conflict status, visibility scope, and allowed agent-use scope

### Requirement: Staged controlled progression
The system SHALL sequence delivery as KDS census, world-kernel contract, read-only workbench, internal assist-mode agents, project simulation, and separately authorized real-world execution. Completion of an earlier stage MUST NOT authorize the next stage automatically.

#### Scenario: Census assessment completes with exceptions
- **WHEN** a census assessment completes while unresolved references remain
- **THEN** the result is eligible for review as a partial assessment and does not authorize a write-enabled workbench or agent execution
