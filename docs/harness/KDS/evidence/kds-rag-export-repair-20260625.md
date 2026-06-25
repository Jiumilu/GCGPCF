---
doc_id: GPCF-DOC-KDS-RAG-EXPORT-REPAIR-20260625
title: KDS RAG export 修复证据 2026-06-25
project: KDS
related_projects: [KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/KDS/evidence/kds-rag-export-repair-20260625.md
source_path: docs/harness/KDS/evidence/kds-rag-export-repair-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: [GPCF-DOC-KDS-REAL-RUNTIME-BASELINE-20260624]
superseded_by: []
---

# KDS RAG export 修复证据 2026-06-25

## 1. 证据定位

本文登记 `KDS-RAG-EXPORT-001` 的本地真实执行结果。

本文只证明 KDS RAG 准入导出、导出校验、证据门禁、API smoke、GBrain search/query 和 wiki trust audit 在 local dev 范围内通过。本文不声明 KDS 真实交付完成，不声明 Brain 已接受该结果，不声明客户验收通过。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| 项目仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS` |
| 执行日期 | 2026-06-25 |
| 输出目录 | `/tmp/kds-rag-export-20260625-083909` |
| 工作区状态 | dirty，存在既有 KDS 100 分评估输出和治理文件改动 |
| 本轮修改文件 | `_governance/scripts/rag_admission_policy.py`、`_governance/scripts/wiki_trust_audit.py` |
| 修改边界 | 仅修复 frontmatter 字段为 list 时的脚本类型兼容，不改知识内容、不改 RAG 准入业务规则 |

## 3. 原始失败

首次执行 RAG 导出失败：

```text
TypeError: unhashable type: 'list'
```

失败点：

```text
_governance/scripts/rag_admission_policy.py
frontmatter.get("verification_status") not in ALLOWED_RAG_VERIFICATION
```

原因：部分 Markdown frontmatter 的 `verification_status` 为 list，例如：

```text
verification_status = ['source_verified']
verification_status = ['source_only']
verification_status = ['needs_review']
```

原策略把 `verification_status` 视为字符串，直接进行 set membership 判断，遇到 list 后触发 `TypeError`。

## 4. 修复内容

| 文件 | 修复 |
|---|---|
| `_governance/scripts/rag_admission_policy.py` | `evidence_rank` 支持 list；新增 `verification_admissible`，list 中任一值属于 `source_verified`、`human_confirmed`、`confirmed` 即视为验证状态可准入 |
| `_governance/scripts/wiki_trust_audit.py` | 新增 `field_contains`，使 AI/E2 RAG 风险统计支持 list 类型 `verification_status` |

## 5. 复跑命令与结果

| 命令 | 结果 | 证据 |
|---|---|---|
| `python3 _governance/scripts/export_rag_admission.py --root . --json-out /tmp/kds-rag-export-20260625-083909/rag-admission.json --txt-out /tmp/kds-rag-export-20260625-083909/rag-allowlist.txt --manifest-out /tmp/kds-rag-export-20260625-083909/rag-manifest.jsonl --md-out /tmp/kds-rag-export-20260625-083909/rag-admission.md` | pass，`allowlist_count=156 rejected_count=6053` | `/tmp/kds-rag-export-20260625-083909/rag-admission.json` |
| `python3 _governance/scripts/validate_rag_export.py --root . --admission /tmp/kds-rag-export-20260625-083909/rag-admission.json --allowlist /tmp/kds-rag-export-20260625-083909/rag-allowlist.txt --manifest /tmp/kds-rag-export-20260625-083909/rag-manifest.jsonl --json-out /tmp/kds-rag-export-20260625-083909/rag-validation.json --md-out /tmp/kds-rag-export-20260625-083909/rag-validation.md` | pass，`allowlist_count=156 manifest_count=156 error_count=0 warning_count=1` | `/tmp/kds-rag-export-20260625-083909/rag-validation.json` |
| `python3 _governance/scripts/validate_evidence_gates.py --root . --json-out /tmp/kds-rag-export-20260625-083909/evidence-gates.json --md-out /tmp/kds-rag-export-20260625-083909/evidence-gates.md` | pass，`gate_count=46 issue_count=0 warning_count=0` | `/tmp/kds-rag-export-20260625-083909/evidence-gates.json` |
| `python3 -m pytest tests/test_api_smoke.py` | pass，`2 passed in 4.52s` | `/tmp/kds-rag-export-20260625-083909/pytest-test-api-smoke.log` |
| `gbrain search "RAG 准入 导出 校验"` | pass，返回历史 RAG 准入导出校验报告等结果 | `/tmp/kds-rag-export-20260625-083909/gbrain-search-rag-export.log` |
| `gbrain query "KDS RAG 准入导出校验当前状态是什么"` | pass，返回 GPCF/KDS 相关上下文 | `/tmp/kds-rag-export-20260625-083909/gbrain-query-rag-export.log` |
| `python3 _governance/scripts/wiki_trust_audit.py --root . --json-out /tmp/kds-rag-export-20260625-083909/wiki-trust-audit.json --md-out /tmp/kds-rag-export-20260625-083909/wiki-trust-audit.md` | pass，`rag_admissible_count=156` | `/tmp/kds-rag-export-20260625-083909/wiki-trust-audit.json` |

## 6. 状态建议

```text
kds_rag_export = verified_with_local_dev_boundary
kds_rag_export_allowlist_count = 156
kds_rag_export_manifest_count = 156
kds_rag_export_error_count = 0
kds_evidence_gate = pass
kds_api_smoke = pass
kds_gbrain_search = pass
kds_gbrain_query = pass
kds_wiki_trust_audit = pass
kds_status_candidate = ready_for_review
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 7. 保留边界

| 边界 | 说明 |
|---|---|
| dirty workspace | KDS 仓仍存在本轮之前的脏工作区和多个未跟踪 100 分评估输出 |
| local dev only | 本轮只在本地执行，不代表生产索引、真实 KDS API 同步或客户环境通过 |
| warning_count=1 | `validate_rag_export.py` 仍报告 1 个 warning，主要用于提示 rejected surface，不构成 error |
| Brain acceptance | Brain 侧尚未把本轮 KDS RAG export 结果作为正式审查输入 |
| human confirmation | 未经用户确认，不得升级为 `accepted`、`integrated` 或客户验收通过 |

## 8. 下一步

1. 将本证据回写 `GlobalCloud 项目群真实执行治理总控板` 和 `GlobalCloud 核心链路真实证据台账`。
2. 由 GPCF 门禁验证 `KDS-RAG-EXPORT-001` 已从 `repair_required` 推进为 `verified_with_local_dev_boundary`。
3. 后续可将 KDS 结果传导给 `BRAIN-REVIEW-HANDOFF-001`，但 Brain 状态升级仍需人工确认。
