import type {
  GfisAssistantRepairReviewDecisionDraftBlockedAction,
} from "./gfis-assistant-repair-review-decision-draft";
import type {
  GfisAssistantRepairSubmissionMetadataRefBundle,
} from "./gfis-assistant-repair-submission-intake";
import type {
  GfisAssistantWaesGuidanceSurface,
} from "./gfis-assistant-waes-guidance-packet";

export type GfisAssistantRepairDraftHandoffPacketType =
  | "human_review_handoff"
  | "metadata_boundary_handoff"
  | "committee_agenda_handoff"
  | "freeze_review_handoff"
  | "blocked_hold_handoff";

export type GfisAssistantRepairDraftHandoffPacketStatus =
  | "draft"
  | "ready_for_handoff_review"
  | "needs_repair"
  | "blocked"
  | "metadata_only";

export type GfisAssistantRepairDraftHandoffTargetCandidate =
  | "kwe_human_review_candidate"
  | "metadata_boundary_review_candidate"
  | "committee_agenda_candidate"
  | "freeze_review_candidate"
  | "blocked_hold_candidate";

export type GfisAssistantRepairDraftHandoffPacketDisplayAction =
  | "show_handoff_packet"
  | "show_target_candidate"
  | "show_required_repair"
  | "show_metadata_boundary"
  | "show_committee_agenda_note"
  | "show_freeze_note"
  | "show_no_write_notice";

export type GfisAssistantRepairDraftHandoffPacketBlockedAction =
  | "create_handoff_record"
  | GfisAssistantRepairReviewDecisionDraftBlockedAction;

export interface GfisAssistantRepairDraftHandoffPacketNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesHandoffRecord: 0;
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

export interface GfisAssistantRepairDraftHandoffPacket {
  handoffPacketId: string;
  decisionDraftRef: string;
  reviewPacketRef: string;
  intakeRef: string;
  checklistRef: string;
  guidancePacketRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWaesGuidanceSurface;
  handoffType: GfisAssistantRepairDraftHandoffPacketType;
  handoffStatus: GfisAssistantRepairDraftHandoffPacketStatus;
  targetCandidate: GfisAssistantRepairDraftHandoffTargetCandidate;
  handoffNoteRefs: string[];
  requiredRepairRefs: string[];
  metadataRefBundle: GfisAssistantRepairSubmissionMetadataRefBundle;
  evidenceHintRefs: string[];
  blockedReasonRefs: string[];
  blockedActions: GfisAssistantRepairDraftHandoffPacketBlockedAction[];
  allowedDisplayActions: GfisAssistantRepairDraftHandoffPacketDisplayAction[];
  submitsEvidence: false;
  persistsEvidence: false;
  createsHandoffRecord: false;
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
  noWrite: GfisAssistantRepairDraftHandoffPacketNoWrite;
}

export interface GfisAssistantRepairDraftHandoffPacketPolicy {
  policyId: "okf.gfis_assistant_repair_draft_handoff_packet_policy";
  version: string;
  handoffTypes: GfisAssistantRepairDraftHandoffPacketType[];
  handoffStatuses: GfisAssistantRepairDraftHandoffPacketStatus[];
  targetCandidates: GfisAssistantRepairDraftHandoffTargetCandidate[];
  allowedDisplayActions: GfisAssistantRepairDraftHandoffPacketDisplayAction[];
  blockedActions: GfisAssistantRepairDraftHandoffPacketBlockedAction[];
  hardBoundaries: {
    handoffPacketOnly: boolean;
    handoffPacketIsNotHandoffRecord: boolean;
    handoffPacketIsNotReviewQueueItem: boolean;
    handoffPacketIsNotConfirmation: boolean;
    handoffPacketIsNotCommitteeDecision: boolean;
    handoffPacketIsNotDecisionRecord: boolean;
    handoffPacketIsNotWaesResult: boolean;
    handoffPacketIsNotBusinessWriteback: boolean;
    targetCandidateIsRecommendationOnly: boolean;
    submitsEvidenceMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    createsHandoffRecordMustBeFalse: boolean;
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
  noWriteGuards: GfisAssistantRepairDraftHandoffPacketNoWrite;
}
