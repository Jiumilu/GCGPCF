export type WaesGateType =
  | "source_gate"
  | "evidence_gate"
  | "dsr_gate"
  | "rag_gate"
  | "writeback_gate"
  | "revenue_gate"
  | "contribution_gate"
  | "bounty_gate"
  | "committee_gate"
  | "freeze_gate"
  | "external_share_gate"
  | "sensitive_data_gate";

export type WaesGateStatus =
  | "pending"
  | "passed"
  | "blocked"
  | "repair_required"
  | "human_required"
  | "committee_required"
  | "redaction_required"
  | "freeze_required"
  | "metadata_only";

export interface WaesGateResult {
  id: string;
  tenantId: string;
  objectId: string;
  gateType: WaesGateType;
  gateStatus: WaesGateStatus;
  policyVersion: string;
  result: Record<string, unknown>;
  requiredActions: string[];
  createdBy: string;
  createdAt: string;
}
