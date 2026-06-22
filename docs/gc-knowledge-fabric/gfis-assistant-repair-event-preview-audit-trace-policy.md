---
doc_id: GPCF-DOC-D15920121E
title: GFIS Assistant Repair Event Preview Audit Trace No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-event-preview-audit-trace-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-event-preview-audit-trace-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Event Preview Audit Trace No-write 规则

## 目标

本规则定义 DKS-118 的 GFIS Assistant Repair Event Preview Audit Trace。

它把 DKS-117 的本地 event preview 转成可展示的审计解释线索，用于说明：

- 该预览来自哪个 action guard。
- 该预览对应哪个 read model。
- 该预览为什么只能展示、修复提示、metadata-only、委员会提示、冻结提示或阻断写入提示。
- 用户界面应如何理解该预览的审计含义。
- 哪些动作仍被禁止。

Audit trace preview 只是一层本地解释，不是治理证据，不是审计记录，不是事件记录，也不是状态变更。

## 硬边界

| 边界 | 要求 |
| --- | --- |
| trace preview | 只能用于本地展示和审计解释 |
| audit trace record | 不创建真实 audit trace record |
| EventRecord | 不创建真实 EventRecord |
| ActionReceipt | 不创建真实 ActionReceipt |
| ReadReceipt | 不创建真实 ReadReceipt |
| Harness Evidence | 不创建、不持久化 Harness evidence |
| WAES Gate Result | 不创建 WAES gate result |
| KWE WorkItem | 不创建 KWE work item |
| KDS lifecycle | 不提升、不冻结、不发布、不 accepted |
| GFIS/GPC/ERP/MES | 不写业务系统 |
| 收益/积分/额度/悬赏 | 不确认、不分配、不结算 |
| 外部 API | 不调用真实外部 API |

## 标准链路

```text
DKS-117 event preview
→ DKS-118 audit trace preview
→ UI 展示审计解释
→ 保持 no-write
```

禁止链路：

```text
audit trace preview
→ Harness evidence
→ EventRecord
→ WAES Gate Result
→ KWE WorkItem
→ KDS lifecycle accepted
→ GFIS 正式写回
```

## Trace 类型

| trace_type | 用途 |
| --- | --- |
| display_audit_trace | 展示普通只读预览的审计解释 |
| repair_audit_trace | 展示补证/修复提示的审计解释 |
| metadata_boundary_audit_trace | 展示敏感资料 metadata-only 边界 |
| committee_audit_trace | 展示委员会触发提示，但不完成裁决 |
| freeze_audit_trace | 展示冻结提示，但不执行冻结 |
| blocked_write_audit_trace | 展示写回阻断提示 |

## Trace 状态

| trace_status | 含义 |
| --- | --- |
| trace_preview_only | 仅审计解释预览 |
| blocked_trace_preview | 阻断状态解释预览 |
| metadata_trace_preview | metadata-only 审计边界预览 |
| repair_trace_preview | 修复/补证审计提示预览 |
| committee_trace_preview | 委员会触发审计提示预览 |
| freeze_trace_preview | 冻结风险审计提示预览 |

## Trace 决策

| trace_decision | 含义 |
| --- | --- |
| show_trace_only | 只显示审计解释 |
| show_repair_trace | 显示修复审计提示 |
| show_metadata_boundary_trace | 显示 metadata-only 审计边界 |
| show_committee_trace | 显示委员会审计提示 |
| show_freeze_trace | 显示冻结审计提示 |
| show_blocked_write_trace | 显示写回阻断审计提示 |

## 必填字段

Audit trace preview 必须具备：

- `auditTraceId`
- `eventPreviewRef`
- `actionGuardRef`
- `readModelRef`
- `tenantId`
- `projectId`
- `surface`
- `traceType`
- `traceStatus`
- `traceDecision`
- `traceSummaryRef`
- `lineageHintRefs`
- `reasonRefs`
- `auditNoteRefs`
- `blockedActions`
- 所有 `creates*` 布尔边界字段
- `noWrite`

## 验收

本轮验收只接受本地校验：

```bash
python3 scripts/gfis/validate_gfis_assistant_repair_event_preview_audit_trace.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
tsc -p packages/shared/tsconfig.json --noEmit
tsc -p packages/api/tsconfig.json --noEmit
```

验收通过不代表：

- 真实审计记录已创建。
- Harness evidence 已固化。
- WAES 已通过。
- KWE 工单已生成。
- KDS lifecycle 已提升。
- GFIS/GPC/ERP/MES 已写回。
- 收益、积分、额度、悬赏已确认。
