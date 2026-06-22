---
doc_id: GPCF-DOC-E53A07CE0C
title: GFIS Assistant Repair Notification Snooze Queue Approval Route Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-route-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-repair-notification-snooze-queue-approval-route-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant Repair Notification Snooze Queue Approval Route Preview No-write 规则

## 1. 定位

本规则定义 GFIS Assistant repair notification snooze queue 的审批路由预览边界。

审批路由预览只描述从 DKS-127 share approval preview 派生出的候选审批路径，用于 Brain、PKC、GFIS Assistant 展示可能的团队、项目、治理、委员会、冻结或外部阻断路由。

审批路由预览不是正式审批路线，不创建审批请求，不分配审批人，不创建审批决定，不写 ACL，不创建外部共享权限，不生成 Harness evidence，不修改 KDS lifecycle，不触发 GFIS/GPC/ERP/MES 写回。

## 2. 输入

- DKS-127 share approval preview 引用。
- DKS-126 view share preview 引用。
- DKS-122 至 DKS-125 snooze queue 预览引用。
- KWE approval route packet 规则引用。
- Committee policy 与外部共享阻断规则引用。

## 3. 输出

每条审批路由预览必须包含：

- routePreviewId。
- approvalPreviewRef。
- sharePreviewRef。
- routeType。
- routeStatus。
- routeDecision。
- routeScope。
- routeStepRefs。
- reasonRefs。
- routeNoteRefs。
- blockedActions。
- noWrite。

## 4. 路由类型

- team_route_preview：团队内部审批路由预览。
- project_route_preview：项目内部审批路由预览。
- governance_route_preview：治理审阅路由预览。
- external_blocked_route_preview：外部共享被阻断的路由预览。
- committee_route_preview：委员会审查路由预览。
- freeze_route_preview：冻结审查路由预览。

## 5. 硬边界

审批路由预览必须满足：

- createsApprovalRoute = false。
- createsRouteStep = false。
- assignsApprover = false。
- createsApprovalRequest = false。
- createsApprovalDecision = false。
- createsShareLink = false。
- createsAclGrant = false。
- createsExternalSharePermission = false。
- createsPublicationApproval = false。
- createsHarnessEvidence = false。
- createsWaesGateResult = false。
- createsKweWorkItem = false。
- persistsEvidence = false。
- approvesBusinessWrite = false。
- promotesLifecycle = false。
- completesCommitteeDecision = false。

## 6. No-write 守卫

以下写入计数必须全部为 0：

- writesGfis / writesGpc / writesErp / writesMes。
- writesApprovalRoute / writesRouteStep / writesApproverAssignment。
- writesApprovalRequest / writesApprovalDecision。
- writesShareLink / writesAclGrant / writesExternalSharePermission。
- writesPublicationApproval。
- writesWaesGateResult / writesKweWorkItem / writesHarnessEvidence。
- writesKdsLifecycle / writesKdsFact / writesKdsAcceptedFact。
- writesExternalApi。

## 7. 验收

本规则由以下文件共同验证：

- `okf/gfis-assistant-repair-notification-snooze-queue-approval-route-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-repair-notification-snooze-queue-approval-route-preview.ts`
- `fixtures/gfis/repair-notification-snooze-queue-approval-route-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_repair_notification_snooze_queue_approval_route_preview.py`

通过条件：

- 6 条预览覆盖 Brain、PKC、GFIS Assistant。
- 6 类 routeType、routeStatus、routeScope 均被覆盖。
- 所有创建、分配、审批、写回、证据、状态提升字段均为 false。
- 所有 noWrite 计数均为 0。
