import type {
  GfisAssistantQueryRequest,
  GfisDocumentAcceptanceRequest,
  GfisWritebackCandidateRequest,
} from "./contracts";
import { GFIS_ENDPOINTS } from "./routes";
import { gfisRepository } from "./repository";

export const gfisService = {
  endpoints: GFIS_ENDPOINTS,
  repository: gfisRepository,
  queryKnowledge(request: GfisAssistantQueryRequest) {
    return gfisRepository.preview("read_only", request);
  },
  queryGfisKnowledgeAssistant(request: GfisAssistantQueryRequest) {
    return gfisRepository.preview("read_only", request);
  },
  queryGfisUsageAssistant(request: GfisAssistantQueryRequest) {
    return gfisRepository.preview("read_only", request);
  },
  checkDocumentAcceptance(request: GfisDocumentAcceptanceRequest) {
    return gfisRepository.preview("candidate_request", request);
  },
  checkGfisDocumentAcceptance(request: GfisDocumentAcceptanceRequest) {
    return gfisRepository.preview("candidate_request", request);
  },
  createWritebackCandidate(request: GfisWritebackCandidateRequest) {
    return gfisRepository.preview("candidate_request", request);
  },
  createGfisWritebackCandidate(request: GfisWritebackCandidateRequest) {
    return gfisRepository.preview("candidate_request", request);
  },
};
