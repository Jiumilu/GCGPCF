---
doc_id: GPCF-DOC-LOOP-COGNEE-P4-REAL-WRITEBACK-LIVE-001
title: Loop Round - GPCF Cognee P4 真实写入运行演练 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee P4 真实写入运行演练 001

## 输入

- `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004.md`
- `docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- `loop/context/cognee/policy.yaml`

## run

- 预期执行：先进行演练模式 run（默认 dry-run），不触发生产 API；审批通过后按需重跑 `--allow-live-write`。
- 先确认本轮输入、授权材料与监控回收机制齐全后执行以下命令。

```bash
python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --dry-run-output-only

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json

python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --allow-live-write

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json
```

## 输出

- `docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json`
- 本轮运行验证结果日志（dry-run 或授权通过后的 live 模式）
- `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001.md`（执行边界与复核更新）

## stop

- 停止类型：`implementation_boundary`
- 停止原因：预检链路已具备脚本运行条件，但生产级 live 写入仍需 owner 与 WAES 双签确认，当前保持 dry-run 演练边界。
- 当前状态：`accepted=false`，`integrated=false`，`production_ready=false`。

## verify

- 复测目标：
  - `cognee_p4_real_writeback_live_output=pass`
  - `record_count=5`
  - `requested_write_count=5`
  - `execution_count=0`（dry-run 模式）
  - `execution_count=5`（`--allow-live-write` 演练口径）
- 复测命令：
```bash
python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --dry-run-output-only

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

- 已补充 `--allow-live-write` 跑一版：
  - `cognee_p4_real_writeback_live_output=pass`
  - `record_count=5`
  - `requested_write_count=5`
  - `execution_count=5`
  - `production_write_count=5`
  - `pilot_gate_pass=True`
- 当前链路说明：`--allow-live-write` 已覆盖演练口径标记（`execution_status=executed`），但脚本当前为本地证据生成器，未包含真实外部系统落库/写入调用。
- 真实生产执行口径（仅在双签通过后，且接入执行层后）：

```bash
python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --allow-live-write
```

## recover

- 若审批材料过期或签署失败：回到 `GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004` 重新提交。

## debug

- 关键阻断：脚本层已就绪，当前闭环关键点在执行授权（Owner/WAES 双签）与 live-write 审批，未完成前不得进入生产执行。
