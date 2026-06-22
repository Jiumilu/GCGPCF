import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewType =
  | "team_acknowledgement_escalation_preview"
  | "project_acknowledgement_escalation_preview"
  | "governance_acknowledgement_escalation_preview"
  | "external_blocked_acknowledgement_escalation_preview"
  | "committee_acknowledgement_escalation_preview"
  | "freeze_acknowledgement_escalation_preview";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewStatus =
  | "escalation_preview_only"
  | "escalation_evidence_required"
  | "escalation_metadata_boundary"
  | "escalation_external_blocked"
  | "escalation_committee_required"
  | "escalation_freeze_required";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewDecision =
  | "show_team_acknowledgement_escalation_preview"
  | "show_project_acknowledgement_escalation_preview"
  | "show_governance_acknowledgement_escalation_preview"
  | "show_external_blocked_acknowledgement_escalation_preview"
  | "show_committee_acknowledgement_escalation_preview"
  | "show_freeze_acknowledgement_escalation_preview";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewLevel =
  | "team_lead_candidate_level"
  | "project_owner_candidate_level"
  | "governance_reviewer_candidate_level"
  | "external_blocked_candidate_level"
  | "committee_candidate_level"
  | "freeze_reviewer_candidate_level";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewTrigger =
  | "acknowledgement_timeout_candidate"
  | "evidence_gap_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewReason =
  | "acknowledgement_timeout_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewBlockedAction =
  | "create_escalation"
  | "create_timeout_event"
  | "create_kwe_work_item"
  | "create_notification"
  | "create_acknowledgement"
  | "create_receipt"
  | "create_read_receipt"
  | "update_delivery_status"
  | "send_external_notification"
  | "create_approval_assignment"
  | "lock_approver"
  | "create_approval_packet"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_committee_decision"
  | "create_freeze_action"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesEscalation: 0;
  writesTimeoutEvent: 0;
  writesKweWorkItem: 0;
  writesNotification: 0;
  writesAcknowledgement: 0;
  writesReceipt: 0;
  writesReadReceipt: 0;
  writesDeliveryStatus: 0;
  writesApprovalAssignment: 0;
  writesApprovalLock: 0;
  writesApprovalPacket: 0;
  writesApprovalRequest: 0;
  writesApprovalDecision: 0;
  writesCommitteeDecision: 0;
  writesFreezeAction: 0;
  writesWaesGateResult: 0;
  writesHarnessEvidence: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreview {
  escalationPreviewId: string;
  acknowledgementPreviewRefs: string[];
  notificationPreviewRefs: string[];
  routingQueuePreviewRefs: string[];
  approvalPacketPreviewRefs: string[];
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  escalationType: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewType;
  escalationStatus: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewStatus;
  escalationDecision: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewDecision;
  escalationScope: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewScope;
  escalationLevel: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewLevel;
  escalationTrigger: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewTrigger;
  candidateEscalationRecipientRefs: string[];
  requiredEvidenceRefs: string[];
  escalationReasonRefs: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewReason[];
  blockedEscalationCount: number;
  boundaryRefs: string[];
  sourceAcknowledgementPreviewRefs: string[];
  escalationSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  escalationNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewBlockedAction[];
  createsEscalation: false;
  createsTimeoutEvent: false;
  createsKweWorkItem: false;
  createsNotification: false;
  createsAcknowledgement: false;
  createsReceipt: false;
  createsReadReceipt: false;
  updatesDeliveryStatus: false;
  sendsExternalNotification: false;
  createsApprovalAssignment: false;
  locksApprover: false;
  createsApprovalPacket: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsCommitteeDecision: false;
  createsFreezeAction: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantDks215RoutingQueueNotificationAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAckEscalationPreviewNoWrite;
}
