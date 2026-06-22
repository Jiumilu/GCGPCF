export type KnowledgeRelationType =
  | "source_provides_evidence"
  | "evidence_supports_object"
  | "object_generates_candidate"
  | "candidate_checked_by_gate"
  | "gate_opens_work_item"
  | "work_item_produces_confirmation"
  | "confirmation_enables_writeback_candidate"
  | "decision_records_contribution"
  | "contribution_links_revenue"
  | "governance_evidence_closes_loop";

export type KnowledgeRelationEndpointType =
  | "source_record"
  | "evidence_record"
  | "knowledge_object"
  | "candidate"
  | "candidate_or_gap"
  | "waes_gate_result"
  | "kwe_work_item"
  | "confirmation_record"
  | "confirmation_or_decision_record"
  | "decision_record"
  | "writeback_candidate"
  | "contribution_record"
  | "revenue_record"
  | "harness_evidence_record"
  | "loop_record";

export interface KnowledgeObjectRelation {
  id: string;
  tenantId: string;
  relationType: KnowledgeRelationType;
  fromType: KnowledgeRelationEndpointType;
  fromId: string;
  toType: KnowledgeRelationEndpointType;
  toId: string;
  requiredRefs: string[];
  poolRefs: string[];
  createdBy: string;
  createdAt: string;
  noWrite: true;
}

export interface KnowledgeObjectRelationshipPolicy {
  policyId: string;
  version: string;
  relationChain: Array<{
    relationType: KnowledgeRelationType;
    fromType: KnowledgeRelationEndpointType;
    toType: KnowledgeRelationEndpointType;
    requiredRefs: string[];
  }>;
  minimumRelationFields: string[];
  hardBoundaries: {
    sourceRequiredForFormalFact: boolean;
    evidenceRequiredForEvidenceReady: boolean;
    waesGateRequiredForCandidates: boolean;
    confirmationRequiredForWritebackCandidate: boolean;
    aiCannotCreateFormalWritebackRelation: boolean;
    loopCannotPromoteBusinessStatus: boolean;
    harnessStoresGovernanceEvidenceOnly: boolean;
    revenueBasisRequiredForDistribution: boolean;
  };
  noWriteAssertions: {
    writesKdsFact: 0;
    writesBusinessSystem: 0;
    writesRevenueDistribution: 0;
    writesExternalApi: 0;
  };
}
