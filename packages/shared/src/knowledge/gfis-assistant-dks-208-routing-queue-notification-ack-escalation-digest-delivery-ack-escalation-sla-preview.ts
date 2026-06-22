import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewType =
  | "team_digest_delivery_ack_escalation_sla_preview"
  | "project_digest_delivery_ack_escalation_sla_preview"
  | "governance_digest_delivery_ack_escalation_sla_preview"
  | "external_blocked_digest_delivery_ack_escalation_sla_preview"
  | "committee_digest_delivery_ack_escalation_sla_preview"
  | "freeze_digest_delivery_ack_escalation_sla_preview";

export type GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewStatus =
  | "sla_preview_only"
  | "sla_at_risk_preview"
  | "sla_metadata_boundary"
  | "sla_external_blocked"
  | "sla_committee_required"
  | "sla_freeze_required";

export type GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewDecision =
  | "show_team_digest_delivery_ack_escalation_sla_preview"
  | "show_project_digest_delivery_ack_escalation_sla_preview"
  | "show_governance_digest_delivery_ack_escalation_sla_preview"
  | "show_external_blocked_digest_delivery_ack_escalation_sla_preview"
  | "show_committee_digest_delivery_ack_escalation_sla_preview"
  | "show_freeze_digest_delivery_ack_escalation_sla_preview";

export type GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewRisk =
  | "within_window_candidate"
  | "at_risk_candidate"
  | "overdue_candidate"
  | "metadata_only_candidate"
  | "external_blocked_candidate"
  | "committee_required_candidate"
  | "freeze_required_candidate";

export type GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewReason =
  | "escalation_sla_missing_ack_candidate"
  | "escalation_sla_at_risk_candidate"
  | "escalation_sla_overdue_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewBlockedAction =
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

export interface GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewNoWrite {
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

export interface GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreview {
  slaPreviewId: string;
  escalationPreviewRefs: string[];
  deliveryAcknowledgementPreviewRefs: string[];
  deliveryPreviewRefs: string[];
  digestPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  slaType: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewType;
  slaStatus: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewStatus;
  slaDecision: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewDecision;
  slaScope: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewScope;
  slaWindowMinutes: number;
  elapsedMinutes: number;
  remainingMinutes: number;
  overdueMinutes: number;
  slaRisk: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewRisk;
  candidateEscalationOwnerRefs: string[];
  slaReasonRefs: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewReason[];
  requiredEvidenceRefs: string[];
  blockedSlaEscalationCount: number;
  boundaryRefs: string[];
  sourceEscalationPreviewRefs: string[];
  slaSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  slaNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewBlockedAction[];
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
  noWrite: GfisAssistantDks208RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaPreviewNoWrite;
}
