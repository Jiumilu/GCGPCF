import type { BrainPkcKweQueueSurface } from "./brain-pkc-kwe-queue-read-model";

export type KweQueueActionType =
  | "submit_evidence"
  | "request_repair"
  | "escalate_committee"
  | "request_freeze"
  | "add_comment"
  | "metadata_only_review"
  | "acknowledge_blocked";

export type KweQueueActionStatus =
  | "intake_received"
  | "validation_required"
  | "committee_request_candidate"
  | "freeze_request_candidate"
  | "blocked";

export interface KweQueueActionIntakeNoWrite {
  writesKweWorkItem: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesWaesGateResult: 0;
  writesBusinessSystem: 0;
  writesTargetReceipt: 0;
  writesCommitteeDecisionCompletion: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesQuotaTransfer: 0;
  writesBountySettlement: 0;
  writesExternalApi: 0;
}

export interface KweQueueActionIntakeRequest {
  requestId: string;
  tenantId: string;
  projectId: string;
  sourceViewRef: string;
  routeRef: string;
  surface: BrainPkcKweQueueSurface;
  actorId: string;
  actionType: KweQueueActionType;
  actionStatus: KweQueueActionStatus;
  payloadRefs: string[];
  evidenceRefs: string[];
  requiredFollowups: string[];
  blockedReasons: string[];
  createsKweWorkItem: false;
  noWrite: KweQueueActionIntakeNoWrite;
}

export interface KweQueueActionIntakeRequestPolicy {
  policyId: "okf.kwe_queue_action_intake_request_policy";
  version: string;
  surfaces: BrainPkcKweQueueSurface[];
  actionTypes: KweQueueActionType[];
  actionStatuses: KweQueueActionStatus[];
  hardBoundaries: {
    requestOnly: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    intakeIsNotApprovalCompletion: boolean;
    intakeIsNotCommitteeDecisionCompletion: boolean;
    intakeIsNotBusinessWriteback: boolean;
    blockedQueueCannotApprove: boolean;
    metadataOnlyCannotIncludeRawContent: boolean;
    evidenceSubmissionRequiresPayloadOrEvidence: boolean;
  };
  noWriteGuards: KweQueueActionIntakeNoWrite;
}
