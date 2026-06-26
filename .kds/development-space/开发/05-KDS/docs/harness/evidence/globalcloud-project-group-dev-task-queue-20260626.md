---
doc_id: GPCF-DOC-DEV-TASK-QUEUE-20260626
title: GlobalCloud 项目群开发态任务队列
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群开发态任务队列

## 队列规则

- 每个项目先进入开发态，不进入验收态。
- 每仓第一任务均为 dirty 分类与本地验证，不提交、不推送。
- 若触发测试失败、敏感路径、生产写入、schema migrate、部署或业务事实冲突，立即暂停该仓。
- 本队列已按 2026-06-26 本轮 Git live gate 刷新；执行任何项目任务前仍必须复跑 17 仓 Git gate，以当次输出为准。
- P0-A dirty 分类已生成：`docs/harness/evidence/globalcloud-project-group-dev-p0-dirty-classification-20260626.md`。
- P0-B 项目级最小验证已生成：`docs/harness/evidence/globalcloud-project-group-dev-p0-project-validation-20260626.md`。

## P0 全仓任务

| 优先级 | 项目 | 当前门禁 | 开发态任务 | 验证命令 |
|---|---|---|---|---|
| P0 | GlobalCloud AAAS | dirty=3 diff=pass | 分类 3 项 dirty，确认是否为开发态候选或需隔离 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud Brain | dirty=3 diff=pass | 分类 Brain L4 retrieval 变更，复跑前端构建 | `npm run build -- --mode development` |
| P0 | WAS世界资产体系 | dirty=4 untracked=1 diff=pass | 分类 WAS 语义契约变更，确认 untracked 是否为受控 evidence | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud XiaoC | dirty=3 diff=pass | 分类 XiaoC 模型路由/编排变更，复跑本地 harness | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud WAES | dirty=3 diff=pass | 分类 WAES integration-release 变更，保持只做治理/审计候选 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud GPC | dirty=6 diff=pass | 分类 GPC 平台开发变更，补最小验证入口 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud Studio | dirty=12 untracked=4 diff=pass | 分类 release review readiness 变更，保持发布动作 blocked | `npm run harness:check` |
| P0 | GlobalCoud GPCF | P0-A classified; live dirty must be rechecked | 继续拆分治理/evidence/KDS mirror 大工作区，禁止直接提交候选 | `python3 tools/kds-sync/loop_document_gate.py` |
| P0 | GlobalCloud XWAIL | dirty=3 diff=pass | 分类 XWAIL WAES/AAAS contract precheck 变更 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud GFIS | dirty=3 diff=pass | 分类 GFIS runtime SOP 变更，真实业务凭证仍作为验收态阻点 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud MMC | dirty=3 diff=pass | 分类 MMC governance template smoke 变更，复跑 runtime tests | `MMC_TEST_MODE=true python3 -m pytest runtime/tests/ -q` |
| P0 | GlobalCloud KDS | dirty=62 untracked=35 diff=pass | 继续分类 KDS 知识导入/治理变更，diff-check 已从 fail 修复为 pass | `python3 -m pytest tests/test_api_smoke.py -q` |
| P0 | GlobalCloud XiaoG | dirty=3 diff=pass | 分类 XiaoG live API auth pack，保持 live API blocked | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud PVAOS | dirty=6 diff=pass | 分类 PVAOS release gate/review 变更，保持 release blocked | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud SOP | dirty=16 untracked=8 diff=pass | 分类 SOP scenario owner review 变更，确认不含生产指令 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud PKC | dirty=8 untracked=2 diff=pass | 分类 PKC task notification 变更，复跑前端构建 | `npm run build -- --mode development` |
| P0 | GlobalCloud XGD | dirty=3 diff=pass | 分类 XGD TICK/Brain smoke 变更，保持桌面/live 调用 blocked | `git status --short --branch && git diff --check -- .` |

## 下一轮执行顺序

1. P0-A：已完成逐仓 dirty 分类证据与 validator。
2. P0-B：已完成 GPC、Studio、MMC、KDS、PKC 项目级最小验证。
3. P0-C：对 SOP/PKC 的 generated/output/dist 类路径做提交前隔离判断。
4. P0-D：对 GPCF 大工作区拆分治理文档、KDS mirror、harness evidence 和 tooling 提交候选。
5. P0-E：复跑 17 仓 Git gate，目标保持 partial 或更好，不出现 sensitive、behind、diff-check failed。

## 状态声明

- development_queue_ready = true
- accepted = false
- integrated = false
- production_ready = false
