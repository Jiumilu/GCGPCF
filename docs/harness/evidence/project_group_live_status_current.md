---
doc_id: GPCF-DOC-PROJECTGROUPLIVESTATUSCURRENT20260701
title: GlobalCloud 项目群当前 Live 状态快照
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP, PQC, SpaceAI, SpaceAIStudio, World, GCMEM, WAE, Project, PDC, SLC, DRC, FireQuote]
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
generated_at: 2026-10-23 00:21:26 +0800
---

# GlobalCloud 项目群当前 Live 状态快照

## Summary

- generated_at: `2026-10-23T00:21:26.508156+08:00`
- freshness_ok: `true`
- project_count: `29`
- pass_repo_count: `3`
- bootstrap_window: `false`

## Current sets

- observed_dirty: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud WAS, GlobalCloud XiaoC, GlobalCloud WAME, GlobalCloud GPC, GlobalCloud Studio, GlobalCloud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud MMC, GlobalCloud KDS, GlobalCloud XiaoG, GlobalCloud PVA, GlobalCloud SOP, GlobalCloud PKC, GlobalCloud XGD, GlobalCloud ICP, GlobalCloud PQC, GlobalCloud SpaceAI Platform, GlobalCloud World, GlobalCloud WAE, GlobalCloud PMC, GlobalCloud PDC, GlobalCloud FireQuote`
- observed_ahead: `GlobalCloud Brain, GlobalCloud XiaoC, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud MMC, GlobalCloud XiaoG, GlobalCloud PKC, GlobalCloud SpaceAI Platform, GlobalCloud WAE, GlobalCloud PMC, GlobalCloud SLC`
- stable_dirty: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud FireQuote, GlobalCloud GFIS, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud ICP, GlobalCloud KDS, GlobalCloud MMC, GlobalCloud PDC, GlobalCloud PKC, GlobalCloud PMC, GlobalCloud PQC, GlobalCloud PVA, GlobalCloud SOP, GlobalCloud SpaceAI Platform, GlobalCloud Studio, GlobalCloud WAE, GlobalCloud WAME, GlobalCloud WAS, GlobalCloud World, GlobalCloud XGD, GlobalCloud XWAIL, GlobalCloud XiaoC, GlobalCloud XiaoG`
- stable_ahead: `GlobalCloud Brain, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud MMC, GlobalCloud PKC, GlobalCloud PMC, GlobalCloud SLC, GlobalCloud SpaceAI Platform, GlobalCloud WAE, GlobalCloud XiaoC, GlobalCloud XiaoG`
- volatile_dirty: `GlobalCloud GPCF`
- sensitive_repos: `GlobalCloud XiaoC, GlobalCloud GPCF, GlobalCloud PKC`
- review_boundary: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud FireQuote, GlobalCloud GFIS, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud ICP, GlobalCloud KDS, GlobalCloud MMC, GlobalCloud PDC, GlobalCloud PKC, GlobalCloud PMC, GlobalCloud PQC, GlobalCloud PVA, GlobalCloud SOP, GlobalCloud SpaceAI Platform, GlobalCloud Studio, GlobalCloud WAE, GlobalCloud WAME, GlobalCloud WAS, GlobalCloud World, GlobalCloud XGD, GlobalCloud XWAIL, GlobalCloud XiaoC, GlobalCloud XiaoG`

## Repo details

| Repo | dirty_count | ahead | behind | sensitive_paths |
|---|---:|---:|---:|---|
| `GlobalCloud AAAS` | 17 | 0 | 0 | `none` |
| `GlobalCloud Brain` | 1 | 2 | 0 | `none` |
| `GlobalCloud WAS` | 2 | 0 | 0 | `none` |
| `GlobalCloud XiaoC` | 209 | 5 | 0 | `.env.bak-20261020-hermes-key, .harness/evidence/xiaoc-feishu-20261022/10-credentials.md, .harness/evidence/xiaoc-feishu-20261022/74-verification-token-wired.md, .harness/evidence/xiaoc-mcp-skill-20261020/23-real-smoke-hermes-credential.md, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-audit.jsonl, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-auth.md, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-health.json, packages/feishu-bridge/.env.example` |
| `GlobalCloud WAME` | 6 | 0 | 0 | `none` |
| `GlobalCloud GPC` | 1 | 5 | 0 | `none` |
| `GlobalCloud Studio` | 1 | 0 | 0 | `none` |
| `GlobalCloud GPCF` | 934 | 7 | 0 | `".kds/development-space/\345\274\200\345\217\221/91-\346\262\273\347\220\206\344\270\216\351\252\214\346\224\266/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/o2-token-consolidation.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/README.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/evidence/README.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/patches/README.md", ".kds/development-space/\345\274\200\345\217\221/92-\350\257\201\346\215\256\344\270\216\344\274\232\350\257\235\345\275\222\346\241\243/.harness/runs/kds-real-token-sync-20260613-062146/workspaces/README.md", .harness/runs/kds-real-token-sync-20260613-062146/README.md, .harness/runs/kds-real-token-sync-20260613-062146/evidence/README.md, .harness/runs/kds-real-token-sync-20260613-062146/patches/README.md, .harness/runs/kds-real-token-sync-20260613-062146/workspaces/README.md` |
| `GlobalCloud XWAIL` | 1 | 0 | 0 | `none` |
| `GlobalCloud GFIS` | 1 | 0 | 0 | `none` |
| `GlobalCloud MMC` | 1 | 13 | 7 | `none` |
| `GlobalCloud KDS` | 4 | 0 | 0 | `none` |
| `GlobalCloud XiaoG` | 1 | 1079 | 16 | `none` |
| `GlobalCloud PVA` | 41 | 0 | 0 | `none` |
| `GlobalCloud SOP` | 21 | 0 | 0 | `none` |
| `GlobalCloud PKC` | 17 | 3 | 0 | `src/styles/gc-tokens.css` |
| `GlobalCloud XGD` | 19 | 0 | 0 | `none` |
| `GlobalCloud ICP` | 1 | 0 | 0 | `none` |
| `GlobalCloud PQC` | 8 | 0 | 0 | `none` |
| `GlobalCloud SpaceAI Platform` | 2297 | 3 | 0 | `none` |
| `GlobalCloud SpaceAI Studio` | 0 | 0 | 0 | `none` |
| `GlobalCloud World` | 1 | 0 | 0 | `none` |
| `GlobalCloud Mem` | 0 | 0 | 0 | `none` |
| `GlobalCloud WAE` | 3 | 6 | 0 | `none` |
| `GlobalCloud PMC` | 3 | 4 | 0 | `none` |
| `GlobalCloud PDC` | 2 | 0 | 0 | `none` |
| `GlobalCloud SLC` | 0 | 5 | 0 | `none` |
| `GlobalCloud DRC` | 0 | 0 | 0 | `none` |
| `GlobalCloud FireQuote` | 38 | 0 | 0 | `none` |
