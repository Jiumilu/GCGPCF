---
doc_id: GPCF-DOC-6784A73289
title: 29 仓统一规范检查（standards）全量体检（2026-10-24）
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/standards-sweep-20261024.md
source_path: docs/reports/standards-sweep-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 29 仓统一规范检查（standards）全量体检（2026-10-24）

- 方法：对注册表 29 仓逐仓执行 `python3 _governance/tools/gc_standard.py check --repo "<仓>" --fail-on error`
- 结论：**27/29 零 error**；2 仓 error 均来自 **R14-dirty-worktree**（属主在途改动），非代码规范违规

## 1. 结果

| 结果 | 仓数 | 说明 |
|---|---:|---|
| error=0 | **27** | 合规 |
| error=1（R14 脏工作树） | **2** | KDS（4266 条）、SpaceAI Platform（2232 条） |

有 warn 的仓：WAE（warn=2），其余仓多为 info=1（脏工作树提示，未达阈值）。

## 2. 两个 error 的明细

| 仓 | 规则 | 详情 |
|---|---|---|
| GlobalCloud KDS | R14-dirty-worktree | 可脏区之外 4266 条未提交变更（阈值 warn 50 / error 200）；分类清单见 `f013-kds-dirty-inventory-20261024.md` |
| GlobalCloud SpaceAI Platform | R14-dirty-worktree | 2232 条未提交变更，其中 79 条在已声明治理可脏区内 |

**处置责任**：两仓属主收敛工作树（提交/归档/ignore 分类处置），GPCF 不代改（纪律⑤）。

## 3. 附带修复：GPCF 自身 CI 构建自检

- P16-2 盘点显示 GPCF 缺 build；本轮在 `.github/workflows/governance.yml` 增加「构建自检（语法解析，无产物）」；
- **为什么不直接 `compileall`**：本仓存在超长文件名（`scripts/gfis/`、`tools/kds-sync/` 中 200+ 字符），
  `compileall` 写 `.pyc` 会因文件名长度超限报 `OSError: [Errno 63]`（本轮实测确认）；改用 `ast.parse` 全量语法解析（1252 个 .py，0 失败）；
- 同步更新 `scan_ci_coverage.py` 的 build 判定（加入 `ast.parse`），实判覆盖变为 standards 29/29、test 10/29、build 13/29。

## 4. 复跑命令

```bash
cd "GlobalCloud V0.0.1"
python3 _governance/tools/gc_standard.py check --repo "GlobalCloud KDS" --fail-on error
python3 "GlobalCloud GPCF/tools/kds-sync/scan_ci_coverage.py" --markdown
```
