import {
  adaptRouteDryRun,
  type RouteAdapterDryRunRequest,
  type RouteAdapterDryRunResponse,
} from "./route-adapter";

export interface AcceptancePacketEvidenceRef {
  kind: "fixture" | "validator" | "loop_evidence" | "contract_doc";
  ref: string;
}

export interface AcceptancePacketDryRunRequest {
  packetId: string;
  title: string;
  routeRequests: RouteAdapterDryRunRequest[];
  evidenceRefs: AcceptancePacketEvidenceRef[];
  requestedBy: string;
  requestId: string;
  traceId: string;
  dryRun: true;
}

export interface AcceptancePacketDryRunResponse {
  ok: boolean;
  packetId: string;
  title: string;
  requestedBy: string;
  requestId: string;
  traceId: string;
  dryRun: true;
  status: "ready_for_review" | "repair_required";
  routeCount: number;
  successCount: number;
  failureCount: number;
  gateEvidenceRefs: AcceptancePacketEvidenceRef[];
  routeResults: RouteAdapterDryRunResponse[];
  requiredHumanReview: true;
  requiredHarnessEvidence: true;
  noWrite: true;
  startsServer: false;
  connectsDatabase: false;
  callsExternalApi: false;
  directBusinessWrite: false;
  acceptedLifecycleWrite: false;
  externalApiWrite: false;
}

function countRouteResults(
  routeResults: RouteAdapterDryRunResponse[],
): Pick<AcceptancePacketDryRunResponse, "successCount" | "failureCount" | "status" | "ok"> {
  const successCount = routeResults.filter((result) => result.ok).length;
  const failureCount = routeResults.length - successCount;
  return {
    ok: failureCount === 0,
    status: failureCount === 0 ? "ready_for_review" : "repair_required",
    successCount,
    failureCount,
  };
}

export function createAcceptancePacketDryRun(
  input: AcceptancePacketDryRunRequest,
): AcceptancePacketDryRunResponse {
  const routeResults = input.routeRequests.map((routeRequest, index) =>
    adaptRouteDryRun({
      ...routeRequest,
      requestId: `${input.requestId}:route:${index + 1}`,
      traceId: input.traceId,
      dryRun: input.dryRun,
    }),
  );
  const counts = countRouteResults(routeResults);

  return {
    ok: counts.ok,
    packetId: input.packetId,
    title: input.title,
    requestedBy: input.requestedBy,
    requestId: input.requestId,
    traceId: input.traceId,
    dryRun: input.dryRun,
    status: counts.status,
    routeCount: routeResults.length,
    successCount: counts.successCount,
    failureCount: counts.failureCount,
    gateEvidenceRefs: [...input.evidenceRefs],
    routeResults,
    requiredHumanReview: true,
    requiredHarnessEvidence: true,
    noWrite: true,
    startsServer: false,
    connectsDatabase: false,
    callsExternalApi: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  };
}
