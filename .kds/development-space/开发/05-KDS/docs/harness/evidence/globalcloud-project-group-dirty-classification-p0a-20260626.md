---
doc_id: GPCF-DOC-DIRTY-CLASSIFICATION-P0A-20260626
title: GlobalCloud 项目群 P0-A Dirty 分类证据
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dirty-classification-p0a-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-dirty-classification-p0a-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 P0-A Dirty 分类证据

## 授权边界

- 授权范围：GlobalCloud 项目群 17 仓开发态阻点消减 P0-A。
- 允许动作：本地只读采样、最小 evidence、只读 validator、文档门禁同步。
- 禁止动作：提交、推送、部署、生产写入、schema migrate、标记 accepted、integrated、production_ready、customer_accepted。
- 当前判断：WAES 授权不是开发态全面启动的最大阻点；WAES/人工确认仍是验收态和状态提升边界。2026-06-28 live recheck 下，开发态当前最大阻点已具体化为 7 仓 dirty 工作区、`GlobalCloud KDS/.env.production.example` sensitive_path，以及未完成的逐仓处理队列。

## P0-A 成功标准

| 标准 | 结果 |
|---|---|
| 17 仓存在并纳入分类 | pass |
| missing/ahead/behind | none |
| sensitive path | `GlobalCloud KDS/.env.production.example` |
| `git diff --check` | 17/17 pass |
| dirty 类型已分流 | pass |
| 开发态是否可启动 | yes |
| 是否进入验收态 | no |

## Git Gate 快照

本轮分类以 2026-06-26 本地只读采样为准。生成本 evidence、Loop round 和 validator 后，GPCF dirty/untracked 数字会自然增加；最终 hard blocker 以 validator 重跑的 17 仓 Git gate 为准。

| 字段 | 结果 |
|---|---|
| checked_repo_count | 17 |
| expected_repo_count | 17 |
| gate | blocked |
| missing_repos | [] |
| ahead_repos | [] |
| behind_repos | [] |
| sensitive_repos | [`GlobalCloud KDS`] |
| diff_check | 17/17 pass |
| remaining_gate_reason | 7 仓 dirty + `GlobalCloud KDS` sensitive_path；`WAS .DS_Store` 与 `SOP output/.DS_Store` 继续沿本地产物路径隔离 |

## 17 仓 Dirty 分类

| 项目 | dirty/untracked | 主要文件族 | 分类 | 开发态动作 | 硬停止 |
|---|---:|---|---|---|---|
| GlobalCloud AAAS | 3/0 | `AGENTS.md`; `docs/GlobalCloud AaaS 实施方案.md`; `docs/GlobalCloud AaaS 总体方案.md` | scheme_transmission_review_candidate | 复核方案传导，保持 diff-check pass | 不提交未确认方案 |
| GlobalCloud Brain | 3/0 | `AGENTS.md`; `GlobalCloud Brain 实施方案.md`; `GlobalCloud Brain 总体方案.md` | scheme_transmission_review_candidate | 复核方案传导，必要时复跑 build | 不提升 integrated |
| WAS世界资产体系 | 4/1 | `AGENTS.md`; WAS 总体/实施方案; `.DS_Store` | scheme_transmission_plus_local_artifact | 方案传导复核；`.DS_Store` 仅作为本地遗留候选处理 | 不提交 `.DS_Store` |
| GlobalCloud XiaoC | 3/0 | `AGENTS.md`; XiaoC 总体/实施方案 | scheme_transmission_review_candidate | 复核模型/编排边界传导 | 不扩大到 live 调用 |
| GlobalCloud WAES | 3/0 | `AGENTS.md`; WAES 总体/实施方案 | authorization_boundary_review_candidate | 复核 WAES 治理边界；只做开发态治理候选 | 不标记 accepted |
| GlobalCloud GPC | 6/0 | `AGENTS.md`; GPC 总体/实施方案; `README.md`; evidence register; e2e spec | platform_evidence_e2e_review_candidate | 复核外部证据登记和 e2e 调整 | 不声明业务闭环完成 |
| GlobalCloud Studio | 12/4 | `docs/harness`; `scripts`; Studio 总体/实施方案 | release_review_readiness_candidate | 复核 release review checklist 与 validator | 不部署、不发布 |
| GlobalCoud GPCF | 666/230 | `.kds/development-space`; `docs/harness`; `tools/kds-sync`; `.harness`; `fixtures` | governance_evidence_kds_mirror_queue | 拆分治理、KDS mirror、evidence、工具链候选；禁止一次性直接提交 | 不跳过文档门禁 |
| GlobalCloud XWAIL | 3/0 | `AGENTS.md`; XWAIL 总体/实施方案 | scheme_transmission_review_candidate | 复核 WAES/AAAS contract 边界 | 不进入集成态 |
| GlobalCloud GFIS | 3/0 | `AGENTS.md`; GFIS 总体/实施方案 | runtime_sop_boundary_review_candidate | 复核运行 SOP 口径；真实业务凭证留作验收态阻点 | 不伪造 source-of-record |
| GlobalCloud MMC | 3/0 | `AGENTS.md`; MMC 总体/实施方案 | scheme_transmission_review_candidate | 复核模板/治理口径；必要时复跑 runtime tests | 不扩大配置面 |
| GlobalCloud KDS | 61/35 | `wiki/sources`; `concepts`; `_governance`; `entities` | knowledge_import_governance_queue | 分类知识导入、治理流水、概念实体同步 | 不绕过 KDS 门禁 |
| GlobalCloud XiaoG | 3/0 | `AGENTS.md`; XiaoG 总体/实施方案 | scheme_transmission_review_candidate | 复核 live API 授权边界 | 不触发 live API |
| GlobalCloud PVAOS | 6/0 | `AGENTS.md`; PVAOS 总体/实施方案; `package*.json`; `vitest.config.ts` | release_gate_test_config_review_candidate | 复核 release gate 测试配置变化 | 不发布 release |
| GlobalCloud SOP | 16/8 | `docs/operations`; `data`; `docs/standardization`; `output` | sop_operations_owner_review_candidate | 分类 SOP 运行包、索引和 owner review 候选 | 不把草案当生产指令 |
| GlobalCloud PKC | 8/2 | `dist`; `AGENTS.md`; PKC 总体/实施方案 | build_artifact_review_candidate | 复核 dist 产物是否与构建证据匹配 | 不提交失配构建产物 |
| GlobalCloud XGD | 3/0 | `AGENTS.md`; XGD 总体/实施方案 | scheme_transmission_review_candidate | 复核 TICK/Brain smoke 边界 | 不触发桌面/live 调用 |

## 开发态任务队列

| 队列 | 项目 | 处理方式 | 验证 |
|---|---|---|---|
| P0-A1 | GPCF, KDS | 大工作区拆分：治理/evidence/KDS mirror/工具链分别形成候选包 | `loop_document_gate.py`; KDS smoke |
| P0-A2 | Studio, PVAOS, PKC, GPC | 工程变更复核：release/test/build/e2e 相关 | 项目级 build/test/harness |
| P0-A3 | SOP, WAS | 本地/草案产物隔离：`.DS_Store`、`output/`、operations 草案 | `git status`; owner review |
| P0-A4 | AAAS, Brain, XiaoC, WAES, XWAIL, GFIS, MMC, XiaoG, XGD | 方案传导复核：AGENTS + 总体/实施方案 | `git diff --check -- .` |

## 验证命令

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --root "/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_dirty_classification_p0a_20260626.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/kds_conflict_guard.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/check_document_pollution.py
```

## 状态声明

- dirty_classification_ready = true
- development_start_allowed = true
- project_group_git_gate = blocked
- dirty_repo_count = 7
- sensitive_repos = GlobalCloud KDS(.env.production.example)
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
