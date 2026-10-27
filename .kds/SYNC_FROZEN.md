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
