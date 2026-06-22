import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewType =
  | "team_approval_packet_preview"
  | "project_approval_packet_preview"
  | "governance_approval_packet_preview"
  | "external_blocked_approval_packet_preview"
  | "committee_approval_packet_preview"
  | "freeze_approval_packet_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewStatus =
  | "approval_packet_preview_only"
  | "approval_packet_evidence_required"
  | "approval_packet_metadata_boundary"
  | "approval_packet_external_blocked"
  | "approval_packet_committee_required"
  | "approval_packet_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewDecision =
  | "show_team_approval_packet_preview"
  | "show_project_approval_packet_preview"
  | "show_governance_approval_packet_preview"
  | "show_external_blocked_approval_packet_preview"
  | "show_committee_approval_packet_preview"
  | "show_freeze_approval_packet_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewRoute =
  | "team_lead_candidate"
  | "project_owner_candidate"
  | "governance_reviewer_candidate"
  | "external_share_blocked_candidate"
  | "committee_candidate"
  | "freeze_reviewer_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewReason =
  | "resolution_option_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewBlockedAction =
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewNoWrite {
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreview {
  approvalPacketPreviewId: string;
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  approvalPacketType: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewType;
  approvalPacketStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewStatus;
  approvalPacketDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewDecision;
  approvalPacketScope: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewScope;
  approvalRoute: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewRoute;
  candidateApproverRefs: string[];
  requiredEvidenceRefs: string[];
  approvalReasonRefs: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewReason[];
  blockedApprovalCount: number;
  boundaryRefs: string[];
  sourceResolutionOptionPreviewRefs: string[];
  approvalSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  approvalNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewBlockedAction[];
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketPreviewNoWrite;
}
