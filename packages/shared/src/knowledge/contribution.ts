export type ContributorType = "user" | "team" | "company" | "external_account";

export type ContributionType =
  | "knowledge"
  | "evidence"
  | "sop"
  | "source"
  | "correction"
  | "channel"
  | "order"
  | "supplier"
  | "customer"
  | "policy"
  | "acceptance"
  | "dispute_resolution";

export type ContributionConfirmationStatus =
  | "candidate"
  | "human_confirmed"
  | "committee_confirmed"
  | "rejected"
  | "frozen";

export interface ContributionRecord {
  id: string;
  contributorType: ContributorType;
  contributorId: string;
  contributionType: ContributionType;
  relatedObjectRefs: string[];
  poolRefs: string[];
  candidateScore?: number;
  confirmedScore?: number;
  confirmationStatus: ContributionConfirmationStatus;
  revenueRelated: boolean;
  revenueRef?: string;
}
