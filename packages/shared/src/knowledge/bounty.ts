import type { GapPriority } from "./gap";

export type BountySettlementMode =
  | "knowledge_points"
  | "ai_reward_quota"
  | "future_revenue_reference"
  | "project_contribution_record"
  | "committee_confirmed_reward";

export type BountyStatus =
  | "draft"
  | "open"
  | "submitted"
  | "under_review"
  | "partially_accepted"
  | "accepted"
  | "rejected"
  | "disputed"
  | "closed"
  | "frozen";

export interface BountyRecord {
  id: string;
  gapRef: string;
  title: string;
  priority: GapPriority;
  settlementModes: BountySettlementMode[];
  sponsorType: "user" | "team" | "project" | "org" | "system";
  sponsorId: string;
  status: BountyStatus;
  evidenceRefs: string[];
  createdAt: string;
  updatedAt: string;
}
