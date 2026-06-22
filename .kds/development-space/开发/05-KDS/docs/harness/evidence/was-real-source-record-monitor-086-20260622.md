---
doc_id: GPCF-DOC-6C0AA90086
title: WAS Real Source Record Monitor 086 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-real-source-record-monitor-086-20260622.md
source_path: docs/harness/evidence/was-real-source-record-monitor-086-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# WAS Real Source Record Monitor 086 证据

## 范围

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-086` 将绿色供应链覆盖扩展到售后现场环境事件记录、现场纠正措施通知、产品召回环境风险评估、客户现场围堵记录、替换或返工处置记录、监管现场行动通知和售后关闭核验声明证据链。只有补齐这些证据，Ontology 才能安全地把交付后环境事件、召回、现场纠正和客户现场处置闭环绑定到下游 WAES/KDS/runtime 门禁中。

## 监控检查

| Check | Value |
|---|---:|
| submitted_real_candidate_files | `0` |
| post_market_environmental_incident_record_gaps | `0` |
| field_corrective_action_notice_gaps | `0` |
| product_recall_environmental_risk_assessment_gaps | `0` |
| customer_site_containment_record_gaps | `0` |
| replacement_or_rework_disposition_record_gaps | `0` |
| regulatory_field_action_notification_gaps | `0` |
| post_market_closure_verification_statement_gaps | `0` |
| accepted_for_post_market_field_action_profile | `0` |
| accepted_for_next_gate | `0` |
| hold_required | `1` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |
| accepted | `False` |
| integrated | `False` |
| production_ready | `False` |

## 必需证据类别

- `post_market_environmental_incident_record`
- `field_corrective_action_notice`
- `product_recall_environmental_risk_assessment`
- `customer_site_containment_record`
- `replacement_or_rework_disposition_record`
- `regulatory_field_action_notification`
- `post_market_closure_verification_statement`

## 必需命令

```bash
python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py
python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py
python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py
python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py
python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py
python3 tools/kds-sync/validate_was_real_source_record_monitor_086.py
```

## 非声明

- 本证据不创建也不推断售后现场环境事件记录、现场纠正措施通知、产品召回环境风险评估、客户现场围堵记录、替换或返工处置记录、监管现场行动通知和售后关闭核验声明。
- 本证据不写入 GFIS/KWE 运行层。
- 本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。

## 下一轮

`GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-087`
