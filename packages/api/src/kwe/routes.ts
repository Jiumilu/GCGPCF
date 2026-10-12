export type KweHttpMethod = "GET" | "POST";

export type KweRouteMode =
  | "read_only"
  | "work_request"
  | "confirmation_request"
  | "committee_request"
  | "promotion_request"
  | "redaction_request"
  | "writeback_request";

export interface KweEndpointDefinition {
  method: KweHttpMethod;
  path: string;
  handler: string;
  routeMode: KweRouteMode;
  requiresWameGate: boolean;
  requiresHumanOrCommitteeForFinality: boolean;
  writesAcceptedFact: false;
  writesBusinessSystem: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
}

export const KWE_ENDPOINTS: KweEndpointDefinition[] = [
  {
    method: "POST",
    path: "/api/v2/kwe/work-items",
    handler: "createWorkItemRequest",
    routeMode: "work_request",
    requiresWameGate: false,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/kwe/work-items",
    handler: "listWorkItems",
    routeMode: "read_only",
    requiresWameGate: false,
    requiresHumanOrCommitteeForFinality: false,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/gaps",
    handler: "createGapRequest",
    routeMode: "work_request",
    requiresWameGate: false,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/bounties",
    handler: "createBountyRequest",
    routeMode: "work_request",
    requiresWameGate: false,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/confirmations",
    handler: "submitConfirmationRequest",
    routeMode: "confirmation_request",
    requiresWameGate: true,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/committees",
    handler: "submitCommitteeReviewRequest",
    routeMode: "committee_request",
    requiresWameGate: true,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/promotions",
    handler: "submitPromotionRequest",
    routeMode: "promotion_request",
    requiresWameGate: true,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/redactions",
    handler: "submitRedactionRequest",
    routeMode: "redaction_request",
    requiresWameGate: true,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/writebacks",
    handler: "submitWritebackRequest",
    routeMode: "writeback_request",
    requiresWameGate: true,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/kwe/disputes",
    handler: "submitDisputeRequest",
    routeMode: "committee_request",
    requiresWameGate: true,
    requiresHumanOrCommitteeForFinality: true,
    writesAcceptedFact: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
];
