---
doc_id: GPCF-DOC-CE28DA4C36
title: GlobalCloud Loop Orchestrator Stage Gates
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/stage-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/stage-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Orchestrator Stage Gates

## 状态升级条件

| 目标状态 | 必备条件 |
|---|---|
| `loop_ready` | Manifest、`docs/harness/loop-state.md`、loops/evidence 目录、无未登记文档债务，依赖和风险已初判 |
| `loop_running` | 至少 1 轮 `loop-round-{ID}.md`，且五段式记录完整 |
| `evidence_ready` | evidence 完整率 >=80%，不得缺 `loop-round-{ID}.md`，且有 Git status/diff、质量、可用性 evidence |
| `audit_ready` | 完成 3 轮微循环或日终/blocked 触发中循环审计，Git dirty 状态已登记，风险和依赖已登记 |
| `harness_review` | 评衡/证验输出审计结果，Harness 可读取 evidence，相关变更已 commit 或登记不提交原因，客户满意度已收集或登记豁免 |
| `accepted` | Harness 建议通过，相关 commit 已 push，工作区 clean，可用性验证通过，客户满意度达标，并经用户人工确认 |
| `integrated` | 小即完成跨项目收口，跨项目版本清单和依赖清单已生成，自我进化复盘完成，并经用户确认 |

## 默认停止条件

以下停止条件适用于普通 Loop。若当前处于 L3 托管冲刺模式，阶段性汇报、完成单轮、完成两轮、完成一个小任务或生成下一轮建议不得作为停止条件；L3 只能因 15 轮预算耗尽、2 小时时间耗尽、P0/P1 硬停止、用户明确暂停/停止，或任务队列为空而停止。

- KDS TOKEN 缺失或权限不符合。
- 需要用户做业务方向判断。
- 需要删除、迁移大量文件。
- 准备提交、推送或发布但用户未授权。
- Git push rejected、远端冲突、敏感文件未处理。
- evidence 缺失导致状态不能升级。
- 测试失败且无法自动修复。
- 可用性验证失败或客户不满意。
- 无回滚方案的高风险变更。
- 依赖阻塞未登记或影响下游项目。
- 出现 GFIS/GPC/WAES/KDS 等跨项目主线冲突。
- 准备进入 `accepted` 或 `integrated`。

## 首轮推荐顺序

1. GPCF 自身：补齐总控仓 `loop-state` 和首轮治理 evidence。
2. GFIS：以现代精工培训资料启动 `GPCF-GF-LR-001`。
3. MMC、KDS、Brain、PKC：进入试点 `loop_ready`。
4. XiaoC：从 `partial` 补齐 loop-state、测试和部署证据。
5. GPC、PVAOS、WAES、XGD、XiaoG：补齐 Manifest 和首轮输入。

## Git 门禁

详细规则见 `git-version-gates.md`。状态升级前必须至少执行：

```bash
python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_git_gate.py .
```

## 完整运行门禁

状态升级前必须执行完整运行门禁：

```bash
python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_operational_gates.py .
```
