import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairAuditTraceReadReceiptPreviewType =
  | "display_read_receipt_preview"
  | "repair_read_receipt_preview"
  | "metadata_boundary_read_receipt_preview"
  | "committee_read_receipt_preview"
  | "freeze_read_receipt_preview"
  | "blocked_write_read_receipt_preview";

export type GfisAssistantRepairAuditTraceReadReceiptPreviewStatus =
  | "receipt_preview_only"
  | "blocked_receipt_preview"
  | "metadata_receipt_preview"
  | "repair_receipt_preview"
  | "committee_receipt_preview"
  | "freeze_receipt_preview";

export type GfisAssistantRepairAuditTraceReadReceiptPreviewDecision =
  | "show_receipt_preview_only"
  | "show_repair_receipt_preview"
  | "show_metadata_boundary_receipt_preview"
  | "show_committee_receipt_preview"
  | "show_freeze_receipt_preview"
  | "show_blocked_write_receipt_preview";

export type GfisAssistantRepairAuditTraceReadReceiptPreviewBlockedAction =
  | "create_read_receipt"
  | "create_audit_trace_record"
  | "create_event_record"
  | "create_action_receipt"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairAuditTraceReadReceiptPreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesReadReceipt: 0;
  writesAuditTraceRecord: 0;
  writesEventRecord: 0;
  writesActionReceipt: 0;
  writesHarnessEvidence: 0;
  writesAdmissionRecord: 0;
  writesReviewQueueItem: 0;
  writesConfirmationRecord: 0;
  writesDecisionRecord: 0;
  writesGapRecord: 0;
  writesBountyRecord: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesEvidenceRecord: 0;
  writesTargetReceipt: 0;
  writesCommitteeDecisionCompletion: 0;
  writesRevenueOrScoreConfirmation: 0;
  writesQuotaTransfer: 0;
  writesBountySettlement: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantRepairAuditTraceReadReceiptPreview {
  readReceiptPreviewId: string;
  auditTraceRef: string;
  eventPreviewRef: string;
  actionGuardRef: string;
  readModelRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  receiptType: GfisAssistantRepairAuditTraceReadReceiptPreviewType;
  receiptStatus: GfisAssistantRepairAuditTraceReadReceiptPreviewStatus;
  receiptDecision: GfisAssistantRepairAuditTraceReadReceiptPreviewDecision;
  receiptSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  receiptNoteRefs: string[];
  blockedActions: GfisAssistantRepairAuditTraceReadReceiptPreviewBlockedAction[];
  createsReadReceipt: false;
  createsAuditTraceRecord: false;
  createsEventRecord: false;
  createsActionReceipt: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairAuditTraceReadReceiptPreviewNoWrite;
}

export interface GfisAssistantRepairAuditTraceReadReceiptPreviewPolicy {
  policyId: "okf.gfis_assistant_repair_audit_trace_read_receipt_preview_policy";
  version: string;
  receiptTypes: GfisAssistantRepairAuditTraceReadReceiptPreviewType[];
  receiptStatuses: GfisAssistantRepairAuditTraceReadReceiptPreviewStatus[];
  receiptDecisions: GfisAssistantRepairAuditTraceReadReceiptPreviewDecision[];
  blockedActions: GfisAssistantRepairAuditTraceReadReceiptPreviewBlockedAction[];
  hardBoundaries: {
    readReceiptPreviewOnly: boolean;
    readReceiptPreviewIsNotReadReceipt: boolean;
    readReceiptPreviewIsNotAuditTraceRecord: boolean;
    readReceiptPreviewIsNotEventRecord: boolean;
    readReceiptPreviewIsNotActionReceipt: boolean;
    readReceiptPreviewIsNotHarnessEvidence: boolean;
    readReceiptPreviewIsNotWaesResult: boolean;
    readReceiptPreviewIsNotKweWorkItem: boolean;
    readReceiptPreviewIsNotLifecycleChange: boolean;
    readReceiptPreviewIsNotBusinessWriteback: boolean;
    createsReadReceiptMustBeFalse: boolean;
    createsAuditTraceRecordMustBeFalse: boolean;
    createsEventRecordMustBeFalse: boolean;
    createsActionReceiptMustBeFalse: boolean;
    createsHarnessEvidenceMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    completesCommitteeDecisionMustBeFalse: boolean;
  };
  noWriteGuards: GfisAssistantRepairAuditTraceReadReceiptPreviewNoWrite;
}
