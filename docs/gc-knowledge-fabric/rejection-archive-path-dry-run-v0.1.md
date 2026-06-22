---
doc_id: GPCF-DOC-558CE4DCB8
title: GC-Knowledge Fabric P0 Rejection Archive Path Dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/rejection-archive-path-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/rejection-archive-path-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Rejection Archive Path Dry-run v0.1

## 定位

本文档定义 P0-D26 rejection archive path 的 dry-run 口径。它从 D24 Harness decision template 中抽取 `rejected` 结论，生成拒绝归档候选规则、复审前置条件和新候选包重建要求。

本路径不写正式归档记录，不写 Harness evidence，不写 KDS，不允许将 rejected 包复用为验收依据。

## 覆盖与排除

| 类型 | 决策结论 | 处理 |
|---|---|---|
| 覆盖 | `rejected` | 生成 rejected candidate archive 候选规则 |
| 排除 | `approved_for_formal_harness_evidence` | 不归档为拒绝 |
| 排除 | `repair_required` | 进入补证路径 |
| 排除 | `scope_violation_found` | 进入治理跟进路径 |

## 拒绝归档候选规则

拒绝归档候选必须包含：

- reviewerId
- reviewedAt
- rejectionReason
- evidenceRefs
- decisionRationale
- sourceCandidateRecordRef

必须执行的候选动作：

- 标记候选包不可复用。
- 记录拒绝依据。
- 要求重新提交时构建新候选包。
- 保留 lineage 引用。

## 重建前置条件

被拒绝候选如需复审，必须满足：

- 新增或修复来源证据。
- 重新生成 Harness review input packet。
- 重新生成 Harness evidence candidate record。
- 重新进入 Harness decision template review。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_rejection_archive_path_dry_run.py
```

预期信号：

```text
gckf_p0_rejection_archive_path_dry_run=pass status=candidate archive_type=rejected_harness_candidate_archive archive_status=candidate source_template_status=candidate covered_decisions=1 excluded_decisions=3 required_fields=6 required_actions=4 rebuild_preconditions=4 required_sources=4 not_final_acceptance=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 writes_archive_record=0 no_write=covered
```

## 下一步

D27 建议建立 approval-to-formal-evidence preflight dry-run，把 `approved_for_formal_harness_evidence` 转为正式 Harness evidence 写入前的预检清单，但仍不执行正式写入。
