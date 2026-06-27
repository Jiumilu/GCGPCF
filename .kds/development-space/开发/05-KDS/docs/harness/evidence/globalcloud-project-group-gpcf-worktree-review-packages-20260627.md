---
doc_id: GPCF-DOC-GPCF-WORKTREE-REVIEW-PACKAGES-20260627
title: GlobalCloud 项目群 GPCF 本仓工作区 Review 包拆分证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-gpcf-worktree-review-packages-20260627.md
source_path: docs/harness/evidence/globalcloud-project-group-gpcf-worktree-review-packages-20260627.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 GPCF 本仓工作区 Review 包拆分证据

## 授权边界

- 输入：承接项目群开发态 P0 队列，执行 `P0-D：GPCF 大工作区 review 包拆分`。
- 范围：只拆分 GPCF 本仓当前 dirty/untracked 路径族，供后续人工 review、stage、commit 授权判断使用。
- 允许动作：只读 Git gate、只读路径族统计、生成 evidence、生成只读 validator、更新开发态任务队列。
- 禁止动作：提交、推送、部署、生产写入、schema migrate、真实外部 API 写入、删除文件、清理本地镜像、stage 文件、标记 accepted/integrated/production_ready/customer_accepted。
- 判定边界：本轮只证明 GPCF 剩余 dirty 已拆成可 review 包，不证明 review 已完成，不证明 Git 全量 clean。

## 当前项目群 Git Gate

本轮运行：

```bash
python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --allow-non-pass-exit-zero
```

结果摘要：

| 字段 | 结果 |
|---|---|
| checked_repo_count | 17 |
| gate | blocked |
| clean repos | 10 |
| dirty repos | GlobalCloud AAAS、WAS世界资产体系、GlobalCoud GPCF、GlobalCloud XWAIL、GlobalCloud GFIS、GlobalCloud KDS、GlobalCloud SOP |
| sensitive repos | GlobalCloud KDS(`.env.production.example`) |
| missing/ahead/behind | none |
| diff-check | 17/17 pass |

## GPCF 路径族基线

本轮按 2026-06-28 当前工作树重新采样，`git -c core.quotePath=false status --porcelain=v1` 已扩展到 596 条路径状态。写入本证据、Loop round、validator 和文档镜像同步后，GPCF dirty 数仍可能继续波动；后续 review 必须以最新 Git 状态为准，且不得再把 GPCF 写成唯一 dirty 仓。

| 包 | 路径族 | 基线数量 | 样本 | Review 判定 |
|---|---|---:|---|---|
| GPCF-RP1 | `.kds/development-space/**` | 21 | `.kds/development-space/开发/05-KDS/docs/harness/evidence/...` | KDS 本地镜像包；只能随对应 source 文档和台账一起 review，不得写成真实 KDS API 同步完成 |
| GPCF-RP2 | `.kds/local-mirror-ledger.jsonl` | 1 | `.kds/local-mirror-ledger.jsonl` | KDS 本地镜像台账包；必须与 conflict guard pass 一起 review |
| GPCF-RP3 | `09-status/**` | 3 | `globalcloud-document-control-register.md`、`globalcloud-document-health-report.md`、`kds-development-space-sync-register.md` | 文档控制/健康/同步台账包；必须与 Loop document gate pass 一起 review |
| GPCF-RP4 | `docs/README.md`、`docs/harness/**/README.md` | 3 | `docs/README.md`、`docs/harness/README.md`、`docs/harness/evidence/README.md` | 文档索引包；只作为本地治理索引，不代表业务完成 |
| GPCF-RP5 | `docs/harness/evidence/agent-reach-p9-*` | 15 | `agent-reach-p9-source-direct-*` | Agent-Reach P9 evidence 包；需由 Agent-Reach 专项 validator 审查，不并入本轮项目群 P0 提交候选 |
| GPCF-RP6 | `tools/kds-sync/*agent_reach*` 与 `fixtures/agent-reach/**` | 7 | `validate_agent_reach_p9_*`、`project-group-full-live-search-coverage-plan-20260622.json` | Agent-Reach tooling/fixture 包；需按搜索能力专项 review |
| GPCF-RP7 | `docs/harness/evidence/globalcloud-project-group-*`、`docs/harness/loops/*PROJECT-GROUP*`、`tools/kds-sync/validate_project_group_*` | 5+ | generated-output-dist isolation evidence / loop / validator | 项目群 P0 本轮包；当前只能作为 `review-ready but blocked-by-live-gate` 候选，不得写成已可直接 review |

## Review 顺序

1. 先 review GPCF-RP7：项目群 P0 evidence/loop/validator，确认 P0 队列状态准确。
2. 再 review GPCF-RP3 + GPCF-RP4：文档台账与索引，确认文档门禁和台账一致。
3. 再 review GPCF-RP1 + GPCF-RP2：KDS 本地镜像与本地镜像台账，确认 conflict guard pass。
4. 最后 review GPCF-RP5 + GPCF-RP6：Agent-Reach 专项包，使用专项 validator，避免和项目群 P0 包混 stage。

## 硬停止

- 出现 sensitive path、behind upstream、diff-check failed、missing repo 时停止。
- 若项目群 Git gate 已从 `partial` 漂移为 `blocked`，则本证据只保留 review 包拆分结构，不得继续宣告可直接进入 REVIEW-AUTH。
- 出现真实 KDS API 写入、生产写入、schema migrate、部署、删除文件需求时停止。
- Agent-Reach 专项 validator 失败时，不影响项目群 P0 包自身证据，但不得把 Agent-Reach 包纳入提交候选。

## 状态声明

- gpcf_worktree_review_packages = recheck_required
- review_package_count = 7
- project_group_git_gate = blocked
- clean_repo_count = 10
- dirty_repo_count = 7
- dirty_repos_current = GlobalCloud AAAS, WAS世界资产体系, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP
- missing_repos = 0
- behind_repos = 0
- sensitive_repos = 1
- diff_check_failed_repos = 0
- development_start_allowed = true
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
