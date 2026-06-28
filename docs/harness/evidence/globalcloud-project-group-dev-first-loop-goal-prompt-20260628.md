---
doc_id: GPCF-DOC-DEV-FIRST-LOOP-GOAL-PROMPT-20260628
title: GlobalCloud 项目群开发优先 Loop 目标提示词 2026-06-28
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dev-first-loop-goal-prompt-20260628.md
source_path: docs/harness/evidence/globalcloud-project-group-dev-first-loop-goal-prompt-20260628.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群开发优先 Loop 目标提示词 2026-06-28

## 目标提示词

```text
你正在执行 GlobalCloud 项目群开发态 Loop。当前首要目标不是继续扩大授权、证据或治理工作，而是在保留安全边界的前提下，把项目群推进到各项目的实质开发。

默认允许：
- 本地代码开发、mock、fixture、dry-run、单元测试、最小集成测试、validator、只读 Git 检查、最小必要文档记录。
- 优先选择能产生真实开发产物的项目切片，例如接口、数据结构、运行脚本、测试、适配器、页面或任务队列。
- 证据只在开发切片完成、出现硬阻塞、或进入提交候选时生成。

默认禁止：
- stage、commit、push、delete、deploy、生产写入、schema migrate、真实外部 API 写入、真实 KDS TOKEN 写入、权限变更、accepted/integrated/production_ready/customer_accepted 状态提升。

执行策略：
1. 先移除或分类阻断开发快线的 Git hard blocker，尤其 sensitive path、behind upstream、diff-check failed、missing repo。
2. 对普通 dirty 不做重复治理，除非它阻断提交候选或含敏感路径。
3. 每轮只选一个项目的一个开发切片，输出可运行或可验证的产物。
4. 每轮只保留 run、stop、verify、recover、debug 五项控制闭环。
5. 提交前再集中执行 17 仓 Git gate、项目专项测试、文档污染、KDS token、Loop document gate。

当前第一执行项：
- 分类 GlobalCloud KDS 的 dirty/untracked 与 .env.production.example sensitive blocker。
- 若 .env.production.example 只是模板且不含真实 secret，则登记为 sensitive-template-candidate，但不自动 stage/commit/push。
- 若发现真实凭证、生产写入、schema migrate 或真实 API 写入，立即 blocked。
```

## 成功标准

| 项 | 标准 |
|---|---|
| 开发优先 | 下一轮必须进入 KDS 或 GFIS 的真实开发切片，不再继续生成重复治理 evidence |
| 治理降噪 | 每个切片最多一份主 evidence、一份 Loop round、一份 validator |
| 安全边界 | stage/commit/push/delete/deploy/runtime/schema/API/status promotion 全部保持 false |
| Git 风险 | sensitive path 必须先分类；未分类前不得提交候选 |
| 证据边界 | 只登记新增事实、硬阻塞、提交候选或授权边界 |

## 推荐执行顺序

1. `KDS-BLOCKER-001`：KDS sensitive path 与 dirty/untracked 分类。
2. `KDS-DEV-001`：KDS 本地 API / sync dry-run 最小开发切片。
3. `GFIS-DEV-001`：GFIS source-record review queue 或 runtime primary-key gate 最小开发切片。
4. `GPCF-ORCH-001`：GPCF 只做编排与收口，不为每个只读检查生成独立 evidence。

## 当前执行进展

| 项 | 当前状态 | 边界 |
|---|---|---|
| `KDS-BLOCKER-001` | `classified_sensitive_template_candidate` | 允许继续本地开发，但仍阻断 stage/commit/push/status promotion |
| `KDS-DEV-001` | `pass_check_only` | 只证明本地 API / sync dry-run 边界；未启动服务、未运行 sync、未调用 API、未写 KDS/GBrain |
| `GFIS-DEV-001` | `pass_readiness` | 聚合 REAL-003 至 REAL-006 门禁；只证明真实 source-of-record 到达后的门禁链路可复核，真实计数仍为 0 |

## 状态声明

- dev_first_loop_goal_prompt = active
- default_local_dev_allowed = true
- redundant_governance_reduction = true
- evidence_generation_policy = minimal_required
- first_execution_item = KDS-BLOCKER-001
- kds_dev_001_local_api_sync_dry_run = pass_check_only
- gfis_dev_001_source_record_runtime_readiness_chain = pass_readiness
- stage_allowed = false
- commit_allowed = false
- push_allowed = false
- delete_allowed = false
- deploy_allowed = false
- runtime_write_allowed = false
- schema_migrate_allowed = false
- real_api_write_allowed = false
- status_promotion_allowed = false
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
