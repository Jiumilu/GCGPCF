import type { ConfirmationStatus, RagAdmission, TrustLevel } from "./object";

export type RagCitationStrength = "L0" | "L1" | "L2" | "L3" | "L4" | "L5";

export interface RagCitationStrengthRule {
  level: RagCitationStrength;
  canRetrieve: boolean;
  canDisplaySummary: boolean;
  canAnswer: boolean;
  canStrongReference: boolean;
  canBusinessAssist: boolean;
}

export interface RagCitationStrengthMapping {
  ragAdmission: RagAdmission;
  allowedStrengths: RagCitationStrength[];
}

export interface RagL5Condition {
  ragAdmission: "safe";
  trustLevels: Extract<TrustLevel, "T0" | "T1">[];
  confirmationStatus: Extract<ConfirmationStatus, "human_confirmed" | "committee_confirmed">[];
  evidenceRequired: true;
}

export interface RagCitationStrengthPolicy {
  policyId: string;
  version: string;
  levels: RagCitationStrengthRule[];
  ragAdmissionMapping: RagCitationStrengthMapping[];
  l5Conditions: RagL5Condition;
  hardBoundaries: {
    l5DoesNotAutoWriteback: boolean;
    l5DoesNotAutoConfirmRevenue: boolean;
    l5DoesNotReplaceCommitteeDecision: boolean;
    sensitiveRequiresMetadataOrRedaction: boolean;
    limitedRequiresBoundaryNotice: boolean;
    repairRequiredMustNotBeConclusion: boolean;
  };
  noWriteAssertions: {
    writesKdsFact: 0;
    writesWaesGateResult: 0;
    writesBusinessSystem: 0;
    writesRevenueDistribution: 0;
    writesExternalApi: 0;
  };
}
