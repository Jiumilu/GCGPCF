import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewType =
  | "watch_escalation_preview"
  | "urgent_escalation_preview"
  | "governance_escalation_preview"
  | "external_blocked_escalation_preview"
  | "committee_escalation_preview"
  | "freeze_escalation_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewStatus =
  | "escalation_preview_only"
  | "escalation_at_risk_preview"
  | "escalation_metadata_boundary"
  | "escalation_external_blocked"
  | "escalation_committee_required"
  | "escalation_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewDecision =
  | "show_watch_escalation_preview"
  | "show_urgent_escalation_preview"
  | "show_governance_escalation_preview"
  | "show_external_blocked_escalation_preview"
  | "show_committee_escalation_preview"
  | "show_freeze_escalation_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewBlockedAction =
  | "create_escalation_schedule"
  | "create_escalation_task"
  | "assign_escalation_owner"
  | "create_reminder"
  | "create_approval_route"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesEscalationSchedule: 0;
  writesEscalationTask: 0;
  writesEscalationOwner: 0;
  writesReminder: 0;
  writesApprovalRoute: 0;
  writesApprovalRequest: 0;
  writesApprovalDecision: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesHarnessEvidence: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreview {
  escalationPreviewId: string;
  slaPreviewRef: string;
  routePreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  escalationType: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewType;
  escalationStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewStatus;
  escalationDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewDecision;
  escalationScope: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewScope;
  escalationLevel: "watch" | "urgent" | "governance" | "committee" | "freeze";
  candidateOwnerRefs: string[];
  responsibilityBoundaryRefs: string[];
  sourceSlaPreviewRefs: string[];
  sourceRoutePreviewRefs: string[];
  escalationSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  escalationNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewBlockedAction[];
  createsEscalationSchedule: false;
  createsEscalationTask: false;
  assignsEscalationOwner: false;
  createsReminder: false;
  createsApprovalRoute: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_sla_escalation_preview_policy";
  version: string;
  escalationTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewType[];
  escalationStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewStatus[];
  escalationDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewDecision[];
  escalationScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaEscalationPreviewNoWrite;
}
