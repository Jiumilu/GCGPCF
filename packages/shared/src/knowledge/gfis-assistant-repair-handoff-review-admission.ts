import type {
  GfisAssistantRepairDraftHandoffPacketType,
  GfisAssistantRepairDraftHandoffPacketStatus,
  GfisAssistantRepairDraftHandoffTargetCandidate,
} from "./gfis-assistant-repair-draft-handoff-packet";
import type {
  GfisAssistantRepairSubmissionMetadataRefBundle,
} from "./gfis-assistant-repair-submission-intake";
import type {
  GfisAssistantWaesGuidanceSurface,
} from "./gfis-assistant-waes-guidance-packet";

export type GfisAssistantRepairHandoffReviewAdmissionStatus =
  | "admitted_candidate"
  | "repair_required"
  | "metadata_only_admitted"
  | "committee_agenda_blocked"
  | "freeze_review_blocked"
  | "blocked_hold";

export type GfisAssistantRepairHandoffReviewAdmissionDecision =
  | "allow_review_candidate"
  | "require_repair"
  | "metadata_only_review_candidate"
  | "prepare_committee_agenda_candidate"
  | "prepare_freeze_review_candidate"
  | "hold_blocked";

export type GfisAssistantRepairHandoffReviewAdmissionDisplayAction =
  | "show_admission_packet"
  | "show_handoff_summary"
  | "show_target_candidate"
  | "show_missing_requirements"
  | "show_metadata_boundary"
  | "show_committee_agenda_note"
  | "show_freeze_note"
  | "show_blocked_hold_note"
  | "show_no_write_notice";

export type GfisAssistantRepairHandoffReviewAdmissionBlockedAction =
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

export interface GfisAssistantRepairHandoffReviewAdmissionNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
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

export interface GfisAssistantRepairHandoffReviewAdmissionPacket {
  admissionPacketId: string;
  handoffPacketRef: string;
  decisionDraftRef: string;
  reviewPacketRef: string;
  intakeRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWaesGuidanceSurface;
  sourceHandoffType: GfisAssistantRepairDraftHandoffPacketType;
  sourceHandoffStatus: GfisAssistantRepairDraftHandoffPacketStatus;
  targetCandidate: GfisAssistantRepairDraftHandoffTargetCandidate;
  admissionStatus: GfisAssistantRepairHandoffReviewAdmissionStatus;
  admissionDecision: GfisAssistantRepairHandoffReviewAdmissionDecision;
  admissionCheckRefs: string[];
  missingRequirementRefs: string[];
  metadataRefBundle: GfisAssistantRepairSubmissionMetadataRefBundle;
  blockedReasonRefs: string[];
  allowedDisplayActions: GfisAssistantRepairHandoffReviewAdmissionDisplayAction[];
  blockedActions: GfisAssistantRepairHandoffReviewAdmissionBlockedAction[];
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
  noWrite: GfisAssistantRepairHandoffReviewAdmissionNoWrite;
}

export interface GfisAssistantRepairHandoffReviewAdmissionPolicy {
  policyId: "okf.gfis_assistant_repair_handoff_review_admission_policy";
  version: string;
  admissionStatuses: GfisAssistantRepairHandoffReviewAdmissionStatus[];
  admissionDecisions: GfisAssistantRepairHandoffReviewAdmissionDecision[];
  allowedDisplayActions: GfisAssistantRepairHandoffReviewAdmissionDisplayAction[];
  blockedActions: GfisAssistantRepairHandoffReviewAdmissionBlockedAction[];
  hardBoundaries: {
    admissionPacketOnly: boolean;
    admissionPacketIsNotAdmissionRecord: boolean;
    admissionPacketIsNotReviewQueueItem: boolean;
    admissionPacketIsNotKweWorkItem: boolean;
    admissionPacketIsNotConfirmation: boolean;
    admissionPacketIsNotDecisionRecord: boolean;
    admissionPacketIsNotWaesResult: boolean;
    admissionPacketIsNotBusinessWriteback: boolean;
    admissionDecisionIsDisplayOnly: boolean;
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
  noWriteGuards: GfisAssistantRepairHandoffReviewAdmissionNoWrite;
}
