---
doc_id: GPCF-DOC-8ECD9BA263
title: 智能体安全矩阵
project: GPCF
related_projects: [GPCF, WAES]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/kds-production-hardening/specs/agent-safety-matrix/spec.md
source_path: openspec/changes/kds-production-hardening/specs/agent-safety-matrix/spec.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# 智能体安全矩阵

## 概述
针对 AI 智能体代码修改采用四层防线：工作区隔离、补丁允许列表、静态风险扫描、人工复核。

## 要求
- 智能体任务必须在隔离的工作区目录中运行
- 文件类型限制：仅允许 `.md`、`.yaml`、`.json`、`.html`、`.css`、`.js`
- 路径限制：`server/core/auth.py`、`server/core/db.py`、`migrations/`、`scripts/deploy`、`scripts/backup`、`.env` 一律阻断
- 静态扫描需检测：SQL `DROP/DELETE/TRUNCATE`、`os.system`、`subprocess`、`eval`、`exec`、`rm -rf`
- 风险级别：低风险（自动接受）、中风险（人工复核 + 回滚方案）、高风险（强制安全复核）、严重风险（直接阻断）
- 所有 `risk >= medium` 的补丁都必须附带回滚方案
- 任务状态机：`not_started -> in_progress -> blocked -> ready_for_human_acceptance -> accepted -> applied -> closed`

## 验收
- [ ] 智能体不能修改 `auth.py`、`db.py` 或 migration 文件
- [ ] 危险 SQL 或 shell 模式能够被检测并标记
- [ ] 高风险补丁必须进入人工复核
- [ ] 缺少回滚方案的补丁会在 accept 步骤被拒绝
