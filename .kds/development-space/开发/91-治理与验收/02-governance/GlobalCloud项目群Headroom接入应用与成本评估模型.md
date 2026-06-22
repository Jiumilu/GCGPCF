---
doc_id: GPCF-DOC-2BBAE6E546
title: GlobalCloud 项目群 Headroom 接入应用与成本评估模型
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群Headroom接入应用与成本评估模型.md
source_path: 02-governance/GlobalCloud项目群Headroom接入应用与成本评估模型.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Headroom 接入应用与成本评估模型

日期：2026-06-21
状态：L1 治理准入与成本模型 v1

## 1. 目标

本文件定义 `chopratejas/headroom` 在 GlobalCloud 项目群中的接入方式、应用边界、Loop 工程纳入方式和成本评估模型。

目标不是把 Headroom 直接升级为业务项目，也不是让它替代 KDS、Brain 或 WAES，而是把它作为 AI 上下文压缩、RAG 片段压缩、工具输出压缩和成本观测候选能力，纳入 GPCF 总控治理。

## 2. 当前准入结论

| 字段 | 当前值 |
|---|---|
| 纳入状态 | `admission_and_cost_model_defined` |
| 项目群角色 | `ai_context_compression_infrastructure_candidate` |
| 允许等级 | L1 文档治理与 L2 本地 dry-run/validator |
| 禁止等级 | 未授权前不得进入 L3.5/L4/L5 真实接口、生产代理、跨项目 memory 或自动写回 |
| 业务状态 | 不等于 accepted、integrated、production_ready |
| 数据主权 | KDS 仍为知识 source of record；Brain 仍为知识引擎；WAES 仍为治理和裁决门禁 |

## 3. 项目群应用范围

| 项目/域 | 首轮接入用途 | 禁止事项 | 成本观测字段 |
|---|---|---|---|
| GPCF | 压缩 Loop 日志、门禁输出、项目群状态矩阵摘要 | 不压缩受控原文作为唯一证据 | `loop_gate_tokens_before/after` |
| KDS | 压缩开发空间检索结果和非敏 metadata-only chunk | 不写真实 KDS Token，不替代 KDS 原文 | `rag_chunk_tokens_before/after` |
| Brain | 压缩 RAG 候选和引用回指候选 | 不吞掉 citation、source_path、doc_id | `retrieval_context_tokens_before/after` |
| WAES | 压缩状态审计输入和 evidence 摘要 | 不改变门禁判定，不生成裁决事实 | `audit_context_tokens_before/after` |
| GFIS | 压缩 dry-run 日志和测试数据门禁输出 | 不压缩真实客户原件、合同、POD 原文入模型 | `runtime_log_tokens_before/after` |
| GPC | 压缩协同链路 dry-run 输出 | 不把压缩摘要当作订单事实 | `workflow_trace_tokens_before/after` |
| PVAOS | 压缩门户/组织/伙伴配置审计输出 | 不写入租户配置或权限配置 | `config_review_tokens_before/after` |
| Edge | 压缩采集日志和补传 dry-run 摘要 | 不处理未脱敏设备凭据或生产回执原文 | `edge_log_tokens_before/after` |
| PKC | 压缩个人知识检索摘要 | 不跨用户合并 memory | `personal_rag_tokens_before/after` |
| XiaoC | 压缩 agent 工具输出和授权检查摘要 | 不自动放宽工具权限 | `agent_tool_tokens_before/after` |
| XGD | 压缩风险分析与验证输出 | 不替代验收或状态裁决 | `risk_analysis_tokens_before/after` |
| XiaoG | 压缩只读查询结果和审计 mock 输出 | 不触达设备 OTA 或真实外部写入 | `readonly_query_tokens_before/after` |
| MMC | 压缩模板和配置清单差异 | 不自动修改模板基线 | `template_diff_tokens_before/after` |
| Studio | 压缩工作流审计和构建日志 | 不触发 release-write workflow | `workflow_log_tokens_before/after` |
| WAS | 压缩 ontology/OKF validator 输出 | 不替代语义契约原文或 KDS source of record | `ontology_gate_tokens_before/after` |

## 4. 接入模式

### 4.1 L1 治理准入

本轮完成：

1. 定义项目群应用边界。
2. 定义成本评估字段和公式。
3. 定义 Loop 纳入 evidence。
4. 建立本地 validator。

### 4.2 L2 本地试点

允许在后续轮次执行：

1. 使用脱敏样本和本地日志做压缩 dry-run。
2. 记录压缩前后 token、耗时、答案一致性和需召回原文次数。
3. 只将统计结果写入 evidence，不写敏感原文。

### 4.3 L3.5 及以上

必须另行显式授权。未授权前禁止：

1. 作为生产 LLM 代理。
2. 处理真实客户原件、合同、POD、金融凭证或密钥。
3. 启用跨项目 memory。
4. 让 `headroom learn` 自动写入 `AGENTS.md`、`CLAUDE.md` 或其他项目规则文件。
5. 执行真实外部 API 写入、生产配置修改、部署、推送或状态升级。

## 5. 安全控制

| 风险 | 控制要求 |
|---|---|
| Telemetry | 默认必须 `HEADROOM_TELEMETRY=off`，只有人工明确批准才可 opt in |
| 原文缓存 | CCR/local cache 必须记录路径、TTL、清理策略和敏感字段处理方式 |
| 密钥泄漏 | 不得记录 Authorization、Cookie、API Key、KDS Token 或项目私密配置 |
| 证据污染 | 压缩摘要不能替代原文、source_path、doc_id、evidence_id 或 validator 输出 |
| Memory 串域 | 首轮禁用跨项目 memory；如启用必须按项目隔离存储 |
| 自动写规则 | `headroom learn` 只能 dry-run，禁止自动改项目规则文件 |

## 6. 成本评估模型

成本模型采用可配置单价，不在本文件写死供应商价格。

### 6.1 输入字段

| 字段 | 含义 |
|---|---|
| `project` | 项目或专项 |
| `scenario` | 场景，如 RAG、Loop gate、build log、tool output |
| `input_tokens_before` | 压缩前输入 token |
| `input_tokens_after` | 压缩后输入 token |
| `output_tokens_before` | 输出 shaping 前输出 token |
| `output_tokens_after` | 输出 shaping 后输出 token |
| `cache_write_tokens_before` | 原链路缓存写 token |
| `cache_write_tokens_after` | Headroom 后缓存写 token |
| `cache_read_tokens_before` | 原链路缓存读 token |
| `cache_read_tokens_after` | Headroom 后缓存读 token |
| `retrieval_miss_count` | 压缩后需要召回原文次数 |
| `answer_equivalence` | `pass` / `partial` / `fail` |
| `sensitive_redaction_gate` | `pass` / `blocked` |

### 6.2 单价变量

| 变量 | 含义 |
|---|---|
| `P_in` | 输入 token 单价 |
| `P_out` | 输出 token 单价 |
| `P_cache_write` | 缓存写 token 单价 |
| `P_cache_read` | 缓存读 token 单价 |
| `P_runtime` | Headroom 本地运行成本，可为 0 或按机器时长折算 |

### 6.3 公式

```text
baseline_cost =
  input_tokens_before * P_in
  + output_tokens_before * P_out
  + cache_write_tokens_before * P_cache_write
  + cache_read_tokens_before * P_cache_read

headroom_cost =
  input_tokens_after * P_in
  + output_tokens_after * P_out
  + cache_write_tokens_after * P_cache_write
  + cache_read_tokens_after * P_cache_read
  + P_runtime

gross_saving = baseline_cost - headroom_cost
saving_rate = gross_saving / baseline_cost

admission_gate =
  answer_equivalence == pass
  and sensitive_redaction_gate == pass
  and retrieval_miss_count <= agreed_threshold
  and saving_rate >= agreed_min_saving_rate
```

### 6.4 推荐门槛

| 阶段 | 最低 saving_rate | 额外条件 |
|---|---:|---|
| L2 dry-run | 20% | 不允许敏感泄漏；答案一致性必须 pass |
| L3 受控试点 | 30% | 至少覆盖 5 个项目域和 3 类场景 |
| L4 自动运营候选 | 40% | 连续 3 轮 Loop evidence 通过；无状态漂移 |
| L5 生产自治候选 | 不在本文件授权 | 需要单独生产治理宪法 |

### 6.5 本地计算器

成本模型落地为本地可回放脚本：

```bash
python3 tools/kds-sync/calculate_headroom_cost_model.py fixtures/headroom/headroom-cost-measurement-template.json
```

样例 fixture 只记录脱敏 token 计数、单价变量和门禁结果，不记录原始上下文。真实 L2 dry-run 应复制该 fixture，替换为实测 token 数据后再进入 evidence。

### 6.6 项目群 L2 dry-run 样本

本轮新增项目群级 L2 样本测量：

```bash
python3 tools/kds-sync/generate_headroom_l2_project_group_dry_run.py
python3 tools/kds-sync/validate_headroom_l2_project_group_dry_run.py
```

该测量覆盖 GPCF、KDS、Brain、WAES、GFIS、GPC、PVAOS、Edge、PKC、XiaoC、XGD、XiaoG、MMC、Studio、WAS 共 15 个项目/域，输入来自既有受控文档、Loop state、状态矩阵和 admission evidence。

当前 `compressor_mode` 为 `structured_surrogate_no_headroom_runtime`：它证明成本模型、项目群覆盖、marker 保真和敏感文本不落盘的测量链路已经可执行，但不证明 `headroom-ai` runtime 已安装、真实 Headroom 压缩器已接入或生产 token 节省已经发生。

### 6.7 真实 runtime 探测门禁

本轮在 `/tmp/gpcf-headroom-runtime-probe` 隔离环境中使用 Python 3.12.13 安装 `headroom-ai==0.26.0`，并以 `HEADROOM_TELEMETRY=off` 执行真实 runtime probe：

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/probe_headroom_runtime.py
```

探测结论：

| 字段 | 当前值 |
|---|---|
| runtime_imported | true |
| headroom_version | 0.26.0 |
| project_count | 15 |
| runtime_saving_rate | 0.0 |
| transforms_applied | 全部 `router:noop` |
| runtime_admission_gate | false |

因此，当前只能声明真实 Headroom runtime 已被隔离探测，但不得声明它已对项目群样本形成有效压缩。进入 L3.5/L4 前，必须先找出受支持的 Headroom transform path、CLI/proxy/MCP 配置或 adapter 配置，并让真实 runtime 的 saving_rate、marker gate 和安全门禁同时通过。

### 6.8 runtime adapter dry-run

在直接压缩 Markdown/Loop state 返回 `router:noop` 后，本轮补充受控 adapter dry-run：将 15 个项目/域 evidence 摘为结构化 `project_group_evidence_json` tool payload，再调用 Headroom `CompressionUnit` + `ContentRouter` runtime 路径。

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_runtime_adapter_dry_run.py
python3 tools/kds-sync/validate_headroom_runtime_adapter_dry_run.py
```

测量结论：

| 字段 | 当前值 |
|---|---|
| headroom_runtime_used | true |
| adapter | project_group_evidence_json |
| project_count | 15 |
| tokens_before | 11049 |
| tokens_after | 10805 |
| tokens_saved | 244 |
| runtime_adapter_saving_rate | 0.022083 |
| minimum_saving_rate | 0.2 |
| all_marker_gates_pass | true |
| runtime_adapter_admission_gate | false |

该结果证明真实 Headroom runtime 对结构化 tool 输出存在可执行压缩路径，但节省率低于 L2 阈值。它只能作为下一轮扩大 tool-output 样本和成本模型对比的依据，不得升级 accepted、integrated 或 production_ready。

### 6.9 runtime scenario matrix

本轮进一步把真实 Headroom runtime 扩展到 4 类 LOOP 输出场景，形成应用矩阵：

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_runtime_scenario_matrix.py
python3 tools/kds-sync/validate_headroom_runtime_scenario_matrix.py
```

测量结论：

| scenario_id | saving_rate | marker_gate | scenario_gate |
|---|---:|---|---|
| project_group_evidence_json | 0.0 | true | false |
| headroom_metric_json_array | 0.510989 | true | true |
| loop_validation_log | 0.870801 | false | false |
| rg_marker_search_output | 0.538702 | false | false |

当前只有 `headroom_metric_json_array` 同时满足节省率和 marker gate。`loop_validation_log` 与 `rg_marker_search_output` 虽然节省率较高，但丢失项目 marker，因此不得纳入自动应用。场景矩阵总门禁仍为 `runtime_matrix_admission_gate=false`。

### 6.10 HeadroomCostMeasurement 输出类与拒绝策略

本轮将唯一达标方向固化为 `HeadroomCostMeasurement` 输出类：

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/build_headroom_cost_measurement_output.py
python3 tools/kds-sync/validate_headroom_cost_measurement_output.py
python3 tools/kds-sync/build_headroom_marker_preservation_policy.py
python3 tools/kds-sync/validate_headroom_marker_preservation_policy.py
```

`HeadroomCostMeasurement` 当前只允许用于 `structured_metric_tool_output_only`，不保存原始上下文，完整成本明细仍以 `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json` 为来源。

| 项 | 当前值 |
|---|---|
| HeadroomCostMeasurement saving_rate | 0.625378 |
| output_gate | true |
| allowed scenarios | `headroom_metric_json_array`, `headroom_cost_measurement_output` |
| rejected scenarios | `project_group_evidence_json`, `loop_validation_log`, `rg_marker_search_output` |
| log/search runtime application | blocked |

应用策略固定为 `reject_unless_saving_and_marker_gates_pass`。marker loss 和低于 saving 阈值均为硬阻断；因此 log/search 类输出在 marker-preserving adapter 完成前不得自动应用 Headroom。

### 6.11 受控 metric-output pilot

本轮将 allowlist 策略执行为最小受控应用闭环：

```bash
python3 tools/kds-sync/run_headroom_controlled_metric_pilot.py
python3 tools/kds-sync/validate_headroom_controlled_metric_pilot.py
```

pilot 应用 `headroom_cost_measurement_output` 与 `marker_preserving_log_search_adapter_output`，并继续阻断所有未经 adapter 的 rejected scenario。

| 项 | 当前值 |
|---|---|
| pilot_scope | `structured_metric_and_marker_preserving_adapter_outputs` |
| allowed_application_count | 2 |
| rejected_application_count | 3 |
| saving_rate | 0.636619 |
| controlled_metric_pilot_gate | true |
| production_admission_gate | false |

该 pilot 证明 Headroom 已在项目群 LOOP 中形成一个最小可复放应用闭环：结构化指标 tool output 与 marker-preserving adapter output 的成本观测压缩。它不代表生产代理、真实外部 API 写入、真实 KDS 写入或全场景 runtime admission。

### 6.12 连续 LOOP 成本观测

本轮将受控 metric-output pilot 接入连续 LOOP 成本观测账本：

```bash
python3 tools/kds-sync/run_headroom_loop_cost_observation.py
python3 tools/kds-sync/validate_headroom_loop_cost_observation.py
```

观测账本只纳入通过 gate 的 metric output 与成本 evidence，并排除 marker loss 或低于阈值的场景。

| 项 | 当前值 |
|---|---|
| observation_window | `HEADROOM-LOOP-COST-WINDOW-20260621-001` |
| runtime_included_count | 3 |
| blocked_scenario_count | 3 |
| runtime_tokens_before | 12261 |
| runtime_tokens_after | 8891 |
| runtime_tokens_saved | 3370 |
| runtime_saving_rate | 0.274346 |
| loop_cost_observation_gate | true |
| production_admission_gate | false |

该观测窗口证明 Headroom 已纳入 LOOP 成本观测体系，但范围仍限于 `metric_output_and_cost_evidence_only`。下一步必须在后续 LOOP round 重复观测，形成多窗口证据后才可申请更高阶段。

### 6.13 三窗口 LOOP 成本观测序列

本轮将 LOOP 成本观测扩展为三窗口序列：

```bash
python3 tools/kds-sync/run_headroom_loop_cost_observation_series.py
python3 tools/kds-sync/validate_headroom_loop_cost_observation_series.py
```

| 项 | 当前值 |
|---|---|
| window_count | 3 |
| window_1 | `HEADROOM-LOOP-COST-WINDOW-20260621-001` |
| window_2 | `HEADROOM-LOOP-COST-WINDOW-20260621-002` |
| window_3 | `HEADROOM-LOOP-COST-WINDOW-20260621-003` |
| runtime_saving_rate_window_1 | 0.274346 |
| runtime_saving_rate_window_2 | 0.274346 |
| runtime_saving_rate_window_3 | 0.274346 |
| max_runtime_saving_rate_drift | 0.0 |
| drift_gate_threshold | 0.01 |
| saving_rate_stability_gate | true |
| window_scope_normalized | true |
| loop_cost_observation_series_gate | true |
| production_admission_gate | false |

该序列证明 Headroom 已具备同口径连续成本观测证据，连续稳定性门禁通过。当前仍只覆盖 `metric_and_adapter_output_and_cost_evidence_only`，且尚未证明生产 token 节省。它不代表生产代理、真实外部 API 写入、真实 KDS 写入、全场景 runtime admission、accepted、integrated 或 production_ready。

### 6.14 log/search marker-preserving adapter pilot

上一轮场景矩阵中，`loop_validation_log` 与 `rg_marker_search_output` 的节省率达标，但因 marker loss 被拒绝。本轮新增受控 adapter 试点：

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_marker_preserving_adapter_pilot.py
python3 tools/kds-sync/validate_headroom_marker_preserving_adapter_pilot.py
```

adapter 策略为 `compressed_payload_plus_project_marker_index`：先执行真实 Headroom runtime compression，再追加最小项目 marker index；不保存原始 log/search 文本。

| 项 | 当前值 |
|---|---|
| adapter_scope | `log_and_search_outputs_only` |
| scenario_count | 2 |
| adapter_gate_pass_count | 2 |
| aggregate_saving_rate | 0.640676 |
| loop_validation_log_saving_rate | 0.856589 |
| rg_marker_search_output_saving_rate | 0.483019 |
| all_marker_gates_pass | true |
| production_admission_gate | false |

该试点证明 log/search 类输出存在 marker-preserving adapter 路径，并已作为受控 adapter output 进入 controlled metric pilot 与 marker policy。其适用范围仍限于 marker-preserving adapter output，不得声明全场景 runtime admission、生产接入、accepted、integrated 或 production_ready。

### 6.15 独立 production-token-free LOOP replay

本轮从原始 `headroom-loop-cost-observation` evidence 重新计算 Headroom 运行时成本观测，而不是复制三窗口序列结果：

```bash
python3 tools/kds-sync/run_headroom_independent_loop_round_replay.py
python3 tools/kds-sync/validate_headroom_independent_loop_round_replay.py
```

| 项 | 当前值 |
|---|---|
| replay_round_id | `GPCF-HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-001` |
| runtime_entry_count | 3 |
| runtime_tokens_before | 12261 |
| runtime_tokens_after | 8891 |
| runtime_tokens_saved | 3370 |
| runtime_saving_rate | 0.274346 |
| saving_rate_drift | 0.0 |
| saving_rate_stability_gate | true |
| independent_round_gate | true |
| production_tokens_used | false |
| production_admission_gate | false |

该 replay 证明 Headroom 已完成一轮独立 production-token-free LOOP 复测，且与同口径三窗口序列保持稳定。它仍不代表生产代理、真实外部 API 写入、真实 KDS 写入、全场景 runtime admission、accepted、integrated 或 production_ready。

### 6.16 生产 token 实测采集前置门禁

本轮建立生产 token 实测采集前置门禁，用于定义真实采集前必须满足的授权、脱敏、安全和成本字段要求：

```bash
python3 tools/kds-sync/build_headroom_production_token_intake_gate.py
python3 tools/kds-sync/validate_headroom_production_token_intake_gate.py
```

| 项 | 当前值 |
|---|---|
| production_source_present | false |
| sanitized_usage_ledger_present | false |
| authorized_window_present | false |
| telemetry_off_enforced | true |
| no_sensitive_raw_text_stored | true |
| production_token_intake_gate | false |
| measured_production_tokens | false |
| production_admission_gate | false |

该门禁证明 Headroom 已具备生产 token 采集的受控前置条件定义，但当前没有授权窗口、生产 token 来源或脱敏使用台账。因此它是阻断门禁，不是生产 token 实测或生产准入证明。

### 6.17 脱敏生产 token 台账模板

本轮新增脱敏生产 token 台账模板和本地校验器：

```bash
python3 tools/kds-sync/validate_headroom_production_token_ledger_template.py
```

| 项 | 当前值 |
|---|---|
| ledger_template | `fixtures/headroom/headroom-production-token-ledger-template.json` |
| ledger_type | `sanitized_production_token_usage_ledger` |
| telemetry | off |
| sensitive_raw_text_stored | false |
| measured_production_tokens | false |
| authorized_window_id | null |
| admission_gate | false |
| production_admission_gate | false |

该模板定义真实脱敏生产 token 台账的最小字段和本地成本模型校验方式。当前文件是未授权占位模板，不能作为生产 token 实测证据。

### 6.18 生产 token 台账负向 fixtures

本轮新增通用生产 token 台账评估器和负向 fixture 集：

```bash
python3 tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py
```

| 项 | 当前值 |
|---|---|
| ledger_evaluator | `tools/kds-sync/evaluate_headroom_production_token_ledger.py` |
| negative_fixtures | `fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json` |
| case_count | 5 |
| rejected | 5 |
| production_admission_gate | false |

负向 fixture 覆盖 telemetry on、raw prompt、缺授权窗口、缺回滚方案和 marker gate 失败。该门禁防止风险台账误入成本模型，不代表生产 token 实测已完成。

### 6.19 生产 token 授权采集包

本轮新增 pending 授权采集包，用于把未来真实采集前需要的人工授权窗口、审批人、审批时间、脱敏台账和回滚计划标准化：

```bash
python3 tools/kds-sync/build_headroom_production_token_authorization_package.py
python3 tools/kds-sync/validate_headroom_production_token_authorization_package.py
```

| 项 | 当前值 |
|---|---|
| authorization_status | pending |
| projects_requested | 15 |
| authorized_window_present | false |
| approver_present | false |
| approval_timestamp_present | false |
| sanitized_ledger_present | false |
| rollback_plan_present | false |
| authorization_package_gate | false |
| production_admission_gate | false |

该授权包只是采集申请，不是授权本身。未获得人工授权窗口前，不得采集生产 token、不得写真实 KDS、不得触达真实外部 API，也不得升级 accepted、integrated 或 production_ready。

### 6.20 生产 token 授权行动队列

本轮把 pending 授权采集包拆成可分配、可审计、可阻断的行动队列：

```bash
python3 tools/kds-sync/build_headroom_production_token_authorization_action_queue.py
python3 tools/kds-sync/validate_headroom_production_token_authorization_action_queue.py
```

| 项 | 当前值 |
|---|---|
| action_count | 6 |
| all_actions_have_owner | true |
| all_actions_have_due_loop | true |
| all_actions_closed | false |
| authorization_action_queue_gate | false |
| measured_production_tokens | false |
| production_admission_gate | false |

行动项覆盖授权窗口、审批人、审批时间、脱敏生产 token 台账、回滚计划、负向 fixture/evaluator 重跑和安全非声明确认。当前所有行动项仍是 pending，因此这是下一轮人工授权前的执行队列，不是授权证明或生产实测证明。

### 6.21 项目群应用路由注册表

本轮将 marker policy、controlled pilot 和 LOOP cost observation series 固化为 dry-run-only 应用路由注册表：

```bash
python3 tools/kds-sync/build_headroom_project_group_application_router.py
python3 tools/kds-sync/validate_headroom_project_group_application_router.py
```

| 项 | 当前值 |
|---|---|
| route_count | 6 |
| allowed_route_count | 3 |
| blocked_route_count | 3 |
| dry_run_application_gate | true |
| production_route_count | 0 |
| authorized_window_present | false |
| measured_production_tokens | false |
| production_admission_gate | false |

路由只允许 `headroom_metric_json_array`、`headroom_cost_measurement_output` 和 `marker_preserving_log_search_adapter_output` 在 dry-run 范围应用；`project_group_evidence_json`、`loop_validation_log` 和 `rg_marker_search_output` 仍按 marker loss 或低节省率阻断。所有路由均要求 marker gate、saving gate、答案一致性、安全脱敏和授权窗口；授权窗口不存在时不得进入生产。

### 6.22 项目级应用覆盖矩阵

本轮将项目群应用路由落到 15 个项目/域，形成项目级 dry-run 覆盖矩阵：

```bash
python3 tools/kds-sync/build_headroom_project_application_coverage_matrix.py
python3 tools/kds-sync/validate_headroom_project_application_coverage_matrix.py
```

| 项 | 当前值 |
|---|---|
| project_count | 15 |
| projects_with_l2_measurement | 15 |
| projects_with_dry_run_routes | 15 |
| projects_with_production_routes | 0 |
| project_application_coverage_gate | true |
| measured_production_tokens | false |
| production_admission_gate | false |

每个项目均绑定 3 条 dry-run 允许路由和 3 条阻断路由，并继承 L2 project measurement、授权窗口要求、脱敏生产 token 台账要求和生产阻断条件。该矩阵证明项目级应用落点已经可审计，不证明生产 rollout 已发生。

### 6.23 成本敏感性模型

本轮在固定成本公式基础上新增三组价格 profile 复算模型，用于观察 Headroom 成本节省率是否依赖单一价格假设：

```bash
python3 tools/kds-sync/build_headroom_cost_sensitivity_model.py
python3 tools/kds-sync/validate_headroom_cost_sensitivity_model.py
```

| 项 | 当前值 |
|---|---|
| profile_count | 3 |
| project_count | 15 |
| min_profile_saving_rate | 0.989505 |
| max_profile_saving_rate | 0.989506 |
| all_profiles_admission_gate | true |
| cost_sensitivity_gate | true |
| measured_production_tokens | false |
| production_admission_gate | false |

该模型只使用脱敏 dry-run token 计数和变量化 profile，不写入供应商真实价格，不证明真实生产账单节省。未来取得授权后的脱敏生产 token 台账应以同一 profile 结构复算，并与本模型比较。

## 7. Loop 纳入方式

本能力纳入 Loop 工程体系时，必须形成：

1. `HeadroomScenario`：场景定义。
2. `HeadroomCostMeasurement`：压缩前后 token 与成本记录。
3. `HeadroomEquivalenceGate`：答案一致性和 citation/source_path 保真检查。
4. `HeadroomSecurityGate`：敏感字段、telemetry、cache、memory 和自动写规则门禁。
5. `HeadroomCostDecision`：继续、回滚、扩大试点或停止。

每轮微循环：

```text
输入：脱敏样本、Loop 输出、RAG chunk 或工具输出
动作：执行压缩或模拟压缩
输出：压缩后上下文、成本记录、等价性判断
检查：安全、引用、成本、召回原文次数
反馈：更新场景门槛、禁用场景或扩大试点
```

## 8. 本轮 Definition of Done

| 项 | 判定 |
|---|---|
| 接入边界已定义 | done |
| 项目群应用矩阵已定义 | done |
| 成本模型公式已定义 | done |
| 成本模型本地计算器已建立 | done |
| 项目群 L2 dry-run 样本测量 | done |
| 真实 Headroom runtime 隔离探测 | done_noop_blocked |
| Headroom runtime adapter dry-run | done_below_l2_threshold |
| Headroom runtime scenario matrix | partial_one_scenario_passed |
| HeadroomCostMeasurement 输出类 | done_output_gate_pass |
| marker preservation policy | done_log_search_blocked |
| controlled metric-output pilot | done_metric_and_adapter_pilot_gate_pass |
| LOOP cost observation | done_metric_output_cost_observation_only |
| LOOP cost observation series | done_normalized_three_window_stability_gate_pass |
| independent production-token-free LOOP replay | done_independent_replay_gate_pass |
| production token intake gate | blocked_until_authorized_sanitized_usage_ledger |
| production token ledger template | done_template_validator_pass_admission_false |
| production token ledger negative fixtures | done_negative_fixtures_rejected |
| production token authorization package | pending_authorization_gate_false |
| production token authorization action queue | pending_action_queue_gate_false |
| project-group application router | done_dry_run_routes_only |
| project application coverage matrix | done_15_projects_dry_run_routes_only |
| cost sensitivity model | done_three_price_profiles |
| log/search marker-preserving adapter pilot | done_adapter_pilot_gate_pass |
| LCX controlled package | done_15_project_routes_proxy_sdk_mcp_agent_wrap_ccr_gate |
| LCX P0 runtime replay | done_runtime_cli_script_cost_marker_gate_pass |
| LCX P1 proxy dry-run smoke | done_local_livez_production_proxy_refusal_pass |
| LCX P2 MCP/SDK dry-run smoke | done_sdk_compress_mcp_cli_retrieve_gate_configured |
| LCX P3 learn preview working memory gate | done_learn_dry_run_apply_guard_memory_candidate_only |
| LCX P4 output shaper profile gate | done_acceptance_compliance_contract_finance_disabled |
| LCX P5 production admission package | done_request_package_generated_admission_false |
| LCX authorization boundary review | done_authorization_signal_present_incomplete_admission_false |
| LCX authorized measurement precheck | pass_precheck_only_waes_harness_admitted_no_measurement |
| LCX authorized measurement authorization template | done_template_generated_authorization_incomplete |
| LCX authorization negative fixtures | done_7_cases_rejected_admission_false |
| LCX authorization schema approval package | done_schema_and_human_approval_template_admission_false |
| LCX approval instance precheck | pass_precheck_only_fields_complete_measurement_blocked |
| LCX measurement admission request | pass_request_package_admitted_for_sanitized_precheck_no_measurement |
| LCX WAES/Harness admission decision checklist | done_positive_negative_fixtures_positive_semantic_approved |
| LCX sanitized measurement dry-run skeleton | pass_check_only_no_real_measurement |
| LCX metadata replay check | pass_check_only_no_real_measurement |
| LCX marker/retrieval miss comparison gate | pass_check_only_no_real_measurement |
| Loop evidence 已建立 | done |
| Validator 已建立 | done |
| 真实生产接入 | not_done |
| 全项目生产实测 token 数据 | not_done |
| L3.5/L4/L5 授权 | not_done |

## 9. 下一步

1. 建立 sanitized token fixture 扩展包，至少覆盖 5 个项目域和 3 类场景。
2. fixture 仍只允许记录 token 计数、marker、redaction、retrieval miss、answer equivalence 等脱敏元数据。
3. 继续保持 `production_token_measurement_allowed=false`、`measured_production_tokens=false`、`accepted=false`、`integrated=false`、`production_ready=false`。
4. 不读取原文、不计算真实生产节省、不启动 Headroom production proxy。
5. 只有扩展 fixture、marker/retrieval miss 门禁、脱敏 token evidence、独立轮次稳定性门禁和授权条件均通过后，才申请 L3.5 或 L4 试点授权。
