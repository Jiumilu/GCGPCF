import type {
  WaesActionGatePrecheckNoWrite,
  WaesActionGatePrecheckStatus,
} from "./waes-action-gate-precheck";
import type { WaesGateType } from "./waes-gate";
import type { WaesReasonCode, WaesReviewerRequirement } from "./waes-gate-io";

export type WaesPrecheckBundleSurface = "brain" | "kwe" | "gfis_assistant";

export type WaesPrecheckBundleScope =
  | "governance_review"
  | "validation_queue"
  | "gfis_writeback_guidance";

export type WaesPrecheckBundleReadAction =
  | "view_precheck_summary"
  | "view_required_actions"
  | "view_reason_codes"
  | "view_reviewer_requirement"
  | "view_harness_evidence_hint";

export type WaesPrecheckBundleBlockedAction =
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "promote_lifecycle"
  | "write_business_system"
  | "complete_committee_decision"
  | "confirm_revenue_or_score";

export interface WaesPrecheckGateSummary {
  gateType: WaesGateType;
  status: WaesActionGatePrecheckStatus;
  count: number;
}

export interface WaesPrecheckBundleReadModel {
  bundleId: string;
  surface: WaesPrecheckBundleSurface;
  tenantId: string;
  projectId: string;
  scope: WaesPrecheckBundleScope;
  precheckRefs: string[];
  routeRefs: string[];
  gateSummary: WaesPrecheckGateSummary[];
  reasonCodeSummary: WaesReasonCode[];
  requiredActions: string[];
  reviewerRequirements: WaesReviewerRequirement[];
  allowedReadActions: WaesPrecheckBundleReadAction[];
  blockedActions: WaesPrecheckBundleBlockedAction[];
  canCreateWaesGateResult: false;
  canCreateKweWorkItem: false;
  canPromoteLifecycle: false;
  noWrite: WaesActionGatePrecheckNoWrite;
}

export interface WaesPrecheckBundleReadModelPolicy {
  policyId: "okf.waes_precheck_bundle_read_model_policy";
  version: string;
  surfaces: WaesPrecheckBundleSurface[];
  scopes: WaesPrecheckBundleScope[];
  allowedReadActions: WaesPrecheckBundleReadAction[];
  blockedWriteActions: WaesPrecheckBundleBlockedAction[];
  hardBoundaries: {
    readModelOnly: boolean;
    canCreateWaesGateResultMustBeFalse: boolean;
    canCreateKweWorkItemMustBeFalse: boolean;
    canPromoteLifecycleMustBeFalse: boolean;
    bundleIsNotGateResult: boolean;
    bundleIsNotWorkItem: boolean;
    bundleIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: WaesActionGatePrecheckNoWrite;
}
