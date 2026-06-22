import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewType =
  | "team_digest_delivery_ack_escalation_resolution_option_preview"
  | "project_digest_delivery_ack_escalation_resolution_option_preview"
  | "governance_digest_delivery_ack_escalation_resolution_option_preview"
  | "external_blocked_digest_delivery_ack_escalation_resolution_option_preview"
  | "committee_digest_delivery_ack_escalation_resolution_option_preview"
  | "freeze_digest_delivery_ack_escalation_resolution_option_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewStatus =
  | "resolution_option_preview_only"
  | "resolution_option_evidence_required"
  | "resolution_option_metadata_boundary"
  | "resolution_option_external_blocked"
  | "resolution_option_committee_required"
  | "resolution_option_freeze_required";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewDecision =
  | "show_team_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_project_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_governance_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_external_blocked_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_committee_digest_delivery_ack_escalation_resolution_option_preview"
  | "show_freeze_digest_delivery_ack_escalation_resolution_option_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewPriority =
  | "p3_candidate"
  | "p2_candidate"
  | "p1_candidate"
  | "metadata_only_candidate"
  | "external_blocked_candidate"
  | "committee_required_candidate"
  | "freeze_required_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewReason =
  | "supplement_delivery_ack_candidate"
  | "repair_evidence_gap_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewBlockedAction =
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

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewNoWrite {
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

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreview {
  resolutionOptionPreviewId: string;
  breachReviewPreviewRefs: string[];
  slaPreviewRefs: string[];
  escalationPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  resolutionOptionType: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewType;
  resolutionOptionStatus: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewStatus;
  resolutionOptionDecision: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewDecision;
  resolutionOptionScope: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewScope;
  resolutionPriority: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewPriority;
  candidateAssigneeRefs: string[];
  requiredEvidenceRefs: string[];
  resolutionReasonRefs: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewReason[];
  blockedResolutionCount: number;
  boundaryRefs: string[];
  sourceBreachReviewPreviewRefs: string[];
  resolutionSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  resolutionNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewBlockedAction[];
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
  noWrite: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionPreviewNoWrite;
}
