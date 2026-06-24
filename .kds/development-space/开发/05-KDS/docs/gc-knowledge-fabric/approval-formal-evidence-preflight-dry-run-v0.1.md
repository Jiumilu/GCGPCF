---
doc_id: GPCF-DOC-8150726FA5
title: GC-Knowledge Fabric P0 Approval Formal Evidence Preflight Dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/approval-formal-evidence-preflight-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/approval-formal-evidence-preflight-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Approval Formal Evidence Preflight Dry-run v0.1

## 定位

本文档定义 P0-D27 approval-to-formal-evidence preflight 的 dry-run 口径。它从 D24 Harness decision template 中抽取 `approved_for_formal_harness_evidence` 结论，生成正式 Harness evidence 写入前的预检清单。

本路径不写正式 Harness evidence，不写 KDS，不升级 lifecycle，不把 P0 标记为 accepted。正式写入必须由后续独立 Harness action 执行，并保留人工或 Harness Governance 审查记录。

## 覆盖与排除

| 类型 | 决策结论 | 处理 |
|---|---|---|
| 覆盖 | `approved_for_formal_harness_evidence` | 生成正式 evidence 写入前预检候选 |
| 排除 | `repair_required` | 进入补证路径 |
| 排除 | `rejected` | 进入拒绝归档路径 |
| 排除 | `scope_violation_found` | 进入治理跟进路径 |

## 预检必填字段

正式 Harness evidence 写入前，预检候选必须包含：

- reviewerId
- reviewedAt
- evidenceRefs
- sourceCandidateRecordRef
- decisionRationale
- targetHarnessEvidenceType

## 预检门禁

必须完成的预检：

- 来源候选记录仍为 candidate。
- 决策模板仍为 candidate。
- 决策结论只能是 `approved_for_formal_harness_evidence`。
- 同一候选不存在未关闭的 repair_required。
- 同一候选不存在 rejected archive。
- 同一候选不存在 scope_violation。
- 存在人工或 Harness Governance reviewer。
- 正式写入必须使用独立 Harness action。

## 禁止动作

- 不写正式 Harness evidence。
- 不提升 lifecycle。
- 不开启业务写回。
- 不标记 P0 accepted。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_approval_formal_evidence_preflight_dry_run.py
```

预期信号：

```text
gckf_p0_approval_formal_evidence_preflight_dry_run=pass status=candidate preflight_type=formal_harness_evidence_write_preflight source_template_status=candidate covered_decisions=1 excluded_decisions=3 required_fields=6 required_evidence_refs=6 preflight_checks=8 required_sources=4 not_final_acceptance=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D28 建议建立 formal evidence write action guard dry-run，定义正式 evidence 写入动作本身的权限、输入、幂等、防重复和回滚前置条件，但仍不执行真实写入。
