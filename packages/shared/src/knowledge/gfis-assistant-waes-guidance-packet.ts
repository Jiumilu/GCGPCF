import type { WaesPrecheckBundleBlockedAction } from "./waes-precheck-bundle-read-model";

export type GfisAssistantWaesGuidanceSurface = "gfis_assistant";

export type GfisAssistantWaesGuidanceMode =
  | "writeback_blocked"
  | "repair_guidance"
  | "metadata_only_guidance"
  | "committee_guidance"
  | "freeze_guidance";

export type GfisAssistantWaesAllowedAction =
  | "explain_waes_gate"
  | "suggest_repair"
  | "show_metadata_boundary"
  | "show_manual_confirmation"
  | "show_committee_path"
  | "show_harness_evidence_hint";

export type GfisAssistantWaesBlockedAction =
  | "approve_business_write"
  | WaesPrecheckBundleBlockedAction;

export interface GfisAssistantWaesGuidanceNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
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

export interface GfisAssistantWaesGuidancePacket {
  packetId: string;
  bundleRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWaesGuidanceSurface;
  guidanceMode: GfisAssistantWaesGuidanceMode;
  writebackExplanation: string;
  repairPrompts: string[];
  metadataOnlyHints: string[];
  manualConfirmationPoints: string[];
  committeeTriggers: string[];
  blockedActions: GfisAssistantWaesBlockedAction[];
  allowedAssistantActions: GfisAssistantWaesAllowedAction[];
  approvedForBusinessWrite: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  promotesLifecycle: false;
  noWrite: GfisAssistantWaesGuidanceNoWrite;
}

export interface GfisAssistantWaesGuidancePacketPolicy {
  policyId: "okf.gfis_assistant_waes_guidance_packet_policy";
  version: string;
  assistantSurfaces: GfisAssistantWaesGuidanceSurface[];
  guidanceModes: GfisAssistantWaesGuidanceMode[];
  allowedAssistantActions: GfisAssistantWaesAllowedAction[];
  blockedActions: GfisAssistantWaesBlockedAction[];
  hardBoundaries: {
    guidanceOnly: boolean;
    approvedForBusinessWriteMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    packetIsNotWritebackApproval: boolean;
    packetIsNotGateResult: boolean;
    packetIsNotWorkItem: boolean;
    packetIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: GfisAssistantWaesGuidanceNoWrite;
}
