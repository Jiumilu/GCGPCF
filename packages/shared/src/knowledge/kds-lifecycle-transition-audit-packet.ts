import type { KnowledgeLifecycle, KnowledgeObjectType } from "./object";
import type {
  KwePromotionRequestActor,
  KwePromotionReviewerRequirement,
} from "./kwe-promotion-request";

export type KdsLifecycleTransitionAuditStatus =
  | "ready_for_review"
  | "repair_required"
  | "waes_required"
  | "human_required"
  | "committee_required"
  | "publication_required"
  | "freeze_required"
  | "blocked";

export interface KdsLifecycleTransitionAuditNoWrite {
  writesKdsLifecycle: 0;
  writesAcceptedFact: 0;
  writesPublishedObject: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesBusinessSystem: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesExternalApi: 0;
}

export interface KdsLifecycleTransitionAuditPacket {
  auditId: string;
  tenantId: string;
  targetObjectId: string;
  targetObjectType: KnowledgeObjectType;
  fromLifecycle: KnowledgeLifecycle;
  toLifecycle: KnowledgeLifecycle;
  transitionActor: KwePromotionRequestActor;
  promotionRequestRefs: string[];
  sourceRefs: string[];
  evidenceRefs: string[];
  waesGateRefs: string[];
  workpackRefs: string[];
  harnessEvidenceRefs: string[];
  decisionRefs: string[];
  reviewerRequirement: KwePromotionReviewerRequirement;
  auditStatus: KdsLifecycleTransitionAuditStatus;
  blockedReasons: string[];
  requiredActions: string[];
  noWrite: KdsLifecycleTransitionAuditNoWrite;
}

export interface KdsLifecycleTransitionAuditPacketPolicy {
  policyId: "okf.kds_lifecycle_transition_audit_packet_policy";
  version: string;
  requiredFields: string[];
  auditStatuses: KdsLifecycleTransitionAuditStatus[];
  transitionActors: KwePromotionRequestActor[];
  reviewerRequirements: KwePromotionReviewerRequirement[];
  hardBoundaries: {
    auditPacketIsNotLifecycleMutation: boolean;
    aiAndLoopCannotAuditHighTrustAsApproved: boolean;
    acceptedRequiresHumanOrCommittee: boolean;
    publishedRequiresPublicationControls: boolean;
    frozenRequiresFreezeReason: boolean;
    terminalStatesBlockTransition: boolean;
    harnessEvidenceIsRequiredForHighTrust: boolean;
    auditPassIsNotBusinessCompletion: boolean;
  };
  noWriteGuards: KdsLifecycleTransitionAuditNoWrite;
}
