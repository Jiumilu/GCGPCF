export type WameGateType =
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

export type WameGateStatus =
  | "pending"
  | "passed"
  | "blocked"
  | "repair_required"
  | "human_required"
  | "committee_required"
  | "redaction_required"
  | "freeze_required"
  | "metadata_only";

export interface WameGateResult {
  id: string;
  tenantId: string;
  objectId: string;
  gateType: WameGateType;
  gateStatus: WameGateStatus;
  policyVersion: string;
  result: Record<string, unknown>;
  requiredActions: string[];
  createdBy: string;
  createdAt: string;
}
