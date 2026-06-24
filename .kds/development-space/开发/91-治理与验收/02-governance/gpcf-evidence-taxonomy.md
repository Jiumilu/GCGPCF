---
doc_id: GPCF-DOC-F113DF5034
title: GPCF Loop Engineering 证据分类体系
project: WAES
related_projects: [GPC, WAES, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/gpcf-evidence-taxonomy.md
source_path: 02-governance/gpcf-evidence-taxonomy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF Loop Engineering 证据分类体系

日期：2026-06-12
状态：v1.0
依赖：gpcf-loop-engineering-spec-v1.md

## 1. 证据类型总表

| 类型 | 文件命名 | 用途 | 必/可选 | 最低字段 |
|---|---|---|---|---|
| loop record | `loop-round-{ID}.md` | 本轮执行记录 | 必 | 输入/动作/输出/检查/反馈 |
| diff evidence | `diff-{ID}.patch` | 文件变更证据 | 必 | 变更文件路径、变更摘要 |
| command log | `command-log-{ID}.txt` | 命令执行证据 | 必 | 命令原文、执行时间、输出摘要 |
| test result | `test-result-{ID}.md` | 测试结果 | 可选 | 测试项、结果、覆盖率 |
| audit report | `status-audit-YYYY-MM-DD.md` | 中循环审计 | 必（中循环时） | 审计项、判定、评分、证据引用 |
| screenshot | `screenshot-{scene}-{N}.png` | 页面/流程证据 | 可选 | 场景描述、时间戳 |
| metric json | `metrics-{ID}.json` | 自动化指标 | 可选 | 指标名、值、采集时间 |

## 2. 各类型详细规范

### 2.1 loop record（必）

- 文件：`loop-round-{ID}.md`
- 位置：项目仓 `docs/harness/loops/` 和 GPCF `08-evidence-samples/{项目}/`
- 模板：`templates/loop-round-template.md`
- 最低字段：输入来源、本轮目标、入口条件、动作（类型+文件+说明）、输出（产物+路径+说明）、检查（检查项+结果+证据）、反馈（阻塞项+风险项+下一轮输入）

### 2.2 diff evidence（必）

- 文件：`diff-{ID}.patch`
- 位置：项目仓 `docs/harness/evidence/`
- 最低字段：变更文件路径（至少 1 条）、变更摘要（一句话）
- 生成方式：`git diff HEAD~1 > diff-{ID}.patch`

### 2.3 command log（必）

- 文件：`command-log-{ID}.txt`
- 位置：项目仓 `docs/harness/evidence/`
- 最低字段：执行的命令原文、执行时间（ISO 8601）、关键输出摘要（至少 1 行）
- 生成方式：手动复制或脚本捕获

### 2.4 test result（可选）

- 文件：`test-result-{ID}.md`
- 位置：项目仓 `docs/harness/evidence/`
- 最低字段：测试项名称、结果（pass/fail）、覆盖率（如适用）

### 2.5 audit report（中循环必）

- 文件：`status-audit-YYYY-MM-DD.md`
- 位置：项目仓 `docs/harness/` 和 GPCF `08-evidence-samples/{项目}/`
- 模板：`templates/loop-audit-template.md`
- 最低字段：审计日期、审计范围、审计项+判定、评分、证据引用、Harness 状态建议

### 2.6 screenshot（可选）

- 文件：`screenshot-{scene}-{N}.png`
- 位置：项目仓 `docs/harness/evidence/screenshots/`
- 最低字段：场景描述、时间戳

### 2.7 metric json（可选）

- 文件：`metrics-{ID}.json`
- 位置：项目仓 `docs/harness/evidence/`
- 最低字段：
```json
{
  "round_id": "GPCF-XX-LR-001",
  "timestamp": "2026-06-12T10:00:00+08:00",
  "metrics": {
    "evidence_completeness": 0.85,
    "gate_pass_rate": 0.80,
    "cycle_time_minutes": 25
  }
}
```

## 3. 证据存放约定

### 项目仓

```
docs/harness/evidence/
  README.md
  evidence-index.md
  diff-{ID}.patch
  command-log-{ID}.txt
  test-result-{ID}.md
  metrics-{ID}.json
  screenshots/
    screenshot-{scene}-{N}.png
```

### GPCF 总仓（汇聚）

```
08-evidence-samples/
  README.md
  evidence-index.md
  {项目名}/
    loop-round-{ID}.md
    status-audit-YYYY-MM-DD.md
    evidence/
      （项目仓 evidence 的副本或链接）
```

## 4. 证据完整率计算

```
证据完整率 = 已收集的必备证据类型数 / 本轮应收集的必备证据类型数

其中必备 = loop record + diff evidence + command log
中循环时额外必备 = audit report
```

## 5. 版本记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.0 | 初始定义：7 种 evidence 类型、命名规范、最低字段、存放约定、完整率计算 |

## 6. 每轮 evidence 最小集合与权重模型

### 6.1 权重分配

| evidence 项 | 是否必需 | 权重 |
|---|---|---|
| `loop-round-{ID}.md` | 必需 | 30% |
| 文件变更清单或 diff | 必需 | 20% |
| command log / 操作记录 | 必需 | 15% |
| test result / 检查结果 | 必需 | 20% |
| metrics JSON | 建议 | 10% |
| screenshot / 页面证据 | 按需 | 5% |

### 6.2 计算规则

```
evidence 完整率 = Σ(已收集项的权重) / Σ(本轮应收集项的权重)
```

### 6.3 不可降级规则

缺失 `loop-round-{ID}.md` 时，不论其他 evidence 权重之和是否 ≥80%，**不得进入 evidence_ready 状态**。loop-round 是循环的骨架记录，缺失它意味着本轮循环不可追溯。

## 7. 版本记录（续）

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.1 | 增加 evidence 权重模型、不可降级规则 |
