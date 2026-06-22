import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozePreviewType =
  | "snooze_display_notification_preview"
  | "snooze_repair_notification_preview"
  | "retain_metadata_boundary_snooze_preview"
  | "retain_committee_snooze_preview"
  | "block_freeze_snooze_preview"
  | "retain_blocked_write_snooze_preview";

export type GfisAssistantRepairNotificationSnoozePreviewStatus =
  | "snooze_preview_only"
  | "deferred_snooze_preview"
  | "retained_snooze_preview"
  | "blocked_snooze_preview"
  | "metadata_boundary_snooze_retained_preview"
  | "freeze_snooze_blocked_preview";

export type GfisAssistantRepairNotificationSnoozePreviewDecision =
  | "show_snooze_preview_only"
  | "show_repair_snooze_preview"
  | "show_metadata_snooze_retained_preview"
  | "show_committee_snooze_retained_preview"
  | "show_freeze_snooze_blocked_preview"
  | "show_blocked_write_snooze_retained_preview";

export type GfisAssistantRepairNotificationSnoozePreviewBlockedAction =
  | "create_snooze_record"
  | "create_scheduled_reminder"
  | "create_dismissal_record"
  | "create_notification"
  | "modify_notification"
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

export interface GfisAssistantRepairNotificationSnoozePreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesSnoozeRecord: 0;
  writesScheduledReminder: 0;
  writesDismissalRecord: 0;
  writesNotification: 0;
  modifiesNotification: 0;
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

export interface GfisAssistantRepairNotificationSnoozePreview {
  snoozePreviewId: string;
  dismissalPreviewRef: string;
  notificationPreviewRef: string;
  readReceiptPreviewRef: string;
  auditTraceRef: string;
  eventPreviewRef: string;
  actionGuardRef: string;
  readModelRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  snoozeType: GfisAssistantRepairNotificationSnoozePreviewType;
  snoozeStatus: GfisAssistantRepairNotificationSnoozePreviewStatus;
  snoozeDecision: GfisAssistantRepairNotificationSnoozePreviewDecision;
  snoozeSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  snoozeNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozePreviewBlockedAction[];
  createsSnoozeRecord: false;
  createsScheduledReminder: false;
  createsDismissalRecord: false;
  createsNotification: false;
  modifiesNotification: false;
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
  noWrite: GfisAssistantRepairNotificationSnoozePreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozePreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_preview_policy";
  version: string;
  snoozeTypes: GfisAssistantRepairNotificationSnoozePreviewType[];
  snoozeStatuses: GfisAssistantRepairNotificationSnoozePreviewStatus[];
  snoozeDecisions: GfisAssistantRepairNotificationSnoozePreviewDecision[];
  blockedActions: GfisAssistantRepairNotificationSnoozePreviewBlockedAction[];
  hardBoundaries: {
    snoozePreviewOnly: boolean;
    snoozePreviewIsNotSnoozeRecord: boolean;
    snoozePreviewIsNotScheduledReminder: boolean;
    snoozePreviewIsNotDismissalRecord: boolean;
    snoozePreviewIsNotNotificationUpdate: boolean;
    snoozePreviewIsNotNotification: boolean;
    snoozePreviewIsNotReadReceipt: boolean;
    snoozePreviewIsNotAuditTraceRecord: boolean;
    snoozePreviewIsNotEventRecord: boolean;
    snoozePreviewIsNotActionReceipt: boolean;
    snoozePreviewIsNotHarnessEvidence: boolean;
    snoozePreviewIsNotWaesResult: boolean;
    snoozePreviewIsNotKweWorkItem: boolean;
    snoozePreviewIsNotLifecycleChange: boolean;
    snoozePreviewIsNotBusinessWriteback: boolean;
    createsSnoozeRecordMustBeFalse: boolean;
    createsScheduledReminderMustBeFalse: boolean;
    createsDismissalRecordMustBeFalse: boolean;
    createsNotificationMustBeFalse: boolean;
    modifiesNotificationMustBeFalse: boolean;
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
  noWriteGuards: GfisAssistantRepairNotificationSnoozePreviewNoWrite;
}
