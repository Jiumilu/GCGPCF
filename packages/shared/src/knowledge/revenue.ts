export type RevenueType =
  | "formal_revenue"
  | "invoiced_revenue"
  | "potential_revenue"
  | "channel_opportunity"
  | "knowledge_potential_value";

export type RevenueBasis =
  | "cash_received"
  | "invoice"
  | "contract"
  | "opportunity"
  | "manual_estimate";

export type RevenueDistributionStatus =
  | "not_applicable"
  | "candidate"
  | "under_review"
  | "committee_required"
  | "confirmed"
  | "distributed"
  | "frozen";

export interface RevenueRecord {
  id: string;
  revenueType: RevenueType;
  amount?: number;
  currency?: string;
  basis: RevenueBasis;
  poolRefs: string[];
  contributionRefs: string[];
  distributionStatus: RevenueDistributionStatus;
  evidenceRefs: string[];
}
