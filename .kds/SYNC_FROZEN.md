# KDS 同步冻结（2026-10-27 生效）

> 出具人：知识官｜授权：老卢（2026-10-27，经 Chief 下达 P0）｜方案：`outbox/20261027-KDS-status整改-同步断开方案.md`

## 为什么冻结

KDS `status` 字段整改期间（148 种 → 5 种），若同步器继续运行，会把 KDS 侧改动写回/覆盖源仓文档（canonical 层 `controlled` 811 篇中有 760 篇带 `source_path`，其中 `bidirectional` 742 篇），属于改写他人主账。

## 冻结范围

- `tools/kds-sync/document_control.py` **非 `--check` / `--dry-run` 模式一律拒绝**（退出码 2）。
- `--check`、`--dry-run` 仍可跑（只读），CI 不受影响。

## 解冻条件（三件都满足才解）

1. 760 篇有源文档已完成只读落地（写入门禁 + `09-status` 登记）；
2. `status_migration_log.jsonl` 就绪且批 1（69 篇）验收通过；
3. P1 的 `--mirror-write=off` 落地，或确认同步不再有写回路径。

解冻方式：显式设置 `KDS_SYNC_UNFREEZE=1` 运行一次，并在提交说明里写理由；**不要删除本文件当作解冻**。

## 相关

- 计数口径：canonical 8,569；`controlled` 811 / `analysis_candidate` 498；全库口径 1,402 / 528（差 591 = `wiki/sources` 589 + `runtime-reports` 2）。
- 已知缺陷已修：`document_control.py:469`（`write_text` 补 frontmatter 多插一个空行），commit `3cf3a9914`。

## 本次批量的事实口径（2026-10-27 18:17，Chief 实测）

- **触及 420 份 README**（18:17:40–18:17:50 两秒窗口被 touch）；
- **其中内容与 HEAD 有差异 150 份**（`git status`）；
- 工作树因此变脏 **159 项**。

> **报告口径纪律**：必须写「触及 420 份、内容差异 150 份」，**不许只写 150**——只写差异数会让下一个人以为工具只碰了 150 个，下次核不出来。

三条硬约束（Chief 裁定，运营官已写进占用表同一行）：
1. **不得提交**这批 150；
2. **不得作为判据**：`--check` 绿一律以 HEAD 隔离副本为准；
3. `.standards/README.md` 的绿**天然不算数**（它是治理仓 `sync_vendor.py` 生成物，README 自述「勿手改」）。

## 解冻条件（第 4 条，2026-10-27 追加）

1. 760 篇有源文档已完成只读落地；
2. `status_migration_log.jsonl` 就绪且批 1 验收通过；
3. `--mirror-write=off` 落地；
4. **解冻后第一件事是重跑一次并核对「生成物目录零写入」**，而不是直接恢复同步——否则解冻那一刻就把这次污染带回去。

## 写入守卫（2026-10-27 落地，根因修复）

`document_control.py` 写模式（非 `--check/--dry-run`）遇到生成物**必须拒写并打印被拒路径**：
优先按文件内 `generated_by:` 标记判定，无标记再按目录兜底（至少覆盖 `.standards/`）。
拒写在 `stderr` 可见，并在进程结束时汇总；**守卫在解冻后照常生效**，不依赖冻结期。
