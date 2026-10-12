import type {
  WameActionGatePrecheckNoWrite,
  WameActionGatePrecheckStatus,
} from "./wame-action-gate-precheck";
import type { WameGateType } from "./wame-gate";
import type { WameReasonCode, WameReviewerRequirement } from "./wame-gate-io";

export type WamePrecheckBundleSurface = "brain" | "kwe" | "gfis_assistant";

export type WamePrecheckBundleScope =
  | "governance_review"
  | "validation_queue"
  | "gfis_writeback_guidance";

export type WamePrecheckBundleReadAction =
  | "view_precheck_summary"
  | "view_required_actions"
  | "view_reason_codes"
  | "view_reviewer_requirement"
  | "view_harness_evidence_hint";

export type WamePrecheckBundleBlockedAction =
  | "create_wame_gate_result"
  | "create_kwe_work_item"
  | "promote_lifecycle"
  | "write_business_system"
  | "complete_committee_decision"
  | "confirm_revenue_or_score";

export interface WamePrecheckGateSummary {
  gateType: WameGateType;
  status: WameActionGatePrecheckStatus;
  count: number;
}

export interface WamePrecheckBundleReadModel {
  bundleId: string;
  surface: WamePrecheckBundleSurface;
  tenantId: string;
  projectId: string;
  scope: WamePrecheckBundleScope;
  precheckRefs: string[];
  routeRefs: string[];
  gateSummary: WamePrecheckGateSummary[];
  reasonCodeSummary: WameReasonCode[];
  requiredActions: string[];
  reviewerRequirements: WameReviewerRequirement[];
  allowedReadActions: WamePrecheckBundleReadAction[];
  blockedActions: WamePrecheckBundleBlockedAction[];
  canCreateWameGateResult: false;
  canCreateKweWorkItem: false;
  canPromoteLifecycle: false;
  noWrite: WameActionGatePrecheckNoWrite;
}

export interface WamePrecheckBundleReadModelPolicy {
  policyId: "okf.wame_precheck_bundle_read_model_policy";
  version: string;
  surfaces: WamePrecheckBundleSurface[];
  scopes: WamePrecheckBundleScope[];
  allowedReadActions: WamePrecheckBundleReadAction[];
  blockedWriteActions: WamePrecheckBundleBlockedAction[];
  hardBoundaries: {
    readModelOnly: boolean;
    canCreateWameGateResultMustBeFalse: boolean;
    canCreateKweWorkItemMustBeFalse: boolean;
    canPromoteLifecycleMustBeFalse: boolean;
    bundleIsNotGateResult: boolean;
    bundleIsNotWorkItem: boolean;
    bundleIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: WameActionGatePrecheckNoWrite;
}
