import type { ConfirmationStatus } from "./object";
import type { TargetSystem } from "./fact-candidate";
import type { WameGateStatus } from "./wame-gate";

export type GfisWritebackMode =
  | "no_write"
  | "sandbox"
  | "approved_write"
  | "production_write";

export type GfisWritebackFinalAction =
  | "pending"
  | "accepted"
  | "rejected"
  | "returned"
  | "rolled_back";

export interface GfisWritebackSandboxRecord {
  candidateId: string;
  sourceFactId: string;
  targetSystem: TargetSystem;
  targetModule: string;
  targetField: string;
  currentValue: unknown;
  proposedValue: unknown;
  diffReason: string;
  evidenceRefs: string[];
  wameResult: WameGateStatus;
  businessOwner: string;
  confirmationStatus: ConfirmationStatus;
  writebackMode: GfisWritebackMode;
  finalAction: GfisWritebackFinalAction;
  noWrite: true;
}

export interface GfisWritebackSandboxPolicy {
  policyId: string;
  version: string;
  writebackModes: GfisWritebackMode[];
  allowedBeforeP1: Extract<GfisWritebackMode, "no_write" | "sandbox">[];
  blockedBeforeP1: Extract<GfisWritebackMode, "approved_write" | "production_write">[];
  finalActions: GfisWritebackFinalAction[];
  minimumFields: string[];
  approvedWriteRequires: string[];
  productionWriteRequires: string[];
  hardBoundaries: {
    aiAllowedModes: Extract<GfisWritebackMode, "no_write" | "sandbox">[];
    aiBlockedModes: Extract<GfisWritebackMode, "approved_write" | "production_write">[];
    noWriteCannotEmitTargetReceipt: boolean;
    sandboxCannotEmitTargetReceipt: boolean;
    finalActionAcceptedIsNotWritebackReceipt: boolean;
    missingEvidenceBlocks: boolean;
    missingWameResultBlocks: boolean;
    missingBusinessOwnerBlocks: boolean;
  };
  noWriteAssertions: {
    writesGfis: 0;
    writesGpc: 0;
    writesErp: 0;
    writesMes: 0;
    writesExternalApi: 0;
  };
}
