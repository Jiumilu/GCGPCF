---
doc_id: GPCF-DOC-7FB1181082
title: Loop L5 Full Production Autonomy Policy
project: WAES
related_projects: [GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_L5_FULL_PRODUCTION_AUTONOMY.md
source_path: 02-governance/loop/LOOP_L5_FULL_PRODUCTION_AUTONOMY.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop L5 Full Production Autonomy Policy

## 定位

L5 = Full Production Autonomy / 完全生产自治模式。

L5 是最高等级生产自治能力。它可以在事先授权的生产治理宪法内，自主完成生产问题发现、定位、修复、测试、发布、部署、监控、回滚、复盘和知识库更新。

L5 的“完全”不是无边界自治，而是在强授权范围内完整承担生产闭环。

## 状态

| 字段 | 值 |
|---|---|
| 模式状态 | executable / not activated |
| 默认是否启用 | 否 |
| 是否可由 L4 自动升级 | 否 |
| 运行上限 | 初始最多 10 轮或 2 小时，以先到者为准 |
| 默认继续 | 强授权范围内生产事件、监控窗口、回滚核查或复盘未闭合且未触发生产安全停止时，必须继续下一轮 |

## 强授权口令

L5 不得由“继续”“下一步”“启动全自动”触发。必须使用强授权口令：

```text
启动 Loop L5 完全生产自治模式。
授权项目：……
授权环境：……
授权分支：……
授权时间窗：……
授权任务范围：……
允许生产动作：……
禁止动作：……
回滚策略：……
验收指标：……
监控指标：……
```

缺少任一关键字段，L5 不得启动。

## 当前项目强授权口令示例

```text
启动 Loop L5 完全生产自治模式。

授权项目：GPC / GlobalCoud GPCF
授权环境：production
授权分支：release/l5-gpc-production-autonomy
授权时间窗：2026-06-13 20:00 至 2026-06-13 22:00，Asia/Shanghai
最大轮次：10 轮
授权任务范围：
- 仅处理已登记在 LOOP_CONTROL_BOARD 中的 P0/P1 生产问题
- 仅允许修复 GPCF 相关生产运行问题
- 仅允许修改与本次事件直接相关的代码、配置、文档、测试和 evidence
允许生产动作：
- 读取生产日志、监控、告警
- 创建生产事件记录
- 修改代码
- 修改白名单内生产配置
- 运行全量测试、构建、安全检查、secrets 扫描
- 创建 release candidate
- 推送发布分支
- 创建或更新 PR
- 部署预发布环境
- 在全部门禁通过后部署 production
- 监控生产指标
- 如指标异常，按回滚策略自动回滚
禁止动作：
- 修改 main 分支
- 扩大权限
- 修改密钥、Token、访问控制
- 删除源码、文档、历史 evidence 或生产数据
- 关闭监控
- 绕过测试、构建、安全检查或审计
- 超出 GPCF 项目边界
回滚策略：
- 优先回滚到 L5 启动前最近一个健康 production 版本
- 回滚后必须生成 incident report 和 postmortem
验收指标：
- 全量测试通过
- build 通过
- secrets 扫描通过
- 安全检查通过
- production 关键接口健康检查通过
- 生产错误率未高于 L5 启动前基线
- 无新增 P0/P1 告警
监控指标：
- API 成功率
- API p95 延迟
- 5xx 错误率
- 任务执行成功率
- KDS 同步错误率
- 资源使用率
```

## 可自动执行范围

在明确授权范围内，L5 可执行：

- 读取生产监控、日志、告警。
- 识别生产问题。
- 判断影响范围。
- 建立生产事件记录。
- 创建修复任务。
- 修改代码。
- 修改白名单内配置。
- 运行全量测试。
- 运行构建。
- 运行 secrets 扫描。
- 运行安全检查。
- 生成 release candidate。
- 推送发布分支。
- 创建或更新 PR。
- 合并授权范围内 PR。
- 部署预发布。
- 部署生产。
- 监控生产指标。
- 自动回滚。
- 生成 incident report。
- 生成 postmortem。
- 更新 KDS、文档、Loop 控制板。

## 禁止动作

除非授权文件明确允许，否则禁止：

- 扩大自身权限。
- 修改最高治理规则。
- 关闭监控。
- 删除审计证据。
- 删除关键数据。
- 删除历史文档。
- 删除源码历史。
- 修改密钥和 Token。
- 创建新的高权限凭证。
- 绕过测试发布。
- 绕过审计发布。
- 隐藏失败。
- 篡改 evidence。
- 越过授权项目。
- 越过授权环境。
- 越过授权时间窗。
- 在未定义回滚策略时部署。
- 在未定义验收指标时发布。

## 启动前门禁

| 门禁 | 要求 |
|---|---|
| L4 | 已可执行 |
| Git | 分支策略和发布分支策略已固化 |
| CI/验证 | CI 或本地等价验证可运行 |
| 测试 | 全量测试入口存在 |
| 构建 | build 入口存在 |
| secrets | secrets 扫描入口存在 |
| 安全 | 安全检查入口存在 |
| 配置 | 生产配置 diff 可审计 |
| 回滚 | 回滚策略存在 |
| 监控 | 监控指标存在 |
| 告警 | 告警渠道存在 |
| 事件 | incident 模板存在 |
| 复盘 | postmortem 模板存在 |

## 真实性计数门禁

L5 的 10 轮预算只能按 `substantive_rounds` 计数。生产日志条数、告警数量、批量修复文件数量、部署步骤数量、监控截图数量或模板化 incident/postmortem 文档，不能自动计为多个实质轮次。

每个 L5 实质轮次必须至少满足 4/5：独立生产事件输入、独立影响/安全判断、独立修复/部署/回滚输出、独立监控或验证证据、独立复盘/下一步反馈。

若 `declared_rounds` 达到 10/10 但 `substantive_rounds` 未达到 10/10，不得使用 `budget_exhausted` 收口，必须更正为 `authorization_boundary` 或 `production_safety`，并运行：

```bash
python3 tools/kds-sync/validate_continuous_round_substance.py
```
| KDS | 同步策略明确 |
| 授权 | 授权记录已写入 evidence |

## 自动暂停条件

- P0/P1 风险。
- 测试失败。
- 构建失败。
- secrets 扫描失败。
- 安全检查失败。
- 生产配置 diff 异常。
- 监控指标异常扩大。
- 回滚失败。
- 授权范围不清。
- 涉及数据破坏风险。
- 涉及权限升级。
- 任务需要业务判断。
- 发现文档与事实冲突。
- 用户发出暂停、停止或降级指令。

## 连续推进与停止规则

L5 active 后，完成一次修复、一次部署、一次回滚或一次阶段性汇报都不是停止条件。每轮必须重新验证生产监控、回滚能力和授权边界。只有满足以下任一条件时才能停止：

1. 已连续完成 10 轮。
2. 已运行满 2 小时。
3. 触发 P0/P1 风险、测试失败、构建失败、secrets 扫描失败、安全检查失败、生产配置 diff 异常、监控指标异常扩大或回滚失败。
4. 授权范围不清、涉及数据破坏风险、涉及权限升级或任务需要业务判断。
5. 用户明确暂停、停止或降级。
6. 生产事件已闭合，监控窗口完成，回滚核查完成，incident report、postmortem 和 KDS/文档更新完成。

## 最高原则

```text
生产连续性 > 数据安全 > 客户影响最小化 > 可回滚 > 可审计 > 自动化速度
```
