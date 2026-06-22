import type { RagAdmission, TrustLevel } from "./object";

export type RagUseCase =
  | "strong_answer"
  | "weak_answer"
  | "background"
  | "risk_hint"
  | "gap_hint"
  | "sop_basis"
  | "command_center_reference"
  | "metadata_reference";

export interface RagAdmissionDecision {
  objectId: string;
  trustLevel: TrustLevel;
  ragAdmission: RagAdmission;
  allowedUseCases: RagUseCase[];
  requiredActions: string[];
  gateResultRef?: string;
  decidedAt: string;
}
