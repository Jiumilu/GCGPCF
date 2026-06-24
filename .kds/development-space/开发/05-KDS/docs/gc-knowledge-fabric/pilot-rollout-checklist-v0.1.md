---
doc_id: GPCF-DOC-D452EC530A
title: GC-Knowledge Fabric 试点推进清单 v0.1
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/pilot-rollout-checklist-v0.1.md
source_path: docs/gc-knowledge-fabric/pilot-rollout-checklist-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 试点推进清单 v0.1

## 1. 试点边界

本清单用于推进葛化 P1 和湖北磷材 P2 试点准备。所有事项在 P0/P1/P2 阶段均保持 candidate、dry-run、metadata-only、no-write 和 evidence-first 边界。

## 2. 葛化 P1 GFIS 母版清单

### 2.1 资料目录

| 资料类别 | 默认处理 | 责任路径 |
|---|---|---|
| 建设资料 | 入 KDS，挂产能池、装备池、数据池 | 项目负责人确认 |
| 工厂运营资料 | 入 KDS，挂产能池、数据池、场景池 | 运营负责人确认 |
| 订单资料 | 入 KDS，挂订单池、产能池、资金池 | 订单负责人确认 |
| 辽宁远航链路资料 | 入 KDS，挂订单池、运力池、客户侧责任边界 | 项目/客户侧确认 |
| 现代精工 OEM 过渡资料 | 入 KDS，挂产能池、质量/交付责任边界 | 工厂/OEM 双方确认 |
| 质量资料 | 默认 metadata-only 或受限引用 | 质量负责人确认 |
| 发货/POD | 默认 metadata-only | 交付负责人确认 |
| 金融凭证 | 默认 metadata-only 或 blocked | 财务负责人确认 |

### 2.2 GFIS 三类助手

| 助手 | P1 能力 | 禁止事项 |
|---|---|---|
| GFIS 知识问答助手 | 回答已准入知识、提示证据缺口、说明风险 | 不确认事实、不判断收益、不归责 |
| GFIS 使用助手 | 解释流程、字段、状态、人工确认点和 WAES 门禁 | 不替代业务负责人写回 |
| GFIS 文档验收助手 | 检查完整性、来源、证据、缺口、敏感资料、RAG 准入 | 不直接验收通过 |

### 2.3 P1 验收闭环

```text
真实资料目录
-> 候选事实样例
-> WAES 判断
-> 人工确认路径
-> GFIS 写回候选 dry-run
-> Harness evidence
```

P1 验收前必须确认：

- 敏感资料不暴露原文。
- 预运营期目标工厂与 OEM 承接方责任可区分。
- AI 输出保持 candidate。
- GFIS 写回保持 dry-run/no-write。

## 3. 湖北磷材 P2 并行线清单

### 3.1 知识库目录

| 知识库 | 内容范围 | 默认挂池 |
|---|---|---|
| 拓厂项目知识库 | 选址、建设条件、设备需求、产线规划、项目资料、合作单位、政策、风险、预运营准备 | 场景池、产能池、装备池、政策池 |
| 原料/行业/订单知识库 | 磷材原料、市场供需、价格、上下游客户、销售订单、采购订单、渠道资源、政策影响 | 原料池、订单池、政策池、资金池 |
| 新工厂复制模板 | 建设、订单、产能、质量、发货、POD、财务凭证闭环 | 场景池、产能池、订单池、数据池 |

### 3.2 P2 验收闭环

```text
拓厂知识包
-> 原料/行业/订单知识包
-> 新工厂复制模板
-> 潜在收益/渠道贡献台账
-> WAES/RAG/LOOP evidence
```

P2 禁止事项：

- 不把葛化模板自动转成湖北磷材事实。
- 不把潜在产值自动转正式收益。
- 不跳过来源、证据、WAES 和人工确认。
- 不默认开放跨单位明细。

## 4. 共同待办

| 编号 | 待办 | 适用试点 | 状态 |
|---|---|---|---|
| C-01 | 指定资料负责人和确认负责人 | 葛化/湖北磷材 | 待确认 |
| C-02 | 建立首批资料目录和编号规则 | 葛化/湖北磷材 | 待执行 |
| C-03 | 标注敏感资料和 metadata-only 对象 | 葛化/湖北磷材 | 待执行 |
| C-04 | 建立候选事实样例 | 葛化 | 待执行 |
| C-05 | 建立 WAES gate 样例 | 葛化/湖北磷材 | 待执行 |
| C-06 | 建立潜在收益和渠道贡献台账 | 湖北磷材 | 待执行 |
| C-07 | 建立 LOOP evidence 记录 | 葛化/湖北磷材 | 待执行 |

## 5. 阻塞项

| 阻塞项 | 影响 | 处理方式 |
|---|---|---|
| 资料负责人未明确 | 无法确认来源和责任 | 人工指定 owner |
| 敏感资料分类不完整 | RAG/助手可能越权 | 默认 metadata-only 或 blocked |
| 证据链缺失 | 不能正式入账 | 进入 repair_required 和 KWE work item |
| 收益口径不清 | 不能进入正式收益 | 只登记潜在收益或知识贡献 |
| 责任边界不清 | 不能归责或写回 | 进入人工/委员会路径 |

## 6. 下一步

1. 由业务侧确认葛化和湖北磷材资料负责人。
2. 先提交目录和元数据，不提交敏感原文。
3. 按 KDS 十一池完成首批挂接。
4. 对高风险资料先跑 WAES gate。
5. 形成第一批 dry-run 验收样例。
