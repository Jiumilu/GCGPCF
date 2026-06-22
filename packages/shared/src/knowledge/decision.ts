export type DecisionType =
  | "committee_decision"
  | "authorized_person_decision"
  | "publication_approval"
  | "freeze_decision"
  | "revenue_distribution_decision"
  | "contribution_confirmation_decision";

export type DecisionStatus = "draft" | "confirmed" | "rejected" | "superseded" | "frozen";

export interface DecisionRecord {
  id: string;
  decisionType: DecisionType;
  issueRef: string;
  participants: string[];
  result: DecisionStatus;
  summary: string;
  evidenceRefs: string[];
  createdBy: string;
  createdAt: string;
}
