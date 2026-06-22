import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewType =
  | "team_approval_preview"
  | "project_approval_preview"
  | "governance_review_approval_preview"
  | "external_share_blocked_approval_preview"
  | "committee_approval_preview"
  | "freeze_approval_preview";

export type GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewStatus =
  | "approval_preview_only"
  | "approval_contains_blocked_items"
  | "approval_metadata_boundary"
  | "approval_committee_required"
  | "approval_external_blocked"
  | "approval_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewDecision =
  | "show_team_approval_preview"
  | "show_project_approval_preview"
  | "show_governance_review_approval_preview"
  | "show_external_share_blocked_approval_preview"
  | "show_committee_approval_preview"
  | "show_freeze_approval_preview";

export type GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "committee_review"
  | "external_blocked"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewBlockedAction =
  | "create_approval_request"
  | "create_approval_decision"
  | "create_share_link"
  | "create_acl_grant"
  | "create_external_share_permission"
  | "create_publication_approval"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesApprovalRequest: 0;
  writesApprovalDecision: 0;
  writesShareLink: 0;
  writesAclGrant: 0;
  writesExternalSharePermission: 0;
  writesPublicationApproval: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesHarnessEvidence: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreview {
  approvalPreviewId: string;
  sharePreviewRef: string;
  savedViewPreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  approvalType: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewType;
  approvalStatus: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewStatus;
  approvalDecision: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewDecision;
  approvalScope: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewScope;
  sourceSharePreviewRefs: string[];
  sourceSavedViewPreviewRefs: string[];
  sourceSnoozePreviewRefs: string[];
  approvalSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  approvalNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewBlockedAction[];
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsShareLink: false;
  createsAclGrant: false;
  createsExternalSharePermission: false;
  createsPublicationApproval: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_share_approval_preview_policy";
  version: string;
  approvalTypes: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewType[];
  approvalStatuses: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewStatus[];
  approvalDecisions: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewDecision[];
  approvalScopes: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueShareApprovalPreviewNoWrite;
}
