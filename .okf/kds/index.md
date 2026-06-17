---
doc_id: GPCF-DOC-40F2D45CE1
title: OKF KDS Bundle 只读索引
project: GPCF
related_projects: [GPCF, GPC, WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.okf/kds/index.md
source_path: .okf/kds/index.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# OKF KDS Bundle 只读索引

## Source Documents

| purpose | source_path | kds_path |
| --- | --- | --- |
| KDS 开发空间安全规范 | `02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | `开发/91-治理与验收/02-governance/GlobalCloud项目群KDS开发空间安全规范.md` |
| KDS 开发空间同步计划 | `09-status/kds-development-space-sync-plan.md` | `开发/91-治理与验收/09-status/kds-development-space-sync-plan.md` |
| KDS 同步台账 | `09-status/kds-development-space-sync-register.md` | `开发/91-治理与验收/09-status/kds-development-space-sync-register.md` |
| KDS 只读探测报告 | `09-status/kds-readonly-probe-report.md` | `开发/91-治理与验收/09-status/kds-readonly-probe-report.md` |
| KDS Markdown 化闭环方案 | `09-status/kds-md-okf-implementation-closure-plan.md` | `开发/91-治理与验收/09-status/kds-md-okf-implementation-closure-plan.md` |
| KDS 关联数据检索机制 | `03-data-ai-knowledge/GlobalCloud Loop开发KDS关联数据检索机制.md` | `开发/05-KDS/03-data-ai-knowledge/GlobalCloud Loop开发KDS关联数据检索机制.md` |
| KDS 知识编制边界 | `03-data-ai-knowledge/GlobalCloudBrain-KDS知识编制与知识UI边界清单.md` | `开发/05-KDS/03-data-ai-knowledge/GlobalCloudBrain-KDS知识编制与知识UI边界清单.md` |
| ODF 受控引入试点方案 | `09-status/odf-introduction-governance-plan.md` | `开发/91-治理与验收/09-status/odf-introduction-governance-plan.md` |
| ODF 试点样本准入台账 | `docs/harness/evidence/odf-pilot-sample-ledger-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-pilot-sample-ledger-20260617.md` |
| ODF 试点闭环报告 | `docs/harness/evidence/odf-pilot-closure-report-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-pilot-closure-report-20260617.md` |
| ODF Phase 2 扩大样本验证计划 | `09-status/odf-phase2-expansion-plan.md` | `开发/91-治理与验收/09-status/odf-phase2-expansion-plan.md` |
| ODF Phase 2 样本准入台账 | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` |
| ODF Phase 2 闭环报告 | `docs/harness/evidence/odf-phase2-closure-report-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase2-closure-report-20260617.md` |

## Ledger And Gates

| evidence | path |
| --- | --- |
| KDS real write ledger | `.kds/sync-ledger.jsonl` |
| Sync plan JSON | `.kds/sync-plan.json` |
| Readonly probe JSON | `.kds/readonly-probe.json` |
| ODF pilot sample ledger | `docs/harness/evidence/odf-pilot-sample-ledger-20260617.json` |
| ODF Phase 2 sample ledger | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.json` |

## Safety Rule

KDS bundle 不展示 TOKEN，不把 `.kds/development-space/开发` 本地镜像当作真实 KDS API 同步结果。真实写入只以 `.kds/sync-ledger.jsonl` 中 `result=http_200` 的记录为证据。
