import type {
  CreateGovernanceEvidenceRequest,
  CreateLoopRecordRequest,
  KnowledgeCiRunRequest,
} from "./contracts";
import { GOVERNANCE_ENDPOINTS } from "./routes";
import { governanceRepository } from "./repository";

export const governanceService = {
  endpoints: GOVERNANCE_ENDPOINTS,
  repository: governanceRepository,
  createLoopRecord(request: CreateLoopRecordRequest) {
    return governanceRepository.preview("governance_evidence_request", request);
  },
  createLoopRecordRequest(request: CreateLoopRecordRequest) {
    return governanceRepository.preview("governance_evidence_request", request);
  },
  getLoopRecord(request: { tenantId: string; loopId: string }) {
    return governanceRepository.preview("read_only", request);
  },
  createEvidence(request: CreateGovernanceEvidenceRequest) {
    return governanceRepository.preview("governance_evidence_request", request);
  },
  createGovernanceEvidenceRequest(request: CreateGovernanceEvidenceRequest) {
    return governanceRepository.preview("governance_evidence_request", request);
  },
  runKnowledgeCi(request: KnowledgeCiRunRequest) {
    return governanceRepository.preview("read_only", request);
  },
  runKnowledgeCiDryRun(request: KnowledgeCiRunRequest) {
    return governanceRepository.preview("read_only", request);
  },
  readLedger<TRequest extends Record<string, unknown>>(request: TRequest) {
    return governanceRepository.preview("ledger_read", request);
  },
  getContributionLedger(request: { tenantId: string }) {
    return governanceRepository.preview("ledger_read", request);
  },
  getRevenueLedger(request: { tenantId: string }) {
    return governanceRepository.preview("ledger_read", request);
  },
  getQuotaLedger(request: { tenantId: string }) {
    return governanceRepository.preview("ledger_read", request);
  },
  getBountyLedger(request: { tenantId: string }) {
    return governanceRepository.preview("ledger_read", request);
  },
};
