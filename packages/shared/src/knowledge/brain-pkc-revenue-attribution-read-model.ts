export type BrainPkcRevenueAttributionSurface = "brain" | "pkc";

export type BrainPkcRevenueAttributionScope =
  | "governance_overview"
  | "project_revenue_contribution"
  | "my_revenue_candidates"
  | "my_contributions"
  | "committee_review";

export type BrainPkcRevenueAttributionVisibility =
  | "own_only"
  | "project_authorized"
  | "governance_aggregate"
  | "committee_authorized";

export type BrainPkcRevenueAttributionDisplayMode =
  | "summary_only"
  | "metadata_only"
  | "authorized_detail"
  | "masked_cross_unit";

export type BrainPkcRevenueAttributionBlockedAction =
  | "confirm_score"
  | "distribute_revenue"
  | "promote_potential_revenue"
  | "override_waes_gate"
  | "complete_committee_decision"
  | "write_business_system"
  | "mutate_kds_lifecycle"
  | "call_external_api";

export interface BrainPkcRevenueAttributionNoWrite {
  writesKdsLifecycle: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesScoreConfirmation: 0;
  writesRevenueDistribution: 0;
  writesBusinessSystem: 0;
  writesExternalApi: 0;
}

export interface BrainPkcRevenueAttributionReadModel {
  viewId: string;
  surface: BrainPkcRevenueAttributionSurface;
  tenantId: string;
  viewerId: string;
  projectId: string;
  scope: BrainPkcRevenueAttributionScope;
  attributionPacketRefs: string[];
  visibleRevenueRefs: string[];
  visibleContributionRefs: string[];
  maskedContributionRefs: string[];
  waesGateRefs: string[];
  kweWorkpackRefs: string[];
  committeeRefs: string[];
  freezeRefs: string[];
  visibility: BrainPkcRevenueAttributionVisibility;
  displayMode: BrainPkcRevenueAttributionDisplayMode;
  blockedActions: BrainPkcRevenueAttributionBlockedAction[];
  noWrite: BrainPkcRevenueAttributionNoWrite;
}

export interface BrainPkcRevenueAttributionReadModelPolicy {
  policyId: "okf.brain_pkc_revenue_attribution_read_model_policy";
  version: string;
  surfaces: BrainPkcRevenueAttributionSurface[];
  scopes: BrainPkcRevenueAttributionScope[];
  visibilityModes: BrainPkcRevenueAttributionVisibility[];
  displayModes: BrainPkcRevenueAttributionDisplayMode[];
  blockedActions: BrainPkcRevenueAttributionBlockedAction[];
  hardBoundaries: {
    readModelOnly: boolean;
    pkcDefaultsToOwnOrAuthorizedOnly: boolean;
    brainCrossUnitDetailRequiresCommitteeOrGovernanceAuthorization: boolean;
    maskedCrossUnitMustNotExposeContributionIds: boolean;
    potentialRevenueNotPromoted: boolean;
    attributionViewIsNotDistribution: boolean;
    attributionViewIsNotScoreConfirmation: boolean;
  };
  noWriteAssertions: BrainPkcRevenueAttributionNoWrite;
}
