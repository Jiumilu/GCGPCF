import type { TrustLevel } from "./object";

export type SourceKind =
  | "business_system_record"
  | "contract"
  | "cash_receipt"
  | "policy_site"
  | "standard_site"
  | "partner_document"
  | "meeting_note"
  | "email"
  | "feishu"
  | "wiki"
  | "web_article"
  | "llm_output";

export interface SourceRecord {
  id: string;
  tenantId: string;
  sourceKind: SourceKind;
  trustLevel: TrustLevel;
  title: string;
  sourceUri?: string;
  externalRef?: string;
  collectedBy: string;
  collectedAt: string;
  versionLabel?: string;
  applicableScope?: string[];
  metadata: Record<string, unknown>;
}
