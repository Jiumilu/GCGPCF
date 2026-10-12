import type {
  FreezeRequest,
  RunWameGatesRequest,
  WameCheckRequest,
} from "./contracts";
import { WAME_ENDPOINTS } from "./routes";
import { wameRepository } from "./repository";

export const wameService = {
  endpoints: WAME_ENDPOINTS,
  repository: wameRepository,
  runGates(request: RunWameGatesRequest) {
    return wameRepository.preview("gate_check", request);
  },
  runWameGates(request: RunWameGatesRequest) {
    return wameRepository.preview("gate_check", request);
  },
  check(request: WameCheckRequest) {
    return wameRepository.preview("gate_check", request);
  },
  checkRagAdmission(request: WameCheckRequest) {
    return wameRepository.preview("gate_check", request);
  },
  checkWriteback(request: WameCheckRequest) {
    return wameRepository.preview("gate_check", request);
  },
  checkRevenue(request: WameCheckRequest) {
    return wameRepository.preview("gate_check", request);
  },
  checkContribution(request: WameCheckRequest) {
    return wameRepository.preview("gate_check", request);
  },
  checkExternalShare(request: WameCheckRequest) {
    return wameRepository.preview("gate_check", request);
  },
  requestFreeze(request: FreezeRequest) {
    return wameRepository.preview("gate_check", request);
  },
};
