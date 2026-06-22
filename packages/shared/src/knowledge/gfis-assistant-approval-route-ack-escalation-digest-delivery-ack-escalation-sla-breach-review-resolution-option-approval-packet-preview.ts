import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewType =
  | "team_digest_delivery_ack_escalation_approval_packet_preview"
  | "project_digest_delivery_ack_escalation_approval_packet_preview"
  | "governance_digest_delivery_ack_escalation_approval_packet_preview"
  | "external_blocked_digest_delivery_ack_escalation_approval_packet_preview"
  | "committee_digest_delivery_ack_escalation_approval_packet_preview"
  | "freeze_digest_delivery_ack_escalation_approval_packet_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewStatus =
  | "approval_packet_preview_only"
  | "approval_packet_evidence_required"
  | "approval_packet_metadata_boundary"
  | "approval_packet_external_blocked"
  | "approval_packet_committee_required"
  | "approval_packet_freeze_required";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewDecision =
  | "show_team_digest_delivery_ack_escalation_approval_packet_preview"
  | "show_project_digest_delivery_ack_escalation_approval_packet_preview"
  | "show_governance_digest_delivery_ack_escalation_approval_packet_preview"
  | "show_external_blocked_digest_delivery_ack_escalation_approval_packet_preview"
  | "show_committee_digest_delivery_ack_escalation_approval_packet_preview"
  | "show_freeze_digest_delivery_ack_escalation_approval_packet_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewRoute =
  | "team_lead_candidate"
  | "project_owner_candidate"
  | "governance_reviewer_candidate"
  | "external_share_blocked_candidate"
  | "committee_candidate"
  | "freeze_reviewer_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewReason =
  | "resolution_option_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewBlockedAction =
  | "create_approval_packet"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_committee_decision"
  | "create_freeze_action"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesApprovalPacket: 0;
  writesApprovalRequest: 0;
  writesApprovalDecision: 0;
  writesCommitteeDecision: 0;
  writesFreezeAction: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesHarnessEvidence: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreview {
  approvalPacketPreviewId: string;
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  slaPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  approvalPacketType: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewType;
  approvalPacketStatus: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewStatus;
  approvalPacketDecision: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewDecision;
  approvalPacketScope: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewScope;
  approvalRoute: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewRoute;
  candidateApproverRefs: string[];
  requiredEvidenceRefs: string[];
  approvalReasonRefs: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewReason[];
  blockedApprovalCount: number;
  boundaryRefs: string[];
  sourceResolutionOptionPreviewRefs: string[];
  approvalSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  approvalNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewBlockedAction[];
  createsApprovalPacket: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsCommitteeDecision: false;
  createsFreezeAction: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewNoWrite;
}
