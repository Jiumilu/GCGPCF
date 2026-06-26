---
doc_id: GPCF-DOC-XIAOC-MODEL-ROUTING-DRYRUN-ENV-BLOCKED-20260625
title: XiaoC 模型路由 Dry-run 环境阻塞证据 2026-06-25
project: XiaoC
related_projects: [WAES, XiaoC]
domain: docs
status: controlled
version: v1.0
owner: XiaoC
kds_space: 开发
kds_path: 开发/08-XiaoC/docs/harness/XiaoC/evidence/xiaoc-model-routing-dryrun-environment-blocked-20260625.md
source_path: docs/harness/XiaoC/evidence/xiaoc-model-routing-dryrun-environment-blocked-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# XiaoC 模型路由 Dry-run 环境阻塞证据 2026-06-25

## 1. 定位

本文补齐 `XIAOC-MODEL-ROUTING-DRYRUN-001` 的真实执行结果：本轮尝试执行任务包定义的 `pnpm run lint`、`pnpm run typecheck:core`、`pnpm run test:fast`、`pnpm run check:locale`，但均被项目 Node engine 门禁阻断。

本文不把失败命令写成通过，不修改 XiaoC 源码、不安装 Node、不切换环境、不触发 Wrangler、Docker、真实模型调用、生产部署、accepted、integrated 或客户验收。

## 2. 控制结论

```text
xiaoc_model_routing_dryrun = environment_blocked
task_id = XIAOC-MODEL-ROUTING-DRYRUN-001
source_project = GlobalCloud XiaoC
source_repo = /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC
target_status_candidate = baseline_controlled / environment_blocked
required_node = ^22.0.0
actual_node = v26.0.0
pnpm_version = 10.6.1
commands_attempted = 4
commands_passed = 0
commands_failed = 4
environment_blocker = ERR_PNPM_UNSUPPORTED_ENGINE
real_model_call_executed = false
wrangler_executed = false
docker_executed = false
production_ready = false
accepted = false
integrated = false
customer_accepted = false
```

## 3. 真实命令结果

| 命令 | 结果 | 原始摘要 |
|---|---|---|
| `pnpm run lint` | `blocked` | `ERR_PNPM_UNSUPPORTED_ENGINE`，Expected Node `^22.0.0`，Got `v26.0.0` |
| `pnpm run typecheck:core` | `blocked` | `ERR_PNPM_UNSUPPORTED_ENGINE`，Expected Node `^22.0.0`，Got `v26.0.0` |
| `pnpm run test:fast` | `blocked` | `ERR_PNPM_UNSUPPORTED_ENGINE`，Expected Node `^22.0.0`，Got `v26.0.0` |
| `pnpm run check:locale` | `blocked` | `ERR_PNPM_UNSUPPORTED_ENGINE`，Expected Node `^22.0.0`，Got `v26.0.0` |

同时出现 pnpm warning：`The "pnpm" field in package.json is no longer read by pnpm`。该 warning 不是本轮主要阻塞，主要阻塞是 Node engine 不匹配。

## 4. 证据边界

| 类型 | 当前结论 |
|---|---|
| 真实进度 | `baseline_controlled / environment_blocked` |
| 真实研发 | `not_verified_this_round`，命令未进入业务校验阶段 |
| 真实运行 | `not_verified_this_round` |
| 真实集成 | `not_verified_this_round` |
| 真实交付 | `not_collected` |
| 客户验收 | `not_collected` |

## 5. 回滚与恢复

| 场景 | 处理 |
|---|---|
| 当前环境继续使用 Node v26 | 保持 `environment_blocked`，不得声明 dry-run 通过 |
| 切换到 Node 22 | 复跑 `pnpm run lint`、`pnpm run typecheck:core`、`pnpm run test:fast`、`pnpm run check:locale` |
| 复跑后命令通过 | 另建 `xiaoc-model-routing-dryrun-*.md` 成功证据 |
| 复跑后命令失败 | 建立 `repair_required` 证据，记录具体失败命令 |

## 6. 禁止声明

- 不声明 XiaoC dry-run 通过；
- 不声明真实模型调用完成；
- 不声明 Wrangler 或 Docker 运行完成；
- 不声明真实部署、生产模型路由可用、客户交付或客户验收；
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

## 7. 下一步

```text
next_task = XIAOC-NODE22-DRYRUN-RETRY-001
required_environment = Node ^22.0.0
required_commands = pnpm run lint; pnpm run typecheck:core; pnpm run test:fast; pnpm run check:locale
authorization_required = false_for_local_node22_dryrun / true_for_real_model_or_wrangler_or_docker_or_deploy
status_boundary = environment_blocked_until_node22
```
