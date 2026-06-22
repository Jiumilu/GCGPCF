import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairActionGuardEventPreviewType =
  | "display_event_preview"
  | "repair_prompt_event_preview"
  | "metadata_boundary_event_preview"
  | "committee_note_event_preview"
  | "freeze_note_event_preview"
  | "blocked_write_event_preview";

export type GfisAssistantRepairActionGuardEventPreviewStatus =
  | "preview_only"
  | "blocked_preview"
  | "metadata_only_preview"
  | "repair_required_preview"
  | "committee_preview"
  | "freeze_preview";

export type GfisAssistantRepairActionGuardEventPreviewDecision =
  | "show_preview_only"
  | "show_repair_preview"
  | "show_metadata_boundary_preview"
  | "show_committee_preview"
  | "show_freeze_preview"
  | "show_blocked_write_preview";

export type GfisAssistantRepairActionGuardEventPreviewBlockedAction =
  | "create_event_record"
  | "create_action_receipt"
  | "create_read_receipt"
  | "create_admission_record"
  | "create_review_queue_item"
  | "create_kwe_work_item"
  | "create_confirmation_record"
  | "create_decision_record"
  | "create_waes_gate_result"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairActionGuardEventPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesEventRecord: 0;
  writesActionReceipt: 0;
  writesReadReceipt: 0;
  writesAdmissionRecord: 0;
  writesReviewQueueItem: 0;
  writesConfirmationRecord: 0;
  writesDecisionRecord: 0;
  writesGapRecord: 0;
  writesBountyRecord: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesEvidenceRecord: 0;
  writesTargetReceipt: 0;
  writesCommitteeDecisionCompletion: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesQuotaTransfer: 0;
  writesBountySettlement: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantRepairActionGuardEventPreview {
  eventPreviewId: string;
  actionGuardRef: string;
  readModelRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  previewType: GfisAssistantRepairActionGuardEventPreviewType;
  previewStatus: GfisAssistantRepairActionGuardEventPreviewStatus;
  previewDecision: GfisAssistantRepairActionGuardEventPreviewDecision;
  previewSummaryRef: string;
  reasonRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairActionGuardEventPreviewBlockedAction[];
  createsEventRecord: false;
  createsActionReceipt: false;
  createsReadReceipt: false;
  createsAdmissionRecord: false;
  createsReviewQueueItem: false;
  createsKweWorkItem: false;
  createsConfirmationRecord: false;
  createsDecisionRecord: false;
  createsWaesGateResult: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairActionGuardEventPreviewNoWrite;
}

export interface GfisAssistantRepairActionGuardEventPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_action_guard_event_preview_policy";
  version: string;
  previewTypes: GfisAssistantRepairActionGuardEventPreviewType[];
  previewStatuses: GfisAssistantRepairActionGuardEventPreviewStatus[];
  previewDecisions: GfisAssistantRepairActionGuardEventPreviewDecision[];
  blockedActions: GfisAssistantRepairActionGuardEventPreviewBlockedAction[];
  hardBoundaries: {
    eventPreviewOnly: boolean;
    eventPreviewIsNotEventRecord: boolean;
    eventPreviewIsNotActionReceipt: boolean;
    eventPreviewIsNotReadReceipt: boolean;
    eventPreviewIsNotAdmissionRecord: boolean;
    eventPreviewIsNotReviewQueueItem: boolean;
    eventPreviewIsNotKweWorkItem: boolean;
    eventPreviewIsNotConfirmation: boolean;
    eventPreviewIsNotDecisionRecord: boolean;
    eventPreviewIsNotWaesResult: boolean;
    eventPreviewIsNotBusinessWriteback: boolean;
    createsEventRecordMustBeFalse: boolean;
    createsActionReceiptMustBeFalse: boolean;
    createsReadReceiptMustBeFalse: boolean;
    createsAdmissionRecordMustBeFalse: boolean;
    createsReviewQueueItemMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    createsConfirmationRecordMustBeFalse: boolean;
    createsDecisionRecordMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    completesCommitteeDecisionMustBeFalse: boolean;
  };
  noWriteGuards: GfisAssistantRepairActionGuardEventPreviewNoWrite;
}
