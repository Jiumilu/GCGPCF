import type {
  CreateFactCandidateRequest,
  CreateSopCandidateRequest,
  CreateWritebackCandidateRequest,
  GraphQueryRequest,
  ImportSourceRequest,
  KnowledgeSearchContext,
} from "./contracts";
import { KDS_V2_ENDPOINTS } from "./routes";
import { kdsV2Repository } from "./repository";

export const kdsV2Service = {
  endpoints: KDS_V2_ENDPOINTS,
  repository: kdsV2Repository,
  listDomains() {
    return kdsV2Repository.preview("read_only", {});
  },
  listPools() {
    return kdsV2Repository.preview("read_only", {});
  },
  listProjects() {
    return kdsV2Repository.preview("read_only", {});
  },
  search(context: KnowledgeSearchContext) {
    return kdsV2Repository.preview("read_only", context);
  },
  searchKnowledge(context: KnowledgeSearchContext) {
    return kdsV2Repository.preview("read_only", context);
  },
  getKnowledgeObject(request: { tenantId: string; uri: string }) {
    return kdsV2Repository.preview("read_only", request);
  },
  importSourceCandidate(request: ImportSourceRequest) {
    return kdsV2Repository.preview("candidate_request", request);
  },
  createFactCandidate(request: CreateFactCandidateRequest) {
    return kdsV2Repository.preview("candidate_request", request);
  },
  createSopCandidate(request: CreateSopCandidateRequest) {
    return kdsV2Repository.preview("candidate_request", request);
  },
  createWritebackCandidate(request: CreateWritebackCandidateRequest) {
    return kdsV2Repository.preview("candidate_request", request);
  },
  getKnowledgeGraph(request: GraphQueryRequest) {
    return kdsV2Repository.preview("read_only", request);
  },
  getGovernanceEvidence(request: { tenantId: string; objectId?: string }) {
    return kdsV2Repository.preview("read_only", request);
  },
};
