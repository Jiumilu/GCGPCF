import type { ContributionConfirmationStatus } from "./contribution";
import type { RevenueBasis, RevenueType } from "./revenue";

export type RevenueContributionAttributionBasis =
  | "cash_received"
  | "invoice_statistical"
  | "contract_reference"
  | "opportunity_reference"
  | "knowledge_value_reference"
  | "channel_reference"
  | "manual_estimate";

export type RevenueContributionAttributionStatus =
  | "candidate"
  | "under_review"
  | "committee_required"
  | "repair_required"
  | "frozen"
  | "distribution_candidate";

export interface RevenueContributionAttributionNoWrite {
  writesScoreConfirmation: 0;
  writesRevenueDistribution: 0;
  writesQuotaTransfer: 0;
  writesBountySettlement: 0;
  writesKdsFact: 0;
  writesBusinessSystem: 0;
  writesExternalApi: 0;
}

export interface RevenueContributionAttributionContributionRef {
  contributionRef: string;
  confirmationStatus: ContributionConfirmationStatus;
  proposedShare?: number;
  attributionReason: string;
}

export interface RevenueContributionAttributionPacket {
  id: string;
  tenantId: string;
  projectId: string;
  revenueRef: string;
  contributionRefs: RevenueContributionAttributionContributionRef[];
  revenueType: RevenueType;
  revenueBasis: RevenueBasis;
  attributionBasis: RevenueContributionAttributionBasis;
  evidenceRefs: string[];
  waesGateRefs: string[];
  confidence: number;
  attributionStatus: RevenueContributionAttributionStatus;
  committeeRequired: boolean;
  freezeRecommended: boolean;
  distributionCandidateOnly: boolean;
  noWrite: RevenueContributionAttributionNoWrite;
}

export interface RevenueContributionAttributionPacketPolicy {
  policyId: string;
  version: string;
  hardBoundaries: {
    formalDistributionRequiresCashReceived: boolean;
    invoicedIsStatisticsOnly: boolean;
    potentialMustNotAutoPromote: boolean;
    channelOpportunityIsReferenceOnly: boolean;
    knowledgeValueIsContributionOnly: boolean;
    attributionPacketIsNotDistribution: boolean;
    attributionPacketIsNotScoreConfirmation: boolean;
    committeeRequiredForCrossUnitOrPotentialToFormal: boolean;
    freezeRequiredForDisputeOrMajorViolation: boolean;
  };
  noWriteAssertions: RevenueContributionAttributionNoWrite;
}
