---
doc_id: GPCF-DOC-E3822328DF
title: GlobalCloud Loop 开发 KDS 关联数据检索机制
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud Loop开发KDS关联数据检索机制.md
source_path: 03-data-ai-knowledge/GlobalCloud Loop开发KDS关联数据检索机制.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop 开发 KDS 关联数据检索机制

日期：2026-06-13
状态：v1.0
用途：规定 Loop 开发过程中如何使用 KDS `开发` 空间进行受控数据检索，服务项目群最小闭环开发的数据需求、字段口径、SOP、证据规则和历史案例引用。

---

## 1. 核心结论

KDS 关联数据检索是 Loop 开发的前置输入机制。每个涉及真实项目仓代码、配置、测试、契约、mock、dry-run 或 evidence 的 Loop 实质轮次，都必须先形成 KDS 关联数据检索清单。

KDS 的定位：

```text
KDS 提供开发口径、字段语义、SOP、历史案例、证据规则、对象契约和引用回指。
GPC / GFIS / WAES / PVAOS 等业务系统提供当前业务事实。
```

KDS 不得被当作业务主账、验收结论或生产事实来源。

---

## 2. 适用范围

本机制适用于以下 Loop 场景：

| 场景 | 是否必须检索 KDS | 说明 |
|---|---|---|
| L3 单项目真实闭环 | 是 | 用于确认字段、SOP、测试样本和 evidence 规则 |
| L4 项目群最小闭环 | 是 | 用于确认跨项目契约、样品确认、转量产、异常、复盘等口径 |
| L3.5 API dry-run | 是 | 用于确认 API contract、禁止动作、mock 数据口径 |
| 文档治理轮 | 视情况 | 若只做台账生成可不检索业务资料，但必须读取控制文档 |
| 真实生产写入 | 不适用 | KDS 检索不能授权生产写入，仍需专项人工确认 |

---

## 3. 每轮检索目标

每个实质开发轮至少检索以下 6 类信息：

1. **对象与字段口径**：如 PlatformOrder、SampleRequest、SampleWorkOrder、ProductionRelease、FactoryOrder、ProofOfDelivery。
2. **状态与门禁口径**：如待打样、打样中、待客户确认、已签样、驳回、已转量产、异常关闭。
3. **SOP 与流程规则**：如报价、订单评审、配方研发、样箱打样、客户签样、转量产、质检、发货、签收。
4. **证据要求**：如签样文件、检测结果、转量产放行、WAES 审计、evidence 回指。
5. **历史案例与风险**：如样品驳回、质量异常、客户投诉、转量产风险、异常复盘。
6. **跨项目依赖**：生产者、消费者、允许动作、禁止动作、验证方式、回滚方式。

---

## 4. 最小闭环重点检索词

| 闭环节点 | KDS 检索词 |
|---|---|
| 项目初始化 | 项目初始化、租户、组织、伙伴、项目空间、角色、权限、发布验证 |
| 平台订单 | 平台订单、订单评审、报价、合同、客户需求、PlatformOrder |
| 样品确认 | 样品申请、配方研发、样箱打样、客户签样、样品检测、SampleRequest、SampleWorkOrder、SampleApproval |
| 转量产 | 转量产、生产放行、ProductionRelease、客户确认、豁免、门禁 |
| 工厂订单 | 工厂订单、FactoryOrder、OrderMapping、工单、齐套、生产需求 |
| 质量库存批次 | 质量检验、库存、批次、追溯、CAPA、QualityInspection |
| 发货签收 | 发货、POD、签收、回单、ProofOfDelivery、争议 |
| 异常复盘 | 异常、关闭、复盘、责任人、影响范围、SOP、案例 |
| WAES 证据 | evidence、审计、状态门禁、越权阻断、治理确认 |
| KDS 沉淀 | SOP、案例、引用回指、知识发布、版本、权限 |

---

## 5. 检索来源优先级

KDS 检索必须按以下优先级引用资料：

1. 受控架构与主线文档。
2. 对象目录、事件合同、连接器合同。
3. SOP 模板库、数据治理模型、知识主存分层方案。
4. WAES 状态、证据、验收与门禁文档。
5. 项目级 evidence 和 loop-state。
6. 历史案例、复盘、培训资料提取内容。
7. 草案文档。

草案内容只能作为候选参考，不得直接作为实现和验收依据。

---

## 6. KDS 检索清单模板

每轮 Loop 必须形成以下结构：

```yaml
kds_retrieval:
  required: true
  status: planned | completed | skipped_with_reason | blocked
  retrieval_mode: local_mirror | kds_api_readonly | kds_api_dry_run
  round_id:
  business_node:
  target_projects:
  query_terms:
    - ""
  source_documents:
    - doc_id:
      title:
      source_path:
      kds_path:
      status:
      relevance:
  retrieved_objects:
    - name:
      owner_project:
      fields:
      source:
  retrieved_statuses:
    - name:
      allowed_transitions:
      blocked_transitions:
      source:
  retrieved_sop:
    - sop_id:
      summary:
      source:
  retrieved_evidence_rules:
    - evidence_type:
      required_fields:
      source:
  development_data_needs:
    - need:
      consumer_project:
      producer_project:
      data_shape:
      verification_method:
  mock_data_needs:
    - scenario:
      fields:
      boundary_cases:
  unresolved_questions:
    - question:
      owner:
      stop_required: true | false
  kds_followup_updates:
    - candidate_update:
      target_doc:
      reason:
```

---

## 7. 开发轮执行流程

每轮实质开发按以下顺序执行：

```text
1. 读取 Round 目标和业务节点。
2. 生成 KDS 检索词。
3. 检索 KDS 本地镜像或受控 KDS API。
4. 形成 KDS 关联数据检索清单。
5. 转换为本轮开发数据需求。
6. 在真实项目仓实现代码、配置、测试、契约或 dry-run。
7. 运行验证命令。
8. 写入项目级 evidence。
9. 写入项目群 evidence。
10. 将新增知识、缺口或冲突登记为 KDS 候选更新。
```

若 KDS 检索失败：

- 可使用本地镜像 fallback。
- 若本地镜像也缺失关键口径，本轮状态最高为 `blocked` 或 `partial`。
- 不得用臆测字段、臆测状态机或临时 mock 伪装为受控口径。

---

## 8. 质量门禁

KDS 检索结果必须满足：

| 门禁 | 要求 |
|---|---|
| 来源受控 | 至少 1 个 controlled 文档作为主依据 |
| 引用可追溯 | 记录 doc_id、source_path 或 kds_path |
| 业务边界清楚 | 区分 KDS 语义口径与业务系统事实 |
| 数据需求明确 | 输出 development_data_needs 或 mock_data_needs |
| 证据规则明确 | 输出 evidence 类型和必填字段 |
| 冲突已登记 | 不一致内容必须进入 unresolved_questions |

不满足上述门禁时，不得计为 L3/L4 实质开发轮完成。

---

## 9. 安全边界

禁止事项：

1. 禁止把 KDS 检索结果当作 GFIS/GPC/WAES 当前业务事实。
2. 禁止把 KDS 检索结果当作生产写入授权。
3. 禁止在文档、日志、evidence 中写入真实 KDS TOKEN。
4. 禁止自动删除或覆盖 KDS 文档。
5. 禁止把草案资料直接作为验收结论。
6. 禁止把 KDS API dry-run 输出当作真实业务写入完成。

允许事项：

1. 读取 KDS 本地镜像。
2. 在 TOKEN 校验通过且授权范围内读取 KDS `开发` 空间。
3. 使用 dry-run 验证检索、索引、引用回指或同步计划。
4. 将开发中发现的新字段、新 SOP、新案例登记为候选更新。

---

## 10. 最小闭环提示词要求

任何项目群最小闭环提示词必须包含：

```text
每轮开发前必须执行 KDS 关联数据检索。
检索内容包括对象字段、状态门禁、SOP、证据规则、历史案例、跨项目依赖和 mock 数据口径。
KDS 提供开发语义和受控口径，不替代 GPC/GFIS/WAES 的业务事实。
若 KDS 检索缺失关键口径，本轮不得继续伪造字段或状态，必须登记 unresolved_questions。
每轮 evidence 必须包含 kds_retrieval 清单。
```
