import type { TargetSystem, WritebackStatus } from "./fact-candidate";
import type { WameGateStatus } from "./wame-gate";

export type WritebackTargetEntityType =
  | "order"
  | "factory"
  | "supplier"
  | "customer"
  | "quality_record"
  | "delivery_record"
  | "pod_record"
  | "finance_record"
  | "sop"
  | "risk"
  | "status";

export interface WritebackCandidate {
  id: string;
  targetSystem: TargetSystem;
  targetEntityType: WritebackTargetEntityType;
  targetEntityId?: string;
  proposedFields: Record<string, unknown>;
  basedOnObjectRefs: string[];
  evidenceRefs: string[];
  poolRefs: string[];
  wameGateStatus: Extract<WameGateStatus, "pending" | "passed" | "blocked" | "human_required" | "committee_required">;
  writebackStatus: Exclude<WritebackStatus, "not_applicable">;
}
