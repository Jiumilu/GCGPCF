import type {
  EvidenceRecord,
  FactCandidate,
  KnowledgeDomain,
  KnowledgeObject,
  KdsPoolCode,
  PoolBinding,
  RagAdmission,
  SopCandidate,
  SourceRecord,
  TrustLevel,
  WaesGateResult,
  WritebackCandidate,
} from "../../../../shared/src/knowledge";

export interface ApiResult<T> {
  ok: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

export interface ListDomainsResponse {
  domains: KnowledgeDomain[];
}

export interface ListPoolsResponse {
  pools: KdsPoolCode[];
}

export interface KnowledgeSearchContext {
  userId: string;
  tenantId: string;
  scope:
    | "current_domain"
    | "my_workspace"
    | "project_delivery"
    | "org_reuse"
    | "supply_chain"
    | "audit"
    | "gfis"
    | "waes"
    | "all_accessible"
    | "public";
  domain?: KnowledgeDomain;
  projectId?: string;
  supplyChainNodeId?: string;
  poolRefs?: KdsPoolCode[];
  domainTags?: string[];
  minTrustLevel?: TrustLevel;
  ragAdmission?: RagAdmission;
  includeGovernance?: boolean;
  includeArchived?: boolean;
  query: string;
}

export interface KnowledgeSearchResult {
  object: KnowledgeObject;
  poolBindings: PoolBinding[];
  latestGateResults: WaesGateResult[];
  canShare: boolean;
  canPromote: boolean;
  canUseForRag: boolean;
  canWriteback: boolean;
}

export interface KnowledgeSearchResponse {
  results: KnowledgeSearchResult[];
  total: number;
}

export interface ImportSourceRequest {
  tenantId: string;
  source: SourceRecord;
  initialPoolRefs: KdsPoolCode[];
  evidenceRefs?: string[];
}

export interface ImportSourceResponse {
  source: SourceRecord;
  object: KnowledgeObject;
  poolBindings: PoolBinding[];
}

export interface CreateEvidenceRequest {
  tenantId: string;
  evidence: EvidenceRecord;
}

export interface CreateFactCandidateRequest {
  tenantId: string;
  candidate: FactCandidate;
}

export interface CreateSopCandidateRequest {
  tenantId: string;
  candidate: SopCandidate;
}

export interface CreateWritebackCandidateRequest {
  tenantId: string;
  candidate: WritebackCandidate;
}

export interface GetObjectResponse {
  object: KnowledgeObject;
  sources: SourceRecord[];
  evidence: EvidenceRecord[];
  poolBindings: PoolBinding[];
  gateResults: WaesGateResult[];
}

export interface GraphQueryRequest {
  tenantId: string;
  objectRefs?: string[];
  poolRefs?: KdsPoolCode[];
  maxDepth?: number;
}

export interface GraphQueryResponse {
  nodes: KnowledgeObject[];
  edges: Array<{
    fromObjectId: string;
    toObjectId: string;
    relationType: string;
    evidenceRefs: string[];
  }>;
}
