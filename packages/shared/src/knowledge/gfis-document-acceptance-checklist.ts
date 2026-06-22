import type { RagAdmission } from "./object";
import type { WaesGateStatus, WaesGateType } from "./waes-gate";

export type GfisDocumentPackageType =
  | "construction_package"
  | "order_package"
  | "quality_package"
  | "delivery_pod_package"
  | "finance_package"
  | "oem_transition_package";

export type GfisDocumentChecklistItem =
  | "source_registered"
  | "evidence_bound"
  | "pool_refs_present"
  | "domain_scope_present"
  | "trust_level_assigned"
  | "rag_admission_assessed"
  | "sensitive_handling_assessed"
  | "waes_gate_suggested"
  | "kwe_workpack_suggested"
  | "writeback_candidate_only";

export type GfisDocumentAcceptanceBatchResult =
  | "candidate_ready"
  | "repair_required"
  | "human_required"
  | "committee_required"
  | "metadata_only"
  | "blocked";

export type GfisDocumentSensitiveHandling =
  | "none"
  | "redaction_required"
  | "metadata_only"
  | "controlled_original";

export interface GfisDocumentAcceptanceChecklistRecord {
  id: string;
  tenantId: string;
  projectId: string;
  packageType: GfisDocumentPackageType;
  sourceObjectId: string;
  checklistItems: Record<GfisDocumentChecklistItem, boolean>;
  poolRefs: string[];
  sourceRefs: string[];
  evidenceRefs: string[];
  gapRefs: string[];
  factCandidateRefs: string[];
  writebackCandidateRefs: string[];
  waesGateSuggestions: Array<{
    gateType: WaesGateType;
    gateStatus: WaesGateStatus;
  }>;
  ragAdmission: RagAdmission;
  sensitiveHandling: GfisDocumentSensitiveHandling;
  containsRawContent: boolean;
  requiresHumanConfirmation: boolean;
  requiresCommittee: boolean;
  kweWorkpackSuggestionRefs: string[];
  batchResult: GfisDocumentAcceptanceBatchResult;
  noWrite: true;
}

export interface GfisDocumentAcceptanceChecklistPolicy {
  policyId: "okf.gfis_document_acceptance_checklist_policy";
  version: string;
  packageTypes: GfisDocumentPackageType[];
  requiredCheckItems: GfisDocumentChecklistItem[];
  batchResults: GfisDocumentAcceptanceBatchResult[];
  sensitiveDefaults: Partial<Record<GfisDocumentPackageType, GfisDocumentSensitiveHandling>>;
  hardBoundaries: {
    checklistPassIsNotFormalAcceptance: boolean;
    batchPassIsNotGfisWriteback: boolean;
    t5AiOnlyCannotStrongReference: boolean;
    sensitivePackageCannotExposeRawContent: boolean;
    gapsRequireGapOrWorkpackSuggestion: boolean;
    committeeRequiredCannotBeHumanOnlyReleased: boolean;
  };
  noWriteGuards: {
    writesGfis: 0;
    writesGpc: 0;
    writesErp: 0;
    writesMes: 0;
    writesKdsFact: 0;
    writesWaesGateResult: 0;
    writesKweWorkItem: 0;
    writesRevenueOrScoreConfirmation: 0;
    writesExternalApi: 0;
  };
}
