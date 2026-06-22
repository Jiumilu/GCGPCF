import type { CandidateGenerator } from "./fact-candidate";

export type SopType =
  | "system_building"
  | "project_development"
  | "factory_construction"
  | "pre_operation_order"
  | "formal_order"
  | "oem_transition"
  | "raw_material_procurement"
  | "production_operation"
  | "quality_acceptance"
  | "delivery_pod"
  | "financial_voucher"
  | "customer_delivery"
  | "exception_dispute"
  | "revenue_distribution";

export interface SopCandidate {
  id: string;
  title: string;
  sopType: SopType;
  basedOnObjectRefs: string[];
  poolRefs: string[];
  generatedBy: Extract<CandidateGenerator, "ai" | "system"> | "human";
  confirmationStatus: string;
  waesGateStatus: string;
  applicableScope: string[];
}
