---
doc_id: GPCF-DOC-4BA3D31617
title: Loop Engineering 五方向实施规范
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md
source_path: 02-governance/loop/LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Engineering 五方向实施规范

本文把 Loop Engineering 的五个方向落成 GPCF 项目群可执行控制面：运行、停止、验证、恢复、调试。它补充现有 `LOOP_CONTROL_BOARD.md` 和 `LOOP_AUTONOMY_POLICY.md`，不替代 KDS、WAES、Harness 或 GFIS 的既有职责。

## 0. 边界

本规范只定义治理控制面和证据格式，不创建真实业务事实，不写入生产系统，不提升 `accepted`、`integrated` 或 `production_ready`。

现有项目群事实边界保持不变：

| 层 | 职责 | 禁止替代 |
|---|---|---|
| KDS | 受控知识事实主存与镜像 | 不替代 GFIS 运行层事实 |
| WAES | 授权、风险、门禁和裁决 | 不替代业务主账或人工裁决 |
| Harness | 执行、证据、回放、指标和验收准备 | 不替代原始凭证 |
| Loop | 微循环、中循环和大循环编排 | 不直接证明业务完成 |
| GFIS | 工厂运行层事实与 SOP E2E 主体 | 不被 Demo、fixture 或文档通过替代 |

## 1. Loop 如何运行

每轮 Loop 必须记录一个五段式运行轨迹：

| 字段 | 要求 |
|---|---|
| input | 输入文档、缺口、目标、授权边界 |
| decision | 本轮判断、取舍、风险、状态上限 |
| action | 本轮实际动作、工具、文件和 no-write 边界 |
| output | 本轮产物、证据、validator 输出和未完成项 |
| next | 下一轮目标、阻塞项、授权需求 |

对应模板：`templates/loop-round-v2-five-direction.yaml`。

## 2. Loop 如何停止

停止必须由 `stop_detector` 判定，不能由阶段性汇报、单轮完成、批量生成文件或局部 validator 通过自动触发。

| 停止类型 | 可用条件 | 状态上限 |
|---|---|---|
| completed_for_round | 本轮目标完成且无 P0/P1 未归属动作 | `evidence_ready` |
| authorization_boundary | 下一步需要用户、真实接口、生产或跨仓授权 | `partial` |
| repair_required | 验证器证明真实链路仍缺 source-of-record 或运行层证据 | `repair_required` |
| task_queue_empty | 队列为空且候选下一步需确认 | `partial` |
| production_safety | 触及生产写入、部署、密钥、外部 API 或 accepted/integrated | `blocked` |

`accepted`、`integrated`、`production_ready` 只能由独立的完成检测器放行，且必须同时满足真实 source-of-record、runtime primary key、review queue、runtime intake、WAES review、verified artifact、人工确认和回放证据。

## 3. Loop 如何验证

每轮必须分三段验证：

| 阶段 | 验证点 | 最低证据 |
|---|---|---|
| precheck | 输入、授权、污染、状态上限 | 文档门禁或专项 validator |
| intermediate_check | 中间产物、写入边界、弱证据拒收 | fixture / dry-run / no-write validator |
| final_gate | 轮次结论、下一步、停止类型、状态上限 | evidence JSON + 受控 Markdown |

验证必须显式区分 `test_data_lane`、`synthetic_dev_lane` 和 `real_business_lane`。测试数据通过不得释放真实运行层主键、review queue、runtime intake、WAES review、verified artifact 或生产写入。

## 4. Loop 如何恢复

每个失败或授权边界轮次必须产生 `recovery_checkpoint`：

| 字段 | 含义 |
|---|---|
| failed_or_stopped_at | 失败或停止位置 |
| last_safe_state | 最后可回放的安全状态 |
| retryable_actions | 可重试动作 |
| non_retryable_actions | 未授权或不可重试动作 |
| required_inputs | 继续所需真实输入、授权或证据 |
| resume_round | 推荐下一轮 Round ID |

恢复检查点不得把缺失证据改写成完成状态；它只说明如何从当前安全状态继续。

## 5. Loop 如何调试

调试视图必须把长控制板压缩成可扫描信号：

| 信号 | 当前要求 |
|---|---|
| recent_state_changes | 最近状态变化和来源文件 |
| failing_gate | 当前阻塞门禁 |
| status_ceiling | 当前最高允许状态 |
| real_lane_counts | 真实业务计数 |
| synthetic_lane_counts | 测试/开发计数 |
| write_counts | 生产、外部 API、KDS/WAES 写入计数 |
| next_authorization | 下一步授权需求 |

对应证据：`docs/harness/evidence/loop-engineering-five-direction-implementation-20260622.{json,md}`。

## 6. 完成检测

本规范落地完成必须同时满足：

| 要求 | 证明 |
|---|---|
| 五方向规范存在 | 本文档受控并纳入 KDS 本地镜像 |
| 运行模板存在 | `templates/loop-round-v2-five-direction.yaml` |
| 当前态 fixture 存在 | `fixtures/loop-dashboard/loop-engineering-five-direction-implementation.json` |
| 证据摘要存在 | `docs/harness/evidence/loop-engineering-five-direction-implementation-20260622.md` |
| validator 通过 | `python3 tools/kds-sync/validate_loop_engineering_five_direction_implementation.py` |
| 文档治理执行 | scoped `document_control.py` 已登记并镜像新增 Markdown；污染检查、KDS TOKEN 检查和五方向 validator 通过 |
| 全局债务保留 | `loop_document_gate.py --check-only` 仍可能因既有中文本地化债务返回 `rework_required`；该结果不得被本文档改写为 pass |

## 7. 当前状态上限

本规范只提升 Loop 工程控制面的可读性、可恢复性和可调试性。GFIS 真实业务 lane 仍保持 `repair_required`；项目群不得因本文档或 validator 通过而升级 `accepted`、`integrated` 或 `production_ready`。
