import type {
  GfisAssistantRepairHandoffReviewAdmissionDecision,
  GfisAssistantRepairHandoffReviewAdmissionStatus,
} from "./gfis-assistant-repair-handoff-review-admission";
import type {
  GfisAssistantRepairDraftHandoffTargetCandidate,
} from "./gfis-assistant-repair-draft-handoff-packet";
import type {
  GfisAssistantRepairSubmissionMetadataRefBundle,
} from "./gfis-assistant-repair-submission-intake";

export type GfisAssistantRepairAdmissionReadModelSurface =
  | "brain"
  | "pkc"
  | "gfis_assistant";

export type GfisAssistantRepairAdmissionReadModelViewType =
  | "brain_governance_read"
  | "pkc_owner_read"
  | "gfis_assistant_read"
  | "committee_candidate_read"
  | "freeze_candidate_read";

export type GfisAssistantRepairAdmissionReadModelVisibilityMode =
  | "own_project_only"
  | "metadata_only"
  | "governance_summary"
  | "committee_authorized"
  | "freeze_authorized";

export type GfisAssistantRepairAdmissionReadModelDisplaySection =
  | "admission_summary"
  | "handoff_summary"
  | "target_candidate"
  | "missing_requirements"
  | "blocked_reasons"
  | "metadata_boundary"
  | "no_write_notice"
  | "next_step_candidate";

export type GfisAssistantRepairAdmissionReadModelBlockedAction =
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

export interface GfisAssistantRepairAdmissionReadModelNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
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

export interface GfisAssistantRepairAdmissionReadModel {
  readModelId: string;
  admissionPacketRef: string;
  handoffPacketRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  viewType: GfisAssistantRepairAdmissionReadModelViewType;
  visibilityMode: GfisAssistantRepairAdmissionReadModelVisibilityMode;
  admissionStatus: GfisAssistantRepairHandoffReviewAdmissionStatus;
  admissionDecision: GfisAssistantRepairHandoffReviewAdmissionDecision;
  targetCandidate: GfisAssistantRepairDraftHandoffTargetCandidate;
  displaySections: GfisAssistantRepairAdmissionReadModelDisplaySection[];
  maskedFields: string[];
  metadataRefBundle: GfisAssistantRepairSubmissionMetadataRefBundle;
  missingRequirementRefs: string[];
  blockedReasonRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairAdmissionReadModelBlockedAction[];
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
  noWrite: GfisAssistantRepairAdmissionReadModelNoWrite;
}

export interface GfisAssistantRepairAdmissionReadModelPolicy {
  policyId: "okf.gfis_assistant_repair_admission_read_model_policy";
  version: string;
  surfaces: GfisAssistantRepairAdmissionReadModelSurface[];
  viewTypes: GfisAssistantRepairAdmissionReadModelViewType[];
  visibilityModes: GfisAssistantRepairAdmissionReadModelVisibilityMode[];
  displaySections: GfisAssistantRepairAdmissionReadModelDisplaySection[];
  blockedActions: GfisAssistantRepairAdmissionReadModelBlockedAction[];
  hardBoundaries: {
    readModelOnly: boolean;
    readModelIsNotReadReceipt: boolean;
    readModelIsNotAdmissionRecord: boolean;
    readModelIsNotReviewQueueItem: boolean;
    readModelIsNotKweWorkItem: boolean;
    readModelIsNotConfirmation: boolean;
    readModelIsNotDecisionRecord: boolean;
    readModelIsNotWaesResult: boolean;
    readModelIsNotBusinessWriteback: boolean;
    rawContentMustBeHidden: boolean;
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
  noWriteGuards: GfisAssistantRepairAdmissionReadModelNoWrite;
}
