import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewType =
  | "team_routing_notification_preview"
  | "project_routing_notification_preview"
  | "governance_routing_notification_preview"
  | "external_blocked_routing_notification_preview"
  | "committee_routing_notification_preview"
  | "freeze_routing_notification_preview";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewStatus =
  | "notification_preview_only"
  | "notification_evidence_required"
  | "notification_metadata_boundary"
  | "notification_external_blocked"
  | "notification_committee_required"
  | "notification_freeze_required";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewDecision =
  | "show_team_routing_notification_preview"
  | "show_project_routing_notification_preview"
  | "show_governance_routing_notification_preview"
  | "show_external_blocked_routing_notification_preview"
  | "show_committee_routing_notification_preview"
  | "show_freeze_routing_notification_preview";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewChannel =
  | "brain_inbox_candidate"
  | "pkc_inbox_candidate"
  | "gfis_assistant_panel_candidate"
  | "external_blocked_channel_candidate"
  | "committee_panel_candidate"
  | "freeze_panel_candidate";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewPriority =
  | "normal_candidate"
  | "evidence_candidate"
  | "metadata_candidate"
  | "blocked_candidate"
  | "committee_candidate"
  | "freeze_candidate";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewReason =
  | "routing_queue_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewBlockedAction =
  | "create_notification"
  | "create_notification_delivery"
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

export interface GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesNotification: 0;
  writesNotificationDelivery: 0;
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

export interface GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreview {
  notificationPreviewId: string;
  routingQueuePreviewRefs: string[];
  approvalPacketPreviewRefs: string[];
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  notificationType: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewType;
  notificationStatus: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewStatus;
  notificationDecision: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewDecision;
  notificationScope: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewScope;
  notificationChannel: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewChannel;
  notificationPriority: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewPriority;
  candidateRecipientRefs: string[];
  requiredEvidenceRefs: string[];
  notificationReasonRefs: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewReason[];
  blockedNotificationCount: number;
  boundaryRefs: string[];
  sourceRoutingQueuePreviewRefs: string[];
  notificationSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  notificationNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewBlockedAction[];
  createsNotification: false;
  createsNotificationDelivery: false;
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
  noWrite: GfisAssistantDks189RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewNoWrite;
}
