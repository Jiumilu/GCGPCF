import type { WaesGateResult, WaesGateType } from "../../../shared/src/knowledge";

export interface RunWaesGatesRequest {
  tenantId: string;
  objectId: string;
  gateTypes: WaesGateType[];
  context?: Record<string, unknown>;
}

export interface RunWaesGatesResponse {
  results: WaesGateResult[];
  blocked: boolean;
  requiredActions: string[];
}

export interface WaesCheckRequest {
  tenantId: string;
  objectId: string;
  context?: Record<string, unknown>;
}

export type RagAdmissionCheckRequest = WaesCheckRequest;
export type WritebackCheckRequest = WaesCheckRequest;
export type RevenueCheckRequest = WaesCheckRequest;
export type ContributionCheckRequest = WaesCheckRequest;
export type ExternalShareCheckRequest = WaesCheckRequest;

export interface FreezeRequest {
  tenantId: string;
  objectId: string;
  reason: string;
  requestedBy: string;
  relatedLedgerRefs?: string[];
}

export interface FreezeResponse {
  gateResult: WaesGateResult;
  frozenObjectRefs: string[];
  frozenLedgerRefs: string[];
}
