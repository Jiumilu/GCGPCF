---
doc_id: GPCF-DOC-0749030BBD
title: Evidence Index — KDS
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/KDS/evidence/evidence-index.md
source_path: docs/harness/KDS/evidence/evidence-index.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Evidence Index — KDS

## 证据索引

| 轮次 | Round ID | evidence 类型 | 文件 | 是否完整 | Harness 结论 |
|---|---|---|---|---|---|
| 1 | GPCF-KD-LR-001 | loop state | `docs/harness/KDS/loop-state.md` | yes | partial |
| 1 | GPCF-KD-LR-001 | loop record | `docs/harness/KDS/loops/loop-round-GPCF-KD-LR-001.md` | yes | partial |
| 1 | GPCF-KD-LR-001 | validator | `tools/kds-sync/validate_kds_initialization.py` | yes | pass |
| 1 | GPCF-KD-LR-001 | token validator | `tools/kds-sync/validate_kds_token.py` | yes | pass fingerprint=bfd9553d |

## 完整率统计

| 统计项 | 值 |
|---|---|
| 已完成轮次 | 1 |
| evidence 完整轮次 | 0 |
| 证据完整率 | 35% |

## 缺口

- KDS 真实项目仓未确认。
- 知识对象、同步边界、API 审计流水与文档主存映射清单尚未完成。
- Git push/PR merge 未执行。
- 未经人工验收不得升级 `accepted` 或 `integrated`。

Current state remains `partial` until KDS 真实项目仓、知识对象映射、运行态同步验收和人工验收完成。
