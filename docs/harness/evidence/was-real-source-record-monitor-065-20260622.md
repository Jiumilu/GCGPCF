---
doc_id: GPCF-DOC-6C0AA90065
title: WAS Real Source Record Monitor 065 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-065-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-065-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 065 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-065` 将绿色供应链覆盖扩展到 EPR / 生产者责任延伸合规链：EPR 注册、生产者责任体系会员、EPR 费用支付记录、回收目标报告、监管方确认回执、EPR 审计证据和 EPR 整改关闭。只有补齐这些证据，Ontology 才能安全地把生产者责任、回收目标、费用履约、监管回执、审计和整改闭环绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| epr_registration_gaps | `0` |
| producer_responsibility_scheme_membership_gaps | `0` |
| epr_fee_payment_record_gaps | `0` |
| takeback_target_report_gaps | `0` |
| regulator_acknowledgement_gaps | `0` |
| epr_audit_evidence_gaps | `0` |
| epr_corrective_action_closure_gaps | `0` |
| accepted_for_epr_compliance_profile | `0` |
| accepted_for_next_gate | `0` |
| hold_required | `1` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 必需证据类别

- `epr_registration`
- `producer_responsibility_scheme_membership`
- `epr_fee_payment_record`
- `takeback_target_report`
- `regulator_acknowledgement`
- `epr_audit_evidence`
- `epr_corrective_action_closure`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_065.py
```

## 非声明

- 本证据不创建也不推断 EPR 注册、生产者责任体系会员、EPR 费用支付记录、回收目标报告、监管方确认回执、EPR 审计证据或 EPR 整改关闭。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-066`
