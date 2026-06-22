import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewType =
  | "watch_ack_preview"
  | "urgent_ack_preview"
  | "governance_ack_preview"
  | "external_blocked_ack_preview"
  | "committee_ack_preview"
  | "freeze_ack_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewStatus =
  | "ack_preview_only"
  | "ack_at_risk_preview"
  | "ack_metadata_boundary"
  | "ack_external_blocked"
  | "ack_committee_required"
  | "ack_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewDecision =
  | "show_watch_ack_preview"
  | "show_urgent_ack_preview"
  | "show_governance_ack_preview"
  | "show_external_blocked_ack_preview"
  | "show_committee_ack_preview"
  | "show_freeze_ack_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewBlockedAction =
  | "create_acknowledgement"
  | "create_read_receipt"
  | "assign_acknowledger"
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesAcknowledgement: 0;
  writesReadReceipt: 0;
  writesAcknowledgerAssignment: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreview {
  acknowledgementPreviewId: string;
  escalationPreviewRef: string;
  slaPreviewRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  ackType: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewType;
  ackStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewStatus;
  ackDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewDecision;
  ackScope: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewScope;
  candidateAcknowledgerRefs: string[];
  ackBoundaryRefs: string[];
  sourceEscalationPreviewRefs: string[];
  sourceSlaPreviewRefs: string[];
  ackSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  ackNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewBlockedAction[];
  createsAcknowledgement: false;
  createsReadReceipt: false;
  assignsAcknowledger: false;
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_escalation_acknowledgement_preview_policy";
  version: string;
  ackTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewType[];
  ackStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewStatus[];
  ackDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewDecision[];
  ackScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalEscalationAcknowledgementPreviewNoWrite;
}
