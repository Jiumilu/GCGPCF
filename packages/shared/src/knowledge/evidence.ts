export type EvidenceKind =
  | "file_hash"
  | "controlled_original"
  | "acceptance_record"
  | "audit_record"
  | "committee_record"
  | "permission_change"
  | "agent_used_knowledge"
  | "publication_approval"
  | "target_system_receipt";

export interface EvidenceRecord {
  id: string;
  tenantId: string;
  evidenceKind: EvidenceKind;
  title: string;
  objectRefs: string[];
  contentHash?: string;
  controlledOriginalRef?: string;
  summary?: string;
  createdBy: string;
  createdAt: string;
  metadata: Record<string, unknown>;
}
