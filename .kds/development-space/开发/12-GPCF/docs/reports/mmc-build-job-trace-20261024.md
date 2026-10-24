---
doc_id: GPCF-DOC-6A1EA019E6
title: MMC 补 build job 留痕（跨仓，模型授权）
project: GPCF
related_projects: [GPCF, WAME, MMC]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/mmc-build-job-trace-20261024.md
source_path: docs/reports/mmc-build-job-trace-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# MMC 补 build job 留痕（跨仓，模型授权）

- 时间：2026-10-24 15:55｜授权：`decide_template(authorization_qa)` → **probability_yes 0.6207 / verdict yes**
- 背景：MMC 已有 `mmc-ci.yml`（test job：postgres 服务 + 契约脚本 + pytest 23 文件 + sdk vitest），但缺 build（P16-2）

## 1. 改动（在既有 workflow 追加 1 个 job，未提交跨仓）

`.github/workflows/mmc-ci.yml` 新增 `build` job：AST 语法解析整仓 `.py`（本地实测 **73 文件，0 失败**），无产物、不改既有 test job。

## 2. 覆盖变化

| 指标 | 改前 | 改后 |
|---|---:|---:|
| build 覆盖 | 22/29 | **23/29** |

## 3. 回滚

```bash
cd "GlobalCloud MMC"
git checkout -- .github/workflows/mmc-ci.yml
```

## 4. 边界

仅追加 CI job，未改业务代码；不构成任何状态提升。

> **激活状态（2026-10-24 16:25 更正）**：本文件所述为**工作区口径**（文件已准备）。该文件在属主仓内仍是未跟踪状态、尚未在 CI 生效；激活与回滚步骤见 `ci-activation-checklist-20261024.md`。
