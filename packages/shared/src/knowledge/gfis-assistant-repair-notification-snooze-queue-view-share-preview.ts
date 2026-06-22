import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewType =
  | "personal_to_team_share_preview"
  | "team_to_project_share_preview"
  | "surface_default_share_preview"
  | "governance_review_share_preview"
  | "external_share_blocked_preview"
  | "committee_share_preview";

export type GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewStatus =
  | "share_preview_only"
  | "share_contains_blocked_items"
  | "share_contains_retained_items"
  | "share_metadata_boundary"
  | "share_committee_items"
  | "share_external_blocked";

export type GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewDecision =
  | "show_personal_to_team_share_preview"
  | "show_team_to_project_share_preview"
  | "show_surface_default_share_preview"
  | "show_governance_review_share_preview"
  | "show_external_share_blocked_preview"
  | "show_committee_share_preview";

export type GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewScope =
  | "team_internal"
  | "project_internal"
  | "surface_default"
  | "governance_review"
  | "external_blocked";

export type GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewBlockedAction =
  | "create_share_link"
  | "create_acl_grant"
  | "create_external_share_permission"
  | "create_publication_approval"
  | "create_saved_view"
  | "create_view_preference"
  | "create_filter_state"
  | "create_notification"
  | "modify_notification"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesShareLink: 0;
  writesAclGrant: 0;
  writesExternalSharePermission: 0;
  writesPublicationApproval: 0;
  writesSavedView: 0;
  writesViewPreference: 0;
  writesFilterState: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueViewSharePreview {
  sharePreviewId: string;
  savedViewPreviewRef: string;
  filterPreviewRef: string;
  queuePreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  shareType: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewType;
  shareStatus: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewStatus;
  shareDecision: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewDecision;
  shareScope: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewScope;
  sourceSavedViewPreviewRefs: string[];
  sourceFilterPreviewRefs: string[];
  sourceQueuePreviewRefs: string[];
  sourceSnoozePreviewRefs: string[];
  shareSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  shareNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewBlockedAction[];
  createsShareLink: false;
  createsAclGrant: false;
  createsExternalSharePermission: false;
  createsPublicationApproval: false;
  createsSavedView: false;
  createsViewPreference: false;
  createsFilterState: false;
  createsNotification: false;
  modifiesNotification: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_view_share_preview_policy";
  version: string;
  shareTypes: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewType[];
  shareStatuses: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewStatus[];
  shareDecisions: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewDecision[];
  shareScopes: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueViewSharePreviewNoWrite;
}
