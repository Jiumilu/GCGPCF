import type { TargetSystem } from "./fact-candidate";
import type {
  GfisWritebackApprovalPreflightStatus,
} from "./gfis-writeback-approval-preflight";
import type { KweConfirmationSensitiveHandling } from "./kwe-confirmation-workpack";
import type { KwePromotionReviewerRequirement } from "./kwe-promotion-request";
import type { WritebackTargetEntityType } from "./writeback-candidate";

export type KweApprovalRouteQueue =
  | "human_queue"
  | "committee_queue"
  | "metadata_only_queue"
  | "repair_queue"
  | "blocked_queue";

export type KweApprovalRouteStatus =
  | "route_ready"
  | "preflight_required"
  | "repair_required"
  | "blocked";

export interface KweApprovalRouteNoWrite {
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

export interface KweApprovalRouteItem {
  routeId: string;
  preflightRef: string;
  candidateId: string;
  targetSystem: Extract<TargetSystem, "GFIS">;
  targetEntityType: WritebackTargetEntityType;
  targetEntityId: string;
  preflightStatus: GfisWritebackApprovalPreflightStatus;
  reviewerRequirement: KwePromotionReviewerRequirement;
  sensitiveHandling: KweConfirmationSensitiveHandling;
  evidenceRefs: string[];
  waesGateRefs: string[];
  lifecycleAuditRefs: string[];
  routeQueue: KweApprovalRouteQueue;
  routeStatus: KweApprovalRouteStatus;
  requiredActions: string[];
  blockedReasons: string[];
  createsKweWorkItem: false;
  noWrite: KweApprovalRouteNoWrite;
}

export interface KweApprovalRouteQueueSummary {
  humanQueue: number;
  committeeQueue: number;
  metadataOnlyQueue: number;
  repairQueue: number;
  blockedQueue: number;
}

export interface KweApprovalRoutePacket {
  routePacketId: string;
  tenantId: string;
  projectId: string;
  basedOnPreflightBatchRef: string;
  createdBy: string;
  dryRun: true;
  items: KweApprovalRouteItem[];
  queueSummary: KweApprovalRouteQueueSummary;
  packetNoWrite: KweApprovalRouteNoWrite;
}

export interface KweApprovalRoutePacketPolicy {
  policyId: "okf.kwe_approval_route_packet_policy";
  version: string;
  routeQueues: KweApprovalRouteQueue[];
  routeStatuses: KweApprovalRouteStatus[];
  hardBoundaries: {
    dryRunRequired: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    routeReadyIsNotApprovalCompletion: boolean;
    blockedRoutesCannotLeaveBlockedQueue: boolean;
    committeeRequiredRoutesCannotBeHumanQueue: boolean;
    metadataOnlyRoutesCannotIncludeRawContent: boolean;
    repairRoutesCannotBeRouteReady: boolean;
    routePacketIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: KweApprovalRouteNoWrite;
}
