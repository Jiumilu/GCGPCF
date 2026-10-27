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
generated_at: 2026-10-27 21:24:10 +0800
---

# GlobalCloud 项目群当前 Live 状态快照

## Summary

- generated_at: `2026-10-27T21:24:10.137316+08:00`
- freshness_ok: `true`
- project_count: `29`
- pass_repo_count: `4`
- bootstrap_window: `false`

## Current sets

- observed_dirty: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud XiaoC, GlobalCloud WAME, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud MMC, GlobalCloud KDS, GlobalCloud XiaoG, GlobalCloud PVA, GlobalCloud PQC, GlobalCloud SpaceAI Platform, GlobalCloud World, GlobalCloud Mem, GlobalCloud WAE, GlobalCloud PMC, GlobalCloud PDC, GlobalCloud FireQuote`
- observed_ahead: `GlobalCloud Brain, GlobalCloud WAS, GlobalCloud XiaoC, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud MMC, GlobalCloud XiaoG, GlobalCloud SOP, GlobalCloud PKC, GlobalCloud ICP, GlobalCloud PQC, GlobalCloud SpaceAI Platform, GlobalCloud Mem, GlobalCloud WAE, GlobalCloud PMC, GlobalCloud PDC, GlobalCloud Token`
- stable_dirty: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud FireQuote, GlobalCloud GFIS, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud KDS, GlobalCloud MMC, GlobalCloud Mem, GlobalCloud PDC, GlobalCloud PMC, GlobalCloud PQC, GlobalCloud PVA, GlobalCloud SpaceAI Platform, GlobalCloud WAE, GlobalCloud WAME, GlobalCloud World, GlobalCloud XWAIL, GlobalCloud XiaoC, GlobalCloud XiaoG`
- stable_ahead: `GlobalCloud Brain, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud MMC, GlobalCloud Mem, GlobalCloud PDC, GlobalCloud PKC, GlobalCloud PMC, GlobalCloud PQC, GlobalCloud SOP, GlobalCloud SpaceAI Platform, GlobalCloud Token, GlobalCloud WAE, GlobalCloud XiaoC, GlobalCloud XiaoG`
- volatile_dirty: `GlobalCloud GPCF`
- sensitive_repos: `GlobalCloud AAAS, GlobalCloud XiaoC, GlobalCloud MMC, GlobalCloud PVA, GlobalCloud World, GlobalCloud WAE, GlobalCloud PDC`
- review_boundary: `GlobalCloud AAAS, GlobalCloud Brain, GlobalCloud FireQuote, GlobalCloud GFIS, GlobalCloud GPC, GlobalCloud GPCF, GlobalCloud KDS, GlobalCloud MMC, GlobalCloud Mem, GlobalCloud PDC, GlobalCloud PMC, GlobalCloud PQC, GlobalCloud PVA, GlobalCloud SpaceAI Platform, GlobalCloud WAE, GlobalCloud WAME, GlobalCloud World, GlobalCloud XWAIL, GlobalCloud XiaoC, GlobalCloud XiaoG`

## Repo details

| Repo | dirty_count | ahead | behind | sensitive_paths |
|---|---:|---:|---:|---|
| `GlobalCloud AAAS` | 67 | 0 | 0 | `apps/aaas-console/.env.example, apps/aaas-console/scripts/make-demo-token.mjs, apps/aaas-console/src/styles/gc.tokens.css, docs/design/aaas-console/prototype/gc.tokens.css` |
| `GlobalCloud Brain` | 1 | 3 | 0 | `none` |
| `GlobalCloud WAS` | 0 | 3 | 0 | `none` |
| `GlobalCloud XiaoC` | 209 | 7 | 0 | `.env.bak-20261020-hermes-key, .harness/evidence/xiaoc-feishu-20261022/10-credentials.md, .harness/evidence/xiaoc-feishu-20261022/74-verification-token-wired.md, .harness/evidence/xiaoc-mcp-skill-20261020/23-real-smoke-hermes-credential.md, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-audit.jsonl, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-auth.md, .harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-health.json, packages/feishu-bridge/.env.example` |
| `GlobalCloud WAME` | 6 | 0 | 0 | `none` |
| `GlobalCloud GPC` | 1 | 8 | 0 | `none` |
| `GlobalCloud GPCF` | 160 | 75 | 0 | `none` |
| `GlobalCloud XWAIL` | 1 | 0 | 20 | `none` |
| `GlobalCloud GFIS` | 52 | 0 | 0 | `none` |
| `GlobalCloud MMC` | 137 | 7 | 9 | `console/.env.example` |
| `GlobalCloud KDS` | 119 | 0 | 0 | `none` |
| `GlobalCloud XiaoG` | 1 | 1082 | 16 | `none` |
| `GlobalCloud PVA` | 128 | 0 | 0 | `design/prototype/shots/01-tokens-dark.png, design/prototype/shots/11-tokens-light.png` |
| `GlobalCloud SOP` | 0 | 1 | 0 | `none` |
| `GlobalCloud PKC` | 0 | 18 | 0 | `none` |
| `GlobalCloud XGD` | 0 | 0 | 0 | `none` |
| `GlobalCloud ICP` | 0 | 3 | 0 | `none` |
| `GlobalCloud PQC` | 45 | 35 | 0 | `none` |
| `GlobalCloud SpaceAI Platform` | 35 | 31 | 0 | `none` |
| `GlobalCloud SpaceAI Studio` | 0 | 0 | 0 | `none` |
| `GlobalCloud World` | 155 | 0 | 0 | `.env.example, docs/architecture/auth-embed-token-handoff.md, docs/harness/evidence/screenshots/phase12/token-handoff-1440.png, packages/server/src/services/embed-token.ts, scripts/mint-embed-token.mjs, tests/server/auth-embed-token.test.ts` |
| `GlobalCloud Mem` | 1 | 8 | 0 | `none` |
| `GlobalCloud WAE` | 375 | 98 | 71 | `docs/evidence/R1/supply-chain/secret-scan.json, packages/embed-token/README.md, packages/embed-token/package.json, packages/embed-token/src/index.test.ts, packages/embed-token/src/index.ts, packages/embed-token/tsconfig.json, packages/host-kit/src/host/embedTokenRoute.test.ts, packages/modules/module-gctoken-console/manifest.yaml, packages/modules/module-gctoken-console/src/index.dom.test.tsx, packages/modules/module-gctoken-console/src/index.tsx` |
| `GlobalCloud PMC` | 4 | 4 | 0 | `none` |
| `GlobalCloud PDC` | 56 | 17 | 0 | `.env.example` |
| `GlobalCloud SLC` | 0 | 0 | 0 | `none` |
| `GlobalCloud DRC` | 0 | 0 | 0 | `none` |
| `GlobalCloud FireQuote` | 38 | 0 | 0 | `none` |
| `GlobalCloud Token` | 0 | 10 | 0 | `none` |
