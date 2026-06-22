import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewType =
  | "team_digest_delivery_ack_escalation_preview"
  | "project_digest_delivery_ack_escalation_preview"
  | "governance_digest_delivery_ack_escalation_preview"
  | "external_blocked_digest_delivery_ack_escalation_preview"
  | "committee_digest_delivery_ack_escalation_preview"
  | "freeze_digest_delivery_ack_escalation_preview";

export type GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewStatus =
  | "escalation_preview_only"
  | "escalation_evidence_required"
  | "escalation_metadata_boundary"
  | "escalation_external_blocked"
  | "escalation_committee_required"
  | "escalation_freeze_required";

export type GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewDecision =
  | "show_team_digest_delivery_ack_escalation_preview"
  | "show_project_digest_delivery_ack_escalation_preview"
  | "show_governance_digest_delivery_ack_escalation_preview"
  | "show_external_blocked_digest_delivery_ack_escalation_preview"
  | "show_committee_digest_delivery_ack_escalation_preview"
  | "show_freeze_digest_delivery_ack_escalation_preview";

export type GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewPriority =
  | "normal_escalation_candidate"
  | "evidence_escalation_candidate"
  | "metadata_escalation_candidate"
  | "blocked_escalation_candidate"
  | "committee_escalation_candidate"
  | "freeze_escalation_candidate";

export type GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewReason =
  | "acknowledgement_missing_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewBlockedAction =
  | "create_escalation"
  | "create_escalation_task"
  | "create_delivery_acknowledgement"
  | "create_digest_delivery"
  | "create_delivery"
  | "create_digest"
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

export interface GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesEscalation: 0;
  writesEscalationTask: 0;
  writesDeliveryAcknowledgement: 0;
  writesDigestDelivery: 0;
  writesDelivery: 0;
  writesDigest: 0;
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

export interface GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreview {
  escalationPreviewId: string;
  deliveryAcknowledgementPreviewRefs: string[];
  deliveryPreviewRefs: string[];
  digestPreviewRefs: string[];
  acknowledgementPreviewRefs: string[];
  notificationPreviewRefs: string[];
  routingQueuePreviewRefs: string[];
  approvalPacketPreviewRefs: string[];
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  escalationType: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewType;
  escalationStatus: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewStatus;
  escalationDecision: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewDecision;
  escalationScope: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewScope;
  escalationPriority: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewPriority;
  candidateEscalationOwnerRefs: string[];
  escalationReasonRefs: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewReason[];
  requiredEvidenceRefs: string[];
  blockedEscalationCount: number;
  boundaryRefs: string[];
  sourceDeliveryAcknowledgementPreviewRefs: string[];
  escalationSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  escalationNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewBlockedAction[];
  createsEscalation: false;
  createsEscalationTask: false;
  createsDeliveryAcknowledgement: false;
  createsDigestDelivery: false;
  createsDelivery: false;
  createsDigest: false;
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
  noWrite: GfisAssistantDks243DigestDeliveryAcknowledgementEscalationPreviewNoWrite;
}
