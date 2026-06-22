export type PkcHttpMethod = "GET" | "POST";

export type PkcRouteMode = "console_read" | "task_read" | "ledger_read";

export interface PkcEndpointDefinition {
  method: PkcHttpMethod;
  path: string;
  handler: string;
  routeMode: PkcRouteMode;
  aggregatesKds: boolean;
  aggregatesKwe: boolean;
  aggregatesGovernance: boolean;
  writesKds: false;
  writesWaes: false;
  writesKwe: false;
  writesBusinessSystem: false;
  writesRevenueDistribution: false;
  writesExternalApi: false;
}

export const PKC_ENDPOINTS: PkcEndpointDefinition[] = [
  {
    method: "POST",
    path: "/api/v2/pkc/console/query",
    handler: "queryPkcConsole",
    routeMode: "console_read",
    aggregatesKds: true,
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
    path: "/api/v2/pkc/tasks",
    handler: "getPkcTasks",
    routeMode: "task_read",
    aggregatesKds: false,
    aggregatesKwe: true,
    aggregatesGovernance: false,
    writesKds: false,
    writesWaes: false,
    writesKwe: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
  {
    method: "GET",
    path: "/api/v2/pkc/ledgers",
    handler: "getPkcLedgers",
    routeMode: "ledger_read",
    aggregatesKds: false,
    aggregatesKwe: false,
    aggregatesGovernance: true,
    writesKds: false,
    writesWaes: false,
    writesKwe: false,
    writesBusinessSystem: false,
    writesRevenueDistribution: false,
    writesExternalApi: false,
  },
];
