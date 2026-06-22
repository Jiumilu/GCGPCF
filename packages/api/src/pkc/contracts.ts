import type {
  BountyRecord,
  ContributionRecord,
  KnowledgeObject,
  QuotaRecord,
  RevenueRecord,
} from "../../../shared/src/knowledge";
import type { KweWorkItem } from "../kwe/contracts";

export type PkcConsoleSection =
  | "my_knowledge"
  | "my_drafts"
  | "my_favorites"
  | "recent"
  | "my_tasks"
  | "my_agent_outputs"
  | "my_kwe_work_items"
  | "my_contributions"
  | "my_points"
  | "my_ai_quota"
  | "my_bounties"
  | "my_project_packs"
  | "recommended_reuse";

export type PkcBlockedAction =
  | "final_fact_confirmation"
  | "committee_decision"
  | "waes_gate_override"
  | "force_kds_lifecycle_change"
  | "formal_revenue_distribution"
  | "business_system_writeback";

export interface PkcConsoleRequest {
  tenantId: string;
  userId: string;
  projectId?: string;
  sections: PkcConsoleSection[];
}

export interface PkcConsoleResponse {
  tenantId: string;
  userId: string;
  sections: PkcConsoleSection[];
  knowledgeObjects: KnowledgeObject[];
  drafts: KnowledgeObject[];
  tasks: KweWorkItem[];
  agentOutputRefs: string[];
  contributionRecords: ContributionRecord[];
  revenueCandidates: RevenueRecord[];
  quotaRecords: QuotaRecord[];
  bountyRecords: BountyRecord[];
  projectPackRefs: string[];
  blockedActions: PkcBlockedAction[];
  noWrite: true;
  kdsWrites: 0;
  waesWrites: 0;
  kweWrites: 0;
  businessWrites: 0;
  externalApiWrites: 0;
}
