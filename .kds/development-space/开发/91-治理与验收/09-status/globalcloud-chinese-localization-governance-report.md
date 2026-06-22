---
doc_id: GPCF-DOC-6630DBEA9D
title: GlobalCloud 项目群中文化治理报告
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-chinese-localization-governance-report.md
source_path: 09-status/globalcloud-chinese-localization-governance-report.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群中文化治理报告

生成时间：2026-06-22T00:58:11.817793+00:00

中文化门禁：`fail`

## 总览

- 检查文档：1759
- 检查软件/样例文件：240
- 问题总数：367

## 问题类型

- `doc_english_heavy`：62
- `doc_english_line`：304
- `software_english_user_text`：1

## 重点目录

- `docs/harness/loops`：157
- `docs/harness`：114
- `docs/gc-knowledge-fabric`：80
- `openspec/changes`：12
- `docs/codegraph`：1
- `templates/evidence-index-template.md`：1
- `templates/loop-state-template.md`：1
- `packages/api`：1

## 治理判定

- 本报告证明当前项目群存在存量中文化债务。
- 中文化债务应以 `localization_debt=true` 进入 Loop 文档门禁摘要，作为可治理债务持续追踪。
- 中文化债务不等同于文档污染、TOKEN 风险或 KDS 镜像冲突，不单独阻断当前文档门禁。
- 新增或本轮修改内容触发中文化问题时，本轮状态应为 `rework_required`。
- 历史归档允许保留原文，但不得作为当前有效规范复用。

## 样本问题

- `docs/codegraph/codegraph-loop-integration.md:58` `doc_english_line`：- evidence：snapshot、query log、impacted symbols、changed paths。
- `docs/gc-knowledge-fabric/formal-evidence-candidate-packet-assembly-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Candidate Packet Assembly Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-acknowledgement-routing-precheck-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Acknowledgement Routing Precheck Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-envelope-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Envelope Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-completeness-precheck-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Completeness Precheck Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-precheck-repair-request-intake-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Precheck Repair Request Intake Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-delivery-precheck-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Acknowledgement Routing Delivery Precheck Dr
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Acknowledgement Routing Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-completeness-precheck-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Acknowledgement Routing Repair Owner Notific
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Acknowledgement Routing Repair Owner Notific
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Acknowledgement Routing Repair Owner Notific
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Acknowledgement Routing Repair Owner Notific
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-completeness-precheck-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Completeness Precheck Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-intake-acknowledgement-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Aggregation Repair Request Intake Acknowledgement Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Notification Receipt Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-precheck-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Precheck Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-routing-dispatch-precheck-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Routing Dispatch Precheck Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-routing-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Acceptance Acknowledgement Routing Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-case-opening-exception-return-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Case Opening Exception Return Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-case-opening-guard-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Case Opening Guard Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-case-opening-receipt-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Case Opening Receipt Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-case-review-packet-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Case Review Packet Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-docket-readiness-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Docket Readiness Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-intake-acceptance-precheck-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Intake Acceptance Precheck Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-receipt-acknowledgement-routing-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Receipt Acknowledgement Routing Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-review-input-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Review Input Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-committee-trigger-package-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Committee Trigger Package Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-escalation-digest-human-confirmation-package-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Escalation Digest Human Confirmation Package Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-evidence-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Evidence Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-exception-return-supplement-intake-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Exception Return Supplement Intake Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-incident-escalation-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Incident Escalation Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-incident-escalation-preview-dry-run-v0.1.md:66` `doc_english_line`：- freeze request packet、human review packet、committee review packet、stop authority packet。
- `docs/gc-knowledge-fabric/formal-evidence-execution-incident-escalation-preview-dry-run-v0.1.md:71` `doc_english_line`：- incident not written、freeze not executed、no write boundary。
- `docs/gc-knowledge-fabric/formal-evidence-execution-notification-acknowledgement-receipt-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Notification Acknowledgement Receipt Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-notification-acknowledgement-receipt-routing-acknowledgement-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Notification Acknowledgement Receipt Routing Acknowledgement Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-reentry-approval-packet-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Re-entry Approval Packet Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-reentry-preflight-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Re-entry Preflight Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-reentry-preflight-preview-dry-run-v0.1.md:43` `doc_english_line`：- repair or reopen work item、repair evidence packet、repair evidence shape。
- `docs/gc-knowledge-fabric/formal-evidence-execution-reentry-preflight-preview-dry-run-v0.1.md:44` `doc_english_line`：- human repair review、committee repair review、stop authority release packet。
- `docs/gc-knowledge-fabric/formal-evidence-execution-repair-request-acknowledgement-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Repair Request Acknowledgement Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-repair-request-intake-completeness-precheck-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Repair Request Intake Completeness Precheck Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-repair-response-deadline-monitor-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Repair Response Deadline Monitor Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-reviewer-acceptance-acknowledgement-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Reviewer Acceptance Acknowledgement Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-reviewer-acceptance-acknowledgement-routing-package-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Reviewer Acceptance Acknowledgement Routing Package Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-reviewer-acknowledgement-routing-receipt-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Reviewer Acknowledgement Routing Receipt Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-reviewer-assignment-acknowledgement-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Reviewer Assignment Acknowledgement Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-rollback-drill-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Rollback Drill Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-routing-package-acknowledgement-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Routing Package Acknowledgement Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-routing-package-intake-guard-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Routing Package Intake Guard Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-routing-receipt-reviewer-acceptance-precheck-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Routing Receipt Reviewer Acceptance Precheck Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-routing-reviewer-assignment-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Routing Reviewer Assignment Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-signer-receipt-escalation-digest-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Signer Receipt Escalation Digest Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-signer-receipt-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Signer Receipt Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-supplement-completeness-precheck-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Supplement Completeness Precheck Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-supplement-precheck-repair-request-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Supplement Precheck Repair Request Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-execution-verification-plan-preview-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Execution Verification Plan Preview Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-final-execution-guard-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Final Execution Guard Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-final-execution-request-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Final Execution Request Dry-run v0.1
- `docs/gc-knowledge-fabric/formal-evidence-write-action-guard-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Formal Evidence Write Action Guard Dry-run v0.1
- `docs/gc-knowledge-fabric/future-formal-write-execution-preflight-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Future Formal Write Execution Preflight Dry-run v0.1
- `docs/gc-knowledge-fabric/gfis-assistant-dks-243-digest-delivery-acknowledgement-escalation-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-243 Digest Delivery Acknowledgement Escalation Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-244-digest-delivery-acknowledgement-escalation-sla-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-244 Digest Delivery Acknowledgement Escalation SLA Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-255-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-255 Digest Delivery Acknowledgement Escalation Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-256-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-256 Digest Delivery Acknowledgement Escalation SLA Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-257-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-257 Digest Delivery Acknowledgement Escalation SLA Breach Review Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-258-ack-escalation-sla-breach-review-resolution-option-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-258 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-259-ack-escalation-sla-breach-review-resolution-option-approval-packet-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-259 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-260-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-260 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-261-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-261 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Notification Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-262-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-262 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Notification Ack Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-263-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-263 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Notification Ack Escalation Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-264-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-264 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Notification Ack Escalation Digest Preview Pol
- `docs/gc-knowledge-fabric/gfis-assistant-dks-265-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-265 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Notification Ack Escalation Digest Delivery Pr
- `docs/gc-knowledge-fabric/gfis-assistant-dks-266-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-266 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Notification Ack Escalation Digest Delivery Ac
- `docs/gc-knowledge-fabric/gfis-assistant-dks-267-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-267 Digest Delivery Acknowledgement Escalation SLA Breach Review Resolution Option Approval Packet Routing Queue Notification Ack Escalation Digest Delivery Ac
- `docs/gc-knowledge-fabric/gfis-assistant-dks-268-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-268 Digest Delivery Acknowledgement Escalation SLA Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-270-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-270 SLA Breach Review Resolution Option Preview Policy
- `docs/gc-knowledge-fabric/gfis-assistant-dks-271-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-preview-policy.md:19` `doc_english_line`：# GFIS Assistant DKS-271 Resolution Option Approval Packet Preview Policy
- `docs/gc-knowledge-fabric/harness-governance-review-decision-intake-dry-run-v0.1.md:19` `doc_english_line`：# GC-Knowledge Fabric P0 Harness Governance Review Decision Intake Dry-run v0.1
- `docs/harness/GPC/loops/loop-round-GPCF-GP-LR-002.md:1` `doc_english_heavy`：english_words=16 chinese_chars=7
- `docs/harness/GPC/loops/loop-round-GPCF-GP-LR-002.md:46` `doc_english_line`：Current state remains `partial`; this round does not write the GPC blueprint, change architecture conclusions, or mark accepted/integrated.
- `docs/harness/MMC/loops/loop-round-GPCF-MM-LR-002.md:1` `doc_english_heavy`：english_words=18 chinese_chars=8
- `docs/harness/MMC/loops/loop-round-GPCF-MM-LR-002.md:49` `doc_english_line`：Current state remains `partial`; this round only creates a controlled governance dictionary and does not mark any project accepted/integrated.
- `docs/harness/PVAOS/loops/loop-round-GPCF-PV-LR-002.md:1` `doc_english_heavy`：english_words=15 chinese_chars=4
- `docs/harness/PVAOS/loops/loop-round-GPCF-PV-LR-002.md:46` `doc_english_line`：Current state remains `partial`; this round does not deploy PVAOS, write a real project repository, or mark accepted/integrated.
- `docs/harness/WAES/loops/loop-round-GPCF-WA-LR-002.md:1` `doc_english_heavy`：english_words=17 chinese_chars=4
- `docs/harness/WAES/loops/loop-round-GPCF-WA-LR-002.md:46` `doc_english_line`：Current state remains `partial`; this round does not change WAES authority, accepted/integrated status, production configuration, or real project repository.
- `docs/harness/XiaoG/loops/loop-round-GPCF-XG-LR-002.md:1` `doc_english_heavy`：english_words=16 chinese_chars=4
- `docs/harness/XiaoG/loops/loop-round-GPCF-XG-LR-002.md:46` `doc_english_line`：Current state remains `partial`; this round does not touch devices, production, real external APIs, or mark accepted/integrated.
- `docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md:1` `doc_english_heavy`：english_words=70 chinese_chars=4
- `docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md:73` `doc_english_line`：- All writeback rows are candidate-only and require manual or committee confirmation.
- `docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md:74` `doc_english_line`：- No real KDS API, WAES write, GFIS/GPC/PVAOS business ledger write, RAG admission, settlement, bounty release, revenue allocation, or AI quota allocation is performed.
- `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md:1` `doc_english_heavy`：english_words=81 chinese_chars=4
- `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md:25` `doc_english_line`：This queue contains hard-stop writeback candidates that require committee review before any downstream action.
- `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md:67` `doc_english_line`：- Queue rows are candidate-only and do not confirm facts, close gaps, or write any system.
- `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md:1` `doc_english_heavy`：english_words=86 chinese_chars=4
- `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md:25` `doc_english_line`：This schema defines the fields required for future committee review of hard-stop base knowledge candidates.
- `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md:72` `doc_english_line`：- This file defines schema only and does not create human confirmation facts.
- `docs/harness/evidence/base-knowledge-committee-review-template-20260619.md:1` `doc_english_heavy`：english_words=73 chinese_chars=4
- `docs/harness/evidence/base-knowledge-committee-review-template-20260619.md:25` `doc_english_line`：This file provides blank records for future committee review based on the DKS-046 committee review schema.
- `docs/harness/evidence/base-knowledge-committee-review-template-20260619.md:66` `doc_english_line`：- Blank records are templates only and contain no real confirmation or committee decision.
- `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md:1` `doc_english_heavy`：english_words=82 chinese_chars=4
- `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md:25` `doc_english_line`：This queue contains non-hard-stop writeback candidates that still require human confirmation before any downstream action.
- `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md:61` `doc_english_line`：- Queue rows are candidate-only and do not confirm facts, close gaps, or write any system.
- `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md:1` `doc_english_heavy`：english_words=86 chinese_chars=4
- `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md:25` `doc_english_line`：This schema defines the fields required for future manual confirmation of non-hard-stop base knowledge candidates.
- `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md:70` `doc_english_line`：- This file defines schema only and does not create human confirmation facts.
- `docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md:1` `doc_english_heavy`：english_words=73 chinese_chars=4
- `docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md:25` `doc_english_line`：This file provides blank records for future manual confirmation based on the DKS-046 human confirmation schema.
- `docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md:60` `doc_english_line`：- Blank records are templates only and contain no real confirmation or committee decision.
- `docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md:1` `doc_english_heavy`：english_words=44 chinese_chars=4
- `docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md:47` `doc_english_line`：- Candidate rows do not create score settlement, revenue allocation, bounty publication, RAG admission, command-center strong reference, or business ledger writes.
- `docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md:48` `doc_english_line`：- Candidate rows must be confirmed by the proper human, KDS, WAES, or committee process before any downstream action.
- `docs/harness/evidence/codegraph-sync-authorization-pack-20260621.md:25` `doc_english_line`：Boundary note: this round does not execute Brain/Studio sync-only closure.
- `docs/harness/evidence/evidence-index.md:1` `doc_english_heavy`：english_words=1983 chinese_chars=914
- `docs/harness/evidence/evidence-index.md:91` `doc_english_line`：- Headroom LCX P3 learn preview working memory gate evidence: `docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.md`
- `docs/harness/evidence/evidence-index.md:93` `doc_english_line`：- Headroom LCX P3 learn preview working memory gate runner: `tools/kds-sync/run_headroom_lcx_p3_learn_preview_working_memory_gate.py`
- `docs/harness/evidence/gfis-owner-receipt-task-ledger-20260617.md:1` `doc_english_heavy`：english_words=26 chinese_chars=0
