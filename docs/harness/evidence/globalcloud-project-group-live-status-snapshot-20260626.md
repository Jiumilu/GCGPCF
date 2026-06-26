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
last_reviewed: 2026-06-26
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
| checked_repo_count | `17` |
| expected_repo_count | `17` |
| git_gate | `partial` |
| dirty_repo_count | `17` |
| pass_repo_count | `0` |
| ahead_repos | `0` |
| behind_repos | `0` |
| sensitive_repos | `0` |
| diff_check | `pass` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文只登记 2026-06-26 live 状态复核结果，用于替换人工记忆和旧 dirty 计数；本版已纳入方案识别规则写入后的全项目 dirty 状态。它不执行删除、stage、commit、push、merge、真实 KDS API 同步、部署或状态升级。

## 2. 17 仓 Live Git 快照

| 仓库 | 分支 | upstream | dirty_count | untracked_count | ahead | behind | diff_check | 当前队列 |
|---|---|---|---:|---:|---:|---:|---|---|
| `GlobalCloud AAAS` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud Brain` | `codex/brain-l4-retrieval` | `origin/codex/brain-l4-retrieval` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `WAS世界资产体系` | `main` | `origin/main` | 4 | 1 | 0 | 0 | `pass` | `DISP-WAS-SYSTEM-NOISE-20260625` |
| `GlobalCloud XiaoC` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud WAES` | `waes/integration-release` | `origin/waes/integration-release` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud GPC` | `main` | `origin/main` | 6 | 0 | 0 | 0 | `pass` | `DISP-GPC-EVIDENCE-BROWSER-20260625` |
| `GlobalCloud Studio` | `main` | `origin/main` | 12 | 4 | 0 | 0 | `pass` | `DISP-STUDIO-EVIDENCE-INDEX-20260625` |
| `GlobalCoud GPCF` | `codex/kds-token-sync-gpcf` | `origin/codex/kds-token-sync-gpcf` | 934 | 482 | 0 | 0 | `pass` | `DISP-GPCF-GOVERNANCE-EVIDENCE-20260625 / DISP-GPCF-SCHEME-RECOGNITION-20260626` |
| `GlobalCloud XWAIL` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud GFIS` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud MMC` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud KDS` | `codex/kds-token-api-kds` | `origin/codex/kds-token-api-kds` | 62 | 35 | 0 | 0 | `pass` | `DISP-KDS-FUNDING-SYNC-RUNS-20260625 / DISP-KDS-SCHEME-RECOGNITION-20260626` |
| `GlobalCloud XiaoG` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud PVAOS` | `pvaos/D4-release-readiness-governance` | `origin/pvaos/D4-release-readiness-governance` | 6 | 0 | 0 | 0 | `pass` | `DISP-PVAOS-RELEASE-GATE-20260625` |
| `GlobalCloud SOP` | `main` | `origin/main` | 16 | 8 | 0 | 0 | `pass` | `DISP-SOP-WUHAN-SCENARIO-20260625 / DISP-SOP-SCHEME-RECOGNITION-20260626` |
| `GlobalCloud PKC` | `codex/pkc-l4-task-notification` | `origin/codex/pkc-l4-task-notification` | 8 | 2 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |
| `GlobalCloud XGD` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `SCHEME-RECOGNITION-RULES-20260626` |

## 3. 跨日漂移结论

| 项 | 2026-06-25 基线 | 2026-06-26 live | 判断 |
|---|---:|---:|---|
| dirty 仓集合 | 7 | 17 | 仓集合已变：方案识别规则写入后全部项目均为 dirty |
| pass 仓数量 | 10 | 0 | 已变：全部项目存在受控文档改动 |
| ahead/behind/sensitive | 0 | 0 | 未出现版本或敏感路径风险 |
| `GlobalCloud KDS` dirty | 4 | 62 | 已发生 live 漂移，仍归入 KDS funding/sync-run owner decision 和 scheme recognition review，不升级事实状态；当前 diff_check 为 pass |
| `GlobalCoud GPCF` dirty | 156 | 934 | 治理文档、validator 与本地镜像聚合仍为 dirty，后续会随受控文档增加继续波动 |
| `GlobalCloud SOP` dirty | 7 | 16 | SOP 场景 owner review 和 scheme recognition review 均在队列内，当前 untracked_count 为 8，计数按 live Git clean gate 输出更新 |

## 4. 下一步执行入口

说明：第 2 节 `dirty_count` / `untracked_count` 采用 17 仓 Git clean gate 的 compact 口径，即 `git status --porcelain=v1`，未跟踪目录可能折叠为一行。`validate_project_group_live_status_snapshot_20260626.py` 采用 raw expanded 口径，即 `git status --short --untracked-files=all`，会展开未跟踪目录内文件。因此判断状态时以 dirty 仓集合、ahead/behind/sensitive/diff_check 和当前门禁结果为准，不以单次行数作为状态升级依据。

raw expanded dirty counts 不在本文中硬编码为固定事实；每次执行前必须以 `validate_project_group_live_status_snapshot_20260626.py` 的当次输出为准。GPCF、KDS、SOP 等包含本地镜像、证据和未跟踪目录的仓库，raw expanded 数字会随受控证据写入继续波动。

| 优先级 | 执行入口 | 当前动作 | 前置确认 |
|---|---|---|---|
| P0 | `DISP-WAS-SYSTEM-NOISE-20260625` | 选择删除 `.DS_Store` 或补充忽略规则 | 需要 `allow_delete_ds_store` 或 `allow_gitignore_update` |
| P0 | `DISP-KDS-FUNDING-SYNC-RUNS-20260625` | 业务 owner 确认资金报告口径，KDS owner 确认 sync-run 归档/纳入/删除 | 需要 business owner 与 KDS owner |
| P0 | `DISP-SOP-WUHAN-SCENARIO-20260625` | scenario owner 确认场景方案保留/返工/归档/入 KDS/对外 | 需要 scenario owner |
| P1 | `DISP-GPCF-GOVERNANCE-EVIDENCE-20260625` | 审查治理包与 KDS 本地镜像包 | 需要 review/stage/commit/push 逐项确认 |
| P1 | `DISP-GPC-EVIDENCE-BROWSER-20260625` | GPC evidence/browser review | 需要 review/stage/commit/push 逐项确认 |
| P1 | `DISP-PVAOS-RELEASE-GATE-20260625` | PVAOS release gate review | 需要 review/stage/commit/push 逐项确认 |
| P1 | `DISP-STUDIO-EVIDENCE-INDEX-20260625` | Studio evidence-index review | 需要 review/stage/commit/push 逐项确认 |

## 5. LOOP 运行控制闭环

| 方向 | 本轮定义 |
|---|---|
| run | 重新执行 17 仓 Git clean 门禁，读取 SOP live Git 状态，形成 2026-06-26 live 快照 |
| stop | 停止在 `authorization_boundary`，不执行删除、stage、commit、push、真实同步或状态升级 |
| verify | 通过 `validate_project_group_live_status_snapshot_20260626.py`、Git clean 门禁和 Loop 文档门禁复核 |
| recover | 若 live 仓集合、dirty 分类或敏感路径发生变化，回滚本文并重新采集快照 |
| debug | 当前阻塞是人工确认边界和 dirty 未处置，不是仓库缺失、远端落后、敏感路径或 diff_check 失败；当前 17 仓均存在受控文档 dirty |

## 6. 禁止升级

- 不声明项目群 Git 全量 clean。
- 不声明任一 dirty 仓可 stage、commit 或 push。
- 不声明 KDS 资金报告已业务确认。
- 不声明 SOP 场景方案已确认、已交付或 KDS 事实入库。
- 不声明 GPC 外部联调、PVAOS 远程 CI、Studio release 或生产部署完成。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
