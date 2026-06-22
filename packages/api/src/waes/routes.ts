export type WaesHttpMethod = "POST";

export type WaesRouteMode = "gate_check" | "dry_run" | "freeze_request";

export interface WaesEndpointDefinition {
  method: WaesHttpMethod;
  path: string;
  handler: string;
  routeMode: WaesRouteMode;
  writesGateResult: false;
  writesBusinessSystem: false;
  writesAcceptedFact: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
  requiresHumanOrCommitteeForFinality: boolean;
}

export const WAES_ENDPOINTS: WaesEndpointDefinition[] = [
  {
    method: "POST",
    path: "/api/v2/waes/gates/run",
    handler: "runWaesGates",
    routeMode: "gate_check",
    writesGateResult: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
    requiresHumanOrCommitteeForFinality: true,
  },
  {
    method: "POST",
    path: "/api/v2/waes/rag-admission/check",
    handler: "checkRagAdmission",
    routeMode: "gate_check",
    writesGateResult: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
    requiresHumanOrCommitteeForFinality: true,
  },
  {
    method: "POST",
    path: "/api/v2/waes/writeback/check",
    handler: "checkWriteback",
    routeMode: "gate_check",
    writesGateResult: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
    requiresHumanOrCommitteeForFinality: true,
  },
  {
    method: "POST",
    path: "/api/v2/waes/revenue/check",
    handler: "checkRevenue",
    routeMode: "gate_check",
    writesGateResult: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
    requiresHumanOrCommitteeForFinality: true,
  },
  {
    method: "POST",
    path: "/api/v2/waes/contribution/check",
    handler: "checkContribution",
    routeMode: "gate_check",
    writesGateResult: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
    requiresHumanOrCommitteeForFinality: true,
  },
  {
    method: "POST",
    path: "/api/v2/waes/external-share/check",
    handler: "checkExternalShare",
    routeMode: "gate_check",
    writesGateResult: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
    requiresHumanOrCommitteeForFinality: true,
  },
  {
    method: "POST",
    path: "/api/v2/waes/freeze",
    handler: "requestFreeze",
    routeMode: "freeze_request",
    writesGateResult: false,
    writesBusinessSystem: false,
    writesAcceptedFact: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
    requiresHumanOrCommitteeForFinality: true,
  },
];
