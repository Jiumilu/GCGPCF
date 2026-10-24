---
doc_id: GPCF-DOC-3CE1BDF7EA
title: "P19 · 90 天组合决策试算表（2026-10-24 15:20 刷新）"
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAME, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/p19-day90-candidate-table-20261024.md
source_path: docs/reports/p19-day90-candidate-table-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P19 · 90 天组合决策试算表（2026-10-24 15:20 刷新）

- 性质：**试算，不是决策**。90 天末须对每项目跑 `classify_project_status` + `gate` + `authorization_qa` 后由老卢裁定。
- 数据源：`render --json`（C_dev 41.53%）、`decisions.yaml`、`runtime/queue.json`

| 项目 | 车道 | C_dev | 当前处置 | Feature 状态 | 试算倾向 |
|---|---|---:|---|---|---|
| PVAOS | core | 10.0% | continue | — | ⚠ 复核 continue/pause |
| SOP | core | 10.0% | continue | F-012:queued | ⚠ 复核 continue/pause |
| SLC | support | 14.5% | continue | — | ⚠ 复核 continue/pause |
| GPC | core | 15.4% | continue | — | continue（观察） |
| DRC | base | 16.0% | continue | — | continue（观察） |
| PQC | support | 25.5% | continue | F-032:queued | continue（观察） |
| Brain | base | 26.7% | continue | F-006:closed, F-007:closed | continue（观察） |
| XiaoG | base | 26.7% | pause | — | pause（维持/复核） |
| MMC | base | 28.0% | continue | — | continue（观察） |
| GFIS | core | 30.0% | continue | F-005:commit | continue |
| KDS | core | 36.4% | continue | — | continue |
| SpaceAI | support | 39.4% | continue | F-017:evaluated, F-024:closed, F-037:queued, F-038:queued | continue |
| WAS | core | 40.0% | continue | F-022:queued, F-023:queued | continue |
| PKC | base | 40.0% | merge | — | merge（待宿主完成） |
| Project | support | 40.0% | continue | F-028:closed | continue |
| PDC | support | 40.0% | continue | F-030:closed | continue |
| AAAS | core | 42.5% | pause | F-020:closed | pause（维持/复核） |
| XWAIL | core | 42.5% | merge | — | merge（待宿主完成） |
| WAME | core | 44.1% | continue | F-035:closed | continue |
| SpaceAIStudio | support | 50.0% | continue | — | continue |
| WAE | base | 50.9% | continue | F-034:evaluated, F-036:queued | continue |
| XiaoC | base | 56.9% | continue | F-033:queued | continue |
| FireQuote | core | 56.9% | continue | — | continue |
| GCMEM | base | 60.0% | continue | F-026:closed | continue |
| GPCF | core | 68.3% | continue | F-002:closed, F-003:closed, F-004:closed, F-009:closed, F-010:closed, F-013:blocked, F-014:evaluated, F-016:commit, F-018:closed, F-025:queued, F-027:closed, F-029:plan | continue |
| XGD | base | 69.2% | continue | F-031:closed | continue |
| ICP | core | 69.2% | pause | F-008:closed, F-019:evaluated | pause（维持/复核） |
| World | base | 70.0% | pause | F-021:closed | pause（维持/复核） |
| Studio | base | 75.0% | exit | F-011:closed, F-015:closed | exit（维持） |

## 使用说明

1. 90 天末先跑 `render_project_group_completion.py --json` 刷新 C_dev；
2. 每项目跑 `classify_project_status`，处置变更项再跑 `gate(redline)` 与 `authorization_qa`；
3. 合并/退出逐项出清单 + 回滚 + 回执，不得批量口令；
4. 结论写回 `decisions.yaml`（append-only）。
