---
doc_id: GPCF-DOC-C93F8F0441
title: "Acceptance Matrix: KDS Real Token Sync"
project: WAES
related_projects: [WAES, KDS]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/kds-real-token-sync-20260613-062146/acceptance-matrix.md
source_path: .harness/runs/kds-real-token-sync-20260613-062146/acceptance-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Acceptance Matrix: KDS Real Token Sync

| Requirement | Implementation | Evidence | Status |
|---|---|---|---|
| Token must require owner, space, and read/write/edit scope | `tools/kds-sync/validate_kds_token.py` | `evidence/validation-results.txt` | [x] |
| Token must reject delete/admin/member/permission scopes | `tools/kds-sync/validate_kds_token.py` | `evidence/validation-results.txt` | [x] |
| Token must not be printed to logs or evidence | `tools/kds-sync/kds_runtime.py` redaction | `evidence/validation-results.txt` | [x] |
| Read-only KDS probe must not write remote data | `tools/kds-sync/kds_readonly_probe.py` | `evidence/validation-results.txt` | [x] |
| Dry-run plan must exist before apply | `tools/kds-sync/kds_sync_plan.py` | `.kds/sync-plan.json` | [x] |
| Real apply must require explicit confirmation | `tools/kds-sync/kds_sync_apply.py` | `evidence/validation-results.txt` | [x] |
| Apply must run Token, pollution, conflict, and clean-plan gates | `tools/kds-sync/kds_sync_apply.py` | `evidence/validation-results.txt` | [x] |
| Real KDS API execution completed | External KDS API call | Missing real Token and API base URL | [ ] |
