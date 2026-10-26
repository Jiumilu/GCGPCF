---
doc_id: GPCF-DOC-PROJECT-GROUP-SINGLE-AUTHORIZATION-LEDGER-20261022
title: GlobalCloud 项目群单一授权清单 v1.0
project: GPCF
related_projects: [GPCF, GFIS, SOP, AAAS, XWAIL, WAME, GPC, Brain, KDS, WAS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-group-single-authorization-ledger-v1.0.md
source_path: 09-status/globalcloud-project-group-single-authorization-ledger-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群单一授权清单 v1.0

> 任务：PG-03（授权单元化）。性质：把分散在 3/5/6/7 四套文档里的待授权项收敛为**一张清单**，并给出最小可批准单元。
> 非声明：本文只登记"待授权项"，不代表任何授权已发生。`authorization_granted=false`、`action_executed=0` 在收到老卢明确口令并登记回执前保持不变。

## 1. 定位

本文是项目群**唯一待授权总清单**。任何授权请求、回执登记、到期回收都必须引用本文的 `auth_id`；与本文冲突的旧"待授权项数 3/5/6/7"一律以本文为准。

## 2. 控制结论

```text
project_group_single_authorization_ledger_v1_0 = controlled
task_id = PG-03
auth_item_count = 14
pending_confirmation_count = 2
blocked_by_pre_wave1_count = 0
historical_verify_count = 2
action_executed_count = 10
review_conclusion_count = 8
wave1_review_conclusion_count = 5
authorized_pending_execution_count = 0
executed_cleanup_count = 2
pre_wave1_concluded = true
authorized_review_only_count = 3
authorization_granted_count = 10
first_batch_recommended = 3
first_batch_auth_ids = AUTH-GPCF-SCHEME-REVIEW-20260626, AUTH-GFIS-SCHEME-REVIEW-20260626, AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 3. 四类授权单元（最小可批准单元）

| 类别 | 名称 | 允许 | 禁止 | 回执要求 |
|---|---|---|---|---|
| A | 本地开发与证据 | 本地代码/文档/脚本/测试；可回滚 Git 本地操作；跨仓代码修复（须列明仓与文件） | 生产写入、删除、发布、改权限、真实外部 API | 命令 + diff + 证据路径 |
| B | 跨仓只读审查 | 读取、review、结论登记、evidence 记录 | stage/commit/push/delete/cleanup/deploy/状态提升 | 结论 + 证据路径 + 时点 |
| C | 真实数据/外部联调 | 脱敏真实单据接收、source validation、runtime intake、外部只读联调 | 生产写入、未脱敏原件落库、对外发布、未授权 API 写 | 脱敏说明 + 回执 + 验证记录 |
| D | 发布/生产/删除/清理 | 明确的发布、部署、删除、cleanup（逐项列出对象） | 超出列明对象的一切动作 | 对象清单 + 回滚 + 验证 |

**最小可批准单元** = 一个 `auth_id` + 固定 scope + 明确禁止项 + 到期日。允许"批量口令"一次批准多个 `auth_id`，但每个 `auth_id` 仍独立登记、独立撤销。

## 4. 单一授权总清单

| # | auth_id | 类别 | 项目/仓 | 动作与范围 | 禁止 | 执行前门禁 | 回执入口 | 状态 |
|---:|---|---|---|---|---|---|---|---|
| 1 | `AUTH-GPCF-SCHEME-REVIEW-20260626` | B | GPCF | 当前治理 review + 结论登记 | stage/commit/push/delete/cleanup/真实 KDS API/状态提升 | `validate_project_group_current_state_baseline_refresh_20260626.py`、`validate_project_group_real_execution_governance_board.py`、`loop_document_gate.py` | post-scheme 回执总账 | `review_concluded` |
| 2 | `AUTH-GFIS-SCHEME-REVIEW-20260626` | B | GFIS | repair boundary review + 结论登记 | stage/commit/push/delete/cleanup/真实 SOR intake/状态提升 | `validate_project_group_pre_wave1_review_authorization_request_20260627.py`、`validate_gfis_real_fact_entry_gate.py`、`loop_document_gate.py` | post-scheme 回执总账 | `review_concluded` |
| 3 | `AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627` | B | SOP | delegated wrapper review + 结论登记 | stage/commit/push/delete/cleanup/真实 KDS API/状态提升 | `validate_project_group_pre_wave1_review_authorization_request_20260627.py`、`validate_project_group_external_loop_gate_delegate_baseline_20260627.py`、`loop_document_gate.py` | post-scheme 回执总账 | `review_concluded` |
| 4 | `AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627` | B | AAAS | delegated wrapper 单仓核对卡 review + 结论登记 | stage/commit/push/delete/状态提升 | `validate_project_group_external_loop_gate_delegate_baseline_20260627.py`、`loop_document_gate.py` | post-scheme 回执总账 | `review_concluded` |
| 5 | `AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627` | B | XWAIL | delegated wrapper 单仓核对卡 review + 结论登记 | stage/commit/push/delete/状态提升 | `validate_project_group_external_loop_gate_delegate_baseline_20260627.py`、`loop_document_gate.py` | post-scheme 回执总账 | `review_concluded` |
| 6 | `AUTH-WAVE1-WAME-LINT-RUNTIME-20260626` | A | WAME | lint/runtime 修复与本地验证 | 发布、注册、权限变更、生产写入 | Wave1 readiness gate + `npm run lint` + runtime smoke | execution 回执总账 | `review_concluded` |
| 7 | `AUTH-WAVE1-GFIS-REAL-SOR-20260626` | C | GFIS | 真实 source-of-record 接收与验证（脱敏） | 未脱敏落库、生产写入、客户验收声明 | Wave1 readiness gate + source validation + runtime intake | execution 回执总账 | `pending_confirmation` |
| 8 | `AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626` | C | GPC | 外部 runtime 联调与证据采集 | 生产写入、对外承诺、客户验收声明 | Wave1 readiness gate + external runtime check | execution 回执总账 | `pending_confirmation` |
| 9 | `AUTH-WAVE1-BRAIN-HUMAN-REVIEW-20260626` | B | Brain | 人工 review 与结论登记 | 写 KDS 事实、自动确认、状态提升 | Wave1 readiness gate + Brain handoff 检查 | execution 回执总账 | `review_concluded` |
| 10 | `AUTH-WAVE1-GPCF-POST-SCHEME-REVIEW-20260626` | B | GPCF | post-scheme review 与结论登记 | stage/commit/push/delete/状态提升 | Wave1 readiness gate + post-scheme command pack | execution 回执总账 | `review_concluded` |
| 11 | `AUTH-KDS-DIFFCHECK-CLEANUP-20260626` | D | KDS | whitespace-only diff cleanup（逐文件列出） | 非列明文件的任何修改、API 同步、commit/push | cleanup precheck + `git diff --check` + 回滚脚本 | execution 回执总账 | `executed_concluded` |
| 12 | `AUTH-WAS-DELETE-DS-STORE-20260626` | D | WAS | 删除 `.DS_Store` 噪声文件（逐文件列出） | 其它文件删除、commit/push | 文件清单 + 确认无业务内容 + 归档副本 | execution 回执总账 | `executed_concluded` |
| 13 | `AUTH-KDS-OWNER-DECISION-20260626` | B | KDS | KDS owner decision 登记 | 代 owner 决策、状态提升 | owner 确认记录 | post-scheme 回执总账 | `待核（是否仍 active）` |
| 14 | `AUTH-KDS-SCHEME-REVIEW-20260626` | B | KDS | KDS scheme review 与结论登记 | stage/commit/push/delete/状态提升 | KDS review gate | post-scheme 回执总账 | `待核（是否仍 active）` |

## 5. 首批授权（3 项，2026-10-22 已批准）

依据现有决策板：**Pre-Wave1 未确认前，Wave 1 连执行回执都不允许生成**（`wave1_entry_blocked_by_pre_review=true`）。因此首批只批 3 项，均为 **B 类只读审查**，不涉及写代码、不涉及真实数据、不涉及删除：

```text
授权 AUTH-GPCF-SCHEME-REVIEW-20260626：只允许人工 review 和结论登记；不允许 stage、commit、push、delete、cleanup、deploy、真实 KDS API 同步、真实外部 API 写入或状态提升。
授权 AUTH-GFIS-SCHEME-REVIEW-20260626：只允许人工 review 和结论登记；不允许 stage、commit、push、delete、cleanup、deploy、真实 SOR intake、真实外部 API 写入或状态提升。
授权 AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627：只允许人工 review 和结论登记；不允许 stage、commit、push、delete、cleanup、deploy、真实 KDS API 同步、真实外部 API 写入或状态提升。
```

批量等价口令：

```text
授权 GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627 的 GPCF/GFIS/SOP 3 仓 review 边界：只允许人工 review 和结论登记；不允许 stage、commit、push、delete、cleanup、deploy、真实 KDS API 同步、真实外部 API 写入或状态提升。
```

**2026-10-22 05:38 老卢经问答批准全部 3 项。** 已登记回执（`runtime/authorization-receipts.yaml`），随后执行：跑 3 项执行前只读门禁 → 准备 review 包 → 人工 review → 记录结论。**本授权不改变任何项目状态。**

## 6. 回执与到期

- 回执字段：`auth_id / granted_at / granted_by / scope / actions_allowed / actions_forbidden / expires_at / evidence / revoked_at`。
- 台账：`runtime/authorization-receipts.yaml`（append-only，只追加不删除）。
- 到期：默认 14 天；到期未执行自动失效，需重新确认。
- 撤销：登记 `revoked_at` 即失效；已执行动作不自动回滚，按各动作回滚边界处理。

## 7. 验证命令

```bash
python3 tools/kds-sync/validate_project_group_single_authorization_ledger.py
python3 tools/kds-sync/loop_document_gate.py
```

## 8. 非声明边界

本文不声明：
- 任何授权已经发生（`authorization_granted=false`）；
- 任何动作已经执行（`action_executed=0`）；
- 任何 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 任何项目状态已升级。

## 9. 授权登记记录（append-only）

| 时点 | auth_id | 授权人 | 依据 | 范围 | 到期 |
|---|---|---|---|---|---|
| 2026-10-22 05:38 | `AUTH-GPCF-SCHEME-REVIEW-20260626` | 老卢 | 问答批准全部 3 项 | 只读 review + 结论登记 + 执行前只读门禁 | 2026-11-05 |
| 2026-10-22 05:38 | `AUTH-GFIS-SCHEME-REVIEW-20260626` | 老卢 | 问答批准全部 3 项 | 只读 review + 结论登记 + 执行前只读门禁 | 2026-11-05 |
| 2026-10-22 05:38 | `AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627` | 老卢 | 问答批准全部 3 项 | 只读 review + 结论登记 + 执行前只读门禁 | 2026-11-05 |

> 回执原文见 `runtime/authorization-receipts.yaml`；本表只追加，不改写。授权不包含 stage/commit/push/delete/cleanup/deploy/真实数据接入/状态提升。
