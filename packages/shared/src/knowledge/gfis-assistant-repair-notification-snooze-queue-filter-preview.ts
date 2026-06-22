import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueFilterPreviewType =
  | "surface_filter_preview"
  | "blocked_items_filter_preview"
  | "retained_items_filter_preview"
  | "metadata_boundary_filter_preview"
  | "committee_filter_preview"
  | "freeze_filter_preview";

export type GfisAssistantRepairNotificationSnoozeQueueFilterPreviewStatus =
  | "filter_preview_only"
  | "filter_contains_blocked_items"
  | "filter_contains_retained_items"
  | "filter_metadata_boundary"
  | "filter_committee_items"
  | "filter_freeze_items";

export type GfisAssistantRepairNotificationSnoozeQueueFilterPreviewDecision =
  | "show_surface_filter_preview"
  | "show_blocked_items_filter_preview"
  | "show_retained_items_filter_preview"
  | "show_metadata_boundary_filter_preview"
  | "show_committee_filter_preview"
  | "show_freeze_filter_preview";

export type GfisAssistantRepairNotificationSnoozeQueueFilterPreviewBlockedAction =
  | "create_filter_state"
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

export interface GfisAssistantRepairNotificationSnoozeQueueFilterPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesFilterState: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueFilterPreview {
  filterPreviewId: string;
  queuePreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  filterType: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewType;
  filterStatus: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewStatus;
  filterDecision: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewDecision;
  sourceQueuePreviewRefs: string[];
  sourceSnoozePreviewRefs: string[];
  filteredSnoozePreviewRefs: string[];
  filterSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  filterNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewBlockedAction[];
  createsFilterState: false;
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueFilterPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_filter_preview_policy";
  version: string;
  filterTypes: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewType[];
  filterStatuses: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewStatus[];
  filterDecisions: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewDecision[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueFilterPreviewNoWrite;
}
