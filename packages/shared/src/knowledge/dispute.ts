export type DisputeType =
  | "contribution_dispute"
  | "revenue_dispute"
  | "bounty_dispute"
  | "rag_reference_dispute"
  | "responsibility_boundary_dispute"
  | "quality_dispute"
  | "delivery_dispute";

export type DisputeStatus =
  | "open"
  | "under_review"
  | "committee_required"
  | "resolved"
  | "rejected"
  | "frozen";

export interface DisputeRecord {
  id: string;
  disputeType: DisputeType;
  relatedObjectRefs: string[];
  claimantType: "user" | "team" | "company" | "external_account";
  claimantId: string;
  status: DisputeStatus;
  decisionRef?: string;
  evidenceRefs: string[];
  createdAt: string;
  updatedAt: string;
}
