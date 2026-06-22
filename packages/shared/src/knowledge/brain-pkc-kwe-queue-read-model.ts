import type {
  KweApprovalRouteQueue,
  KweApprovalRouteQueueSummary,
} from "./kwe-approval-route-packet";

export type BrainPkcKweQueueSurface = "brain" | "pkc" | "gfis_assistant";

export type BrainPkcKweQueueScope =
  | "kwe_queue_overview"
  | "my_kwe_tasks"
  | "gfis_writeback_queue"
  | "committee_queue"
  | "blocked_queue";

export type BrainPkcKweQueueVisibility =
  | "own_only"
  | "project_authorized"
  | "governance_aggregate"
  | "committee_authorized";

export type BrainPkcKweQueueDisplayMode =
  | "summary_only"
  | "queue_detail"
  | "metadata_only"
  | "masked_cross_unit";

export type BrainPkcKweQueueBlockedAction =
  | "create_kwe_work_item"
  | "complete_approval"
  | "complete_committee_decision"
  | "approve_gfis_writeback"
  | "mutate_kds_lifecycle"
  | "write_waes_gate_result"
  | "write_business_system"
  | "call_external_api";

export interface BrainPkcKweQueueFilter {
  routeQueues: KweApprovalRouteQueue[];
  targetSystem?: "GFIS";
  sensitiveHandling?: "none" | "redaction_required" | "metadata_only" | "controlled_original";
  includeBlocked: boolean;
}

export interface BrainPkcKweQueueNoWrite {
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

export interface BrainPkcKweQueueReadModel {
  viewId: string;
  surface: BrainPkcKweQueueSurface;
  tenantId: string;
  viewerId: string;
  projectId: string;
  scope: BrainPkcKweQueueScope;
  routePacketRefs: string[];
  visibleRouteRefs: string[];
  maskedRouteRefs: string[];
  queueSummary: KweApprovalRouteQueueSummary;
  filter: BrainPkcKweQueueFilter;
  visibility: BrainPkcKweQueueVisibility;
  displayMode: BrainPkcKweQueueDisplayMode;
  blockedActions: BrainPkcKweQueueBlockedAction[];
  noWrite: BrainPkcKweQueueNoWrite;
}

export interface BrainPkcKweQueueReadModelPolicy {
  policyId: "okf.brain_pkc_kwe_queue_read_model_policy";
  version: string;
  surfaces: BrainPkcKweQueueSurface[];
  scopes: BrainPkcKweQueueScope[];
  visibilityModes: BrainPkcKweQueueVisibility[];
  displayModes: BrainPkcKweQueueDisplayMode[];
  blockedActions: BrainPkcKweQueueBlockedAction[];
  hardBoundaries: {
    readModelOnly: boolean;
    pkcDefaultsToOwnOrAuthorizedOnly: boolean;
    gfisAssistantCannotCompleteApproval: boolean;
    brainCrossUnitDetailRequiresGovernanceOrCommitteeAuthorization: boolean;
    maskedCrossUnitMustNotExposeRouteIds: boolean;
    queueViewIsNotWorkItemCreation: boolean;
    queueViewIsNotApprovalCompletion: boolean;
    queueViewIsNotBusinessWriteback: boolean;
  };
  noWriteAssertions: BrainPkcKweQueueNoWrite;
}
