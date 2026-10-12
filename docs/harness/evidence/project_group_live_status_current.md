---
doc_id: GPCF-DOC-PROJECTGROUPLIVESTATUSCURRENT20260701
title: GlobalCloud 项目群当前 Live 状态快照
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: harness
type: project_group_live_status_current
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/project_group_live_status_current.md
source_path: docs/harness/evidence/project_group_live_status_current.md
sync_direction: bidirectional
last_reviewed: 2026-07-01
supersedes: []
superseded_by: []
data_layer: derived
authority_level: A2
verification_status: source_verified
generated_at: 2026-10-12 16:16:33 +0800
---

# GlobalCloud 项目群当前 Live 状态快照

## Summary

- generated_at: `2026-10-12T16:16:33.618090+08:00`
- freshness_ok: `true`
- project_count: `18`
- pass_repo_count: `12`
- bootstrap_window: `false`

## Current sets

- observed_dirty: `GlobalCloud WAES, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud KDS, GlobalCloud XGD`
- observed_ahead: `GlobalCloud Studio, GlobalCloud KDS`
- stable_dirty: `GlobalCloud KDS, GlobalCloud WAES, GlobalCloud XGD, GlobalCloud XWAIL, GlobalCoud GPCF`
- stable_ahead: `GlobalCloud KDS, GlobalCloud Studio`
- volatile_dirty: `GlobalCoud GPCF`
- sensitive_repos: `GlobalCoud GPCF`
- review_boundary: `GlobalCloud KDS, GlobalCloud WAES, GlobalCloud XGD, GlobalCloud XWAIL, GlobalCoud GPCF`

## Repo details

| Repo | dirty_count | ahead | behind | sensitive_paths |
|---|---:|---:|---:|---|
| `GlobalCloud AAAS` | 0 | 0 | 0 | `none` |
| `GlobalCloud Brain` | 0 | 0 | 0 | `none` |
| `WAS世界资产体系` | 0 | 0 | 0 | `none` |
| `GlobalCloud XiaoC` | 0 | 0 | 0 | `none` |
| `GlobalCloud WAES` | 13 | 0 | 0 | `none` |
| `GlobalCloud GPC` | 0 | 0 | 0 | `none` |
| `GlobalCloud Studio` | 0 | 21 | 0 | `none` |
| `GlobalCloud WAE` | 0 | 0 | 0 | `none` |
| `GlobalCoud GPCF` | 3558 | 0 | 0 | `".kds/development-space/\345\274\200\345\217\221/05-KDS/docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-a11y-verified-20260624.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-account-action-whitelist-verified-20260625.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-backend-enforcement-20260623.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-backend-runtime-verified-20260624.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-completion-gate-verified-20260625.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-login-redirect-verified-20260622.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-mobile-runtime-verified-20260623.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-post-change-closure-verified-20260622.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-prompt-mobile-compact-verified-20260622.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-prompt-nonblocking-verified-20260622.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-remediation-whitelist-verified-20260625.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-runtime-chain-verified-20260623.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/evidence/studio-default-credential-zero-noise-remediation-20260624.md", ".kds/development-space/\345\274\200\345\217\221/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-001.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/README.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/acceptance-matrix.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/evidence/README.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/patches/README.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/workspaces/README.md", .harness/runs/kds-real-token-sync-20260613-062146/README.md, .harness/runs/kds-real-token-sync-20260613-062146/evidence/README.md, .harness/runs/kds-real-token-sync-20260613-062146/patches/README.md, .harness/runs/kds-real-token-sync-20260613-062146/workspaces/README.md` |
| `GlobalCloud XWAIL` | 1 | 0 | 0 | `none` |
| `GlobalCloud GFIS` | 0 | 0 | 0 | `none` |
| `GlobalCloud MMC` | 0 | 0 | 0 | `none` |
| `GlobalCloud KDS` | 3 | 1 | 0 | `none` |
| `GlobalCloud XiaoG` | 0 | 0 | 0 | `none` |
| `GlobalCloud PVAOS` | 0 | 0 | 0 | `none` |
| `GlobalCloud SOP` | 0 | 0 | 0 | `none` |
| `GlobalCloud PKC` | 0 | 0 | 0 | `none` |
| `GlobalCloud XGD` | 1 | 0 | 0 | `none` |
