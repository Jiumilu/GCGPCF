import type { KnowledgeLifecycle, KnowledgeObjectType } from "./object";
import type { KnowledgeStateActor } from "./status-machine";
import type { WaesReviewerRequirement } from "./waes-gate-io";

export type KwePromotionRequestActor = KnowledgeStateActor | "loop";

export type KwePromotionStatus =
  | "draft_request"
  | "ready_for_kwe_review"
  | "repair_required"
  | "waes_required"
  | "human_required"
  | "committee_required"
  | "freeze_required"
  | "blocked";

export type KwePromotionReviewerRequirement =
  | WaesReviewerRequirement
  | "publication_owner_required";

export interface KwePromotionNoWrite {
  writesKdsLifecycle: 0;
  writesAcceptedFact: 0;
  writesPublishedObject: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesBusinessSystem: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesExternalApi: 0;
}

export interface KwePromotionRequest {
  id: string;
  tenantId: string;
  targetObjectId: string;
  targetObjectType: KnowledgeObjectType;
  currentLifecycle: KnowledgeLifecycle;
  requestedLifecycle: KnowledgeLifecycle;
  requestedBy: string;
  requestActor: KwePromotionRequestActor;
  sourceRefs: string[];
  evidenceRefs: string[];
  waesGateRefs: string[];
  workpackRefs: string[];
  harnessEvidenceRefs: string[];
  reviewerRequirement: KwePromotionReviewerRequirement;
  promotionStatus: KwePromotionStatus;
  blockedReasons: string[];
  requiredActions: string[];
  noWrite: KwePromotionNoWrite;
}

export interface KwePromotionRequestPolicy {
  policyId: "okf.kwe_promotion_request_policy";
  version: string;
  requiredFields: string[];
  promotionStatuses: KwePromotionStatus[];
  requestActors: KwePromotionRequestActor[];
  reviewerRequirements: KwePromotionReviewerRequirement[];
  hardBoundaries: {
    promotionRequestIsNotLifecycleMutation: boolean;
    aiCannotRequestVerifiedAcceptedPublished: boolean;
    loopCannotRequestVerifiedAcceptedPublished: boolean;
    acceptedRequiresHumanOrCommittee: boolean;
    publishedRequiresPublicationRedactionAclGate: boolean;
    frozenRequiresFreezeReason: boolean;
    terminalStatesCannotBePromoted: boolean;
  };
  noWriteGuards: KwePromotionNoWrite;
}
