# GlobalCloud 绿色供应链体系设计工作区

日期：2026-06-10  
用途：集中管理 GlobalCloud GPCF 公共服务与治理体系、工厂执行子域、GPC-Native 路线、专项图集和实施提示词。  
口径基线：[GlobalCloud绿色供应链体系总架构.md](01-architecture/GlobalCloud%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E4%BD%93%E7%B3%BB%E6%80%BB%E6%9E%B6%E6%9E%84.md)

## 0. 统一定义（口径基线，与 [总架构] 一致）

1. **GlobalCloud GPCF** 是面向绿色供应链的公共服务与治理体系，不是单一软件产品，也不是某一套 ERP 的二开。
2. **GPC-Native** 是绿色供应链公共服务平台本体，平台主线与公共服务平台本体；不是"协同中台"，不是"新增中间层"。主责：平台订单、需求池、供应商协作、产能协同、工厂分配、ASN、预约、运输、POD、异常协同、绿色绩效、合规证据包、服务开放、生态接入。GPC-Native 内部流程引擎统一命名为"平台服务流程编排引擎 / 绿色供应链协同流程运行时 / 供应链公共服务流程引擎"，不得再称为"虚拟工厂运行时"。
3. **PVAOS** 是平台运营、租户、组织、伙伴、用户、权限、门户、项目和应用入口底座，不是平台订单主账。主责：租户、组织、用户、角色、权限、伙伴档案、项目空间、应用入口、门户菜单、平台运营配置。
4. **GFIS** 是工厂执行系统 / 工厂事实主账。主责：工厂订单、工单、生产报工、质量检验、质量放行、库存事务、批次、设备维护、发货出库、工厂执行证据。当前仓库中的 gcfis_custom、ERPNext 相关代码只能称为 GFIS 历史实现资产、适配器资产或 legacy reference，不作为 GFIS 主线定义来源。
5. **WAES** 是治理、证据确证、状态门控、合规、风险、审计和 AI 越权控制系统，不是平台订单主账，也不是工厂执行主账。主责：治理规则、证据确证、状态门控、合规校验、风险控制、审计追踪、模型授权、AI 越权拦截、异常升级、验收证据管理。
6. **Edge** 是现场采集与边缘缓冲层，优先服务 GFIS 的工厂执行事实确认，不得绕过 GFIS 先进入 GPC 公共服务数据池。
7. **Brain / LLM Wiki** 是企业知识主存 / 知识编制与引擎候选；**XiaoC / Hermes / XGD** 是 AI 与 Agent 编排层，二者均不能直接写业务事实。
8. 任何系统不得越权写入其他系统的主账事实；跨系统只能通过对象主责、事件合同、连接器合同和证据链路协同。

## 0.1 体系只承认的 5 个根连接器

1. `CON-GPC-GFIS-001`：GPC-Native ↔ GFIS 业务协同连接器。
2. `CON-GPC-WAES-001`：GPC-Native ↔ WAES 平台证据 / 治理状态连接器。
3. `CON-GFIS-WAES-001`：GFIS ↔ WAES 工厂治理 / 异常 / 审计 / 证据直连连接器（不废弃）。
4. `CON-EDGE-GFIS-001`：Edge → GFIS 现场采集连接器。
5. `CON-EDGE-WAES-001`：Edge → WAES 异常 / 安全 / 审计证据连接器（可选）。

任何其他跨系统连接器必须挂接到这 5 个根连接器下。

## 0.2 SOP 分层

1. GPC-Native：平台服务流程 SOP（`SOP-GPC-*`）。
2. GFIS：工厂执行 SOP（`SOP-GFIS-*`）。
3. WAES：治理规则 SOP（`SOP-WAES-*`）。
4. Brain / LLM Wiki：知识型 SOP（`SOP-KNOW-*`）。
5. PVAOS：平台运营 SOP（`SOP-PVAOS-*`）。
6. Edge：边缘接入 SOP（`SOP-EDGE-*`）。

## 文档索引

| 文档 | 用途 |
|---|---|
| [GlobalCloud绿色供应链体系层次化结构与优化提示词.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系层次化结构与优化提示词.md) | 更名后的体系级分层架构与优化提示词 |
| [GlobalCloud绿色供应链体系总架构.md](01-architecture/GlobalCloud%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E4%BD%93%E7%B3%BB%E6%80%BB%E6%9E%B6%E6%9E%84.md) | 体系级统一基线：总定位、主账边界、主链路、5 根连接器、SOP 分层、引擎命名修正（v2 口径修正稿） |
| [GPC 绿色供应链公共服务平台总体方案.md](03-data-ai-knowledge/GPC%20%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E5%85%AC%E5%85%B1%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0%E6%80%BB%E4%BD%93%E6%96%B9%E6%A1%88.md) | GPC 平台主体总体方案：平台身份、12 类主责、核心能力地图、引擎、验收矩阵（v2 口径修正稿） |
| [GlobalCloud绿色供应链体系对象目录.md](03-data-ai-knowledge/GlobalCloud%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E4%BD%93%E7%B3%BB%E5%AF%B9%E8%B1%A1%E7%9B%AE%E5%BD%95.md) | L0-L5 统一对象目录、主责系统、AI 写入边界和优先级对象（v2 口径修正稿） |
| [GlobalCloud绿色供应链体系事件合同.md](03-data-ai-knowledge/GlobalCloud%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E4%BD%93%E7%B3%BB%E4%BA%8B%E4%BB%B6%E5%90%88%E5%90%8C.md) | GFIS、GPC-Native、WAES、PVAOS、Brain、Agent 的一期事件合同（v2 口径修正稿） |
| [GlobalCloud绿色供应链体系连接器合同.md](03-data-ai-knowledge/GlobalCloud%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E4%BD%93%E7%B3%BB%E8%BF%9E%E6%8E%A5%E5%99%A8%E5%90%88%E5%90%8C.md) | 5 个根连接器编号、连接器等级、合同字段、状态机和验收要求（v2 口径修正稿） |
| [GlobalCloud绿色供应链体系一期验收矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系一期验收矩阵.md) | 一期端到端验收场景、证据要求、人工确认点和完成判定 |
| [GlobalCloud绿色供应链体系全局初始化SOP方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系全局初始化SOP方案.md) | WAES 发起供应链项目、四阶段生命周期、项目初始化、SOP 建设、试运营、正式运营和持续治理监控 |
| [GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md) | 从治理流、业务流、数据流、AI 服务流综合分析体系架构、遗漏内容、边界冲突和优化方案 |
| [GlobalCloud绿色供应链平台主架构与宪法约束融合建议.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链平台主架构与宪法约束融合建议.md) | 以现有绿链平台架构为主、吸收宪法治理约束后的统一架构主线 |
| [GlobalCloud绿色供应链体系最新架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系最新架构图.md) | 最新统一总架构图 |
| [GlobalCloud绿色供应链体系真实层次架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系真实层次架构图.md) | 去掉实现细节后的真实主责层次架构图 |
| [GlobalCloud绿色供应链平台业务流架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链平台业务流架构图.md) | 只看平台业务主链的拆分架构图 |
| [GlobalCloud绿色供应链体系WAES控制塔治理架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系WAES控制塔治理架构图.md) | 只看 WAES 控制塔、证据、状态和治理约束的拆分架构图 |
| [GlobalCloud绿色供应链体系WAES控制塔与治理门禁图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系WAES控制塔与治理门禁图.md) | WAES 控制塔、治理门禁、知识治理和 AI 授权的完整拆分图 |
| [GlobalCloud绿色供应链体系连接器合同.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系连接器合同.md) | 连接器身份、权限、API、事件、DLQ、重放、证据、降级恢复和治理生命周期合同 |
| [GlobalCloud绿色供应链体系SOP模板库.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系SOP模板库.md) | 可配置、可版本化、可执行、可验收的 P0/P1/P2 SOP 模板 |
| [GlobalCloud绿色供应链体系AI服务模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系AI服务模型.md) | Brain、XiaoC、Hermes/XGD、WAES 的 AI 授权、Agent 工具、建议结果和越权拦截模型 |
| [GlobalCloud绿色供应链体系数据治理模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系数据治理模型.md) | Schema、数据质量、死信、重放、血缘、证据、保留和租户隔离模型 |
| [GlobalCloud绿色供应链体系企业级知识库方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系企业级知识库方案.md) | 面向企业级知识真源、知识引擎层和 WAES 治理的知识底座主方案 |
| [GlobalCloud绿色供应链体系知识主存层与知识引擎层分层方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系知识主存层与知识引擎层分层方案.md) | 定义知识主存层、知识引擎层、AI 消费层和 WAES 治理层的分层边界 |
| [GlobalCloud企业级知识系统冲突点与收口方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud企业级知识系统冲突点与收口方案.md) | 对企业级知识主存、LLM Wiki、GBrain、Brain、WAES 当前冲突点进行收口并形成最终唯一口径 |
| [GlobalCloud智能体团队-企业级知识系统实施任务书.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队-企业级知识系统实施任务书.md) | 面向小即团队的企业级知识系统实施任务书，统一主存、编制、引擎、服务和 WAES 治理实施口径 |
| [GlobalCloud企业级知识系统总目标与执行分解表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud企业级知识系统总目标与执行分解表.md) | 将企业级知识系统整体工作拆成总目标、阶段、交付物、完成标准、当前进度和下一步动作的总控分解表 |
| [GlobalCloud绿色供应链体系LLM Wiki与GBrain测试评估矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系LLM Wiki与GBrain测试评估矩阵.md) | 用于并行测试结束后的唯一性选择和升级判定 |
| [GlobalCloud绿色供应链体系企业级知识库主存层与LLM Wiki-GBrain升级图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系企业级知识库主存层与LLM Wiki-GBrain升级图.md) | 企业级知识主存层与 LLM Wiki/GBrain 升级关系图 |
| [GlobalCloud绿色供应链体系全链路事件与证据闭环图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系全链路事件与证据闭环图.md) | 业务事实、事件、证据、知识引用、AI 建议和治理状态的全链路闭环图 |
| [GlobalCloud绿色供应链体系系统-数据库边界总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系系统-数据库边界总表.md) | 各系统数据库主责、可写边界、禁止事项和跨域协同方式总表 |
| [GlobalCloud绿色供应链体系资源仓库-业务对象映射总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系资源仓库-业务对象映射总表.md) | 资源仓库各池与业务对象、主责系统、AI 写入边界的映射总表 |
| [GlobalCloud绿色供应链体系知识与Agent授权治理总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系知识与Agent授权治理总表.md) | 知识真源、知识引擎、Agent 分层、权限边界和强制禁止清单总表 |
| [GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md) | 按当前设计基线完成整体评估、量化评分、缺口修复和 100 分复评的正式报告 |
| [GlobalCloud绿色供应链体系总体实施路线与交付保障方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系总体实施路线与交付保障方案.md) | 从设计基线推进到骨架落地、联调准备、试运行和正式运行准备的总体实施路线 |
| [GlobalCloud绿色供应链体系多智能体实施团队与协同方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系多智能体实施团队与协同方案.md) | 按 Harness Engineering 治理机制设计的多智能体实施团队、职责划分和协同规则 |
| [GlobalCloud绿色供应链体系实施项目控制与量化机制.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系实施项目控制与量化机制.md) | 交付包控制、评分分层、成本控制、节奏机制和量化项目管理方法 |
| [GlobalCloud绿色供应链体系动运转达标标准与质量门禁.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系动运转达标标准与质量门禁.md) | 定义体系何时算能动运转，以及进入下一阶段前必须通过的质量门禁 |
| [GlobalCloud智能体团队总体规划与行动计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队总体规划与行动计划.md) | 以小即为总负责人的 GlobalCloud 智能体团队组织、控制塔、汇报机制和行动计划总方案 |
| [GlobalCloud智能体团队控制塔与周报机制.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队控制塔与周报机制.md) | 小即团队的总体控制塔模块、总览字段、下钻字段和周报机制 |
| [GlobalCloud智能体团队8个交付包责任分解表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队8个交付包责任分解表.md) | 8 个交付包的牵头成员、协同成员、审计成员和交付范围分解 |
| [GlobalCloud智能体团队PMBOK项目管理台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队PMBOK项目管理台账.md) | 小即团队的 PMBOK 管理域、范围/进度/成本/质量/风险/相关方台账模板 |
| [GlobalCloud智能体团队阶段行动计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队阶段行动计划.md) | 从基线冻结到试运行准备的阶段目标、成员动作和完成判定 |
| [GlobalCloud项目群在Codex中的模型分工与成本控制方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud项目群在Codex中的模型分工与成本控制方案.md) | 项目群在 Codex 中的主质量模型、副模型和成本控制策略建议 |
| [GlobalCloud智能体团队模型使用治理与成本控制机制.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队模型使用治理与成本控制机制.md) | 小即团队执行模型选择、升级、返工和成本控制的正式治理机制 |
| [GlobalCloud统一模型配置体系方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud统一模型配置体系方案.md) | 为全体系建立全局模型配置真源、项目引用边界、用户偏好和治理主线 |
| [GlobalCloud全局模型目录与能力标签标准.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud全局模型目录与能力标签标准.md) | 统一模型目录、能力标签、档位、参数基线和本地/自定义模型元数据标准 |
| [GlobalCloud项目模型引用与用户模型偏好方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud项目模型引用与用户模型偏好方案.md) | 统一项目如何引用模型、用户如何在白名单和受控边界内选择模型 |
| [GlobalCloud模型授权审计计量与分期结算规划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud模型授权审计计量与分期结算规划.md) | 统一模型授权、审计、计量、统计、配额和 V1/V2/V3 充值结算分期规划 |
| [GlobalCloud智能体团队首版周报.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队首版周报.md) | 小即团队第 1 期初始化周报，包含总体状态、交付包快照、成员摘要和 PMBOK 偏差 |
| [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md) | 小即团队已接入/待接入专项会话回报的统一汇总台账 |
| [GlobalCloud智能体团队显性智能体名录与可见机制.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队显性智能体名录与可见机制.md) | 明确每个智能体的固定身份、会话状态、回报入口和可见性约束 |
| [GlobalCloud智能体团队下一步执行清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队下一步执行清单.md) | 小即总控当前阶段的直接执行清单，明确剩余专项接入和总控收口动作 |
| [GlobalCloud智能体团队当前总目标.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队当前总目标.md) | 小即团队当前总控目标，统一约束 6 个专项的首轮实施前验证、样本取证和联调前准备判断 |
| [GlobalCloud智能体团队侧边聊天完整归纳总览.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队侧边聊天完整归纳总览.md) | 对侧边聊天内容按 10 条主线做统一归纳，避免遗漏模型治理、界面治理、知识系统、执行版包和环境治理等侧线 |
| [GlobalCloud智能体团队侧边聊天10条主线-团队责任分配总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队侧边聊天10条主线-团队责任分配总表.md) | 将侧边聊天形成的 10 条主线逐条绑定到团队主责、协同、审计和交付包，避免“已归纳未落实” |
| [GlobalCloud智能体团队侧边聊天10条主线-当前实施准备完成度总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队侧边聊天10条主线-当前实施准备完成度总表.md) | 按 10 条主线判断已归纳、已分配、已工单化与正式实施开发前准备完成度 |
| [GlobalCloud智能体团队正式实施开发前缺口关闭清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队正式实施开发前缺口关闭清单.md) | 把距离“正式实施开发前准备完成”仍缺的关键缺口收口成可关闭清单 |
| [GlobalCloud智能体团队文档全量盘点与分类总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队文档全量盘点与分类总表.md) | 对当前 141 份文件做全量盘点与分类，明确主索引、正式基线、执行记录、样本证据、模板草案和历史参考层 |
| [GlobalCloud智能体团队文档理解与纳入审计.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队文档理解与纳入审计.md) | 判断所有文档是否已被正确理解、正确纳入工作内容，以及是否已具备实施前基线条件 |
| [GlobalCloud智能体团队文档清理与补充完善建议.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队文档清理与补充完善建议.md) | 给出当前轻清理策略、补强建议、缺口优先级和后续目录级整理建议 |
| [GlobalCloud智能体团队正式实施开发前准备100分量化评分提示词.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队正式实施开发前准备100分量化评分提示词.md) | 面向正式实施开发前准备的补强版 100 分量化评分提示词，已纳入 PMBOK、软件工程规范、最小闭环、团队工作规范、工具/技能治理、执行矩阵、环境门和阶段门禁 |
| [GlobalCloud智能体团队正式实施开发前准备评分文档纳入覆盖矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队正式实施开发前准备评分文档纳入覆盖矩阵.md) | 明确评分提示词是否已按文档分类全量纳入当前工作区全部正式文档类别，避免继续靠人工提醒补漏 |
| [GlobalCloud智能体实施团队准备度评估.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体实施团队准备度评估.md) | 小即团队当前“已就绪/部分就绪/未就绪”状态的正式准备度评估结论 |
| [GlobalCloud智能体团队实施前准备目标模式要求.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前准备目标模式要求.md) | 小即团队从设计基线推进到实施前准备就绪的目标模式、量化指标、完成标准和必交付物 |
| [GlobalCloud智能体团队真实项目仓库映射与只读预检计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队真实项目仓库映射与只读预检计划.md) | 6 个专项进入真实项目仓库前的仓库映射、只读预检顺序和检查口径 |
| [GlobalCloud智能体团队实施前准备差距清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前准备差距清单.md) | 从当前实施准备分推进到实施前准备就绪的剩余差距与关闭顺序 |
| [GlobalCloud智能体团队实施前证据与阻塞总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前证据与阻塞总表.md) | 6 个专项进入真实实施前必须具备的设计证据、运行前证据、阻塞和关闭条件总表 |
| [链同专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项会话状态报告.md) | 链同专项首轮正式回报，包含 PVAOS/GPC 协同域当前证据、进度、阻塞和给小即的结论 |
| [厂行专项会话状态报告.md](06-workstreams/%E5%8E%82%E8%A1%8C%E4%B8%93%E9%A1%B9%E4%BC%9A%E8%AF%9D%E7%8A%B6%E6%80%81%E6%8A%A5%E5%91%8A.md) | 厂行专项首轮正式回报，包含 GFIS/Edge 执行域当前证据、进度、阻塞和给小即的结论（v2 口径修正稿） |
| [知源专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项会话状态报告.md) | 知源专项首轮正式回报，包含知识主存/知识引擎域当前证据、进度、阻塞和给小即的结论 |
| [GlobalCloud智能体团队实施前准备完成结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前准备完成结论.md) | 小即对实施前准备收口已完成的正式结论，说明该阶段已结束并已进入预检与验证前置阶段 |
| [GlobalCloud绿色供应链体系实施过程控制规范清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系实施过程控制规范清单.md) | 把当前体系从设计总控推进到实施执行控制层的过程控制规范总清单 |
| [GlobalCloud绿色供应链体系交付物完成判定规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系交付物完成判定规范.md) | 统一规定文档、配置、接口、数据库、代码、测试、验收交付物何时算完成 |
| [GlobalCloud绿色供应链体系项目仓库实施准入规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系项目仓库实施准入规范.md) | 规定专项何时允许进入真实项目仓库实施，以及 dirty state、分支和写入边界控制 |
| [GlobalCloud绿色供应链体系设计-实现追踪矩阵规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系设计-实现追踪矩阵规范.md) | 统一设计、仓库、文件、对象、事件与验收之间的追踪链要求 |
| [GlobalCloud绿色供应链体系测试与验证规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系测试与验证规范.md) | 统一从仓库级验证到运行前验证的分层验证口径 |
| [GlobalCloud绿色供应链体系状态升级与验收放行规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系状态升级与验收放行规范.md) | 统一 Harness 状态升级、退回条件与验收放行规则 |
| [宪衡专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/宪衡专项正式只读预检结论.md) | WAES 治理与控制塔域的真实项目仓库正式只读预检结论 |
| [链同专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项正式只读预检结论.md) | PVAOS + GPC 原型协同域的真实项目仓库正式只读预检结论 |
| [厂行专项正式只读预检结论.md](06-workstreams/%E5%8E%82%E8%A1%8C%E4%B8%93%E9%A1%B9%E6%AD%A3%E5%BC%8F%E5%8F%AA%E8%AF%BB%E9%A2%84%E6%A3%80%E7%BB%93%E8%AE%BA.md) | GFIS + Edge 执行域的真实项目仓库正式只读预检结论（v2 口径修正稿） |
| [数枢专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/数枢专项正式只读预检结论.md) | AI 与数据底座跨仓库正式只读预检结论 |
| [知源专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项正式只读预检结论.md) | Brain 知识主存与知识引擎域的真实项目仓库正式只读预检结论 |
| [灵策与评证专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策与评证专项正式只读预检结论.md) | XiaoC + Hermes + XGD AI 服务与审计验证域的真实项目仓库正式只读预检结论 |
| [GlobalCloud智能体团队首轮实施前验证入口判断.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队首轮实施前验证入口判断.md) | 小即对 6 个专项正式只读预检完成后是否允许进入首轮实施前验证准备的正式判断 |
| [GlobalCloud绿色供应链体系模块实施分级判定表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系模块实施分级判定表.md) | P0 最小闭环下 12 个核心模块在 WAES/PVAOS/GPC/GFIS 四条主线中的实施分级前置判定表 |
| [GlobalCloud绿色供应链体系界面分阶段治理规则.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面分阶段治理规则.md) | 规定第一阶段禁止无必要新建界面、第二阶段新增界面统一纳管、最终交付阶段统一界面规范的分阶段治理规则 |
| [GlobalCloud绿色供应链体系统一体验骨架规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系统一体验骨架规范.md) | 统一新增界面的页面结构、对话模式、操作方式、状态反馈、证据展示和 AI 展示方式的骨架规范 |
| [GlobalCloud绿色供应链体系最终交付界面规范与样式规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系最终交付界面规范与样式规范.md) | 定义最终交付阶段必须统一的页面规范、样式规范、使用规范和跨平台一致性要求 |
| [GlobalCloud绿色供应链体系对话模式与操作模式规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系对话模式与操作模式规范.md) | 统一查询、建议、操作辅助、复盘、治理确认等对话模式，以及主操作、危险操作、异常处置、证据确认的操作方式 |
| [GlobalCloud绿色供应链体系统一组件与设计令牌规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系统一组件与设计令牌规范.md) | 统一颜色、字体、间距、图标、按钮、表单、表格、状态标签、弹窗、AI 组件等设计系统层约束 |
| [GlobalCloud绿色供应链体系界面实施差距清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面实施差距清单.md) | 将当前界面规范转化为 P0/P1/P2 差距、分系统差距和关闭顺序的执行清单 |
| [GlobalCloud绿色供应链体系统一组件库建设计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系统一组件库建设计划.md) | 将统一组件与设计令牌规范转成首批组件、阶段目标、优先级和建设路径 |
| [GlobalCloud绿色供应链体系首批统一组件清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批统一组件清单.md) | 定义首批必须建设、必须优先接入高风险模块的统一组件清单 |
| [GlobalCloud绿色供应链体系高风险模块界面收口计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系高风险模块界面收口计划.md) | 定义平台订单、签收、异常、质量、证据/审计、AI 建议与治理确认等高风险模块的优先收口顺序与方式 |
| [GlobalCloud绿色供应链体系高风险模块界面收口任务分解表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系高风险模块界面收口任务分解表.md) | 将高风险模块的结构收口、交互收口、组件接入、样式收口拆成可执行任务 |
| [GlobalCloud绿色供应链体系首批统一组件验收标准.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批统一组件验收标准.md) | 定义首批统一组件做到什么程度才算通过，并要求在高风险模块完成接入样板 |
| [GlobalCloud绿色供应链体系P0最小闭环界面实施清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系P0最小闭环界面实施清单.md) | 将 P0 最小闭环节点逐项绑定到“是否允许新建界面、采用何种实施方式、接入哪些统一组件、如何验收”的实施清单 |
| [GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵.md) | 定义 P0 闭环节点界面何时算通过、需要哪些证据、哪些不得误判为完成 |
| [GlobalCloud绿色供应链体系平台订单-签收-异常界面收口专项方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系平台订单-签收-异常界面收口专项方案.md) | 对最危险的一条链单独制定结构、交互、组件、风险和验收收口方案 |
| [GlobalCloud绿色供应链体系高风险模块样板页清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系高风险模块样板页清单.md) | 定义高风险模块第一批必须优先做成标准样板的页面清单和优先顺序 |
| [GlobalCloud绿色供应链体系首批统一组件接入样板清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批统一组件接入样板清单.md) | 定义首批统一组件先在哪些样板页真实接入，并形成第一批必须跑通的组件组合 |
| [GlobalCloud绿色供应链体系样板页实施计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系样板页实施计划.md) | 将样板页清单推进为分阶段、可排期、可验收的样板页实施计划 |
| [GlobalCloud绿色供应链体系首批组件接入实施计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批组件接入实施计划.md) | 将首批统一组件清单和接入样板清单推进为实际接入顺序与接入通过标准 |
| [GlobalCloud绿色供应链体系界面实施排期表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面实施排期表.md) | 将高风险链路、样板页和组件接入推进为按阶段执行的统一排期表 |
| [GlobalCloud绿色供应链体系界面实施责任分配表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面实施责任分配表.md) | 将样板页、统一组件和高风险模块收口任务落实到明确责任域、协同域和复核域 |
| [GlobalCloud智能体团队运行与实施环境总体规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队运行与实施环境总体规范.md) | 将设计控制环境、项目仓库环境、本地运行环境、集成验证环境、试运行环境、生产环境统一成环境门模型 |
| [GlobalCloud智能体团队工作区与项目仓库操作规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队工作区与项目仓库操作规范.md) | 明确总控工作区与真实项目仓库的双层工作机制、preflight 和回写要求 |
| [GlobalCloud智能体团队Codex工具与技能使用治理规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队Codex工具与技能使用治理规范.md) | 统一 Codex 主线程、专项线程、Shell、Git、Linear、Skill、自动化与密钥的使用矩阵和治理规则 |
| [GlobalCloud智能体团队软件全过程实施与交付控制规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队软件全过程实施与交付控制规范.md) | 从目标、设计、环境、仓库预检到验证、试运行、验收、发布和复盘的全过程控制链规范 |
| [GlobalCloud智能体团队阶段-工作-工具-技能-方法-效率-成本执行矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队阶段-工作-工具-技能-方法-效率-成本执行矩阵.md) | 将不同阶段、不同工作类型对应的环境、工具、技能、方法、效率要求、成本上限、证据类型和状态上限固定成执行矩阵 |
| [GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵.md) | 把 6 个专项在首轮实施前验证阶段的环境、工具、技能、方法、效率要求、成本上限、证据清单和状态上限统一固定下来 |
| [GlobalCloud智能体团队6个专项首轮实施前验证执行台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队6个专项首轮实施前验证执行台账.md) | 把 6 个专项首轮实施前验证包推进到逐项执行、逐项留证、逐项识别阻塞的统一执行台账 |
| [GlobalCloud智能体团队首轮实施前验证包总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队首轮实施前验证包总表.md) | 6 个专项首轮实施前验证包的总表与统一执行纪律 |
| [宪衡专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/宪衡专项首轮实施前验证包.md) | WAES 治理与控制塔域的首轮实施前验证包 |
| [宪衡专项首轮实施前验证执行记录.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/宪衡专项首轮实施前验证执行记录.md) | WAES 治理与控制塔域首轮实施前验证从预检与验证包推进到执行记录的首份落账 |
| [链同专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项首轮实施前验证包.md) | PVAOS + GPC 协同域的首轮实施前验证包 |
| [链同专项首轮实施前验证执行记录.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项首轮实施前验证执行记录.md) | PVAOS 生态入口与 GPC 协同原型域首轮实施前验证从预检与验证包推进到执行记录的首份落账 |
| [厂行专项首轮实施前验证包.md](06-workstreams/%E5%8E%82%E8%A1%8C%E4%B8%93%E9%A1%B9%E9%A6%96%E8%BD%AE%E5%AE%9E%E6%96%BD%E5%89%8D%E9%AA%8C%E8%AF%81%E5%8C%85.md) | GFIS + Edge 执行域的首轮实施前验证包（v2 口径修正稿） |
| [厂行专项首轮实施前验证执行记录.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/厂行专项首轮实施前验证执行记录.md) | GFIS 工厂执行与 Edge 联合域首轮实施前验证从预检与验证包推进到执行记录的首份落账 |
| [数枢专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/数枢专项首轮实施前验证包.md) | AI 与数据底座跨仓库域的首轮实施前验证包 |
| [数枢专项首轮实施前验证执行记录.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/数枢专项首轮实施前验证执行记录.md) | AI 与数据底座跨仓库域首轮实施前验证从预检与验证包推进到执行记录的首份落账 |
| [知源专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项首轮实施前验证包.md) | Brain 知识主存与知识引擎域的首轮实施前验证包 |
| [知源专项首轮实施前验证执行记录.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项首轮实施前验证执行记录.md) | Brain 知识主存与知识引擎域首轮实施前验证从预检与验证包推进到执行记录的首份落账 |
| [灵策与评证专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策与评证专项首轮实施前验证包.md) | XiaoC + Hermes + XGD AI 服务与审计验证域的首轮实施前验证包 |
| [灵策与评证专项首轮实施前验证执行记录.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策与评证专项首轮实施前验证执行记录.md) | XiaoC + Hermes + XGD AI 服务与审计验证联合域首轮实施前验证从预检与验证包推进到执行记录的首份落账 |
| [GlobalCloud智能体团队本阶段首轮实施前验证目标.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队本阶段首轮实施前验证目标.md) | 固定当前阶段唯一主目标、专项目标、量化目标和完成判定的阶段目标文档 |
| [链同专项会话状态报告模板.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项会话状态报告模板.md) | 链同专项首轮回报模板，统一 PVAOS/GPC-Native 协同域回报格式 |
| [厂行专项会话状态报告模板.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/厂行专项会话状态报告模板.md) | 厂行专项首轮回报模板，统一 GFIS/Edge 执行域回报格式 |
| [知源专项会话状态报告模板.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项会话状态报告模板.md) | 知源专项首轮回报模板，统一知识主存/知识引擎域回报格式 |
| [灵策与评证专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策与评证专项会话状态报告.md) | 灵策与评证专项会话的当前进度、已完成工作、下一步计划、主要困难、当前阻塞和给小即的汇报结论 |
| [GlobalCloud绿色供应链体系多厂协同模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系多厂协同模型.md) | 一链多厂、多链多厂的分单、产能、库存可视、质量追溯和跨厂异常模型 |
| [GlobalCloud绿色供应链体系Edge接入与安全模型.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系Edge接入与安全模型.md) | Edge 采集、缓存、补传、去重、遥测事实和 OT/IT 安全边界 |
| [AI驱动工厂信息化系统完整方案V3.1.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/AI驱动工厂信息化系统完整方案V3.1.md) | 工厂执行子域 V3.1 基础方案 |
| [基于GlobalCloud项目群的智慧工厂架构设计方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/基于GlobalCloud项目群的智慧工厂架构设计方案.md) | 基于现有项目群的架构基础稿，后续应向绿色供应链体系口径迁移 |
| [GlobalCloud智慧工厂项目群架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智慧工厂项目群架构图.md) | 项目群总览 Mermaid 架构图，后续作为绿色供应链体系图基础 |
| [GlobalCloud智慧工厂专项架构图集.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智慧工厂专项架构图集.md) | 数据事件、集成边界、OT/IT、安全、异常闭环专项图 |
| [ADR-GPC从Odoo二开调整为原生协同中台.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/ADR-GPC从Odoo二开调整为原生协同中台.md) | GPC 从 Odoo 二开切换到 GPC-Native 的架构决策 |
| [GlobalCloud智慧工厂项目群控制表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智慧工厂项目群控制表.md) | 项目群状态、角色和下一步控制表 |
| [GlobalCloud智慧工厂进一步梳理与提示词库.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智慧工厂进一步梳理与提示词库.md) | 进一步梳理路线和可直接使用的 Codex/Agent 提示词 |

## 当前主结论

1. 总体系名称调整为 **GlobalCloud 绿色供应链体系**。
2. 主架构采用三层：治理与监控层、运营与协同层、生产与执行层。
3. “智慧工厂”降级为体系内的工厂执行与本地运行子域。
4. GFIS 是单厂本地执行事实源。
5. GPC 主线调整为 GPC-Native 轻量绿色供应链协同中台。
6. 现有 Odoo GPC 降级为历史原型、流程样本和可选 back-office connector。
7. WAES 是治理与监控中枢、规则审批和证据平面，不审批具体事务，不是业务主账。
8. Brain/XiaoC/Hermes/XGD 提供知识、Prompt、Agent 和交互能力，必须遵守三层架构下的 AI 授权边界。
9. Edge 是现场与 GFIS 之间的边缘接入层，负责采集、协议转换、缓存和回执，不是业务主账。
10. 全局初始化 SOP 采用四阶段：项目初始化、项目配置与 SOP 建设、正式运营、WAES 持续治理与监控。
11. 四流综合架构采用治理流、业务流、数据流、AI 服务流进行交叉约束：治理流约束业务流，业务流产生数据流，数据流支撑治理流，AI 服务流消费数据流并受治理流授权。
12. 当前已补齐对象目录、事件合同、一期验收矩阵、全局初始化 SOP、四流综合架构、连接器合同、SOP 模板库、AI 服务模型、数据治理模型、多厂协同模型和 Edge 接入安全模型。
13. 后续应继续把 GFIS LES 模型、GPC-Native 一期服务模型和 WAES 控制塔模型落成独立实施方案，并与连接器合同和验收矩阵绑定。
14. 当前全部文档的架构更新主线为：以 `GPC-Native` 为绿色供应链平台主线，以 `WAES` 为治理平面，以 `GFIS` 为工厂事实平面，以宪法内容作为证据、状态、授权和连接器治理约束。
15. 当前体系主结构采用：治理与监控层、运营与协同层、生产与执行层，以及横向 `AI 与数据层`。
16. `AI 与数据层` 内部包含：资源仓库域、结构化数据库域、企业级知识主存域、知识引擎域、AI 服务域、事件证据指标追踪域；资源仓库当前已定义十一池，后续可继续扩展其它池。
17. `LLM Wiki` 与 `GBrain` 当前处于并行测试期，只作为知识引擎层候选，不直接等同于企业级知识真源。
18. 本阶段新增重点工作为企业级知识库方案、知识主存层/知识引擎层分层方案，以及 `LLM Wiki` 与 `GBrain` 的升级与唯一性评估。
19. 当前已新增《GlobalCloud企业级知识系统冲突点与收口方案》，用于统一知识主存、LLM Wiki、GBrain、Brain、WAES 的最终唯一口径。
20. 当前已新增《GlobalCloud智能体团队-企业级知识系统实施任务书》，用于按小即团队实施方式推进企业级知识系统落地。
21. 当前已新增统一模型配置主线，明确：全局模型配置只有一个真源，项目只引用，用户只在统一治理边界内选择，自定义模型和本地模型统一接入、统一审计、统一授权、统一降级。
22. 当前统一模型配置采用分期落地：V1 统一治理与统一配置，V2 统一计量与统计，V3 充值与结算。
21. 当前实施组织按多智能体团队推进：总控、专业实施、评估审计和证据验收分层协同，统一受 Harness Engineering 状态和证据纪律约束。
22. 当前 100 分只代表设计基线完备度达到 100/100，不代表真实联调、试运行或规模化运行已经完成。
23. 当前智能体团队总负责人名称确定为 **小即**，并已形成中文团队命名、统一汇报机制和总体控制塔规划。
24. 当前已补齐小即团队的控制塔、8个交付包责任分解、PMBOK 项目管理台账和阶段行动计划配套文档。
25. 当前已形成小即团队首版周报，并已同步到 Linear 项目台账与总控事项。
26. 当前已建立专项回报汇总台账，并已完成 6/6 专项首轮正式回报接入：宪衡、链同、厂行、数枢、知源、灵策与评证。
27. 当前已形成小即总控的下一步执行清单，下一阶段主线已切换为 6 个专项正式只读预检结论和首轮实施前验证准备。
28. 当前已形成小即团队准备度评估，明确：团队基础准备已就绪，专项接入准备已就绪，实施前准备已就绪，真实实施与运行准备未就绪。
29. 当前已完成“小即团队实施前准备目标模式”收口，在不伪造运行完成的前提下，已完成 6/6 专项接入、真实项目仓库映射、实施前证据清单和总控收口结论。
30. 当前已形成第一版 6 个专项真实项目仓库映射与只读预检计划，已纳入 WAES、PVAOS、GFIS、GPC、Brain、XiaoC、Hermes、XGD 的首轮仓库级只读证据。
31. 当前已形成第一版实施前准备差距清单，以及 6 个专项的实施前证据与阻塞总表。
32. 当前已形成《GlobalCloud智能体团队实施前准备完成结论》，正式确认：实施前准备收口阶段已经结束，但仍不得写成联调完成、试运行完成或 `complete`。
33. 当前已形成 6 个专项正式只读预检结论：宪衡、链同、厂行、数枢、知源、灵策与评证。
34. 当前已形成《GlobalCloud智能体团队首轮实施前验证入口判断》，正式确认：已完成 6 个专项真实项目仓库正式只读预检，可以进入首轮实施前验证准备，但仍不得写成联调完成、试运行完成或生产可用。
35. 当前已形成《GlobalCloud绿色供应链体系模块实施分级判定表》，作为后续开发、配置、局部开发、重构的前置门；没有分级判定，不得进入开发。
36. 当前已形成《GlobalCloud绿色供应链体系界面分阶段治理规则》，明确第一阶段不为统一视觉而新建界面，第二阶段所有新增界面必须纳入统一体验骨架。
37. 当前已形成《GlobalCloud绿色供应链体系统一体验骨架规范》，用于统一列表页、详情页、配置页、工作台、异常页、证据页和 AI 对话/侧栏的结构与交互。
38. 当前已形成《GlobalCloud绿色供应链体系最终交付界面规范与样式规范》，用于约束最终交付阶段的统一页面规范、统一样式规范、统一使用规范和跨平台一致性。
39. 当前已形成《GlobalCloud绿色供应链体系对话模式与操作模式规范》，用于统一查询、建议、治理确认、异常处置、证据确证等高频交互模式，避免不同系统形成不同交互语言。
40. 当前已形成《GlobalCloud绿色供应链体系统一组件与设计令牌规范》，用于把界面、交互、最终交付要求进一步收口到统一设计系统层。
41. 当前已形成《GlobalCloud绿色供应链体系界面实施差距清单》，明确当前不是缺规范，而是进入“规范齐全、执行收口不足”阶段。
42. 当前已形成《GlobalCloud绿色供应链体系统一组件库建设计划》，用于把统一界面、统一交互、统一设计系统转为真实组件库建设任务。
43. 当前已形成《GlobalCloud绿色供应链体系首批统一组件清单》，明确首批统一组件优先级、优先接入模块和强约束。
44. 当前已形成《GlobalCloud绿色供应链体系高风险模块界面收口计划》，明确平台订单、签收、异常、质量、证据/审计、AI 建议等高风险模块的收口顺序与方式。
45. 当前已形成《GlobalCloud绿色供应链体系高风险模块界面收口任务分解表》，将高风险模块的收口从原则和计划推进到任务层。
46. 当前已形成《GlobalCloud绿色供应链体系首批统一组件验收标准》，将首批组件建设推进到可验收层。
47. 当前已形成《GlobalCloud绿色供应链体系P0最小闭环界面实施清单》，把界面治理线正式绑定到了 P0 最小闭环实施主线。
48. 当前已形成《GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵》，把界面实施进一步推进到闭环验收层。
49. 当前已形成《GlobalCloud绿色供应链体系平台订单-签收-异常界面收口专项方案》，把最危险的一条链单独抽出进行优先收口。
50. 当前已形成《GlobalCloud绿色供应链体系高风险模块样板页清单》，明确先做哪些标准样板页，而不是大面积同时起页面。
51. 当前已形成《GlobalCloud绿色供应链体系首批统一组件接入样板清单》，明确首批组件必须先在哪些样板页真实落地。
52. 当前已形成《GlobalCloud绿色供应链体系样板页实施计划》，把样板页从“清单”推进到“分阶段实施计划”。
53. 当前已形成《GlobalCloud绿色供应链体系首批组件接入实施计划》，把组件接入从“组件-页面绑定”推进到“实际接入顺序与通过标准”。
54. 当前已形成《GlobalCloud绿色供应链体系界面实施排期表》，把高风险链路、样板页和首批组件接入推进到真实排期层。
55. 当前已形成《GlobalCloud绿色供应链体系界面实施责任分配表》，把界面实施从任务和验收推进到责任绑定层。
56. 当前已补齐“运行与实施环境、工作区与项目仓库、Codex 工具与技能、软件全过程控制”四类一级规范，用于把环境门、工具门、过程门与整体设计、实施、软件工作全过程正式绑定。
57. 当前已形成 6 个专项首轮实施前验证包，下一阶段主线已经从“只读预检结论形成”切换为“运行前样本收集与验证入口确认”。
58. 当前已新增实施过程控制规范清单，以及交付物完成判定、仓库实施准入、设计-实现追踪、测试与验证、状态升级与验收放行五类强约束规范，并已绑定到小即团队和实施路线。
59. 当前企业级知识系统主线已新增《GlobalCloud企业级知识系统总目标与执行分解表》，后续工作统一按总目标、阶段、交付物、完成标准和下一步动作推进，不再停留在零散知识文档讨论。
60. 当前小即团队总控目标已正式独立成文：后续主线不再是继续扩方案，而是围绕 6 个专项的首轮实施前验证、运行前样本取证和联调前准备判断推进。
61. 当前已新增“侧边聊天 10 条主线责任分配总表、当前实施准备完成度总表、正式实施开发前缺口关闭清单”，用于把“已归纳 / 已分配 / 已工单化 / 已具备开发前条件”严格区分开，避免误判为已全量准备完成。
62. 当前已完成 145 份文档的第一轮全量盘点、分类、理解与纳入审计，并已明确：实施前基线条件已具备，但正式实施开发前准备仍未全量完善。
63. 当前已形成《GlobalCloud智能体团队正式实施开发前准备100分量化评分提示词》，用于按正式开发前口径而非设计完成口径执行 100 分评分、门禁判断和补分路径设计。
64. 当前已形成《GlobalCloud智能体团队正式实施开发前准备评分文档纳入覆盖矩阵》，用于确认评分提示词已按文档分类全量纳入当前工作区的正式文档类别，不再依赖人工提醒补漏。

## 0.9 口径修正收口（2026-06-10 落地）

1. 体系身份、主账边界、主链路、5 根连接器、SOP 分层、引擎命名修正统一以 [GlobalCloud绿色供应链体系总架构.md](01-architecture/GlobalCloud%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E4%BD%93%E7%B3%BB%E6%80%BB%E6%9E%B6%E6%9E%84.md) 为基线。
2. 对象目录、事件合同、连接器合同、厂行专项三份核心文件、GPC 平台总体方案已按 v2 口径修正稿同步。
3. GPC-Native 不再称为"协同中台"或"新增中间层"；GPC-Native 内部引擎不再称为"虚拟工厂运行时"。
4. 仓库中 gcfis_custom、ERPNext 资产归为 GFIS 历史实现资产 / 适配器资产 / legacy reference。
5. `CON-GFIS-WAES-001` 不废弃。
6. 后续文档、对话、Codex 智能体团队、专项回报、验收记录如与本文不一致，必须以 [总架构] 为准。

## 当前设计基线

1. 体系身份与主账边界以 [GlobalCloud绿色供应链体系总架构.md](01-architecture/GlobalCloud%E7%BB%BF%E8%89%B2%E4%BE%9B%E5%BA%94%E9%93%BE%E4%BD%93%E7%B3%BB%E6%80%BB%E6%9E%B6%E6%9E%84.md) 为基线，GPC-Native = 公共服务平台本体，PVAOS = 运营与门户底座，GFIS = 工厂执行系统 / 工厂事实主账，WAES = 治理 / 证据 / 状态门控 / AI 越权控制，Edge = 现场采集与边缘缓冲，Brain = 知识主存，XiaoC / Hermes / XGD = AI 与 Agent 编排。
2. 三层主架构用于业务表达：治理与监控层、运营与协同层、生产与执行层。
3. 体系只承认 5 个根连接器：`CON-GPC-GFIS-001` / `CON-GPC-WAES-001` / `CON-GFIS-WAES-001`（不废弃） / `CON-EDGE-GFIS-001` / `CON-EDGE-WAES-001`（可选）。
4. GPC-Native 内部流程引擎统一命名为"平台服务流程编排引擎 / 绿色供应链协同流程运行时 / 供应链公共服务流程引擎"，不得再称为"虚拟工厂运行时"。
5. 仓库中 gcfis_custom、ERPNext 相关代码归为 GFIS 历史实现资产 / 适配器资产 / legacy reference，不作为 GFIS 主线定义来源。
6. Edge 优先服务 GFIS，不得绕过 GFIS 先进入 GPC 公共服务数据池。
7. L0-L5 作为内部实施映射保留，不再作为对外主表达。
8. 先以对象目录统一业务对象、主责系统和状态口径。
9. 再以事件合同约束跨系统事实流，禁止 AI 建议伪装为业务事实。
10. 最后用一期验收矩阵定义端到端场景、证据、治理确认点和完成判定。
11. 四流综合架构用于检查治理、业务、数据和 AI 服务之间的边界冲突、遗漏对象、事件缺口、连接器合同、SOP 模板和验收矩阵扩展。
12. 连接器合同、SOP 模板库、AI 服务模型、数据治理模型、多厂协同模型和 Edge 接入安全模型作为四流优化后的专项设计基线。
13. 在完成真实运行态联调前，系统状态最多可判定为 `ready_for_human_acceptance`，不得标记为 `complete`。
14. 在 `LLM Wiki` 与 `GBrain` 并行测试结束前，两者都只作为知识编制层或知识引擎层候选，不作为企业级知识库唯一真源。
15. 实施阶段必须同时遵循：交付包控制、量化评分、五层质量门禁和动运转达标标准。

## 当前建议阅读顺序

如果要先看更新后的架构，建议按下面顺序阅读：

1. [GlobalCloud绿色供应链平台主架构与宪法约束融合建议.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链平台主架构与宪法约束融合建议.md)
2. [GlobalCloud绿色供应链体系最新架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系最新架构图.md)
3. [GlobalCloud绿色供应链平台业务流架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链平台业务流架构图.md)
4. [GlobalCloud绿色供应链体系WAES控制塔治理架构图.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系WAES控制塔治理架构图.md)
5. [GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md)
6. [GlobalCloud绿色供应链体系对象目录.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系对象目录.md)
7. [GlobalCloud绿色供应链体系事件合同.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系事件合同.md)
8. [GlobalCloud绿色供应链体系企业级知识库方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系企业级知识库方案.md)
9. [GlobalCloud绿色供应链体系知识主存层与知识引擎层分层方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系知识主存层与知识引擎层分层方案.md)
10. [GlobalCloud企业级知识系统冲突点与收口方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud企业级知识系统冲突点与收口方案.md)
11. [GlobalCloud绿色供应链体系LLM Wiki与GBrain测试评估矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系LLM Wiki与GBrain测试评估矩阵.md)
12. [GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md)
13. [GlobalCloud绿色供应链体系总体实施路线与交付保障方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系总体实施路线与交付保障方案.md)
14. [GlobalCloud绿色供应链体系多智能体实施团队与协同方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系多智能体实施团队与协同方案.md)
15. [GlobalCloud绿色供应链体系实施项目控制与量化机制.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系实施项目控制与量化机制.md)
16. [GlobalCloud绿色供应链体系动运转达标标准与质量门禁.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系动运转达标标准与质量门禁.md)
17. [GlobalCloud智能体团队总体规划与行动计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队总体规划与行动计划.md)
18. [GlobalCloud智能体团队控制塔与周报机制.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队控制塔与周报机制.md)
19. [GlobalCloud智能体团队8个交付包责任分解表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队8个交付包责任分解表.md)
20. [GlobalCloud智能体团队PMBOK项目管理台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队PMBOK项目管理台账.md)
21. [GlobalCloud智能体团队阶段行动计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队阶段行动计划.md)
22. [GlobalCloud智能体团队首版周报.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队首版周报.md)
23. [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md)
24. [GlobalCloud智能体团队显性智能体名录与可见机制.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队显性智能体名录与可见机制.md)
25. [GlobalCloud智能体团队下一步执行清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队下一步执行清单.md)
25. [GlobalCloud智能体实施团队准备度评估.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体实施团队准备度评估.md)
26. [GlobalCloud智能体团队实施前准备目标模式要求.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前准备目标模式要求.md)
27. [GlobalCloud智能体团队真实项目仓库映射与只读预检计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队真实项目仓库映射与只读预检计划.md)
28. [GlobalCloud智能体团队实施前准备差距清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前准备差距清单.md)
29. [GlobalCloud智能体团队实施前证据与阻塞总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前证据与阻塞总表.md)
30. [链同专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项会话状态报告.md)
31. [厂行专项会话状态报告.md](06-workstreams/%E5%8E%82%E8%A1%8C%E4%B8%93%E9%A1%B9%E4%BC%9A%E8%AF%9D%E7%8A%B6%E6%80%81%E6%8A%A5%E5%91%8A.md)
32. [知源专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项会话状态报告.md)
33. [GlobalCloud智能体团队实施前准备完成结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前准备完成结论.md)
34. [宪衡专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/宪衡专项正式只读预检结论.md)
35. [链同专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项正式只读预检结论.md)
36. [厂行专项正式只读预检结论.md](06-workstreams/%E5%8E%82%E8%A1%8C%E4%B8%93%E9%A1%B9%E6%AD%A3%E5%BC%8F%E5%8F%AA%E8%AF%BB%E9%A2%84%E6%A3%80%E7%BB%93%E8%AE%BA.md)
37. [数枢专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/数枢专项正式只读预检结论.md)
38. [知源专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项正式只读预检结论.md)
39. [灵策与评证专项正式只读预检结论.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策与评证专项正式只读预检结论.md)
40. [GlobalCloud智能体团队首轮实施前验证入口判断.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队首轮实施前验证入口判断.md)
41. [GlobalCloud绿色供应链体系模块实施分级判定表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系模块实施分级判定表.md)
41. [GlobalCloud智能体团队运行与实施环境总体规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队运行与实施环境总体规范.md)
42. [GlobalCloud智能体团队工作区与项目仓库操作规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队工作区与项目仓库操作规范.md)
43. [GlobalCloud智能体团队Codex工具与技能使用治理规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队Codex工具与技能使用治理规范.md)
44. [GlobalCloud智能体团队软件全过程实施与交付控制规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队软件全过程实施与交付控制规范.md)
41. [GlobalCloud智能体团队首轮实施前验证包总表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队首轮实施前验证包总表.md)
42. [宪衡专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/宪衡专项首轮实施前验证包.md)
43. [链同专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项首轮实施前验证包.md)
44. [厂行专项首轮实施前验证包.md](06-workstreams/%E5%8E%82%E8%A1%8C%E4%B8%93%E9%A1%B9%E9%A6%96%E8%BD%AE%E5%AE%9E%E6%96%BD%E5%89%8D%E9%AA%8C%E8%AF%81%E5%8C%85.md)
45. [数枢专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/数枢专项首轮实施前验证包.md)
46. [知源专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项首轮实施前验证包.md)
47. [灵策与评证专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策与评证专项首轮实施前验证包.md)
48. [GlobalCloud绿色供应链体系界面分阶段治理规则.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面分阶段治理规则.md)
49. [GlobalCloud绿色供应链体系统一体验骨架规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系统一体验骨架规范.md)
50. [GlobalCloud绿色供应链体系最终交付界面规范与样式规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系最终交付界面规范与样式规范.md)
51. [GlobalCloud绿色供应链体系对话模式与操作模式规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系对话模式与操作模式规范.md)
52. [GlobalCloud绿色供应链体系统一组件与设计令牌规范.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系统一组件与设计令牌规范.md)
53. [GlobalCloud绿色供应链体系界面实施差距清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面实施差距清单.md)
54. [GlobalCloud绿色供应链体系统一组件库建设计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系统一组件库建设计划.md)
55. [GlobalCloud绿色供应链体系首批统一组件清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批统一组件清单.md)
56. [GlobalCloud绿色供应链体系高风险模块界面收口计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系高风险模块界面收口计划.md)
57. [GlobalCloud绿色供应链体系高风险模块界面收口任务分解表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系高风险模块界面收口任务分解表.md)
58. [GlobalCloud绿色供应链体系首批统一组件验收标准.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批统一组件验收标准.md)
59. [GlobalCloud绿色供应链体系P0最小闭环界面实施清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系P0最小闭环界面实施清单.md)
60. [GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵.md)
61. [GlobalCloud绿色供应链体系平台订单-签收-异常界面收口专项方案.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系平台订单-签收-异常界面收口专项方案.md)
62. [GlobalCloud绿色供应链体系高风险模块样板页清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系高风险模块样板页清单.md)
63. [GlobalCloud绿色供应链体系首批统一组件接入样板清单.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批统一组件接入样板清单.md)
64. [GlobalCloud绿色供应链体系样板页实施计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系样板页实施计划.md)
65. [GlobalCloud绿色供应链体系首批组件接入实施计划.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系首批组件接入实施计划.md)
66. [GlobalCloud绿色供应链体系界面实施排期表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面实施排期表.md)
67. [GlobalCloud绿色供应链体系界面实施责任分配表.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系界面实施责任分配表.md)

## 0.10 项目群治理状态（2026-06-10 交叉分析）

基于对 GlobalCloud V0.0.1 下 11 个项目的全量扫描与交叉分析，当前治理状态如下。详细分析见 [GlobalCloud项目群交叉分析报告](01-architecture/GlobalCloud%E9%A1%B9%E7%9B%AE%E7%BE%A4%E4%BA%A4%E5%8F%89%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A.md)。

### 项目群状态一览

| 项目 | 定位 | Harness评分 | 治理状态 | 关键问题 |
|------|------|------------|---------|---------|
| GFIS | 工厂执行系统 | 96/100 | ready_for_human_acceptance | 最成熟，4分外部证据缺口 |
| XiaoC | 提示词工程服务 | 78/100 | partial | UI测试阻塞 + Wrangler未安装 |
| GPC | 供应链公共服务平台 | - | not_started | docs/含GFIS品牌文档，CHANGELOG标题仍为GFIS |
| PVAOS | 运营与门户底座 | - | not_started | Manifest为模板占位 |
| WAES | 治理/证据/AI越权控制 | - | not_started | Manifest为模板占位，remote仍为本地 |
| Brain | 知识主存/LLM Wiki | - | 基础Manifest | 与WIKI并存违反唯一真源原则 |
| WIKI | 知识库(Wiki空间) | - | not_started | 与Brain几乎完全相同，需收口 |
| GPCF | 体系文档工作区 | - | not_started | 本工作区，Manifest为模板占位 |
| 开发控制台 | Harness Engineering控制台 | - | 无Manifest | 自身即模板来源 |
| XGD | 数字意识框架(AI Agent) | - | 无Manifest | 未纳入治理体系 |
| XiaoG | 本地语音助手 | - | 无Manifest | 未纳入治理体系 |

### 优先行动

1. **P0**：Brain/WIKI 收口——WIKI 标注为 Brain 镜像，消除知识主存歧义
2. **P0**：GPC 文档分类——将 docs/ 下 GFIS 品牌文档标注为 "historical reference"
3. **P0**：GPC CHANGELOG 标题修正——从 "GFIS" 修正为 "GPC"
4. **P1**：XGD、XiaoG 补充 PROJECT_HARNESS_MANIFEST.md
5. **P1**：GPCF Manifest 从占位升级为详细配置
6. **P2**：PVAOS/WAES/WIKI Manifest 补齐详细 CLI/反馈/上下文配置

### 覆盖结论

- 11/11 项目已全部纳入 GitHub Jiumilu 组织，remote 统一
- 9/11 有 openspec 配置，XiaoG 待补齐
- 8/11 同步 opsx-full-cycle v1.1，XiaoG/开发控制台/WIKI 独立演进
- 仅 2/11 有量化 Harness 评分(GFIS 96, XiaoC 78)，其余需推进
- 1 项严重冗余(Brain↔WIKI)，1 项文档混用(GPC↔GFIS docs)，2 项治理缺口(XGD,XiaoG 无 Manifest)
