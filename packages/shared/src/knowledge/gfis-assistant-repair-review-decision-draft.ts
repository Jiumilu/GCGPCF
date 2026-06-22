import type {
  GfisAssistantRepairIntakeReviewPacketBlockedAction,
} from "./gfis-assistant-repair-intake-review-packet";
import type {
  GfisAssistantRepairSubmissionMetadataRefBundle,
} from "./gfis-assistant-repair-submission-intake";
import type {
  GfisAssistantWaesGuidanceSurface,
} from "./gfis-assistant-waes-guidance-packet";

export type GfisAssistantRepairReviewDecisionDraftType =
  | "human_action_draft"
  | "metadata_boundary_note"
  | "committee_agenda_note"
  | "freeze_note"
  | "blocked_hold_note";

export type GfisAssistantRepairReviewDecisionDraftStatus =
  | "draft"
  | "needs_repair"
  | "blocked"
  | "metadata_only";

export type GfisAssistantRepairReviewSuggestedDisposition =
  | "request_more_evidence"
  | "keep_metadata_only"
  | "prepare_committee_agenda"
  | "keep_frozen"
  | "hold_blocked";

export type GfisAssistantRepairReviewDecisionDraftDisplayAction =
  | "show_decision_draft"
  | "show_reviewer_note"
  | "show_required_repair"
  | "show_metadata_boundary"
  | "show_committee_agenda_note"
  | "show_freeze_note"
  | "show_no_write_notice";

export type GfisAssistantRepairReviewDecisionDraftBlockedAction =
  | "create_confirmation_record"
  | "create_decision_record"
  | GfisAssistantRepairIntakeReviewPacketBlockedAction;

export interface GfisAssistantRepairReviewDecisionDraftNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
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

export interface GfisAssistantRepairReviewDecisionDraft {
  decisionDraftId: string;
  reviewPacketRef: string;
  intakeRef: string;
  checklistRef: string;
  guidancePacketRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWaesGuidanceSurface;
  draftType: GfisAssistantRepairReviewDecisionDraftType;
  draftStatus: GfisAssistantRepairReviewDecisionDraftStatus;
  suggestedDisposition: GfisAssistantRepairReviewSuggestedDisposition;
  reviewerNoteRefs: string[];
  requiredRepairRefs: string[];
  metadataRefBundle: GfisAssistantRepairSubmissionMetadataRefBundle;
  evidenceHintRefs: string[];
  blockedReasonRefs: string[];
  blockedActions: GfisAssistantRepairReviewDecisionDraftBlockedAction[];
  allowedDisplayActions: GfisAssistantRepairReviewDecisionDraftDisplayAction[];
  submitsEvidence: false;
  persistsEvidence: false;
  createsReviewQueueItem: false;
  createsConfirmationRecord: false;
  createsDecisionRecord: false;
  createsGapRecord: false;
  createsBountyRecord: false;
  createsKweWorkItem: false;
  createsWaesGateResult: false;
  routesToHumanQueue: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairReviewDecisionDraftNoWrite;
}

export interface GfisAssistantRepairReviewDecisionDraftPolicy {
  policyId: "okf.gfis_assistant_repair_review_decision_draft_policy";
  version: string;
  draftTypes: GfisAssistantRepairReviewDecisionDraftType[];
  draftStatuses: GfisAssistantRepairReviewDecisionDraftStatus[];
  suggestedDispositions: GfisAssistantRepairReviewSuggestedDisposition[];
  allowedDisplayActions: GfisAssistantRepairReviewDecisionDraftDisplayAction[];
  blockedActions: GfisAssistantRepairReviewDecisionDraftBlockedAction[];
  hardBoundaries: {
    decisionDraftOnly: boolean;
    decisionDraftIsNotConfirmation: boolean;
    decisionDraftIsNotCommitteeDecision: boolean;
    decisionDraftIsNotDecisionRecord: boolean;
    decisionDraftIsNotWaesResult: boolean;
    decisionDraftIsNotBusinessWriteback: boolean;
    suggestedDispositionIsRecommendationOnly: boolean;
    submitsEvidenceMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    createsReviewQueueItemMustBeFalse: boolean;
    createsConfirmationRecordMustBeFalse: boolean;
    createsDecisionRecordMustBeFalse: boolean;
    createsGapRecordMustBeFalse: boolean;
    createsBountyRecordMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    routesToHumanQueueMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    completesCommitteeDecisionMustBeFalse: boolean;
  };
  noWriteGuards: GfisAssistantRepairReviewDecisionDraftNoWrite;
}
