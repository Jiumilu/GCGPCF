export type BrainHttpMethod = "GET" | "POST";

export type BrainRouteMode = "aggregate_read" | "dashboard_read" | "governance_read";

export interface BrainEndpointDefinition {
  method: BrainHttpMethod;
  path: string;
  handler: string;
  routeMode: BrainRouteMode;
  aggregatesKds: boolean;
  aggregatesWaes: boolean;
  aggregatesKwe: boolean;
  aggregatesGovernance: boolean;
  writesKds: false;
  writesWaes: false;
  writesKwe: false;
  writesBusinessSystem: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
}

export const BRAIN_ENDPOINTS: BrainEndpointDefinition[] = [
  {
    method: "POST",
    path: "/api/v2/brain/command-center/query",
    handler: "queryBrainCommandCenter",
    routeMode: "aggregate_read",
    aggregatesKds: true,
    aggregatesWaes: true,
    aggregatesKwe: true,
    aggregatesGovernance: true,
    writesKds: false,
    writesWaes: false,
    writesKwe: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/brain/governance",
    handler: "getBrainGovernanceView",
    routeMode: "governance_read",
    aggregatesKds: false,
    aggregatesWaes: true,
    aggregatesKwe: false,
    aggregatesGovernance: true,
    writesKds: false,
    writesWaes: false,
    writesKwe: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/brain/loop-dashboard",
    handler: "getBrainLoopDashboard",
    routeMode: "dashboard_read",
    aggregatesKds: true,
    aggregatesWaes: true,
    aggregatesKwe: true,
    aggregatesGovernance: true,
    writesKds: false,
    writesWaes: false,
    writesKwe: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
];
