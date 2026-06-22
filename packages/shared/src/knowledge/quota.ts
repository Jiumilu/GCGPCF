export type QuotaType =
  | "platform_quota"
  | "self_purchased_quota"
  | "contributed_quota"
  | "shared_quota"
  | "reward_quota";

export type QuotaOwnerType = "platform" | "company" | "project" | "user";

export interface QuotaRecord {
  id: string;
  quotaType: QuotaType;
  ownerType: QuotaOwnerType;
  ownerId: string;
  amount: number;
  usedAmount: number;
  poolRefs: string[];
  revenuePoolEligible: boolean;
  note?: string;
}
