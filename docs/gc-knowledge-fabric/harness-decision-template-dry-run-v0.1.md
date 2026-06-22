---
doc_id: GPCF-DOC-28C41FEC64
title: GC-Knowledge Fabric P0 Harness Decision Template Dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/harness-decision-template-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/harness-decision-template-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Harness Decision Template Dry-run v0.1

## 定位

本文档定义 P0-D24 Harness decision template 的 dry-run 口径。它从 D23 Harness evidence candidate record 派生，用于约束后续人工或 Harness Governance 审查时允许形成的结论结构。

本模板不是正式 Harness 决议，不写正式 evidence，不提升任何 lifecycle。

## 允许结论

| 结论 | 含义 | 关键要求 |
|---|---|---|
| `approved_for_formal_harness_evidence` | 候选证据可进入正式 Harness evidence 写入审查 | 需要 reviewer、时间、证据引用、来源候选记录和理由 |
| `repair_required` | 证据存在缺口，需要回到补证路径 | 需要修复动作、缺口引用和理由 |
| `rejected` | 候选证据被拒绝，不能继续沿用为验收依据 | 需要拒绝原因、证据引用和理由 |
| `scope_violation_found` | 发现范围或边界违规，需要治理跟进 | 需要违规引用、严重等级和理由 |

默认决策状态必须保持 `pending`。`pending` 不是最终结论。

## 禁止动作

所有结论模板均禁止：

- `write_formal_evidence`
- `promote_lifecycle`
- 直接关闭 P0 acceptance
- 启用业务写回
- 忽略范围违规

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_harness_decision_template_dry_run.py
```

预期信号：

```text
gckf_p0_harness_decision_template_dry_run=pass status=candidate template_type=harness_decision_template source_candidate_status=candidate source_review_status=pending decision_cases=4 requires_human_review=covered requires_harness_governance=covered not_final_acceptance=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D25 建议建立 repair path workpack dry-run，把 `repair_required` 和 `scope_violation_found` 两类结论转为 KWE/LOOP 可追踪的补证或治理跟进候选工单。
