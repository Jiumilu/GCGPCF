export type FourPoolLedger =
  | "contribution_points"
  | "revenue_pool"
  | "ai_quota_pool"
  | "bounty_pool";

export type FourPoolAllowedAction =
  | "register_contribution"
  | "record_candidate_score"
  | "record_confirmation_status"
  | "bind_evidence_refs"
  | "freeze_record"
  | "register_revenue_basis"
  | "record_candidate_distribution"
  | "record_review_status"
  | "register_quota_type"
  | "record_owner"
  | "record_amount"
  | "record_used_amount"
  | "record_revenue_pool_eligibility"
  | "register_gap"
  | "record_submission"
  | "record_acceptance_status"
  | "record_dispute_window"
  | "record_candidate_reward";

export type FourPoolBlockedAction =
  | "auto_confirm_score"
  | "auto_deduct_score"
  | "auto_exchange_reward"
  | "auto_distribute_revenue"
  | "auto_promote_potential_to_formal"
  | "distribute_without_cash_received"
  | "put_self_purchased_quota_into_unified_pool"
  | "auto_transfer_quota"
  | "auto_exchange_quota"
  | "auto_settle_bounty"
  | "skip_dispute_window"
  | "ai_direct_acceptance";

export interface FourPoolLedgerBoundary {
  pool: FourPoolLedger;
  allowedActions: FourPoolAllowedAction[];
  blockedActions: FourPoolBlockedAction[];
}

export interface FourPoolLedgerP0Policy {
  policyId: string;
  version: string;
  pools: FourPoolLedgerBoundary[];
  hardBoundaries: {
    formalRevenueRequiresCashReceived: boolean;
    invoicedRevenueIsFinancialStatisticsOnly: boolean;
    potentialRevenueMustNotAutoPromote: boolean;
    contributionConfirmedScoreRequiresHumanOrCommittee: boolean;
    selfPurchasedQuotaExcludedFromUnifiedRevenuePool: boolean;
    bountySettlementRequiresWaesHumanAcceptanceAndDisputeWindowClosed: boolean;
    majorDisputeCanFreezeAllFourPools: boolean;
  };
  noWriteAssertions: {
    writesScoreConfirmation: 0;
    writesRevenueDistribution: 0;
    writesQuotaTransfer: 0;
    writesBountySettlement: 0;
    writesExternalApi: 0;
  };
}
