---
doc_id: GPCF-DOC-P0D-REVIEW-QUEUE-20260626
title: GlobalCloud 项目群 P0-D 开发态 Review Queue 拆分证据
project: KDS
related_projects: [GPC, WAES, KDS, PKC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-p0d-review-queue-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-p0d-review-queue-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 P0-D 开发态 Review Queue 拆分证据

## 授权边界

- 输入：用户要求“下一步”，承接 P0-C。
- 范围：把项目群剩余 dirty 工作区拆成开发态 review queue。
- 允许动作：只读 Git 采样、review queue 分类、生成 evidence、KDS 本地镜像同步。
- 禁止动作：提交、推送、部署、生产写入、schema migrate、真实外部 API 写入、删除文件、清理 `.DS_Store`、清理 `dist`/`output`、标记 accepted、integrated、production_ready、customer_accepted。
- 判定边界：P0-D 只建立提交/推送/验收前的 review queue，不等于 review 已完成。

## P0-D 重点采样

| 项目 | dirty/untracked | 主要路径族 | diff-check | 拆分判定 |
|---|---:|---|---|---|
| GlobalCoud GPCF | 910/458 | `.kds/development-space` 359; `docs/harness` 269; `tools/kds-sync` 137; `.harness` 45; `fixtures` 25 | pass | governance_evidence_kds_mirror_review_queue |
| GlobalCloud KDS | 62/35 | `wiki/sources` 22; `concepts` 20; `_governance` 9; `entities` 3 | pass | knowledge_import_governance_review_queue |
| GlobalCloud PKC | 8/2 | `dist` 5; AGENTS/总体/实施方案 3 | pass | build_artifact_review_queue |
| GlobalCloud SOP | 16/8 | `docs/operations` 6; `data` 4; `output` 1 | pass | sop_operations_owner_review_queue |
| WAS世界资产体系 | 4/1 | AGENTS/总体/实施方案 3; `.DS_Store` 1 | pass | local_artifact_isolation_queue |
| GlobalCloud Studio | 12/4 | `docs/harness` 6; `scripts` 3; AGENTS/总体/实施方案 3 | pass | release_review_queue |

## Review Queue

| 队列 | 范围 | owner | 进入条件 | 出队条件 | 硬停止 |
|---|---|---|---|---|---|
| P0-D-Q1 | GPCF governance/evidence/KDS mirror/tools | GPCF/KDS | 文档门禁 pass；KDS conflict guard pass；Git gate 无 hard blocker | 拆成 `docs/harness`、`tools/kds-sync`、`.kds mirror`、`fixtures`、`registers` 独立候选包 | 不跳过文档门禁；不写真实 KDS API |
| P0-D-Q2 | KDS knowledge import / governance runs | KDS | KDS smoke pass；diff-check pass；无 token 明文 | 区分知识导入、概念实体、治理流水、删除/重命名 sources | 不把本地 mirror 写成真实 API 完成 |
| P0-D-Q3 | PKC `dist` build artifact | PKC | P0-B build pass；dist 文件与当前构建输出一致 | review 确认是否提交 dist 或改为派生产物排除 | 不提交陈旧构建产物 |
| P0-D-Q4 | SOP operations/output/data indexes | SOP | P0-C diff-check pass；owner review 可执行 | 草案、模板、输出、索引分别确认归属 | 不把草案/output 写成生产指令 |
| P0-D-Q5 | WAS `.DS_Store` 本地产物隔离 | WAS | P0-C diff-check pass；`.DS_Store` 已识别 | 人工确认删除或忽略策略；本轮不自动删除 | 不提交 `.DS_Store` |
| P0-D-Q6 | Studio release review readiness | Studio/GPCF | P0-B harness pass；release review checklist 存在 | 人工复核 release/write workflows 后再决定提交候选 | 不触发 release workflow、不发布 |
| P0-D-Q7 | 方案传导小队列 | WAES/各项目 owner | AGENTS + 总体/实施方案传导 dirty | 与项目群总控方案一致后进入提交候选 | 不提交未确认方案传导 |

## 当前状态

| 字段 | 结果 |
|---|---|
| review_queue_count | 7 |
| review_queue_ready | true |
| project_group_git_gate | partial |
| hard_blockers | none |
| missing/ahead/behind/sensitive | none |
| diff_check | pass |

## 下一轮建议

1. P0-E1：先处理 `WAS .DS_Store` 和 SOP `output/` 的隔离策略，只登记，不自动删除。
2. P0-E2：对 PKC `dist` 做 build artifact consistency decision，确认是否可进入提交候选。
3. P0-E3：把 GPCF/KDS 大队列拆成 3 到 5 个可 review 的候选包。
4. P0-E4：Studio release review 人工复核记录到位前，不进入发布或 push。

## 状态声明

- p0d_review_queue_ready = true
- review_queue_count = 7
- development_start_allowed = true
- project_group_git_gate = partial
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
