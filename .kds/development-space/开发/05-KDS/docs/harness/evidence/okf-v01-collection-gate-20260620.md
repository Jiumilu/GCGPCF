---
doc_id: GPCF-DOC-FB59ECF423
title: OKF v0.1 集合门禁证据
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-collection-gate-20260620.md
source_path: docs/harness/evidence/okf-v01-collection-gate-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# OKF v0.1 集合门禁证据

generated_at: 2026-06-21T00:41:45.157348+00:00

## 摘要

| metric | value |
| --- | --- |
| status | pass |
| bundles | 3 |
| policy | `metadata_only_no_body_copy` |
| source_of_record | `KDS / Git controlled documents` |
| relationship_graph | `docs/harness/evidence/okf-v01-relationship-graph-20260620.md` |
| consumption_benchmark | `docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md` |
| summary_admission_gate | `docs/harness/evidence/okf-v01-summary-admission-gate-20260620.md` |
| summary_admission_ledger | `docs/harness/evidence/okf-v01-summary-admission-ledger-20260620.md` |
| summary_approval_request_gate | `docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.md` |
| summary_approval_negative_fixtures | `docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md` |
| summary_approval_expiry_gate | `docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md` |
| approved_summary_writer_dry_run | `docs/harness/evidence/okf-v01-approved-summary-writer-dry-run-20260620.md` |
| approved_summary_writer_positive_fixture | `docs/harness/evidence/okf-v01-approved-summary-writer-positive-fixture-20260620.md` |

## 结果

| gate | exit_code | output |
| --- | ---: | --- |
| kds_bundle | 0 | `okf_bundle_gate=pass bundle=.okf/bundles/kds-v0.1 okf_version=0.1 concepts=36 types=Governance Gate:2,Governance Plan:11,Governance Report:13,KDS Document:5,KDS Ledger:5 reserved_filenames=pass frontmatter=pass source_of_record=kds derivation_policy=metadata_only_no_body_copy links=pass backlinks=pass stale=pass` |
| governance_bundle | 0 | `okf_bundle_gate=pass bundle=.okf/bundles/governance-v0.1 okf_version=0.1 concepts=39 types=Governance Gate:2,Governance Plan:9,Governance Report:12,KDS Document:10,KDS Ledger:5,Knowledge Index:1 reserved_filenames=pass frontmatter=pass source_of_record=kds derivation_policy=metadata_only_no_body_copy links=pass backlinks=pass stale=pass` |
| architecture_bundle | 0 | `okf_bundle_gate=pass bundle=.okf/bundles/architecture-v0.1 okf_version=0.1 concepts=6 types=Architecture Document:4,Governance Plan:1,Governance Report:1 reserved_filenames=pass frontmatter=pass source_of_record=kds derivation_policy=metadata_only_no_body_copy links=pass backlinks=pass stale=pass` |
| collection | 0 | `okf_collection_gate=pass bundles=3 concepts=81 bundle_summaries=.okf/bundles/kds-v0.1:36,.okf/bundles/governance-v0.1:39,.okf/bundles/architecture-v0.1:6 duplicate_sources=30` |
| relationship_graph | 0 | `okf_relationship_graph=pass bundles=3 concepts=81 nodes=186 edges=303 duplicate_sources=30` |
| consumption_benchmark | 0 | `okf_consumption_benchmark=pass concepts=81 passed=6/6` |
| summary_approval_request_gate | 0 | `okf_summary_approval_request_gate=pass requests=1 failures=0` |
| summary_approval_negative_fixtures | 0 | `okf_summary_approval_negative_fixtures=pass fixtures=4` |
| summary_approval_expiry_gate | 0 | `okf_summary_approval_expiry_gate=pass requests=1 expired_real_requests=0 fixtures=1` |
| summary_admission_gate | 0 | `okf_summary_admission_gate=pass concepts=81 approved_summaries=0 pending_requests=3 approved_requests=0 sensitive_hits=0 violations=0` |
| approved_summary_writer_dry_run | 0 | `okf_approved_summary_writer_dry_run=pass approved_rows=0 would_write=0 blocked=0` |
| approved_summary_writer_positive_fixture | 0 | `okf_approved_summary_writer_positive_fixture=pass approved_rows=1 would_write=1` |

## 边界

- OKF 是派生的消费与交换层。
- KDS / Git 受控文档仍是 source of record。
- 本 evidence 不升级业务、验收或集成状态。
