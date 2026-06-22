import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewType =
  | "team_ack_digest_preview"
  | "project_ack_digest_preview"
  | "governance_ack_digest_preview"
  | "external_blocked_ack_digest_preview"
  | "committee_ack_digest_preview"
  | "freeze_ack_digest_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewStatus =
  | "digest_preview_only"
  | "digest_at_risk_preview"
  | "digest_metadata_boundary"
  | "digest_external_blocked"
  | "digest_committee_required"
  | "digest_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewDecision =
  | "show_team_ack_digest_preview"
  | "show_project_ack_digest_preview"
  | "show_governance_ack_digest_preview"
  | "show_external_blocked_ack_digest_preview"
  | "show_committee_ack_digest_preview"
  | "show_freeze_ack_digest_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewBlockedAction =
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
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

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreview {
  digestPreviewId: string;
  acknowledgementPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  digestType: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewType;
  digestStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewStatus;
  digestDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewDecision;
  digestScope: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewScope;
  coverageCount: number;
  blockedAckCount: number;
  candidateAcknowledgerRefs: string[];
  boundaryRefs: string[];
  sourceAcknowledgementPreviewRefs: string[];
  digestSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  digestNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewBlockedAction[];
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
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewNoWrite;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_notification_snooze_queue_approval_acknowledgement_digest_preview_policy";
  version: string;
  digestTypes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewType[];
  digestStatuses: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewStatus[];
  digestDecisions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewDecision[];
  digestScopes: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewScope[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewBlockedAction[];
  noWriteGuards: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestPreviewNoWrite;
}
