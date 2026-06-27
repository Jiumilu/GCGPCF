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
| recheck_date | `2026-06-27` |
| checked_repo_count | `17` |
| expected_repo_count | `17` |
| git_gate | `blocked` |
| dirty_repo_count | `7` |
| pass_repo_count | `10` |
| ahead_repos | `0` |
| behind_repos | `0` |
| sensitive_repos | `1` |
| diff_check | `pass` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文保留 `GPCF-LIVE-STATUS-SNAPSHOT-20260626-001` 任务编号，并在 2026-06-27 按当前工作树重新复核 live 状态，用于替换人工记忆和失效 dirty 计数。当前 dirty 仓为 `GlobalCloud AAAS`、`WAS世界资产体系`、`GlobalCoud GPCF`、`GlobalCloud XWAIL`、`GlobalCloud GFIS`、`GlobalCloud KDS`、`GlobalCloud SOP` 七仓，10 个仓 clean，且 `GlobalCloud KDS` 因 `.env.production.example` 被 Git clean gate 识别为 `sensitive_path`，所以项目群 Git gate 从 `partial` 收紧为 `blocked`。其中 `WAS世界资产体系/.DS_Store` 仍按 system noise cleanup 单独治理，不并入 `pre-wave1` 六仓 review 边界。它不执行删除、stage、commit、push、merge、真实 KDS API 同步、部署或状态升级。

当前单仓锚点：

```text
WAS -> globalcloud-project-group-first-execution-authorization-request-20260626.md section = 4.1 A 项单仓核对卡 / 4.2 A 项确认后状态传导摘要
KDS -> globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md section = 5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要
AAAS -> globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md section = 5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要
XWAIL -> globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md section = 5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要
SOP -> globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md section = 5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要
```

```text
review_boundary_repo_count = 6
noise_cleanup_repo_count = 1
review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP
noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)
```

## 2. 17 仓 Live Git 快照

| 仓库 | 分支 | upstream | dirty_count | untracked_count | ahead | behind | diff_check | 当前队列 |
|---|---|---|---:|---:|---:|---:|---|---|
| `GlobalCloud AAAS` | `main` | `origin/main` | 1 | 1 | 0 | 0 | `pass` | `loop_gate_missing_review / untracked loop_document_gate.py` |
| `GlobalCloud Brain` | `codex/brain-l4-retrieval` | `origin/codex/brain-l4-retrieval` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `WAS世界资产体系` | `main` | `origin/main` | 1 | 0 | 0 | 0 | `pass` | `noise_cleanup_pending / tracked .DS_Store` |
| `GlobalCloud XiaoC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud WAES` | `waes/integration-release` | `origin/waes/integration-release` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud GPC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud Studio` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCoud GPCF` | `codex/kds-token-sync-gpcf` | `origin/codex/kds-token-sync-gpcf` | 231 | 72 | 0 | 0 | `pass` | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627 / REVIEW-AUTH-GPCF-WORKTREE-20260627 / GPCF-EXECUTION-CONTROL-001` |
| `GlobalCloud XWAIL` | `main` | `origin/main` | 1 | 1 | 0 | 0 | `pass` | `loop_gate_missing_review / untracked loop_document_gate.py` |
| `GlobalCloud GFIS` | `main` | `origin/main` | 54 | 0 | 0 | 0 | `pass` | `GFIS-REAL-SOR-001 / existing dirty review boundary` |
| `GlobalCloud MMC` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud KDS` | `codex/kds-token-api-kds` | `origin/codex/kds-token-api-kds` | 24 | 15 | 0 | 0 | `pass` | `GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001 / sensitive_path(.env.production.example)` |
| `GlobalCloud XiaoG` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud PVAOS` | `pvaos/D4-release-readiness-governance` | `origin/pvaos/D4-release-readiness-governance` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud SOP` | `main` | `origin/main` | 2 | 1 | 0 | 0 | `pass` | `loop_gate_missing_review / output_.DS_Store_noise_pending / untracked loop_document_gate.py` |
| `GlobalCloud PKC` | `codex/pkc-l4-task-notification` | `origin/codex/pkc-l4-task-notification` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |
| `GlobalCloud XGD` | `main` | `origin/main` | 0 | 0 | 0 | 0 | `pass` | `clean / no pending git action` |

## 3. 跨日漂移结论

| 项 | 2026-06-26 记录值 | 2026-06-27 live recheck | 判断 |
|---|---:|---:|---|
| dirty 仓数量 | 17 | 7 | 已收敛但仍阻断：当前 dirty 仓为 `GlobalCloud AAAS`、`WAS世界资产体系`、`GlobalCoud GPCF`、`GlobalCloud XWAIL`、`GlobalCloud GFIS`、`GlobalCloud KDS`、`GlobalCloud SOP` 七仓 |
| pass 仓数量 | 0 | 10 | 已恢复：10 仓 clean，可从旧的全量 dirty 口径中剥离 |
| ahead/behind | 0 | 0 | 未出现版本追赶风险 |
| sensitive_repos | 0 | 1 | 新阻塞：`GlobalCloud KDS` 出现 `.env.production.example`，Git clean gate 从 `partial` 收紧为 `blocked` |
| `GlobalCloud KDS` dirty | 62 | 24 | compact 口径已下降，但 sensitive_path 仍在，review/stage/commit/push 继续阻断 |
| `GlobalCoud GPCF` dirty | 934 | 231 | 治理证据聚合仍为主要 dirty 来源，且本轮 live gate 收口已新增 delegated wrapper review 与 pre-wave1 桥接动作 |
| `GlobalCloud GFIS` dirty | 3 | 54 | 当前 dirty 明显上升，需与 `GFIS-REAL-SOR-001` 一并审查来源与保留边界 |
| `GlobalCloud AAAS/XWAIL/SOP` dirty | 0 | 1/1/2 | AAAS/XWAIL 仍为 delegated wrapper 未跟踪；SOP 额外包含 `output/.DS_Store` system noise，需与 wrapper replay 一并判定 |
| `WAS世界资产体系` dirty | 4 | 1 | 当前只剩 `.DS_Store` system noise；需沿既有 `AUTH-WAS-DELETE-DS-STORE-20260626` 路径处理，不并入 pre-wave1 六仓 review 边界 |

## 4. 下一步执行入口

说明：第 2 节 `dirty_count` / `untracked_count` 采用 17 仓 Git clean gate 的 compact 口径，即 `git status --porcelain=v1`，未跟踪目录可能折叠为一行。`validate_project_group_live_status_snapshot_20260626.py` 采用 raw expanded 口径，即 `git status --short --untracked-files=all`，会展开未跟踪目录内文件。因此判断状态时以 dirty 仓集合、ahead/behind/sensitive/diff_check 和当前门禁结果为准，不以单次行数作为状态升级依据。

当前 raw expanded live counts 为 `GlobalCloud AAAS=1`、`WAS世界资产体系=1`、`GlobalCoud GPCF=231`、`GlobalCloud XWAIL=1`、`GlobalCloud GFIS=54`、`GlobalCloud KDS=38`、`GlobalCloud SOP=2`，其余 10 仓为 0。GPCF、KDS 等包含本地镜像、证据和未跟踪目录的仓库，raw expanded 数字仍会随受控证据写入继续波动。

| 优先级 | 执行入口 | 当前动作 | 前置确认 |
|---|---|---|---|
| P0 | `GPCF-LIVE-STATUS-SNAPSHOT-20260626-001` | 按 7 仓 dirty 新事实重放 dirty classification / post-scheme queue / review authorization chain，防止继续沿用 3 仓口径；其中 6 仓 review 边界继续收口到 `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`，`WAS .DS_Store` 沿 system noise cleanup 路径单独处理 | 需要先接受 7 仓 live drift 为当前真实基线，再决定是否扩容授权链 |
| P0 | `GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001` | 审查 `GlobalCloud KDS` 的 `.env.production.example` sensitive_path，决定保留、改名、忽略或清理路径，并在执行前复跑 Git gate | 需要 KDS owner 与显式 review/cleanup 授权 |
| P0 | `GFIS-REAL-SOR-001` | 将 `GlobalCloud GFIS` 当前 dirty 审查与真实 source-of-record 补证入口合并处理，防止脏工作树掩盖真实业务输入边界 | 需要业务输入或人工确认保留边界 |
| P1 | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001` | 对 `KDS/AAAS/XWAIL/GPCF/GFIS/SOP` 六仓 review 边界做人工确认和结论登记，再进入 Wave 1 或 GPCF worktree review | 需要逐仓人工确认 |

## 5. LOOP 运行控制闭环

| 方向 | 本轮定义 |
|---|---|
| run | 重新执行 17 仓 Git clean 门禁，读取当前 17 仓 live Git 状态，形成 2026-06-27 recheck 结果，并验证 delegated loop gate 缺口已补齐 |
| stop | 停止在 `authorization_boundary`，不执行删除、stage、commit、push、真实同步或状态升级 |
| verify | 通过 `validate_project_group_live_status_snapshot_20260626.py`、Git clean 门禁和 Loop 文档门禁复核 |
| recover | 若 live 仓集合、dirty 分类或敏感路径发生变化，回滚本文并重新采集快照 |
| debug | 当前阻塞是 `GlobalCloud KDS` sensitive_path、`GlobalCloud AAAS / WAS世界资产体系 / GlobalCoud GPCF / GlobalCloud XWAIL / GlobalCloud GFIS / GlobalCloud KDS / GlobalCloud SOP` 七仓 dirty 和人工确认边界；其中 `WAS .DS_Store` 仍走 noise cleanup 路径。仓库缺失型 loop gate blocker 已消除，远端落后和 diff_check 仍未出现 |

## 6. 禁止升级

- 不声明项目群 Git 全量 clean。
- 不声明任一 dirty 仓可 stage、commit 或 push。
- 不声明 KDS 资金报告已业务确认。
- 不声明 SOP 场景方案已确认、已交付或 KDS 事实入库。
- 不声明 GPC 外部联调、PVAOS 远程 CI、Studio release 或生产部署完成。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
