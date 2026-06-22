import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewType =
  | "personal_saved_view_preview"
  | "team_saved_view_preview"
  | "surface_default_view_preview"
  | "blocked_items_saved_view_preview"
  | "committee_saved_view_preview"
  | "freeze_saved_view_preview";

export type GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewStatus =
  | "saved_view_preview_only"
  | "saved_view_contains_blocked_items"
  | "saved_view_contains_retained_items"
  | "saved_view_metadata_boundary"
  | "saved_view_committee_items"
  | "saved_view_freeze_items";

export type GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewDecision =
  | "show_personal_saved_view_preview"
  | "show_team_saved_view_preview"
  | "show_surface_default_view_preview"
  | "show_blocked_items_saved_view_preview"
  | "show_committee_saved_view_preview"
  | "show_freeze_saved_view_preview";

export type GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewScope =
  | "personal"
  | "team"
  | "surface_default"
  | "governance_review";

export type GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewBlockedAction =
  | "create_saved_view"
  | "create_view_preference"
  | "create_filter_state"
  | "create_queue_item"
  | "create_snooze_record"
  | "create_scheduled_reminder"
  | "create_notification"
  | "modify_notification"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesSavedView: 0;
  writesViewPreference: 0;
  writesFilterState: 0;
  writesQueueItem: 0;
  writesSnoozeRecord: 0;
  writesScheduledReminder: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueSavedViewPreview {
  savedViewPreviewId: string;
  filterPreviewRef: string;
  queuePreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  savedViewType: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewType;
  savedViewStatus: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewStatus;
  savedViewDecision: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewDecision;
  sourceFilterPreviewRefs: string[];
  sourceQueuePreviewRefs: string[];
  sourceSnoozePreviewRefs: string[];
  viewScope: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewScope;
  viewSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  viewNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewBlockedAction[];
  createsSavedView: false;
  createsViewPreference: false;
  createsFilterState: false;
  createsQueueItem: false;
  createsSnoozeRecord: false;
  createsScheduledReminder: false;
  createsNotification: false;
  modifiesNotification: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_saved_view_preview_policy";
  version: string;
  savedViewTypes: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewType[];
  savedViewStatuses: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewStatus[];
  savedViewDecisions: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewDecision[];
  viewScopes: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueSavedViewPreviewNoWrite;
}
