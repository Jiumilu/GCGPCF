import type {
  FreezeRequest,
  RunWaesGatesRequest,
  WaesCheckRequest,
} from "./contracts";
import { WAES_ENDPOINTS } from "./routes";
import { waesRepository } from "./repository";

export const waesService = {
  endpoints: WAES_ENDPOINTS,
  repository: waesRepository,
  runGates(request: RunWaesGatesRequest) {
    return waesRepository.preview("gate_check", request);
  },
  runWaesGates(request: RunWaesGatesRequest) {
    return waesRepository.preview("gate_check", request);
  },
  check(request: WaesCheckRequest) {
    return waesRepository.preview("gate_check", request);
  },
  checkRagAdmission(request: WaesCheckRequest) {
    return waesRepository.preview("gate_check", request);
  },
  checkWriteback(request: WaesCheckRequest) {
    return waesRepository.preview("gate_check", request);
  },
  checkRevenue(request: WaesCheckRequest) {
    return waesRepository.preview("gate_check", request);
  },
  checkContribution(request: WaesCheckRequest) {
    return waesRepository.preview("gate_check", request);
  },
  checkExternalShare(request: WaesCheckRequest) {
    return waesRepository.preview("gate_check", request);
  },
  requestFreeze(request: FreezeRequest) {
    return waesRepository.preview("gate_check", request);
  },
};
