export type GovernanceHttpMethod = "GET" | "POST";

export type GovernanceRouteMode =
  | "loop_record_request"
  | "read_only"
  | "evidence_request"
  | "knowledge_ci_dry_run";

export interface GovernanceEndpointDefinition {
  method: GovernanceHttpMethod;
  path: string;
  handler: string;
  routeMode: GovernanceRouteMode;
  requiresEvidenceBoundary: boolean;
  dryRunOnly: boolean;
  writesBusinessSystem: false;
  writesAcceptedFact: false;
  writesRevenueDistribution: false;
  writesQuotaMutation: false;
  writesBountySettlement: false;
  writesExternalApi: false;
}

export const GOVERNANCE_ENDPOINTS: GovernanceEndpointDefinition[] = [
  {
    method: "POST",
    path: "/api/v2/governance/loop",
    handler: "createLoopRecordRequest",
    routeMode: "loop_record_request",
    requiresEvidenceBoundary: true,
    dryRunOnly: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/governance/loop/{id}",
    handler: "getLoopRecord",
    routeMode: "read_only",
    requiresEvidenceBoundary: true,
    dryRunOnly: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/governance/evidence",
    handler: "createGovernanceEvidenceRequest",
    routeMode: "evidence_request",
    requiresEvidenceBoundary: true,
    dryRunOnly: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/governance/knowledge-ci/run",
    handler: "runKnowledgeCiDryRun",
    routeMode: "knowledge_ci_dry_run",
    requiresEvidenceBoundary: true,
    dryRunOnly: true,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/governance/ledger/contributions",
    handler: "getContributionLedger",
    routeMode: "read_only",
    requiresEvidenceBoundary: true,
    dryRunOnly: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/governance/ledger/revenue",
    handler: "getRevenueLedger",
    routeMode: "read_only",
    requiresEvidenceBoundary: true,
    dryRunOnly: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/governance/ledger/quota",
    handler: "getQuotaLedger",
    routeMode: "read_only",
    requiresEvidenceBoundary: true,
    dryRunOnly: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/governance/ledger/bounties",
    handler: "getBountyLedger",
    routeMode: "read_only",
    requiresEvidenceBoundary: true,
    dryRunOnly: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesQuotaMutation: false,
    writesBountySettlement: false,
    writesExternalApi: false,
  },
];
