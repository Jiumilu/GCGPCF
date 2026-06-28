---
doc_id: GPCF-DOC-PROJECT-GROUP-LIVE-STATUS-SNAPSHOT-20260626
title: GlobalCloud 项目群 Live 状态快照 2026-06-26
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-live-status-snapshot-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-live-status-snapshot-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Live 状态快照 2026-06-26

## 1. 任务信息

| 项 | 内容 |
|---|---|
| task_id | `GPCF-LIVE-STATUS-SNAPSHOT-20260626-001` |
| 前置证据 | `globalcloud-project-group-dirty-disposition-queue-20260625.md`、`globalcloud-project-group-status-advancement-matrix-20260625.md` |
| 当前结论 | `project_group_live_status_snapshot_20260626 = controlled` |
| 状态候选 | `live_status_snapshot_controlled` |
| snapshot_date | `2026-06-26` |
| recheck_date | `2026-06-28` |
| checked_repo_count | `17` |
| expected_repo_count | `17` |
| git_gate | `partial` |
| dirty_repo_count | `2` |
| pass_repo_count | `15` |
| ahead_repos | `0` |
| behind_repos | `0` |
| sensitive_repos | `0` |
| diff_check | `pass` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文保留 `GPCF-LIVE-STATUS-SNAPSHOT-20260626-001` 任务编号，并在 2026-06-28 按当前工作树重新复核 live 状态，用于替换人工记忆和失效 dirty 计数。当前 dirty 仓为 `GlobalCloud Brain`、`GlobalCoud GPCF` 两仓，15 个仓 clean，且 KDS 已从当前 dirty/sensitive 阻塞源中移除，项目群 Git gate 当前为 `partial`。AAAS、WAS、XWAIL、GFIS、KDS 和 SOP 已从旧 dirty/ahead 口径中剥离；GFIS commit `c7bd07e` 已推送到 `origin/main`；SOP commit `73cd317` 已推送到 `origin/main`。本轮不执行删除、cleanup、merge、真实 KDS API 同步、部署或状态升级。

当前单仓锚点：

```text
KDS -> globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md section = 5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要
```

```text
review_boundary_repo_count = 2
noise_cleanup_repo_count = 0
review_boundary_repos_current = GlobalCloud Brain, GlobalCoud GPCF
noise_cleanup_repo_current = none
gpcf_dirty_count_policy = volatile_observation_not_fact_entry
```

## 2. 17 仓 Live Git 快照

| 仓库 | 分支 | upstream | dirty_count | untracked_count | ahead | behind | diff_check | 当前队列 |
|---|---|---|---:|---:|---:|---:|---|---|
| `GlobalCloud AAAS` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud Brain` | `codex/brain-l4-retrieval` | `origin/codex/brain-l4-retrieval` | 2 | 1 | 0 | 0 | `pass` | `Brain source ingest boundary dirty / review required` |
| `WAS世界资产体系` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud XiaoC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud WAES` | `waes/integration-release` | `origin/waes/integration-release` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud GPC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud Studio` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCoud GPCF` | `codex/kds-token-sync-gpcf` | `origin/codex/kds-token-sync-gpcf` | volatile | volatile | 0 | 0 | `pass` | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001 / REVIEW-AUTH-GPCF-WORKTREE-20260627 / governance_worktree_volatile` |
| `GlobalCloud XWAIL` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud GFIS` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / pushed c7bd07e / no pending git action` |
| `GlobalCloud MMC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud KDS` | `codex/kds-token-api-kds` | `origin/codex/kds-token-api-kds` | 0 | 0 | 0 | 0 | `pass` | `clean / pushed 042f4803 / no pending git action` |
| `GlobalCloud XiaoG` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud PVAOS` | `pvaos/D4-release-readiness-governance` | `origin/pvaos/D4-release-readiness-governance` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud SOP` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / pushed 73cd317 / no pending git action` |
| `GlobalCloud PKC` | `codex/pkc-l4-task-notification` | `origin/codex/pkc-l4-task-notification` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud XGD` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |

## 3. 跨日漂移结论

| 项 | 2026-06-26 记录值 | 2026-06-28 live recheck | 判断 |
|---|---:|---:|---|
| dirty 仓数量 | 17 | 2 | 已收敛但仍未全量 clean：当前 dirty 仓为 `GlobalCloud Brain`、`GlobalCoud GPCF` 两仓 |
| pass 仓数量 | 0 | 15 | 已恢复：15 仓 clean，可从旧的全量 dirty 口径中剥离 |
| ahead/behind | 0 | 0 | GFIS 与 SOP main 已推送，当前无 ahead/behind |
| sensitive_repos | 0 | 0 | KDS sensitive_path 已处理并推送，当前 sensitive repos 为空 |
| `GlobalCloud KDS` dirty | 62 | 0 | KDS 已 clean，HEAD `042f4803`，ahead/behind 为 `0/0` |
| `GlobalCoud GPCF` dirty | 934 | volatile / observed_only | 治理证据聚合仍需人工 review；当前以 dirty 仓集合和门禁结果为准，GPCF 本仓瞬时行数不得作为真实事实入口或状态升级依据 |
| `GlobalCloud GFIS` dirty | 3 | 0 / ahead=0 | dirty 已由 commit `c7bd07e` 收口并推送；真实业务验证仍等待 source-of-record |
| `GlobalCloud Brain` dirty | 0 | 2 | Brain 出现 `package.json` 与 `scripts/validate_brain_sources_ingest_boundary.mjs` dirty，需单独 review |
| `GlobalCloud SOP` dirty | 2 | 0 | SOP 两份方案文档已由 commit `73cd317` 收口并推送 |
| `GlobalCloud AAAS/XWAIL/SOP` dirty | 0 | 0/0/2 | AAAS/XWAIL delegated wrapper dirty 已收敛；SOP 因方案文档修改进入 owner review 边界，不得声明场景方案已确认或交付 |
| `WAS世界资产体系` dirty | 4 | 0 | system noise 已收敛，当前不再纳入 dirty review 边界 |

## 4. 下一步执行入口

说明：第 2 节 `dirty_count` / `untracked_count` 采用 raw expanded 口径，即 `git status --short --untracked-files=all`，会展开未跟踪目录内文件；compact 对照仅在第 3 节漂移结论中保留。因此判断状态时以 dirty 仓集合、ahead/behind/sensitive/diff_check 和当前门禁结果为准，不以单次行数作为状态升级依据。

当前 raw expanded live counts 中 `GlobalCoud GPCF` 只作为 volatile observation 记录，由 validator 实时输出；`GlobalCloud Brain=2`、`GlobalCloud GFIS=0`、`GlobalCloud SOP=0`、`GlobalCloud KDS=0`，其余 15 仓为 0。GPCF、Brain 等包含本地证据和未跟踪目录的仓库，raw expanded 数字仍会随受控证据写入继续波动。GPCF 本仓瞬时行数不得替代 GFIS 真实 source-of-record、等效正式确认文件、人工核验、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。

| 优先级 | 执行入口 | 当前动作 | 前置确认 |
|---|---|---|---|
| P0 | `GPCF-LIVE-STATUS-SNAPSHOT-20260626-001` | 按 2 仓 dirty 新事实重放 dirty classification / review authorization chain，防止继续沿用 4/7 仓口径；当前 review 边界收敛到 `GlobalCloud Brain`、`GlobalCoud GPCF` 两仓 | 需要先接受 2 仓 dirty live drift 为当前真实基线，再决定是否收缩授权链 |
| P0 | `GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001` | KDS sensitive_path 已处理并推送，保留为历史 cleanup 证据，不再作为当前 live 阻塞源 | 无需继续阻断本地开发；真实 KDS API sync 仍未授权 |
| P0 | `GFIS-REAL-SOR-001` | GFIS dirty 已由 commit `c7bd07e` 收口并推送；本任务仍不补真实 source-of-record | 需要业务输入或人工确认保留边界 |
| P1 | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001` | 对 `Brain/GPCF` 两仓 review 边界做人工确认和结论登记，再进入 Wave 1 或 GPCF worktree review | 需要逐仓人工确认 |

## 5. LOOP 运行控制闭环

| 方向 | 本轮定义 |
|---|---|
| run | 重新执行 17 仓 Git clean 门禁，读取当前 17 仓 live Git 状态，形成 2026-06-28 recheck 结果，并验证 delegated loop gate 缺口已补齐 |
| stop | 停止在 `authorization_boundary`，不执行删除、stage、commit、push、真实同步或状态升级 |
| verify | 通过 `validate_project_group_live_status_snapshot_20260626.py`、Git clean 门禁和 Loop 文档门禁复核 |
| recover | 若 live 仓集合、dirty 分类或敏感路径发生变化，回滚本文并重新采集快照 |
| debug | 当前阻塞是 `GlobalCloud Brain / GlobalCoud GPCF` 两仓 dirty 和人工确认边界。GFIS 与 SOP main 已推送并 clean；KDS sensitive_path 已从当前阻塞源移除，仓库缺失型 loop gate blocker 已消除，远端落后和 diff_check 仍未出现 |

## 6. 禁止升级

- 不声明项目群 Git 全量 clean。
- 不声明任一 dirty 仓可 stage、commit 或 push。
- 不声明 KDS 资金报告已业务确认。
- 不声明 SOP 场景方案已确认、已交付或 KDS 事实入库。
- 不声明 GPC 外部联调、PVAOS 远程 CI、Studio release 或生产部署完成。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
