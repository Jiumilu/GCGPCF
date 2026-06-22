import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewType =
  | "team_delivery_ack_escalation_sla_preview"
  | "project_delivery_ack_escalation_sla_preview"
  | "governance_delivery_ack_escalation_sla_preview"
  | "external_blocked_delivery_ack_escalation_sla_preview"
  | "committee_delivery_ack_escalation_sla_preview"
  | "freeze_delivery_ack_escalation_sla_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewStatus =
  | "sla_preview_only"
  | "sla_at_risk_preview"
  | "sla_metadata_boundary"
  | "sla_external_blocked"
  | "sla_committee_required"
  | "sla_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewDecision =
  | "show_team_delivery_ack_escalation_sla_preview"
  | "show_project_delivery_ack_escalation_sla_preview"
  | "show_governance_delivery_ack_escalation_sla_preview"
  | "show_external_blocked_delivery_ack_escalation_sla_preview"
  | "show_committee_delivery_ack_escalation_sla_preview"
  | "show_freeze_delivery_ack_escalation_sla_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewRisk =
  | "within_window_candidate"
  | "at_risk_candidate"
  | "overdue_candidate"
  | "metadata_only_candidate"
  | "external_blocked_candidate"
  | "committee_required_candidate"
  | "freeze_required_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewReason =
  | "escalation_sla_missing_ack_candidate"
  | "escalation_sla_at_risk_candidate"
  | "escalation_sla_overdue_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewBlockedAction =
  | "create_sla_timer"
  | "create_escalation"
  | "create_reminder"
  | "create_escalation_task"
  | "create_delivery_acknowledgement"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesSlaTimer: 0;
  writesEscalation: 0;
  writesReminder: 0;
  writesEscalationTask: 0;
  writesDeliveryAcknowledgement: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreview {
  slaPreviewId: string;
  escalationPreviewRefs: string[];
  deliveryAcknowledgementPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  slaType: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewType;
  slaStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewStatus;
  slaDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewDecision;
  slaScope: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewScope;
  slaWindowMinutes: number;
  elapsedMinutes: number;
  remainingMinutes: number;
  overdueMinutes: number;
  slaRisk: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewRisk;
  candidateEscalationOwnerRefs: string[];
  slaReasonRefs: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewReason[];
  blockedSlaEscalationCount: number;
  boundaryRefs: string[];
  sourceEscalationPreviewRefs: string[];
  slaSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  slaNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewBlockedAction[];
  createsSlaTimer: false;
  createsEscalation: false;
  createsReminder: false;
  createsEscalationTask: false;
  createsDeliveryAcknowledgement: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_acknowledgement_escalation_sla_preview_policy";
  version: string;
  slaTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewType[];
  slaStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewStatus[];
  slaDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewDecision[];
  slaScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewScope[];
  slaRisks: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewRisk[];
  slaReasons: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewReason[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaPreviewNoWrite;
}
