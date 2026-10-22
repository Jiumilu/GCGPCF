---
doc_id: GPCF-DOC-PROJECT-GROUP-CALIBER-BASELINE-20261022
title: GlobalCloud 项目群口径基准 v1.0
project: GPCF
related_projects: [GPCF, ALL]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-group-caliber-baseline-v1.0.md
source_path: 09-status/globalcloud-project-group-caliber-baseline-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群口径基准 v1.0

> 任务：PG-01（口径冻结）。性质：受控基准，只冻结"分母口径"，不提升任何项目状态。
> 非声明：本文不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`，不声明任何 Git 仓已 clean、任何授权已发生。

## 1. 定位

本文是 GlobalCloud 项目群**唯一口径基准**：规定"项目数、dirty 仓数、门禁分母、状态判定来源"四个基础量的取值来源与时点规则。任何完成度、就绪度、Git gate、授权项数的计算，必须先引用本文口径；与本文冲突的旧数字一律标注废止，不得继续作为分母。

## 2. 控制结论

```text
project_group_caliber_baseline_v1_0 = controlled
task_id = PG-01
project_count = 29
project_count_source = config/project-group-projects.yaml
dirty_source = single_live_git_status
dirty_sample_rule = one_shot_git_no_optional_locks_status_porcelain_uall
gate_denominator = 29
legacy_gate_denominator_deprecated = 17, 20
deprecated_dirty_values = 3, 5, 7, 21, 22
status_source_priority = feature_yaml_and_evidence > status_matrix_claim > project_STATUS_narrative
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 3. 现存口径清单与裁定

### 3.1 项目数口径

| 口径值 | 出处 | 时点 | 裁定 |
|---:|---|---|---|
| 17 | `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`、`...dev-task-queue-20260626.md` | 2026-06-26 | **废止**为当前分母；仅作历史基线 |
| 20 | `09-status/globalcloud-project-master-plan-control-register.md` 中的门禁表述 | 2026-07 前后 | **废止**为当前分母；仅作历史表述 |
| 29 | `config/project-group-projects.yaml`（`current_project_count: 29`，含 FireQuote） | 2026-10-22 确认 | **采用**为唯一当前分母 |
| 28 | `config/project-group-projects.yaml`（FireQuote 纳入前） | 2026-10-21 确认 | **废止**为当前分母；仅作历史基线 |

### 3.2 dirty 仓口径

| 口径值 | 出处 | 时点 | 裁定 |
|---:|---|---|---|
| 3 | `...current-state-baseline-refresh-20260626.md` | 2026-06-26 | 历史快照；**不得引用为当前值** |
| 5 | `...project_group_live_status_current.md` 引用的 live 快照 | 2026-06-26 | 历史快照；**不得引用为当前值** |
| 7 | `09-status/globalcloud-project-implementation-control-register.md` | 2026-10-21 复核（引旧证据） | 失效引用；**不得引用为当前值** |
| 21 | `...project_group_live_status_current.md` | 2026-10-21 14:16 | 过时快照；**不得引用为当前值** |
| 22 | 2026-10-22 05:15 本机实测 | 2026-10-22 | **采用**为当前基线；每次重新采集以最新一次实测为准 |

### 3.3 状态判定来源优先级

| 优先级 | 来源 | 说明 |
|---:|---|---|
| 1 | `features/active/*/feature.yaml` + 证据文件 | 可验证证据，最高优先 |
| 2 | `09-status/gpcf-project-status-matrix.md` 等受控台账声明 | 声明级，需与证据一致 |
| 3 | 各项目 `projects/<id>/STATUS.md` 叙述 | 最低；已发现 14 份为批量重生成、13 份 `last_reviewed` 仍为 2026-07-08 |

## 4. 唯一口径规则

1. **项目数**：当前项目群固定为 **29**（2026-10-22 纳入 FireQuote），以 `config/project-group-projects.yaml` 为唯一事实源；历史 17/26/27/28 项目证据保留，不重算、不覆盖。
2. **dirty 仓数**：只取**当次** `git --no-optional-locks status --porcelain -uall` 的实测结果；一次采集一个值，写清采集时点与命令；不得混用不同时点的数字。
3. **门禁分母**：固定为 **29**（随 FireQuote 纳入同步；历史 28 分母的既往门禁快照不改写）。旧 17 项目 gate 链覆盖的 11 个项目——ICP、PQC、SpaceAI、SpaceAI Studio、World、GCMEM、WAE、Project(PMC)、PDC、SLC、DRC——必须显式列入门禁覆盖清单，不得因"未在旧链内"而漏计。
4. **状态判定**：按 §3.3 优先级；声明与证据冲突时以证据为准，并触发受控台账回写。
5. **完成度**：引用 PG-02 的 VU 双账本（`runtime/vu-ledger.yaml` + `render_project_group_completion.py`），不得用 Feature 数、文档数或状态表平均数替代。
6. **待核项**：`GlobalCoud GPCF` 实测 behind 128、`GlobalCloud XiaoG` ahead 1065，性质未确认；在核清前不得用"本地为准"下结论。

## 5. 废止与影响

- 废止值：项目数 17/20；dirty 数 3/5/7/21/22 作为"当前值"的用法。
- 保留：上述数字作为历史证据的出处保留，标注时点与"历史/失效"属性。
- 影响文件（需在下次复核时引用本文）：
  - `09-status/globalcloud-project-implementation-control-register.md`
  - `09-status/globalcloud-project-group-real-execution-governance-board.md`
  - `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
  - `docs/harness/evidence/project_group_live_status_current.md`

## 6. 验证命令

```bash
python3 tools/kds-sync/validate_project_group_caliber_baseline.py
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/loop_document_gate.py
```

## 7. 非声明边界

本文只冻结分母口径，不声明：
- 任何项目真实研发/运行/集成/交付/验收完成；
- 任何 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 任何 Git 仓已 clean、任何授权已发生、任何 KDS/WAME 裁决已完成。
