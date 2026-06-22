export type GfisHttpMethod = "POST";

export type GfisRouteMode =
  | "assistant_query"
  | "usage_guidance"
  | "document_acceptance_check"
  | "writeback_candidate";

export interface GfisEndpointDefinition {
  method: GfisHttpMethod;
  path: string;
  handler: string;
  routeMode: GfisRouteMode;
  requiresKdsSearch: boolean;
  requiresWaesGate: boolean;
  requiresKweFlowForFinality: boolean;
  writesFact: false;
  writesBusinessSystem: false;
  writesAcceptedFact: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
}

export const GFIS_ENDPOINTS: GfisEndpointDefinition[] = [
  {
    method: "POST",
    path: "/api/v2/gfis/knowledge-assistant/query",
    handler: "queryGfisKnowledgeAssistant",
    routeMode: "assistant_query",
    requiresKdsSearch: true,
    requiresWaesGate: true,
    requiresKweFlowForFinality: true,
    writesFact: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/gfis/usage-assistant/query",
    handler: "queryGfisUsageAssistant",
    routeMode: "usage_guidance",
    requiresKdsSearch: true,
    requiresWaesGate: true,
    requiresKweFlowForFinality: true,
    writesFact: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/gfis/document-acceptance/check",
    handler: "checkGfisDocumentAcceptance",
    routeMode: "document_acceptance_check",
    requiresKdsSearch: true,
    requiresWaesGate: true,
    requiresKweFlowForFinality: true,
    writesFact: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "POST",
    path: "/api/v2/gfis/writeback-candidates",
    handler: "createGfisWritebackCandidate",
    routeMode: "writeback_candidate",
    requiresKdsSearch: true,
    requiresWaesGate: true,
    requiresKweFlowForFinality: true,
    writesFact: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
];
