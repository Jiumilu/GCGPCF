export const KNOWLEDGE_DOMAINS = [
  "private",
  "workspace",
  "project",
  "org",
  "supply_chain",
  "public",
  "governance",
] as const;

export type KnowledgeDomain = (typeof KNOWLEDGE_DOMAINS)[number];

export const KNOWLEDGE_OBJECT_TYPES = [
  "source",
  "claim",
  "fact",
  "entity",
  "relation",
  "view",
  "evidence",
  "policy",
  "event",
  "fact_candidate",
  "sop_candidate",
  "writeback_candidate",
  "gap",
  "bounty",
  "contribution",
  "decision",
  "revenue",
  "quota",
  "dispute",
] as const;

export type KnowledgeObjectType = (typeof KNOWLEDGE_OBJECT_TYPES)[number];

export type KnowledgeOwnerType =
  | "user"
  | "team"
  | "project"
  | "org"
  | "external_account"
  | "system";

export type KnowledgeVisibility =
  | "private"
  | "restricted"
  | "internal"
  | "external_shared"
  | "public";

export type KnowledgeLifecycle =
  | "draft"
  | "candidate"
  | "reviewing"
  | "repair_required"
  | "evidence_ready"
  | "verified"
  | "accepted"
  | "published"
  | "frozen"
  | "superseded"
  | "archived";

export type TrustLevel = "T0" | "T1" | "T2" | "T3" | "T4" | "T5";

export type RagAdmission =
  | "safe"
  | "limited"
  | "repair_required"
  | "blocked"
  | "sensitive_metadata_only";

export type ConfirmationStatus =
  | "not_required"
  | "ai_checked"
  | "human_required"
  | "human_confirmed"
  | "committee_required"
  | "committee_confirmed"
  | "rejected";

export interface KnowledgeObject {
  id: string;
  uri: string;
  tenantId: string;
  domain: KnowledgeDomain;
  objectType: KnowledgeObjectType;
  poolRefs: string[];
  projectId?: string;
  supplyChainNodeId?: string;
  businessSystemRef?: string;
  ownerType: KnowledgeOwnerType;
  ownerId: string;
  visibility: KnowledgeVisibility;
  lifecycle: KnowledgeLifecycle;
  trustLevel: TrustLevel;
  ragAdmission: RagAdmission;
  confirmationStatus: ConfirmationStatus;
  sourceRefs: string[];
  evidenceRefs: string[];
  lineageRefs: string[];
  createdAt: string;
  updatedAt: string;
}
