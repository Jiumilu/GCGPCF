---
doc_id: GPCF-DOC-7B5E3B05D7
title: GlobalCloud 项目群最小闭环 L4 实施方案
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud项目群最小闭环L4实施方案.md
source_path: 01-architecture/GlobalCloud项目群最小闭环L4实施方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群最小闭环 L4 实施方案

日期：2026-06-13
状态：v1.0
用途：把“全部 12 个项目纳入最小闭环，只是激活深度不同”的架构原则落成 L4 实施作战图，确保项目群从单项目 L3 真实闭环升级为跨项目最小业务闭环。

---

## 1. 实施结论

L4 最小闭环不是选取少数项目组成一条链路，而是将 12 个项目全部纳入同一个项目群闭环。不同项目的参与深度可以不同，但每个项目都必须具备职责、输入、输出、验证方式和 evidence。

L4 的核心完成标准：

```text
12 个项目全部在闭环中有明确位置；
成熟项目真实运行，低成熟项目至少完成契约、mock、dry-run 或占位验证；
闭环结果能够回到 GPCF / GPC / KDS / WAES 形成受控证据、状态和知识沉淀。
```

本方案承接：

- `01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md`
- `02-governance/GlobalCloud绿色供应链体系模块实施分级判定表.md`
- `04-ui-delivery/GlobalCloud绿色供应链体系P0最小闭环界面实施清单.md`
- `02-governance/loop/LOOP_L4_AUTONOMOUS_OPERATIONS.md`
- `09-status/globalcloud-l3-admission-matrix.md`

---

## 2. L4 与 L3 的边界

| 层级 | 目标 | 通过标准 |
|---|---|---|
| L3 | 单项目真实闭环 | 每个项目能在真实仓完成代码/配置/测试/evidence 闭环 |
| L4 | 项目群最小闭环 | 12 个项目围绕同一最小业务链路形成跨项目输入、输出、验证和证据 |
| L5 | 客户场景闭环 | 面向真实客户、工厂或运营角色可使用、可验收、可度量 |

L4 不允许用以下内容替代：

1. 不允许用 12 个项目各自测试通过替代项目群闭环通过。
2. 不允许用文档描述替代真实仓代码、配置、测试、dry-run 或 evidence。
3. 不允许用批量生成 round 文档替代实质轮次。
4. 不允许把 mock 或 dry-run 标记为 production-ready。
5. 不允许自动升级 `accepted` 或 `integrated`。

---

## 3. 项目群最小闭环业务主线

P0 最小闭环业务主线为：

```text
项目初始化
-> 组织/伙伴接入
-> 平台订单
-> 报价/订单评审/合同
-> 配方研发
-> 样品打样/样箱打样
-> 客户签样确认
-> 转量产门禁
-> 工厂订单
-> 工单
-> 质量/库存/批次
-> 发货
-> 签收
-> 异常
-> WAES 状态/证据
-> 日报/复盘
-> KDS 知识沉淀
-> GPCF 项目群收口
```

这条主线对应四类能力面：

| 能力面 | 项目 | 职责 |
|---|---|---|
| 控制与治理 | GPC, GPCF, WAES, MMC | 目标控制、状态门禁、证据、策略模板、实施节奏 |
| 知识与智能 | KDS, Brain, PKC | 知识主存、检索呈现、个人工作台、结构化沉淀 |
| 工厂与供应链执行 | GFIS, GPC, PVAOS | 工厂事实、平台协同、样品确认、生态入口、组织伙伴 |
| AI 执行体系 | XiaoC, XGD, XiaoG | 蚁后编排、大象重分析、蚂蚁执行终端 |

---

## 4. 12 项目职责、输入、输出与验证

| 项目 | L4 职责 | 输入 | 输出 | 阶段一深度 | 最小验证 |
|---|---|---|---|---|---|
| GFIS | 工厂事实主账，承接配方研发、样品打样、工厂订单、工单、质量、库存、批次、发货事实 | GPC 平台订单/样品申请/转量产门禁、XiaoG 只读查询、WAES 治理规则 | 样品工单、样品检测、工厂订单、工单状态、质量/库存/批次/发货证据 | 全激活 | Frappe/ERPNext API 或样本 dry-run、样品/工单字段验证、证据样本 |
| GPC | 平台公共服务本体，承接平台订单、样品申请、客户签样、转量产、ASN、预约、TMS、POD、异常协同 | PVAOS 组织伙伴、GFIS 样品/工厂回执、WAES 状态门 | 平台订单、样品确认、转量产指令、签收/POD、外部异常、协同状态 | 薄激活 | GPC 一期对象/接口契约、订单/样品/签收 mock/dry-run |
| PVAOS | 生态入口，承接租户、组织、伙伴、权限和项目空间 | 项目初始化需求、组织伙伴资料、GPC 协同关系 | 组织/伙伴接入结果、项目空间、权限边界 | 薄激活 | 组织/伙伴/租户对象验证、权限边界说明 |
| WAES | 治理中枢，承接状态、证据、AI 越权拦截和审计 | 全项目事件、XiaoG 审计日志、GPCF 状态规则 | 状态判定、证据台账、风险阻断、审计记录 | 活跃 | evidence 写入 dry-run、状态门禁验证、越权阻断样本 |
| KDS | 知识主存，承接受控文档、SOP、案例、参数和发布状态 | GPCF 文档、WAES evidence、GFIS/GPC 业务样本 | 知识索引、版本记录、引用回指、发布状态 | 活跃 | KDS 索引/API contract dry-run、文档引用回指 |
| Brain | 知识 UI 与检索呈现，承接 SOP 检索、案例匹配、复盘视图 | KDS 知识索引、PKC 用户问题、XiaoC 编排请求 | 检索结果、复盘视图、知识解释 | 活跃 | lint/build/test 或 smoke、检索 mock 结果 |
| PKC | 个人知识工作台，承接任务、通知、对话和跨项目状态同步 | Brain 结果、XiaoG 推送、WAES 状态 | 用户任务面板、通知、审批待办、状态同步 | 活跃 | 任务/通知/状态 mock、UI 或接口验证 |
| MMC | 管理配置中心，承接治理模板、配置基线、策略边界 | WAES 规则、GPCF 模板、项目群配置需求 | 模板基线、配置标准、策略边界 | 活跃 | 模板字段校验、配置 validator、runtime tests |
| XiaoC | 蚁后，承接任务拆解、模型路由、Agent 调度和结果汇总 | 用户意图、Brain/KDS 上下文、GPCF 任务队列 | 子任务、模型路由、Agent 调度结果、汇总结论 | 活跃 | 模型路由 dry-run、任务拆解测试、UI/agent smoke |
| XGD | 大象，承接长程分析、重任务、复杂推理和可靠性评估 | XiaoC 分解任务、GFIS/GPC 数据样本、KDS 历史知识 | 深度分析、瓶颈判断、根因分析、风险建议 | 薄激活 | 分析接口契约、样例推理 dry-run、桌面/服务 smoke |
| XiaoG | 蚂蚁执行终端，承接跨系统 API 调用、只读查询和审计写入 | XiaoC 子任务、WAES 授权边界、目标系统 API | GFIS/GPC/KDS 查询结果、PKC 通知、WAES 审计日志 | 活跃 | 只读 API dry-run、WAES 审计写入 mock、设备/脚本入口验证 |
| GPCF | 项目群治理总控，承接统一口径、Loop、evidence、KDS 映射和矩阵收口 | 全项目 evidence、Git/测试结果、KDS 同步状态 | 状态矩阵、L4 评分、项目群 evidence、下一轮计划 | 全激活 | 文档门禁、KDS dry-run、Loop evidence gate |

---

## 5. 跨项目接口与事件契约

L4 第一阶段不追求所有系统都接真实生产 API，但必须形成以下契约：

| 契约 | 生产者 | 消费者 | 第一阶段形态 | 必须 evidence |
|---|---|---|---|---|
| 项目初始化契约 | PVAOS / WAES | GPC / GPCF | 配置 + mock | 项目、租户、组织、角色样本 |
| 组织伙伴契约 | PVAOS | GPC / GFIS / WAES | 对象合同 | 组织、伙伴、权限边界 |
| 平台订单契约 | GPC | GFIS / WAES / PKC | mock/dry-run | 订单字段、状态、样品申请入口、异常入口 |
| 样品确认契约 | GPC / GFIS | WAES / KDS / Brain / PKC | mock/dry-run | 配方研发、样箱打样、样品检测、客户签样、转量产门禁 |
| 工厂订单映射契约 | GFIS | GPC / WAES | 只读样本 | 已签样平台订单到工厂订单映射 |
| 工单状态契约 | GFIS | XiaoG / PKC / Brain | 只读 API 或样本 | 工单状态、负责人、风险 |
| 质量异常契约 | GFIS | WAES / Brain / PKC | 样本 + 复盘 | 异常、CAPA、知识回流 |
| 发货签收契约 | GFIS / GPC | WAES / PKC | mock/dry-run | 发货、POD、争议证据 |
| AI 任务契约 | XiaoC | XGD / XiaoG / Brain | dry-run | 任务拆解、模型路由、结果汇总 |
| 执行审计契约 | XiaoG | WAES / GPCF | mock 或 dry-run | trace_id、授权边界、执行结果 |
| 知识沉淀契约 | WAES / GPCF / GFIS | KDS / Brain | 文档/索引 | evidence 到知识条目的引用回指 |

所有契约必须至少包含：

```text
contract_id
producer
consumer
input_schema
output_schema
allowed_operations
forbidden_operations
verification_command_or_method
evidence_path
rollback_or_degrade_path
```

---

## 6. L4 实施 Round 计划

L4 建议以 12 轮为第一批次，每轮只算实质轮次，不按文档数量计数。

| Round | 主项目 | 协同项目 | 目标 | 实质输出 |
|---|---|---|---|---|
| L4-001 | GPCF | 全项目 | 建立 L4 控制面与项目群 evidence 目录 | L4 状态板、评分矩阵、evidence 模板 |
| L4-002 | MMC | WAES, GPCF | 固化配置模板与策略边界 | 模板字段、validator、runtime tests |
| L4-003 | KDS | GPCF, Brain | 建立知识索引与引用回指契约 | KDS contract dry-run、索引样本 |
| L4-004 | Brain | KDS, PKC | 建立 SOP/案例检索最小路径 | 检索 smoke、UI 或接口验证 |
| L4-005 | PKC | Brain, XiaoG, WAES | 建立任务/通知/状态接收路径 | 任务通知 mock、状态同步 evidence |
| L4-006 | PVAOS | GPC, WAES | 建立组织/伙伴/权限输入基线 | 组织伙伴样本、权限边界 |
| L4-007 | GPC | PVAOS, GFIS, WAES | 建立平台订单、样品申请、客户签样与转量产契约 | 订单/样品/签样 mock、状态映射 |
| L4-008 | GFIS | GPC, WAES, XiaoG | 建立配方研发、样品打样、工厂订单/工单/库存只读样本 | GFIS 样品与工单样本/API dry-run、字段证据 |
| L4-009 | XiaoC | Brain, XGD, XiaoG | 建立任务拆解与模型路由 dry-run | agent routing evidence、子任务列表 |
| L4-010 | XGD | XiaoC, KDS, GFIS | 建立重分析样例 | 分析输入、输出、风险建议 |
| L4-011 | XiaoG | XiaoC, GFIS, WAES, PKC | 建立只读查询与审计写入 mock | API dry-run、WAES 审计记录 |
| L4-012 | GPCF | 全项目 | 项目群最小闭环收口 | L4 评分、阻塞、下一阶段 L5 建议 |

每轮必须输出：

```text
L4 Round ID
涉及项目
业务节点
真实仓路径
代码/配置/测试变更
验证命令或 dry-run 方法
验证结果
evidence 路径
风险与回滚
下一轮输入
```

---

## 7. L4 100 分评分模型

L4 每轮必须按 100 分评分。低于 80 分不得计为 L4 实质轮；低于 70 分必须降级为 L3 补齐轮；低于 60 分必须停止并登记阻塞。

| 指标 | 分值 | 满分判定 | 扣分与归零条件 |
|---|---:|---|---|
| 职责边界准确性 | 15 | 本轮涉及项目的事实主账、协同输入、输出、禁止越界事项全部清楚，且无 GFIS/GPC/MMC/WAES/KDS 边界混淆 | 边界说明不完整扣 5；无法判断主账归属扣 10；把 MMC 写成工厂执行系统、把 WAES 写成业务主账、把 KDS 写成当前业务事实库，或让 AI 项目绕过授权写业务事实，计 0 |
| KDS 关联数据检索质量 | 10 | 形成完整 `kds_retrieval` 清单，覆盖字段语义、对象契约、状态门禁、SOP、证据规则、历史案例、跨项目依赖和 mock 数据口径 | 缺 1-2 类检索项扣 3；只有泛泛引用且未转化为开发数据需求扣 7；未执行 KDS 检索或伪造 KDS 来源，计 0 |
| 真实仓实质变更 | 15 | 在真实项目仓完成代码、配置、契约、测试、mock、dry-run 或 evidence 的实质变更，并说明业务节点价值 | 有实质变更但业务价值或影响范围说明不足扣 5；只有文档或模板更新且未触达真实开发闭环扣 10；只生成轮次说明无可验证产出，计 0 |
| 测试与验证 | 15 | 运行对应测试、lint、校验脚本、dry-run 或 smoke，结果通过且可复现 | 只运行部分验证扣 5；仅人工检查或命令不可复现扣 10；未验证或验证失败仍声称完成，计 0 |
| Evidence 完整性 | 15 | evidence 包含输入、变更、验证命令、结果、KDS 检索摘要、风险、回滚、下一轮建议 | 缺风险、回滚或 KDS 摘要之一扣 5；只有结果描述、无命令和证据链扣 10；无 evidence，计 0 |
| 最小闭环贡献度 | 10 | 明确推进主线业务节点，能接入项目群最小闭环 | 只做支撑工作扣 3；仅准备性工作且闭环贡献弱扣 7；与最小闭环无关，计 0 |
| Git 与工作区可审计性 | 10 | Git 状态清楚，变更范围可解释，无敏感文件，无覆盖用户工作风险 | Git dirty 但范围可识别且已登记扣 3；大量未解释变更扣 7；冲突、敏感文件、TOKEN、不可判断 dirty 状态或覆盖风险，计 0 |
| 下一轮可执行性 | 10 | 下一轮目标、输入、涉及项目、验证方式和停止条件明确 | 缺验证方式或输入清单扣 3；只有泛泛建议扣 7；无下一轮建议或建议无法执行，计 0 |

状态判定：

| 分数 | 状态 | 处理 |
|---:|---|---|
| 90-100 | L4 Ready | 本轮可计为高质量 L4 实质轮；若项目群累计达标，可进入 L5 客户场景验证准备 |
| 80-89 | L4 Conditional | 本轮可计为 L4 实质轮，但必须登记改进项、阻塞项和下一轮补分目标 |
| 70-79 | L3 Repair | 本轮不得计为 L4 实质轮，必须降级补齐 L3 真实项目仓闭环 |
| 60-69 | Blocked | 本轮停止，修复关键缺口后再继续 |
| 0-59 | Invalid | 本轮无效，不得进入下一轮 L4 |

项目群阶段评分：

| 指标 | 分值 | 判定 |
|---|---:|---|
| 12 项目覆盖率 | 15 | 12 个项目均有职责、输入、输出、验证和 evidence |
| P0 主线业务链路贯通度 | 20 | 主线从项目初始化到 GPCF 收口可按样本或 dry-run 复现 |
| 真实仓代码/配置/测试闭环率 | 20 | 项目群实质轮均落到代码、配置、契约、测试、mock、dry-run 或 evidence |
| KDS 检索与知识回指完整度 | 10 | KDS 检索清单、来源文档、字段口径和回指完整 |
| Evidence 与审计完整度 | 15 | 项目级 evidence 与项目群 evidence 可互相引用，WAES 审计路径清楚 |
| 跨项目契约一致性 | 10 | 对象、事件、状态和任务契约一致，无主账冲突 |
| 用户可复现与 L5 准备度 | 10 | 非开发人员可复现 P0 链路，具备客户场景验证输入 |

项目群 L4 出口标准：

| 项目群总分 | 出口判定 | 处理 |
|---:|---|---|
| 90-100 | L5 Ready | 可进入 L5 客户场景验证准备 |
| 80-89 | L4 Conditional | 可继续补齐短板后进入 L5 预备 |
| 70-79 | L4 Repair | 继续 L4 补齐，不得进入 L5 |
| 0-69 | Return to L3/L3.5 | 退回补齐基础闭环或集成闭环 |

每轮输出必须给出 100 分评分明细、扣分原因、是否计为 L4 实质轮、项目群阶段累计评分和下一轮补分目标。

---

## 8. 硬停止与降级规则

出现以下情况必须停止 L4 升级：

1. 任一参与项目真实仓状态不可判断。
2. 任一项目缺少 L3 代码/配置/测试/evidence 基础闭环。
3. 跨项目接口事实不明，且无法用契约或 mock 降级。
4. 测试失败且无法局部修复。
5. 发现 Git 冲突、敏感文件、TOKEN、密钥或权限风险。
6. 触及生产写入、真实部署、真实权限变更。
7. 需要人工业务判断。
8. 文档与真实仓事实严重冲突。

降级规则：

| 情况 | 最高状态 |
|---|---|
| 只有文档，没有真实仓任务 | L2 |
| 有真实仓任务，但无测试/验证 | L2.5 |
| 有测试，但无 evidence | L3 Partial |
| 单项目通过，但无跨项目契约 | L3 Ready，不可升级 L4 |
| 跨项目 mock 通过，但无真实仓变更 | L3.5 Integration Partial |
| 12 项目有缺席项目 | L4 Blocked |

---

## 9. Evidence 结构

L4 evidence 必须分两层：

1. 项目级 evidence：保存在各真实项目仓或 GPCF `docs/harness/{Project}/` 映射目录。
2. 项目群 evidence：保存在 GPCF `docs/harness/loops/` 和 `docs/harness/evidence/`。

推荐结构：

```text
docs/harness/loops/loop-round-GPCF-L4-001.md
docs/harness/loops/loop-round-GPCF-L4-002.md
docs/harness/evidence/gpcf_l4_minimum_closed_loop_evidence.json
docs/harness/{Project}/l4-evidence-index.md
```

项目级 evidence 最少字段：

```yaml
round_id:
project:
repo_path:
business_node:
input:
output:
changed_files:
verification:
verification_result:
upstream_dependencies:
downstream_dependencies:
risk:
rollback:
next_input:
```

---

## 10. 第一阶段实施顺序

第一阶段不追求所有项目等深实现，而是按“先控制、再知识、再业务、再智能执行、最后收口”的顺序推进。

1. GPCF 建立 L4 控制面、评分矩阵和 evidence 总入口。
2. MMC 固化模板、配置和策略边界，减少后续项目各自发散。
3. KDS 建立知识索引、文档引用和 evidence 回指。
4. Brain / PKC 建立知识消费与用户任务承接。
5. PVAOS / GPC / GFIS 建立组织、订单、样品确认、转量产、工厂执行、发货签收主线。
6. WAES 建立状态、证据、审计和越权阻断。
7. XiaoC / XGD / XiaoG 建立 AI 编排、重分析和执行终端 dry-run。
8. GPCF 收口 L4 评分、阻塞和 L5 准备项。

---

## 11. L4 启动提示词

```text
启动 GlobalCloud 项目群 L4 最小闭环实施。

目标：
在所有项目达到或补齐 L3 真实项目仓代码/配置/测试/evidence 闭环基础上，推进项目群 L4 最小闭环。

硬要求：
12 个项目必须全部纳入闭环。每个项目都必须有职责、输入、输出、验证方式和 evidence。成熟项目真实运行；低成熟项目至少以契约、mock、dry-run 或占位验证参与，但不得从闭环中消失。

执行依据：
1. 01-architecture/GlobalCloud项目群最小闭环L4实施方案.md
2. 01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md
3. 02-governance/GlobalCloud绿色供应链体系模块实施分级判定表.md
4. 02-governance/loop/LOOP_L4_AUTONOMOUS_OPERATIONS.md
5. 09-status/globalcloud-l3-admission-matrix.md
6. 03-data-ai-knowledge/GlobalCloud Loop开发KDS关联数据检索机制.md

执行规则：
- 每轮必须落到真实仓代码、配置、测试、契约、脚本、dry-run 或 evidence。
- 每轮开发前必须执行 KDS 关联数据检索，形成 `kds_retrieval` 清单。
- KDS 检索内容必须覆盖对象字段、状态门禁、SOP、证据规则、历史案例、跨项目依赖和 mock 数据口径。
- KDS 提供开发语义和受控口径，不替代 GPC/GFIS/WAES/PVAOS 的业务事实。
- 若 KDS 检索缺失关键口径，本轮不得伪造字段或状态，必须登记 `unresolved_questions`。
- 纯文档轮不得计为 L4 实质轮。
- 每轮必须输出项目级 evidence 和项目群 evidence。
- 每轮 evidence 必须包含 KDS 检索结果、使用了哪些来源文档、转化出的开发数据需求和未解决问题。
- 每轮必须给出 100 分评分明细、扣分原因、是否计为 L4 实质轮、项目群阶段累计评分和下一轮补分目标。
- 低于 80 分不得计为 L4 实质轮；低于 70 分必须降级为 L3 补齐轮；低于 60 分必须停止并登记阻塞。
- 不得自动真实写入生产系统、真实 TOKEN、权限系统或部署环境。
- 不得自动标记 accepted 或 integrated。
- 发现任一项目缺少 L3 基础闭环时，先降级回 L3 补齐。

第一批 12 轮：
L4-001 GPCF 控制面与 evidence 总入口
L4-002 MMC 配置模板与策略边界
L4-003 KDS 知识索引与引用回指
L4-004 Brain SOP/案例检索路径
L4-005 PKC 任务/通知/状态接收路径
L4-006 PVAOS 组织/伙伴/权限输入基线
L4-007 GPC 平台订单、样品确认、签收契约
L4-008 GFIS 配方研发、样品打样、工厂订单/工单/库存只读样本
L4-009 XiaoC 任务拆解与模型路由
L4-010 XGD 重分析样例
L4-011 XiaoG 只读查询与审计写入 mock
L4-012 GPCF 项目群最小闭环收口

最终交付：
KDS 关联数据检索清单、L4 评分矩阵、跨项目契约清单、项目级 evidence、项目群 evidence、阻塞项、回滚方案、L5 客户场景验证建议。
```

---

## 12. 下一阶段出口

L4 完成后不直接进入生产化，应进入 L5 客户场景验证准备。L5 的最小入口条件：

1. L4 分数不低于 90，或 L4 Conditional 阻塞项均有责任人和期限。
2. 至少一条 P0 业务链路可由非开发人员复现。
3. 有明确客户角色、工厂角色或运营角色的使用场景。
4. 有客户满意度或用户可用性代理指标。
5. 有真实权限、安全、审计、回滚和数据保护方案。

L5 的目标是验证“用户是否真的能用”，不是继续证明“系统之间是否能接”。
