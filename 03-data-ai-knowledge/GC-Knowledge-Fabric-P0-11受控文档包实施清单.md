---
doc_id: GPCF-DOC-139A718B66
title: GC-Knowledge Fabric P0 11受控文档包实施清单
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-P0-11受控文档包实施清单.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-P0-11受控文档包实施清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 11受控文档包实施清单

## 1. 定位

本清单用于跟踪 GC-Knowledge Fabric P0 阶段的 11 份受控文档。P0 的目标是固化制度、编号、目录、门禁、台账、敏感资料处理和 LOOP 模板，不声明业务闭环已完成。

## 2. P0 文档包

| 序号 | 文件 | 用途 | 当前状态 |
|---|---|---|---|
| 1 | `GC-Knowledge-Fabric-KDS十一池挂接规则.md` | 定义十一池、默认挂接、复合挂接和例外处理 | draft |
| 2 | `GC-Knowledge-Fabric-WAES门禁规则.md` | 定义 Source / Evidence / RAG / Writeback / Revenue 等门禁口径 | draft |
| 3 | `GC-Knowledge-Fabric-RAG准入与引用强度规则.md` | 定义 safe / limited / repair_required / blocked / metadata-only | draft |
| 4 | `GC-Knowledge-Fabric-葛化GFIS知识库目录.md` | 定义葛化 GFIS P1 母版知识目录 | draft |
| 5 | `GC-Knowledge-Fabric-湖北磷材知识库目录.md` | 定义湖北磷材拓厂、原料、行业、订单目录 | draft |
| 6 | `GC-Knowledge-Fabric-积分收益额度悬赏台账模型.md` | 定义四类台账与候选/确认边界 | draft |
| 7 | `GC-Knowledge-Fabric-敏感资料入库规则.md` | 定义合同、POD、金融凭证、质量争议等资料入库边界 | draft |
| 8 | `GC-Knowledge-Fabric-LOOP跟踪模板.md` | 定义每轮 LOOP 必填项、证据项和状态边界 | draft |
| 9 | `GC-Knowledge-Fabric-统一编号规则.md` | 定义对象、证据、候选、工单、决议等编号 | draft |
| 10 | `GC-Knowledge-Fabric-统一状态机与状态提升规则.md` | 定义 lifecycle、确认状态、写回状态和冻结规则 | draft |
| 11 | `GC-Knowledge-Fabric-核心对象关系与最小字段契约.md` | 定义核心对象关系和最小字段 | draft |

## 3. P0 验收口径

- 所有新资料必须能分配编号。
- 所有关键对象必须能挂接 Domain 与 KDS 十一池。
- AI 输出只能进入候选态。
- GFIS 写回必须经过 WAES 与人工确认。
- 收益、积分、额度、悬赏必须保留候选和确认状态。
- 敏感资料必须进入 metadata-only 或受控原件引用模式。
- LOOP 只记录证据和状态变化，不自动声明业务完成。

## 4. 不纳入本清单的事项

- 不声明数据库表已迁移。
- 不声明 API 已上线。
- 不声明 GFIS / GPC 已正式写回。
- 不声明 RAG safe 率已达到生产目标。
- 不声明委员会已完成实际裁决。
- 不声明收益或积分已经正式分配。
