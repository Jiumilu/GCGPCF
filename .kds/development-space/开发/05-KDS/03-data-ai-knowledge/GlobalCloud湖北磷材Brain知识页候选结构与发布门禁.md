---
doc_id: GPCF-DOC-59CCD41F2D
title: GlobalCloud 湖北磷材 Brain 知识页候选结构与发布门禁
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选结构与发布门禁.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选结构与发布门禁.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材 Brain 知识页候选结构与发布门禁

日期：2026-06-17  
状态：`planned_brain_page_gate`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-033 的湖北磷材真实资料接收任务包与人工评测演练，定义湖北磷材第一阶段 Brain 知识页候选结构、页面块标准、权限过滤、发布前门禁、WAES 放行边界和撤回规则。

本文只建立候选结构和发布门禁，不表示：

- 湖北磷材已经提交真实资料；
- DSR-L2 / DSR-L3 原文已经进入系统；
- Brain 知识页已经正式发布；
- KDS、WAES、GFIS、GPC 或其他业务系统已经发生真实写入；
- 拓厂、原料、行业、订单或模板事实已经被正式确认；
- 积分、收益、额度、悬赏、争议或 SOP 已经生效。

## 2. Brain 知识页总规则

| 项 | 规则 |
|---|---|
| 默认状态 | `planned_page_candidate` |
| 页面来源 | DKS-033 的 `BKC-HBLC-*` 知识页候选 |
| 允许输入 | 脱敏摘要、来源索引、WAES 规则候选、KDS 对象编号、人工评测候选结果 |
| 禁止输入 | 未授权 DSR-L3 原文、客户订单原文、合同原文、供应商报价原文、个人敏感信息、跨单位不可见事实 |
| 表达原则 | Brain 只做知识表达、检索和协同入口，不替代 KDS 事实主账 |
| 可信原则 | 页面必须展示来源层级、事实状态、人工评测状态和发布门禁状态 |
| 权限原则 | 页面内容按单位、项目、角色、密级和邀请关系过滤 |
| 发布原则 | 未通过发布门禁前只能保持候选态或内部草案态 |
| 撤回原则 | 来源、权限、评分、红线、争议或事实状态变化时必须可撤回、可降级、可追溯 |

## 3. KnowledgePageCandidateStructure 台账

| brainPageId | linkedBrainCandidateId | pageType | pagePurpose | requiredBlocks | kdsPoolRefs | enhancedLedgerRefs | defaultStatus |
|---|---|---|---|---|---|---|---|
| `BKP-HBLC-FEA-202606-0001` | `BKC-HBLC-FEA-202606-0001` | 拓厂项目知识页候选 | 支撑湖北磷材拓厂项目评估、缺口识别和新工厂复制模板输入 | 来源摘要、区域/政策索引、条件评分、缺口、下一步 | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | 悬赏池 / 贡献账本 / SOP 账本 | planned |
| `BKP-HBLC-RAW-202606-0001` | `BKC-HBLC-RAW-202606-0001` | 原料知识页候选 | 支撑原料类别、质量指标、供应链来源和采购边界识别 | 原料类别、质量指标摘要、来源索引、采购边界、缺口 | 原料池 / 数据池 / 资金池 / 场景池 | 悬赏池 / 贡献账本 / 潜在产值池 | planned |
| `BKP-HBLC-IND-202606-0001` | `BKC-HBLC-IND-202606-0001` | 行业资料页候选 | 支撑政策、标准、行业资料和可信来源分层 | 权威来源、检索时间、适用范围、可信级别、引用边界 | 政策池 / 数据池 / 场景池 | 贡献账本 / SOP 账本 | planned |
| `BKP-HBLC-ORD-202606-0001` | `BKC-HBLC-ORD-202606-0001` | 订单线索页候选 | 支撑预运营期订单线索、潜在产值、产能调度和补证动作 | 客户匿名编号、需求摘要、规格区间、潜在产值、补证清单 | 订单池 / 产能池 / 运力池 / 资金池 / 数据池 | 潜在产值池 / 悬赏池 / 贡献账本 | planned |
| `BKP-HBLC-TPL-202606-0001` | `BKC-HBLC-TPL-202606-0001` | 新工厂复制模板页候选 | 支撑以葛化为标准母版的新工厂复制模板、差异项和候选 SOP | 母版结构、湖北磷材差异项、候选 SOP、控制点、门禁 | 装备池 / 产能池 / 人才池 / 数据池 / 场景池 | SOP 账本 / 贡献账本 / 争议池 | planned |
| `BKP-HBLC-MIX-202606-0001` | `RTP-HBLC-MIX-202606-0001` | 治理映射页候选 | 支撑 KDS 11 池、增强账本、LOOP evidence 和 WAES 规则的统一索引 | KDS 池挂接、增强账本、门禁状态、证据链、缺口 | 订单池 / 运力池 / 产能池 / 资金池 / 政策池 / 装备池 / 数据池 / 能源池 / 原料池 / 人才池 / 场景池 | 积分池 / 收益池 / 额度池 / 悬赏池 / 争议池 / SOP 账本 / 贡献账本 / 潜在产值池 | planned |

## 4. PageBlockSchema 标准

| blockId | blockName | required | contentRule | forbiddenContent | gate |
|---|---|---|---|---|---|
| `PBS-SOURCE-SUMMARY` | 来源摘要 | yes | 记录脱敏摘要、来源类型、责任主体和时间戳 | 原文全文、未授权附件、个人敏感信息 | redaction_check |
| `PBS-TRUST-LAYER` | 可信层级 | yes | 标记 T0 / T1 / T2 / T3 / DSR 层级和检索时间 | 未核验结论伪装为权威事实 | waes_trust_check |
| `PBS-FACT-STATUS` | 事实状态 | yes | 标记 candidate / pending_manual / verified / blocked / withdrawn | 候选事实直接写成 confirmed | manual_check |
| `PBS-KDS-POOL-REFS` | KDS 11 池挂接 | yes | 至少挂接一个 KDS 11 池 | 增强账本脱离 KDS 11 池独立存在 | kds_pool_check |
| `PBS-LEDGER-REFS` | 增强账本挂接 | conditional | 仅在涉及积分、收益、额度、悬赏、争议、SOP 或潜在产值时出现 | 无委员会或人工确认的正式结论 | committee_check |
| `PBS-WAES-GATE` | WAES 门禁 | yes | 记录规则、边界、例外和门禁状态 | WAES 被写成业务主账 | waes_boundary_check |
| `PBS-MANUAL-SCORE` | 人工评测 | conditional | 记录评测人、评分项、红线项和建议 | AI 自动确认人工评分 | manual_score_check |
| `PBS-REDLINE` | 红线状态 | yes | 记录 redline_pass / redline_return / redline_block | 红线未检查即发布 | redline_check |
| `PBS-NEXT-ACTION` | 下一步动作 | yes | 记录补证、悬赏、邀请、退回或发布前动作 | 直接触发生产写入 | action_boundary_check |
| `PBS-PUBLISH-GATE` | 发布门禁 | yes | 记录 planned / draft / review / published / withdrawn | 未通过门禁即公开发布 | publish_gate_check |

## 5. PermissionFilterMatrix

| viewScope | 可见对象 | 可见内容 | 不可见内容 | 触发条件 |
|---|---|---|---|---|
| `public_summary` | 公开或外部展示对象 | 非敏感摘要、公开政策链接、通用模板说明 | 客户、订单、价格、合同、供应商、未公开拓厂条件 | 人工确认可公开 |
| `unit_self` | 湖北磷材授权人员 | 本单位提交的脱敏摘要、评测候选、缺口、悬赏和自有贡献积分候选 | 其他单位不可见事实、委员会内部争议详情 | 单位账号与角色匹配 |
| `project_group` | 项目组成员 | 项目范围内的候选事实、知识页草案、SOP 候选和补证动作 | 非项目范围商业敏感信息 | 项目组授权 |
| `committee` | 委员会成员 | 积分、收益、争议、重大违规、复议和例外处理资料 | 与裁决无关的个人敏感信息 | 委员会事项进入审议 |
| `governance_admin` | 平台治理角色 | 全量候选索引、门禁状态、撤回记录、审计链 | TOKEN、未授权外部系统凭证 | 治理与审计需要 |
| `invited_partner` | 被邀请合作单位 | 被邀请范围内的缺口、悬赏、任务和协作材料 | 发起方未授权的内部资料 | 邀请或悬赏生效 |

## 6. PublicationGateChecklist

| gateItemId | gateName | requirement | passStandard | currentStatus |
|---|---|---|---|---|
| `PGC-HBLC-001` | 来源索引完整 | 每个页面必须有来源索引、责任主体和时间戳 | 缺一不可 | not_checked |
| `PGC-HBLC-002` | 脱敏检查 | 不含未授权 DSR-L3 原文、合同原文、订单原文、报价原文或个人敏感信息 | redaction_pass | not_checked |
| `PGC-HBLC-003` | KDS 11 池挂接 | 每个页面至少挂接一个 KDS 11 池 | kds_pool_ref_present | not_checked |
| `PGC-HBLC-004` | 增强账本挂接 | 积分、收益、额度、悬赏、争议、SOP 和潜在产值必须挂接 KDS 11 池 | no_orphan_ledger | not_checked |
| `PGC-HBLC-005` | WAES 规则记录 | 发布前必须有 WAES 规则候选或门禁记录 | waes_record_present | not_checked |
| `PGC-HBLC-006` | 人工评测 | 发布为项目组可见前建议人工评分不低于 85；低于 85 只能内部草案或退回 | manual_score_ok | not_checked |
| `PGC-HBLC-007` | 红线状态 | 红线必须 pass；return 或 block 不得发布 | redline_pass | not_checked |
| `PGC-HBLC-008` | 权限过滤 | 页面必须配置可见范围和不可见字段 | permission_filter_present | not_checked |
| `PGC-HBLC-009` | 正式收益边界 | 到账才算正式收入，开票只作为统计、财务和流程口径 | revenue_boundary_present | not_checked |
| `PGC-HBLC-010` | 委员会事项 | 涉及正式积分、收益、争议、重大违规和分配规则必须进入委员会机制 | committee_required_when_applicable | not_checked |
| `PGC-HBLC-011` | 生产写入边界 | 页面发布不得触发真实 KDS API、WAES API、GFIS 写入或外部系统写入 | writeback_blocked | not_checked |
| `PGC-HBLC-012` | 撤回机制 | 页面必须可撤回、降级、留痕和重评 | withdrawal_ready | not_checked |

## 7. WAESPublicationGateCandidate 台账

| waesPublicationGateId | linkedBrainPageId | linkedReceiptOrGateId | gateType | ruleToConfirm | allowedOutcome | currentStatus |
|---|---|---|---|---|---|---|
| `WPG-HBLC-FEA-202606-0001` | `BKP-HBLC-FEA-202606-0001` | `WGR-HBLC-FEA-202606-0001` | publish_boundary | 拓厂知识页不得等同投资、合作或建设启动确认 | draft / return / block | planned |
| `WPG-HBLC-RAW-202606-0001` | `BKP-HBLC-RAW-202606-0001` | `WGR-HBLC-RAW-202606-0001` | purchase_boundary | 原料知识页不得等同采购事实或确认价格 | draft / return / block | planned |
| `WPG-HBLC-IND-202606-0001` | `BKP-HBLC-IND-202606-0001` | `WGR-HBLC-IND-202606-0001` | trusted_source | T3 可信来源必须有权威来源、检索时间和适用范围 | draft / return / block | planned |
| `WPG-HBLC-ORD-202606-0001` | `BKP-HBLC-ORD-202606-0001` | `WGR-HBLC-ORD-202606-0001` | revenue_boundary | 订单线索不得等同正式订单、开票或到账收入 | draft / return / block | planned |
| `WPG-HBLC-TPL-202606-0001` | `BKP-HBLC-TPL-202606-0001` | `WGR-HBLC-TPL-202606-0001` | reuse_boundary | 葛化母版只能复用结构、控制点和已授权经验，不得复制未确认事实 | draft / return / block | planned |
| `WPG-HBLC-MIX-202606-0001` | `BKP-HBLC-MIX-202606-0001` | `RTP-HBLC-MIX-202606-0001` | governance_boundary | 增强账本必须归入 KDS 11 池，不得形成游离事实底座 | draft / return / block | planned |

## 8. BrainOutputBoundary

| outputType | 允许输出 | 禁止输出 | 确认主体 |
|---|---|---|---|
| 知识页候选 | 页面结构、来源摘要、缺口、候选下一步 | 正式事实、正式收益、正式积分、正式 SOP | KDS / Brain / 人工 |
| SOP 候选 | 分段 SOP 建议、控制点、适用条件 | 自动生效 SOP、绕过 WAES 的业务动作 | WAES / 人工 |
| 缺口与悬赏 | 知识缺口、悬赏建议、参考积分区间 | 强制分配、自动扣分、自动收益划拨 | 委员会 / 发起方 |
| 潜在产值 | 线索区间、来源、补证要求 | 正式收入、到账事实、开票事实 | 人工 / 财务口径 |
| 写回建议 | KDS / WAES / GFIS 的候选字段和候选事实 | 真实 API 写入、生产主账写入、外部通知发送 | 人工确认后另行执行 |

## 9. 撤回与降级规则

| trigger | action | ledgerImpact | requiredRecord |
|---|---|---|---|
| 来源被证明错误 | 页面降级为 withdrawn 或 blocked | 贡献积分可按一般或重大规则扣回 | 撤回记录、来源复核记录 |
| 权限配置错误 | 立即撤回并重新脱敏 | 视影响范围进入争议池 | 权限事故记录、WAES 规则记录 |
| 红线未通过 | 不得发布，退回补证 | 不产生正式贡献 | 红线记录 |
| 重大违规 | 撤回、冻结相关积分或收益候选，进入委员会 | 可按事实比例或全部扣除 | 委员会记录、争议记录 |
| 页面被合作单位邀请复用 | 保持原事实归属，新增复用贡献候选 | 复用积分按协商或委员会规则处理 | 邀请记录、复用范围 |

## 10. 完成定义

本文完成条件：

1. 六类 Brain 页面候选均具备统一编号。
2. 每类页面均挂接 KDS 11 池和必要增强账本。
3. PageBlockSchema 覆盖来源、可信、事实、KDS、账本、WAES、人工、红线、动作和发布门禁。
4. PermissionFilterMatrix 覆盖公开、本单位、项目组、委员会、治理和邀请合作方。
5. PublicationGateChecklist 能阻断未脱敏、未授权、未评分、未挂接、未门禁和越权写入。
6. WAESPublicationGateCandidate 保持 planned 状态，不生成真实放行。
7. 所有输出只形成候选，不确认真实事实、正式积分、正式收益或正式 SOP。
8. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 11. DKS-035 建议

下一轮建议建立“湖北磷材 Brain 知识页候选运行评审空白台账与发布前问题清单”，把本文的页面候选转为可填报评审记录、问题清单、退回原因、发布建议和撤回登记。
