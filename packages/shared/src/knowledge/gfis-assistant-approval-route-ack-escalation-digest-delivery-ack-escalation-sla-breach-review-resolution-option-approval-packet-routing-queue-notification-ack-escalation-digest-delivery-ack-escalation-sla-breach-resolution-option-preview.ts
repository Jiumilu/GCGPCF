import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewType =
  | "team_digest_delivery_ack_escalation_resolution_option_preview"
  | "project_digest_delivery_ack_escalation_resolution_option_preview"
  | "governance_digest_delivery_ack_escalation_resolution_option_preview"
  | "external_blocked_digest_delivery_ack_escalation_resolution_option_preview"
  | "committee_digest_delivery_ack_escalation_resolution_option_preview"
  | "freeze_digest_delivery_ack_escalation_resolution_option_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewStatus =
  | "resolution_option_preview_only"
  | "resolution_option_evidence_required"
  | "resolution_option_metadata_boundary"
  | "resolution_option_external_blocked"
  | "resolution_option_committee_required"
  | "resolution_option_freeze_required";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewDecision =
  | "show_team_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_project_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_governance_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_external_blocked_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_committee_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_freeze_digest_delivery_ack_escalation_resolution_option_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewPriority =
  | "p3_candidate"
  | "p2_candidate"
  | "p1_candidate"
  | "metadata_only_candidate"
  | "external_blocked_candidate"
  | "committee_required_candidate"
  | "freeze_required_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewReason =
  | "supplement_delivery_ack_candidate"
  | "repair_evidence_gap_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewBlockedAction =
  | "create_resolution"
  | "create_dispute_update"
  | "create_committee_decision"
  | "create_freeze_action"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesResolution: 0;
  writesDisputeUpdate: 0;
  writesCommitteeDecision: 0;
  writesFreezeAction: 0;
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

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreview {
  resolutionOptionPreviewId: string;
  breachReviewPreviewRefs: string[];
  slaPreviewRefs: string[];
  escalationPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  resolutionOptionType: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewType;
  resolutionOptionStatus: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewStatus;
  resolutionOptionDecision: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewDecision;
  resolutionOptionScope: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewScope;
  resolutionPriority: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewPriority;
  candidateAssigneeRefs: string[];
  requiredEvidenceRefs: string[];
  resolutionReasonRefs: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewReason[];
  blockedResolutionCount: number;
  boundaryRefs: string[];
  sourceBreachReviewPreviewRefs: string[];
  resolutionSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  resolutionNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewBlockedAction[];
  createsResolution: false;
  createsDisputeUpdate: false;
  createsCommitteeDecision: false;
  createsFreezeAction: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachResolutionOptionPreviewNoWrite;
}
