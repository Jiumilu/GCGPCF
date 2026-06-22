import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewType =
  | "team_delivery_ack_preview"
  | "project_delivery_ack_preview"
  | "governance_delivery_ack_preview"
  | "external_blocked_delivery_ack_preview"
  | "committee_delivery_ack_preview"
  | "freeze_delivery_ack_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewStatus =
  | "acknowledgement_preview_only"
  | "acknowledgement_at_risk_preview"
  | "acknowledgement_metadata_boundary"
  | "acknowledgement_external_blocked"
  | "acknowledgement_committee_required"
  | "acknowledgement_freeze_required";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewDecision =
  | "show_team_delivery_ack_preview"
  | "show_project_delivery_ack_preview"
  | "show_governance_delivery_ack_preview"
  | "show_external_blocked_delivery_ack_preview"
  | "show_committee_delivery_ack_preview"
  | "show_freeze_delivery_ack_preview";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewMethod =
  | "preview_seen"
  | "candidate_ack"
  | "manual_review_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate"
  | "external_blocked_candidate";

export type GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewBlockedAction =
  | "create_delivery_acknowledgement"
  | "create_delivery"
  | "create_notification"
  | "create_digest"
  | "create_acknowledgement"
  | "create_read_receipt"
  | "create_reminder"
  | "create_escalation_task"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesDeliveryAcknowledgement: 0;
  writesDelivery: 0;
  writesNotification: 0;
  writesDigest: 0;
  writesAcknowledgement: 0;
  writesReadReceipt: 0;
  writesReminder: 0;
  writesEscalationTask: 0;
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

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreview {
  deliveryAcknowledgementPreviewId: string;
  deliveryPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  acknowledgementType: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewType;
  acknowledgementStatus: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewStatus;
  acknowledgementDecision: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewDecision;
  acknowledgementScope: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewScope;
  candidateAcknowledgerRefs: string[];
  acknowledgementMethodRefs: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewMethod[];
  blockedAcknowledgementCount: number;
  boundaryRefs: string[];
  sourceDeliveryPreviewRefs: string[];
  acknowledgementSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  acknowledgementNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewBlockedAction[];
  createsDeliveryAcknowledgement: false;
  createsDelivery: false;
  createsNotification: false;
  createsDigest: false;
  createsAcknowledgement: false;
  createsReadReceipt: false;
  createsReminder: false;
  createsEscalationTask: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewNoWrite;
}

export interface GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewPolicy {
  policyId: "okf.gfis_assistant_approval_route_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_acknowledgement_escalation_digest_delivery_acknowledgement_preview_policy";
  version: string;
  acknowledgementTypes: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewType[];
  acknowledgementStatuses: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewStatus[];
  acknowledgementDecisions: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewDecision[];
  acknowledgementScopes: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewScope[];
  acknowledgementMethods: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewMethod[];
  blockedActions: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewBlockedAction[];
  noWriteGuards: GfisAssistantApprovalRouteAckEscalationDigestDeliveryAckEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAcknowledgementPreviewNoWrite;
}
