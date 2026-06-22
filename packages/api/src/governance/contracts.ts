import type {
  BountyRecord,
  ContributionRecord,
  EvidenceRecord,
  LoopRecord,
  QuotaRecord,
  RevenueRecord,
} from "../../../shared/src/knowledge";

export interface CreateLoopRecordRequest {
  tenantId: string;
  loop: LoopRecord;
}

export interface CreateGovernanceEvidenceRequest {
  tenantId: string;
  evidence: EvidenceRecord;
}

export interface KnowledgeCiRunRequest {
  tenantId: string;
  scope: "okf" | "kds" | "waes" | "kwe" | "gfis" | "all";
  dryRun: boolean;
}

export interface KnowledgeCiRunResponse {
  passed: boolean;
  checks: Array<{
    name: string;
    status: "passed" | "blocked" | "repair_required";
    details?: Record<string, unknown>;
  }>;
}

export interface ContributionLedgerResponse {
  records: ContributionRecord[];
}

export interface RevenueLedgerResponse {
  records: RevenueRecord[];
}

export interface QuotaLedgerResponse {
  records: QuotaRecord[];
}

export interface BountyLedgerResponse {
  records: BountyRecord[];
}
