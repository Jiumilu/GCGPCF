import type {
  GfisAssistantWaesBlockedAction,
  GfisAssistantWaesGuidanceSurface,
} from "./gfis-assistant-waes-guidance-packet";

export type GfisAssistantRepairPromptItemType =
  | "source_repair"
  | "evidence_repair"
  | "owner_confirmation"
  | "metadata_only_review"
  | "committee_material"
  | "freeze_risk_material";

export type GfisAssistantRepairPromptItemStatus =
  | "open"
  | "ready_for_submission"
  | "repair_required"
  | "blocked";

export type GfisAssistantRepairPromptChecklistStatus =
  | "open"
  | "repair_required"
  | "blocked";

export type GfisAssistantRepairPromptDisplayAction =
  | "show_repair_item"
  | "show_required_evidence"
  | "show_metadata_boundary"
  | "show_owner_confirmation"
  | "show_committee_material"
  | "show_freeze_risk_material";

export type GfisAssistantRepairPromptBlockedAction =
  | "submit_evidence"
  | "create_gap_record"
  | "create_bounty_record"
  | GfisAssistantWaesBlockedAction;

export interface GfisAssistantRepairPromptChecklistNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesGapRecord: 0;
  writesBountyRecord: 0;
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

export interface GfisAssistantRepairPromptChecklistItem {
  itemId: string;
  itemType: GfisAssistantRepairPromptItemType;
  itemStatus: GfisAssistantRepairPromptItemStatus;
  prompt: string;
  requiredRefs: string[];
  evidenceHintRefs: string[];
  metadataOnly: boolean;
}

export interface GfisAssistantRepairPromptChecklist {
  checklistId: string;
  guidancePacketRef: string;
  tenantId: string;
  projectId: string;
  assistantSurface: GfisAssistantWaesGuidanceSurface;
  checklistStatus: GfisAssistantRepairPromptChecklistStatus;
  items: GfisAssistantRepairPromptChecklistItem[];
  blockedActions: GfisAssistantRepairPromptBlockedAction[];
  allowedDisplayActions: GfisAssistantRepairPromptDisplayAction[];
  submitsEvidence: false;
  createsGapRecord: false;
  createsBountyRecord: false;
  createsKweWorkItem: false;
  createsWaesGateResult: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  noWrite: GfisAssistantRepairPromptChecklistNoWrite;
}

export interface GfisAssistantRepairPromptChecklistPolicy {
  policyId: "okf.gfis_assistant_repair_prompt_checklist_policy";
  version: string;
  itemTypes: GfisAssistantRepairPromptItemType[];
  itemStatuses: GfisAssistantRepairPromptItemStatus[];
  checklistStatuses: GfisAssistantRepairPromptChecklistStatus[];
  allowedDisplayActions: GfisAssistantRepairPromptDisplayAction[];
  blockedActions: GfisAssistantRepairPromptBlockedAction[];
  hardBoundaries: {
    checklistOnly: boolean;
    submitsEvidenceMustBeFalse: boolean;
    createsGapRecordMustBeFalse: boolean;
    createsBountyRecordMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    checklistIsNotSubmission: boolean;
    checklistIsNotAcceptance: boolean;
    checklistIsNotBusinessWriteback: boolean;
  };
  noWriteGuards: GfisAssistantRepairPromptChecklistNoWrite;
}
