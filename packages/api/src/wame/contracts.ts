import type { WameGateResult, WameGateType } from "../../../shared/src/knowledge";

export interface RunWameGatesRequest {
  tenantId: string;
  objectId: string;
  gateTypes: WameGateType[];
  context?: Record<string, unknown>;
}

export interface RunWameGatesResponse {
  results: WameGateResult[];
  blocked: boolean;
  requiredActions: string[];
}

export interface WameCheckRequest {
  tenantId: string;
  objectId: string;
  context?: Record<string, unknown>;
}

export type RagAdmissionCheckRequest = WameCheckRequest;
export type WritebackCheckRequest = WameCheckRequest;
export type RevenueCheckRequest = WameCheckRequest;
export type ContributionCheckRequest = WameCheckRequest;
export type ExternalShareCheckRequest = WameCheckRequest;

export interface FreezeRequest {
  tenantId: string;
  objectId: string;
  reason: string;
  requestedBy: string;
  relatedLedgerRefs?: string[];
}

export interface FreezeResponse {
  gateResult: WameGateResult;
  frozenObjectRefs: string[];
  frozenLedgerRefs: string[];
}
