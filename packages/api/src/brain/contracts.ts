import type {
  ContributionRecord,
  KnowledgeObject,
  KdsPoolCode,
  LoopRecord,
  QuotaRecord,
  RagAdmission,
  RevenueRecord,
  WaesGateResult,
} from "../../../shared/src/knowledge";
import type { KweWorkItem } from "../kwe/contracts";

export type BrainWorkbenchModule =
  | "knowledge_command_center"
  | "pkc_console"
  | "gfis_knowledge_assistant"
  | "gfis_usage_assistant"
  | "gfis_document_acceptance_assistant"
  | "kds_object_center"
  | "waes_gate_center"
  | "kwe_work_queue"
  | "supply_chain_graph"
  | "governance_center"
  | "committee_center"
  | "revenue_contribution_center"
  | "ai_quota_center"
  | "gap_bounty_center"
  | "loop_dashboard";

export type BrainBlockedAction =
  | "direct_accept_fact"
  | "direct_publish_object"
  | "direct_gfis_writeback"
  | "direct_revenue_distribution"
  | "direct_contribution_confirmation"
  | "direct_waes_gate_override"
  | "direct_committee_decision";

export interface BrainCommandCenterRequest {
  tenantId: string;
  userId: string;
  projectId?: string;
  poolRefs?: KdsPoolCode[];
  modules: BrainWorkbenchModule[];
}

export interface BrainRagDashboardSummary {
  safe: number;
  limited: number;
  repairRequired: number;
  blocked: number;
  sensitiveMetadataOnly: number;
}

export interface BrainKnowledgeClosureMetricInput {
  stateCoverageRate: number;
  factMaturityDqRate: number;
  sourceEvidenceQualifiedRate: number;
  registryLedgerReportConsistencyRate: number;
  automationEffectiveRate: number;
  writebackGapClosureRate: number;
}

export interface BrainKnowledgeClosureMetric {
  score: number;
  weights: {
    stateCoverage: 20;
    factMaturityDq: 25;
    sourceEvidenceQualified: 20;
    registryLedgerReportConsistency: 15;
    automationEffective: 10;
    writebackGapClosure: 10;
  };
  inputs: BrainKnowledgeClosureMetricInput;
  noWrite: true;
}

export interface BrainLoopDashboardAuxiliaryMetrics {
  ragSafeRate: number;
  blockedKnowledgeRate: number;
  repairRequiredGapCount: number;
  waesInterceptionCount: number;
  humanConfirmationCompletionRate: number;
  committeeClosureRate: number;
  revenueCandidateToFormalRate: number;
  bountyClosureRate: number;
  aiCandidateAdoptionRate: number;
  externalShareViolationCount: number;
  sensitiveMetadataOnlyRate: number;
}

export interface BrainLoopDashboardResponse {
  tenantId: string;
  projectId?: string;
  knowledgeClosureMetric: BrainKnowledgeClosureMetric;
  auxiliaryMetrics: BrainLoopDashboardAuxiliaryMetrics;
  loopRecords: LoopRecord[];
  gateResults: WaesGateResult[];
  noWrite: true;
  kdsWrites: 0;
  waesWrites: 0;
  kweWrites: 0;
  businessWrites: 0;
  externalApiWrites: 0;
}

export interface BrainCommandCenterResponse {
  tenantId: string;
  modules: BrainWorkbenchModule[];
  visibleObjects: KnowledgeObject[];
  workItems: KweWorkItem[];
  gateResults: WaesGateResult[];
  ragAdmissionSummary: BrainRagDashboardSummary;
  contributionRecords: ContributionRecord[];
  revenueRecords: RevenueRecord[];
  quotaRecords: QuotaRecord[];
  loopRecords: LoopRecord[];
  allowedRagAdmissions: RagAdmission[];
  blockedActions: BrainBlockedAction[];
  noWrite: true;
  kdsWrites: 0;
  waesWrites: 0;
  kweWrites: 0;
  businessWrites: 0;
  externalApiWrites: 0;
}

export interface BrainReadOnlyGovernanceView {
  tenantId: string;
  gateResultRefs: string[];
  loopRefs: string[];
  contributionRefs: string[];
  revenueRefs: string[];
  quotaRefs: string[];
  committeeDecisionRefs: string[];
  blockedActions: BrainBlockedAction[];
  noWrite: true;
  governanceWrites: 0;
  businessWrites: 0;
  externalApiWrites: 0;
}
