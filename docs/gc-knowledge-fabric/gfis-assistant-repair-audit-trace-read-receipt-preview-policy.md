---
doc_id: GPCF-DOC-E07ACF4305
title: GFIS Assistant Repair Audit Trace Read Receipt Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-audit-trace-read-receipt-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-audit-trace-read-receipt-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Audit Trace Read Receipt Preview No-write 规则

## 目标

本规则定义 DKS-119 的 GFIS Assistant Repair Audit Trace Read Receipt Preview。

它把 DKS-118 的 audit trace preview 转成本地只读回执预览，用于说明用户查看审计解释时界面可以展示的候选回执信息：

- 查看的是哪个 audit trace preview。
- 来源 event preview、action guard 和 read model 是什么。
- UI 可以展示什么 read receipt preview 文案。
- 哪些治理动作仍被阻断。
- 为什么该预览不能被当作真实 ReadReceipt、Harness evidence 或 KDS 状态变化。

Read receipt preview 只是一层本地显示候选，不是已读回执，不是审计记录，不是证据，不是事件，也不是状态变更。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| read receipt preview | 只能用于本地展示 |
| ReadReceipt | 不创建真实 ReadReceipt |
| audit trace record | 不创建真实 audit trace record |
| EventRecord | 不创建真实 EventRecord |
| ActionReceipt | 不创建真实 ActionReceipt |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES Gate Result | 不创建 WAES gate result |
| KWE WorkItem | 不创建 KWE work item |
| KDS lifecycle | 不提升、不冻结、不发布、不 accepted |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 收益/积分/额度/悬赏 | 不确认、不分配、不结算 |
| 外部 API | 不调用真实外部 API |

## 标准链路

```text
DKS-118 audit trace preview
→ DKS-119 read receipt preview
→ UI 展示已查看候选提示
→ 保持 no-write
```

禁止链路：

```text
read receipt preview
→ ReadReceipt
→ Harness evidence
→ EventRecord
→ WAES Gate Result
→ KWE WorkItem
→ KDS lifecycle accepted
→ GFIS 正式写回
```

## Receipt 类型

| receipt_type | 用途 |
| --- | --- |
| display_read_receipt_preview | 普通只读审计解释的查看回执预览 |
| repair_read_receipt_preview | 修复提示审计解释的查看回执预览 |
| metadata_boundary_read_receipt_preview | metadata-only 边界的查看回执预览 |
| committee_read_receipt_preview | 委员会提示的查看回执预览 |
| freeze_read_receipt_preview | 冻结提示的查看回执预览 |
| blocked_write_read_receipt_preview | 写回阻断提示的查看回执预览 |

## Receipt 状态

| receipt_status | 含义 |
| --- | --- |
| receipt_preview_only | 仅回执预览 |
| blocked_receipt_preview | 阻断回执预览 |
| metadata_receipt_preview | metadata-only 回执预览 |
| repair_receipt_preview | 修复提示回执预览 |
| committee_receipt_preview | 委员会提示回执预览 |
| freeze_receipt_preview | 冻结提示回执预览 |

## Receipt 决策

| receipt_decision | 含义 |
| --- | --- |
| show_receipt_preview_only | 只显示回执预览 |
| show_repair_receipt_preview | 显示修复回执预览 |
| show_metadata_boundary_receipt_preview | 显示 metadata-only 回执预览 |
| show_committee_receipt_preview | 显示委员会回执预览 |
| show_freeze_receipt_preview | 显示冻结回执预览 |
| show_blocked_write_receipt_preview | 显示写回阻断回执预览 |

## 必填字段

Read receipt preview 必须具备：

- `readReceiptPreviewId`
- `auditTraceRef`
- `eventPreviewRef`
- `actionGuardRef`
- `readModelRef`
- `tenantId`
- `projectId`
- `surface`
- `receiptType`
- `receiptStatus`
- `receiptDecision`
- `receiptSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `receiptNoteRefs`
- `blockedActions`
- 所有 `creates*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_audit_trace_read_receipt_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表：

- 真实 ReadReceipt 已创建。
- 真实 audit trace record 已创建。
- Harness evidence 已固化。
- WAES 已通过。
- KWE 工单已生成。
- KDS lifecycle 已提升。
- GFIS/GPC/ERP/MES 已写回。
- 收益、积分、额度、悬赏已确认。
