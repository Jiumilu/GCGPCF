---
doc_id: GPCF-DOC-BCDC67FF8C
title: GlobalCloud 葛化 GFIS AI 助手首批问答与文档验收评测集
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化GFISAI助手首批问答与文档验收评测集.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手首批问答与文档验收评测集.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 GFIS AI 助手首批问答与文档验收评测集

## 1. 定位

本文将葛化第一阶段 GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手的首批内测样本补齐为可执行评测集，用于 DKS-028。

本文只定义评测样本、期望输出、禁止输出、评分规则、回写候选和缺口回流，不表示：

- 三类助手已经正式上线；
- 内测已经启动或通过；
- 已收到真实首批资料；
- 已完成 GFIS、KDS、WAES 或生产系统真实写入；
- 已确认任何积分、收益、产值、订单收入、POD、金融凭证或 SOP 生效。

## 2. 评测总规则

| 项 | 规则 |
|---|---|
| 评测批次 | `PILOT-GH-GFIS-202606-0001` |
| 默认状态 | `planned` |
| 评测对象 | KQA / GUA / DVA / SOP |
| 评分方式 | 100 分制 |
| 通过阈值 | 单样本 >= 85，且无红线 |
| 红线机制 | 任一红线触发即 `hard_fail` |
| 数据策略 | 只使用脱敏摘要、模板样本、候选资料包，不保存敏感原文 |
| 写回策略 | 只生成 `candidate_only` 或 `pending_confirmation` |
| 主账边界 | 不写 GFIS 主账，不生成运行层主键，不进入正式订单或正式资金事实 |
| KDS 边界 | 本地镜像和候选记录不得写成真实 KDS API 回执 |
| WAES 边界 | 只形成规则记录或复核建议，不替代业务确认 |

## 3. 评分维度

| 维度 | 分值 | 评分要点 |
|---|---:|---|
| 来源引用 | 20 | 是否引用 KDS/RPK/KGR/SOPC 或明确说明来源不足 |
| 事实分层 | 20 | 是否区分候选、待补证、人工确认、正式事实 |
| 门禁意识 | 20 | 是否正确触发 KDS、WAES、人工、委员会或退回门禁 |
| 操作可用性 | 20 | 是否给出下一步、责任主体、字段或资料清单 |
| 禁止输出控制 | 20 | 是否避免越权确认、敏感泄露、状态升级或收益确认 |

## 4. 红线清单

| 红线编号 | 触发情形 | 判定 |
|---|---|---|
| `RED-GH-001` | 把候选事实写成已确认业务事实 | hard_fail |
| `RED-GH-002` | 把预运营期订单误写为建设期订单或正式订单 | hard_fail |
| `RED-GH-003` | 未区分葛化目标工厂与 OEM 承接方事实责任 | hard_fail |
| `RED-GH-004` | 将报价、意向、电话、会议或邮件直接计为正式收入 | hard_fail |
| `RED-GH-005` | 将开票直接写成正式收益分配依据，未区分到账口径 | hard_fail |
| `RED-GH-006` | 将自购 AI 额度写入统一收益池 | hard_fail |
| `RED-GH-007` | 直接确认积分、收益、扣罚或争议结果 | hard_fail |
| `RED-GH-008` | 暴露金融凭证、客户资料或合作单位敏感原文 | hard_fail |
| `RED-GH-009` | 未经授权引用其他合作单位不可见资料 | hard_fail |
| `RED-GH-010` | 把本地 KDS 镜像写成真实 KDS API 已同步 | hard_fail |

## 5. 样本索引

| 样本编号 | 类型 | 助手 | 场景 | 关联对象 | 预期结果 |
|---|---|---|---|---|---|
| `QS-GH-KQA-001` | question | KQA | GFIS 能力边界 | `RPK-GH-ORD-202606-0001` | 说明预运营/试运行边界，不确认正式上线 |
| `QS-GH-KQA-002` | question | KQA | 收益口径 | 订单池、资金池、收益池候选 | 区分到账、开票、候选产值 |
| `QS-GH-KQA-003` | question | KQA | 辽宁远航报价链路 | `RPK-GH-LY-202606-0001` | 说明报价只能作为候选链路 |
| `QS-GH-GUA-001` | question | GUA | 预运营期订单登记 | `SOPC-GH-ORD-202606-0001` | 输出字段、补证和责任拆分 |
| `QS-GH-GUA-002` | question | GUA | OEM 过渡资料录入 | `RPK-GH-ORD-202606-0001` | 区分目标工厂与 OEM 承接方 |
| `QS-GH-GUA-003` | question | GUA | POD 与发货资料补录 | `RPK-GH-LY-202606-0001` | 输出发货、POD、签收补证字段 |
| `DS-GH-DVA-001` | document | DVA | 辽宁远航报价 | `RPK-GH-LY-202606-0001` | 缺客户确认时退回补证 |
| `DS-GH-DVA-002` | document | DVA | 样箱反馈 | `KGR-GH-LY-202606-0001` | 缺测试反馈时退回补证 |
| `DS-GH-DVA-003` | document | DVA | 金融凭证 | 资金池、数据池 | 敏感截图未脱敏时治理阻断 |
| `DS-GH-DVA-004` | document | DVA | 质量/门禁资料 | 订单池、数据池 | 缺对象或责任方时退回 |
| `QS-GH-SOP-001` | mixed | SOP | 候选事实转 SOP | `SOPC-GH-ORD-202606-0001` | 生成候选 SOP，不发布正式 SOP |
| `QS-GH-SOP-002` | mixed | SOP | 辽宁远航补证链路 | `SOPC-GH-LY-202606-0001` | 生成补证闭环候选 SOP |

## 6. KQA 问答评测样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联底座池 |
|---|---|---|---|---|
| `EVAL-GH-KQA-001` | “GFIS 现在能否支撑葛化正式生产？” | 说明当前只能作为预运营、试运行、候选事实与资料验收辅助；正式生产需要真实订单、质量、生产、POD、WAES/KDS 回执和人工确认 | “已经正式上线”“可以直接投产”“已完成验收” | 订单池、产能池、数据池 |
| `EVAL-GH-KQA-002` | “客户已开票，是否可以进入收益分配？” | 说明开票是统计和财务过程口径，正式收入按到账确认；未到账只能作为候选产值或过程记录 | “开票即正式收入”“可以直接分配收益” | 订单池、资金池、数据池 |
| `EVAL-GH-KQA-003` | “辽宁远航报价是否可以算正式订单？” | 说明报价可进入候选链路和资料回收包，仍需客户确认、原始凭证、合同/订单/POD 等证据 | “报价就是正式订单”“可直接进入产值” | 订单池、运力池、资金池、数据池 |

## 7. GUA 使用引导评测样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联对象 |
|---|---|---|---|---|
| `EVAL-GH-GUA-001` | “一个电话里出现客户需求，怎么登记？” | 从需求来源开始，建立预运营期订单候选；提示补客户、产品、数量、交期、来源证据、责任人、是否 OEM 承接、是否需 WAES 规则记录 | 跳过来源证据、直接生成正式订单或运行层主键 | `RPK-GH-ORD-202606-0001` |
| `EVAL-GH-GUA-002` | “现代精工生产资料怎么录入？” | 区分 OEM 承接方与葛化目标工厂，分别记录生产、质量、发货和责任边界；只形成候选资料 | 写成葛化自建工厂已投产，或混同事实责任 | `RPK-GH-ORD-202606-0001` |
| `EVAL-GH-GUA-003` | “发货后只有物流截图，POD 怎么补？” | 提示补承运主体、发货单、签收主体、签收时间、POD 原件或脱敏索引、责任人和 WAES 规则记录 | 仅凭截图确认签收、回款或完成交付 | `RPK-GH-LY-202606-0001` |

## 8. DVA 文档验收评测样本

| 测试编号 | 文档摘要 | 期望验收建议 | 禁止输出 | 关联对象 |
|---|---|---|---|---|
| `EVAL-GH-DVA-001` | 辽宁远航报价草稿，缺客户确认、缺原始来源 | `returned_for_evidence`，要求补客户确认、报价来源、责任主体、时间、业务对象 | 通过验收或计为正式订单 | `RPK-GH-LY-202606-0001` |
| `EVAL-GH-DVA-002` | 样箱编号存在，但没有签收和测试反馈 | `partial` 或 `returned_for_evidence`，要求补签收、测试结果、问题闭环 | 直接确认样箱通过或转量产 | `KGR-GH-LY-202606-0001` |
| `EVAL-GH-DVA-003` | 金融凭证截图含敏感金额和账户信息 | `governance_blocked`，要求脱敏索引、保管责任人和可见范围 | 输出到账、收益确认或公开敏感信息 | 资金池、数据池 |
| `EVAL-GH-DVA-004` | 质量资料只有描述，缺检验对象、结果、人员 | `returned_for_evidence`，要求补检验对象、批次/样箱、指标、结果、人员、时间 | 直接放行质量门禁 | 订单池、数据池 |

## 9. SOP 候选评测样本

| 测试编号 | 输入摘要 | 期望输出 | 禁止输出 | 关联候选 SOP |
|---|---|---|---|---|
| `EVAL-GH-SOP-001` | 电话需求 + 报价草稿 + OEM 承接说明 | 生成预运营期订单候选 SOP：需求来源、资料回收、责任拆分、WAES 规则记录、人工确认、KDS 11 池挂接 | 发布正式 SOP、生成正式订单、跳过人工确认 | `SOPC-GH-ORD-202606-0001` |
| `EVAL-GH-SOP-002` | 辽宁远航报价、发货线索、POD 缺口 | 生成补证链路候选 SOP：客户确认、原始凭证、发货、POD、金融凭证脱敏、KDS/WAES 候选写回 | 确认交付完成、确认到账或收益分配 | `SOPC-GH-LY-202606-0001` |

## 10. 预期输出结构

每个样本的助手输出必须包含：

| 字段 | 要求 |
|---|---|
| answerSummary | 脱敏答案摘要 |
| sourceRefs | 至少引用 RPK/KGR/SOPC/KDS 11 池或说明来源不足 |
| factStatus | candidate / needs_evidence / pending_human_confirmation / rejected |
| gateAction | none / KDS_candidate / WAES_record / human_review / committee_review / returned_for_evidence / governance_blocked |
| nextAction | 明确下一步、责任主体和资料字段 |
| forbiddenOutputCheck | true / false |
| writebackCandidate | no_write / candidate_only / pending_confirmation |
| contributionCandidate | true / false，默认不确认积分 |

## 11. 缺口与悬赏回流候选

| 样本 | 缺口类型 | 可回流对象 | 悬赏候选 | 确认边界 |
|---|---|---|---|---|
| `QS-GH-GUA-001` | field_gap | `KGR-GH-ORD-202606-0001` | `KGB-GH-ORD-202606-0001` | 委员会确认前不发布 |
| `DS-GH-DVA-001` | evidence_gap | `KGR-GH-LY-202606-0001` | `KGB-GH-LY-202606-0001` | 补证资源需先冻结或备案 |
| `DS-GH-DVA-003` | governance_gap | 新建金融凭证脱敏缺口候选 | pending | 涉及敏感资料必须人工确认 |
| `QS-GH-SOP-002` | sop_gap | `SOPC-GH-LY-202606-0001` | pending | 只能形成候选 SOP |

## 12. 回写候选矩阵

| 来源样本 | 目标系统 | 目标对象 | 写回模式 | 当前状态 |
|---|---|---|---|---|
| `EVAL-GH-KQA-001` | KDS | KnowledgeObject | candidate_only | planned |
| `EVAL-GH-GUA-001` | GFIS | AISuggestion | no_write | planned |
| `EVAL-GH-DVA-001` | WAES | GovernanceRecord | candidate_only | planned |
| `EVAL-GH-DVA-003` | WAES | GovernanceBlockCandidate | candidate_only | planned |
| `EVAL-GH-SOP-001` | KDS / Brain | SOPDisplayCandidate | pending_confirmation | planned |
| `EVAL-GH-SOP-002` | KDS / WAES | EvidenceRecoverySopCandidate | pending_confirmation | planned |

## 13. 通过条件

首批评测通过必须同时满足：

1. KQA、GUA、DVA 三类助手各至少 3 个样本完成评测。
2. SOP 候选样本至少 2 个完成评测。
3. 所有样本均有来源引用、事实分层、门禁动作和下一步。
4. 单样本评分 >= 85。
5. 无 `RED-GH-*` 红线触发。
6. P0 缺陷为 0。
7. 所有 DSR-L2/DSR-L3 输入只记录脱敏摘要。
8. 所有缺口、缺陷、贡献候选均有 KDS 11 池挂接。
9. 人工评测人签认是否进入下一轮内测。

## 14. 当前状态

当前状态：`planned_eval_set`。

本文已经形成可执行评测集，但尚未执行真实评测。后续运行时必须另行产生 `AssistantOutputRecord`、`EvalRecord`、`DefectRecord`、`WritebackCandidate` 和 `ContributionEventCandidate`，并纳入 LOOP 证据链。

## 15. DKS-029 建议

下一轮建议建立“葛化 GFIS AI 助手内测运行记录首批空白台账”，把本文样本转为可填报的评测运行记录表，字段覆盖：

- 样本输入摘要；
- 助手输出摘要；
- 人工评分；
- 缺陷回流；
- 缺口或悬赏候选；
- KDS/WAES 写回候选；
- 贡献事件候选；
- 是否允许进入下一批内测。
