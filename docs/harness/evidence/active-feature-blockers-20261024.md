---
doc_id: GPCF-DOC-ACTIVE-FEATURE-BLOCKERS-20261024
title: 活跃 Feature 阻塞清单（2026-10-24）
project: GPCF
related_projects: [GPC, PVAOS, WAME, KDS, Brain, PKC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/active-feature-blockers-20261024.md
source_path: docs/harness/evidence/active-feature-blockers-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# 活跃 Feature 阻塞清单（2026-10-24）

| ID | name | status | check-only | blockers |
|---|---|---|---|---|
| F-005 | factory-exception-intake-dry-run | active | false | — |
| F-012 | icp-sop-foundation-coupling | active | false | — |
| F-013 | knowledge-asset-model-system | active | false | ~~kds_p1_apply_blocked_by_dirty_worktree~~（2026-10-24 已解除：KDS 脏树 4266→1，见 docs/reports/collab-completion-20261024.md §9）; gpcf_a10r27_current_truth_4file_delta_pending_independent_review_and_separate_commit_push_disposition; kds_green_supply_chain_role_view_local_commit_pending_separate_human_authorization; brain_browser_r2_postpush_revalidated_chat_send_not_executed_mobile_ui_rework_required; brain_authenticated_readonly_e2e_deferred_pending_a10_control; studio_release0_external_daily_sync_post_sync_governance_disposition_pending; kds_release0_runtime_activation_independently_verified_local_gbrain_missing_knowledge_intake_audit_relation; kds_local_gbrain_schema_inventory_and_separate_migration_fixture_authorization_required; studio_gehua_authoritative_project_session_target_fixture_lifecycle_not_executed; kds_stage_b_read_admission_technical_verified_governance_blocked; studio_intake_phase1_authorized_phase2_blocked_by_mmc_prepare_retry_policy_review; studio_a6_external_daily_sync_commit_push_requires_governance_disposition; unexpected_external_kds_local_mirror_write_requires_review; mmc_a9_bounded_read_subset_technical_verified_global_policy_not_narrowed; mmc_delegation_and_human_confirmation_pending |
| F-014 | industrial-meeting-to-project-control-loop | active | false | B3 KDS/MMC 运行配置边界变更未授权（跨项目运行态配置，需属主执行）；真实试点已获批 B1+B2，执行回执待回填 |
| F-016 | industrial-green-chain-graph-readonly-pilot | active | false | 业务确认人、来源读取权限、正式 SOP 版本、试点验收人待落实（不虚构任命）; B2—B5 放行依赖 B1 完成与各自授权流程 |
| F-017 | cwme-city-world-model-engine | active | false | D1 命名已确认「万象引擎」；D6 首个演示对象＝光谷（2026-10-11 按建议；如调整请指出）; GPU 验证环境与光谷/黄梅数据场地接触待排期; B4-1—B4-5 首月件已完成（2026-10-11；见 evidence/summary.md）；申请一（域包登记）已提交，decision 待治理方 |
| F-021 | world-project-onboarding | blocked | false | World 总体方案 Ontology 版本与现行基线冲突（World 方案 0.2.x vs WAS 实发 0.2.0），项目方案仍为 candidate；需 WAS 出具基线裁定（见 docs/reports/f021-was-ontology-ruling-request-20261022.md） |
| F-022 | was-scenario-flow-extension | active | false | WAS 侧治理复核（承接方式与六项声明）待进行; XWAIL flowType 影响评估待进行 |
| F-023 | was-flow-naming-migration | active | false | 兼容窗口关闭时点（另行版本发布）待定; 存量引用（GPCF fixtures／KDS WAME 文档）切换批次待排 |
| F-025 | project-group-arch-iteration | active | false | 架构迭代分析与分期规划尚需逐项复核；本 Feature 不代表真实开发完成 |
| F-029 | hermes-ai-runtime-admission | active | false | Hermes /v1/skills 已修复；同一完整接口测试文件在独立临时克隆中 114 项通过，原安装路径的 16 项失败已定位为测试隔离守卫冲突；跨模块完整套件未运行; 对外 Hermes Web UI 返回 502，本机 8648 未监听；恢复前须核实访问控制，恢复动作待授权; DSH headless 已完成限定任务包及隔离测试补充材料的只读复核；未执行完整源码审查或完整 Hermes 测试套件; 主值守为用户本人；用户确认暂无替补，告警通道未指定，试点项目恢复责任人与权限隔离证据仍待核实 |
| F-032 | pqc-external-service-via-pvaai | active | false | — |
| F-033 | r1-ecosystem-integration | active | false | WAME 正式治理裁定/发布（本轮为 PoC governor，scope 限定联调）; 消费方实际联调（XiaoG 会话验证、PKC 浏览器联调、XGD/飞书 工具范围）; GPCF 状态复核（本 feature 处于 evidence 步，未 done） |
| F-034 | wae-p0-shell-and-role-convergence | active | false | 2026-10-22 回滚：状态提升未经老卢确认（WAE 侧长期目标纪律：F-034 至多 ready_for_review）。原 status: done 由另一 Agent 依据其 2026-10-22 18:02 自建证据置位，未覆盖 WAE 主线后续证据（O1 因 A2 删框架壳已改述、O3 项目侧未归并、PKC/Brain/PVAOS 未接入）。; O2 跨仓令牌：PKC 快照过期（缺 12 令牌）、Brain 5 独有+28 差异，整改属两仓属主; O3 侧栏统一：WAE 产品壳首例已落（WameSidebarPlugin + capability）；WAME 侧 F-035 已 closed（app-registry 契约消费 + E2E 冒烟）；WAE 项目侧三套仍未归并; M3 首批接入（Studio 例外→PKC→Brain→PVAOS）：Studio 例外材料待三方签；PKC 侧 7 项待属主; task_flow_e2e_status / evidence_overexposure_gate：仍待运行时证据 |
| F-036 | wae-pkc-intake-integration | active | false | PKC P4/P5 已最小接入：gc 令牌快照 + theme 映射（C6 0→117）、7 值状态字典 + StatusBadge（C5 存在）；残留=非真实包消费、部分页面未迁移、C1/C4/C10 既有项; PKC 真实运行时受控嵌入：dev bypass 与登录态（system-admin + 隔离 IdP）均已验证点击后 iframe 加载 PKC Home（evidence/embed-20261023、embed-auth-20261023）；WAE 修复已 push（d9d9ee9/3247e53）；生产构建/CSP/SSO/403 未验证; 正式评审已做（evidence/formal-review-20261024.md）：conditional，不批准关闭；CSP frame-ancestors 行为已验证（csp-20261024）；生产部署/SSO/403 与属主签字未满足 |
| F-037 | map-3d-l4-precision-model | active | false | 真实 L4 资产未接入：采购、自采、合规外部数据三条路径均未授权（2026-10-22 决定暂停自采）；真实几何精度需供应商质检或实测后方可验收 |
| F-038 | panorama-operation-normalization | active | false | B5 剩余五大块（卡片列 / 气泡 / 飞翔 / CWME / 控制器）仍在内联，PanoramaDeep.vue script 目标未达; i18n 约 600 行与人工验收未完成，属下一轮范围; 工作区仍有并行会话 WIP（apps/desktop、pnpm-workspace.yaml 等），本 Feature 未纳入 |
