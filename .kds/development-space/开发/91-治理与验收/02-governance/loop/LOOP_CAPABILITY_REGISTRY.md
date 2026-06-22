---
doc_id: GPCF-DOC-9B8C2D4F61
title: LOOP 能力注册表
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CAPABILITY_REGISTRY.md
source_path: 02-governance/loop/LOOP_CAPABILITY_REGISTRY.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP 能力注册表

本文是 LOOP 工程体系的能力注册表。它登记纳入 LOOP 主进程的技能、工具和方法，并定义准入、默认启用、证据升级、降级停用和门禁检查规则。

本文不替代 [LOOP 工程体系整体实施规范](./LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md)。整体实施规范定义基线；本文维护能力清单。能力登记只代表可被治理，不代表可直接执行高风险动作。

## 1. 注册目标

能力注册表必须解决四个问题：

| 问题 | 约束 |
|---|---|
| 什么能力已纳入 LOOP | 以技能池、工具池、方法池三类登记 |
| 能力能否默认使用 | 由风险分级裁决，不由效率收益单独决定 |
| 能力能否升级状态 | `pilot` 以上状态变化必须有 evidence |
| 能力如何退出 | 支持降级、停用、废弃、替代和回滚路径 |

## 2. 状态模型

| 状态 | 含义 | 最低证据 |
|---|---|---|
| `fast_admitted` | 快速准入，已进入能力池但尚未完整治理 | 有用途说明和风险初判 |
| `candidate` | 候选能力，可在低风险或只读场景试用 | 有适用场景和禁用场景 |
| `pilot` | 试点能力，可在限定范围内执行 | 有 evidence、回滚或停用方式 |
| `controlled` | 受控能力，可在注册边界内稳定使用 | 有 validator、门禁或可回放证据 |
| `default_enabled` | 默认启用能力 | 风险分级允许，且有清晰禁止边界 |
| `downgraded` | 已降级 | 有降级原因和影响说明 |
| `disabled` | 已停用 | 有停用原因和替代路径 |
| `deprecated` | 已废弃 | 有废弃原因和迁移路径 |
| `superseded` | 已被替代 | 有替代能力标识 |

## 3. 风险分级

| 风险 | 典型能力 | 默认策略 |
|---|---|---|
| `low` | 只读检查、文档读取、局部 validator、无写入检索 | 可作为 `default_enabled` 候选 |
| `medium` | 本地文档写入、受控报告、候选 evidence、非生产自动化 | 可 `pilot` 或 `controlled`，默认启用需额外证据 |
| `high` | 跨仓修改、外部搜索结果影响状态、自动多智能体执行、工具链写入 | 默认不启用，必须按任务授权 |
| `critical` | 生产写入、外部 API 写入、schema sync、部署、权限、commit、push | 不因能力登记获得授权 |

## 4. 注册字段

每个能力条目必须能追溯以下字段：

| 字段 | 含义 |
|---|---|
| `capability_id` | 能力唯一标识 |
| `type` | `skill`、`tool` 或 `method` |
| `status` | 状态模型中的一个或多个状态 |
| `risk_level` | 风险分级 |
| `version_scope` | 适用 LOOP 版本范围 |
| `owner` | 责任主体 |
| `allowed_contexts` | 允许使用的上下文 |
| `forbidden_contexts` | 禁止使用的上下文 |
| `evidence_required` | 使用、升级或默认启用所需 evidence |
| `validator_or_gate` | 对应 validator、门禁或检查命令 |
| `rollback_or_disable` | 回滚、停用或降级方式 |
| `last_reviewed` | 最近复核日期 |

## 5. 全局规则

- 快速准入只表示进入能力池，不表示自动启用。
- `default_enabled` 必须由风险分级裁决。
- `pilot` 以上状态变化必须有 evidence。
- 高风险和关键风险能力必须按任务授权。
- 能力登记不得绕过 `LOOP_AUTONOMY_POLICY.md`、`LOOP_EXECUTION_RULES.md`、`LOOP_CONTROL_BOARD.md` 或 Harness Governance。
- 能力注册表是 LOOP 文档门禁硬检查；`validate_loop_capability_registry.py` 失败时，`loop_document_gate.py` 必须进入 `rework_required`。
- 能力登记不授权 production write、external API write、schema sync、bench migrate、deployment、permission change、commit、push、accepted 或 integrated。

## 6. 核心技能池

| capability_id | status | risk_level | allowed_contexts | forbidden_contexts | validator_or_gate |
|---|---|---|---|---|---|
| `skill.globalcloud-loop-orchestrator` | `controlled`, `default_enabled` | `low` | LOOP 轮次编排、下一轮输入、状态上限判断 | 自动验收、自动生产写入 | 必读技能 + 文档门禁 |
| `skill.globalcloud-document-governance` | `controlled`, `default_enabled` | `low` | 文档治理、污染检查、TOKEN 检查、KDS 边界判断 | 未授权运行会改写镜像的同步命令 | `loop_document_gate.py` |
| `skill.globalcloud-ui-quality-gate` | `pilot` | `medium` | UI 审计、可用性、可访问性、Playwright 证据 | 未授权改动产品主线 | UI 专项 evidence + `validate_loop_ui_quality_baseline.py` |
| `skill.opsx-full-cycle` | `pilot` | `medium` | 需求到 evidence 的受控执行编排 | 最终验收裁决 | OpsX evidence |
| `skill.globalcloud-harness-governance` | `pilot` | `medium` | evidence 审计、验收状态收口 | 变更编排、生产写入 | Harness 判定记录 |
| `skill.software-project-assessment` | `candidate` | `low` | 项目健康评估、功能完整性检查 | 把评估结论写成验收完成 | 评估报告 evidence |

## 7. 核心工具池

| capability_id | status | risk_level | allowed_contexts | forbidden_contexts | validator_or_gate |
|---|---|---|---|---|---|
| `tool.loop_document_gate.py` | `controlled`, `default_enabled` | `low` | 文档门禁总检查 | 用检查通过替代业务完成 | `python3 tools/kds-sync/loop_document_gate.py --check-only` |
| `tool.check_document_pollution.py` | `controlled`, `default_enabled` | `low` | 防污染检查 | 自动修正文档事实 | `python3 tools/kds-sync/check_document_pollution.py` |
| `tool.validate_kds_token.py` | `controlled`, `default_enabled` | `low` | KDS TOKEN 泄漏检查 | 输出或写入密钥 | `python3 tools/kds-sync/validate_kds_token.py` |
| `tool.check_chinese_localization_gate.py` | `controlled` | `low` | 中文本地化门禁 | 自动改写历史证据 | `python3 tools/kds-sync/check_chinese_localization_gate.py` |
| `tool.validate_loop_engineering_master_plan.py` | `controlled`, `default_enabled` | `low` | 主实施规范校验 | 证明业务闭环完成 | `python3 tools/kds-sync/validate_loop_engineering_master_plan.py` |
| `tool.validate_loop_capability_registry.py` | `controlled`, `default_enabled` | `low` | 能力注册表校验 | 授权高风险能力执行 | `python3 tools/kds-sync/validate_loop_capability_registry.py` |
| `tool.validate_loop_baseline_sync_readiness.py` | `controlled`, `default_enabled` | `low` | LOOP 基线文档 scoped 同步准入预检 | 执行同步写入或替代人工授权 | `python3 tools/kds-sync/validate_loop_baseline_sync_readiness.py` |
| `tool.validate_loop_engineering_five_direction_implementation.py` | `controlled`, `default_enabled` | `low` | 五方向实施规范校验 | 替代运行层事实 | validator 输出 |
| `tool.validate_loop_ui_quality_baseline.py` | `controlled`, `default_enabled` | `low` | Loop UI gate baseline、模板和显式 UI round 结构校验 | 替代真实 UI 运行证据或客户验收 | `python3 tools/kds-sync/validate_loop_ui_quality_baseline.py` |
| `tool.validate_loop_round_efficiency_audit.py` | `controlled` | `low` | 轮次效率审计 | 把批量生成计为实质轮次 | validator 输出 |
| `tool.validate_continuous_round_substance.py` | `controlled` | `low` | 连续轮次实质性检查 | 掩盖空转 | validator 输出 |
| `tool.validate_l3_continuation_guard.py` | `controlled` | `low` | L3 连续性门禁 | 越权进入 L4/L5 | validator 输出 |
| `tool.git-status-diff-check` | `controlled`, `default_enabled` | `low` | `git status`、`git diff`、`git diff --check` | commit、push、reset、checkout 覆盖用户工作 | Git 输出 |
| `tool.document_control.py.scoped` | `pilot` | `medium` | 明确授权后的 scoped 文档受控同步 | 未授权改写镜像、登记簿或 KDS | 同步报告 + diff |

## 8. 核心方法池

| capability_id | status | risk_level | allowed_contexts | forbidden_contexts | validator_or_gate |
|---|---|---|---|---|---|
| `method.six_segment_microcycle` | `controlled`, `default_enabled` | `low` | 六段式微循环：输入、判断、动作、输出、检查、反馈 | 省略证据链 | round record |
| `method.task_package` | `controlled`, `default_enabled` | `low` | 文档 + validator + evidence + 状态同步 + 运行层事实或明确阻塞 | 只有文档无验证 | 任务包检查 |
| `method.evidence_first` | `controlled`, `default_enabled` | `low` | 以 evidence 决定状态 | 以意图、口述、fixture 替代事实 | evidence index |
| `method.no_write_dry_run` | `controlled`, `default_enabled` | `low` | 高风险动作前 no-write 验证 | 把 dry-run 当成真实执行 | 命令输出 |
| `method.lane_layering` | `controlled`, `default_enabled` | `low` | `test_data_lane`、`candidate_lane`、`real_business_lane` 分层 | 混淆测试、候选、真实业务 | 状态矩阵 |
| `method.owner_waes_harness_release` | `controlled` | `medium` | candidate 到 real 的组合放行 | 单 agent 自动放行 | 放行记录 |
| `method.three_layer_scoring` | `controlled` | `low` | 治理成熟度、工程执行进度、业务闭环三层评分 | 用单分数覆盖真实阻塞 | 评分报告 |
| `method.layered_conflict_priority` | `controlled` | `low` | 运行事实、项目群状态、历史记录分层裁决 | 用历史文档覆盖当前运行证据 | 冲突记录 |
| `method.controlled_engineering_change` | `controlled` | `medium` | 受控工程修改 | 生产写入、部署、权限、schema、外部 API 写入 | diff + validator |
| `method.per_task_git_authorization` | `controlled`, `default_enabled` | `low` | 按任务授权 Git 操作 | 自动 commit、push、reset | Git 授权记录 |
| `method.codegraph` | `controlled` | `medium` | CodeGraph 只读索引、依赖分析、调用图分析 | 自动改写代码、跨仓写入 | CodeGraph evidence |
| `method.external_search_retrieval` | `controlled` | `medium` | 外部搜索/检索用于事实核验和候选情报 | 把外部搜索直接升级为内部完成态 | 检索引用 + 人工裁决 |
| `method.rag_semantic_index` | `controlled` | `medium` | RAG/语义索引用于受控知识检索和上下文召回 | 未验证召回直接写成 source-of-record | 索引刷新和命中证据 |
| `method.multi_agent_parallel_development` | `controlled` | `high` | 多智能体并行开发用于 disjoint scope 分析、候选实现、审查 | 未隔离写同一文件、自动合并、自动提交 | 分工记录 + 主线程整合验证 |
| `family.codegraph` | `controlled` | `medium/high` | CodeGraph 能力族：索引、依赖、调用图、影响面、watchlist、drift 监控 | 自动改写代码、跨仓写入、自动提交 | CodeGraph validator 与 drift evidence |
| `family.agent_reach` | `pilot` | `medium/high` | Agent-Reach 能力族：外部搜索、候选检索、benchmark、候选质量回放 | 未经 WAES/KDS 复核直接进入内部 source-of-record | Agent-Reach benchmark 与 review evidence |
| `family.ontology` | `controlled/pilot` | `medium` | Ontology 语义治理能力族：对象、关系、状态、语义合同、validator | 未验证语义合同直接改写运行层事实 | Ontology validator 与语义合同 evidence |
| `family.was_ontology_was` | `pilot` | `medium/high` | WAS / Ontology-WAS 能力族：WAS 准入、真实 source record intake、Ontology-WAS 监控 | 未授权接收真实业务源记录或写入 GFIS/WAES | WAS/Ontology-WAS validator 与 intake evidence |
| `family.headroom` | `pilot` | `medium/high` | Headroom 能力族：成本、运行时、proxy dry-run、runtime adapter、measurement admission | 未授权生产测量、真实 token、外部服务写入或成本承诺 | Headroom dry-run/proxy/runtime evidence |
| `family.okf_odf` | `controlled` | `medium` | OKF/ODF 治理能力族：metadata-only 派生、受控摘要、对象/文档/证据治理 | 把派生层写成 KDS source-of-record 或真实业务完成 | OKF/ODF validator 与 approval evidence |
| `family.lcx` | `pilot` | `medium/high` | LCX 能力族：authorization、approval instance、measurement precheck、controlled package | 未授权测量、生产 token、外部写入或状态升级 | LCX precheck、authorization 和 package evidence |
| `family.waes_kds_rag_writeback` | `candidate/pilot` | `high` | WAES-KDS RAG writeback 能力族：RAG 写回门禁包、候选回写、人工复核流 | 未授权写回 KDS、WAES、外部 API 或状态机 | WAES-KDS RAG writeback gate pack |

## 9. 核心能力族与子能力矩阵

能力族用于治理一组相互关联的技能、工具、方法和 evidence。能力族不是单个工具名；每个能力族必须明确只读/分析子能力、候选/试点子能力、禁止越界、绑定 evidence 或 validator。

| 能力族 | 建议类型 | 建议状态 | 风险 | 受控子能力 | 试点或候选子能力 | 绑定 evidence 或 validator |
|---|---|---|---|---|---|---|
| CodeGraph | core method family | `controlled` | `medium/high by sub-capability` | 只读索引、依赖分析、调用图分析、影响面分析、watchlist 监控 | 自动生成候选补丁、跨仓影响推断、sync-only closure | `validate_codegraph_*`、CodeGraph drift/watchlist evidence |
| Agent-Reach | method/tool family | `pilot` | `medium/high` | 搜索目标定义、候选检索、benchmark、候选质量趋势分析 | limited candidate ingestion、外部来源候选进入 review queue | `validate_agent_reach_*`、Agent-Reach benchmark/review evidence |
| Ontology | semantic governance method | `controlled/pilot` | `medium` | 对象目录、关系图、语义合同、negative fixtures、validator | 语义合同候选写入、跨项目 ontology registry 更新 | `validate_ontology_*`、Ontology contract evidence |
| WAS / Ontology-WAS | method family | `pilot` | `medium/high` | WAS 状态矩阵、source record precheck、monitor、waiting room | real source record intake pack、candidate precheck execution | `validate_was_*`、`validate_ontology_was_*`、source-record intake evidence |
| Headroom | cost/runtime measurement method | `pilot` | `medium/high` | cost model、marker preservation、proxy dry-run、runtime probe | runtime adapter、measurement admission、production token authorization package | `validate_headroom_*`、Headroom dry-run/proxy/runtime evidence |
| RAG/语义索引 | method family | `controlled` | `medium` | 受控文档召回、语义命中、索引刷新验证 | 自动摘要、候选任务包、候选 writeback draft | RAG index evidence、命中 evidence |
| 多智能体并行开发 | method family | `controlled with restrictions` | `high` | 只读审查、分离文件分析、候选实现、独立验证 | 多 worktree 候选执行、并行修复提案 | 分工记录、主线程整合验证 |
| OKF/ODF | governance method family | `controlled` | `medium` | metadata-only collection、summary approval、ODF small-batch governance | approved summary writer dry-run、ODF directed sync candidate | `validate_okf_*`、ODF gate evidence |
| LCX | authorization/measurement method family | `pilot` | `medium/high` | authorization schema、approval instance precheck、controlled package | authorized measurement、production token intake/authorization | `validate_headroom_lcx_*`、LCX authorization evidence |
| WAES-KDS RAG writeback | gate/writeback method | `candidate/pilot` | `high` | writeback gate pack、candidate queue、manual review packet | RAG writeback execution、KDS/WAES writeback | `validate_was_waes_kds_rag_writeback_gate_pack.py`、writeback evidence |

## 10. 核心方法子能力分级

| 方法 | 受控子能力 | 试点或候选子能力 | 禁止越界 |
|---|---|---|---|
| CodeGraph | 只读索引、依赖分析、调用图分析、影响面分析 | 自动生成候选补丁、跨仓影响推断 | 自动写入、自动提交、替代测试 |
| 外部搜索/检索 | 公开资料核验、官方文档检索、事实交叉验证 | 搜索结果驱动的候选方案 | 外部搜索直接变更内部状态或生产事实 |
| RAG/语义索引 | 受控文档召回、语义命中、索引刷新验证 | 自动生成候选摘要和候选任务包 | 未验证召回替代 KDS、GFIS 或 WAES source-of-record |
| 多智能体并行开发 | 只读审查、分离文件分析、候选实现、独立验证 | 多分支或多 worktree 候选执行 | 未授权合并、自动覆盖用户工作、自动推送 |
| Agent-Reach | benchmark、候选质量趋势、外部来源归因 | limited candidate ingestion、review queue 候选导入 | 外部搜索结果直接写入 KDS source-of-record |
| Ontology / WAS | schema、semantic contract、negative fixtures、monitor | real source record candidate precheck、intake pack | 未授权创建真实 source-of-record 或 GFIS runtime primary key |
| Headroom / LCX | cost model、dry-run、proxy smoke、authorization precheck | runtime measurement、production token authorization package | 未授权生产测量、真实 token、外部服务写入 |
| OKF/ODF / WAES-KDS writeback | metadata-only gate、approval request、writeback gate pack | directed sync candidate、RAG writeback candidate | 未授权 KDS/WAES 写回、状态升级或业务完成声明 |

## 11. 候选能力池

| capability_id | status | risk_level | allowed_contexts | forbidden_contexts | validator_or_gate |
|---|---|---|---|---|---|
| `tool.figma` | `candidate` | `medium` | 设计上下文、截图、受控设计资产生成 | 未授权改产品实现或发布设计基线 | Figma evidence |
| `tool.vercel` | `candidate` | `high` | 预览检查、只读部署信息、日志诊断 | 未授权部署、环境变量写入、域名变更 | Vercel evidence |
| `tool.linear` | `candidate` | `medium` | issue 查询、候选任务同步 | 未授权修改项目状态或客户需求 | Linear 记录 |
| `tool.browser_automation` | `candidate` | `medium` | 本地页面验证、截图、可用性检查 | 未授权线上写入或账户操作 | 浏览器 evidence |

## 12. 能力族升级规则

- 只读分析、索引、评估、候选生成可以进入 `controlled`。
- 写回、同步、外部 API、跨仓执行、成本测量、自动修复必须保持 `pilot` 或 `candidate`，并按任务授权。
- 写入、自动化、跨仓和外部 API 子能力不得因能力族登记自动启用。
- `pilot` 以上状态变化必须有 evidence。
- 能力族必须绑定 validator 或 evidence；没有 validator 或 evidence 的能力族不得进入 `default_enabled`。
- 能力族登记不得授权真实 KDS API 写入、WAES 写回、GFIS 运行层写入、生产 token、生产成本测量、外部 API 写入、commit、push、accepted 或 integrated。

## 13. 退役与替代

能力出现以下情况时必须进入降级、停用、废弃或替代流程：

- 产生状态膨胀、弱证据误判或主体错位。
- 与 `LOOP_AUTONOMY_POLICY.md`、`LOOP_EXECUTION_RULES.md` 或项目边界冲突。
- validator 漂移导致漏报或误报。
- 外部工具、API、权限或成本边界发生变化。
- 有更低风险、更可回放的替代能力。

退役记录必须说明原能力、状态变化、原因、影响、替代能力、回滚或停用方式和 evidence。

## 14. 当前结论

截至 `2026-06-22`，LOOP 能力治理采用快速准入、风险分级默认启用、`pilot` 以上 evidence 升级、退役可追溯的模型。CodeGraph、Agent-Reach、Ontology、Headroom、RAG/语义索引、多智能体并行开发、OKF/ODF、LCX、WAES-KDS RAG writeback 已进入能力族治理结构；其写入、同步、自动化、跨仓、成本测量和外部 API 子能力仍受 `pilot`、`candidate` 或显式任务授权约束。
