---
doc_id: GPCF-DOC-MMC-INTAKE-REG-LOOP-20261014
title: Loop Round GPCF MMC Intake Registration 001
project: GPCF
related_projects: [GPC, WAME, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-MMC-INTAKE-REG-001.md
source_path: docs/harness/loops/loop-round-GPCF-MMC-INTAKE-REG-001.md
sync_direction: bidirectional
last_reviewed: 2026-10-14
supersedes: []
superseded_by: []
---

# Loop Round GPCF MMC Intake Registration 001

## 输入

- 老卢「继续」授权（2026-10-14）：推进 MMC·M2 扩展——受理器接入（P1）。
- 前置件：MMC `docs/planning/m2-d2.1-extension-candidates_v0.1.md`（受理器=P1 候选·登记顺序与纪律）。
- 现场事实：受理器 :3210 在跑（`GET /health` → 200）；只读端点面自 `intake_server.py` 源码核读。

## 动作

- 建 `docs/harness/MMC/evidence/mmc-intake-readonly-capability-registration-request-20261014.json` / `.md`（request 包）。
- 登记范围＝6 条只读能力（candidate 态请求）；写面明示排除（governor 保护端点不接）。
- 保证：不改受理器、不改 WAES 仓；`current_decision` 留 `pending_governance_review`。

## 输出

- `docs/harness/MMC/evidence/mmc-intake-readonly-capability-registration-request-20261014.md`
- `docs/harness/MMC/evidence/mmc-intake-readonly-capability-registration-request-20261014.json`
- `tools/kds-sync/validate_mmc_intake_readonly_capability_registration.py`

## 检查

- `python3 tools/kds-sync/validate_mmc_intake_readonly_capability_registration.py`
- `python3 tools/kds-sync/document_control.py`（scoped：DOCUMENT_CONTROL_SCOPE）

## 反馈

- 请求包已提交（submitted=true）；`registry_entry_added=false`、`governance_reviewed=false`、`wame_authorized=false`、`accepted=false`。
- 待治理方裁定后：更新 json＋md＋validator（accepted 分支）并推进 next_step（catalog 登记 6 能力）。

## 下一轮

- 裁定「accepted」→ MMC catalog 增 `intake_mcp?—否—intake_rest` 连接器条目（6 只读能力·candidate）＋validator 复跑。
- 裁定「rejected/requires_rework」→ 按 findings 修订后重提。
