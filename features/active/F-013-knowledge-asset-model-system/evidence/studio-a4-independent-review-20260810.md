---
doc_id: GPCF-DOC-F013-STUDIO-A4-INDEPENDENT-REVIEW-20260810
title: Studio A4 独立只读复核
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/studio-a4-independent-review-20260810.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/studio-a4-independent-review-20260810.md
sync_direction: bidirectional
last_reviewed: 2026-08-10
supersedes: []
superseded_by: []
---

# Studio A4 独立只读复核

## 判定

```yaml
handoff_result:
  change_id: integrate-studio-kds-knowledge-intake
  reviewed_commit: 1f63a464ce017c3394f3733200618f678a016674
  reconciliation: GKE-001-COORDINATION-20260810-001-A5
  audit_timestamp: 2026-08-10T01:46:48Z
  final_status: partial
  technical_decision: rework_required
  repository_state: clean_main_equals_origin_main
  phase_1_classification: simulated_only
  phase_2_authorized: false
  real_kds_or_mmc_write: false
  allow_archive: false
  status_ceiling: partial
  completion: not_complete
```

当前实现保持无 KDS/MMC 写入、无 Studio 本地知识主账，聚焦测试、模拟浏览器测试、构建、OpenSpec 与 Studio Harness 均通过。但 A4 的可信身份、canonical read contract 和浏览器任务验收要求尚未完整实现，不能判为 `technical_review_verified`、`accepted`、`integrated` 或 `production_ready`。

## 发现

### P1-1 允许角色未执行

A4 要求可信用户角色仅为 `admin` 或 `super_admin`。当前 `AuthenticatedUser` 包含 `role`，但 `trustedKnowledgeIntakeContext()` 未读取或校验该字段；现有路由测试也只构造 `admin`，没有非允许角色拒绝回归。因此任意已登录且满足 tenant/business identity 与项目 binding 的角色都可进入 Phase 1 prepare 路径，未实现 A4 明示的权限上限。

证据：

- A4 `trusted_identity_inputs.user_identity.allowed_roles`
- Studio `packages/server/src/middleware/user-auth.ts:28`
- Studio `packages/server/src/services/governance/knowledge-intake.ts:102`
- Studio `tests/server/project-knowledge-intake-route.test.ts:118`

### P1-2 组织绑定无法与认证上下文核对

A4 要求项目会话 binding 的 tenant 与 org 都匹配认证上下文。当前 `AuthenticatedUser` 没有 `orgId`，`trustedKnowledgeIntakeContext()` 只比较 tenant/business role/sensitivity，随后直接返回 binding 的 `orgId`。这使 `tenant_and_org_match_authenticated_context` 中的 org 条件既未实现，也无法由当前类型表达。

证据：

- A4 `project_session_binding.requirements`
- Studio `packages/server/src/middleware/user-auth.ts:28`
- Studio `packages/server/src/services/governance/knowledge-intake.ts:114`
- Studio `packages/server/src/services/governance/knowledge-intake.ts:125`

### P1-3 canonical 只读合同不完整

A4 v0.1 明列 Stage A search/asset/content/versions 和 Stage B extractions/content/evidence-links 只读端点。当前 `KDS_KNOWLEDGE_INTAKE_CONTRACT` 仅声明 revision、manifest、intake 与 retry，未提供上述只读端点、方法或投影类型；OpenSpec 却将 status、version、extraction、evidence 合同任务标记完成。Phase 1 可继续保持 capability-blocked，但不能把当前合同视为已完整实现。

证据：

- A4 `canonical_contract.endpoints.stage_a_read` 与 `stage_b_read`
- Studio `packages/server/src/services/core/kds-client.ts:30`
- Studio `openspec/changes/integrate-studio-kds-knowledge-intake/tasks.md:3`

### P1-4 浏览器任务场景证据不足

A4 要求 success、duplicate、409、429/502/503/504、failed/retry、403/404 no-leak 和 cancellation/navigation 浏览器场景。当前 Playwright 只有三项：success、duplicate 加 502、navigation cancellation；第二项标题包含 conflict，但实现没有产生 409。服务端路由测试覆盖部分状态码，不能替代 A4 明示的浏览器任务证据。

证据：

- A4 `browser_task_flow.scenarios`
- Studio `tests/e2e/project-session-knowledge-intake.spec.ts:34`
- Studio `tests/e2e/project-session-knowledge-intake.spec.ts:49`
- Studio `tests/e2e/project-session-knowledge-intake.spec.ts:69`
- Studio `tests/server/project-knowledge-intake-route.test.ts:68`

### P2-1 确定性内容 SHA 与幂等键未建立

A4 测试资产要求 deterministic SHA-256。当前面板的幂等键仅由文件名和大小组成，没有计算内容 SHA-256；同名同大小但内容不同的文件会得到相同键。Phase 1 不上传内容，因此尚未造成 KDS 事实冲突，但该实现不能作为 Phase 2 幂等基础。

证据：

- A4 `browser_task_flow.test_asset.deterministic_sha256`
- Studio `packages/client/src/components/studio/ProjectKnowledgeIntakePanel.vue:53`

### P2-2 文件边界仅做最小结构校验

当前面板允许任意文件类型，服务端仅校验文件名、非空 content type、非负安全整数大小、幂等键和确认状态；没有把 A4 的 synthetic text/markdown 测试资产范围表达为允许类型或大小上限。Phase 1 无内容写入，风险暂时受 capability block 限制；进入任何后续写入阶段前必须收口。

证据：

- A4 `browser_task_flow.test_asset`
- Studio `packages/client/src/components/studio/ProjectKnowledgeIntakePanel.vue:91`
- Studio `packages/server/src/services/governance/knowledge-intake.ts:138`

## 已验证能力

| Evidence ID | Source | Command/File | Result | Freshness | Trust Level | Status Impact |
|---|---|---|---|---|---|---|
| STUDIO-A4-R1 | Studio current HEAD | focused Vitest: intake route/client/panel + SessionObjectPanel | 4 files, 101 tests passed | current | machine_generated | implementation verified, findings not cleared |
| STUDIO-A4-R2 | Studio current HEAD | Playwright `project-session-knowledge-intake.spec.ts` | 3/3 passed, mocked only | current | machine_generated | simulated_only |
| STUDIO-A4-R3 | Studio current HEAD | `npm run build` | passed | current | machine_generated | build verified |
| STUDIO-A4-R4 | Studio current HEAD | OpenSpec strict validation | passed | current | machine_generated | specification parses; completeness findings remain |
| STUDIO-A4-R5 | Studio current HEAD | Studio Loop validator and Harness | passed, LR-874 waived round selected | current | machine_generated | governance gate aligned, not product acceptance |
| STUDIO-A4-R6 | Studio Git | HEAD and origin/main | both `755f7b5d3583601418fc51abc828837d4dc1df30`, worktree clean | current | machine_generated | A5 freeze review baseline stable |

## 保持成立的边界

- Phase 1 结果明确标记 `simulated_only` 与 `capability_blocked`。
- 未执行真实或共享 KDS/MMC 调用、资料写入、版本写入、证据写入、长期记忆写入、关系确认或业务状态改变。
- `hermes_local_draft` 未被改造为知识事实主账。
- A5 冻结已由 Studio lane 确认；本轮未修改 Studio 仓库、未提交、未推送、未部署、未重写或回滚已发布历史。

## 后续门禁

Studio lane 继续冻结。修复上述 P1/P2 发现需要 coordinator 另行下发精确返工 amendment，包含 change_id、文件 allowlist、测试场景和证据范围。在此之前不得进行产品或证据写入，也不得进入 Phase 2、Brain 只读 E2E、真实 KDS/MMC 写入或状态提升。
