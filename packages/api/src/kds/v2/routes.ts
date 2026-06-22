export type KdsV2HttpMethod = "GET" | "POST";

export type KdsV2MutationMode = "read_only" | "candidate_only" | "dry_run";

export interface KdsV2EndpointDefinition {
  method: KdsV2HttpMethod;
  path: string;
  handler: string;
  mutationMode: KdsV2MutationMode;
  requiresWaesGate: boolean;
  requiresKweFlow: boolean;
  directBusinessWrite: false;
  acceptedLifecycleWrite: false;
  externalApiWrite: false;
}

export const KDS_V2_ENDPOINTS: KdsV2EndpointDefinition[] = [
  {
    method: "GET",
    path: "/api/v2/domains",
    handler: "listDomains",
    mutationMode: "read_only",
    requiresWaesGate: false,
    requiresKweFlow: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "GET",
    path: "/api/v2/pools",
    handler: "listPools",
    mutationMode: "read_only",
    requiresWaesGate: false,
    requiresKweFlow: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "GET",
    path: "/api/v2/projects",
    handler: "listProjects",
    mutationMode: "read_only",
    requiresWaesGate: false,
    requiresKweFlow: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "POST",
    path: "/api/v2/search",
    handler: "searchKnowledge",
    mutationMode: "read_only",
    requiresWaesGate: false,
    requiresKweFlow: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "GET",
    path: "/api/v2/objects/{uri}",
    handler: "getKnowledgeObject",
    mutationMode: "read_only",
    requiresWaesGate: false,
    requiresKweFlow: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "POST",
    path: "/api/v2/sources/import",
    handler: "importSourceCandidate",
    mutationMode: "candidate_only",
    requiresWaesGate: true,
    requiresKweFlow: true,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "POST",
    path: "/api/v2/fact-candidates",
    handler: "createFactCandidate",
    mutationMode: "candidate_only",
    requiresWaesGate: true,
    requiresKweFlow: true,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "POST",
    path: "/api/v2/sop-candidates",
    handler: "createSopCandidate",
    mutationMode: "candidate_only",
    requiresWaesGate: true,
    requiresKweFlow: true,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "POST",
    path: "/api/v2/writeback-candidates",
    handler: "createWritebackCandidate",
    mutationMode: "candidate_only",
    requiresWaesGate: true,
    requiresKweFlow: true,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "GET",
    path: "/api/v2/graph",
    handler: "getKnowledgeGraph",
    mutationMode: "read_only",
    requiresWaesGate: false,
    requiresKweFlow: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
  {
    method: "GET",
    path: "/api/v2/governance/evidence",
    handler: "getGovernanceEvidence",
    mutationMode: "read_only",
    requiresWaesGate: false,
    requiresKweFlow: false,
    directBusinessWrite: false,
    acceptedLifecycleWrite: false,
    externalApiWrite: false,
  },
];
