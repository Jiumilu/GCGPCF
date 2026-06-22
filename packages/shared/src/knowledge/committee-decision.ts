import type { DecisionStatus, DecisionType } from "./decision";
import type { KnowledgeDomain } from "./object";

export type CommitteeDecisionTrigger =
  | "point_confirmation_dispute"
  | "revenue_distribution_dispute"
  | "major_violation"
  | "bounty_settlement_dispute"
  | "potential_to_formal_revenue_conversion"
  | "cross_unit_contribution_dispute"
  | "third_party_pool_distribution"
  | "project_internal_dispute"
  | "major_rag_strong_reference_dispute"
  | "revenue_pool_rule_dispute";

export type CommitteeFreezeScope =
  | "object"
  | "rag_admission"
  | "contribution_score"
  | "revenue_distribution"
  | "quota_transfer"
  | "bounty_settlement"
  | "external_share";

export type CommitteeDecisionReasonCode =
  | "evidence_conflict"
  | "contribution_boundary_unclear"
  | "revenue_basis_dispute"
  | "major_violation_risk"
  | "cross_unit_conflict"
  | "bounty_acceptance_dispute"
  | "rag_strong_reference_risk"
  | "external_visibility_risk";

export type CommitteeVotingMethod =
  | "majority_vote"
  | "supermajority_vote"
  | "authorized_owner_decision";

export interface CommitteeDecisionInput {
  decisionId: string;
  tenantId: string;
  issueRef: string;
  decisionType: DecisionType;
  triggerReason: CommitteeDecisionTrigger;
  relatedObjectRefs: string[];
  evidenceRefs: string[];
  participants: string[];
  votingMethod: CommitteeVotingMethod;
  requestedBy: string;
  requiresFreezeReview: boolean;
}

export interface CommitteeDecisionOutput {
  decisionId: string;
  result: DecisionStatus;
  reasonCodes: CommitteeDecisionReasonCode[];
  requiredActions: string[];
  freezeScope: CommitteeFreezeScope[];
  visibilityScope: "governance_only" | "participant_only" | "authorized_project_view";
  harnessEvidenceRef: string;
  effectiveState: "decision_recorded" | "freeze_required" | "repair_required" | "rejected";
  writesBusinessSystem: false;
  writesRevenueDistribution: false;
  writesScoreConfirmation: false;
  writesExternalApi: false;
}

export interface CommitteeDecisionPolicy {
  policyId: string;
  version: string;
  decisionTriggers: CommitteeDecisionTrigger[];
  minimumInputFields: string[];
  minimumOutputFields: string[];
  freezeScopes: CommitteeFreezeScope[];
  reasonCodes: CommitteeDecisionReasonCode[];
  votingMethods: CommitteeVotingMethod[];
  hardBoundaries: {
    decisionDomain: Extract<KnowledgeDomain, "governance">;
    committeeDoesNotReplaceWaesGate: boolean;
    committeeCannotWriteBusinessSystem: boolean;
    committeeCannotDirectlyDistributeRevenue: boolean;
    committeeCannotDirectlyConfirmScore: boolean;
    harnessEvidenceRequired: boolean;
    externalAccountAuthorizedViewOnly: boolean;
  };
  noWriteAssertions: {
    writesBusinessSystem: 0;
    writesRevenueDistribution: 0;
    writesScoreConfirmation: 0;
    writesQuotaTransfer: 0;
    writesBountySettlement: 0;
    writesExternalApi: 0;
  };
}
