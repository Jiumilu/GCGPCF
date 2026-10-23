---
doc_id: GPCF-DOC-8B424ACBF2
title: P18 · 发布 / 回滚 / 监控 / 归档 Runbook 模板（草案，未执行）
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p18-release-rollback-runbook-template-20261022.md
source_path: docs/reports/p18-release-rollback-runbook-template-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P18 · 发布 / 回滚 / 监控 / 归档 Runbook 模板（草案，未执行）

- 日期：2026-10-22｜状态：模板。**不含任何生产发布授权**；生产发布需单独授权（红线：生产环境）
- 适用：首个进入真实业务验证的项目（当前候选：PQC）

## 1. 发布前检查（staging）

| # | 检查 | 命令/证据 |
|---|---|---|
| 1 | 目标版本构建通过 | 项目仓 `build` 绿 + 产物 hash |
| 2 | 迁移脚本可回滚 | 回滚脚本 dry-run 通过 |
| 3 | 配置差异清单 | env/配置 diff（敏感项脱敏） |
| 4 | 监控基线就绪 | 关键指标 + 告警阈值登记 |
| 5 | 回滚演练已完成 | 演练记录（时间/命令/耗时/回滚前后断言） |

## 2. 发布步骤（staging 彩排）

1. 打 tag/快照 → 2. 部署 staging → 3. 冒烟（关键路径 5 条）→ 4. 记录版本与时间 → 5. 观察 30 分钟指标。

## 3. 回滚判据与步骤

- 触发：冒烟失败 / 错误率超阈值 / 关键路径不可用；
- 步骤：停止流量 → 回退版本 → 执行迁移回滚 → 验证断言（HTTP 200 且版本号回退可见）→ 记录。

## 4. 归档

- 产物与证据打包至 `_archive/<pkg>/`，写 `MANIFEST.md`（含 checksum）；
- 归档不等于删除，保留原始证据链。

## 5. 非声明

- 本模板不构成发布授权、不声明 production_ready / customer_accepted；
- 生产发布需 `gate(rule=production)` + 老卢书面授权 + 回执。
