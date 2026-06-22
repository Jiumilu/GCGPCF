import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairEventPreviewAuditTraceType =
  | "display_audit_trace"
  | "repair_audit_trace"
  | "metadata_boundary_audit_trace"
  | "committee_audit_trace"
  | "freeze_audit_trace"
  | "blocked_write_audit_trace";

export type GfisAssistantRepairEventPreviewAuditTraceStatus =
  | "trace_preview_only"
  | "blocked_trace_preview"
  | "metadata_trace_preview"
  | "repair_trace_preview"
  | "committee_trace_preview"
  | "freeze_trace_preview";

export type GfisAssistantRepairEventPreviewAuditTraceDecision =
  | "show_trace_only"
  | "show_repair_trace"
  | "show_metadata_boundary_trace"
  | "show_committee_trace"
  | "show_freeze_trace"
  | "show_blocked_write_trace";

export type GfisAssistantRepairEventPreviewAuditTraceBlockedAction =
  | "create_audit_trace_record"
  | "create_event_record"
  | "create_action_receipt"
  | "create_read_receipt"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairEventPreviewAuditTraceNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesAuditTraceRecord: 0;
  writesEventRecord: 0;
  writesActionReceipt: 0;
  writesReadReceipt: 0;
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

export interface GfisAssistantRepairEventPreviewAuditTrace {
  auditTraceId: string;
  eventPreviewRef: string;
  actionGuardRef: string;
  readModelRef: string;
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  traceType: GfisAssistantRepairEventPreviewAuditTraceType;
  traceStatus: GfisAssistantRepairEventPreviewAuditTraceStatus;
  traceDecision: GfisAssistantRepairEventPreviewAuditTraceDecision;
  traceSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  auditNoteRefs: string[];
  blockedActions: GfisAssistantRepairEventPreviewAuditTraceBlockedAction[];
  createsAuditTraceRecord: false;
  createsEventRecord: false;
  createsActionReceipt: false;
  createsReadReceipt: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairEventPreviewAuditTraceNoWrite;
}

export interface GfisAssistantRepairEventPreviewAuditTracePolicy {
  policyId: "okf.gfis_assistant_repair_event_preview_audit_trace_policy";
  version: string;
  traceTypes: GfisAssistantRepairEventPreviewAuditTraceType[];
  traceStatuses: GfisAssistantRepairEventPreviewAuditTraceStatus[];
  traceDecisions: GfisAssistantRepairEventPreviewAuditTraceDecision[];
  blockedActions: GfisAssistantRepairEventPreviewAuditTraceBlockedAction[];
  hardBoundaries: {
    auditTracePreviewOnly: boolean;
    auditTracePreviewIsNotAuditTraceRecord: boolean;
    auditTracePreviewIsNotEventRecord: boolean;
    auditTracePreviewIsNotActionReceipt: boolean;
    auditTracePreviewIsNotReadReceipt: boolean;
    auditTracePreviewIsNotHarnessEvidence: boolean;
    auditTracePreviewIsNotWaesResult: boolean;
    auditTracePreviewIsNotKweWorkItem: boolean;
    auditTracePreviewIsNotLifecycleChange: boolean;
    auditTracePreviewIsNotBusinessWriteback: boolean;
    createsAuditTraceRecordMustBeFalse: boolean;
    createsEventRecordMustBeFalse: boolean;
    createsActionReceiptMustBeFalse: boolean;
    createsReadReceiptMustBeFalse: boolean;
    createsHarnessEvidenceMustBeFalse: boolean;
    createsWaesGateResultMustBeFalse: boolean;
    createsKweWorkItemMustBeFalse: boolean;
    persistsEvidenceMustBeFalse: boolean;
    approvesBusinessWriteMustBeFalse: boolean;
    promotesLifecycleMustBeFalse: boolean;
    completesCommitteeDecisionMustBeFalse: boolean;
  };
  noWriteGuards: GfisAssistantRepairEventPreviewAuditTraceNoWrite;
}
