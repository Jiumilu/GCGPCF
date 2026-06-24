---
doc_id: GPCF-DOC-788E973803
title: GPCF-KDS-DKS-006 湖北磷材拓厂项目知识库与新工厂复制模板 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-006.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-006.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-KDS-DKS-006 湖北磷材拓厂项目知识库与新工厂复制模板 Loop 记录

日期：2026-06-17
状态：loop_ready / manual_confirmation_required
模式：GPCF 方案治理微循环

## 1. 输入

用户已确认湖北磷材作为第二条并行线，第一阶段不做 GFIS 深度，优先做：

1. 拓厂项目知识库。
2. 原料 / 行业 / 订单知识库。
3. 新工厂复制模板。

上一轮 `GPCF-KDS-DKS-005` 已完成辽宁远航链路证据缺口请求包与知识悬赏草案，并建议本轮进入 HBLC 拓厂模板。

## 2. 动作

本轮执行动作：

1. 建立受控模板文档：
   `03-data-ai-knowledge/GlobalCloud湖北磷材拓厂项目知识库与新工厂复制模板.md`
2. 定义 HBLC 第一阶段知识源目录。
3. 建立 `FactoryExpansionAssessment` 初始权重模型。
4. 建立新工厂复制模板。
5. 建立首批 `AIS-HBLC-*` 建议和 `KGR-HBLC-*` 知识缺口。
6. 明确 HBLC 第一阶段不做 GFIS 深度、不确认订单或原料事实。

## 3. 输出

| 产物 | 路径 | 说明 |
|---|---|---|
| 湖北磷材拓厂项目知识库与新工厂复制模板 | `03-data-ai-knowledge/GlobalCloud湖北磷材拓厂项目知识库与新工厂复制模板.md` | 定义 HBLC 知识源、拓厂评估表、复制模板、AI 建议、知识缺口和密级规则 |
| Loop round 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-006.md` | 记录本轮五段式治理微循环 |

## 4. 检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| GFIS 边界 | pass | HBLC 第一阶段不做 GFIS 深度 |
| 知识源边界 | pass | 只建立 KDS 候选知识源，不确认原料或订单事实 |
| 权重边界 | pass | 评估分只用于排序，不自动决策 |
| 预运营期订单边界 | pass | 高权重加分项，不是一票通过 |
| 密级边界 | pass | S3 字段默认脱敏索引 |
| 状态升级 | pass | 本轮不声明 accepted、complete 或 integrated |

## 5. 反馈

本轮结论：

1. 湖北磷材第一阶段模板已形成。
2. 葛化母版已转化为 HBLC 的拓厂评估和新工厂复制输入。
3. 当前状态仍为 `loop_ready / manual_confirmation_required`。

下一轮建议：

```text
GPCF-KDS-DKS-007：
知识收益治理委员会 DecisionRecord 模板与争议处理表，用于积分、收益、悬赏、密级、负积分和潜在产值贡献的多数决裁决。
```

待用户回答：

1. 湖北磷材第一批拓厂资料是否已有目录或联系人？
2. 原料资料是否优先从 PP 原料、回收料、供应商报价、采购订单开始？
3. 行业知识是否需要接入权威政策/标准网站作为高可信源？
4. 销售订单资料是否允许先做脱敏索引，再进入 KDS 候选？
5. `FEA-HBLC-202606-0001` 的权重是否采用本文建议的 20/20/15/20/10/5/10 初始模型？
