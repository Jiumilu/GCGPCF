import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewType =
  | "team_escalation_digest_delivery_preview"
  | "project_escalation_digest_delivery_preview"
  | "governance_escalation_digest_delivery_preview"
  | "external_blocked_escalation_digest_delivery_preview"
  | "committee_escalation_digest_delivery_preview"
  | "freeze_escalation_digest_delivery_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewStatus =
  | "delivery_preview_only"
  | "delivery_evidence_required"
  | "delivery_metadata_boundary"
  | "delivery_external_blocked"
  | "delivery_committee_required"
  | "delivery_freeze_required";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewDecision =
  | "show_team_escalation_digest_delivery_preview"
  | "show_project_escalation_digest_delivery_preview"
  | "show_governance_escalation_digest_delivery_preview"
  | "show_external_blocked_escalation_digest_delivery_preview"
  | "show_committee_escalation_digest_delivery_preview"
  | "show_freeze_escalation_digest_delivery_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewChannel =
  | "brain_digest_delivery_candidate"
  | "pkc_digest_delivery_candidate"
  | "gfis_assistant_digest_delivery_candidate"
  | "external_blocked_digest_delivery_candidate"
  | "committee_digest_delivery_candidate"
  | "freeze_digest_delivery_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewBlockedAction =
  | "create_digest_delivery"
  | "create_delivery"
  | "create_digest"
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

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesDigestDelivery: 0;
  writesDelivery: 0;
  writesDigest: 0;
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

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreview {
  deliveryPreviewId: string;
  digestPreviewRefs: string[];
  escalationPreviewRefs: string[];
  acknowledgementPreviewRefs: string[];
  notificationPreviewRefs: string[];
  routingQueuePreviewRefs: string[];
  approvalPacketPreviewRefs: string[];
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  deliveryType: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewType;
  deliveryStatus: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewStatus;
  deliveryDecision: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewDecision;
  deliveryScope: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewScope;
  candidateRecipientRefs: string[];
  candidateChannelRefs: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewChannel[];
  blockedDeliveryCount: number;
  boundaryRefs: string[];
  sourceDigestPreviewRefs: string[];
  deliverySummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  deliveryNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewBlockedAction[];
  createsDigestDelivery: false;
  createsDelivery: false;
  createsDigest: false;
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
  noWrite: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryPreviewNoWrite;
}
