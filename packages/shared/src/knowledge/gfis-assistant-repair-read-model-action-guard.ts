import type {
  GfisAssistantRepairAdmissionReadModelSurface,
  GfisAssistantRepairAdmissionReadModelViewType,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairReadModelActionGuardKind =
  | "display_only"
  | "repair_prompt"
  | "metadata_boundary_prompt"
  | "committee_note_prompt"
  | "freeze_note_prompt"
  | "blocked_write_action";

export type GfisAssistantRepairReadModelActionGuardStatus =
  | "allowed_display_only"
  | "repair_prompt_only"
  | "metadata_prompt_only"
  | "committee_prompt_only"
  | "freeze_prompt_only"
  | "blocked_no_write";

export type GfisAssistantRepairReadModelActionGuardDecision =
  | "show_only"
  | "show_repair_prompt"
  | "show_metadata_boundary_prompt"
  | "show_committee_note_prompt"
  | "show_freeze_note_prompt"
  | "block_write_action";

export type GfisAssistantRepairReadModelDisplayAction =
  | "view_admission_summary"
  | "view_handoff_summary"
  | "view_missing_requirements"
  | "view_metadata_boundary"
  | "view_committee_note"
  | "view_freeze_note"
  | "view_no_write_notice"
  | "view_next_step_candidate";

export type GfisAssistantRepairReadModelActionGuardBlockedAction =
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

export interface GfisAssistantRepairReadModelActionGuardNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
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

export interface GfisAssistantRepairReadModelActionGuard {
  actionGuardId: string;
  readModelRef: string;
  admissionPacketRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  viewType: GfisAssistantRepairAdmissionReadModelViewType;
  actionId: GfisAssistantRepairReadModelDisplayAction | GfisAssistantRepairReadModelActionGuardBlockedAction;
  actionKind: GfisAssistantRepairReadModelActionGuardKind;
  guardStatus: GfisAssistantRepairReadModelActionGuardStatus;
  guardDecision: GfisAssistantRepairReadModelActionGuardDecision;
  displayLabelRef: string;
  reasonRefs: string[];
  blockedActions: GfisAssistantRepairReadModelActionGuardBlockedAction[];
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
  noWrite: GfisAssistantRepairReadModelActionGuardNoWrite;
}

export interface GfisAssistantRepairReadModelActionGuardPolicy {
  policyId: "okf.gfis_assistant_repair_read_model_action_guard_policy";
  version: string;
  actionKinds: GfisAssistantRepairReadModelActionGuardKind[];
  guardStatuses: GfisAssistantRepairReadModelActionGuardStatus[];
  guardDecisions: GfisAssistantRepairReadModelActionGuardDecision[];
  allowedDisplayActions: GfisAssistantRepairReadModelDisplayAction[];
  blockedActions: GfisAssistantRepairReadModelActionGuardBlockedAction[];
  hardBoundaries: {
    actionGuardOnly: boolean;
    actionGuardIsNotActionReceipt: boolean;
    actionGuardIsNotReadReceipt: boolean;
    actionGuardIsNotAdmissionRecord: boolean;
    actionGuardIsNotReviewQueueItem: boolean;
    actionGuardIsNotKweWorkItem: boolean;
    actionGuardIsNotConfirmation: boolean;
    actionGuardIsNotDecisionRecord: boolean;
    actionGuardIsNotWaesResult: boolean;
    actionGuardIsNotBusinessWriteback: boolean;
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
  noWriteGuards: GfisAssistantRepairReadModelActionGuardNoWrite;
}
