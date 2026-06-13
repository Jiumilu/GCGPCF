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

## 1.1 连续运行计数器

| 字段 | 值 |
|---|---|
| continuous session | active / stopped / not_applicable |
| continuous mode | L3 / L3.5 / L4 / L5 / not_applicable |
| declared_rounds | n/上限 |
| substantive_rounds | n/上限 |
| generated_items |  |
| batch_generated | true / false |
| substance_gate | pass / partial / fail / not_applicable |
| substance_evidence |  |
| 剩余轮次 | 上限-n |
| 已用时间 | x/时间上限 |
| 停止类型 | none / hard_stop / user_stop / budget_exhausted / time_exhausted / task_queue_empty / authorization_boundary / production_safety |
| 停止证据 |  |
| 是否符合停止规则 | yes / no / not_applicable |
| 未停止时下一轮 |  |

## 1.2 轮次真实性检查

L3、L3.5、L4、L5 必填。每轮至少满足 4/5，才可计为 `substantive_round=1`。同一脚本、同一时间窗口、同一模板批量生成多个文档时，整批默认最多计 1 个实质轮次。

| 项 | 判定 | 证据 |
|---|---|---|
| 独立输入 | yes / no |  |
| 独立判断 | yes / no |  |
| 独立输出 | yes / no |  |
| 独立验证 | yes / no |  |
| 独立反馈 | yes / no |  |

| 字段 | 值 |
|---|---|
| generated_item | true / false |
| substantive_round | true / false |
| counted_as_continuous_round | true / false |
| batch_generated | true / false |
| batch_id |  |
| similarity_with_previous | low / medium / high |
| substance_score | 0-5 |
| correction_required | yes / no |
| corrected_stop_type | none / hard_stop / user_stop / budget_exhausted / time_exhausted / task_queue_empty / authorization_boundary / production_safety |

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
| 连续运行是否必须继续 | yes / no / not_applicable |

## 12. 下一轮建议

- 下一轮 Round ID：
- 下一轮目标：
- 下一轮仍禁止：
