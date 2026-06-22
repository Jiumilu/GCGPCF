import {
  invokeHandlerStubEnvelope,
  type HandlerStubEnvelopeResponse,
} from "./handler-stub";

export interface RouteAdapterDryRunRequest {
  method: "GET" | "POST";
  path: string;
  body?: Record<string, unknown>;
  query?: Record<string, unknown>;
  requestId: string;
  traceId: string;
  dryRun: true;
}

export interface RouteAdapterDryRunResponse {
  ok: boolean;
  requestId: string;
  traceId: string;
  dryRun: true;
  method: RouteAdapterDryRunRequest["method"];
  path: string;
  handler?: string;
  statusCode: 200 | 404 | 405;
  envelope: HandlerStubEnvelopeResponse;
  noWrite: true;
  startsServer: false;
  connectsDatabase: false;
  callsExternalApi: false;
  directBusinessWrite: false;
  acceptedLifecycleWrite: false;
  externalApiWrite: false;
}

interface RouteEntry {
  method: RouteAdapterDryRunRequest["method"];
  path: string;
  handler: string;
}

const ROUTE_ENTRIES: RouteEntry[] = [
  { method: "GET", path: "/api/v2/domains", handler: "listDomains" },
  { method: "GET", path: "/api/v2/pools", handler: "listPools" },
  { method: "GET", path: "/api/v2/projects", handler: "listProjects" },
  { method: "POST", path: "/api/v2/search", handler: "searchKnowledge" },
  { method: "GET", path: "/api/v2/objects/{uri}", handler: "getKnowledgeObject" },
  { method: "POST", path: "/api/v2/sources/import", handler: "importSourceCandidate" },
  { method: "POST", path: "/api/v2/fact-candidates", handler: "createFactCandidate" },
  { method: "POST", path: "/api/v2/sop-candidates", handler: "createSopCandidate" },
  { method: "POST", path: "/api/v2/writeback-candidates", handler: "createWritebackCandidate" },
  { method: "GET", path: "/api/v2/graph", handler: "getKnowledgeGraph" },
  { method: "GET", path: "/api/v2/governance/evidence", handler: "getGovernanceEvidence" },
  { method: "POST", path: "/api/v2/waes/gates/run", handler: "runWaesGates" },
  { method: "POST", path: "/api/v2/waes/rag-admission/check", handler: "checkRagAdmission" },
  { method: "POST", path: "/api/v2/waes/writeback/check", handler: "checkWriteback" },
  { method: "POST", path: "/api/v2/waes/revenue/check", handler: "checkRevenue" },
  { method: "POST", path: "/api/v2/waes/contribution/check", handler: "checkContribution" },
  { method: "POST", path: "/api/v2/waes/external-share/check", handler: "checkExternalShare" },
  { method: "POST", path: "/api/v2/waes/freeze", handler: "requestFreeze" },
  { method: "POST", path: "/api/v2/kwe/work-items", handler: "createWorkItemRequest" },
  { method: "GET", path: "/api/v2/kwe/work-items", handler: "listWorkItems" },
  { method: "POST", path: "/api/v2/kwe/gaps", handler: "createGapRequest" },
  { method: "POST", path: "/api/v2/kwe/bounties", handler: "createBountyRequest" },
  { method: "POST", path: "/api/v2/kwe/confirmations", handler: "submitConfirmationRequest" },
  { method: "POST", path: "/api/v2/kwe/committees", handler: "submitCommitteeReviewRequest" },
  { method: "POST", path: "/api/v2/kwe/promotions", handler: "submitPromotionRequest" },
  { method: "POST", path: "/api/v2/kwe/redactions", handler: "submitRedactionRequest" },
  { method: "POST", path: "/api/v2/kwe/writebacks", handler: "submitWritebackRequest" },
  { method: "POST", path: "/api/v2/kwe/disputes", handler: "submitDisputeRequest" },
  { method: "POST", path: "/api/v2/gfis/knowledge-assistant/query", handler: "queryGfisKnowledgeAssistant" },
  { method: "POST", path: "/api/v2/gfis/usage-assistant/query", handler: "queryGfisUsageAssistant" },
  { method: "POST", path: "/api/v2/gfis/document-acceptance/check", handler: "checkGfisDocumentAcceptance" },
  { method: "POST", path: "/api/v2/gfis/writeback-candidates", handler: "createGfisWritebackCandidate" },
  { method: "POST", path: "/api/v2/governance/loop", handler: "createLoopRecordRequest" },
  { method: "GET", path: "/api/v2/governance/loop/{id}", handler: "getLoopRecord" },
  { method: "POST", path: "/api/v2/governance/evidence", handler: "createGovernanceEvidenceRequest" },
  { method: "POST", path: "/api/v2/governance/knowledge-ci/run", handler: "runKnowledgeCiDryRun" },
  { method: "GET", path: "/api/v2/governance/ledger/contributions", handler: "getContributionLedger" },
  { method: "GET", path: "/api/v2/governance/ledger/revenue", handler: "getRevenueLedger" },
  { method: "GET", path: "/api/v2/governance/ledger/quota", handler: "getQuotaLedger" },
  { method: "GET", path: "/api/v2/governance/ledger/bounties", handler: "getBountyLedger" },
];

export function listRouteAdapterDryRunRoutes(): RouteEntry[] {
  return [...ROUTE_ENTRIES];
}

function buildRequestPayload(input: RouteAdapterDryRunRequest): Record<string, unknown> {
  return {
    ...(input.query ?? {}),
    ...(input.body ?? {}),
    dryRun: input.dryRun,
    route: {
      method: input.method,
      path: input.path,
    },
  };
}

function createRouteEnvelope(
  input: RouteAdapterDryRunRequest,
  handler: string,
): HandlerStubEnvelopeResponse {
  return invokeHandlerStubEnvelope({
    handler,
    request: buildRequestPayload(input),
    requestId: input.requestId,
    traceId: input.traceId,
    dryRun: input.dryRun,
  });
}

function createAdapterResponse(
  input: RouteAdapterDryRunRequest,
  envelope: HandlerStubEnvelopeResponse,
  statusCode: RouteAdapterDryRunResponse["statusCode"],
  handler?: string,
): RouteAdapterDryRunResponse {
  return {
    ok: envelope.ok,
    requestId: input.requestId,
    traceId: input.traceId,
    dryRun: input.dryRun,
    method: input.method,
    path: input.path,
    ...(handler ? { handler } : {}),
    statusCode,
    envelope,
    noWrite: true,
    startsServer: false,
    connectsDatabase: false,
    callsExternalApi: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  };
}

export function adaptRouteDryRun(
  input: RouteAdapterDryRunRequest,
): RouteAdapterDryRunResponse {
  const methodPathMatch = ROUTE_ENTRIES.find(
    (entry) => entry.method === input.method && entry.path === input.path,
  );
  if (methodPathMatch) {
    const envelope = createRouteEnvelope(input, methodPathMatch.handler);
    return createAdapterResponse(input, envelope, envelope.ok ? 200 : 404, methodPathMatch.handler);
  }

  const pathMatch = ROUTE_ENTRIES.find((entry) => entry.path === input.path);
  if (pathMatch) {
    const envelope = createRouteEnvelope(input, "routeAdapterMethodNotAllowed");
    return createAdapterResponse(input, envelope, 405);
  }

  const envelope = createRouteEnvelope(input, "routeAdapterNotFound");
  return createAdapterResponse(input, envelope, 404);
}
