---
doc_id: GPCF-DOC-0BFC37D7C2
title: "0–30 天尾巴 4 项 · 催办单（2026-10-22 22:12）"
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/tail-4-followup-20261022.md
source_path: docs/reports/tail-4-followup-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 0–30 天尾巴 4 项 · 催办单（2026-10-22 22:12）

- 依据：老卢裁定「先催办 0–30 天尾巴」（模型 37.0%）
- 当前 blocked = 4：F-013 / F-014 / F-021 / F-030

| # | Feature | 归属/责任方 | 需对方做什么 | 判据（回读） | 阻塞级别 |
|---|---|---|---|---|---|
| 1 | F-013 知识资产模型 | KDS 属主 | 收敛工作树脏项 + 复核 4 文件 delta 并独立提交 | `git -C "GlobalCloud KDS" status --porcelain -uall` 落在登记范围；`gpcf_check_evidence.py F-013` 不再报 blocker | 中（工程可控） |
| 2 | F-014 会议到项目控制 | 老卢指定 owner + 授权 | 指定**权威接收台账 owner**、留存策略口径；真实数据授权 | `authorization_granted=true` 回执 + owner 书面指定 | **高（需老卢授权）** |
| 3 | F-021 World 纳管 | WAS → World 属主 | WAS 出具 Ontology 基线裁定（0.2.x vs 0.2.0）→ World 更新方案与 6 项 metadata | `loop_document_gate` 无 rework_required；方案 candidate→authoritative 台账确认 | 中（跨项目裁定） |
| 4 | F-030 PDC 纳管 | PDC 属主 | 按《PDC 重采清单》重跑 tests/summary 并回填证据 | `gpcf_check_evidence.py F-030` 不再报 evidence 类理由 | 低（1 天） |

## 催办记录

| 时间 | 动作 | 结果 |
|---|---|---|
| 2026-10-22 22:12 | 出单并登记 GPCF 侧（本文件） | 待各属主回应 |

## 本单不代做的事

- 不代写 KDS/PDC/World/WAS 仓；
- 不代替老卢指定 F-014 owner；
- 不对 F-021 的 Ontology 版本下结论（属 WAS 语义裁定）。
