import type {
  ConfirmationRequest,
  CreateGapRequest,
  CreateKweWorkItemRequest,
  KweWritebackRequest,
} from "./contracts";
import { KWE_ENDPOINTS } from "./routes";
import { kweRepository } from "./repository";

export const kweService = {
  endpoints: KWE_ENDPOINTS,
  repository: kweRepository,
  listWorkItems(request: { tenantId: string; assigneeId?: string }) {
    return kweRepository.preview("read_only", request);
  },
  createWorkItemRequest(request: CreateKweWorkItemRequest) {
    return kweRepository.preview("work_request", request);
  },
  createGapRequest(request: CreateGapRequest) {
    return kweRepository.preview("work_request", request);
  },
  createBountyRequest(request: Record<string, unknown>) {
    return kweRepository.preview("work_request", request);
  },
  submitConfirmationRequest(request: ConfirmationRequest) {
    return kweRepository.preview("work_request", request);
  },
  submitCommitteeReviewRequest(request: Record<string, unknown>) {
    return kweRepository.preview("work_request", request);
  },
  submitPromotionRequest(request: Record<string, unknown>) {
    return kweRepository.preview("work_request", request);
  },
  submitRedactionRequest(request: Record<string, unknown>) {
    return kweRepository.preview("work_request", request);
  },
  submitWritebackRequest(request: KweWritebackRequest) {
    return kweRepository.preview("work_request", request);
  },
  submitDisputeRequest(request: Record<string, unknown>) {
    return kweRepository.preview("work_request", request);
  },
};
