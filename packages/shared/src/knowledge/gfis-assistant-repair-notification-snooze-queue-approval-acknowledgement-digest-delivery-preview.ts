import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewType =
  | "team_digest_delivery_preview"
  | "project_digest_delivery_preview"
  | "governance_digest_delivery_preview"
  | "external_blocked_digest_delivery_preview"
  | "committee_digest_delivery_preview"
  | "freeze_digest_delivery_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewStatus =
  | "delivery_preview_only"
  | "delivery_at_risk_preview"
  | "delivery_metadata_boundary"
  | "delivery_external_blocked"
  | "delivery_committee_required"
  | "delivery_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewDecision =
  | "show_team_digest_delivery_preview"
  | "show_project_digest_delivery_preview"
  | "show_governance_digest_delivery_preview"
  | "show_external_blocked_digest_delivery_preview"
  | "show_committee_digest_delivery_preview"
  | "show_freeze_digest_delivery_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewChannel =
  | "brain_inbox"
  | "pkc_task_center"
  | "gfis_assistant_panel"
  | "governance_console"
  | "committee_console"
  | "freeze_review_console";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewBlockedAction =
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreview {
  deliveryPreviewId: string;
  digestPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  deliveryType: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewType;
  deliveryStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewStatus;
  deliveryDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewDecision;
  deliveryScope: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewScope;
  candidateRecipientRefs: string[];
  candidateChannelRefs: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewChannel[];
  blockedDeliveryCount: number;
  boundaryRefs: string[];
  sourceDigestPreviewRefs: string[];
  deliverySummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  deliveryNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewBlockedAction[];
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_delivery_preview_policy";
  version: string;
  deliveryTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewType[];
  deliveryStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewStatus[];
  deliveryDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewDecision[];
  deliveryScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewScope[];
  deliveryChannels: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewChannel[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryPreviewNoWrite;
}
