---
doc_id: GPCF-DOC-68559C2B7E
title: GFIS Residual Drift Evidence
project: KDS
related_projects: [GFIS, GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-dev-execution-gfis-residual-drift-20260622.md
source_path: docs/harness/evidence/codegraph-dev-execution-gfis-residual-drift-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Residual Drift Evidence

本轮对应 `GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007`，只复核残余漂移，不做清理。

## 结论

- `pendingChanges.added=1`
- `codegraph_sync_only_closure=false`
- `.codegraph/` 保持 Git 隔离
- `untracked_files_total=226`
- `untracked_codegraph_scannable_files=73`
- `FAIL: KDS coverage must not have missing controlled sources`

## 约束

- 不删除 GFIS untracked files
- 不 stage GFIS files
- 不 commit GFIS changes
- 不 push GFIS changes
- 不 deploy GFIS

## 下一轮

`GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008`
