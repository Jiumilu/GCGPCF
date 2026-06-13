---
doc_id: GPCF-DOC-5E646AC9A6
title: Loop L4 Autonomous Operations Policy
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_L4_AUTONOMOUS_OPERATIONS.md
source_path: 02-governance/loop/LOOP_L4_AUTONOMOUS_OPERATIONS.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop L4 Autonomous Operations Policy

## 定位

L4 = Full Autonomous Operations Mode / 全自动运营模式。

L4 面向项目群开发运营，不直接承担生产最终自治。它可以持续推进开发、治理、测试、文档、提交、非主分支推送、KDS dry-run 或白名单同步。

## 状态

| 字段 | 值 |
|---|---|
| 模式状态 | executable / not activated |
| 默认是否启用 | 否 |
| 是否可由 L3 或 L3.5 自动升级 | 否 |
| 运行上限 | 初始最多 30 轮或 4 小时，以先到者为准 |

## 启动口令

最小口令：

```text
启动 Loop L4 全自动运营模式
```

建议完整口令：

```text
启动 Loop L4 全自动运营模式。
授权项目：GPCF / GFIS / 全项目群
授权时间窗：4 小时
最大轮次：30 轮
允许动作：文档、代码、小范围重构、测试、dry-run、本地 commit、非主分支 push
禁止动作：生产部署、真实生产写入、修改权限、删除关键文件、合并 main
```

## 可自动执行范围

- 自动读取 Loop 控制板。
- 自动读取任务队列。
- 自动选择下一轮目标。
- 自动拆分任务。
- 自动修改文档。
- 自动修改代码。
- 自动补测试。
- 自动运行 lint/test/build/dry-run。
- 自动生成 evidence。
- 自动更新项目状态。
- 自动更新 Loop 控制板。
- 自动更新文档台账。
- 自动本地 commit。
- 自动推送到指定非主分支。
- 自动生成日报、周报、风险报告。
- 自动生成下一轮计划。
- 自动执行 KDS dry-run。
- 在白名单下执行 KDS 开发空间同步。

## 禁止动作

- 直接修改 `main`。
- 直接合并 PR。
- 生产部署。
- 真实生产 API 写入。
- 修改密钥、Token、权限。
- 删除关键文档、源码、证据。
- 清空历史 evidence。
- 改变项目战略定位。
- 改变验收结论。
- 标记 accepted / integrated。
- 绕过失败门禁继续执行。
- 在授权范围外继续运行。

## 启动前门禁

| 门禁 | 要求 |
|---|---|
| 控制板 | 存在 `LOOP_CONTROL_BOARD.md` |
| 授权边界 | 存在 `LOOP_AUTONOMY_POLICY.md` |
| 轮次模板 | 存在 `LOOP_ROUND_TEMPLATE.md` |
| evidence | 存在 evidence 目录 |
| 任务队列 | 存在且可解释 |
| Git | 状态可解释，当前不在不可控 dirty main 状态 |
| 验证入口 | 测试或 dry-run 入口存在 |
| secrets | 扫描机制存在 |
| 回滚 | 回滚策略存在 |
| 暂停机制 | 自动暂停机制存在 |
| 授权 | 当前用户授权口令完整 |

## 自动暂停条件

- 出现 P0 风险。
- Git 冲突。
- 测试或 build 失败且无法局部修复。
- secrets 扫描异常。
- 触及生产配置。
- 触及权限或 Token。
- 触及真实生产 API 写入。
- 需要删除或迁移关键文件。
- 任务目标不清。
- 连续 2 轮无实质进展。
- 授权时间窗到期。
- 用户发出暂停、停止或降级指令。

## 输出要求

每轮必须产出：

- 本轮目标。
- 输入文档。
- 实际变更。
- 验证结果。
- 风险判断。
- evidence 路径。
- Git 状态。
- 下一轮建议。
