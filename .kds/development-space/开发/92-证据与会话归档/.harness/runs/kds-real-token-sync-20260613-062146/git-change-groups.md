---
doc_id: GPCF-DOC-B89D14C3C8
title: KDS Real Token Sync Git Change Groups
project: WAES
related_projects: [WAES, GPC, KDS, GPCF]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/kds-real-token-sync-20260613-062146/git-change-groups.md
source_path: .harness/runs/kds-real-token-sync-20260613-062146/git-change-groups.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# KDS Real Token Sync Git Change Groups

Purpose: define safe Git grouping for the KDS real Token implementation without staging unrelated dirty work.

## Group A: KDS API Capability

Repository: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS`

Files:

- `api_server.py`

Scope:

- Adds Token-protected document read/write/edit endpoints.
- Constrains the configured Token to `KDS_SPACE_NAME=开发`.
- Rejects forbidden scopes through runtime configuration.
- Does not add delete, admin, member management, or permission management APIs.

Suggested commit:

```text
kds: add development-space token document API
```

## Group B: KDS Development Space Data

Repository: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS`

Files:

- `concepts/开发/**`

Scope:

- Real KDS development-space Markdown documents created or updated through the Token-gated API.
- Treat as source-of-record KDS data only if the project decides the KDS repo should version the `开发` corpus.

Suggested commit, if approved:

```text
kds: sync development-space document corpus
```

## Group C: GPCF Sync Toolchain

Repository: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF`

Files:

- `tools/kds-sync/kds_runtime.py`
- `tools/kds-sync/kds_readonly_probe.py`
- `tools/kds-sync/kds_sync_plan.py`
- `tools/kds-sync/kds_sync_apply.py`
- `tools/kds-sync/validate_kds_token.py`
- `tools/kds-sync/loop_document_gate.py`

Scope:

- Loads private env file without logging secrets.
- Validates owner, space, read/write/edit scope, forbidden scopes, placeholder values, env-file permissions, and plaintext leaks.
- Provides read-only probe, dry-run plan, apply, ledger, conflict guard integration, and stable document gate behavior.

Suggested commit:

```text
gpcf: add token-gated KDS sync workflow
```

## Group D: GPCF Governance Evidence

Repository: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF`

Files:

- `.harness/runs/kds-real-token-sync-20260613-062146/**`
- `.kds/sync-ledger.jsonl`
- `.kds/sync-plan.json`
- `.kds/readonly-probe.json`
- `09-status/kds-development-space-sync-plan.md`
- `09-status/kds-readonly-probe-report.md`
- `09-status/globalcloud-document-health-report.md`
- matching `.kds/development-space/开发/**` mirror files

Scope:

- Records validation, sync ledger, rollback hints, and document-governance state.
- Does not contain Token plaintext.

Suggested commit:

```text
gpcf: record KDS token sync governance evidence
```

## Hold For Review

Do not stage automatically without review:

- Pre-existing GlobalCloud architecture/governance Markdown edits unrelated to KDS Token implementation.
- Loop LR002-LR031 generated documents unless the current release scope includes the broader L3 governance corpus.
- Any file containing external source tokens from historical Feishu or Bitable imports.
