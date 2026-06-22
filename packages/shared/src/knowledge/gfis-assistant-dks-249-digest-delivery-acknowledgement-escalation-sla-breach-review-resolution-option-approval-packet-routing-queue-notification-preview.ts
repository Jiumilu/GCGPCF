import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewType =
  | "team_routing_notification_preview"
  | "project_routing_notification_preview"
  | "governance_routing_notification_preview"
  | "external_blocked_routing_notification_preview"
  | "committee_routing_notification_preview"
  | "freeze_routing_notification_preview";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewStatus =
  | "notification_preview_only"
  | "notification_evidence_required"
  | "notification_metadata_boundary"
  | "notification_external_blocked"
  | "notification_committee_required"
  | "notification_freeze_required";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewDecision =
  | "show_team_routing_notification_preview"
  | "show_project_routing_notification_preview"
  | "show_governance_routing_notification_preview"
  | "show_external_blocked_routing_notification_preview"
  | "show_committee_routing_notification_preview"
  | "show_freeze_routing_notification_preview";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewChannel =
  | "brain_inbox_candidate"
  | "pkc_inbox_candidate"
  | "gfis_assistant_panel_candidate"
  | "external_blocked_channel_candidate"
  | "committee_panel_candidate"
  | "freeze_panel_candidate";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewPriority =
  | "normal_candidate"
  | "evidence_candidate"
  | "metadata_candidate"
  | "blocked_candidate"
  | "committee_candidate"
  | "freeze_candidate";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewReason =
  | "routing_queue_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewBlockedAction =
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

export interface GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewNoWrite {
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

export interface GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreview {
  notificationPreviewId: string;
  routingQueuePreviewRefs: string[];
  approvalPacketPreviewRefs: string[];
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  notificationType: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewType;
  notificationStatus: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewStatus;
  notificationDecision: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewDecision;
  notificationScope: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewScope;
  notificationChannel: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewChannel;
  notificationPriority: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewPriority;
  candidateRecipientRefs: string[];
  requiredEvidenceRefs: string[];
  notificationReasonRefs: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewReason[];
  blockedNotificationCount: number;
  boundaryRefs: string[];
  sourceRoutingQueuePreviewRefs: string[];
  notificationSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  notificationNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewBlockedAction[];
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
  noWrite: GfisAssistantDks249DigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationPreviewNoWrite;
}
