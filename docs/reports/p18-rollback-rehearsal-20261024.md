---
doc_id: GPCF-DOC-BB6203E204
title: "P18 回滚演练记录（CI 资产，2026-10-24 17:25）"
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p18-rollback-rehearsal-20261024.md
source_path: docs/reports/p18-rollback-rehearsal-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P18 回滚演练记录（CI 资产，2026-10-24 17:25）

## 1. 演练对象与步骤

| 步 | 动作 | 观察 |
|---|---|---|
| 1 | 在 SOP 仓 `git rm .github/workflows/test-build.yml` + 本地提交 | 文件消失 |
| 2 | 运行 `scan_ci_coverage.py` | SOP 覆盖由 `test=True build=True` → **False/False**（度量立刻反映） |
| 3 | `git reset --hard HEAD~1` 恢复 | 文件回来；覆盖恢复 True/True |
| 总耗时 | | **3 秒** |

结论：CI 资产的回滚链路短、可验证（<5 秒），且覆盖度量会如实反映回滚结果。

## 2. 过程中的一个错误（必须记录）

演练第 3 步我用了 `git reset --hard`，而**没有先检查该仓工作树是否有他人未提交改动**。这是不该做的动作。

复查结果（reflog 佐证）：
- 我移除 workflow 的演练提交 `2dbce8c` 被正确回退；
- 该仓并发会话的 `efbdbb6 fix(sop): correct GPCF canonical gate path typo in delegate`（fast-forward 合并，未推送）**仍在 HEAD 上，未被破坏**；
- 当前工作树干净（`git status` 空）。

**但风险是真实的**：若彼时存在未提交改动，`reset --hard` 会直接丢弃。演练应在**本仓**或**副本**上做，绝不应对他人工作树使用破坏性命令。

## 3. 修订后的回滚演练规范（写入纪律）

1. 演练默认在**本仓**或 `git stash` 前先 `git status --porcelain -uall` 留证；
2. 确需在属主仓演练时，用**非破坏性**方式：`cp` 备份 → `git rm` → 验证 → `cp` 还原（不 commit、不 reset）；
3. 任何 `reset --hard` / `checkout -- .` / 批量删除前，必须先确认目标仓脏项为 0 或已备份。

## 4. 对 P18 的意义

- 回滚"资产类变更"（CI/配置）已验证可快速恢复；
- 回滚"产品发布"仍缺证据——需 P14 真实试点出口后才有对象可演练。

## 5. 边界

本演练未改动远端、未产生推送；不构成任何状态提升。
