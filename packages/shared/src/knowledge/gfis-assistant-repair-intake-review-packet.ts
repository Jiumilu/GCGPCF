import type {
  GfisAssistantRepairSubmissionBlockedAction,
  GfisAssistantRepairSubmissionMetadataRefBundle,
} from "./gfis-assistant-repair-submission-intake";
import type {
  GfisAssistantWaesGuidanceSurface,
} from "./gfis-assistant-waes-guidance-packet";

export type GfisAssistantRepairIntakeReviewPacketType =
  | "human_review_packet"
  | "metadata_boundary_packet"
  | "committee_review_packet"
  | "freeze_review_packet"
  | "blocked_hold_packet";

export type GfisAssistantRepairIntakeReviewPacketStatus =
  | "queued_preview"
  | "needs_repair"
  | "blocked"
  | "metadata_only";

export type GfisAssistantRepairIntakeReviewPacketDisplayAction =
  | "show_review_context"
  | "show_intake_refs"
  | "show_metadata_boundary"
  | "show_reviewer_focus"
  | "show_blocked_reason"
  | "show_no_write_notice";

export type GfisAssistantRepairIntakeReviewPacketBlockedAction =
  | "create_review_queue_item"
  | GfisAssistantRepairSubmissionBlockedAction;

export interface GfisAssistantRepairIntakeReviewPacketNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesReviewQueueItem: 0;
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

export interface GfisAssistantRepairIntakeReviewPacket {
  reviewPacketId: string;
  intakeRef: string;
  checklistRef: string;
  guidancePacketRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWaesGuidanceSurface;
  reviewType: GfisAssistantRepairIntakeReviewPacketType;
  reviewStatus: GfisAssistantRepairIntakeReviewPacketStatus;
  reviewerFocus: string[];
  intakeItemRefs: string[];
  metadataRefBundle: GfisAssistantRepairSubmissionMetadataRefBundle;
  evidenceHintRefs: string[];
  blockedReasonRefs: string[];
  blockedActions: GfisAssistantRepairIntakeReviewPacketBlockedAction[];
  allowedDisplayActions: GfisAssistantRepairIntakeReviewPacketDisplayAction[];
  submitsEvidence: false;
  persistsEvidence: false;
  createsReviewQueueItem: false;
  createsGapRecord: false;
  createsBountyRecord: false;
  createsKweWorkItem: false;
  createsWaesGateResult: false;
  routesToHumanQueue: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairIntakeReviewPacketNoWrite;
}

export interface GfisAssistantRepairIntakeReviewPacketPolicy {
  policyId: "okf.gfis_assistant_repair_intake_review_packet_policy";
  version: string;
  reviewTypes: GfisAssistantRepairIntakeReviewPacketType[];
  reviewStatuses: GfisAssistantRepairIntakeReviewPacketStatus[];
  allowedDisplayActions: GfisAssistantRepairIntakeReviewPacketDisplayAction[];
  blockedActions: GfisAssistantRepairIntakeReviewPacketBlockedAction[];
  hardBoundaries: {
    reviewPacketOnly: boolean;
    reviewPacketIsNotQueueItem: boolean;
    reviewPacketIsNotSubmission: boolean;
    reviewPacketIsNotEvidenceRecord: boolean;
    reviewPacketIsNotKweWorkItem: boolean;
    reviewPacketIsNotGapOrBounty: boolean;
    reviewPacketIsNotWaesResult: boolean;
    reviewPacketIsNotBusinessWriteback: boolean;
    reviewPacketIsNotCommitteeDecision: boolean;
    reviewerFocusIsRecommendationOnly: boolean;
    submitsEvidenceMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    createsReviewQueueItemMustBeFalse: boolean;
    createsGapRecordMustBeFalse: boolean;
    createsBountyRecordMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    routesToHumanQueueMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    completesCommitteeDecisionMustBeFalse: boolean;
  };
  noWriteGuards: GfisAssistantRepairIntakeReviewPacketNoWrite;
}
