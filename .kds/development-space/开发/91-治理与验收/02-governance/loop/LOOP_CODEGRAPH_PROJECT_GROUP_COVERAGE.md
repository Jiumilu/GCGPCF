---
doc_id: GPCF-DOC-6CC5F6A45C
title: Loop CodeGraph Project Group Coverage
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md
source_path: 02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop CodeGraph Project Group Coverage

## 覆盖结论

2026-06-21 已将项目群当前 14 个本机 Git 仓库纳入 CodeGraph 本地代码图谱生成范围，其中 `WAS世界资产体系` 已作为第 14 项进入项目群、代码图谱和 Loop 工程登记。这里的“14 个本机 Git 仓库纳入 CodeGraph”是项目群覆盖的固定口径。

本轮只完成本地代码图谱生成与治理登记，不执行 `codegraph install`，不修改 Agent MCP 配置，不提交、不推送、不部署、不生产写入、不真实外部 API 写入，也不把任何项目升级为 `accepted`、`integrated` 或 `production_ready`。

## 工具与边界

| 字段 | 值 |
|---|---|
| CodeGraph package | `@colbymchenry/codegraph@1.0.1` |
| CLI version | `1.0.1` |
| telemetry | disabled |
| graph storage | 每个项目本地 `.codegraph/` |
| Git 保护 | `.codegraph/` 写入各仓 `.git/info/exclude`，不纳入提交 |
| MCP install | 未执行 |
| project_group_repo_count | 14 |
| studio_included | true |
| was_included | true |

## 项目群代码图谱覆盖表

本表即 `CodeGraph 项目群覆盖表`，用于固化 14 个本机 Git 仓库纳入 CodeGraph 的项目群覆盖口径。

| # | 项目 | 仓库路径 | Files | Nodes | Edges | DB Size | CodeGraph 状态 | Git 跟踪状态 |
|---|---|---|---:|---:|---:|---:|---|---|
| 1 | GlobalCloud Brain | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain` | 150 | 1,990 | 4,124 | 4.43 MB | up_to_date | `.codegraph` 未进入 Git |
| 2 | GlobalCloud GFIS | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` | 1,022 | 13,152 | 38,142 | 65.24 MB | indexed_with_internal_pending_notice | `.codegraph` 未进入 Git |
| 3 | GlobalCloud GPC | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC` | 70 | 705 | 1,995 | 2.77 MB | up_to_date | `.codegraph` 未进入 Git |
| 4 | GlobalCloud KDS | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS` | 516 | 3,437 | 6,986 | 9.65 MB | up_to_date | `.codegraph` 未进入 Git |
| 5 | GlobalCloud MMC | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC` | 84 | 522 | 1,083 | 1.20 MB | up_to_date | `.codegraph` 未进入 Git |
| 6 | GlobalCloud PKC | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC` | 110 | 1,034 | 2,685 | 2.41 MB | up_to_date | `.codegraph` 未进入 Git |
| 7 | GlobalCloud PVAOS | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS` | 604 | 8,899 | 28,838 | 25.67 MB | up_to_date | `.codegraph` 未进入 Git |
| 8 | GlobalCloud Studio | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio` | 778 | 14,202 | 46,489 | 43.00 MB | up_to_date | `.codegraph` 未进入 Git |
| 9 | GlobalCloud WAES | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES` | 281 | 3,511 | 11,298 | 10.38 MB | up_to_date | `.codegraph` 未进入 Git |
| 10 | GlobalCloud XGD | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD` | 181 | 3,645 | 9,914 | 8.57 MB | up_to_date | `.codegraph` 未进入 Git |
| 11 | GlobalCloud XiaoC | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC` | 1,176 | 15,520 | 64,515 | 57.11 MB | up_to_date | `.codegraph` 未进入 Git |
| 12 | GlobalCloud XiaoG | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG` | 752 | 13,943 | 45,987 | 42.53 MB | up_to_date | `.codegraph` 未进入 Git |
| 13 | GlobalCoud GPCF | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF` | 363 | 5,158 | 14,109 | 15.26 MB | up_to_date | `.codegraph` 未进入 Git |
| 14 | WAS 世界资产体系 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系` | 30 | 70 | 209 | 0.27 MB | up_to_date | `.codegraph` 未进入 Git |

## WAS 纳入规则

- `WAS世界资产体系` 作为项目群第 14 项登记，当前定位为 Ontology / WAS 八维八流语义契约来源，机器角色为 `semantic_foundation_project`。
- WAS 已有 `AGENTS.md`、`PROJECT_HARNESS_MANIFEST.md`、`docs/harness/loop-state.md`、`docs/harness/evidence/evidence-index.md` 和 `docs/harness/loops/loop-round-WAS-LR-001.md`。
- WAS 远端为 private `Jiumilu/GCWAS`，默认分支 `main`，HEAD 为 `7ec9c332db981f4d19d0edb3194fc7173f9b1d67`。
- WAS 原生 validator `python3 okf/validators/validate_all.py` 全部 PASS。
- WAS CodeGraph 已本地生成，统计为 `files=30 nodes=70 edges=209 db_size=0.27 MB`。
- WAS 是语义契约源，不是 KDS source of record、GFIS runtime 或 WAES gate authority；本轮不声明 accepted、integrated 或 production_ready。

## Studio 纳入规则

- `GlobalCloud Studio` 作为项目群第 13 项登记，当前定位为 Studio / Hermes / Agent 工作台与治理扩展入口。
- Studio 已有 `docs/harness/loops/loop-round-GPCF-STUDIO-*` 轮次文件，说明它已进入 Loop 工程上下文；本轮不改动 Studio 大量未提交源码，只在 GPCF 总控侧登记其纳入事实。
- Studio 的 CodeGraph 已本地生成，统计为 `files=778 nodes=14202 edges=46489 db_size=43.00 MB`。
- Studio 已补齐最小 Loop 准入包：`PROJECT_MANIFEST.md`、`docs/harness/loop-state.md`、`docs/harness/evidence/evidence-index.md`、`docs/harness/evidence/studio-loop-admission-20260620.json`、`docs/harness/loops/loop-round-GPCF-STUDIO-LR-018.md` 和 `scripts/validate_studio_loop_admission.py`。
- Studio 已补齐 LR-021 质量门禁修复证据：`docs/harness/evidence/studio-quality-gate-repair-20260620.json`、`docs/harness/evidence/studio-quality-gate-repair-20260620.md`、`docs/harness/loops/loop-round-GPCF-STUDIO-LR-021.md` 和 `scripts/validate_studio_quality_gate_repair.py`。`npm run test` 已通过，`npm run build` 已通过。
- Studio 已补齐 LR-022 harness foundation 证据：`docs/harness/evidence/studio-harness-foundation-20260620.json`、`docs/harness/evidence/studio-harness-foundation-20260620.md`、`docs/harness/loops/loop-round-GPCF-STUDIO-LR-022.md` 和 `scripts/validate_studio_harness_foundation.py`。`npm run harness:check` 已通过；新增 workflow 为基础门禁骨架，不证明发布执行、accepted、integrated 或 production_ready。
- Studio 已补齐 LR-023 workflow release boundary 证据：`docs/harness/evidence/studio-workflow-release-boundary-20260620.json`、`docs/harness/evidence/studio-workflow-release-boundary-20260620.md`、`docs/harness/loops/loop-round-GPCF-STUDIO-LR-023.md` 和 `scripts/validate_studio_workflow_release_boundary.py`。当前提交前状态为 `review_required_before_commit`，不证明发布执行、accepted、integrated 或 production_ready。
- Studio 当前仓库为未提交初始仓，本轮不把该状态解释为交付完成或验收通过。

## 异常与非声明

- GFIS 当前 CodeGraph 状态在 `sync` 后仍提示 `Pending Changes: Added 1 files`，但同步输出为 `Synced 1 changed files` 且 `Added: 1 - 0 nodes`；本轮将其登记为 CodeGraph 内部/无节点变化待同步提示，不作为业务代码图谱失败。
- 本轮不证明 GFIS 真实业务 source-of-record、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact 已完成。
- 本轮不证明任一项目已获得人工验收、UAT 签收、客户满意度闭环、`accepted`、`integrated` 或 `production_ready`。
- 本轮不授权生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、提交、推送或合并。
