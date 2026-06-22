import type {
  KweQueueActionIntakeNoWrite,
  KweQueueActionType,
  KweQueueActionIntakeRequest,
} from "./kwe-queue-action-intake-request";

export type KweActionValidationCheck =
  | "actor_permission"
  | "route_consistency"
  | "payload_integrity"
  | "evidence_presence"
  | "metadata_only_boundary"
  | "blocked_reason_presence"
  | "no_write_guard";

export type KweActionValidationStatus =
  | "validation_passed"
  | "repair_required"
  | "committee_review_candidate"
  | "freeze_review_candidate"
  | "blocked";

export interface KweActionValidationCheckResult {
  check: KweActionValidationCheck;
  status: "passed" | "repair_required" | "blocked";
  reasonCodes: string[];
}

export interface KweActionValidationWorkpack {
  workpackId: string;
  requestRef: string;
  tenantId: string;
  projectId: string;
  sourceViewRef: string;
  routeRef: string;
  surface: KweQueueActionIntakeRequest["surface"];
  actorId: string;
  actionType: KweQueueActionType;
  validationStatus: KweActionValidationStatus;
  validationChecks: KweActionValidationCheckResult[];
  acceptedPayloadRefs: string[];
  acceptedEvidenceRefs: string[];
  rejectedRefs: string[];
  requiredFollowups: string[];
  validationNotes: string[];
  createsKweWorkItem: false;
  promotesLifecycle: false;
  noWrite: KweQueueActionIntakeNoWrite;
}

export interface KweActionValidationWorkpackPolicy {
  policyId: "okf.kwe_action_validation_workpack_policy";
  version: string;
  validationChecks: KweActionValidationCheck[];
  validationStatuses: KweActionValidationStatus[];
  hardBoundaries: {
    validationOnly: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    validationIsNotApprovalCompletion: boolean;
    validationIsNotCommitteeDecisionCompletion: boolean;
    validationIsNotBusinessWriteback: boolean;
    metadataOnlyCannotIncludeRawContent: boolean;
    blockedWorkpackCannotApprove: boolean;
  };
  noWriteGuards: KweQueueActionIntakeNoWrite;
}
