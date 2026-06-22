import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewType =
  | "team_sla_breach_review_preview"
  | "project_sla_breach_review_preview"
  | "governance_sla_breach_review_preview"
  | "external_blocked_sla_breach_review_preview"
  | "committee_sla_breach_review_preview"
  | "freeze_sla_breach_review_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewStatus =
  | "breach_review_preview_only"
  | "breach_review_evidence_gap"
  | "breach_review_metadata_boundary"
  | "breach_review_external_blocked"
  | "breach_review_committee_required"
  | "breach_review_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewDecision =
  | "show_team_sla_breach_review_preview"
  | "show_project_sla_breach_review_preview"
  | "show_governance_sla_breach_review_preview"
  | "show_external_blocked_sla_breach_review_preview"
  | "show_committee_sla_breach_review_preview"
  | "show_freeze_sla_breach_review_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewSeverity =
  | "low_candidate"
  | "medium_candidate"
  | "high_candidate"
  | "metadata_only_candidate"
  | "external_blocked_candidate"
  | "committee_required_candidate"
  | "freeze_required_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewReason =
  | "overdue_ack_candidate"
  | "missing_delivery_ack_candidate"
  | "missing_evidence_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewBlockedAction =
  | "create_breach_record"
  | "create_dispute"
  | "create_committee_case"
  | "create_freeze_request"
  | "create_reminder"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesBreachRecord: 0;
  writesDispute: 0;
  writesCommitteeCase: 0;
  writesFreezeRequest: 0;
  writesReminder: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreview {
  breachReviewPreviewId: string;
  slaPreviewRefs: string[];
  escalationPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  breachReviewType: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewType;
  breachReviewStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewStatus;
  breachReviewDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewDecision;
  breachReviewScope: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewScope;
  breachSeverity: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewSeverity;
  overdueMinutes: number;
  candidateReviewerRefs: string[];
  evidenceGapRefs: string[];
  breachReasonRefs: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewReason[];
  blockedReviewCount: number;
  boundaryRefs: string[];
  sourceSlaPreviewRefs: string[];
  breachSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  breachNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewBlockedAction[];
  createsBreachRecord: false;
  createsDispute: false;
  createsCommitteeCase: false;
  createsFreezeRequest: false;
  createsReminder: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewPreviewNoWrite;
}
