---
doc_id: GPCF-DOC-A861AD5583
title: spec
project: KDS
related_projects: [KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-evidence-twin/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-evidence-twin/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: Evidence-linked organization assets
The system SHALL represent a GCWORLD asset as one of person, organization, team, project, system, physical asset, document, role, or relationship endpoint. Every asset record SHALL include a stable world identifier, asset type, lifecycle state, provenance references, evidence status, and valid-time range where known. The system MUST preserve aliases and uncertainty without automatically merging identities.

#### Scenario: Ambiguous person mention is discovered
- **WHEN** a source record contains a person name that maps to more than one possible identity
- **THEN** the system records a candidate reference with its source evidence and marks the identity as unresolved rather than linking it to a canonical person asset

### Requirement: Four separated world states
The system SHALL label every world-state record as exactly one of `fact`, `operational`, `target`, or `simulation`. Evidence-layer and candidate classifications MUST be stored separately from world state. Target and simulation records MUST NOT be presented as factual observations or written into KDS canonical facts without a separately authorized review process.

#### Scenario: Simulation produces a project-delay outcome
- **WHEN** a scenario model calculates a possible delay based on stated assumptions
- **THEN** the output is stored as `simulation` with its input version and assumptions and is not displayed as an actual project status

#### Scenario: A project plan is recorded
- **WHEN** a project plan states an expected production capacity or revenue outcome
- **THEN** the system records it as `target` with its source and planning period and does not treat it as an achieved fact

### Requirement: Evidence-linked temporal relationships
The system SHALL represent each relationship with a subject asset, predicate, object asset, evidence references, evidence status, and known valid-time range. The system MUST allow multiple relationships between the same assets when their predicates or valid-time ranges differ.

#### Scenario: A person changes organizational role
- **WHEN** evidence shows a person holds a new role after a recorded date
- **THEN** the system retains the prior role relationship with its valid-time range and creates or proposes a separate time-bounded relationship for the new role
