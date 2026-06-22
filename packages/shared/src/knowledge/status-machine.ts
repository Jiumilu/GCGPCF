import type { KnowledgeLifecycle } from "./object";

export type KnowledgeStateActor =
  | "ai"
  | "owner"
  | "system"
  | "kds"
  | "waes"
  | "kwe"
  | "human_reviewer"
  | "committee"
  | "publication_owner"
  | "governance_owner";

export type KnowledgeAllowedOperation =
  | "search"
  | "rag_weak_reference"
  | "rag_strong_reference"
  | "writeback_candidate"
  | "formal_writeback"
  | "contribution_candidate"
  | "revenue_confirmation"
  | "publication"
  | "freeze"
  | "archive";

export interface KnowledgeLifecycleStateRule {
  state: KnowledgeLifecycle;
  terminal: boolean;
  allowedOperations: KnowledgeAllowedOperation[];
}

export interface KnowledgeStatePromotionRule {
  id: string;
  from: KnowledgeLifecycle | "any";
  to: KnowledgeLifecycle;
  allowedActors: KnowledgeStateActor[];
  requires: string[];
}

export interface KnowledgeStateMachinePolicy {
  policyId: string;
  version: string;
  lifecycleStates: KnowledgeLifecycleStateRule[];
  promotionRules: KnowledgeStatePromotionRule[];
  hardBoundaries: {
    aiAllowedTargetStates: KnowledgeLifecycle[];
    loopAllowedTargetStates: KnowledgeLifecycle[];
    aiCannotPromoteTo: KnowledgeLifecycle[];
    loopCannotPromoteTo: KnowledgeLifecycle[];
    terminalStates: KnowledgeLifecycle[];
    formalWritebackRequiresAccepted: boolean;
    revenueConfirmationRequiresAccepted: boolean;
    templateIsNotFact: boolean;
  };
  noWriteAssertions: {
    writesKdsFact: 0;
    writesBusinessSystem: 0;
    writesRevenueDistribution: 0;
    writesExternalApi: 0;
  };
}
