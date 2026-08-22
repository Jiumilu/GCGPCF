---
doc_id: GPCF-DOC-7608F9E00C
title: spec
project: GPCF
related_projects: [GPCF]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-role-agent-governance/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-role-agent-governance/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: Functional role-agent registration
The system SHALL register each GCWORLD agent with an agent ID, bound organization-asset role, owner, source scope, one operating mode of `mirror`, `assist`, `delegated`, or `autonomous`, allowed actions, forbidden actions, risk level, evidence requirements, and confirmation requirements. A role agent MUST NOT represent itself as the real person associated with its role.

#### Scenario: A project-coordination role agent is created
- **WHEN** an operator proposes an agent for a project-coordination role
- **THEN** the registration identifies the project role, human owner, permitted evidence scope, and prohibited external actions before the agent can operate

#### Scenario: A mirror-mode agent is queried
- **WHEN** a user queries an agent registered in `mirror` mode
- **THEN** the agent returns only evidence-linked profile and relationship information and cannot create tasks, messages, or business actions

### Requirement: Action envelopes and confirmation boundaries
The system SHALL require an action envelope for every agent action beyond read-only observation. The envelope MUST record agent ID, actor role, target, intended action, evidence references, risk, authorization state, confirmation state, and result. Actions affecting external communication, money, contracts, permissions, identity, government communication, or business state MUST remain blocked without separate authorization and human confirmation.

#### Scenario: An agent drafts an external partner message
- **WHEN** an agent prepares a message for a partner
- **THEN** it may save a draft with evidence references but cannot send the message until the required authorization and human confirmation are recorded

### Requirement: Auditable agent execution ledger
The system SHALL retain an append-only execution ledger for permitted agent actions and outcomes, including no-op and blocked actions. The ledger MUST distinguish recommendation, draft, approved execution, rejected execution, and failed execution.

#### Scenario: A prohibited action is requested
- **WHEN** an agent receives a request outside its registered action modes
- **THEN** the system records a blocked execution entry with the prohibition reason and performs no external side effect
