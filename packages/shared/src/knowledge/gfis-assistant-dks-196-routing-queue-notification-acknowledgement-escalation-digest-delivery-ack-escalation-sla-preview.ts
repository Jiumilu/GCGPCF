import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewType =
  | "team_digest_delivery_ack_escalation_sla_preview"
  | "project_digest_delivery_ack_escalation_sla_preview"
  | "governance_digest_delivery_ack_escalation_sla_preview"
  | "external_blocked_digest_delivery_ack_escalation_sla_preview"
  | "committee_digest_delivery_ack_escalation_sla_preview"
  | "freeze_digest_delivery_ack_escalation_sla_preview";

export type GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewStatus =
  | "sla_preview_only"
  | "sla_at_risk_preview"
  | "sla_metadata_boundary"
  | "sla_external_blocked"
  | "sla_committee_required"
  | "sla_freeze_required";

export type GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewDecision =
  | "show_team_digest_delivery_ack_escalation_sla_preview"
  | "show_project_digest_delivery_ack_escalation_sla_preview"
  | "show_governance_digest_delivery_ack_escalation_sla_preview"
  | "show_external_blocked_digest_delivery_ack_escalation_sla_preview"
  | "show_committee_digest_delivery_ack_escalation_sla_preview"
  | "show_freeze_digest_delivery_ack_escalation_sla_preview";

export type GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewRisk =
  | "within_window_candidate"
  | "at_risk_candidate"
  | "overdue_candidate"
  | "metadata_only_candidate"
  | "external_blocked_candidate"
  | "committee_required_candidate"
  | "freeze_required_candidate";

export type GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewReason =
  | "escalation_sla_missing_ack_candidate"
  | "escalation_sla_at_risk_candidate"
  | "escalation_sla_overdue_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewBlockedAction =
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

export interface GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewNoWrite {
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

export interface GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreview {
  slaPreviewId: string;
  escalationPreviewRefs: string[];
  deliveryAcknowledgementPreviewRefs: string[];
  deliveryPreviewRefs: string[];
  digestPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  slaType: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewType;
  slaStatus: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewStatus;
  slaDecision: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewDecision;
  slaScope: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewScope;
  slaWindowMinutes: number;
  elapsedMinutes: number;
  remainingMinutes: number;
  overdueMinutes: number;
  slaRisk: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewRisk;
  candidateEscalationOwnerRefs: string[];
  slaReasonRefs: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewReason[];
  blockedSlaEscalationCount: number;
  boundaryRefs: string[];
  sourceEscalationPreviewRefs: string[];
  slaSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  slaNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewBlockedAction[];
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
  noWrite: GfisAssistantDks196RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaPreviewNoWrite;
}
