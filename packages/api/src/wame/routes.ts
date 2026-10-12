export type WameHttpMethod = "POST";

export type WameRouteMode = "gate_check" | "dry_run" | "freeze_request";

export interface WameEndpointDefinition {
  method: WameHttpMethod;
  path: string;
  handler: string;
  routeMode: WameRouteMode;
  writesGateResult: false;
  writesBusinessSystem: false;
  writesAcceptedFact: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
  requiresHumanOrCommitteeForFinality: boolean;
}

export const WAME_ENDPOINTS: WameEndpointDefinition[] = [
  {
    method: "POST",
    path: "/api/v2/wame/gates/run",
    handler: "runWameGates",
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
    path: "/api/v2/wame/rag-admission/check",
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
    path: "/api/v2/wame/writeback/check",
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
    path: "/api/v2/wame/revenue/check",
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
    path: "/api/v2/wame/contribution/check",
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
    path: "/api/v2/wame/external-share/check",
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
    path: "/api/v2/wame/freeze",
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
