import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewType =
  | "team_route_preview"
  | "project_route_preview"
  | "governance_route_preview"
  | "external_blocked_route_preview"
  | "committee_route_preview"
  | "freeze_route_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewStatus =
  | "route_preview_only"
  | "route_contains_blocked_items"
  | "route_metadata_boundary"
  | "route_committee_required"
  | "route_external_blocked"
  | "route_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewDecision =
  | "show_team_route_preview"
  | "show_project_route_preview"
  | "show_governance_route_preview"
  | "show_external_blocked_route_preview"
  | "show_committee_route_preview"
  | "show_freeze_route_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "committee_review"
  | "external_blocked"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewBlockedAction =
  | "create_approval_route"
  | "create_route_step"
  | "assign_approver"
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesApprovalRoute: 0;
  writesRouteStep: 0;
  writesApproverAssignment: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreview {
  routePreviewId: string;
  approvalPreviewRef: string;
  sharePreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  routeType: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewType;
  routeStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewStatus;
  routeDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewDecision;
  routeScope: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewScope;
  routeStepRefs: string[];
  sourceApprovalPreviewRefs: string[];
  sourceSharePreviewRefs: string[];
  sourceSnoozePreviewRefs: string[];
  routeSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  routeNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewBlockedAction[];
  createsApprovalRoute: false;
  createsRouteStep: false;
  assignsApprover: false;
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_route_preview_policy";
  version: string;
  routeTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewType[];
  routeStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewStatus[];
  routeDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewDecision[];
  routeScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalRoutePreviewNoWrite;
}
