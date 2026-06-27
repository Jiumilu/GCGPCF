---
doc_id: GPCF-DOC-DEV-P0-DIRTY-CLASSIFICATION-20260626
title: GlobalCloud 项目群开发态 P0-A Dirty 分类证据
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dev-p0-dirty-classification-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-dev-p0-dirty-classification-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群开发态 P0-A Dirty 分类证据

## 授权边界

- 授权范围：GlobalCloud 项目群 17 仓开发态阻点消减 P0-A。
- 允许动作：只读 Git 扫描、本地最小 evidence、validator、Loop round。
- 禁止动作：提交、推送、部署、生产写入、schema migrate、标记 accepted、integrated、production_ready。
- 本轮目标：把 17 仓 dirty/untracked 从单一阻点拆为开发态任务类别，支持正常开发工作启动。2026-06-28 live recheck 显示 Git gate 已重新收紧为 `blocked`，但 dirty 分类本身仍有效。

## 总结判定

| 字段 | 结果 |
|---|---|
| dirty_classification_ready | true |
| checked_repo_count | 17 |
| expected_repo_count | 17 |
| missing_repos | [] |
| ahead_repos | [] |
| behind_repos | [] |
| sensitive_repos | [`GlobalCloud KDS`] |
| diff_check | 17/17 pass |
| project_group_git_gate | blocked |
| development_start_allowed | true |
| accepted | false |
| integrated | false |
| production_ready | false |
| customer_accepted | false |

结论：WAES 授权不再是本轮开发态的唯一最大硬阻点；2026-06-28 当前最大剩余阻点已具体化为 7 仓 dirty、`GlobalCloud KDS/.env.production.example` sensitive_path，以及 `WAS世界资产体系/.DS_Store` / `GlobalCloud SOP/output/.DS_Store` 等本地产物隔离边界。该阻点限制提交、推送和验收，不限制开发态启动。

## 分类规则

| 路径族 | 含义 | 提交前要求 |
|---|---|---|
| governance_doc | AGENTS、README、总体方案、实施方案、治理/状态/操作文档 | owner review + frontmatter/文档门禁 |
| evidence_or_fixture | harness evidence、loop round、fixture、历史运行证据 | evidence 索引与状态边界复核 |
| harness_tooling | validator、smoke、dry-run、Loop/Git/文档门禁脚本 | 本地 validator 通过 |
| kds_mirror_or_wiki | `.kds` 本地镜像、KDS wiki | KDS diff-check、污染检查、Token 不入库 |
| test | 测试文件或 E2E spec | 对应项目测试通过 |
| config_or_workflow | package、Vitest、GitHub workflow、运行配置 | 发布/生产动作保持 blocked |
| generated_or_cache | dist、output、build、缓存等生成物 | 提交前隔离或 owner 明确确认 |
| other | 项目数据、索引、未归类路径 | owner review 后再进入提交候选 |

## 17 仓 Dirty 分类快照

> 快照说明：本表来自 2026-06-26 本轮只读扫描。新增本 evidence、Loop round 和 validator 后，GPCF 本地 dirty/untracked 数会自然增加；提交/推送前必须复跑 17 仓 Git gate。

| 项目 | 分支 | dirty | untracked | 主要路径族 | 样本 | 分类动作 |
|---|---|---:|---:|---|---|---|
| GlobalCloud AAAS | main | 3 | 0 | governance_doc:3 | M AGENTS.md; M docs/GlobalCloud AaaS 实施方案.md; M docs/GlobalCloud AaaS 总体方案.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud Brain | codex/brain-l4-retrieval | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud Brain 实施方案.md; M GlobalCloud Brain 总体方案.md | keep_as_dev_candidate_after_owner_review |
| WAS世界资产体系 | main | 4 | 1 | governance_doc:3, other:1 | M AGENTS.md; M docs/GlobalCloud WAS 实施方案.md; M docs/GlobalCloud WAS 总体方案.md; ?? .DS_Store | keep_as_dev_candidate_after_owner_review |
| GlobalCloud XiaoC | main | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud XiaoC 实施方案.md; M GlobalCloud XiaoC 总体方案.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud WAES | waes/integration-release | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud WAES 实施方案.md; M GlobalCloud WAES 总体方案.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud GPC | main | 6 | 0 | governance_doc:5, test:1 | M AGENTS.md; M GlobalCloud GPC 实施方案.md; M GlobalCloud GPC 总体方案.md; M README.md; M docs/26-gcfis-100-external-evidence-register.md | dev_candidate_requires_project_test |
| GlobalCloud Studio | main | 12 | 4 | governance_doc:6, evidence_or_fixture:3, harness_tooling:3 | M AGENTS.md; M GlobalCloud Studio 实施方案.md; M GlobalCloud Studio 总体方案.md; M docs/harness/evidence/evidence-index.md; M docs/harness/loop-state.md | keep_as_dev_candidate_after_owner_review |
| GlobalCoud GPCF | codex/kds-token-sync-gpcf | 940 | 488 | kds_mirror_or_wiki:364, evidence_or_fixture:305, harness_tooling:150, governance_doc:119 | M .codex/skills/globalcloud-loop-orchestrator/SKILL.md; M .codex/skills/globalcloud-loop-orchestrator/references/git-version-gates.md; M .codex/skills/globalcloud-ui-quality-gate/SKILL.md; M .codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md; M .harness/README.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud XWAIL | main | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud XWAIL 实施方案.md; M GlobalCloud XWAIL 总体方案.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud GFIS | main | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud GFIS 实施方案.md; M GlobalCloud GFIS 总体方案.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud MMC | main | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud MMC 实施方案.md; M GlobalCloud MMC 总体方案.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud KDS | codex/kds-token-api-kds | 62 | 35 | governance_doc:28, kds_mirror_or_wiki:25, other:9 | M AGENTS.md; M GlobalCloud KDS 实施方案.md; M GlobalCloud KDS 总体方案.md; M _governance/kds-data-quality-exceptions.json; M _governance/worktree-baseline/kds-worktree-dirty-baseline-20260625.json | keep_as_dev_candidate_after_owner_review |
| GlobalCloud XiaoG | main | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud XiaoG 实施方案.md; M GlobalCloud XiaoG 总体方案.md | keep_as_dev_candidate_after_owner_review |
| GlobalCloud PVAOS | pvaos/D4-release-readiness-governance | 6 | 0 | config_or_workflow:3, governance_doc:3 | M AGENTS.md; M GlobalCloud PVAOS 实施方案.md; M GlobalCloud PVAOS 总体方案.md; M package-lock.json; M package.json | keep_as_dev_candidate_after_owner_review |
| GlobalCloud SOP | main | 16 | 8 | governance_doc:9, other:6, generated_or_cache:1 | M AGENTS.md; M GlobalCloud SOP 实施方案.md; M GlobalCloud SOP 总体方案.md; M data/indexes/projects.json; M data/indexes/sessions.json | isolate_generated_before_commit |
| GlobalCloud PKC | codex/pkc-l4-task-notification | 8 | 2 | generated_or_cache:5, governance_doc:3 | M AGENTS.md; M GlobalCloud PKC 实施方案.md; M GlobalCloud PKC 总体方案.md; D dist/assets/index-Alkv4S2P.js; D dist/assets/index-OZjH4az7.css | isolate_generated_before_commit |
| GlobalCloud XGD | main | 3 | 0 | governance_doc:3 | M AGENTS.md; M GlobalCloud XGD 实施方案.md; M GlobalCloud XGD 总体方案.md | keep_as_dev_candidate_after_owner_review |

## 阻点拆解

| 类别 | 项目 | 开发态动作 | 提交/验收边界 |
|---|---|---|---|
| 治理文档候选 | AAAS, Brain, WAS, XiaoC, WAES, XWAIL, GFIS, MMC, XiaoG, XGD | 可继续开发，先做 owner review 与文档门禁 | 不 owner review 不进入提交候选 |
| 需项目测试 | GPC | 跑最小 GPC E2E/相关测试后再进入提交候选 | 测试失败则保持 partial |
| 发布/配置边界 | PVAOS | 允许本地开发检查，发布动作 blocked | 不触发 release/deploy |
| 工作台治理候选 | Studio | 继续 release review readiness 和 harness check | 不发布、不改 GitHub release metadata |
| KDS 知识治理候选 | KDS | 继续 KDS diff-check、污染检查、Token 安全检查 | Token 不入库，不真实 API 状态升级 |
| 生成物隔离 | SOP, PKC | 先隔离 generated/output/dist，再评估源码或文档候选 | 生成物不得直接混入提交候选 |
| GPCF 大治理工作区 | GPCF | 继续拆分 KDS mirror、harness evidence、tooling 与治理文档 | 禁止一次性整体提交，提交前需二次分类 |

## 下一步任务队列

1. P0-B：对 GPC、Studio、MMC、KDS、PKC 跑项目级最小测试或 harness。
2. P0-C：对 SOP/PKC 的 generated/output/dist 类路径做提交前隔离判断，不删除用户工作。
3. P0-D：对 GPCF 大工作区拆分为 KDS mirror、harness evidence、tooling、governance_doc 四组，分别建立提交候选边界。
4. P0-E：复跑 17 仓 Git gate，要求继续保持 no missing / no ahead / no behind / diff-check pass，并显式重放 `GlobalCloud KDS` sensitive-path 边界。

## 验证命令

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --root "/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_dev_p0_dirty_classification_20260626.py
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
