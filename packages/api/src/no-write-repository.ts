export type NoWriteRepositoryOperation =
  | "read_only"
  | "candidate_request"
  | "gate_check"
  | "work_request"
  | "governance_evidence_request"
  | "ledger_read";

export interface NoWriteRepositoryResult<TPayload> {
  payload: TPayload;
  operation: NoWriteRepositoryOperation;
  noWrite: true;
  connectsDatabase: false;
  callsExternalApi: false;
  writesKds: false;
  writesBusinessSystem: false;
  writesAcceptedLifecycle: false;
}

export interface NoWriteRepository {
  name: string;
  connectsDatabase: false;
  callsExternalApi: false;
  writesKds: false;
  writesBusinessSystem: false;
  writesAcceptedLifecycle: false;
  preview<TPayload>(
    operation: NoWriteRepositoryOperation,
    payload: TPayload,
  ): NoWriteRepositoryResult<TPayload>;
}

export function createNoWriteRepository(name: string): NoWriteRepository {
  return {
    name,
    connectsDatabase: false,
    callsExternalApi: false,
    writesKds: false,
    writesBusinessSystem: false,
    writesAcceptedLifecycle: false,
    preview<TPayload>(
      operation: NoWriteRepositoryOperation,
      payload: TPayload,
    ): NoWriteRepositoryResult<TPayload> {
      return {
        payload,
        operation,
        noWrite: true,
        connectsDatabase: false,
        callsExternalApi: false,
        writesKds: false,
        writesBusinessSystem: false,
        writesAcceptedLifecycle: false,
      };
    },
  };
}
