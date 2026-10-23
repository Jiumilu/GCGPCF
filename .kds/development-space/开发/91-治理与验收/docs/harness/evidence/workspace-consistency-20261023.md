---
doc_id: GPCF-DOC-WORKSPACE-CONSISTENCY-20261023
title: Feature 工作区一致性检查（2026-10-23）
project: GPCF
related_projects: [GPCF, WAME]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/workspace-consistency-20261023.md
source_path: docs/harness/evidence/workspace-consistency-20261023.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# Feature 工作区一致性检查（2026-10-23）

## 1. 发现

`features/active` 中存在 queue 已 closed 的重复目录：

| Feature | queue 状态 | active 目录 | done 目录 | 说明 |
|---|---|---|---|---|
| F-010 | closed | 存在 | 存在 | active 含 artifacts/studio-runtime-reference；done 含 ui-gates-20261022 |
| F-011 | closed | 存在 | 存在 | 两侧内容需 diff |
| F-019 | closed | 存在 | 存在 | active 为最新证据（API 复核），done 为旧快照 |

## 2. 影响

- 门禁未报错（validator 不检查 active/done 重复），但会造成“已关闭 Feature 仍在 active”的误读。
- F-019 的 active 证据比 done 新，若直接删除 active 会丢证据。

## 3. 建议处置（需授权）

1. F-019：将 active 的新证据合并到 done（api.txt/summary/feature.yaml），再移除 active 重复目录。
2. F-010：将 active 的 artifacts/studio-runtime-reference 合并到 done（若确认有价值），再移除 active。
3. F-011：diff 两侧后合并差异，再移除 active。
4. 清理为 L2 操作：需清单 + 回滚方案 + 老卢授权；本轮只记录，不删除。

## 4. 非声明

- 不声明已清理；不声明任何状态变化。
