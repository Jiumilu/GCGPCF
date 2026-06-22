import type {
  KnowledgeDomain,
  KnowledgeVisibility,
  RagAdmission,
  TrustLevel,
} from "./object";
import type { KdsPoolCode } from "./pool";
import type { RagCitationStrength } from "./rag-citation-strength";

export type RagAssistantSurface =
  | "brain"
  | "pkc"
  | "gfis_knowledge_assistant"
  | "gfis_usage_assistant"
  | "gfis_document_acceptance_assistant"
  | "command_center"
  | "agent";

export type RagAnswerMode =
  | "no_answer"
  | "metadata_only"
  | "weak_answer"
  | "strong_answer"
  | "business_assist"
  | "blocked_with_reason";

export interface RagResponseCitation {
  citationId: string;
  objectId: string;
  sourceRefs: string[];
  evidenceRefs: string[];
  trustLevel: TrustLevel;
  ragAdmission: RagAdmission;
  citationStrength: Exclude<RagCitationStrength, "L0">;
  domain: KnowledgeDomain;
  poolRefs: KdsPoolCode[];
  visibility: KnowledgeVisibility;
  metadataOnly: boolean;
  redacted: boolean;
  canUseForAnswer: boolean;
  canUseForStrongReference: boolean;
  canUseForBusinessAssist: boolean;
}

export interface RagResponseCitationPacket {
  packetId: string;
  tenantId: string;
  userId: string;
  assistantSurface: RagAssistantSurface;
  query: string;
  answerMode: RagAnswerMode;
  citations: RagResponseCitation[];
  highestCitationStrength: Exclude<RagCitationStrength, "L0">;
  boundaryNotices: string[];
  missingEvidenceRefs: string[];
  waesGateRefs: string[];
  aclDecisionRefs: string[];
  generatedAt: string;
  noWrite: true;
  writesKdsFact: false;
  writesWaesGateResult: false;
  writesKweWorkItem: false;
  writesBusinessSystem: false;
  writesExternalApi: false;
}

export interface RagResponseCitationPacketPolicy {
  policyId: string;
  version: string;
  assistantSurfaces: RagAssistantSurface[];
  answerModes: RagAnswerMode[];
  minimumPacketFields: string[];
  minimumCitationFields: string[];
  requiredBoundaryNotices: string[];
  hardBoundaries: {
    l0CitationAllowed: false;
    metadataOnlyRawContentAllowed: false;
    l3RequiresBoundaryNotice: boolean;
    l4L5AutoWritebackAllowed: false;
    l5ReplacesHumanOrCommittee: false;
    missingEvidenceAllowsStrongAnswer: false;
    blockedRagAllowedInPacket: false;
    t5AiOnlyAllowedAsFact: false;
    noAclAllowedInPacket: false;
    packetPassIsFormalFact: false;
  };
  noWriteAssertions: {
    writesKdsFact: 0;
    writesWaesGateResult: 0;
    writesKweWorkItem: 0;
    writesBusinessSystem: 0;
    writesRevenueOrScoreConfirmation: 0;
    writesExternalApi: 0;
  };
}
