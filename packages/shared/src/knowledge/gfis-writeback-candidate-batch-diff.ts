import type { TargetSystem, WritebackStatus } from "./fact-candidate";
import type { KweConfirmationSensitiveHandling } from "./kwe-confirmation-workpack";
import type { WritebackTargetEntityType } from "./writeback-candidate";
import type { WaesGateStatus } from "./waes-gate";

export type GfisWritebackBatchDiffAction =
  | "candidate_only"
  | "return_for_repair"
  | "block_writeback"
  | "escalate_human"
  | "escalate_committee"
  | "metadata_only";

export type GfisWritebackBatchKweNextAction =
  | "none"
  | "create_confirmation_workpack"
  | "request_evidence_repair"
  | "create_committee_review"
  | "freeze_or_block";

export type GfisWritebackBatchRiskLevel =
  | "low"
  | "medium"
  | "high"
  | "critical";

export interface GfisWritebackCandidateFieldDiff {
  fieldPath: string;
  currentValue: unknown;
  proposedValue: unknown;
  diffReason: string;
  riskLevel: GfisWritebackBatchRiskLevel;
}

export interface GfisWritebackCandidateBatchNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesKdsAcceptedFact: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesExternalApi: 0;
}

export interface GfisWritebackCandidateBatchDiffItem {
  candidateId: string;
  targetEntityType: WritebackTargetEntityType;
  targetEntityId: string;
  fieldDiffs: GfisWritebackCandidateFieldDiff[];
  basedOnObjectRefs: string[];
  evidenceRefs: string[];
  poolRefs: string[];
  waesGateStatus: Extract<
    WaesGateStatus,
    "pending" | "passed" | "blocked" | "human_required" | "committee_required"
  >;
  writebackStatus: Exclude<WritebackStatus, "not_applicable">;
  diffAction: GfisWritebackBatchDiffAction;
  sensitiveHandling: KweConfirmationSensitiveHandling;
  kweNextAction: GfisWritebackBatchKweNextAction;
  approvedForBusinessWrite: false;
  targetReceiptRefs: [];
  noWrite: GfisWritebackCandidateBatchNoWrite;
}

export interface GfisWritebackCandidateBatchDiff {
  batchId: string;
  tenantId: string;
  projectId: string;
  targetSystem: Extract<TargetSystem, "GFIS">;
  createdBy: string;
  dryRun: true;
  items: GfisWritebackCandidateBatchDiffItem[];
  batchNoWrite: GfisWritebackCandidateBatchNoWrite;
}

export interface GfisWritebackCandidateBatchDiffPolicy {
  policyId: "okf.gfis_writeback_candidate_batch_diff_policy";
  version: string;
  diffActions: GfisWritebackBatchDiffAction[];
  sensitiveHandlingModes: KweConfirmationSensitiveHandling[];
  kweNextActions: GfisWritebackBatchKweNextAction[];
  riskLevels: GfisWritebackBatchRiskLevel[];
  hardBoundaries: {
    dryRunRequired: boolean;
    approvedForBusinessWriteMustBeFalse: boolean;
    targetReceiptsForbidden: boolean;
    writtenBackStatusForbidden: boolean;
    waesPassedIsCandidateOnly: boolean;
    sensitiveRawContentForbidden: boolean;
    missingEvidenceBlocksOrRepairs: boolean;
    podFinanceQualityDisputeRequiresMetadataOrControlledOriginal: boolean;
  };
  noWriteAssertions: GfisWritebackCandidateBatchNoWrite;
}
