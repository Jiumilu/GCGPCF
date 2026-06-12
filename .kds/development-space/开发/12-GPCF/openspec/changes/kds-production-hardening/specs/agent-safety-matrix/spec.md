---
doc_id: GPCF-DOC-8ECD9BA263
title: Agent Safety Matrix
project: GPCF
related_projects: [GPCF]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/kds-production-hardening/specs/agent-safety-matrix/spec.md
source_path: openspec/changes/kds-production-hardening/specs/agent-safety-matrix/spec.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Agent Safety Matrix

## Overview
Four-layer defense for AI agent code modifications: workspace isolation, patch allowlist, static risk scan, human review.

## Requirements
- Agent tasks run in isolated workspace directories
- File type restrictions: .md, .yaml, .json, .html, .css, .js only
- Path restrictions: server/core/auth.py, server/core/db.py, migrations/, scripts/deploy, scripts/backup, .env blocked
- Static scan detects: SQL DROP/DELETE/TRUNCATE, os.system, subprocess, eval, exec, rm -rf
- Risk levels: low (auto-accept), medium (human review + rollback plan), high (mandatory security review), critical (blocked)
- Every patch requires rollback plan for risk >= medium
- 6-state task machine: not_started -> in_progress -> blocked -> ready_for_human_acceptance -> accepted -> applied -> closed

## Acceptance
- [ ] Agent cannot modify auth.py, db.py, or migration files
- [ ] Dangerous SQL/shell patterns detected and flagged
- [ ] High-risk patches require human review
- [ ] Patches without rollback plan rejected at accept step
