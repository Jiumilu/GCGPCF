export interface LoopRecord {
  id: string;
  tenantId: string;
  loopName: string;
  projectId?: string;
  goal: string;
  inputRefs: string[];
  newObjectRefs: string[];
  newGapRefs: string[];
  candidateFactRefs: string[];
  candidateSopRefs: string[];
  waesResultRefs: string[];
  confirmationRefs: string[];
  committeeRefs: string[];
  risks: Array<Record<string, unknown>>;
  nextActions: Array<Record<string, unknown>>;
  createdBy: string;
  createdAt: string;
}
