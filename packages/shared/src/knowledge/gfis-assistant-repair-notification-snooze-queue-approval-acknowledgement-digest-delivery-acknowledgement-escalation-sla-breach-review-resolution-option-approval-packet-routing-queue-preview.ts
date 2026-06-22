import type {
  GfisAssistantRepairAdmissionReadModelSurface,
} from "./gfis-assistant-repair-admission-read-model";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewType =
  | "team_routing_queue_preview"
  | "project_routing_queue_preview"
  | "governance_routing_queue_preview"
  | "external_blocked_routing_queue_preview"
  | "committee_routing_queue_preview"
  | "freeze_routing_queue_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewStatus =
  | "routing_queue_preview_only"
  | "routing_queue_evidence_required"
  | "routing_queue_metadata_boundary"
  | "routing_queue_external_blocked"
  | "routing_queue_committee_required"
  | "routing_queue_freeze_required";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewDecision =
  | "show_team_routing_queue_preview"
  | "show_project_routing_queue_preview"
  | "show_governance_routing_queue_preview"
  | "show_external_blocked_routing_queue_preview"
  | "show_committee_routing_queue_preview"
  | "show_freeze_routing_queue_preview";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewScope =
  | "team_internal"
  | "project_internal"
  | "governance_review"
  | "external_blocked"
  | "committee_review"
  | "freeze_review";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewSlot =
  | "team_lead_candidate_slot"
  | "project_owner_candidate_slot"
  | "governance_reviewer_candidate_slot"
  | "external_share_blocked_candidate_slot"
  | "committee_candidate_slot"
  | "freeze_reviewer_candidate_slot";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewPriority =
  | "normal_candidate"
  | "evidence_candidate"
  | "metadata_candidate"
  | "blocked_candidate"
  | "committee_candidate"
  | "freeze_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewReason =
  | "approval_packet_candidate"
  | "evidence_required_candidate"
  | "metadata_boundary_candidate"
  | "external_share_blocked_candidate"
  | "committee_review_candidate"
  | "freeze_review_candidate";

export type GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewBlockedAction =
  | "create_routing_queue"
  | "create_queue_item"
  | "create_approval_assignment"
  | "lock_approver"
  | "create_approval_packet"
  | "create_approval_request"
  | "create_approval_decision"
  | "create_committee_decision"
  | "create_freeze_action"
  | "create_harness_evidence"
  | "create_waes_gate_result"
  | "create_kwe_work_item"
  | "persist_evidence"
  | "approve_business_write"
  | "promote_lifecycle"
  | "complete_committee_decision";

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewNoWrite {
  writesGfis: 0;
  writesGpc: 0;
  writesErp: 0;
  writesMes: 0;
  writesRoutingQueue: 0;
  writesQueueItem: 0;
  writesApprovalAssignment: 0;
  writesApprovalLock: 0;
  writesApprovalPacket: 0;
  writesApprovalRequest: 0;
  writesApprovalDecision: 0;
  writesCommitteeDecision: 0;
  writesFreezeAction: 0;
  writesWaesGateResult: 0;
  writesKweWorkItem: 0;
  writesHarnessEvidence: 0;
  writesKdsLifecycle: 0;
  writesKdsFact: 0;
  writesKdsAcceptedFact: 0;
  writesExternalApi: 0;
}

export interface GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreview {
  routingQueuePreviewId: string;
  approvalPacketPreviewRefs: string[];
  resolutionOptionPreviewRefs: string[];
  breachReviewPreviewRefs: string[];
  tenantId: string;
  projectId: string;
  surface: GfisAssistantRepairAdmissionReadModelSurface;
  routingQueueType: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewType;
  routingQueueStatus: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewStatus;
  routingQueueDecision: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewDecision;
  routingQueueScope: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewScope;
  routingQueueSlot: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewSlot;
  routingQueuePriority: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewPriority;
  candidateAssigneeRefs: string[];
  requiredEvidenceRefs: string[];
  queueReasonRefs: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewReason[];
  blockedRouteCount: number;
  boundaryRefs: string[];
  sourceApprovalPacketPreviewRefs: string[];
  routingSummaryRef: string;
  lineageHintRefs: string[];
  reasonRefs: string[];
  routingNoteRefs: string[];
  nextStepCandidateRefs: string[];
  blockedActions: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewBlockedAction[];
  createsRoutingQueue: false;
  createsQueueItem: false;
  createsApprovalAssignment: false;
  locksApprover: false;
  createsApprovalPacket: false;
  createsApprovalRequest: false;
  createsApprovalDecision: false;
  createsCommitteeDecision: false;
  createsFreezeAction: false;
  createsHarnessEvidence: false;
  createsWaesGateResult: false;
  createsKweWorkItem: false;
  persistsEvidence: false;
  approvesBusinessWrite: false;
  promotesLifecycle: false;
  completesCommitteeDecision: false;
  noWrite: GfisAssistantRepairNotificationSnoozeQueueApprovalAcknowledgementDigestDeliveryAcknowledgementEscalationSlaBreachReviewResolutionOptionApprovalPacketRoutingQueuePreviewNoWrite;
}
