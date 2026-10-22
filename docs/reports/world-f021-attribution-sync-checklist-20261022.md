---
doc_id: GPCF-DOC-8A36559878
title: World 仓 F-021 归属同步清单（交属主执行）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/world-f021-attribution-sync-checklist-20261022.md
source_path: docs/reports/world-f021-attribution-sync-checklist-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# World 仓 F-021 归属同步清单（交属主执行）

- 日期：2026-10-22｜依据：老卢 Q（gate 0.915 stop）裁定「清单交属主执行，不由 GPCF 代写 World 仓」
- GPCF 侧已完成：`features/active/F-021-*/feature.yaml:3` `project: world`、`runtime/queue.json` F-021 `project: world`、回执 `AUTH-PG-F021-ATTRIBUTION-20261022`
- 状态边界：本清单是**待执行动作**，不构成 World 仓已完成同步的声明

## 1. 需检查/修改的 World 仓位置（属主逐项确认）

| # | 位置 | 检查内容 | 建议动作 |
|---|---|---|---|
| 1 | `README.md` | 是否声明"F-021 归属 GPCF"或"由 GPCF 代管" | 改为"F-021 立项于 GPCF、归属 World，证据在 GPCF 中央门禁" |
| 2 | `AGENTS.md` | related_projects 是否含 GPCF、是否把 F-021 列为他项目 | 保留 GPCF 为关联，明确本仓承接 F-021 的 STATUS/证据 |
| 3 | `PROJECT_HARNESS_MANIFEST.md` | Feature 列表是否含 F-021 | 补 F-021，注明 iteration/证据路径 |
| 4 | `projects/world/STATUS.md`（若在 GPCF 侧） | 已按 F-021 登记（GPCF 实测 :26/:29/:41） | 无需改；仅确认接手后更新 loop_status |
| 5 | 仓内 `docs/**` 涉及 F-021 的引用 | `grep -rn "F-021" .` 逐条判断 | 把"归属 GPCF"表述改为"立项 GPCF / 归属 World" |
| 6 | `openspec/**` 若含 F-021 规格 | 覆盖范围是否与 world-project-onboarding 一致 | 不一致则在 openspec 侧登记差异，不擅自改 GPCF 侧 |

## 2. 属主可用的核对命令

```bash
cd "GlobalCloud World"
grep -rn "F-021" --include="*.md" --include="*.yaml" . | head -20
grep -rn "gpcf" README.md AGENTS.md PROJECT_HARNESS_MANIFEST.md
```

## 3. 完成判据（World 属主回执）

1. World 仓内不再出现「F-021 属于 GPCF」的表述；
2. `PROJECT_HARNESS_MANIFEST.md` 含 F-021 且指向 GPCF Feature 工作区；
3. 属主在 GPCF 决策台账追加一条 `kind: dispose` 或在本清单回填完成标记；
4. GPCF 侧不改 World 仓、不代签。

## 4. 回滚

World 仓改动均为文档级，`git revert <commit>` 即可；不涉及数据/服务。
