import type { WaesGateStatus } from "./waes-gate";

export type FactType =
  | "order_fact"
  | "factory_fact"
  | "production_fact"
  | "quality_fact"
  | "delivery_fact"
  | "pod_fact"
  | "finance_fact"
  | "policy_fact"
  | "supplier_fact"
  | "customer_fact"
  | "oem_transition_fact";

export type CandidateGenerator = "ai" | "user" | "system" | "partner";

export type TargetSystem = "GFIS" | "GPC" | "KDS" | "WAES" | "ERP" | "MES";

export type WritebackStatus =
  | "not_applicable"
  | "candidate"
  | "approved"
  | "written_back"
  | "rejected"
  | "rolled_back";

export interface FactCandidate {
  id: string;
  sourceObjectId: string;
  candidateText: string;
  factType: FactType;
  poolRefs: string[];
  generatedBy: CandidateGenerator;
  confidence: number;
  waesGateStatus: Extract<WaesGateStatus, "pending" | "passed" | "blocked" | "human_required" | "committee_required">;
  targetSystem?: TargetSystem;
  writebackStatus: Exclude<WritebackStatus, "rolled_back">;
}
