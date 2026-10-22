---
doc_id: GPCF-DOC-F036waepkcin
title: F-036-wae-pkc-intake-integration journal
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/journal.md
source_path: features/active/F-036-wae-pkc-intake-integration/journal.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# F-036-wae-pkc-intake-integration WAE·PKC 接入演练

## LOOP 日志

### Iteration 0（建账补齐，2026-10-22）

1. 这轮做什么？
   - 补齐 Feature Workspace 结构（feature.yaml 已存在，缺 journal 与 evidence/artifacts 目录）。
   - 目标：完成 PKC 在 WAE 的注册与首批接入演练（placement/manifests/menus、UI gate、令牌与状态语义、回滚）。
2. 改了什么？
   - 新增本 journal、evidence/、artifacts/ 目录；feature.yaml 保持由该 Feature 属主写入的内容不变。
3. 怎么验证？
   - `python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py` 结构校验通过；
     证据状态以 feature.yaml 的 evidence 字段为准（本轮回填结构，未新增证据）。
4. 发现什么问题？
   - 该 Feature 在 2026-10-22 的 P0x 治理批次中只提交了 feature.yaml，缺 journal 与证据目录，
     导致 `feature_workspace` 门禁失败；本轮按最小补齐原则修复结构，不改动其业务状态与 blockers。
5. 是否可以提交？
   - 可以（仅补结构）；Feature 仍为 active 且带 blockers，状态不提升。
