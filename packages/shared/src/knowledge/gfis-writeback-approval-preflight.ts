import type { TargetSystem } from "./fact-candidate";
import type { GfisWritebackCandidateBatchNoWrite } from "./gfis-writeback-candidate-batch-diff";
import type { KdsLifecycleTransitionAuditStatus } from "./kds-lifecycle-transition-audit-packet";
import type { KweConfirmationSensitiveHandling } from "./kwe-confirmation-workpack";
import type { KwePromotionReviewerRequirement } from "./kwe-promotion-request";
import type { WaesGateStatus } from "./waes-gate";
import type { WritebackTargetEntityType } from "./writeback-candidate";

export type GfisWritebackApprovalPreflightStatus =
  | "preflight_required"
  | "human_required"
  | "committee_required"
  | "metadata_only_required"
  | "repair_required"
  | "blocked";

export interface GfisWritebackApprovalPreflightNoWrite
  extends GfisWritebackCandidateBatchNoWrite {
  writesKdsLifecycle: 0;
  writesTargetReceipt: 0;
}

export interface GfisWritebackApprovalPreflightItem {
  preflightId: string;
  candidateId: string;
  targetSystem: Extract<TargetSystem, "GFIS">;
  targetEntityType: WritebackTargetEntityType;
  targetEntityId: string;
  batchDiffRef: string;
  lifecycleAuditRefs: string[];
  fieldPaths: string[];
  evidenceRefs: string[];
  waesGateRefs: string[];
  harnessEvidenceRefs: string[];
  sensitiveHandling: KweConfirmationSensitiveHandling;
  waesGateStatus: Extract<
    WaesGateStatus,
    "pending" | "passed" | "blocked" | "human_required" | "committee_required"
  >;
  lifecycleAuditStatus: KdsLifecycleTransitionAuditStatus;
  reviewerRequirement: KwePromotionReviewerRequirement;
  preflightStatus: GfisWritebackApprovalPreflightStatus;
  requiredActions: string[];
  blockedReasons: string[];
  approvalEligible: false;
  businessWriteAllowed: false;
  targetReceiptRefs: [];
  noWrite: GfisWritebackApprovalPreflightNoWrite;
}

export interface GfisWritebackApprovalPreflightBatch {
  preflightBatchId: string;
  tenantId: string;
  projectId: string;
  targetSystem: Extract<TargetSystem, "GFIS">;
  basedOnBatchDiffRef: string;
  createdBy: string;
  dryRun: true;
  items: GfisWritebackApprovalPreflightItem[];
  batchNoWrite: GfisWritebackApprovalPreflightNoWrite;
}

export interface GfisWritebackApprovalPreflightPolicy {
  policyId: "okf.gfis_writeback_approval_preflight_policy";
  version: string;
  preflightStatuses: GfisWritebackApprovalPreflightStatus[];
  hardBoundaries: {
    dryRunRequired: boolean;
    approvalEligibleMustBeFalse: boolean;
    businessWriteAllowedMustBeFalse: boolean;
    targetReceiptsForbidden: boolean;
    blockedGateBlocksPreflight: boolean;
    committeeGateRequiresCommitteePath: boolean;
    metadataOnlyRequiresMetadataPath: boolean;
    lifecycleBlockBlocksPreflight: boolean;
    missingEvidenceRepairsOrBlocks: boolean;
    preflightPassIsNotWritebackApproval: boolean;
  };
  noWriteGuards: GfisWritebackApprovalPreflightNoWrite;
}
