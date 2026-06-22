---
doc_id: GPCF-DOC-D5550386C6
title: Loop Metrics
project: WAES
related_projects: [WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_METRICS.md
source_path: 02-governance/loop/LOOP_METRICS.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Metrics

## 指标目标

Loop 指标用于衡量“推进速度是否真实、质量是否受控、证据是否可追溯、用户满意度是否可解释”。指标不得被用来掩盖未完成事实。

## 核心指标

| 指标 | 计算方式 | 目标 |
|---|---|---|
| round_throughput | 单次 L3 时间盒内完成轮次数 | <=15 轮 |
| round_duration | 每轮开始到收口耗时 | 可追溯 |
| gate_pass_rate | 通过门禁数 / 运行门禁数 | 趋势提升 |
| evidence_coverage | 有 evidence 的输出 / 总输出 | >=80% 才能考虑 evidence_ready |
| doc_control_coverage | 有 front matter 文档 / Markdown 文档 | 100% |
| kds_mirror_consistency | KDS 本地镜像一致检查 | pass |
| pollution_fail_count | 污染检查失败次数 | 0 |
| human_pause_count | 人工暂停次数 | 可解释 |
| rollback_ready_rate | 有回滚路径任务 / 有风险任务 | 100% |
| satisfaction_record_rate | 有满意度/豁免记录轮次 / 总轮次 | 趋势提升 |
| l3_unjustified_stop_count | L3 未触发停止条件却停止的次数 | 0 |
| l3_budget_progress | L3 已完成轮次和已用时间 | 每轮记录 |
| continuous_unjustified_stop_count | L3/L3.5/L4/L5 未触发停止条件却停止的次数 | 0 |
| continuous_budget_progress | 连续运行模式已完成轮次和已用时间 | 每轮记录 |

## 每轮记录字段

| 字段 | 说明 |
|---|---|
| round_id | 轮次编号 |
| mode | L0/L1/L2/L3/L3.5/L4/L5 |
| started_at | 开始时间 |
| ended_at | 结束时间 |
| files_changed | 变更文件数 |
| validators_run | 运行校验命令 |
| validators_passed | 通过校验命令 |
| evidence_files | evidence 文件 |
| risk_level | 本轮最高风险 |
| next_round | 下一轮建议 |
| continuous_session | active / stopped / not_applicable |
| continuous_mode | L3/L3.5/L4/L5/not_applicable |
| continuous_stop_type | none / hard_stop / user_stop / budget_exhausted / time_exhausted / task_queue_empty / authorization_boundary / production_safety |

## 状态解释

- 指标通过不等于业务完成。
- 本地 KDS 镜像一致不等于真实 KDS API 已同步。
- 文档完整不等于 UAT、生产、外部联调或客户满意已经完成。
- 只有用户确认和 Harness 门禁共同满足时，才可能进入 `accepted` 或 `integrated`。
