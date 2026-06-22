---
doc_id: GPCF-DOC-5E60043D38
title: GlobalCloud 项目群 Headroom LCX 全量实施方案与执行提示词
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群Headroom-LCX全量实施方案与执行提示词.md
source_path: 02-governance/GlobalCloud项目群Headroom-LCX全量实施方案与执行提示词.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Headroom LCX 全量实施方案与执行提示词

日期：2026-06-21
状态：全量实施蓝图 / 授权前受控方案

## 1. 执行结论

`chopratejas/headroom` 可以纳入 GlobalCloud 项目群，但只能按 `LCX / LOOP Context Optimization Layer` 定位实施。

Headroom 的项目群角色是：

```text
上下文压缩
Token 成本治理
可逆上下文缓存
跨 Agent 工作记忆候选
失败经验学习候选
```

Headroom 不得被定位为：

```text
Agent 框架
KDS 替代品
WAES 替代品
Harness 替代品
业务事实源
验收裁决源
生产自治授权源
```

## 2. 项目群范围差异处理

用户要求是整个项目群，不是单项目试点。因此本方案把外部方案中的能力清单扩展到 GPCF 状态矩阵当前覆盖的 15 个项目/域：

| # | 项目/域 | LCX 首要接入对象 | 首轮等级 | 生产门禁 |
|---|---|---|---|---|
| 1 | GPCF | Loop 控制板、治理日志、项目群状态摘要 | L2/L3 dry-run | 需授权 |
| 2 | KDS | RAG chunk、开发空间检索结果、metadata-only 摘要 | L2/L3 dry-run | 需授权 |
| 3 | Brain | 知识检索候选、引用回指候选、工作台上下文 | L2/L3 dry-run | 需授权 |
| 4 | WAES | 审计输入、风险摘要、门禁候选上下文 | L2/L3 dry-run | 需授权 |
| 5 | GFIS | runtime log、测试数据门禁输出、受控 dry-run trace | L2/L3 dry-run | 需授权 |
| 6 | GPC | 协同链路 dry-run、公共服务 trace、链路日志 | L2/L3 dry-run | 需授权 |
| 7 | PVAOS | 门户配置审计、组织/伙伴配置 diff | L2/L3 dry-run | 需授权 |
| 8 | Edge | 采集日志、补传 dry-run 摘要、设备侧非敏 trace | L2/L3 dry-run | 需授权 |
| 9 | PKC | 个人知识检索摘要、只读知识工作流输出 | L2/L3 dry-run | 需授权 |
| 10 | XiaoC | Agent 工具输出、模型路由检查、权限摘要 | L2/L3 dry-run | 需授权 |
| 11 | XGD | 长程任务日志、风险分析、验证输出 | L2/L3 dry-run | 需授权 |
| 12 | XiaoG | 只读查询结果、审计 mock、轻量执行 trace | L2/L3 dry-run | 需授权 |
| 13 | MMC | 模板 diff、配置清单、治理模板校验输出 | L2/L3 dry-run | 需授权 |
| 14 | Studio | workflow 审计、构建日志、工作台工具输出 | L2/L3 dry-run | 需授权 |
| 15 | WAS | ontology/OKF validator 输出、语义契约 gate 输出 | L2/L3 dry-run | 需授权 |

## 3. 目标架构

```text
GlobalCloud / LOOP Engineering
|
+-- KDS: 知识事实主存与受控镜像
+-- WAES: 规则、门禁、风险和授权裁决
+-- Harness: 执行、证据、回放、指标和验收准备
+-- Agent Runtime: Codex / Claude / Cursor / LiteLLM / LangChain / 项目自研 Agent
+-- LCX Headroom Layer:
    +-- LCX-Proxy
    +-- LCX-SDK
    +-- LCX-MCP
    +-- LCX-Agent-Wrap
    +-- LCX-CCR
    +-- LCX-Working-Memory
    +-- LCX-Learn
    +-- LCX-Output-Shaper
```

实施原则：

| 层 | 权限 |
|---|---|
| Headroom / LCX | 只处理上下文压缩、恢复、成本观测和候选记忆 |
| Harness | 记录压缩前后 token、恢复行为、质量等价和可回放证据 |
| WAES | 判断是否允许压缩、恢复、写记忆、启用 output shaping 或进入生产代理 |
| KDS | 登记能力、版本、策略和 evidence 索引，不接收 Headroom memory 作为正式事实 |
| Loop | 组织任务闭环、阶段升级、失败学习和下一轮输入 |

## 4. 全量能力映射

| Headroom 能力 | GlobalCloud 命名 | 项目群用途 | 首轮策略 |
|---|---|---|---|
| Proxy | LCX-Proxy | 作为 Agent/App 到 LLM provider 的受控出口 | 先 dev/test，生产禁用 |
| Library | LCX-SDK | 嵌入 KDS RAG、Brain、Harness、Agent runtime | 只处理脱敏样本 |
| Agent wrap | LCX-Agent-Wrap | 统一封装 Codex、Claude、Cursor、Aider、Copilot 等 | 只能由 Loop 启动器调用 |
| MCP server | LCX-MCP | 暴露 compress/retrieve/stats 工具 | retrieve 需要 WAES 高权限 |
| CCR | LCX-CCR | 压缩后按需恢复原文 | 取回必须进入 evidence |
| Cross-agent memory | LCX-Working-Memory | 工程工作记忆、路径修正、失败经验 | 禁止作为业务事实 |
| Failure learning | LCX-Learn | 从失败会话生成候选经验 | 只允许 preview/dry-run |
| Output reduction | LCX-Output-Shaper | 降低冗余输出 token | 验收/合规/财务/合同场景默认关闭 |

## 5. 受控能力包

最终工程化对象命名为：

```text
globalcloud-loop-headroom-adapter
```

建议目录结构：

```text
loop/context/headroom/
  README.md
  policy.yaml
  config.schema.yaml
  compression-profiles.yaml
  mcp.json
  proxy.env.example
  adapters/
    codex/
    claude/
    cursor/
    litellm/
    langchain/
    brain/
    kds-rag/
    harness/
    gpc/
  harness/
    evidence.schema.yaml
    metrics.schema.yaml
  waes/
    headroom-policy.yaml
    sensitive-pass-through.yaml
    ccr-retrieve-gate.yaml
  kds/
    context-optimization-component.yaml
  scripts/
    install-headroom.sh
    start-proxy.sh
    wrap-codex.sh
    collect-metrics.sh
    learn-preview.sh
    apply-approved-memory.sh
  docs/
    architecture.md
    operating-model.md
    security.md
    license.md
    rollout.md
```

本结构是目标蓝图。当前仓库已有 Headroom admission、runtime probe、成本观测、项目覆盖矩阵、授权包和行动队列 evidence；全量实现不得跳过这些门禁直接进入生产代理。

## 6. 阶段实施计划

### P0：OSS、License、安全与隔离安装

目标：

```text
确认 Apache-2.0 合规要求
锁定 Headroom 版本
隔离安装运行环境
关闭 telemetry
形成 OSS / Security / Runtime 初评
```

交付物：

| 产物 | 路径 |
|---|---|
| OSS review | `third_party/headroom/OSS_REVIEW.md` |
| Security review | `third_party/headroom/SECURITY_REVIEW.md` |
| Source record | `third_party/headroom/SOURCE.md` |
| Version lock | `third_party/headroom/VERSION.lock` |
| Modification register | `third_party/headroom/MODIFICATIONS.md` |
| Runtime probe evidence | `docs/harness/evidence/headroom-runtime-probe-*.json` |

验收：

```text
HEADROOM_TELEMETRY=off
不写真实 TOKEN
不写生产配置
runtime_imported=true
accepted=false
integrated=false
production_ready=false
```

### P1：项目群 LCX-Proxy 受控 dry-run

目标：

```text
为 Codex、Claude、Cursor、LiteLLM 建立统一代理入口
只在 dev/test/dry-run 使用
记录 tokens_before/tokens_after/quality_equivalence
```

交付物：

| 产物 | 路径 |
|---|---|
| Proxy env example | `loop/context/headroom/proxy.env.example` |
| Proxy start script | `loop/context/headroom/scripts/start-proxy.sh` |
| Agent route policy | `loop/context/headroom/policy.yaml` |
| Harness evidence schema | `loop/context/headroom/harness/evidence.schema.yaml` |
| Project coverage matrix | `docs/harness/evidence/headroom-project-application-coverage-matrix-*.json` |

硬门禁：

```text
不允许个人终端临时启动生产 proxy
不允许把真实客户原件、合同、POD、密钥或 KDS TOKEN 送入压缩链
不允许用压缩摘要替代原始 evidence
```

### P2：LCX-SDK 与 LCX-MCP 接入

目标：

```text
在 KDS RAG、Brain、Harness、Agent runtime 中接入 SDK 或 MCP
每次压缩均生成 Harness evidence
MCP retrieve 必须写入恢复原因和调用者
```

交付物：

| 产物 | 路径 |
|---|---|
| MCP config | `loop/context/headroom/mcp.json` |
| SDK adapter docs | `loop/context/headroom/docs/operating-model.md` |
| KDS registry object | `loop/context/headroom/kds/context-optimization-component.yaml` |
| WAES retrieve gate | `loop/context/headroom/waes/ccr-retrieve-gate.yaml` |

采集字段：

```yaml
headroom_evidence:
  task_id: string
  project_id: string
  agent_id: string
  model_id: string
  mode: proxy | sdk | mcp | wrap
  content_type: tool_output | log | rag_chunk | file | conversation
  tokens_before: number
  tokens_after: number
  compression_ratio: number
  ccr_enabled: boolean
  ccr_retrieve_count: number
  ccr_retrieve_reason: string
  policy_profile: string
  waes_decision: pass | warn | block
  answer_equivalence: pass | partial | fail | unknown
  marker_gate: pass | fail
  timestamp: string
```

### P3：LCX-Learn 与工作记忆治理

目标：

```text
把 headroom learn 转成 Loop Failure Learning Pipeline
只产候选经验，不直接写 AGENTS.md / CLAUDE.md / GEMINI.md
```

流程：

```text
失败会话
  -> headroom learn preview
  -> Harness 记录失败 evidence
  -> WAES 判定可写范围
  -> Owner 审核
  -> 写入项目工作记忆
  -> 必要时形成 KDS candidate
```

记忆分级：

| 等级 | 含义 | 写入条件 |
|---|---|---|
| L0 | 临时会话记忆 | 可自动，TTL 短 |
| L1 | 工程工作记忆 | Harness evidence + Owner 审核 |
| L2 | 受控知识事实 | KDS/WAES 正式流程，Headroom 不直写 |

禁止写入：

```text
客户合同事实
财务结论
业务审批结论
收益分配规则
政策性判断
合规结论
WAES 门禁结论
KDS 正式事实
```

### P4：LCX-Output-Shaper 与成本优化

目标：

```text
在开发、日志分析、测试修复、重复读取场景降低输出 token
在评审、验收、合规、合同、财务场景关闭 output shaping
```

推荐 profile：

```yaml
profiles:
  dev_fast:
    output_shaper: true
    effort_routing: true
    verbosity: low
  review_safe:
    output_shaper: false
    effort_routing: false
    verbosity: normal
  compliance_strict:
    output_shaper: false
    effort_routing: false
    verbosity: full
  log_debug:
    output_shaper: true
    effort_routing: true
    verbosity: terse
```

### P5：项目群生产准入候选

P5 不是当前授权范围。只有同时满足以下条件，才能申请：

```text
生产授权窗口已批准
脱敏生产 token 账本已通过
真实 provider 单价已登记
连续多窗口成本观测通过
answer_equivalence >= 95%
CCR 可恢复率 100%
WAES 敏感内容拦截 100%
marker_gate 100%
无 Headroom memory 事实污染
accepted=false/integrated=false/production_ready=false 直到 Harness/WAES 另行裁决
```

## 7. 授权模型

| 权限 | 允许角色 | 适用动作 | 必要条件 |
|---|---|---|---|
| LCX_INSTALL | LOOP_PLATFORM_ADMIN, DEVOPS_OWNER | 安装/升级 Headroom | OSS/Security review pass |
| LCX_PROXY_RUN | LOOP_AGENT_OPERATOR, DEVOPS_OWNER | dev/test/staging proxy | Harness trace required |
| LCX_AGENT_WRAP | DEVELOPER, AGENT_OPERATOR | agent wrap | project policy required |
| LCX_MCP_USE | APPROVED_AGENT, REVIEWER | compress/stats | tool visibility controlled |
| LCX_CCR_RETRIEVE | PROJECT_OWNER, REVIEWER, WAES_APPROVED_AGENT | retrieve 原文 | reason + evidence + sensitive check |
| LCX_MEMORY_WRITE | PROJECT_OWNER, LOOP_MEMORY_STEWARD | 写工作记忆 | review required |
| LCX_LEARN_APPLY | PROJECT_OWNER, LOOP_ENGINEERING_LEAD | 应用失败经验 | human approval |
| LCX_OUTPUT_SHAPER_ENABLE | PROJECT_OWNER, LOOP_PLATFORM_ADMIN | 输出压缩 | 禁止验收/合规/财务/合同 |

## 8. WAES 门禁包

建议策略文件：

```text
loop/context/headroom/waes/headroom-policy.yaml
```

核心规则：

```yaml
rules:
  - id: LCX-001
    name: Sensitive passthrough
    action: block_or_passthrough
    description: 高敏内容默认不压缩，不进入 LLM。
  - id: LCX-002
    name: CCR retrieve evidence required
    action: require_evidence
    description: 原文恢复必须记录 task_id、原因、调用者和内容类型。
  - id: LCX-003
    name: No official facts from Headroom memory
    action: block_fact_promotion
    description: Headroom memory 不得成为 KDS 正式事实源。
  - id: LCX-004
    name: Learn apply requires approval
    action: require_human_approval
    description: headroom learn 只能生成候选经验。
  - id: LCX-005
    name: Output shaping forbidden in acceptance
    action: disable_output_shaper
    description: 正式验收、合规、合同、财务任务禁止降低输出深度。
```

## 9. Harness 证据要求

每次 Headroom 介入必须生成证据。最低字段：

```yaml
headroom_evidence:
  evidence_id:
  task_id:
  loop_round_id:
  project_id:
  agent_id:
  model_id:
  mode:
  content_type:
  tokens_before:
  tokens_after:
  tokens_saved:
  saving_rate:
  ccr_enabled:
  ccr_retrieve_count:
  ccr_retrieve_reason:
  policy_profile:
  waes_decision:
  answer_equivalence:
  marker_gate:
  sensitive_redaction_gate:
  production_token_source:
  measured_production_tokens:
  accepted:
  integrated:
  production_ready:
```

禁止证据：

```text
原始客户合同全文
密钥、TOKEN、Cookie、Authorization header
未脱敏客户原件
未授权生产提示词全文
未经 Owner 审核的跨项目 memory
```

## 10. KDS 登记对象

建议新增 KDS 候选对象：

```yaml
id: LCX-HEADROOM
name: Headroom Context Optimization Layer
source_repo: chopratejas/headroom
license: Apache-2.0
usage_modes:
  - proxy
  - sdk
  - mcp
  - agent_wrap
  - ccr
  - working_memory
  - learn_preview
  - output_shaper
trust_level: L2_ENGINEERING_TOOL
fact_authority: false
evidence_authority: false
policy_controlled_by: WAES
evidence_recorded_by: Harness
kds_status: candidate_component
```

## 11. 成本评估模型

本方案沿用既有成本模型，不在文档中写死供应商单价。

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
```

准入门槛：

| 阶段 | 最低 saving_rate | 质量门禁 |
|---|---:|---|
| L2 dry-run | 20% | answer_equivalence pass；marker_gate pass |
| L3 受控试点 | 30% | 覆盖至少 5 个项目域和 3 类场景 |
| L4 自动运营候选 | 40% | 连续 3 轮 evidence 通过，无状态漂移 |
| L5 生产自治候选 | 不在本文件授权 | 另行生产治理宪法 |

## 12. 项目群全量 Definition of Done

全量实现必须达到：

```text
1. 15 个项目/域均有 LCX route：allowed、blocked、pending_authorization 三态之一。
2. LCX-Proxy、LCX-SDK、LCX-MCP、LCX-Agent-Wrap 均有受控配置和回放 evidence。
3. LCX-CCR retrieve 有 WAES gate、调用理由和 Harness evidence。
4. LCX-Learn 默认 preview，不自动写 AGENTS.md / CLAUDE.md / GEMINI.md。
5. LCX-Working-Memory 只承载工程工作记忆，不承载业务事实。
6. LCX-Output-Shaper 按 profile 启停，验收/合规/财务/合同默认关闭。
7. 成本模型覆盖输入、输出、cache write、cache read、runtime cost。
8. 每次压缩都有 tokens_before、tokens_after、saving_rate、quality gate。
9. KDS 只登记能力和 evidence 索引，不接收 Headroom memory 作为正式事实。
10. WAES 仍是授权与门禁裁决层。
11. Harness 仍是证据、回放和验收准备层。
12. 未经生产授权前，所有 production_admission_gate=false。
```

## 13. 全量实现提示词

以下提示词用于把本方案交给后续 Codex/Agent 继续执行。执行时必须保留本仓 AGENTS.md、Loop、KDS、WAES、Harness 边界。

```text
你是 GlobalCloud 项目群 GPCF 总控仓的工程执行 Agent。请严格执行
`02-governance/GlobalCloud项目群Headroom-LCX全量实施方案与执行提示词.md`
和 `02-governance/GlobalCloud项目群Headroom接入应用与成本评估模型.md`。

目标：
把 `chopratejas/headroom` 纳入整个 GlobalCloud 项目群，作为 LCX / LOOP Context Optimization Layer。
范围必须覆盖 15 个项目/域：GPCF、KDS、Brain、WAES、GFIS、GPC、PVAOS、Edge、PKC、XiaoC、XGD、XiaoG、MMC、Studio、WAS。

定位约束：
Headroom 只能作为上下文压缩、成本治理、可逆上下文缓存、工作记忆候选和失败经验学习候选能力。
不得把 Headroom 作为 Agent 框架、KDS 替代品、WAES 替代品、Harness 替代品、业务事实源、验收裁决源或生产自治授权源。

实施阶段：
P0：建立 OSS / License / Security / Runtime 隔离安装包，默认 `HEADROOM_TELEMETRY=off`。
P1：建立 LCX-Proxy 受控 dry-run，禁止生产代理。
P2：建立 LCX-SDK 与 LCX-MCP，所有 compress/retrieve/stats 进入 Harness evidence。
P3：建立 LCX-Learn 与工作记忆治理，`headroom learn` 只允许 preview/dry-run。
P4：建立 LCX-Output-Shaper profile，验收、合规、合同、财务场景关闭。
P5：只生成生产准入申请包，不得自行进入生产。

必须创建或更新的目标产物：
1. `loop/context/headroom/README.md`
2. `loop/context/headroom/policy.yaml`
3. `loop/context/headroom/config.schema.yaml`
4. `loop/context/headroom/compression-profiles.yaml`
5. `loop/context/headroom/mcp.json`
6. `loop/context/headroom/proxy.env.example`
7. `loop/context/headroom/adapters/*`
8. `loop/context/headroom/harness/evidence.schema.yaml`
9. `loop/context/headroom/harness/metrics.schema.yaml`
10. `loop/context/headroom/waes/headroom-policy.yaml`
11. `loop/context/headroom/waes/sensitive-pass-through.yaml`
12. `loop/context/headroom/waes/ccr-retrieve-gate.yaml`
13. `loop/context/headroom/kds/context-optimization-component.yaml`
14. `loop/context/headroom/scripts/install-headroom.sh`
15. `loop/context/headroom/scripts/start-proxy.sh`
16. `loop/context/headroom/scripts/wrap-codex.sh`
17. `loop/context/headroom/scripts/collect-metrics.sh`
18. `loop/context/headroom/scripts/learn-preview.sh`
19. `loop/context/headroom/scripts/apply-approved-memory.sh`
20. `loop/context/headroom/docs/architecture.md`
21. `loop/context/headroom/docs/operating-model.md`
22. `loop/context/headroom/docs/security.md`
23. `loop/context/headroom/docs/license.md`
24. `loop/context/headroom/docs/rollout.md`
25. 对应 Harness evidence JSON/MD、Loop round 文档和 validator。

项目群 route 要求：
每个项目/域必须有一条记录，字段至少包括：
project_id、source_path、allowed_modes、blocked_modes、requires_authorization、cost_fields、sensitive_boundaries、owner、current_gate。

Harness evidence 要求：
每次 Headroom 介入必须记录：
task_id、loop_round_id、project_id、agent_id、model_id、mode、content_type、tokens_before、tokens_after、tokens_saved、saving_rate、ccr_enabled、ccr_retrieve_count、policy_profile、waes_decision、answer_equivalence、marker_gate、sensitive_redaction_gate、measured_production_tokens、accepted、integrated、production_ready。

WAES 门禁要求：
高敏内容默认 block_or_passthrough。
CCR retrieve 必须 require_evidence。
Headroom memory 不得成为 KDS 正式事实源。
learn apply 必须 human_approval。
正式验收、合规、合同、财务任务必须 disable_output_shaper。

禁止事项：
不得写入真实 TOKEN。
不得写入真实 KDS API。
不得把 KDS 本地镜像写成真实 KDS API 已同步。
不得启用跨项目 memory 作为业务事实。
不得执行 `headroom learn --apply` 自动修改受控规则文件。
不得处理未脱敏客户合同、POD、财务凭证、密钥或生产凭证。
不得生产部署、推送、真实外部 API 写入、数据库迁移或权限变更。
不得把任何文档通过、validator 通过或 dry-run 通过声明为 accepted、integrated 或 production_ready。

验证命令至少包括：
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/validate_headroom_project_group_admission.py
python3 tools/kds-sync/validate_headroom_project_application_coverage_matrix.py
python3 tools/kds-sync/validate_headroom_cost_sensitivity_model.py
python3 tools/kds-sync/validate_headroom_project_group_application_router.py

成功标准：
15 个项目/域都有 LCX route。
LCX-Proxy、LCX-SDK、LCX-MCP、LCX-Agent-Wrap 均有受控配置。
CCR retrieve 有 WAES gate 和 Harness evidence。
成本模型可回放，且不保存敏感原文。
文档门禁、污染检查、KDS TOKEN 检查通过。
全量实现完成前仍保持 accepted=false、integrated=false、production_ready=false，除非用户另行授权并由 Harness/WAES evidence 裁决。

输出要求：
用中文写实施记录。
每轮输出必须包含：输入、动作、输出、检查、反馈、下一轮。
如发现范围冲突，以“整个项目群”优先，不得退化为单项目试点。
```

## 14. 本轮边界

本文件只建立全量实施方案和执行提示词，不声明 Headroom 已完成全量工程化接入。

当前仍保持：

```text
accepted=false
integrated=false
production_ready=false
production_admission_gate=false
measured_production_tokens=false
```
