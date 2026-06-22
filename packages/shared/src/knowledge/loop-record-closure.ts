export type LoopNextActionPriority = "P0" | "P1" | "P2" | "P3";

export type LoopNextActionStatus =
  | "open"
  | "in_progress"
  | "blocked"
  | "evidence_ready"
  | "closed";

export type LoopClosureGateStatus =
  | "open"
  | "blocked"
  | "repair_required"
  | "evidence_ready"
  | "closed_for_round";

export interface LoopNextAction {
  actionId: string;
  title: string;
  priority: LoopNextActionPriority;
  ownerType: "user" | "team" | "project" | "org" | "committee" | "system";
  ownerId: string;
  requiredEvidenceRefs: string[];
  requiredGateRefs: string[];
  blockedByRefs: string[];
  status: LoopNextActionStatus;
  closeCondition: string;
}

export interface LoopClosureGate {
  status: LoopClosureGateStatus;
  validationRefs: string[];
  openP0P1ActionCount: number;
  blockedActionCount: number;
  missingOwnerCount: number;
  missingEvidenceCount: number;
  humanRequiredCount: number;
  committeeRequiredCount: number;
  closeableForRound: boolean;
  closedForRoundIsBusinessCompletion: false;
  writesAccepted: false;
  writesIntegrated: false;
  writesBusinessSystem: false;
  writesExternalApi: false;
}

export interface LoopRecordClosurePolicy {
  policyId: string;
  version: string;
  minimumLoopRecordFields: string[];
  minimumNextActionFields: string[];
  nextActionStatuses: LoopNextActionStatus[];
  closureGateStatuses: LoopClosureGateStatus[];
  closureRules: Array<{
    id: string;
    required: boolean;
    description: string;
  }>;
  hardBoundaries: {
    loopCanMarkAccepted: false;
    loopCanMarkIntegrated: false;
    loopCanMarkProductionReadiness: false;
    loopCanWriteBusinessSystem: false;
    loopCanConfirmRevenueOrScore: false;
    loopCanTransferQuota: false;
    loopCanSettleBounty: false;
    loopCanCompleteCommitteeDecision: false;
    loopCanWriteExternalApi: false;
    closedForRoundIsBusinessCompletion: false;
  };
  noWriteAssertions: {
    writesAccepted: 0;
    writesIntegrated: 0;
    writesBusinessSystem: 0;
    writesRevenueOrScoreConfirmation: 0;
    writesQuotaTransfer: 0;
    writesBountySettlement: 0;
    writesCommitteeDecisionCompletion: 0;
    writesExternalApi: 0;
  };
}
