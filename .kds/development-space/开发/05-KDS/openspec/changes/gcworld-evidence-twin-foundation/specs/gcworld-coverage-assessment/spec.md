---
doc_id: GPCF-DOC-8F0920DB54
title: spec
project: KDS
related_projects: [KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-coverage-assessment/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-coverage-assessment/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: Read-only source manifest assessment
The system SHALL accept an explicitly approved local KDS source manifest and SHALL assess it without modifying source files, KDS metadata, KDS APIs, or business systems. The assessment SHALL record the manifest version, deterministic file order, source path, and source hash for every examined record.

#### Scenario: Assessment is run against an approved manifest
- **WHEN** an operator runs the coverage assessment with an approved local manifest
- **THEN** the assessment produces only derived local evidence artifacts and reports zero source-file modifications

### Requirement: Coverage and exception reporting
The system SHALL produce a reviewable report containing source-record count, extracted asset-reference count, resolved-reference count, unresolved-reference count, duplicate-candidate count, relationship-evidence count, exclusions, and data-quality exceptions. Each exception MUST link to its source evidence or declared exclusion reason.

#### Scenario: A referenced organization lacks a resolved asset
- **WHEN** the assessment finds an organization mention with no verified canonical asset link
- **THEN** the report lists it as an unresolved reference with source location and does not claim complete organizational coverage

### Requirement: No-completeness claim without explicit closure
The system MUST NOT state that all people or organizations are covered unless every manifest record is either linked to a verified asset or listed in an explicit exception/exclusion disposition and the resulting closure report is human-approved.

#### Scenario: Outstanding unresolved references remain
- **WHEN** the assessment report contains unresolved or unreviewed identity references
- **THEN** the report status is partial and any completeness statement is withheld
