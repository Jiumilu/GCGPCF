import type { RagAdmission } from "./object";
import type { WaesGateStatus } from "./waes-gate";

export type SensitiveDataClass =
  | "contract_sensitive_terms"
  | "finance_voucher"
  | "pod_original"
  | "quality_dispute"
  | "customer_supplier_identity"
  | "credential_or_token"
  | "unpublished_policy_interpretation"
  | "commercial_quote_or_commission";

export type SensitiveStorageMode =
  | "metadata_only"
  | "redacted_copy"
  | "controlled_original"
  | "blocked";

export interface SensitiveMetadataRecord {
  objectId: string;
  tenantId: string;
  sensitiveClass: SensitiveDataClass;
  storageMode: SensitiveStorageMode;
  sourceRef: string;
  evidenceRef: string;
  hashOrOriginalPointer: string;
  controlledOriginalRef: string;
  aclRef: string;
  citationScope: string;
  ragAdmission: Extract<RagAdmission, "sensitive_metadata_only" | "blocked" | "limited">;
  sensitiveDataGateResult: Extract<WaesGateStatus, "metadata_only" | "blocked" | "redaction_required">;
  summary: string;
  rawContentStored: false;
}

export interface SensitiveMetadataStoragePolicy {
  policyId: string;
  version: string;
  sensitiveClasses: SensitiveDataClass[];
  storageModes: SensitiveStorageMode[];
  minimumMetadataFields: string[];
  controlledOriginalPointerRules: {
    noSecretValues: boolean;
    authorizedControlledSpaceOnly: boolean;
    hashOrIrreversibleDigestRequired: boolean;
    aclRequired: boolean;
    citationScopeRequired: boolean;
    evidenceRefRequired: boolean;
    gateResultRequired: boolean;
  };
  hardBoundaries: {
    metadataOnlyRawContentAllowed: false;
    controlledOriginalRawContentAllowedInKds: false;
    credentialOrTokenDefaultBlockedOrMetadataOnly: boolean;
    defaultRagAdmissionForSensitive: Extract<RagAdmission, "sensitive_metadata_only">;
    externalShareRequiresRedactionAclAndGate: boolean;
    rawOriginalStaysInControlledSpace: boolean;
  };
  noWriteAssertions: {
    writesRawContentToKds: 0;
    writesSecretToDocs: 0;
    writesSecretToEvidence: 0;
    writesExternalApi: 0;
  };
}
