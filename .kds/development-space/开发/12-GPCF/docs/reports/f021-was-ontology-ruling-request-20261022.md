---
doc_id: GPCF-DOC-102B1BBB47
title: F-021 · WAS Ontology 基线裁定请求（交 WAS 属主）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/f021-was-ontology-ruling-request-20261022.md
source_path: docs/reports/f021-was-ontology-ruling-request-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-021 · WAS Ontology 基线裁定请求（交 WAS 属主）

- 日期：2026-10-22｜提出方：GPCF｜受理方：WAS（世界资产语义治理）
- 现状：F-021（world-project-onboarding）唯一剩余阻塞 = Ontology 版本冲突
- 状态：**已成稿归档（2026-10-22 22:52 老卢裁定：起草并归档，由我方不跨项目发函；由老卢或属主渠道递交）**
- 非声明：本文件是裁定请求，不代表裁定已发生；World 方案仍为 `candidate`

## 1. 冲突事实

| 项 | 实测 |
|---|---|
| World 项目方案声明的 Ontology 基线 | `0.2.x` |
| WAS 实发（现行）基线 | `0.2.0` |
| 影响 | World 总体方案无法升 `authoritative`；中央门禁对该 Feature 曾判 `rework_required`；6 项 metadata 待补 |

## 2. 请求 WAS 裁定的三个问题

1. **基线口径**：World 应继承 `0.2.0`（WAS 实发）还是允许 `0.2.x` 兼容区间？若允许区间，写清上下界与不兼容项。
2. **升级路径**：若 World 必须跟随 `0.2.0`，需要哪些迁移动作（schema/xap 变更、验证用例）？
3. **裁定形式**：以 WAS 仓内受控文档 + 回执号给出，GPCF 侧据此把 World 方案 `candidate → authoritative`（该提升仍需老卢确认）。

## 3. GPCF 侧同时会做的（不等裁定）

- 6 项 metadata 补齐（属 GPCF 侧台账）；
- F-021 证据声明已完成（P05），复跑仅剩 Ontology 阻塞；
- World 仓归属同步清单已出（`world-f021-attribution-sync-checklist-20261022.md`）。

## 4. 判据

`python3 scripts/gpcf_check_evidence.py F-021 --check-only` → `close_candidate=true`（需 blockers 为空）。
