import type { WaesGateStatus } from "./waes-gate";

export type KweConfirmationWorkpackTargetType =
  | "fact_candidate"
  | "sop_candidate"
  | "writeback_candidate"
  | "contribution_candidate"
  | "revenue_candidate";

export type KweConfirmationReviewerType = "human" | "committee";

export type KweConfirmationDecisionOption =
  | "allow_accept"
  | "request_repair"
  | "reject"
  | "escalate_committee"
  | "freeze";

export type KweConfirmationSensitiveHandling =
  | "none"
  | "redaction_required"
  | "metadata_only"
  | "controlled_original";

export type KweConfirmationWorkpackResult =
  | "ready_for_human_review"
  | "ready_for_committee_review"
  | "repair_required"
  | "blocked";

export interface KweConfirmationWorkpack {
  id: string;
  tenantId: string;
  workItemId: string;
  targetObjectId: string;
  targetObjectType: KweConfirmationWorkpackTargetType;
  poolRefs: string[];
  sourceRefs: string[];
  evidenceRefs: string[];
  waesGateRefs: string[];
  waesGateStatus: WaesGateStatus;
  reviewerType: KweConfirmationReviewerType;
  reviewerRefs: string[];
  committeeTriggerReason?: string;
  decisionOptions: KweConfirmationDecisionOption[];
  requiredActions: string[];
  sensitiveHandling: KweConfirmationSensitiveHandling;
  containsRawContent: boolean;
  missingEvidenceRefs: string[];
  harnessEvidenceRefs: string[];
  workpackResult: KweConfirmationWorkpackResult;
  noWrite: true;
}

export interface KweConfirmationWorkpackPolicy {
  policyId: "okf.kwe_confirmation_workpack_policy";
  version: string;
  requiredFields: string[];
  targetObjectTypes: KweConfirmationWorkpackTargetType[];
  reviewerTypes: KweConfirmationReviewerType[];
  decisionOptions: KweConfirmationDecisionOption[];
  sensitiveHandlingModes: KweConfirmationSensitiveHandling[];
  workpackResults: KweConfirmationWorkpackResult[];
  integrityRules: {
    workItemAndTargetObjectMustCrossReference: boolean;
    sourceRefsRequired: boolean;
    evidenceRefsRequired: boolean;
    waesGateRefsRequired: boolean;
    metadataOnlyCannotIncludeRawContent: boolean;
    humanReviewerCannotCompleteCommitteeDecision: boolean;
    committeeReviewerRequiresTriggerReason: boolean;
    missingEvidenceCannotHaveAcceptOnlyDecision: boolean;
    blockedGateCannotBeHumanAccepted: boolean;
    committeeRequiredGateCannotBeHumanAccepted: boolean;
    workpackPassIsNotFactConfirmation: boolean;
    workpackPassIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: {
    writesKweWorkItem: 0;
    writesKdsFact: 0;
    writesWaesGateResult: 0;
    writesBusinessSystem: 0;
    writesRevenueOrScoreConfirmation: 0;
    writesQuotaTransfer: 0;
    writesBountySettlement: 0;
    writesCommitteeDecisionCompletion: 0;
    writesExternalApi: 0;
  };
}
