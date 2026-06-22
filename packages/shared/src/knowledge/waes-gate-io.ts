import type { KnowledgeLifecycle, KnowledgeObjectType } from "./object";
import type { WaesGateStatus, WaesGateType } from "./waes-gate";

export type WaesReasonCode =
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

export type WaesAllowedOperation =
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

export type WaesReviewerRequirement =
  | "none"
  | "human_required"
  | "committee_required"
  | "governance_owner_required";

export interface WaesGateCheckInput {
  gateId: string;
  tenantId: string;
  gateType: WaesGateType;
  targetObjectType: KnowledgeObjectType;
  targetObjectId: string;
  policyRefs: string[];
  sourceRefs: string[];
  evidenceRefs: string[];
  aclRefs: string[];
  riskSignals: WaesReasonCode[];
  requestedBy: string;
  dryRun: true;
}

export interface WaesGateCheckOutput {
  gateId: string;
  result: WaesGateStatus;
  reasonCodes: WaesReasonCode[];
  requiredActions: string[];
  nextState: KnowledgeLifecycle;
  allowedOperations: WaesAllowedOperation[];
  reviewerRequirement: WaesReviewerRequirement;
  harnessEvidenceRequired: boolean;
  writesGateResult: false;
  writesBusinessSystem: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
}

export interface WaesHardStopRule {
  gateType: WaesGateType;
  triggers: WaesReasonCode[];
  defaultResult: WaesGateStatus;
}

export interface WaesGateIoPolicy {
  policyId: string;
  version: string;
  minimumInputFields: string[];
  minimumOutputFields: string[];
  reasonCodes: WaesReasonCode[];
  hardStopRules: WaesHardStopRule[];
  allowedOperations: WaesAllowedOperation[];
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
