import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueuePreviewType =
  | "brain_snooze_queue_preview"
  | "pkc_snooze_queue_preview"
  | "gfis_assistant_snooze_queue_preview";

export type GfisAssistantRepairNotificationSnoozeQueuePreviewStatus =
  | "queue_preview_only"
  | "queue_contains_blocked_items"
  | "queue_contains_retained_items";

export type GfisAssistantRepairNotificationSnoozeQueuePreviewDecision =
  | "show_brain_snooze_queue_preview"
  | "show_pkc_snooze_queue_preview"
  | "show_gfis_assistant_snooze_queue_preview";

export type GfisAssistantRepairNotificationSnoozeQueuePreviewBlockedAction =
  | "create_queue_item"
  | "create_snooze_record"
  | "create_scheduled_reminder"
  | "create_dismissal_record"
  | "create_notification"
  | "modify_notification"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueuePreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesQueueItem: 0;
  writesSnoozeRecord: 0;
  writesScheduledReminder: 0;
  writesDismissalRecord: 0;
  writesNotification: 0;
  modifiesNotification: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesHarnessEvidence: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantRepairNotificationSnoozeQueuePreview {
  queuePreviewId: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  queueType: GfisAssistantRepairNotificationSnoozeQueuePreviewType;
  queueStatus: GfisAssistantRepairNotificationSnoozeQueuePreviewStatus;
  queueDecision: GfisAssistantRepairNotificationSnoozeQueuePreviewDecision;
  sourceSnoozePreviewRefs: string[];
  orderedSnoozePreviewRefs: string[];
  queueSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  queueNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueuePreviewBlockedAction[];
  createsQueueItem: false;
  createsSnoozeRecord: false;
  createsScheduledReminder: false;
  createsDismissalRecord: false;
  createsNotification: false;
  modifiesNotification: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueuePreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueuePreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_preview_policy";
  version: string;
  queueTypes: GfisAssistantRepairNotificationSnoozeQueuePreviewType[];
  queueStatuses: GfisAssistantRepairNotificationSnoozeQueuePreviewStatus[];
  queueDecisions: GfisAssistantRepairNotificationSnoozeQueuePreviewDecision[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueuePreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueuePreviewNoWrite;
}
