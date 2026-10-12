import type { KnowledgeLifecycle, KnowledgeObjectType } from "./object";
import type { WameGateStatus, WameGateType } from "./wame-gate";

export type WameReasonCode =
  | "missing_source"
  | "missing_evidence"
  | "t5_ai_only"
  | "acl_unknown"
  | "sensitive_raw_content"
  | "owner_confirmation_missing"
  | "committee_required_by_policy"
  | "revenue_basis_missing"
  | "duplicate_or_conflicting_contribution"
  | "major_violation_risk";

export type WameAllowedOperation =
  | "metadata_only"
  | "weak_rag_reference"
  | "strong_rag_reference"
  | "create_kwe_work_item"
  | "create_confirmation_workpack"
  | "create_writeback_candidate"
  | "create_redaction_request"
  | "create_committee_review"
  | "freeze_object"
  | "block_operation";

export type WameReviewerRequirement =
  | "none"
  | "human_required"
  | "committee_required"
  | "governance_owner_required";

export interface WameGateCheckInput {
  gateId: string;
  tenantId: string;
  gateType: WameGateType;
  targetObjectType: KnowledgeObjectType;
  targetObjectId: string;
  policyRefs: string[];
  sourceRefs: string[];
  evidenceRefs: string[];
  aclRefs: string[];
  riskSignals: WameReasonCode[];
  requestedBy: string;
  dryRun: true;
}

export interface WameGateCheckOutput {
  gateId: string;
  result: WameGateStatus;
  reasonCodes: WameReasonCode[];
  requiredActions: string[];
  nextState: KnowledgeLifecycle;
  allowedOperations: WameAllowedOperation[];
  reviewerRequirement: WameReviewerRequirement;
  harnessEvidenceRequired: boolean;
  writesGateResult: false;
  writesBusinessSystem: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
}

export interface WameHardStopRule {
  gateType: WameGateType;
  triggers: WameReasonCode[];
  defaultResult: WameGateStatus;
}

export interface WameGateIoPolicy {
  policyId: string;
  version: string;
  minimumInputFields: string[];
  minimumOutputFields: string[];
  reasonCodes: WameReasonCode[];
  hardStopRules: WameHardStopRule[];
  allowedOperations: WameAllowedOperation[];
  hardBoundaries: {
    p0P1RequiresDryRun: boolean;
    noDirectGateResultPersistence: boolean;
    noBusinessWriteback: boolean;
    noRevenueDistribution: boolean;
    noExternalApiWrite: boolean;
    humanOrCommitteeRequiredForFinality: boolean;
  };
  noWriteAssertions: {
    writesGateResult: 0;
    writesBusinessSystem: 0;
    writesRevenueDistribution: 0;
    writesExternalApi: 0;
  };
}
