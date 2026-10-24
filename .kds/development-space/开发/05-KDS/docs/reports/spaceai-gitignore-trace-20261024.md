---
doc_id: GPCF-DOC-3176540E62
title: SpaceAI Platform 脏树治理留痕（跨仓，模型授权）
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/spaceai-gitignore-trace-20261024.md
source_path: docs/reports/spaceai-gitignore-trace-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# SpaceAI Platform 脏树治理留痕（跨仓，模型授权）

- 时间：2026-10-24 15:15｜授权：`decide_template(authorization_qa)` → **probability_yes 0.8794 / verdict yes**；`gate(rule=production)` → go 0.197（非红线）
- 依据：老卢 2026-10-24 授权「自动按决策模型推荐选择确认」
- 目的：修复该仓 `R14-dirty-worktree` error（2311 条 → 38 条）

## 1. 根因

`classify_dirty_paths.py` 只读分类显示：2311 条脏项中 **2298 条为未跟踪生成物**：

| 目录 | 条数 |
|---|---:|
| `data/cctv-stills/` | 530 |
| `data/videos/` | 512 |
| `data/monitor-images/` | 501 |
| `data/cctv-streams/` | 457 |
| `data/snapshots/` | 152 |
| `data/rebuild/` | 33 |
| `.harness/runs/` | 79 |

`.gitignore` 原本未忽略 `data/` 与 `.harness/runs/`。

## 2. 改动（仅 2 行 + 1 行注释，未提交跨仓）

```gitignore
# 生成物 / 运行时数据（GPCF 2026-10-24：data/ 下 CCTV 视频与快照、.harness 运行记录不纳入版本库）
data/
.harness/runs/
```

`data/` 下原有 2 个已跟踪文件不受影响（gitignore 不改变已跟踪状态）。

## 3. 效果（实测）

| 指标 | 改前 | 改后 |
|---|---:|---:|
| `git status --porcelain -uall \| wc -l` | **2311** | **38** |
| `gc_standard check --repo "GlobalCloud SpaceAI Platform" --fail-on error` | error 1（R14） | **error 0 → PASS** |

29 仓 standards 口径由 27/29 → **28/29**（仅剩 KDS 的 R14）。

## 4. 回滚

```bash
cd "GlobalCloud SpaceAI Platform"
git checkout -- .gitignore
# 或从备份恢复：/tmp/spaceai_gitignore.bak
```

## 5. 备注

- 若属主后续要纳入部分 `data/` 内容，可在 `.gitignore` 用 `!` 例外逐条放行；
- 该仓另有 38 条真实改动（含 `.standards/*`、`apps/desktop/src/main.ts` 等），需属主自行提交或归类。
