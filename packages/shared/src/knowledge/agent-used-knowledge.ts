import type { KnowledgeDomain, RagAdmission } from "./object";
import type { WaesGateStatus } from "./waes-gate";

export type AgentCapabilityType =
  | "rag_query"
  | "candidate_fact_generation"
  | "candidate_sop_generation"
  | "writeback_suggestion"
  | "document_acceptance_check"
  | "governance_review";

export type AgentOverreadRiskSignal =
  | "cross_tenant_access"
  | "cross_supplier_access"
  | "acl_missing"
  | "domain_scope_mismatch"
  | "rag_blocked_used"
  | "t5_used_as_final_fact"
  | "sensitive_raw_content_requested"
  | "unverified_strong_conclusion"
  | "promotion_bypass_attempt"
  | "external_share_without_gate";

export type AgentKnowledgeUseOutcome =
  | "candidate_fact"
  | "candidate_sop"
  | "candidate_writeback"
  | "candidate_gap"
  | "candidate_risk"
  | "candidate_summary"
  | "metadata_only_answer"
  | "blocked_with_reason";

export interface AgentUsedKnowledgeRecord {
  invocationId: string;
  tenantId: string;
  agentId: string;
  userId: string;
  capabilityId: string;
  capabilityType: AgentCapabilityType;
  purpose: string;
  requestedScope: string;
  allowedScope: string;
  requestedDomains: KnowledgeDomain[];
  allowedDomains: KnowledgeDomain[];
  poolRefs: string[];
  inputObjectRefs: string[];
  retrievedObjectRefs: string[];
  sourceRefs: string[];
  evidenceRefs: string[];
  waesGateRefs: string[];
  ragAdmissionsUsed: RagAdmission[];
  overreadSignals: AgentOverreadRiskSignal[];
  outputCandidateRefs: string[];
  outcome: AgentKnowledgeUseOutcome;
  waesGateStatus: WaesGateStatus;
  harnessEvidenceRef?: string;
  createdAt: string;
  writesAccepted: false;
  writesPublic: false;
  writesGovernanceEvidence: false;
  writesBusinessSystem: false;
  writesExternalApi: false;
}

export interface AgentUsedKnowledgePolicy {
  policyId: string;
  version: string;
  capabilityTypes: AgentCapabilityType[];
  minimumInvocationFields: string[];
  overreadRiskSignals: AgentOverreadRiskSignal[];
  allowedOutcomes: AgentKnowledgeUseOutcome[];
  hardBoundaries: {
    agentCanWriteAccepted: false;
    agentCanWritePublic: false;
    agentCanModifyGovernanceEvidence: false;
    crossSupplierWithoutAclAllowed: false;
    t5FinalFactAllowed: false;
    promotionWithoutKweAllowed: false;
    businessSystemWriteAllowed: false;
    revenueOrScoreConfirmationAllowed: false;
    sensitiveRawContentAllowedInEvidence: false;
    harnessEvidenceRequiredForHighRisk: boolean;
  };
  requiredGates: string[];
  noWriteAssertions: {
    writesAccepted: 0;
    writesPublic: 0;
    writesGovernanceEvidence: 0;
    writesBusinessSystem: 0;
    writesRevenueOrScoreConfirmation: 0;
    writesExternalApi: 0;
  };
}
