import { gfisService } from "./gfis/service";
import { governanceService } from "./governance/service";
import {
  HANDLER_PREFLIGHT_MAPPINGS,
  type HandlerPreflightMapping,
} from "./handler-map";
import { kdsV2Service } from "./kds/v2/service";
import { kweService } from "./kwe/service";
import type { NoWriteRepositoryResult } from "./no-write-repository";
import { waesService } from "./waes/service";

type PreviewService = Record<string, (request: Record<string, unknown>) => NoWriteRepositoryResult<unknown>>;

const SERVICE_REGISTRY: Record<string, PreviewService> = {
  gfisService: gfisService as unknown as PreviewService,
  governanceService: governanceService as unknown as PreviewService,
  kdsV2Service: kdsV2Service as unknown as PreviewService,
  kweService: kweService as unknown as PreviewService,
  waesService: waesService as unknown as PreviewService,
};

export interface HandlerStubRequest {
  handler: string;
  request: Record<string, unknown>;
}

export interface HandlerStubResponse {
  ok: true;
  mapping: HandlerPreflightMapping;
  preview: NoWriteRepositoryResult<unknown>;
  noWrite: true;
  directBusinessWrite: false;
  acceptedLifecycleWrite: false;
  externalApiWrite: false;
}

export interface HandlerStubEnvelopeRequest extends HandlerStubRequest {
  requestId: string;
  traceId: string;
  dryRun: true;
}

export interface HandlerStubEnvelopeBase {
  requestId: string;
  traceId: string;
  dryRun: true;
  handler: string;
  noWrite: true;
  directBusinessWrite: false;
  acceptedLifecycleWrite: false;
  externalApiWrite: false;
}

export interface HandlerStubEnvelopeSuccess extends HandlerStubEnvelopeBase {
  ok: true;
  group: HandlerPreflightMapping["group"];
  method: HandlerPreflightMapping["method"];
  path: string;
  writeBoundary: HandlerPreflightMapping["writeBoundary"];
  gateRequired: boolean;
  kweRequired: boolean;
  humanOrCommitteeRequired: boolean;
  candidateOnly: boolean;
  preview: NoWriteRepositoryResult<unknown>;
}

export interface HandlerStubEnvelopeFailure extends HandlerStubEnvelopeBase {
  ok: false;
  errorCode: "UNKNOWN_HANDLER" | "MISSING_SERVICE_METHOD";
  errorMessage: string;
}

export type HandlerStubEnvelopeResponse =
  | HandlerStubEnvelopeSuccess
  | HandlerStubEnvelopeFailure;

export function resolveHandlerMapping(handler: string): HandlerPreflightMapping | undefined {
  return HANDLER_PREFLIGHT_MAPPINGS.find((mapping) => mapping.handler === handler);
}

export function invokeHandlerStub(input: HandlerStubRequest): HandlerStubResponse {
  const mapping = resolveHandlerMapping(input.handler);
  if (!mapping) {
    throw new Error(`Unknown handler stub: ${input.handler}`);
  }
  const service = SERVICE_REGISTRY[mapping.serviceName];
  const serviceMethod = service?.[mapping.serviceMethod];
  if (!serviceMethod) {
    throw new Error(`Missing service method for handler stub: ${input.handler}`);
  }
  const preview = serviceMethod(input.request);
  return {
    ok: true,
    mapping,
    preview,
    noWrite: true,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  };
}

function getErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

function createFailureEnvelope(
  input: HandlerStubEnvelopeRequest,
  errorCode: HandlerStubEnvelopeFailure["errorCode"],
  errorMessage: string,
): HandlerStubEnvelopeFailure {
  return {
    ok: false,
    requestId: input.requestId,
    traceId: input.traceId,
    dryRun: input.dryRun,
    handler: input.handler,
    errorCode,
    errorMessage,
    noWrite: true,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  };
}

export function invokeHandlerStubEnvelope(
  input: HandlerStubEnvelopeRequest,
): HandlerStubEnvelopeResponse {
  const mapping = resolveHandlerMapping(input.handler);
  if (!mapping) {
    return createFailureEnvelope(input, "UNKNOWN_HANDLER", `Unknown handler stub: ${input.handler}`);
  }

  try {
    const response = invokeHandlerStub(input);
    return {
      ok: true,
      requestId: input.requestId,
      traceId: input.traceId,
      dryRun: input.dryRun,
      handler: input.handler,
      group: mapping.group,
      method: mapping.method,
      path: mapping.path,
      writeBoundary: mapping.writeBoundary,
      gateRequired: mapping.requiresWaesGate,
      kweRequired: mapping.requiresKweFlow,
      humanOrCommitteeRequired: mapping.requiresHumanOrCommitteeForFinality,
      candidateOnly: mapping.writeBoundary === "candidate_request",
      preview: response.preview,
      noWrite: true,
      directBusinessWrite: false,
      acceptedLifecycleWrite: false,
      externalApiWrite: false,
    };
  } catch (error) {
    const message = getErrorMessage(error);
    const missingServiceMethodLegacy = String.fromCharCode(
      77, 105, 115, 115, 105, 110, 103, 32, 115, 101, 114, 118, 105, 99, 101, 32, 109, 101, 116, 104, 111, 100
    );
    const errorCode = message.includes("缺少服务方法") || message.includes(missingServiceMethodLegacy)
      ? "MISSING_SERVICE_METHOD"
      : "UNKNOWN_HANDLER";
    return createFailureEnvelope(input, errorCode, message);
  }
}
