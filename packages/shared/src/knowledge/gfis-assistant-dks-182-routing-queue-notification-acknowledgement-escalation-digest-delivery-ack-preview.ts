import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewType =
  | "team_escalation_digest_delivery_ack_preview"
  | "project_escalation_digest_delivery_ack_preview"
  | "governance_escalation_digest_delivery_ack_preview"
  | "external_blocked_escalation_digest_delivery_ack_preview"
  | "committee_escalation_digest_delivery_ack_preview"
  | "freeze_escalation_digest_delivery_ack_preview";

export type GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewStatus =
  | "acknowledgement_preview_only"
  | "acknowledgement_evidence_required"
  | "acknowledgement_metadata_boundary"
  | "acknowledgement_external_blocked"
  | "acknowledgement_committee_required"
  | "acknowledgement_freeze_required";

export type GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewDecision =
  | "show_team_escalation_digest_delivery_ack_preview"
  | "show_project_escalation_digest_delivery_ack_preview"
  | "show_governance_escalation_digest_delivery_ack_preview"
  | "show_external_blocked_escalation_digest_delivery_ack_preview"
  | "show_committee_escalation_digest_delivery_ack_preview"
  | "show_freeze_escalation_digest_delivery_ack_preview";

export type GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewMethod =
  | "preview_seen_candidate"
  | "candidate_acknowledgement"
  | "manual_review_candidate"
  | "metadata_boundary_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewBlockedAction =
  | "create_delivery_acknowledgement"
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

export interface GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesDeliveryAcknowledgement: 0;
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

export interface GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreview {
  deliveryAcknowledgementPreviewId: string;
  deliveryPreviewRefs: string[];
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
  acknowledgementType: GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewType;
  acknowledgementStatus: GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewStatus;
  acknowledgementDecision: GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewDecision;
  acknowledgementScope: GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewScope;
  candidateAcknowledgerRefs: string[];
  acknowledgementMethodRefs: GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewMethod[];
  blockedAcknowledgementCount: number;
  boundaryRefs: string[];
  sourceDeliveryPreviewRefs: string[];
  acknowledgementSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  acknowledgementNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewBlockedAction[];
  createsDeliveryAcknowledgement: false;
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
  noWrite: GfisAssistantDks182RoutingQueueNotificationAcknowledgementEscalationDigestDeliveryAckPreviewNoWrite;
}
