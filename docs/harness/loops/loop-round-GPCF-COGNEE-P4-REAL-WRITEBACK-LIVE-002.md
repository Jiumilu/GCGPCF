---
doc_id: GPCF-DOC-LOOP-COGNEE-P4-REAL-WRITEBACK-LIVE-002
title: Loop Round - GPCF Cognee P4 真实写入生产写入前授权签核 002
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-002.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-002.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee P4 真实写入生产写入前授权签核 002

## 输入

- `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001.md`
- `docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md`
- `docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- `loop/context/cognee/policy.yaml`

## run

- 复核 live-演练结果：`cognee_p4_real_writeback_live_output=pass`、`record_count=5`、`requested_write_count=5`、`execution_count=5`、`pilot_gate_pass=True` 已保持，`production_write_count=5` 标识处于演练口径。
- 准备 Owner/WAES 联署签核文本，明确：
  - Owner 签字与授权来源（含 `owner_token_source`）；
  - WAES 决策与运行时依赖确认；
  - 回滚计划与失败退出条件；
  - 数据范围、授权有效期与失效策略。
- 生成签核包证据 `docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md`（待签字段由人工录入，不得代填）。
- 维护机读签核实例 `fixtures/cognee/cognee-p4-live-authorization-signoff.pending.json`，后续人工签核信息先写该文件，再同步 Markdown。
- 仍不执行真实外部系统写入；脚本仅用于受控证据复核口径。
- 固定签核收口校验：
```bash
python3 tools/kds-sync/sync_cognee_p4_live_authorization_signoff.py

python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py
```

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮为生产切换前的人审签核边界，缺少双签确认前不推进 live 生产执行。
- 当前状态：`accepted=false`，`integrated=false`，`production_ready=false`，`production_write=false`。

## verify

- 生产切换前验收要求：
  - `cognee_p4_real_writeback_live_output=pass`
  - `record_count=5`
  - `requested_write_count=5`
  - `execution_count=5`
  - `pilot_gate_pass=true`
  - `live_execution_ready_rate=1.0`
- 签核通过前置要求：
  - `owner_token_source` 可追溯；
  - `waes_decision=pass` 与 `runtime_dependency_ok=true`；
  - `rollback_plan_verified=true` 与回滚窗口记录完整；
  - `authorization_token_source_coverage=1.0`。
- 签核收口命令：
```bash
python3 tools/kds-sync/sync_cognee_p4_live_authorization_signoff.py

python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py \
  --require-complete-signoff
```
- 固定执行命令清单（签核完成后才允许进入）：
```bash
python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json

python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --allow-live-write

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json
```

## 反馈

- 当前输出仍是演练口径，未形成生产授权许可；
- 下一步动作为：完成 Owner/WAES 签字补齐后，输出 `GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-002` 的签核结论并驱动下轮生产执行决策文档。
- 文档门禁保持：未完成双签前，`production_write`、`accepted`、`integrated`、`production_ready` 不得提升为 `true`。
- 数据同步门禁保持：Markdown 与 `cognee-p4-live-authorization-signoff.pending.json` 必须一致，否则签核校验失败。

## recover

- 若签核到期或签字信息与脚本输出冲突：返回 `GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004` 重新确认授权链路后再提交至本轮。
- 若发现 live 演练证据参数发生变化：返回 `GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001` 重跑演练。

## debug

- 当前唯一阻断：Owner 与 WAES 双签文本待齐备。
- 一旦签核材料齐全且不再退签，可直接进入外部执行边界验证分支。
