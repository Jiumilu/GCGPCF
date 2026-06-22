import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewType =
  | "team_notification_acknowledgement_preview"
  | "project_notification_acknowledgement_preview"
  | "governance_notification_acknowledgement_preview"
  | "external_blocked_notification_acknowledgement_preview"
  | "committee_notification_acknowledgement_preview"
  | "freeze_notification_acknowledgement_preview";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewStatus =
  | "acknowledgement_preview_only"
  | "acknowledgement_evidence_required"
  | "acknowledgement_metadata_boundary"
  | "acknowledgement_external_blocked"
  | "acknowledgement_committee_required"
  | "acknowledgement_freeze_required";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewDecision =
  | "show_team_notification_acknowledgement_preview"
  | "show_project_notification_acknowledgement_preview"
  | "show_governance_notification_acknowledgement_preview"
  | "show_external_blocked_notification_acknowledgement_preview"
  | "show_committee_notification_acknowledgement_preview"
  | "show_freeze_notification_acknowledgement_preview";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewChannel =
  | "brain_inbox_ack_candidate"
  | "pkc_inbox_ack_candidate"
  | "gfis_assistant_panel_ack_candidate"
  | "external_blocked_ack_candidate"
  | "committee_panel_ack_candidate"
  | "freeze_panel_ack_candidate";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewDeadline =
  | "normal_candidate_deadline"
  | "evidence_candidate_deadline"
  | "metadata_candidate_deadline"
  | "blocked_candidate_deadline"
  | "committee_candidate_deadline"
  | "freeze_candidate_deadline";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewReason =
  | "notification_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewBlockedAction =
  | "create_acknowledgement"
  | "create_receipt"
  | "create_read_receipt"
  | "update_delivery_status"
  | "create_notification"
  | "create_message"
  | "create_inbox_item"
  | "send_external_notification"
  | "create_routing_queue"
  | "create_queue_item"
  | "create_approval_assignment"
  | "lock_approver"
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

export interface GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesAcknowledgement: 0;
  writesReceipt: 0;
  writesReadReceipt: 0;
  writesDeliveryStatus: 0;
  writesNotification: 0;
  writesMessage: 0;
  writesInboxItem: 0;
  writesRoutingQueue: 0;
  writesQueueItem: 0;
  writesApprovalAssignment: 0;
  writesApprovalLock: 0;
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

export interface GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreview {
  acknowledgementPreviewId: string;
  notificationPreviewRefs: string[];
  routingQueuePreviewRefs: string[];
  approvalPacketPreviewRefs: string[];
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  acknowledgementType: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewType;
  acknowledgementStatus: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewStatus;
  acknowledgementDecision: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewDecision;
  acknowledgementScope: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewScope;
  acknowledgementChannel: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewChannel;
  acknowledgementDeadline: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewDeadline;
  candidateAcknowledgerRefs: string[];
  requiredEvidenceRefs: string[];
  acknowledgementReasonRefs: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewReason[];
  blockedAcknowledgementCount: number;
  boundaryRefs: string[];
  sourceNotificationPreviewRefs: string[];
  acknowledgementSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  acknowledgementNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewBlockedAction[];
  createsAcknowledgement: false;
  createsReceipt: false;
  createsReadReceipt: false;
  updatesDeliveryStatus: false;
  createsNotification: false;
  createsMessage: false;
  createsInboxItem: false;
  sendsExternalNotification: false;
  createsRoutingQueue: false;
  createsQueueItem: false;
  createsApprovalAssignment: false;
  locksApprover: false;
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
  noWrite: GfisAssistantDks202RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementPreviewNoWrite;
}
