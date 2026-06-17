---
doc_id: GPCF-DOC-37BA319CB6
title: OKF Governance Bundle 只读索引
project: GPCF
related_projects: [GPCF, GPC, WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.okf/governance/index.md
source_path: .okf/governance/index.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# OKF Governance Bundle 只读索引

## Source Documents

| purpose | source_path | kds_path |
| --- | --- | --- |
| 文档综合治理规范 | `02-governance/GlobalCloud项目群文档综合治理规范.md` | `开发/91-治理与验收/02-governance/GlobalCloud项目群文档综合治理规范.md` |
| 文档防污染规则 | `02-governance/GlobalCloud项目群文档防污染规则.md` | `开发/91-治理与验收/02-governance/GlobalCloud项目群文档防污染规则.md` |
| Loop 执行规则 | `02-governance/loop/LOOP_EXECUTION_RULES.md` | `开发/91-治理与验收/02-governance/loop/LOOP_EXECUTION_RULES.md` |
| Loop 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | `开发/91-治理与验收/02-governance/loop/LOOP_CONTROL_BOARD.md` |
| Loop 治理运行边界 | `02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md` | `开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md` |
| Loop 阶段目标 | `02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md` | `开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md` |
| Harness evidence index | `docs/harness/evidence/evidence-index.md` | `开发/12-GPCF/docs/harness/evidence/evidence-index.md` |
| 文档健康报告 | `09-status/globalcloud-document-health-report.md` | `开发/91-治理与验收/09-status/globalcloud-document-health-report.md` |
| 文档控制台账 | `09-status/globalcloud-document-control-register.md` | `开发/91-治理与验收/09-status/globalcloud-document-control-register.md` |
| ODF 受控引入试点方案 | `09-status/odf-introduction-governance-plan.md` | `开发/91-治理与验收/09-status/odf-introduction-governance-plan.md` |
| ODF 试点样本准入台账 | `docs/harness/evidence/odf-pilot-sample-ledger-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-pilot-sample-ledger-20260617.md` |
| ODF 试点闭环报告 | `docs/harness/evidence/odf-pilot-closure-report-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-pilot-closure-report-20260617.md` |
| ODF Phase 2 扩大样本验证计划 | `09-status/odf-phase2-expansion-plan.md` | `开发/91-治理与验收/09-status/odf-phase2-expansion-plan.md` |
| ODF Phase 2 样本准入台账 | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` |
| ODF Phase 2 闭环报告 | `docs/harness/evidence/odf-phase2-closure-report-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase2-closure-report-20260617.md` |
| ODF Phase 3 受控模板化与准入门禁计划 | `09-status/odf-phase3-schema-gate-plan.md` | `开发/91-治理与验收/09-status/odf-phase3-schema-gate-plan.md` |
| ODF Phase 3 Schema Gate Evidence | `docs/harness/evidence/odf-phase3-schema-gate-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase3-schema-gate-20260617.md` |
| ODF Phase 4 小批量准入试运行方案 | `09-status/odf-phase4-small-batch-admission-plan.md` | `开发/91-治理与验收/09-status/odf-phase4-small-batch-admission-plan.md` |
| ODF Phase 4 小批量准入台账 | `docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.md` |
| ODF Phase 4 闭环报告 | `docs/harness/evidence/odf-phase4-small-batch-closure-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase4-small-batch-closure-20260617.md` |
| ODF Phase 5 准入变更申请治理方案 | `09-status/odf-phase5-change-request-governance-plan.md` | `开发/91-治理与验收/09-status/odf-phase5-change-request-governance-plan.md` |
| ODF Phase 5 准入变更申请台账 | `docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md` |
| ODF Phase 5 闭环报告 | `docs/harness/evidence/odf-phase5-change-request-closure-20260617.md` | `开发/05-KDS/docs/harness/evidence/odf-phase5-change-request-closure-20260617.md` |

## Verification Gates

```bash
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
python3 tools/kds-sync/kds_conflict_guard.py
python3 tools/kds-sync/validate_odf_schema_gate.py
python3 tools/kds-sync/validate_odf_change_request_gate.py
```
