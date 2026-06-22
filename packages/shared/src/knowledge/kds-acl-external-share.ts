import type {
  KnowledgeDomain,
  KnowledgeVisibility,
  RagAdmission,
} from "./object";
import type { KdsPoolCode } from "./pool";
import type { WaesGateStatus } from "./waes-gate";

export type KdsAclSubjectType =
  | "user"
  | "team"
  | "project"
  | "org"
  | "external_account"
  | "agent";

export type KdsAclAction =
  | "read_metadata"
  | "read_redacted_summary"
  | "read_full_content"
  | "use_for_limited_rag"
  | "use_for_safe_rag"
  | "create_candidate"
  | "request_promotion"
  | "request_external_share";

export interface KdsAclRecord {
  aclId: string;
  tenantId: string;
  subjectType: KdsAclSubjectType;
  subjectId: string;
  objectId: string;
  domain: KnowledgeDomain;
  visibility: KnowledgeVisibility;
  allowedActions: KdsAclAction[];
  deniedActions: KdsAclAction[];
  poolRefs: KdsPoolCode[];
  projectId?: string;
  supplyChainNodeId?: string;
  expiresAt?: string;
  createdBy: string;
  createdAt: string;
}

export interface KdsExternalShareView {
  viewId: string;
  tenantId: string;
  externalAccountId: string;
  objectId: string;
  visibleFields: string[];
  redactedFields: string[];
  metadataOnly: boolean;
  ragAdmission: Extract<RagAdmission, "safe" | "limited" | "sensitive_metadata_only">;
  waesGateStatus: Extract<WaesGateStatus, "passed" | "metadata_only" | "redaction_required">;
  publicationApprovalRef?: string;
  evidenceRefs: string[];
  expiresAt?: string;
}

export interface KdsAclExternalSharePolicy {
  policyId: string;
  version: string;
  subjectTypes: KdsAclSubjectType[];
  allowedActions: KdsAclAction[];
  minimumAclFields: string[];
  minimumExternalViewFields: string[];
  externalAccountDefaultActions: KdsAclAction[];
  requiredGatesForExternalShare: string[];
  hardBoundaries: {
    tenantIsolationRequired: boolean;
    supplyChainPartitionRequired: boolean;
    externalAccountCrossUnitDetailDefaultDenied: boolean;
    sensitiveMetadataOnlyRawContentDenied: boolean;
    blockedRagExternalShareDenied: boolean;
    t5AiOnlyExternalFactDenied: boolean;
    externalShareRequiresWaesGate: boolean;
    publicVisibilityRequiresPublicationApproval: boolean;
    aclPassIsNotRagStrongReference: boolean;
    aclPassIsNotBusinessWriteback: boolean;
    aclPassIsNotRevenueOrScoreConfirmation: boolean;
  };
  noWriteAssertions: {
    writesAclStore: 0;
    writesExternalSharePermission: 0;
    writesPublicationApproval: 0;
    writesKdsObject: 0;
    writesBusinessSystem: 0;
    writesRevenueOrScoreConfirmation: 0;
    writesExternalApi: 0;
  };
}
