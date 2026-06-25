---
doc_id: GPCF-DOC-2B9E7E6A18
title: Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-TASK-INTAKE-008
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-TASK-INTAKE-008.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-TASK-INTAKE-008.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Loop Round - GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-TASK-INTAKE-008

## run

- 输入：项目群业务执行窗口已授予，用户要求“按建议执行”。
- 范围：GFIS 辽宁远航真实回执 hold register 的真实业务候选 intake。
- 动作：用真实 `codegraph query` / `codegraph node` / `codegraph affected` 结果固化任务开工前门禁，形成可复用的真实业务任务入口。
- 约束：不提交、不推送、不部署、不生产写入、不外部 API 写入、不真实 KDS 写入、不真实 WAES 写入。

## stop

- stop_type：`implementation_blocked_pending_real_receipts`
- 停止证据：GFIS runtime SOP 仍因 `KDS coverage must not have missing controlled sources` 失败；当前只能记录 task intake，不能宣称业务已完成。
- 状态上限：`partial`

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_task_intake_gate.py --task-file docs/harness/evidence/codegraph-dev-execution-business-task-intake-008.json
python3 /Users/lujunxiang/Projects/GlobalCloud\ V0.0.1/GlobalCloud\ GFIS/scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py
python3 /Users/lujunxiang/Projects/GlobalCloud\ V0.0.1/GlobalCloud\ GFIS/scripts/validate_gfis_runtime_sop_e2e.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-EXECUTION-WINDOW-GRANT-007`
- 可重试动作：收到真实回执文件、客户确认函、签章完成件或等效正式确认原件后，重新进入 implementation。
- 不可重试动作：未授权 commit、push、deploy、production write、external API write、real KDS write、real WAES write。

## debug

- 当前阻塞：GFIS runtime SOP 的真实 KDS coverage 缺口仍未闭合。
- 本轮只把真实业务候选正式纳入 task intake，并保留 CodeGraph 前置分析、fallback tests 和受控实现边界。
- 下一轮：`GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008`

## 输出

- `docs/harness/evidence/codegraph-dev-execution-business-task-intake-008.json`
- `docs/harness/evidence/codegraph-dev-execution-business-task-intake-008.md`
