import type {
  GapRecord,
  KnowledgeDomain,
  WaesGateResult,
  WritebackCandidate,
} from "../../../shared/src/knowledge";

export type KweWorkType =
  | "fact_confirmation"
  | "sop_confirmation"
  | "evidence_gap"
  | "bounty"
  | "promotion"
  | "redaction"
  | "publication"
  | "writeback"
  | "revenue_review"
  | "contribution_review"
  | "dispute_resolution"
  | "committee_review"
  | "freeze";

export type KweWorkStatus =
  | "open"
  | "in_progress"
  | "submitted"
  | "approved"
  | "rejected"
  | "closed"
  | "frozen";

export interface KweWorkItem {
  id: string;
  tenantId: string;
  sourceObjectId: string;
  targetObjectId?: string;
  projectId?: string;
  supplyChainNodeId?: string;
  workType: KweWorkType;
  targetDomain: KnowledgeDomain;
  status: KweWorkStatus;
  priority: "P0" | "P1" | "P2" | "P3";
  assigneeType?: "user" | "team" | "committee" | "system";
  assigneeId?: string;
  requiredActions: string[];
  evidenceGapRefs: string[];
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateKweWorkItemRequest {
  tenantId: string;
  item: KweWorkItem;
}

export interface CreateGapRequest {
  tenantId: string;
  gap: GapRecord;
}

export interface ConfirmationRequest {
  tenantId: string;
  workItemId: string;
  decision: "approve" | "reject" | "request_repair" | "committee_required";
  evidenceRefs: string[];
  confirmedBy: string;
}

export interface KweWritebackRequest {
  tenantId: string;
  workItemId: string;
  candidate: WritebackCandidate;
  gateResult: WaesGateResult;
}
