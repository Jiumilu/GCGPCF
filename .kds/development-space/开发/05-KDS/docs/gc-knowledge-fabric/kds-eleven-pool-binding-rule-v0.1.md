---
doc_id: GPCF-DOC-4EE3DDAB80
title: GC-Knowledge Fabric KDS 十一池挂接规则 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kds-eleven-pool-binding-rule-v0.1.md
source_path: docs/gc-knowledge-fabric/kds-eleven-pool-binding-rule-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric KDS 十一池挂接规则 v0.1

## 1. 定位

KDS 十一池用于把知识对象挂接到绿色供应链业务事实底座。P0 阶段，挂池只表示治理归类和后续校验入口，不代表业务事实已确认。

## 2. 十一池

| 池 | poolCode | 典型对象 |
|---|---|---|
| 订单池 | ORDER | 订单事实、客户需求、销售/采购订单 |
| 运力池 | TRANSPORT | 物流、发货、POD、运力节点 |
| 产能池 | CAPACITY | 工厂、产线、产能、OEM 承接 |
| 资金池 | FUND | 到账、开票、合同、金融凭证 |
| 政策池 | POLICY | 政策、标准、合规要求 |
| 装备池 | EQUIPMENT | 设备、产线、工艺装备 |
| 数据池 | DATA | 文档、台账、报告、系统数据 |
| 能源池 | ENERGY | 能耗、碳、绿色能源 |
| 原料池 | MATERIAL | 原料、材料、供应商资源 |
| 人才池 | TALENT | 团队、专家、服务商 |
| 场景池 | SCENARIO | 项目场景、区域机会、应用案例 |

## 3. 默认挂接规则

| 内容类型 | 默认挂池 |
|---|---|
| 订单事实 | ORDER |
| 物流与发货 | TRANSPORT |
| POD | TRANSPORT + DATA |
| 工厂与产线 | CAPACITY |
| OEM 过渡资料 | CAPACITY + ORDER + DATA |
| 到账、开票、金融凭证 | FUND |
| 政策、标准、合规 | POLICY |
| 设备与工艺装备 | EQUIPMENT |
| 文档、台账、报告、系统数据 | DATA |
| 能耗、碳、绿色能源 | ENERGY |
| 原料、材料、供应商资源 | MATERIAL |
| 团队、专家、服务商 | TALENT |
| 项目场景、区域机会、应用案例 | SCENARIO |
| 质量类内容 | DATA + SCENARIO + ORDER |

## 4. repair_required 默认路径

无法判断挂池时，先挂：

```text
DATA + repair_required
```

需要 KWE 生成补充工单，要求提供对象类型、来源、业务场景和责任 owner。

## 5. P0 禁止事项

- 不因挂池而确认事实。
- 不因挂池而允许 RAG 强引用。
- 不因挂池而允许 GFIS/GPC 写回。
- 不因挂池而进入正式收益分配。
