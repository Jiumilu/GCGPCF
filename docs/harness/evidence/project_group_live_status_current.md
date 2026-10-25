---
doc_id: GPCF-DOC-PROJECTGROUPLIVESTATUSCURRENT20260701
title: GlobalCloud 项目群当前 Live 状态快照
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP, PQC, SpaceAI, SpaceAIStudio, World, GCMEM, WAE, Project, PDC, SLC, DRC, FireQuote, GCToken]
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
generated_at: 2026-10-26 00:06:42 +0800
---

# GlobalCloud 项目群当前 Live 状态快照

## Summary

- generated_at: `2026-10-26T00:06:42.558881+08:00`
- freshness_ok: `true`
- project_count: `29`
- pass_repo_count: `5`
- bootstrap_window: `false`

## Current sets

- observed_dirty: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud XiaoC, GlobalCloud WAME, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud MMC, GlobalCloud KDS, GlobalCloud XiaoG, GlobalCloud PVA, GlobalCloud PQC, GlobalCloud SpaceAI Platform, GlobalCloud World, GlobalCloud Mem, GlobalCloud WAE, GlobalCloud PMC, GlobalCloud PDC, GlobalCloud FireQuote`
- observed_ahead: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud XiaoC, GlobalCloud WAME, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud MMC, GlobalCloud XiaoG, GlobalCloud PVA, GlobalCloud SOP, GlobalCloud PKC, GlobalCloud SpaceAI Platform, GlobalCloud WAE, GlobalCloud PMC, GlobalCloud SLC, GlobalCloud Token`
- stable_dirty: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud FireQuote, GlobalCloud GFIS, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud KDS, GlobalCloud MMC, GlobalCloud Mem, GlobalCloud PDC, GlobalCloud PMC, GlobalCloud PQC, GlobalCloud PVA, GlobalCloud SpaceAI Platform, GlobalCloud WAE, GlobalCloud WAME, GlobalCloud World, GlobalCloud XWAIL, GlobalCloud XiaoC, GlobalCloud XiaoG`
- stable_ahead: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud MMC, GlobalCloud PKC, GlobalCloud PMC, GlobalCloud PVA, GlobalCloud SLC, GlobalCloud SOP, GlobalCloud SpaceAI Platform, GlobalCloud Token, GlobalCloud WAE, GlobalCloud WAME, GlobalCloud XiaoC, GlobalCloud XiaoG`
- volatile_dirty: `GlobalCloud GPCF`
- sensitive_repos: `GlobalCloud XiaoC, GlobalCloud GPCF, GlobalCloud WAE`
- review_boundary: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud FireQuote, GlobalCloud GFIS, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud KDS, GlobalCloud MMC, GlobalCloud Mem, GlobalCloud PDC, GlobalCloud PMC, GlobalCloud PQC, GlobalCloud PVA, GlobalCloud SpaceAI Platform, GlobalCloud WAE, GlobalCloud WAME, GlobalCloud World, GlobalCloud XWAIL, GlobalCloud XiaoC, GlobalCloud XiaoG`

## Repo details

| Repo | dirty_count | ahead | behind | sensitive_paths |
|---|---:|---:|---:|---|
| `GlobalCloud AAAS` | 24 | 2 | 0 | `none` |
| `GlobalCloud Brain` | 1 | 3 | 0 | `none` |
| `GlobalCloud WAS` | 0 | 0 | 0 | `none` |
| `GlobalCloud XiaoC` | 209 | 7 | 0 | `.env.bak-20261020-hermes-key, .harness/evidence/xiaoc-feishu-20261022/10-credentials.md, .harness/evidence/xiaoc-feishu-20261022/74-verification-token-wired.md, .harness/evidence/xiaoc-mcp-skill-20261020/23-real-smoke-hermes-credential.md, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-audit.jsonl, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-auth.md, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-health.json, packages/feishu-bridge/.env.example` |
| `GlobalCloud WAME` | 6 | 1 | 26 | `none` |
| `GlobalCloud GPC` | 1 | 8 | 0 | `none` |
| `GlobalCloud GPCF` | 439 | 58 | 0 | `.harness/runs/kds-real-token-sync-20260613-062146/README.md, .harness/runs/kds-real-token-sync-20260613-062146/evidence/README.md, .harness/runs/kds-real-token-sync-20260613-062146/patches/README.md, .harness/runs/kds-real-token-sync-20260613-062146/workspaces/README.md` |
| `GlobalCloud XWAIL` | 1 | 0 | 20 | `none` |
| `GlobalCloud GFIS` | 52 | 0 | 0 | `none` |
| `GlobalCloud MMC` | 2 | 7 | 9 | `none` |
| `GlobalCloud KDS` | 39 | 0 | 0 | `none` |
| `GlobalCloud XiaoG` | 1 | 1082 | 16 | `none` |
| `GlobalCloud PVA` | 19 | 8 | 0 | `none` |
| `GlobalCloud SOP` | 0 | 1 | 0 | `none` |
| `GlobalCloud PKC` | 0 | 6 | 0 | `none` |
| `GlobalCloud XGD` | 0 | 0 | 0 | `none` |
| `GlobalCloud ICP` | 0 | 0 | 0 | `none` |
| `GlobalCloud PQC` | 29 | 0 | 0 | `none` |
| `GlobalCloud SpaceAI Platform` | 38 | 3 | 0 | `none` |
| `GlobalCloud SpaceAI Studio` | 0 | 0 | 0 | `none` |
| `GlobalCloud World` | 1 | 0 | 0 | `none` |
| `GlobalCloud Mem` | 2 | 0 | 0 | `none` |
| `GlobalCloud WAE` | 258 | 30 | 67 | `apps/wame/.env.example, docs/evidence/R1/supply-chain/secret-scan.json` |
| `GlobalCloud PMC` | 3 | 3 | 0 | `none` |
| `GlobalCloud PDC` | 1 | 0 | 0 | `none` |
| `GlobalCloud SLC` | 0 | 7 | 0 | `none` |
| `GlobalCloud DRC` | 0 | 0 | 0 | `none` |
| `GlobalCloud FireQuote` | 38 | 0 | 0 | `none` |
| `GlobalCloud Token` | 0 | 2 | 0 | `none` |
