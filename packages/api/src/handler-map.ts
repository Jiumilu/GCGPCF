import { GFIS_ENDPOINTS } from "./gfis/routes";
import { GOVERNANCE_ENDPOINTS } from "./governance/routes";
import { KDS_V2_ENDPOINTS } from "./kds/v2/routes";
import { KWE_ENDPOINTS } from "./kwe/routes";
import { WAES_ENDPOINTS } from "./waes/routes";

export type HandlerGroup =
  | "kds_v2"
  | "waes"
  | "kwe"
  | "gfis_assistant"
  | "governance_loop";

export type HandlerWriteBoundary =
  | "read_only"
  | "candidate_request"
  | "gate_check"
  | "work_request"
  | "governance_evidence_request"
  | "ledger_read";

export interface HandlerPreflightMapping {
  group: HandlerGroup;
  method: "GET" | "POST";
  path: string;
  handler: string;
  serviceName: string;
  serviceMethod: string;
  writeBoundary: HandlerWriteBoundary;
  requiresWaesGate: boolean;
  requiresKweFlow: boolean;
  requiresHumanOrCommitteeForFinality: boolean;
  directBusinessWrite: false;
  acceptedLifecycleWrite: false;
  externalApiWrite: false;
  noWrite: true;
}

function mapKdsEndpoint(endpoint: (typeof KDS_V2_ENDPOINTS)[number]): HandlerPreflightMapping {
  const candidateHandlers = new Set([
    "importSourceCandidate",
    "createFactCandidate",
    "createSopCandidate",
    "createWritebackCandidate",
  ]);
  return {
    group: "kds_v2",
    method: endpoint.method,
    path: endpoint.path,
    handler: endpoint.handler,
    serviceName: "kdsV2Service",
    serviceMethod: endpoint.handler,
    writeBoundary: candidateHandlers.has(endpoint.handler) ? "candidate_request" : "read_only",
    requiresWaesGate: endpoint.requiresWaesGate,
    requiresKweFlow: endpoint.requiresKweFlow,
    requiresHumanOrCommitteeForFinality: endpoint.requiresKweFlow,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
    noWrite: true,
  };
}

function mapWaesEndpoint(endpoint: (typeof WAES_ENDPOINTS)[number]): HandlerPreflightMapping {
  return {
    group: "waes",
    method: endpoint.method,
    path: endpoint.path,
    handler: endpoint.handler,
    serviceName: "waesService",
    serviceMethod: endpoint.handler,
    writeBoundary: "gate_check",
    requiresWaesGate: true,
    requiresKweFlow: false,
    requiresHumanOrCommitteeForFinality: endpoint.requiresHumanOrCommitteeForFinality,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
    noWrite: true,
  };
}

function mapKweEndpoint(endpoint: (typeof KWE_ENDPOINTS)[number]): HandlerPreflightMapping {
  return {
    group: "kwe",
    method: endpoint.method,
    path: endpoint.path,
    handler: endpoint.handler,
    serviceName: "kweService",
    serviceMethod: endpoint.handler,
    writeBoundary: endpoint.routeMode === "read_only" ? "read_only" : "work_request",
    requiresWaesGate: endpoint.requiresWaesGate,
    requiresKweFlow: endpoint.routeMode !== "read_only",
    requiresHumanOrCommitteeForFinality: endpoint.requiresHumanOrCommitteeForFinality,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
    noWrite: true,
  };
}

function mapGfisEndpoint(endpoint: (typeof GFIS_ENDPOINTS)[number]): HandlerPreflightMapping {
  return {
    group: "gfis_assistant",
    method: endpoint.method,
    path: endpoint.path,
    handler: endpoint.handler,
    serviceName: "gfisService",
    serviceMethod: endpoint.handler,
    writeBoundary:
      endpoint.routeMode === "assistant_query" || endpoint.routeMode === "usage_guidance"
        ? "read_only"
        : "candidate_request",
    requiresWaesGate: endpoint.requiresWaesGate,
    requiresKweFlow: endpoint.requiresKweFlowForFinality,
    requiresHumanOrCommitteeForFinality: endpoint.requiresKweFlowForFinality,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
    noWrite: true,
  };
}

function mapGovernanceEndpoint(endpoint: (typeof GOVERNANCE_ENDPOINTS)[number]): HandlerPreflightMapping {
  const ledgerHandlers = new Set([
    "getContributionLedger",
    "getRevenueLedger",
    "getQuotaLedger",
    "getBountyLedger",
  ]);
  return {
    group: "governance_loop",
    method: endpoint.method,
    path: endpoint.path,
    handler: endpoint.handler,
    serviceName: "governanceService",
    serviceMethod: endpoint.handler,
    writeBoundary: ledgerHandlers.has(endpoint.handler)
      ? "ledger_read"
      : endpoint.routeMode === "read_only" || endpoint.routeMode === "knowledge_ci_dry_run"
        ? "read_only"
        : "governance_evidence_request",
    requiresWaesGate: false,
    requiresKweFlow: false,
    requiresHumanOrCommitteeForFinality: endpoint.routeMode !== "read_only",
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
    noWrite: true,
  };
}

export const HANDLER_PREFLIGHT_MAPPINGS: HandlerPreflightMapping[] = [
  ...KDS_V2_ENDPOINTS.map(mapKdsEndpoint),
  ...WAES_ENDPOINTS.map(mapWaesEndpoint),
  ...KWE_ENDPOINTS.map(mapKweEndpoint),
  ...GFIS_ENDPOINTS.map(mapGfisEndpoint),
  ...GOVERNANCE_ENDPOINTS.map(mapGovernanceEndpoint),
];
