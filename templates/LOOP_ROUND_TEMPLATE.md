---
doc_id: GPCF-DOC-C3B9DFCB0C
title: Loop Round Template
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/LOOP_ROUND_TEMPLATE.md
source_path: templates/LOOP_ROUND_TEMPLATE.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Round Template

复制到：`docs/harness/loops/loop-round-{ROUND_ID}.md`

## 1. 基本信息

| 字段 | 值 |
|---|---|
| Round ID |  |
| 触发来源 |  |
| Loop 模式 | L0 / L1 / L2 / L3 / L3.5 / L4 / L5 |
| 本轮状态 | planned / running / blocked / completed / needs-human-review |
| 开始时间 |  |
| 完成时间 |  |

## 1.1 L3 连续推进计数器

| 字段 | 值 |
|---|---|
| L3 session | active / stopped / not_applicable |
| 已完成轮次 | n/15 |
| 剩余轮次 | 15-n |
| 已用时间 | x/120 分钟 |
| 停止类型 | none / hard_stop / user_stop / budget_exhausted / time_exhausted / task_queue_empty |
| 停止证据 |  |
| 是否符合 L3 停止规则 | yes / no / not_applicable |
| 未停止时下一轮 |  |

## 2. 本轮目标

- 最小目标：
- 不处理范围：
- 成功判定：

## 3. 输入文档

| 文档 | 路径 | 用途 |
|---|---|---|
|  |  |  |

## 4. 影响范围

| 项目/模块 | 影响 | 风险等级 |
|---|---|---|
|  |  | P0/P1/P2/P3 |

## 5. 授权边界

### 允许动作

- 

### 禁止动作

- Git push / 合并主分支，除非用户明确授权。
- 删除文件或大规模迁移，除非用户明确授权。
- 真实 API 写入、生产写入、部署、权限变更，除非当前模式为 L3.5/L4/L5 且专项政策与显式授权均允许。
- KDS TOKEN 写入或真实 KDS API 同步声明。
- 标记 `accepted` / `integrated`。

### L3.5 / L4 / L5 专项授权字段

| 字段 | 值 |
|---|---|
| 授权项目 |  |
| 授权环境 |  |
| 授权分支/API |  |
| 授权时间窗 |  |
| 最大轮次 |  |
| 允许真实动作 |  |
| 禁止动作 |  |
| 回滚策略 |  |
| 验收指标 |  |
| 监控指标 |  |

## 6. 执行步骤

| 步骤 | 动作 | 结果 |
|---|---|---|
| 1 |  |  |

## 7. 验证命令

| 命令 | 结果 | 证据 |
|---|---|---|
|  | pass/partial/fail |  |

## 8. 产出文件

| 文件 | 类型 | 说明 |
|---|---|---|
|  | 新增/修改 |  |

## 9. Evidence 清单

| evidence | 路径 | 是否完整 |
|---|---|---|
|  |  | yes/no |

## 10. 风险与回滚

| 风险 | 等级 | 处置 | 回滚/撤销路径 |
|---|---|---|---|
|  | P0/P1/P2/P3 |  |  |

## 11. 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | planned / running / blocked / completed / needs-human-review |
| 门禁结果 | pass / partial / fail |
| 是否需要人工确认 | yes / no |
| 是否可进入下一轮 | yes / no |
| L3 是否必须继续 | yes / no / not_applicable |

## 12. 下一轮建议

- 下一轮 Round ID：
- 下一轮目标：
- 下一轮仍禁止：
