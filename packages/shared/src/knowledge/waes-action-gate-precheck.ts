import type { KweQueueActionType } from "./kwe-queue-action-intake-request";
import type { WaesGateType } from "./waes-gate";
import type { WaesReasonCode, WaesReviewerRequirement } from "./waes-gate-io";

export type WaesActionGatePrecheckStatus =
  | "precheck_passed"
  | "repair_required"
  | "human_required"
  | "committee_required"
  | "freeze_required"
  | "blocked";

export interface WaesActionGatePrecheckNoWrite {
  writesWaesGateResult: 0;
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

export interface WaesActionGatePrecheck {
  precheckId: string;
  workpackRef: string;
  tenantId: string;
  projectId: string;
  routeRef: string;
  actionType: KweQueueActionType;
  requestedGateTypes: WaesGateType[];
  precheckStatus: WaesActionGatePrecheckStatus;
  reasonCodes: WaesReasonCode[];
  requiredActions: string[];
  reviewerRequirement: WaesReviewerRequirement;
  harnessEvidenceRequired: boolean;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  promotesLifecycle: false;
  noWrite: WaesActionGatePrecheckNoWrite;
}

export interface WaesActionGatePrecheckPolicy {
  policyId: "okf.waes_action_gate_precheck_policy";
  version: string;
  requestedGateTypes: WaesGateType[];
  precheckStatuses: WaesActionGatePrecheckStatus[];
  reasonCodes: WaesReasonCode[];
  reviewerRequirements: WaesReviewerRequirement[];
  hardBoundaries: {
    precheckOnly: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    precheckIsNotGateResult: boolean;
    precheckIsNotApprovalCompletion: boolean;
    precheckIsNotCommitteeDecisionCompletion: boolean;
    precheckIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: WaesActionGatePrecheckNoWrite;
}
