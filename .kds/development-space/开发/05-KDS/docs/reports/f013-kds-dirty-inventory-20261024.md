---
doc_id: GPCF-DOC-0CB7CDB808
title: F-013 · KDS 脏工作树分类清单（只读盘点，交 KDS 属主收敛）
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/f013-kds-dirty-inventory-20261024.md
source_path: docs/reports/f013-kds-dirty-inventory-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-013 · KDS 脏工作树分类清单（只读盘点，交 KDS 属主收敛）

- 时间：2026-10-24 15:03｜工具：`tools/kds-sync/classify_dirty_paths.py`（只读）｜指纹 `dec56309…12c72e`
- 目的：把 F-013 的 `kds_p1_apply_blocked_by_dirty_worktree` 阻塞变成**可执行收敛清单**
- 边界：本文件只读盘点，**未改 KDS 任何文件**

## 1. 总量与分类（4266 条 dirty）

| 分类 | 条数 | 占比 |
|---|---:|---:|
| governance | 12 | 0.3% |
| product | 1226 | 28.7% |
| noise | 1 | 0.0% |
| sensitive | 0 | 0.0% |
| **unknown** | **3027** | **71.0%** |

状态码分布：`M`=3029、`D`=1213、`??`=24。

## 2. 目录聚合（Top 8）

| 目录 | 条数 | product | unknown |
|---|---:|---:|---:|
| `raw/import-macmini-20261007/` | 873 | 140 | 733 |
| `concepts/` | 822 | 0 | 822 |
| `wiki/sources/` | 640 | 35 | 605 |
| `entities/` | 631 | 631 | 0 |
| `wiki/media/` | 277 | 134 | 143 |
| `concepts/ops/` | 255 | 0 | 255 |
| `concepts/public/` | 251 | 0 | 251 |
| `concepts/personal/` | 217 | 195 | 22 |

## 3. 建议的三步收敛（属主执行）

| 步 | 动作 | 判据 |
|---|---|---|
| 1 | **先处理 1213 个删除 + 3029 个修改**：按目录批量核对是"有意重构"还是"误删/误改"，决定提交或 `git restore` | `git -C "GlobalCloud KDS" status --porcelain -uall \| wc -l` 显著下降；`D` 与 `M` 分类有处置记录 |
| 2 | **分类 unknown 3027 条**：`concepts/`（822）与 `wiki/sources/`（605）多为新导入内容，需给每个目录一个归属结论（纳入版本库 / 进 `_archive/` / 加 `.gitignore`） | `classify_dirty_paths.py --only KDS` 的 unknown 占比由 71% 降到 <20% |
| 3 | **清 noise（1 条）** 与 **governance/mechanical（12 条）**：机械类可加 ignore 或 `git rm --cached`（需授权） | git gate 可见变更集 = 真正待审内容 |

## 4. 复跑命令（只读）

```bash
cd "GlobalCloud GPCF"
python3 tools/kds-sync/classify_dirty_paths.py --only KDS --markdown --top 8 --per-repo-top 6
```

## 5. 顺带修复

- `classify_dirty_paths.py` 原用受限 regex 解析注册表，遇到我按要求加的 `retired: true / denominator_retained: true` 字段会直接报错；
- 已改为 **优先 yaml 解析、regex 兜底**，并容忍附加字段（本轮实测 exit 0 通过）。

## 6. F-013 解除条件（不变）

属主完成上述收敛后回填 summary → `python3 scripts/gpcf_check_evidence.py F-013 --check-only` 不再报 blocker → GPCF 解除阻塞并登记回执。
