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
last_reviewed: 2026-06-30
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
| recheck_date | `2026-06-30` |
| checked_repo_count | `17` |
| expected_repo_count | `17` |
| git_gate | `partial` |
| dirty_repo_count | `5` |
| pass_repo_count | `12` |
| ahead_repos | `2` |
| behind_repos | `0` |
| sensitive_repos | `0` |
| diff_check | `pass` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文保留 `GPCF-LIVE-STATUS-SNAPSHOT-20260626-001` 任务编号，并在 2026-06-30 按当前工作树重新复核 live 状态，用于替换人工记忆和失效 dirty 计数。当前 stable dirty 仓为 `GlobalCloud Brain`、`GlobalCloud Studio`、`GlobalCloud KDS`、`GlobalCloud SOP`，12 个仓 clean，且 `GlobalCloud Studio`、`GlobalCloud MMC` 出现 ahead 漂移，KDS 重新进入 dirty review 边界但 sensitive repos 仍为 0，项目群 Git gate 当前为 `partial`。GPCF 本仓在治理自更新与提交前检查过程中可能短暂显示为 dirty，仅作为 volatile observation，不作为独立业务事实入口；GFIS 已从当前 dirty 集合中剥离并保持 clean；SOP 当前保留 owner review 候选文档，因此继续处于 stable dirty 集合。Brain/Studio/KDS/SOP 作为当前稳定 review 边界，GPCF 作为治理 worktree volatile observation 一并纳入当前 live 复核，MMC 则作为 ahead-only 漂移对象单独登记。本轮不执行删除、cleanup、merge、真实 KDS API 同步、部署或状态升级。

当前单仓锚点：

```text
KDS -> globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md section = 5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要
```

```text
review_boundary_repo_count = 5
noise_cleanup_repo_count = 0
review_boundary_repos_current = GlobalCloud Brain, GlobalCoud GPCF, GlobalCloud Studio, GlobalCloud KDS, GlobalCloud SOP
noise_cleanup_repo_current = none
gpcf_dirty_count_policy = volatile_observation_not_fact_entry
```

## 2. 17 仓 Live Git 快照

| 仓库 | 分支 | upstream | dirty_count | untracked_count | ahead | behind | diff_check | 当前队列 |
|---|---|---|---:|---:|---:|---:|---|---|
| `GlobalCloud AAAS` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud Brain` | `codex/brain-l4-retrieval` | `origin/codex/brain-l4-retrieval` | 21 | 3 | 0 | 0 | `pass` | `Brain review handoff evidence refresh / dirty review required` |
| `WAS世界资产体系` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud XiaoC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud WAES` | `waes/integration-release` | `origin/waes/integration-release` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud GPC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud Studio` | `main` | `origin/main` | 2 | 0 | 13 | 0 | `pass` | `workflow permissions / session object panel / ahead review required` |
| `GlobalCoud GPCF` | `codex/kds-token-sync-gpcf` | `origin/codex/kds-token-sync-gpcf` | volatile | volatile | 0 | 0 | `pass` | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001 / REVIEW-AUTH-GPCF-WORKTREE-20260627 / governance_worktree_volatile` |
| `GlobalCloud XWAIL` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud GFIS` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / pushed c7bd07e / no pending git action` |
| `GlobalCloud MMC` | `main` | `origin/main` | 0 | 0 | 2 | 0 | `pass` | `ahead-only drift / no dirty worktree` |
| `GlobalCloud KDS` | `codex/kds-token-api-kds` | `origin/codex/kds-token-api-kds` | 119 | 95 | 0 | 0 | `pass` | `KDS runtime maintenance / distributed knowledge / assessment evidence dirty review required` |
| `GlobalCloud XiaoG` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud PVAOS` | `pvaos/D4-release-readiness-governance` | `origin/pvaos/D4-release-readiness-governance` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud SOP` | `main` | `origin/main` | 0 | 1 | 0 | 0 | `pass` | `owner review candidate untracked / review required` |
| `GlobalCloud PKC` | `codex/pkc-l4-task-notification` | `origin/codex/pkc-l4-task-notification` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud XGD` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |

## 3. 跨日漂移结论

| 项 | 2026-06-26 记录值 | 2026-06-28 live recheck | 判断 |
|---|---:|---:|---|
| dirty 仓数量 | 17 | 5 | 已收敛但仍未全量 clean：当前 stable dirty 仓为 `GlobalCloud Brain`、`GlobalCloud Studio`、`GlobalCloud KDS`、`GlobalCloud SOP`，`GlobalCoud GPCF` 保持 volatile observation |
| pass 仓数量 | 0 | 12 | 已恢复：12 仓 clean，可从旧的全量 dirty 口径中剥离 |
| ahead/behind | 0 | 2 / 0 | `GlobalCloud Studio` ahead=`13`、`GlobalCloud MMC` ahead=`2`，当前无 behind |
| sensitive_repos | 0 | 0 | KDS sensitive_path 已处理并推送，当前 sensitive repos 为空 |
| `GlobalCloud KDS` dirty | 62 | 119 | KDS 重新进入 dirty review 边界，ahead/behind 为 `0/0`，当前 sensitive repos 仍为 `0` |
| `GlobalCoud GPCF` dirty | 934 | volatile / observed_only | 治理证据聚合仍需人工 review；当前以 dirty 仓集合和门禁结果为准，GPCF 本仓瞬时行数不得作为真实事实入口或状态升级依据 |
| `GlobalCloud GFIS` dirty | 3 | 0 / ahead=0 | dirty 已由 commit `c7bd07e` 收口并推送；真实业务验证仍等待 source-of-record |
| `GlobalCloud Brain` dirty | 0 | 21 / ahead=0 | Brain evidence refresh 与 handoff 文档重新进入 stable dirty review 边界 |
| `GlobalCloud Studio` dirty | 0 | 2 / ahead=13 | Studio 进入 dirty + ahead 复合漂移，需与 release boundary review 一起收口 |
| `GlobalCloud MMC` ahead | 0 | 2 / dirty=0 | MMC 当前无 dirty worktree，但存在 ahead-only 漂移，需纳入 live baseline |
| `GlobalCloud SOP` dirty | 2 | 1 | SOP 当前新增 `docs/operations/wuhan-city-circle-sop-master-implementation-plan.md`，进入 owner review 边界 |
| `GlobalCloud AAAS/XWAIL/SOP` dirty | 0 | 0/0/1 | AAAS/XWAIL delegated wrapper dirty 已收敛；SOP 当前因 owner review 候选文档进入 stable dirty 边界，不得声明场景方案已确认或交付 |
| `WAS世界资产体系` dirty | 4 | 0 | system noise 已收敛，当前不再纳入 dirty review 边界 |

## 4. 下一步执行入口

说明：第 2 节 `dirty_count` / `untracked_count` 采用 raw expanded 口径，即 `git status --short --untracked-files=all`，会展开未跟踪目录内文件；compact 对照仅在第 3 节漂移结论中保留。因此判断状态时以 dirty 仓集合、ahead/behind/sensitive/diff_check 和当前门禁结果为准，不以单次行数作为状态升级依据。

当前 raw expanded live counts 中 `GlobalCoud GPCF` 只作为 volatile observation 记录，由 validator 实时输出并允许在提交前自更新过程中短暂出现；`GlobalCloud Brain`、`GlobalCloud Studio`、`GlobalCloud KDS` 与 `GlobalCloud SOP` 是当前 stable dirty 仓，`GlobalCloud MMC` 为 ahead-only 漂移，`GlobalCloud GFIS=0`，其余 12 仓为 0。GPCF、Brain、Studio、KDS、SOP 等包含本地证据、代码或未跟踪目录的仓库，raw expanded 数字仍会随受控证据写入继续波动。GPCF 本仓瞬时行数不得替代 GFIS 真实 source-of-record、等效正式确认文件、人工核验、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。

| 优先级 | 执行入口 | 当前动作 | 前置确认 |
|---|---|---|---|
| P0 | `GPCF-LIVE-STATUS-SNAPSHOT-20260626-001` | 按 4 仓 stable dirty + 1 仓 volatile observation + 2 仓 ahead 漂移新事实重放 dirty classification / review authorization chain，防止继续沿用失效基线；当前 review 边界收敛到 `GlobalCloud Brain / GlobalCoud GPCF / GlobalCloud Studio / GlobalCloud KDS / GlobalCloud SOP`，ahead 边界为 `GlobalCloud Studio / GlobalCloud MMC` | 需要先接受当前 live drift 为最新真实基线，再决定是否收缩授权链 |
| P0 | `GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001` | KDS sensitive_path 已处理并推送，但 2026-06-29 KDS workwiki / distributed knowledge / search anchor 改动重新进入 dirty review 边界 | 无需声明 KDS clean；真实 KDS API sync 仍未授权 |
| P0 | `GFIS-REAL-SOR-001` | GFIS dirty 已由 commit `c7bd07e` 收口并推送；本任务仍不补真实 source-of-record | 需要业务输入或人工确认保留边界 |
| P1 | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001` | 对 `Brain/Studio/KDS/SOP` stable dirty、`GPCF` volatile governance review 边界以及 `Studio/MMC` ahead 漂移做人工确认和结论登记，再进入 Wave 1 或 GPCF worktree review | 需要逐仓人工确认 |

## 5. LOOP 运行控制闭环

| 方向 | 本轮定义 |
|---|---|
| run | 重新执行 17 仓 Git clean 门禁，读取当前 17 仓 live Git 状态，形成 2026-06-28 recheck 结果，并验证 delegated loop gate 缺口已补齐 |
| stop | 停止在 `authorization_boundary`，不执行删除、stage、commit、push、真实同步或状态升级 |
| verify | 通过 `validate_project_group_live_status_snapshot_20260626.py`、Git clean 门禁和 Loop 文档门禁复核 |
| recover | 若 live 仓集合、dirty 分类或敏感路径发生变化，回滚本文并重新采集快照 |
| debug | 当前稳定阻塞是 `GlobalCloud Brain`、`GlobalCloud Studio`、`GlobalCloud KDS`、`GlobalCloud SOP` dirty 与人工确认边界，以及 `GlobalCloud Studio`、`GlobalCloud MMC` ahead 漂移；`GlobalCoud GPCF` 本仓 dirty 只作为治理自更新过程中的 volatile observation。GFIS 已 clean；KDS sensitive_path 未重新出现，远端落后和 diff_check 仍未出现 |

## 6. 禁止升级

- 不声明项目群 Git 全量 clean。
- 不声明任一 dirty 仓可 stage、commit 或 push。
- 不声明 KDS 资金报告已业务确认。
- 不声明 SOP 场景方案已确认、已交付或 KDS 事实入库。
- 不声明 GPC 外部联调、PVAOS 远程 CI、Studio release 或生产部署完成。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
