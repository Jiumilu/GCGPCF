import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewType =
  | "team_delivery_ack_escalation_preview"
  | "project_delivery_ack_escalation_preview"
  | "governance_delivery_ack_escalation_preview"
  | "external_blocked_delivery_ack_escalation_preview"
  | "committee_delivery_ack_escalation_preview"
  | "freeze_delivery_ack_escalation_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewStatus =
  | "escalation_preview_only"
  | "escalation_at_risk_preview"
  | "escalation_metadata_boundary"
  | "escalation_external_blocked"
  | "escalation_committee_required"
  | "escalation_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewDecision =
  | "show_team_delivery_ack_escalation_preview"
  | "show_project_delivery_ack_escalation_preview"
  | "show_governance_delivery_ack_escalation_preview"
  | "show_external_blocked_delivery_ack_escalation_preview"
  | "show_committee_delivery_ack_escalation_preview"
  | "show_freeze_delivery_ack_escalation_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewReason =
  | "acknowledgement_missing_candidate"
  | "acknowledgement_at_risk_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewBlockedAction =
  | "create_escalation"
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesEscalation: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreview {
  escalationPreviewId: string;
  deliveryAcknowledgementPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  escalationType: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewType;
  escalationStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewStatus;
  escalationDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewDecision;
  escalationScope: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewScope;
  candidateEscalationOwnerRefs: string[];
  escalationReasonRefs: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewReason[];
  blockedEscalationCount: number;
  boundaryRefs: string[];
  sourceDeliveryAcknowledgementPreviewRefs: string[];
  escalationSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  escalationNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewBlockedAction[];
  createsEscalation: false;
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_acknowledgement_escalation_preview_policy";
  version: string;
  escalationTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewType[];
  escalationStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewStatus[];
  escalationDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewDecision[];
  escalationScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewScope[];
  escalationReasons: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewReason[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationPreviewNoWrite;
}
