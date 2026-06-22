import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairReadReceiptNotificationPreviewType =
  | "display_notification_preview"
  | "repair_notification_preview"
  | "metadata_boundary_notification_preview"
  | "committee_notification_preview"
  | "freeze_notification_preview"
  | "blocked_write_notification_preview";

export type GfisAssistantRepairReadReceiptNotificationPreviewStatus =
  | "notification_preview_only"
  | "blocked_notification_preview"
  | "metadata_notification_preview"
  | "repair_notification_preview_status"
  | "committee_notification_preview_status"
  | "freeze_notification_preview_status";

export type GfisAssistantRepairReadReceiptNotificationPreviewDecision =
  | "show_notification_preview_only"
  | "show_repair_notification_preview"
  | "show_metadata_boundary_notification_preview"
  | "show_committee_notification_preview"
  | "show_freeze_notification_preview"
  | "show_blocked_write_notification_preview";

export type GfisAssistantRepairReadReceiptNotificationPreviewBlockedAction =
  | "create_notification"
  | "create_read_receipt"
  | "create_audit_trace_record"
  | "create_event_record"
  | "create_action_receipt"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairReadReceiptNotificationPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesNotification: 0;
  writesReadReceipt: 0;
  writesAuditTraceRecord: 0;
  writesEventRecord: 0;
  writesActionReceipt: 0;
  writesHarnessEvidence: 0;
  writesAdmissionRecord: 0;
  writesReviewQueueItem: 0;
  writesConfirmationRecord: 0;
  writesDecisionRecord: 0;
  writesGapRecord: 0;
  writesBountyRecord: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesEvidenceRecord: 0;
  writesTargetReceipt: 0;
  writesCommitteeDecisionCompletion: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesQuotaTransfer: 0;
  writesBountySettlement: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantRepairReadReceiptNotificationPreview {
  notificationPreviewId: string;
  readReceiptPreviewRef: string;
  auditTraceRef: string;
  eventPreviewRef: string;
  actionGuardRef: string;
  readModelRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  notificationType: GfisAssistantRepairReadReceiptNotificationPreviewType;
  notificationStatus: GfisAssistantRepairReadReceiptNotificationPreviewStatus;
  notificationDecision: GfisAssistantRepairReadReceiptNotificationPreviewDecision;
  notificationSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  notificationNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairReadReceiptNotificationPreviewBlockedAction[];
  createsNotification: false;
  createsReadReceipt: false;
  createsAuditTraceRecord: false;
  createsEventRecord: false;
  createsActionReceipt: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairReadReceiptNotificationPreviewNoWrite;
}

export interface GfisAssistantRepairReadReceiptNotificationPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_read_receipt_notification_preview_policy";
  version: string;
  notificationTypes: GfisAssistantRepairReadReceiptNotificationPreviewType[];
  notificationStatuses: GfisAssistantRepairReadReceiptNotificationPreviewStatus[];
  notificationDecisions: GfisAssistantRepairReadReceiptNotificationPreviewDecision[];
  blockedActions: GfisAssistantRepairReadReceiptNotificationPreviewBlockedAction[];
  hardBoundaries: {
    notificationPreviewOnly: boolean;
    notificationPreviewIsNotNotification: boolean;
    notificationPreviewIsNotReadReceipt: boolean;
    notificationPreviewIsNotAuditTraceRecord: boolean;
    notificationPreviewIsNotEventRecord: boolean;
    notificationPreviewIsNotActionReceipt: boolean;
    notificationPreviewIsNotHarnessEvidence: boolean;
    notificationPreviewIsNotWaesResult: boolean;
    notificationPreviewIsNotKweWorkItem: boolean;
    notificationPreviewIsNotLifecycleChange: boolean;
    notificationPreviewIsNotBusinessWriteback: boolean;
    createsNotificationMustBeFalse: boolean;
    createsReadReceiptMustBeFalse: boolean;
    createsAuditTraceRecordMustBeFalse: boolean;
    createsEventRecordMustBeFalse: boolean;
    createsActionReceiptMustBeFalse: boolean;
    createsHarnessEvidenceMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    completesCommitteeDecisionMustBeFalse: boolean;
  };
  noWriteGuards: GfisAssistantRepairReadReceiptNotificationPreviewNoWrite;
}
