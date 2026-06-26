---
doc_id: GPCF-DOC-PROJECT-GROUP-AUTHORIZATION-ROUTING-20260625
title: GlobalCloud 项目群授权路由证据 2026-06-25
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-authorization-routing-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-authorization-routing-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群授权路由证据 2026-06-25

## 1. 任务标识

| 项 | 内容 |
|---|---|
| task_id | `GPCF-AUTHORIZATION-PACKAGE-ROUTING-001` |
| 前置证据 | `globalcloud-project-group-review-packages-20260625.md`、`globalcloud-project-group-human-confirmation-request-20260625.md`、`globalcloud-project-group-next-executable-task-packs-20260625.md` |
| 当前结论 | `project_group_authorization_routing = prepared` |
| 状态候选 | `authorization_routing_ready` |
| review_package_count | `4` |
| hold_package_count | `3` |
| confirmation_item_count | `7` |
| review_allowed | `false` |
| stage_allowed | `false` |
| commit_allowed | `false` |
| push_allowed | `false` |
| delete_allowed | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文只建立授权路由，不代表用户已经授权 review、stage、commit、push、delete、accepted、integrated 或 customer acceptance。

## 2. 授权路由总览

| 路由 ID | 来源包 | 当前路由 | 允许动作 | 必须确认 | 禁止声明 |
|---|---|---|---|---|---|
| `ROUTE-GPC-EVIDENCE-BROWSER-20260625` | `PKG-GPC-EVIDENCE-BROWSER-20260625` | `review_candidate` | `none_until_user_confirmation` | `allow_review`、`allow_stage`、`allow_commit`、`allow_push` | 不声明外部联调完成、生产确认完成或客户验收 |
| `ROUTE-PVAOS-RELEASE-GATE-20260625` | `PKG-PVAOS-RELEASE-GATE-20260625` | `review_candidate` | `none_until_user_confirmation` | `allow_review`、`allow_stage`、`allow_commit`、`allow_push` | 不声明远程 CI、PR、merge、生产发布或客户验收 |
| `ROUTE-GPCF-GOVERNANCE-EVIDENCE-20260625` | `PKG-GPCF-GOVERNANCE-EVIDENCE-20260625` | `review_candidate` | `none_until_user_confirmation` | `allow_review`、`allow_stage`、`allow_commit`、`allow_push` | 不声明项目群 Git clean、可提交、可推送或验收 |
| `ROUTE-GPCF-KDS-MIRROR-20260625` | `PKG-GPCF-KDS-MIRROR-20260625` | `mirror_review_candidate` | `none_until_user_confirmation` | `allow_review`、`allow_stage`、`allow_commit`、`allow_push` | 不声明真实 KDS API 已同步或业务内容已确认 |
| `ROUTE-WAS-SYSTEM-NOISE-20260625` | `HOLD-WAS-SYSTEM-NOISE-20260625` | `hold_delete_or_ignore_decision_required` | `none_until_user_confirmation` | `allow_delete_ds_store`、`allow_gitignore_update` | 不自动删除 `.DS_Store` |
| `ROUTE-KDS-FUNDING-REPORT-20260625` | `HOLD-KDS-FUNDING-REPORT-20260625` | `hold_business_owner_required` | `none_until_user_confirmation` | `business_owner_confirmed`、`allow_review`、`allow_stage`、`allow_commit` | 不声明资金报告口径、金额或逾期判断已确认 |
| `ROUTE-SOP-WUHAN-SCENARIO-20260625` | `HOLD-SOP-WUHAN-SCENARIO-20260625` | `hold_scenario_owner_required` | `none_until_user_confirmation` | `scenario_owner_confirmed`、`allow_review`、`allow_stage`、`allow_commit`、`allow_delete_output_ds_store` | 不声明场景方案已确认、已交付或客户验收 |

## 3. 动作门禁

| 动作 | 默认状态 | 进入条件 | 复核命令 |
|---|---|---|---|
| review | `review_allowed = false` | 用户逐包确认 `allow_review=true` | 对应项目 review checklist 与 evidence validator |
| stage | `stage_allowed = false` | 用户逐包确认 `allow_stage=true`，且 Git 范围只包含该包文件 | `git status --short --untracked-files=all`、`git diff --check` |
| commit | `commit_allowed = false` | 用户确认 `allow_commit=true`，且对应包门禁复跑通过 | 对应项目测试、GPCF governance gates |
| push | `push_allowed = false` | 用户确认 `allow_push=true`，且无 ahead/behind/sensitive path | project group Git clean gate |
| delete | `delete_allowed = false` | 用户确认删除系统噪声或输出噪声 | 删除前后 Git diff、污染检查 |

## 4. 状态传导规则

| 输入状态 | 输出状态 | 传导限制 |
|---|---|---|
| `project_group_review_packages = controlled` | `authorization_routing_ready` | 只说明路由已准备，不授权任何动作 |
| `human_confirmation_request = prepared` | `authorization_routing_ready` | 只说明用户可按包确认，不等于确认已发生 |
| 任一包 `allow_review=true` | `review_allowed_for_package` | 仅限该包，不能传导到 stage/commit/push |
| 任一包 `allow_stage=true` | `stage_allowed_for_package` | 仅限该包文件，必须重新跑 Git 和证据门禁 |
| 任一包 `allow_commit=true` | `commit_allowed_for_package` | 仅限该包提交，不代表 push |
| 任一包 `allow_push=true` | `push_allowed_for_package` | 仅限该仓当前分支，必须重新检查 ahead/behind/sensitive |

## 5. 回滚与降级

- 若 review 包或 hold 包数量不等于 7，回滚本文并保持 `human_confirmation_request_prepared`。
- 若任一授权字段被默认置为 true，立即降级为 `partial/rework`。
- 若 Git clean 门禁出现 sensitive path、behind、diff check failure，授权路由不得升级。
- 若用户确认范围与当前 dirty 文件不一致，必须重新生成路由证据。
- 若用户未确认，所有动作保持 `false`。

## 6. 当前结论

```text
project_group_authorization_routing = prepared
authorization_routing_ready = true
confirmation_item_count = 7
review_package_count = 4
hold_package_count = 3
review_allowed = false
stage_allowed = false
commit_allowed = false
push_allowed = false
delete_allowed = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

当前不得声明：

- 不声明项目群可提交；
- 不声明项目群可推送；
- 不声明任何包已获得用户授权；
- 不声明真实 KDS API 已同步；
- 不声明 KDS/SOP hold 包业务内容已确认；
- 不声明 `accepted`、`integrated`、`production_ready`、`customer_accepted`。
