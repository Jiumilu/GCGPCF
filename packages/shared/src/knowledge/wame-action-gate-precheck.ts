import type { KweQueueActionType } from "./kwe-queue-action-intake-request";
import type { WameGateType } from "./wame-gate";
import type { WameReasonCode, WameReviewerRequirement } from "./wame-gate-io";

export type WameActionGatePrecheckStatus =
  | "precheck_passed"
  | "repair_required"
  | "human_required"
  | "committee_required"
  | "freeze_required"
  | "blocked";

export interface WameActionGatePrecheckNoWrite {
  writesWameGateResult: 0;
  writesKweWorkItem: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesBusinessSystem: 0;
  writesTargetReceipt: 0;
  writesCommitteeDecisionCompletion: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesQuotaTransfer: 0;
  writesBountySettlement: 0;
  writesExternalApi: 0;
}

export interface WameActionGatePrecheck {
  precheckId: string;
  workpackRef: string;
  tenantId: string;
  projectId: string;
  routeRef: string;
  actionType: KweQueueActionType;
  requestedGateTypes: WameGateType[];
  precheckStatus: WameActionGatePrecheckStatus;
  reasonCodes: WameReasonCode[];
  requiredActions: string[];
  reviewerRequirement: WameReviewerRequirement;
  harnessEvidenceRequired: boolean;
  createsWameGateResult: false;
  createsKweWorkItem: false;
  promotesLifecycle: false;
  noWrite: WameActionGatePrecheckNoWrite;
}

export interface WameActionGatePrecheckPolicy {
  policyId: "okf.wame_action_gate_precheck_policy";
  version: string;
  requestedGateTypes: WameGateType[];
  precheckStatuses: WameActionGatePrecheckStatus[];
  reasonCodes: WameReasonCode[];
  reviewerRequirements: WameReviewerRequirement[];
  hardBoundaries: {
    precheckOnly: boolean;
    createsWameGateResultMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    precheckIsNotGateResult: boolean;
    precheckIsNotApprovalCompletion: boolean;
    precheckIsNotCommitteeDecisionCompletion: boolean;
    precheckIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: WameActionGatePrecheckNoWrite;
}
