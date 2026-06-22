import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationDismissalPreviewType =
  | "dismiss_display_notification_preview"
  | "defer_repair_notification_preview"
  | "retain_metadata_boundary_notification_preview"
  | "retain_committee_notification_preview"
  | "block_freeze_notification_dismissal_preview"
  | "retain_blocked_write_notification_preview";

export type GfisAssistantRepairNotificationDismissalPreviewStatus =
  | "dismissal_preview_only"
  | "deferred_dismissal_preview"
  | "retained_notification_preview"
  | "blocked_dismissal_preview"
  | "metadata_boundary_retained_preview"
  | "freeze_dismissal_blocked_preview";

export type GfisAssistantRepairNotificationDismissalPreviewDecision =
  | "show_dismissal_preview_only"
  | "show_defer_repair_preview"
  | "show_metadata_retained_preview"
  | "show_committee_retained_preview"
  | "show_freeze_dismissal_blocked_preview"
  | "show_blocked_write_retained_preview";

export type GfisAssistantRepairNotificationDismissalPreviewBlockedAction =
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

export interface GfisAssistantRepairNotificationDismissalPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
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

export interface GfisAssistantRepairNotificationDismissalPreview {
  dismissalPreviewId: string;
  notificationPreviewRef: string;
  readReceiptPreviewRef: string;
  auditTraceRef: string;
  eventPreviewRef: string;
  actionGuardRef: string;
  readModelRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  dismissalType: GfisAssistantRepairNotificationDismissalPreviewType;
  dismissalStatus: GfisAssistantRepairNotificationDismissalPreviewStatus;
  dismissalDecision: GfisAssistantRepairNotificationDismissalPreviewDecision;
  dismissalSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  dismissalNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationDismissalPreviewBlockedAction[];
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
  noWrite: GfisAssistantRepairNotificationDismissalPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationDismissalPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_dismissal_preview_policy";
  version: string;
  dismissalTypes: GfisAssistantRepairNotificationDismissalPreviewType[];
  dismissalStatuses: GfisAssistantRepairNotificationDismissalPreviewStatus[];
  dismissalDecisions: GfisAssistantRepairNotificationDismissalPreviewDecision[];
  blockedActions: GfisAssistantRepairNotificationDismissalPreviewBlockedAction[];
  hardBoundaries: {
    dismissalPreviewOnly: boolean;
    dismissalPreviewIsNotDismissalRecord: boolean;
    dismissalPreviewIsNotNotificationUpdate: boolean;
    dismissalPreviewIsNotNotification: boolean;
    dismissalPreviewIsNotReadReceipt: boolean;
    dismissalPreviewIsNotAuditTraceRecord: boolean;
    dismissalPreviewIsNotEventRecord: boolean;
    dismissalPreviewIsNotActionReceipt: boolean;
    dismissalPreviewIsNotHarnessEvidence: boolean;
    dismissalPreviewIsNotWaesResult: boolean;
    dismissalPreviewIsNotKweWorkItem: boolean;
    dismissalPreviewIsNotLifecycleChange: boolean;
    dismissalPreviewIsNotBusinessWriteback: boolean;
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
  noWriteGuards: GfisAssistantRepairNotificationDismissalPreviewNoWrite;
}
