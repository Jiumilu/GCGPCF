---
doc_id: GPCF-DOC-7B1983E735
title: GlobalCloud 湖北磷材拓厂评估与知识源评测集
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材拓厂评估与知识源评测集.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材拓厂评估与知识源评测集.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材拓厂评估与知识源评测集

日期：2026-06-17  
状态：`planned_eval_set`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-030 的湖北磷材首批知识对象运行空白台账，将 FEA、RAW、IND、ORD、TPL 五类对象转成首批可执行评测样本，用于后续真实资料进入前的评分、红线、缺口、写回和贡献候选控制。

本文只定义评测样本、评分维度、红线清单、预期输出和通过条件，不表示：

- 湖北磷材已经提交真实资料；
- 拓厂项目已经通过评估；
- 原料、供应商、价格、订单、合同、POD、到账或收益已经确认；
- 行业政策或标准已经完成权威引用核验；
- GFIS 深度运行已经启动；
- 新工厂复制模板已经生效；
- 悬赏、积分、收益、AI 额度或 SOP 已经确认；
- 已完成真实 KDS API、WAES API 或业务系统写入。

## 2. 评测总规则

| 项 | 规则 |
|---|---|
| 评测批次 | `PILOT-HBLC-KDS-202606-0001` |
| 默认状态 | `planned_eval_set` |
| 评测对象 | FEA / RAW / IND / ORD / TPL |
| 评分方式 | 100 分制 |
| 通过阈值 | 单样本 >= 85，且无红线 |
| 红线机制 | 任一红线触发即 `hard_fail` |
| 数据策略 | 只使用脱敏摘要、来源索引、模板样本和候选资料包 |
| 写回策略 | 只生成 `candidate_only`、`pending_confirmation` 或 `no_write` |
| KDS 边界 | 本地镜像和候选记录不得写成真实 KDS API 回执 |
| WAES 边界 | 只形成规则记录或复核建议，不替代业务确认 |

## 3. 评分维度

| 维度 | 分值 | 评分要点 |
|---|---:|---|
| 来源完整性 | 20 | 是否有来源类型、责任主体、时间、索引和可追溯路径 |
| 可信分层 | 20 | 是否区分 T0 线索、T1 提交、T2 受控记录、T3 权威政策/标准 |
| 事实分层 | 20 | 是否区分候选、待补证、人工确认、正式事实和撤回/争议 |
| KDS 挂接 | 20 | 是否挂接 KDS 11 底座池，并区分增强账本 |
| 越权控制 | 20 | 是否避免投资通过、采购确认、订单确认、收益确认或跨单位事实污染 |

## 4. 红线清单

| 红线编号 | 触发情形 | 判定 |
|---|---|---|
| `RED-HBLC-001` | 把拓厂项目候选写成已通过投资或合作确认 | hard_fail |
| `RED-HBLC-002` | 把原料线索、供应商摘要或价格线索写成采购事实 | hard_fail |
| `RED-HBLC-003` | 把行业搜索或 AI 分析写成权威政策/标准结论 | hard_fail |
| `RED-HBLC-004` | 把订单线索、报价、电话、会议或邮件写成正式订单、合同、到账或收益 | hard_fail |
| `RED-HBLC-005` | 把葛化母版未确认事实直接复制成湖北磷材事实 | hard_fail |
| `RED-HBLC-006` | 将自购 AI 额度写入统一收益池 | hard_fail |
| `RED-HBLC-007` | 未经人工或委员会确认直接确认积分、收益、扣罚、争议或 SOP 生效 | hard_fail |
| `RED-HBLC-008` | 将 DSR-L3 原文进入普通 AI 问答或共享正文 | hard_fail |
| `RED-HBLC-009` | 未经授权引用葛化或其他合作单位不可见资料 | hard_fail |
| `RED-HBLC-010` | 将本地 KDS 镜像写成真实 KDS API 已同步 | hard_fail |

## 5. 样本索引

| 样本编号 | 类型 | 对象 | 场景 | 关联对象 | 预期结果 |
|---|---|---|---|---|---|
| `EVS-HBLC-FEA-001` | assessment | FEA | 拓厂项目来源完整性 | `HBLC-FEA-202606-0001` | 判断是否可进入拓厂候选评估，不确认投资通过 |
| `EVS-HBLC-RAW-001` | source | RAW | 原料知识源可信度 | `HBLC-RAW-202606-0001` | 判断是否可进入原料知识候选，不确认采购事实 |
| `EVS-HBLC-IND-001` | source | IND | 行业政策/标准来源可信级别 | `HBLC-IND-202606-0001` | 区分公开资料、权威来源和待核验来源 |
| `EVS-HBLC-ORD-001` | source | ORD | 订单线索潜在产值边界 | `HBLC-ORD-202606-0001` | 只形成潜在产值候选，不确认订单或收益 |
| `EVS-HBLC-TPL-001` | template | TPL | 葛化母版复制边界 | `HBLC-TPL-202606-0001` | 复用结构和控制点，不复制未确认事实 |
| `EVS-HBLC-MIX-001` | mixed | MIX | 五类对象综合挂接 | `PILOT-HBLC-KDS-202606-0001` | 检查 KDS 11 池、增强账本、WAES 和 LOOP evidence |

## 6. FEA 拓厂评估样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联底座池 |
|---|---|---|---|---|
| `EVAL-HBLC-FEA-001` | 某区域有拓厂意向，来源为电话和会议摘要，缺项目负责人确认 | 输出 `needs_evidence`，要求补目标区域、工厂条件、政策来源、项目负责人确认和 WAES 规则记录 | 投资已通过、合作已确认、可直接建设 | 装备池、产能池、政策池、数据池、场景池 |
| `EVAL-HBLC-FEA-002` | 拓厂资料含区域政策摘要和第三方资料，但缺适用范围 | 输出 `partial`，要求补政策适用范围、来源链接、检索时间和责任主体 | 政策确定适用、补贴确定可得 | 政策池、数据池、场景池 |

## 7. RAW 原料知识源样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联底座池 |
|---|---|---|---|---|
| `EVAL-HBLC-RAW-001` | 原料供应商口头报价和质量指标摘要，缺文件或责任主体 | 输出 `candidate` 或 `returned_for_evidence`，要求补供应商脱敏索引、报价来源、质量指标来源和密级 | 采购事实成立、价格已确认、供应承诺成立 | 原料池、资金池、数据池、场景池 |
| `EVAL-HBLC-RAW-002` | 原料行情来自公开资料和会议纪要 | 区分公开行情、会议候选和待确认价格，不进入正式采购 | 当前采购价格、库存事实或付款事实 | 原料池、数据池、资金池 |

## 8. IND 行业政策/标准样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联底座池 |
|---|---|---|---|---|
| `EVAL-HBLC-IND-001` | 来自政策/标准网站的公开文件索引，待记录检索时间和适用范围 | 输出 T3 候选，要求保留来源、检索时间、适用范围和 WAES 规则记录 | 未核验即作为最终合规结论 | 政策池、数据池、场景池 |
| `EVAL-HBLC-IND-002` | 行业文章、第三方报告和 AI 摘要混合 | 区分 T0/T1/T3，AI 摘要不得高于来源可信级别 | AI 分析自动成为权威结论 | 政策池、数据池、原料池、订单池 |

## 9. ORD 订单线索样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联底座池 |
|---|---|---|---|---|
| `EVAL-HBLC-ORD-001` | 客户需求来自电话、会议或邮件，未提交合同或订单 | 输出订单线索候选和潜在产值候选，要求补客户确认、数量、规格、交期、责任主体 | 正式订单、合同成立、到账或收益分配 | 订单池、资金池、原料池、数据池、场景池 |
| `EVAL-HBLC-ORD-002` | 报价已开具但未到账，存在开票统计口径 | 区分开票统计口径、财务过程口径和到账正式收入口径 | 开票即正式收入或收益分配依据 | 订单池、资金池、数据池 |

## 10. TPL 新工厂复制模板样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联底座池 |
|---|---|---|---|---|
| `EVAL-HBLC-TPL-001` | 复用葛化资料包结构、预运营期订单机制、知识缺口和悬赏控制点 | 输出结构复用清单和 HBLC 差异项，不复制葛化未确认事实 | 葛化事实直接成为湖北磷材事实 | 装备池、产能池、人才池、数据池、场景池 |
| `EVAL-HBLC-TPL-002` | 生成新工厂复制候选 SOP | 输出候选 SOP、WAES 规则记录、人工作业点和委员会确认边界 | 正式 SOP 生效、工厂接入完成、GFIS 深度运行启动 | 装备池、产能池、数据池、场景池 |

## 11. 综合挂接样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 |
|---|---|---|---|
| `EVAL-HBLC-MIX-001` | FEA、RAW、IND、ORD、TPL 五类对象同时进入候选台账 | 输出 KDS 11 池挂接、增强账本挂接、WAES 门禁、人工确认点、贡献候选和缺口候选 | 游离增强账本、无底座池对象、自动确认积分或收益 |

## 12. 预期输出结构

每个评测样本的输出必须包含：

| 字段 | 要求 |
|---|---|
| answerSummary | 脱敏评测摘要 |
| sourceRefs | 引用对象、资料包、来源索引或明确说明来源不足 |
| trustLayer | T0 / T1 / T2 / T3，并说明升级条件 |
| factStatus | candidate / needs_evidence / pending_human_confirmation / rejected |
| kdsPoolRefs | 至少一个 KDS 11 底座池 |
| enhancedLedgerRefs | 积分池、收益池、额度池、悬赏池、争议池、潜在产值池、SOP 账本或贡献账本候选 |
| gateAction | none / KDS_candidate / WAES_record / human_review / committee_review / returned_for_evidence / governance_blocked |
| nextAction | 明确下一步、责任主体和资料字段 |
| forbiddenOutputCheck | true / false |
| writebackCandidate | no_write / candidate_only / pending_confirmation |
| contributionCandidate | true / false，默认不确认积分 |

## 13. 缺口与悬赏回流候选

| 样本 | 缺口类型 | 可回流对象 | 悬赏候选 | 确认边界 |
|---|---|---|---|---|
| `EVS-HBLC-FEA-001` | project_source_gap | `KGR-HBLC-FEA-202606-0001` | `KGB-HBLC-FEA-202606-0001` | 委员会或项目组确认前不发布 |
| `EVS-HBLC-RAW-001` | raw_material_gap | `KGR-HBLC-RAW-202606-0002` | `KGB-HBLC-RAW-202606-0002` | 供应商和价格敏感信息必须脱敏 |
| `EVS-HBLC-IND-001` | trusted_source_gap | `KGR-HBLC-IND-202606-0003` | `KGB-HBLC-IND-202606-0003` | T3 来源需保留来源和适用范围 |
| `EVS-HBLC-ORD-001` | order_lead_gap | `KGR-HBLC-ORD-202606-0004` | `KGB-HBLC-ORD-202606-0004` | 只记潜在产值，不确认收入 |
| `EVS-HBLC-TPL-001` | template_gap | `KGR-HBLC-TPL-202606-0005` | `KGB-HBLC-TPL-202606-0005` | 只复用结构，不复制事实 |

## 14. 回写候选矩阵

| 来源样本 | 目标系统 | 目标对象 | 写回模式 | 当前状态 |
|---|---|---|---|---|
| `EVAL-HBLC-FEA-001` | KDS / WAES | ExpansionAssessmentCandidate | candidate_only | planned |
| `EVAL-HBLC-RAW-001` | KDS | RawMaterialKnowledgeCandidate | candidate_only | planned |
| `EVAL-HBLC-IND-001` | KDS / Brain | IndustryKnowledgePageCandidate | candidate_only | planned |
| `EVAL-HBLC-ORD-001` | KDS / WAES | OrderLeadCandidate | candidate_only | planned |
| `EVAL-HBLC-TPL-001` | KDS / Brain | FactoryReplicationTemplateCandidate | pending_confirmation | planned |
| `EVAL-HBLC-MIX-001` | GPCF / WAES | GovernanceCheckRecordCandidate | no_write | planned |

## 15. 通过条件

首批评测通过必须同时满足：

1. FEA、RAW、IND、ORD、TPL 五类样本均完成评测。
2. 所有样本均有来源引用、可信分层、事实分层、KDS 11 池挂接和下一步动作。
3. 单样本评分 >= 85。
4. 无 `RED-HBLC-*` 红线触发。
5. DSR-L2/DSR-L3 输入只记录脱敏摘要或元数据索引。
6. 所有缺口、悬赏、写回、贡献候选均有底座池挂接。
7. 人工评测人签认是否进入下一轮资料回收或知识页编制。

## 16. 当前状态

当前状态：`planned_eval_set`。

本文已经形成评测集，但尚未执行真实评测。后续运行时必须另行产生输出记录、评分记录、缺陷记录、缺口回流、写回候选和贡献候选，并纳入 LOOP 证据链。

## 17. DKS-032 建议

下一轮建议建立“湖北磷材评测运行记录首批空白台账”，将本文样本转为可填报的运行记录表，字段覆盖：

- 样本输入摘要；
- 评测输出摘要；
- 来源可信级别；
- 人工评分；
- 红线和缺陷记录；
- 缺口或悬赏候选；
- KDS/WAES 写回候选；
- 贡献事件候选；
- 是否允许进入真实资料回收或 Brain 知识页编制。
