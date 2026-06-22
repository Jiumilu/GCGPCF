import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewType =
  | "standard_sla_preview"
  | "urgent_sla_preview"
  | "governance_sla_preview"
  | "external_blocked_sla_preview"
  | "committee_sla_preview"
  | "freeze_sla_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewStatus =
  | "sla_preview_only"
  | "sla_at_risk_preview"
  | "sla_metadata_boundary"
  | "sla_external_blocked"
  | "sla_committee_required"
  | "sla_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewDecision =
  | "show_standard_sla_preview"
  | "show_urgent_sla_preview"
  | "show_governance_sla_preview"
  | "show_external_blocked_sla_preview"
  | "show_committee_sla_preview"
  | "show_freeze_sla_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewBlockedAction =
  | "create_sla_timer"
  | "create_reminder"
  | "schedule_escalation"
  | "assign_escalation_owner"
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesSlaTimer: 0;
  writesReminder: 0;
  writesEscalationSchedule: 0;
  writesEscalationOwner: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreview {
  slaPreviewId: string;
  routePreviewRef: string;
  approvalPreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  slaType: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewType;
  slaStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewStatus;
  slaDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewDecision;
  slaScope: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewScope;
  dueWindowMinutes: number;
  elapsedMinutes: number;
  remainingMinutes: number;
  escalationLevel: "none" | "watch" | "urgent" | "committee" | "freeze";
  sourceRoutePreviewRefs: string[];
  sourceApprovalPreviewRefs: string[];
  sourceSnoozePreviewRefs: string[];
  slaSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  slaNoteRefs: string[];
  escalationCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewBlockedAction[];
  createsSlaTimer: false;
  createsReminder: false;
  schedulesEscalation: false;
  assignsEscalationOwner: false;
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_sla_preview_policy";
  version: string;
  slaTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewType[];
  slaStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewStatus[];
  slaDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewDecision[];
  slaScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalSlaPreviewNoWrite;
}
