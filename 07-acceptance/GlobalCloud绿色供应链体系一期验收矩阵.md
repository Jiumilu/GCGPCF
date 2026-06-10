# GlobalCloud 绿色供应链体系一期验收矩阵

日期：2026-06-07  
状态：一期验收矩阵 v1  
验收口径：验证“生态入口/平台订单 -> GPC-Native 协同 -> GFIS 工厂执行 -> GPC-Native 运输签收 -> WAES 证据台账和复盘”的最小闭环。

## 1. 验收原则

1. **不能用页面存在代替闭环完成**。
2. **不能用 AI 建议代替业务事实**。
3. **不能用旧报告代替当前证据**。
4. **不能把 GFIS/GPC-Native/WAES 的边界混在一起**。
5. **每个场景必须有来源记录、事件、证据和确认点**：事务确认在 GFIS/GPC-Native，治理确认、证据确证和状态升级在 WAES/Harness。
6. **未完成真实运行态联调前，状态只能是 `partial` 或 `ready_for_human_acceptance`，不能是 `complete`。**
7. **平台通过不等于业务通过**：`GPC-Native`、`WAES`、连接器或控制塔通过，只表示平台层和治理层通过；业务是否完成仍取决于 `GFIS/GPC-Native` 主责回执。

## 2. 一期主链路

```text
生态入口/平台订单
-> GPC-Native 订单协同
-> GFIS 工厂订单确认
-> 齐套检查
-> 工单
-> 备料和线边配送
-> 生产报工
-> 质量检验
-> 成品入库
-> 发货出库
-> GPC-Native 运输和签收
-> WAES 证据台账和异常复盘
```

## 3. 验收场景总表

| 编号 | 场景 | 参与系统 | 完成判定 | 优先级 |
|---|---|---|---|---|
| A1 | 一张平台订单到客户签收 | PVAOS / GPC-Native / GFIS / WAES | 平台订单、工厂订单、工单、质检、发货、运输、POD、证据全部闭环 | P0 |
| A2 | 一批物料从供应商到成品客户追溯 | GPC-Native / GFIS / WAES | 批次可追溯到供应商、ASN、工单、成品、发货、客户 | P0 |
| A3 | 一次缺料风险预警与补料建议 | GFIS / WAES / Agent | 缺料事件、AI 建议、GFIS 事务确认、补料任务、执行回执闭环 | P0 |
| A4 | 一次线边配送闭环 | GFIS / WAES / XGD | 配送任务创建、派发、执行、确认、证据闭环 | P0 |
| A5 | 一次质量异常闭环 | GFIS / WAES / Brain / Agent | 不合格、隔离、处理、CAPA、复盘、关闭验收 | P0 |
| A6 | 一次运输签收异常闭环 | GPC-Native / GFIS / WAES | 延迟或争议签收、异常工单、处理、POD 修正、回传闭环 | P0 |
| A7 | 一份 WAES 生产/物流/交付日报 | WAES / GFIS / GPC-Native / Brain / XiaoC | 日报引用真实来源记录和证据，不含未确证事实 | P1 |
| A8 | 一次设备异常建单、维修、关闭 | GFIS / WAES / XGD | 停机事件、维修工单、维修记录、验收、复盘闭环 | P1 |
| A9 | 一次 AI 建议被治理规则驳回且不写业务事实 | WAES / Agent / GFIS / GPC-Native | 建议有证据、被治理规则或人工确认驳回后无业务主账写入 | P1 |

## 4. 详细验收矩阵

### A1 一张平台订单到客户签收

| 项 | 内容 |
|---|---|
| 目标 | 验证从生态入口/平台订单到 GFIS 工厂执行、GPC-Native 运输签收、WAES 证据台账的完整闭环 |
| 参与系统 | PVAOS、GPC-Native、GFIS、WAES |
| 前置条件 | 客户、供应商、工厂、物料、仓库、承运商、车辆、月台、用户权限已建立 |
| 操作步骤 | 1. PVAOS/GPC-Native 创建平台订单；2. GPC-Native 分发到 GFIS；3. GFIS 确认工厂订单；4. GFIS 齐套检查；5. GFIS 释放工单；6. GFIS 完成生产报工；7. GFIS QMS 合格放行；8. GFIS 成品入库；9. GFIS 发货出库；10. GPC-Native 创建运输记录；11. GPC-Native 完成在途和签收；12. WAES 收集证据 |
| 期望结果 | 订单、工单、批次、质检、发货、运输、POD、证据均能通过 traceId 串联 |
| 证据类型 | 业务记录、事件、POD、截图、日志、WAES EvidenceRecord |
| 来源系统 | GPC-Native、GFIS、WAES |
| 确认点 | 工厂订单确认、质量放行、发货出库、客户签收均在 GFIS/GPC-Native；WAES 只确认证据链和验收口径 |
| 阻塞条件 | 任一主责事实缺失；POD 未形成；WAES 无证据链；AI 自动写入主账 |
| 完成判定 | 端到端链路全部有来源记录和证据，且无越权写入 |

### A2 一批物料从供应商到成品客户追溯

| 项 | 内容 |
|---|---|
| 目标 | 验证物料批次可从供应商、ASN、收货、质检、生产、成品、发货追溯到客户 |
| 参与系统 | GPC-Native、GFIS、WAES |
| 前置条件 | 供应商、ASN、物料、批次、BOM、工单、客户订单已存在 |
| 操作步骤 | 1. GPC-Native 创建 ASN；2. GFIS 收货并生成批次；3. GFIS 来料质检；4. GFIS 合格入库；5. GFIS 工单领料；6. GFIS 生产成品批次；7. GFIS 成品质检；8. GFIS 发货出库；9. GPC-Native 签收；10. WAES 展示追溯链 |
| 期望结果 | 批次能追溯到供应商、ASN、工单、成品批次、客户和 POD |
| 证据类型 | ASN、收货记录、QualityInspection、InventoryTransaction、WorkOrder、FactoryShipmentRelease、POD |
| 来源系统 | GPC-Native、GFIS |
| 确认点 | 来料质检、成品质检、异常批次处置在 GFIS；WAES 只确认证据可追溯 |
| 阻塞条件 | 批次断点、质量状态缺失、库存事务缺失、发货与批次不一致 |
| 完成判定 | WAES 能展示完整追溯链，且每个节点可回到来源记录 |

### A3 一次缺料风险预警与补料建议

| 项 | 内容 |
|---|---|
| 目标 | 验证 GFIS 缺料事件、AI 建议、人工确认和补料执行闭环 |
| 参与系统 | GFIS、WAES、Hermes/XGD、XiaoC |
| 前置条件 | 工单、BOM、库存、线边库存、配送资源已存在 |
| 操作步骤 | 1. GFIS 执行齐套检查；2. GFIS 触发 `gfis.kitting_check.shortage_detected`；3. WAES 生成风险；4. AI 生成补料建议；5. 调度员确认；6. GFIS 创建补料/配送任务；7. 任务完成后回执到 WAES |
| 期望结果 | AI 只生成建议，不自动创建或关闭补料任务；补料执行由 GFIS 确认 |
| 证据类型 | KittingCheck、AISuggestion、BusinessApprovalReference、LogisticsTask、EvidenceRecord |
| 来源系统 | GFIS、WAES、Hermes/XGD |
| 确认点 | 补料/配送任务确认在 GFIS；WAES 只确认 AI 建议未越权和证据已归档 |
| 阻塞条件 | AI 自动创建任务；无库存证据；无人工确认；任务无回执 |
| 完成判定 | 缺料预警、建议、确认、任务、回执和复盘完整 |

### A4 一次线边配送闭环

| 项 | 内容 |
|---|---|
| 目标 | 验证 LES 线边配送从创建到关闭 |
| 参与系统 | GFIS、WAES、XGD |
| 前置条件 | 工单已释放，物料合格可用，线边库位和配送资源已配置 |
| 操作步骤 | 1. GFIS 根据工单生成 LineSideDelivery；2. 仓库拣货；3. 配送任务派发；4. AGV/叉车/人工执行；5. 线边确认；6. GFIS 更新线边库存；7. WAES 展示准时率和异常 |
| 期望结果 | 配送任务状态完整，库存变化和线边确认可追踪 |
| 证据类型 | LineSideDelivery、LogisticsTask、LineSideStock、InventoryTransaction、EvidenceRecord |
| 来源系统 | GFIS、WAES |
| 确认点 | 线边收货确认、异常改派确认在 GFIS；WAES 只展示风险和证据 |
| 阻塞条件 | 无任务状态；无库存回写；无线边确认；任务超时未升级 |
| 完成判定 | 创建、派发、执行、确认、关闭全部有记录 |

### A5 一次质量异常闭环

| 项 | 内容 |
|---|---|
| 目标 | 验证不合格品从识别、隔离、处理、CAPA 到复盘 |
| 参与系统 | GFIS、WAES、Brain、Hermes/XGD |
| 前置条件 | 质量检验模板、隔离仓、责任岗位、CAPA 流程已配置 |
| 操作步骤 | 1. GFIS QMS 记录不合格；2. GFIS 批次状态变为 quarantined/rejected；3. GFIS 触发异常；4. WAES 生成异常工单；5. AI 生成 CAPA 草案；6. 质量负责人确认处理；7. 处理完成并复盘；8. Brain 收录复盘候选 |
| 期望结果 | AI 不自动质量放行；不合格品被隔离；CAPA 有人工确认 |
| 证据类型 | QualityInspection、MaterialLot、ExceptionCase、AISuggestion、CAPA 记录、KnowledgeEntry |
| 来源系统 | GFIS、WAES、Brain |
| 确认点 | 不合格处置、CAPA、关闭验收在 GFIS/QMS；WAES 只归档复盘证据和治理结论 |
| 阻塞条件 | AI 自动放行；批次未隔离；CAPA 无确认；复盘无证据 |
| 完成判定 | 异常处理闭环，且复盘进入 Brain 候选知识 |

### A6 一次运输签收异常闭环

| 项 | 内容 |
|---|---|
| 目标 | 验证运输延迟、客户拒收、数量争议或回单缺失的闭环 |
| 参与系统 | GPC-Native、GFIS、WAES、Hermes/XGD |
| 前置条件 | Shipment、车辆、承运商、客户、POD 模板已存在 |
| 操作步骤 | 1. GPC-Native 记录运输异常；2. 触发 `gpc.external_exception.raised`；3. WAES 生成异常工单；4. AI 生成原因分析和处理建议；5. 物流/客服确认处理；6. GPC-Native 更新签收或争议状态；7. 回传 GFIS；8. WAES 归档证据 |
| 期望结果 | 异常不直接改变 GFIS 发货事实；POD 争议状态可追踪 |
| 证据类型 | Shipment、TransitCheckpoint、ProofOfDelivery、ExternalException、BusinessApprovalReference、EvidenceRecord |
| 来源系统 | GPC-Native、GFIS、WAES |
| 确认点 | 客户签收争议处理、数量差异确认、交期承诺变更在 GPC-Native；WAES 只引用业务处理结果并归档证据 |
| 阻塞条件 | 无 POD；客户签收被 AI 自动确认；争议无处理记录 |
| 完成判定 | 异常有处理链，POD 和回传状态一致 |

### A7 一份 WAES 生产/物流/交付日报

| 项 | 内容 |
|---|---|
| 目标 | 验证 WAES 能基于真实来源记录生成日报 |
| 参与系统 | WAES、GFIS、GPC-Native、Brain、XiaoC、Hermes/XGD |
| 前置条件 | 已完成至少一条订单到签收链路，指标定义已配置 |
| 操作步骤 | 1. WAES 汇总 GFIS/GPC-Native 事件；2. 计算订单、生产、质量、物流、交付指标；3. AI 生成日报草案；4. 人工审阅；5. 证据引用归档 |
| 期望结果 | 日报每个结论都有来源记录或 EvidenceRecord |
| 证据类型 | MetricSnapshot、EvidenceRecord、AISuggestion、日报文档 |
| 来源系统 | WAES、GFIS、GPC-Native |
| 确认点 | 日报发布或对外发送属于 WAES 治理确认；不改变业务事实 |
| 阻塞条件 | 日报含无证据结论；AI 将建议写成事实；指标口径不明 |
| 完成判定 | 日报可追溯、可审计、无越权承诺 |

### A8 一次设备异常建单、维修、关闭

| 项 | 内容 |
|---|---|
| 目标 | 验证设备异常对生产/物流调度的影响闭环 |
| 参与系统 | GFIS、WAES、XGD、Brain |
| 前置条件 | 设备台账、点检规则、维修岗位、备件记录已配置 |
| 操作步骤 | 1. GFIS 记录设备异常；2. WAES 展示风险；3. AI 生成维修建议；4. 设备负责人确认；5. GFIS 建维修工单；6. 维修完成并验收；7. WAES 复盘停机影响 |
| 期望结果 | AI 不自动停机/验收；设备状态影响工单或物流能力判断 |
| 证据类型 | Equipment、MaintenanceOrder、AISuggestion、EvidenceRecord |
| 来源系统 | GFIS、WAES、Brain |
| 确认点 | 维修建议确认、维修关闭验收在 GFIS/EAM；WAES 只复盘停机影响和证据 |
| 阻塞条件 | AI 自动停机；维修无验收；设备状态未影响调度判断 |
| 完成判定 | 异常、维修、验收、复盘全部闭环 |

### A9 一次 AI 建议被治理规则驳回且不写业务事实

| 项 | 内容 |
|---|---|
| 目标 | 验证 AI 越权防线 |
| 参与系统 | WAES、Hermes/XGD、GFIS、GPC-Native |
| 前置条件 | AI 建议、治理规则、业务系统连接器已配置 |
| 操作步骤 | 1. AI 生成发货批次替换或交期调整建议；2. WAES 按治理规则标记为 L4；3. 治理规则或人工确认驳回；4. 检查 GFIS/GPC-Native 无业务主账写入；5. 建议关闭并归档 |
| 期望结果 | 被驳回建议不产生业务事实事件 |
| 证据类型 | AISuggestion、GovernanceApproval、事件日志、业务系统查询结果 |
| 来源系统 | WAES、GFIS、GPC-Native |
| 确认点 | 治理规则命中或人工治理确认 |
| 阻塞条件 | AI 建议绕过治理规则写入业务系统；没有驳回证据 |
| 完成判定 | 建议被驳回后无主账变化，证据完整 |

## 5. 四流优化扩展验收场景

以下场景根据四流综合架构新增，用于把治理规则、连接器、数据治理、AI 服务、多厂协同、知识主存发布、数据库边界和模型治理纳入一期后续验收扩展。A10-A13 建议进入 P0，A14-A17 建议进入 P1，A18-A24 进入 P2。

| 编号 | 场景 | 参与系统 | 完成判定 | 优先级 |
|---|---|---|---|---|
| A10 | 一次治理规则生效、命中和回滚 | WAES / Harness / GFIS / GPC-Native | `GovernanceRuleVersion` 生效、命中记录、回滚记录和证据完整 | P0 |
| A11 | 一次连接器降级与恢复 | WAES / Connector Registry / GFIS / GPC-Native | 连接器降级、业务影响、恢复、补偿和证据完整 | P0 |
| A12 | 一次事件死信与重放 | Event Bus / WAES / SourceSystem | `DeadLetterRecord`、`ReplayRequest`、`ReplayRun` 和重放结果完整 | P0 |
| A13 | 一次 AI 越权拦截 | WAES / Hermes / XGD / GFIS / GPC-Native | `ai.overreach.blocked` 产生，业务主账无变化，建议关闭或补证 | P0 |
| A14 | 一次 SOP 版本冻结和回滚 | WAES / Brain / GFIS / GPC-Native | SOP 冻结、回滚、影响范围、执行版本和证据完整 | P1 |
| A15 | 一次一链多厂订单分发 | GPC-Native / GFIS / WAES | `FactoryAllocation`、`CapacityCommitment`、GFIS 接单确认和证据完整 | P1 |
| A16 | 一次 Edge 断网缓存补传 | Edge / GFIS / WAES | 缓存、去重、补传、回执和 trace 连贯 | P1 |
| A17 | 一次指标口径变更和重算 | WAES / Data Platform / GFIS / GPC-Native | 口径版本、重算范围、血缘、旧口径冻结和证据完整 | P1 |
| A18 | 一次多租户或多链数据隔离验证 | PVAOS / WAES / GPC-Native / GFIS / Agent | 越权查询被阻断，AI 无跨租户证据泄露 | P2 |
| A19 | 一次知识发布、ingest 与失效拦截 | 知识主存 / LLM Wiki / GBrain / Brain / WAES | 知识版本生效、索引完成、失效版本被拦截 | P2 |
| A20 | 一次数据库边界与读模型隔离验证 | PVAOS / GPC-Native / GFIS / WAES / Data Platform | 无跨系统直写主账，读模型可查询且不反写主账 | P2 |
| A21 | 一次模型授权变更与生效验证 | WAES / XiaoC / Hermes | `ModelAuthorizationGrant` 变更后新调用按授权生效，旧越界调用被阻断 | P2 |
| A22 | 一次模型路由、降级与回退验证 | XiaoC / WAES / Hermes | `ModelRouteDecision`、回退原因、证据和影响范围完整 | P2 |
| A23 | 一次模型使用计量与统计回指验证 | XiaoC / Hermes / WAES / Data Platform | `ModelUsageRecord` 与 `ModelMeterSnapshot` 可回指且口径一致 | P2 |
| A24 | 一次模型越权或超预算拦截验证 | WAES / XiaoC / Hermes / Human | `ai.model_overreach.blocked` 产生且无未授权模型调用落地 | P2 |

### A10 治理规则生效、命中和回滚

| 项 | 内容 |
|---|---|
| 目标 | 验证治理规则从草案、生效、命中、冻结到回滚的完整生命周期 |
| 参与系统 | WAES、Harness、GFIS、GPC-Native |
| 前置条件 | 已存在 `GovernanceRule`、`GovernanceRuleVersion`、`PolicyAssignment` |
| 操作步骤 | 1. WAES 创建规则版本；2. 绑定到项目或连接器；3. 规则生效；4. 触发业务事件命中规则；5. 生成治理证据；6. 回滚到上一版本 |
| 确认点 | 规则生效、回滚和状态变更属于 WAES/Harness 治理确认；业务动作仍由 GFIS/GPC-Native 确认 |
| 完成判定 | 规则版本、命中审计、回滚记录、证据和状态审计齐全 |

### A11 连接器降级与恢复

| 项 | 内容 |
|---|---|
| 目标 | 验证连接器故障不会被误判为业务完成，并能进入治理降级、恢复和补偿流程 |
| 参与系统 | WAES、Connector Registry、Event Bus、GFIS、GPC-Native |
| 前置条件 | 连接器合同、健康检查、重试和死信策略已配置 |
| 操作步骤 | 1. 模拟连接器失败；2. 生成 `ConnectorLifecycleRecord`；3. 进入 degraded；4. 事件进入 retry 或 DLQ；5. 恢复连接器；6. 完成补偿或重放 |
| 确认点 | 连接器上线、下线、降级、恢复需要 WAES 治理确认；不替代业务事务确认 |
| 完成判定 | 降级、恢复、补偿、死信或重放记录完整 |

### A12 事件死信与重放

| 项 | 内容 |
|---|---|
| 目标 | 验证失败事件可追踪、可审批重放、可恢复指标和证据链 |
| 参与系统 | Event Bus、WAES、SourceSystem、Harness |
| 前置条件 | `DeadLetterRecord`、`ReplayRequest`、`ReplayRun` 已定义 |
| 操作步骤 | 1. 制造消费失败；2. 生成死信；3. WAES 发起重放请求；4. 治理确认；5. Event Bus 重放；6. WAES 校验证据链恢复 |
| 确认点 | 高风险重放需要治理确认；重放不得生成重复业务事实 |
| 完成判定 | 死信、重放、幂等检查、证据链修复全部有记录 |

### A13 AI 越权拦截

| 项 | 内容 |
|---|---|
| 目标 | 验证 Agent 调用禁止工具或尝试写业务主账时被 WAES 拦截 |
| 参与系统 | WAES、Hermes、XGD、GFIS、GPC-Native |
| 前置条件 | `AgentToolGrant`、`AgentToolPolicy`、禁止动作清单已配置 |
| 操作步骤 | 1. Agent 尝试质量放行、库存调整或签收确认；2. WAES 检查授权；3. 阻断工具调用；4. 生成 `ai.overreach.blocked`；5. 校验 GFIS/GPC-Native 主账无变化 |
| 确认点 | 越权拦截属于治理事实；业务系统不得产生对应业务完成事件 |
| 完成判定 | 越权事件、工具调用日志、业务主账无变化证据齐全 |

### A19 知识发布、ingest 与失效拦截

| 项 | 内容 |
|---|---|
| 目标 | 验证知识主存域、知识引擎域和 WAES 知识治理闭环 |
| 参与系统 | 知识主存服务、LLM Wiki、GBrain、Brain、WAES |
| 前置条件 | `KnowledgeDocument`、`KnowledgeVersion`、`KnowledgeRelease`、`KnowledgeAccessPolicy` 已定义 |
| 操作步骤 | 1. 创建知识版本；2. 审批并生效；3. 触发 ingest；4. 校验知识引擎可检索；5. 废止旧版本；6. 验证失效版本默认不被 AI 作为首选引用 |
| 确认点 | 知识生效、回滚和失效拦截由知识主存服务与 WAES 治理确认；AI 只消费结果 |
| 完成判定 | 知识发布、索引、引用、失效拦截和审计记录完整 |

### A20 数据库边界与读模型隔离验证

| 项 | 内容 |
|---|---|
| 目标 | 验证结构化数据库域边界、读模型和主账隔离可执行 |
| 参与系统 | PVAOS、GPC-Native、GFIS、WAES、Data Platform |
| 前置条件 | `DatabaseDomain`、`DatabaseAccessPolicy`、`ReadModelProjection` 已定义 |
| 操作步骤 | 1. 校验各系统主账库独立；2. 通过读模型查询跨系统视图；3. 模拟跨系统直写被阻断；4. 验证控制塔视图来自读模型而非共享主账 |
| 确认点 | 读模型只读；主账写入仅限主责系统 |
| 完成判定 | 数据库边界、访问策略、读模型发布和阻断证据完整 |

### A21 模型授权变更与生效验证

| 项 | 内容 |
|---|---|
| 目标 | 验证模型治理授权变更后，新调用按新授权生效，未授权模型被阻断 |
| 参与系统 | WAES、XiaoC、Hermes |
| 前置条件 | `ModelAuthorizationPolicy`、`ModelAuthorizationGrant`、全局模型目录和项目模型引用已定义 |
| 操作步骤 | 1. 为指定项目或 Agent 变更模型授权；2. 发起一次授权内模型调用；3. 发起一次越界模型调用；4. 校验授权内调用成功、越界调用被阻断；5. 核对授权变更事件和证据 |
| 确认点 | 模型授权属于 WAES 治理事实；不改变业务主账事实 |
| 完成判定 | 授权变更、调用结果、阻断证据、审计记录完整 |

### A22 模型路由、降级与回退验证

| 项 | 内容 |
|---|---|
| 目标 | 验证模型路由、失败降级、人工覆盖和回退链条完整 |
| 参与系统 | XiaoC、WAES、Hermes |
| 前置条件 | `ModelCapabilityProfile`、`ModelRouteDecision`、回退策略已配置 |
| 操作步骤 | 1. 发起一次正常模型调用；2. 模拟首选模型不可用或超限；3. 触发降级或切换；4. 记录回退原因；5. 校验最终模型选择和治理证据 |
| 确认点 | 降级、切换和覆盖必须有 `ModelRouteDecision`；不得绕过 WAES 授权 |
| 完成判定 | 路由、降级、回退、影响范围和证据完整 |

### A23 模型使用计量与统计回指验证

| 项 | 内容 |
|---|---|
| 目标 | 验证模型使用记录、token/费用计量和统计快照口径一致且可回指 |
| 参与系统 | XiaoC、Hermes、WAES、Data Platform |
| 前置条件 | `ModelUsageRecord`、`ModelMeterSnapshot`、计量规则已定义 |
| 操作步骤 | 1. 发起多次模型调用；2. 记录 usage、延迟、费用、trace；3. 生成计量快照；4. 从快照回指到单次调用记录；5. 校验项目/Agent/模型维度汇总一致 |
| 确认点 | 计量记录属于治理与审计事实；不作为业务主账事实 |
| 完成判定 | 使用记录、计量快照、回指链和统计口径完整一致 |

### A24 模型越权或超预算拦截验证

| 项 | 内容 |
|---|---|
| 目标 | 验证模型调用因超授权、超预算、超密级或超场景而被 WAES 阻断 |
| 参与系统 | WAES、XiaoC、Hermes、Human |
| 前置条件 | `ModelAuthorizationPolicy`、预算或密级规则、越权拦截策略已配置 |
| 操作步骤 | 1. 发起一次超预算或超密级模型调用；2. WAES 检查授权与预算；3. 阻断调用；4. 生成 `ai.model_overreach.blocked`；5. 核对无未授权调用结果落地 |
| 确认点 | 模型越权拦截属于治理事实；不得把被阻断调用伪装为正常业务完成 |
| 完成判定 | 拦截事件、预算/授权依据、调用日志和审计证据完整 |

## 6. 一期完成定义

一期可以标记为 `ready_for_human_acceptance` 的条件：

1. A1-A6 全部具备当前证据。
2. A7 至少生成内部日报草案并完成证据引用。
3. 所有业务事实均来自主责系统。
4. 所有 L3/L4 治理动作均有治理确认或证据确证记录；具体事务确认由 GFIS/GPC-Native 提供引用。
5. WAES Evidence Ledger 能回指来源记录。
6. AI 未直接写入 GFIS/GPC-Native 主账。
7. 失败、阻塞和未完成项已进入状态审计。

一期可以标记为 `complete` 的条件：

1. 已达到 `ready_for_human_acceptance`。
2. 用户或业务负责人明确验收。
3. 外部 UAT、运行态联调或生产试运行证据齐全。
4. 无 P0 阻塞。
5. 状态审计、证据台账、治理确认记录和业务审批引用全部归档。

不能标记为 `complete` 的情况：

- 只有设计文档，没有运行证据。
- 只有静态 demo，没有业务闭环。
- 只有 AI 生成日报，没有来源证据。
- GFIS/GPC-Native/WAES 任一主链路缺失。
- L4 治理动作缺少治理确认，或具体事务缺少 GFIS/GPC-Native 业务确认引用。
- 仍把 Odoo GPC 当主线底座继续二开。
