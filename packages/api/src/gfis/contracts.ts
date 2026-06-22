import type {
  KnowledgeSearchResult,
} from "../kds/v2/contracts";
import type {
  FactCandidate,
  GapRecord,
  RagAdmissionDecision,
  WaesGateResult,
  WritebackCandidate,
} from "../../../shared/src/knowledge";

export interface GfisAssistantQueryRequest {
  tenantId: string;
  userId: string;
  projectId: string;
  query: string;
  poolRefs?: string[];
}

export interface GfisAssistantQueryResponse {
  answer: string;
  citations: KnowledgeSearchResult[];
  gaps: GapRecord[];
  ragDecisions: RagAdmissionDecision[];
  noWrite: true;
}

export interface GfisDocumentAcceptanceRequest {
  tenantId: string;
  userId: string;
  projectId: string;
  sourceObjectId: string;
}

export interface GfisDocumentAcceptanceResponse {
  factCandidates: FactCandidate[];
  gaps: GapRecord[];
  gateResults: WaesGateResult[];
  requiresHumanConfirmation: boolean;
  requiresCommittee: boolean;
  noWrite: true;
}

export interface GfisWritebackCandidateRequest {
  tenantId: string;
  userId: string;
  candidate: WritebackCandidate;
}

export interface GfisWritebackCandidateResponse {
  candidate: WritebackCandidate;
  gateResults: WaesGateResult[];
  approvedForBusinessWrite: boolean;
  noWrite: true;
  businessWrites: 0;
  externalApiWrites: 0;
}
