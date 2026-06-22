---
doc_id: GPCF-DOC-BA8E89A900
title: GC-Knowledge Fabric P0 Harness Evidence Candidate Record Dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/harness-evidence-candidate-record-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/harness-evidence-candidate-record-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Harness Evidence Candidate Record Dry-run v0.1

## 定位

本文档定义 P0-D23 Harness evidence candidate record 的 dry-run 口径。它从 D22 Harness review input packet 生成候选证据记录结构，用于后续人工或 Harness Governance 审查。

本记录不是正式 Harness evidence，不写入 `harness_evidence_records`，不代表 P0 已验收。

## 候选记录字段

| 字段 | 值 |
|---|---|
| id | `GCKF-P0-HER-CANDIDATE-001` |
| recordType | `harness_evidence_candidate` |
| subject | `GC-Knowledge Fabric P0 D9-D22 dry-run evidence review` |
| sourcePacketRef | `GCKF-P0-HARNESS-REVIEW-INPUT-PACKET-DRY-RUN-V0.1` |
| reviewStatus | `pending` |
| requiredReviewerType | `human_or_harness_governance` |

## 允许结论

候选记录只允许后续审查形成以下结论候选：

- `approved_for_formal_harness_evidence`
- `repair_required`
- `rejected`
- `scope_violation_found`

默认结论仍为 `pending`，且 `pending` 不属于最终结论。

## 禁止行为

D23 禁止：

- 写正式 Harness evidence。
- 写 KDS。
- 写业务系统。
- 启动 server。
- 连接数据库。
- 调用外部 API。
- 提升 lifecycle 为 `accepted` 或 `integrated`。
- 宣称 `production_ready` 或 `business_write_enabled`。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_harness_evidence_candidate_record_dry_run.py
```

预期信号：

```text
gckf_p0_harness_evidence_candidate_record_dry_run=pass status=candidate record_type=harness_evidence_candidate source_packet_status=candidate review_status=pending decision_outcomes=4 source_inputs=4 risk_refs=3 required_sources=4 requires_human_review=covered requires_harness_governance=covered not_final_acceptance=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D24 建议建立 Harness decision template dry-run，明确 `approved_for_formal_harness_evidence`、`repair_required`、`rejected`、`scope_violation_found` 四类结论的字段、证据要求和禁止越权动作。
