import type { EvidenceKind } from "./evidence";

export type HarnessEvidenceReferenceGroup =
  | "object_refs"
  | "source_refs"
  | "gate_refs"
  | "loop_refs"
  | "decision_refs";

export type HarnessEvidenceIntegrityStatus =
  | "passed"
  | "blocked"
  | "repair_required";

export interface HarnessEvidenceIntegrityRecord {
  evidenceId: string;
  tenantId: string;
  evidenceKind: EvidenceKind;
  title: string;
  objectRefs: string[];
  sourceRefs: string[];
  gateRefs: string[];
  loopRefs: string[];
  decisionRefs: string[];
  contentHash?: string;
  controlledOriginalRef?: string;
  summary: string;
  createdBy: string;
  createdAt: string;
  metadata: Record<string, unknown>;
  integrityStatus: HarnessEvidenceIntegrityStatus;
  unresolvedRefs: string[];
  sensitiveRawContentStored: false;
  passedIsBusinessCompletion: false;
  writesKdsFact: false;
  writesBusinessSystem: false;
  writesExternalApi: false;
}

export interface HarnessEvidenceIntegrityPolicy {
  policyId: string;
  version: string;
  minimumEvidenceFields: string[];
  referenceGroups: HarnessEvidenceReferenceGroup[];
  evidenceKinds: EvidenceKind[];
  integrityStatuses: HarnessEvidenceIntegrityStatus[];
  integrityRules: Array<{
    id: string;
    required: boolean;
    description: string;
  }>;
  hardBoundaries: {
    evidenceCanCreateFormalFact: false;
    evidenceCanWriteBusinessSystem: false;
    evidenceCanDistributeRevenue: false;
    evidenceCanConfirmScore: false;
    evidenceCanTransferQuota: false;
    evidenceCanSettleBounty: false;
    evidenceCanCompleteCommitteeDecision: false;
    evidenceCanAllowExternalShare: false;
    sensitiveRawContentAllowed: false;
    passedIsBusinessCompletion: false;
  };
  noWriteAssertions: {
    writesKdsFact: 0;
    writesBusinessSystem: 0;
    writesRevenueDistribution: 0;
    writesScoreConfirmation: 0;
    writesQuotaTransfer: 0;
    writesBountySettlement: 0;
    writesCommitteeDecisionCompletion: 0;
    writesExternalSharePermission: 0;
    writesExternalApi: 0;
  };
}
