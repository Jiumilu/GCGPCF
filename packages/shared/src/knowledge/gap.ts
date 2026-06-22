export type GapType =
  | "missing_source"
  | "missing_evidence"
  | "missing_field"
  | "missing_sop"
  | "missing_policy"
  | "missing_order_data"
  | "missing_finance_proof"
  | "missing_pod"
  | "missing_quality_record"
  | "missing_responsibility_boundary";

export type GapPriority = "P0" | "P1" | "P2" | "P3";

export type GapStatus =
  | "open"
  | "in_progress"
  | "submitted"
  | "partially_accepted"
  | "accepted"
  | "rejected"
  | "closed";

export interface GapRecord {
  id: string;
  title: string;
  description: string;
  gapType: GapType;
  poolRefs: string[];
  discoveredBy: "system" | "ai" | "user" | "partner" | "committee";
  priority: GapPriority;
  bountyEnabled: boolean;
  bountyRef?: string;
  status: GapStatus;
}
