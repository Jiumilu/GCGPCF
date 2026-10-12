import type {
  GfisAssistantRepairPromptBlockedAction,
} from "./gfis-assistant-repair-prompt-checklist";
import type {
  GfisAssistantWameGuidanceSurface,
} from "./gfis-assistant-wame-guidance-packet";

export type GfisAssistantRepairSubmissionIntakeStatus =
  | "draft"
  | "ready_for_review"
  | "repair_required"
  | "blocked";

export type GfisAssistantRepairSubmissionRecommendedRoute =
  | "human_review"
  | "committee_review"
  | "metadata_boundary_review"
  | "freeze_review"
  | "blocked_hold";

export type GfisAssistantRepairSubmissionDisplayAction =
  | "show_intake_summary"
  | "show_required_refs"
  | "show_metadata_boundary"
  | "show_recommended_route"
  | "show_blocked_reason";

export type GfisAssistantRepairSubmissionBlockedAction =
  | "persist_evidence"
  | "complete_committee_decision"
  | GfisAssistantRepairPromptBlockedAction;

export interface GfisAssistantRepairSubmissionIntakeNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWameGateResult: 0;
  writesKweWorkItem: 0;
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

export interface GfisAssistantRepairSubmissionMetadataRefBundle {
  objectRefs: string[];
  sourceRefs: string[];
  controlledOriginalRefs: string[];
  metadataOnly: boolean;
}

export interface GfisAssistantRepairSubmissionIntake {
  intakeId: string;
  checklistRef: string;
  guidancePacketRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWameGuidanceSurface;
  intakeStatus: GfisAssistantRepairSubmissionIntakeStatus;
  recommendedRoute: GfisAssistantRepairSubmissionRecommendedRoute;
  submittedItemRefs: string[];
  metadataRefBundle: GfisAssistantRepairSubmissionMetadataRefBundle;
  evidenceHintRefs: string[];
  blockedReasonRefs: string[];
  blockedActions: GfisAssistantRepairSubmissionBlockedAction[];
  allowedDisplayActions: GfisAssistantRepairSubmissionDisplayAction[];
  submitsEvidence: false;
  persistsEvidence: false;
  createsGapRecord: false;
  createsBountyRecord: false;
  createsKweWorkItem: false;
  createsWameGateResult: false;
  routesToHumanQueue: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairSubmissionIntakeNoWrite;
}

export interface GfisAssistantRepairSubmissionIntakePolicy {
  policyId: "okf.gfis_assistant_repair_submission_intake_policy";
  version: string;
  intakeStatuses: GfisAssistantRepairSubmissionIntakeStatus[];
  recommendedRoutes: GfisAssistantRepairSubmissionRecommendedRoute[];
  allowedDisplayActions: GfisAssistantRepairSubmissionDisplayAction[];
  blockedActions: GfisAssistantRepairSubmissionBlockedAction[];
  hardBoundaries: {
    intakeOnly: boolean;
    intakeIsNotSubmission: boolean;
    intakeIsNotEvidenceRecord: boolean;
    intakeIsNotKweWorkItem: boolean;
    intakeIsNotGapOrBounty: boolean;
    intakeIsNotWameResult: boolean;
    intakeIsNotBusinessWriteback: boolean;
    intakeIsNotCommitteeDecision: boolean;
    routesAreRecommendationsOnly: boolean;
    submitsEvidenceMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    createsGapRecordMustBeFalse: boolean;
    createsBountyRecordMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    createsWameGateResultMustBeFalse: boolean;
    routesToHumanQueueMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    completesCommitteeDecisionMustBeFalse: boolean;
  };
  noWriteGuards: GfisAssistantRepairSubmissionIntakeNoWrite;
}
