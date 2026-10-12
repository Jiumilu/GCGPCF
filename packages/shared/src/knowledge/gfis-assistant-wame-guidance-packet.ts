import type { WamePrecheckBundleBlockedAction } from "./wame-precheck-bundle-read-model";

export type GfisAssistantWameGuidanceSurface = "gfis_assistant";

export type GfisAssistantWameGuidanceMode =
  | "writeback_blocked"
  | "repair_guidance"
  | "metadata_only_guidance"
  | "committee_guidance"
  | "freeze_guidance";

export type GfisAssistantWameAllowedAction =
  | "explain_wame_gate"
  | "suggest_repair"
  | "show_metadata_boundary"
  | "show_manual_confirmation"
  | "show_committee_path"
  | "show_harness_evidence_hint";

export type GfisAssistantWameBlockedAction =
  | "approve_business_write"
  | WamePrecheckBundleBlockedAction;

export interface GfisAssistantWameGuidanceNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWameGateResult: 0;
  writesKweWorkItem: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesTargetReceipt: 0;
  writesCommitteeDecisionCompletion: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesQuotaTransfer: 0;
  writesBountySettlement: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantWameGuidancePacket {
  packetId: string;
  bundleRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWameGuidanceSurface;
  guidanceMode: GfisAssistantWameGuidanceMode;
  writebackExplanation: string;
  repairPrompts: string[];
  metadataOnlyHints: string[];
  manualConfirmationPoints: string[];
  committeeTriggers: string[];
  blockedActions: GfisAssistantWameBlockedAction[];
  allowedAssistantActions: GfisAssistantWameAllowedAction[];
  approvedForBusinessWrite: false;
  createsWameGateResult: false;
  createsKweWorkItem: false;
  promotesLifecycle: false;
  noWrite: GfisAssistantWameGuidanceNoWrite;
}

export interface GfisAssistantWameGuidancePacketPolicy {
  policyId: "okf.gfis_assistant_wame_guidance_packet_policy";
  version: string;
  assistantSurfaces: GfisAssistantWameGuidanceSurface[];
  guidanceModes: GfisAssistantWameGuidanceMode[];
  allowedAssistantActions: GfisAssistantWameAllowedAction[];
  blockedActions: GfisAssistantWameBlockedAction[];
  hardBoundaries: {
    guidanceOnly: boolean;
    approvedForBusinessWriteMustBeFalse: boolean;
    createsWameGateResultMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    packetIsNotWritebackApproval: boolean;
    packetIsNotGateResult: boolean;
    packetIsNotWorkItem: boolean;
    packetIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: GfisAssistantWameGuidanceNoWrite;
}
