---
doc_id: GPCF-DOC-F013-GKE001-KDS-STAGEB-RUN-HANDOFF-COMMIT-20260813
title: GKE-001 KDS Stage B run/handoff 本地提交与独立复核
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-run-handoff-local-commit-and-review-20260813.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-run-handoff-local-commit-and-review-20260813.md
sync_direction: bidirectional
last_reviewed: 2026-08-13
supersedes: []
superseded_by: []
---

# GKE-001 KDS Stage B run/handoff 本地提交与独立复核

- control: `GKE-001-COORDINATION-20260813-037-A10I1D4R9A1`
- control_sha256: `39c17b96c6ef9834bed15a8876a7734a253c37ede86733781cb5e33b7da42419`
- receipt: `GKE-001-COORDINATION-20260813-038-A10I1D4R9A2`
- receipt_sha256: `18d976e696cb30f8ba88da02a3bccb13f370763eabb850e36fe358f50d1abfe5`
- commit: `690ea04abf5485563b760d1bc1620493db017662`
- parent: `a7ec87412f03fb18a9f52e11f07980e6911f22a1`
- subject: `chore(kds): record document extraction handoff`
- F-013 classification: `local_stageb_run_handoff_13_commit_independent_review_passed`
- status: `active / partial / not_complete`

用户只授权在 KDS 创建 `stageb_run_handoff_13` 的单次本地提交，不授权 push、后续单元、部署或状态提升。KDS 在暂存前精确复核 `a7ec8741` 硬基线，随后只暂存 13 个授权路径；路径集、ordered manifest、37907-byte 补丁及 diff-check 均通过后创建唯一提交。

协调器与 F-013 分别只读核验 commit、parent、tree、subject、13 个 `100644` 路径、`502/0` 行统计、pathset、manifest、patch、当前 Git 状态、锁缺席和 role-view 排除哈希。F-013 同时确认提交内 handoff 保持 `partial/not_complete`，并覆盖 ACL-before-read/count、审计、lineage、canonical mirror、migration dry-run、补偿式回滚和 unresolved risks。

`66 + 23` 测试仅作为 inherited / not rerun / not live evidence。本轮未运行测试、数据库、API 或网络。提交前完整 NUL porcelain 流未由 F-013 的外部索引可靠重建，因此该单项记为 `not_independently_reproduced`；精确提交对象、当前状态哈希及排除文件哈希已经直接验证，不构成本地 handoff 提交验收阻塞。

最终 KDS 状态：HEAD `690ea04a`，origin/main `f28edb51`，ahead/behind/staged `4/0/0`，ordinary/expanded dirty `190/449`，OpsX lock absent。回滚仅允许另行复核的补偿式 `git revert`。
