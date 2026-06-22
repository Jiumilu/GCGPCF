---
doc_id: GPCF-DOC-FIVE-DIRECTION-FULL-SUMMARY-001
title: LOOP 运行控制闭环全量总结 20260622
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-five-direction-full-summary-20260622.md
source_path: docs/harness/evidence/loop-five-direction-full-summary-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP 运行控制闭环全量总结 20260622

## 结论

LOOP 运行控制闭环能力已经从一次性试运行，升级为 GPCF LOOP 的常驻工程控制能力。历史名称 `LOOP 五方向` 保留为别名，用于兼容既有文件名、validator 和 evidence 链。

当前状态应记为：

```text
completed_control_plane_and_self_evolution_adopted
```

不得记为：

```text
accepted
integrated
production_ready
```

## 背景

用户要求分析文章后，判断项目群治理 LOOP 工程体系是否可借鉴，并进一步要求新加入能力不仅能在单轮运行，还要能作用于其它所有 LOOP 工作。随后进行了以下推进：

1. 建立 LOOP 五方向工程结构。
2. 启动 `GPCF-LOOP-FIVE-DIRECTION-RUN-001` no-write L3 试运行。
3. 将五方向能力接入 Orchestrator、Autonomy Policy、Control Board、模板和 validator。
4. 用非 RUN-001 工作项 `GFIS-runtime-gap-resolution-plan` 做 standing smoke test。
5. 建立 `GPCF-LOOP-FIVE-DIRECTION-SELF-EVOLUTION-001`，把运行经验转成后续默认约束。

## 新能力定义

旧微循环：

```text
输入 -> 动作 -> 输出 -> 检查 -> 反馈
```

LOOP 运行控制闭环：

```text
run -> stop -> verify -> recover -> debug
```

旧微循环仍可作为内部说明，但不得替代五方向结构。

## 运行控制闭环职责

| 方向 | 职责 | 关键价值 |
|---|---|---|
| `run` | 记录输入、目标、范围、动作、输出和下一轮候选 | 避免只描述动作、不说明边界 |
| `stop` | 记录停止类型、停止证据和状态升级许可 | 防止把单轮完成误当作合法停止 |
| `verify` | 记录前置检查、中间检查、最终门禁和三条 lane 状态 | 区分 test、synthetic、real business |
| `recover` | 记录最后安全状态、可重试动作、不可重试动作、所需输入和恢复轮次 | 让失败后可恢复、可续跑 |
| `debug` | 记录失败门禁、状态天花板、真实 lane 计数、写入计数和下一授权 | 让问题定位结构化 |

## 已落地产物

### 常驻规则

| 层 | 路径 | 作用 |
|---|---|---|
| Orchestrator | `.codex/skills/globalcloud-loop-orchestrator/SKILL.md` | 要求所有非只读 LOOP 工作登记五方向 |
| Policy | `02-governance/loop/LOOP_AUTONOMY_POLICY.md` | 定义五方向常驻接入规则，覆盖 L1、L2、L3、L3.5、L4、L5 |
| Control Board | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 记录五方向能力为 `active / all Loop work` |
| Template | `templates/loop-round-v2-five-direction.yaml` | 声明 `mandatory_for: [L1, L2, L3, L3.5, L4, L5]` |
| Base Validator | `tools/kds-sync/validate_loop_engineering_five_direction_implementation.py` | 检查常驻接入点和自我进化事件 |

### 试运行与验证

| 证据 | 路径 | 结论 |
|---|---|---|
| RUN-001 轮次 | `docs/harness/loops/loop-round-GPCF-LOOP-FIVE-DIRECTION-RUN-001.md` | 五方向 no-write L3 首轮已完成 |
| RUN-001 JSON | `docs/harness/evidence/loop-five-direction-run-001-20260622.json` | `started=true`、`completed_for_round=true`、`stop_type=authorization_boundary` |
| RUN-001 Evidence | `docs/harness/evidence/loop-five-direction-run-001-20260622.md` | 记录 RUN-001 运行证据 |
| RUN-001 Validator | `tools/kds-sync/validate_loop_five_direction_run_001.py` | `validate_loop_five_direction_run_001=pass` |
| Standing Smoke Round | `docs/harness/loops/loop-round-GPCF-LOOP-FIVE-DIRECTION-STANDING-SMOKE-001.md` | 证明非 RUN-001 工作也能采用五方向 |
| Standing Smoke JSON | `docs/harness/evidence/loop-five-direction-standing-smoke-20260622.json` | 目标为 `GFIS-runtime-gap-resolution-plan` |
| Standing Smoke Evidence | `docs/harness/evidence/loop-five-direction-standing-smoke-20260622.md` | `five_direction_standing_smoke=pass` |
| Standing Smoke Validator | `tools/kds-sync/validate_loop_five_direction_standing_smoke.py` | `run/stop/verify/recover/debug` 全部通过 |
| Self Evolution JSON | `docs/harness/evidence/loop-five-direction-self-evolution-20260622.json` | `status=adopted_as_default_loop_constraint` |
| Self Evolution Evidence | `docs/harness/evidence/loop-five-direction-self-evolution-20260622.md` | 运行经验已转成规则、模板和门禁 |
| Self Evolution Validator | `tools/kds-sync/validate_loop_five_direction_self_evolution.py` | `loop_five_direction_self_evolution=pass` |

## 已验证输出

```text
validate_loop_five_direction_run_001=pass
five_direction_standing_smoke=pass
loop_five_direction_self_evolution=pass
loop_engineering_five_direction_implementation=pass
document_pollution=pass
kds_token=pass fingerprint=bfd9553d
loop_document_gate.py --check-only => gate: pass
```

## 相对旧微循环的提升

| 维度 | 旧微循环 | 新五方向 LOOP |
|---|---|---|
| 运行 | 说明做了什么 | 说明输入、目标、范围、动作、输出和下一轮 |
| 停止 | 容易把阶段性完成当停止 | 必须记录 `stop_type` 和 `stop_evidence` |
| 验证 | 单一检查口径 | 区分 precheck、intermediate check、final gate 和三条 lane |
| 恢复 | 通常只有下一步建议 | 有 `last_safe_state`、`retryable_actions`、`required_inputs` |
| 调试 | 问题散落在叙述中 | 集中记录 failing gate、status ceiling、lane counts、write counts |
| 状态诚实度 | 依赖人工不误判 | 通过 validator 保持 `accepted=false`、`integrated=false`、`production_ready=false` |
| 跨项目复用 | 格式容易漂移 | 模板、政策、控制板、Orchestrator 和 validator 共同约束 |

## 长期约束

所有非只读 LOOP 轮次必须包含：

```text
run
stop
verify
recover
debug
```

未登记 LOOP 运行控制闭环的 LOOP 轮次：

1. 状态最高只能为 `partial`。
2. 不得作为 `accepted` 升级证据。
3. 不得作为 `integrated` 升级证据。
4. 不得作为 `production_ready` 升级证据。

## 当前边界

| 字段 | 当前值 |
|---|---|
| status | `completed_control_plane_and_self_evolution_adopted` |
| status_ceiling | `partial_repair` |
| real_business_lane | `repair_required` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| production_writes | `0` |
| real_external_api_writes | `0` |
| kds_fact_writes | `0` |
| waes_gate_result_writes | `0` |

## 后续运行要求

后续任何 GPCF LOOP 工作若不是纯只读问答，应直接使用五方向结构。

若继续推进 GFIS、WAES、KDS、Headroom、WAS、Studio 或其它项目群任务，应优先检查：

1. 是否有独立输入。
2. 是否有明确 stop_type。
3. 是否区分 test/synthetic/real business lane。
4. 是否保留 last_safe_state。
5. 是否记录 failing_gate、status_ceiling 和 write_counts。
6. 是否仍保持 no-write 或已取得明确更高授权。

## 自我提升结论

本次工作已经完成自我提升闭环：

```text
一次运行经验
-> 发现常驻接入缺口
-> 修改 Orchestrator / Policy / Control Board / Template / Validator
-> 使用非原始任务 smoke test
-> 建立 self-evolution evidence
-> 形成后续 LOOP 默认约束
```

该闭环可作为后续类似能力引入的标准方式。
