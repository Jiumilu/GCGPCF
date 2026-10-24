---
doc_id: GPCF-DOC-63A3055B85
title: 门禁检查扩充：把曾人工发现的回归纳入自动拦截（2026-10-24）
project: GPCF
related_projects: [GFIS, GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/gate-check-expansion-20261024.md
source_path: docs/reports/gate-check-expansion-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 门禁检查扩充：把曾人工发现的回归纳入自动拦截（2026-10-24）

- 授权：`decide_template(authorization_qa)` → **probability_yes 0.8573 / verdict yes**
- 动因：本轮前 `validate_project_plan_inheritance` 回归（GPCF 自身总体方案 token 被并发编辑回退）**门禁未拦截**，靠人工全量体检才发现

## 1. 新增到 `loop_document_gate` 的 3 项校验

| 检查名 | 校验器 | 耗时 |
|---|---|---|---:|
| `project_group_plan_inheritance` | `validate_project_plan_inheritance.py` | ~0.03s |
| `project_group_contract_matrix` | `validate_contract_matrix.py` | ~0.06s |
| `project_group_master_plan_register` | `validate_project_master_plan_register.py` | ~0.04s |

门禁总耗时维持约 **14s**（新增开销 <0.2s）。

## 2. 反向验证（证明真的能拦）

临时把 GPCF 总体方案里的控制 token 改成 `XXX回归测试`：
```json
{"gate":"rework_required","gate_reasons":["hard_failure:project_group_plan_inheritance"]}
```
恢复后：`{"gate":"pass"}` —— 该回归类型现已自动阻断。

## 3. 刻意**未**纳入的一项

`validate_project_group_caliber_baseline.py`（分母 29 口径）：门禁自身有"GFIS real-fact guard"元检查，
要求每个 gate 校验器引用 GFIS 真实事实守卫；该口径校验器与 GFIS 事实无关，
**不做语义造假**去凑 guard 文本，故不纳入门禁，改为在每轮人工全量体检中执行。

## 4. 回滚

```bash
cd "GlobalCloud GPCF"
git checkout -- tools/kds-sync/loop_document_gate.py
```

## 5. 边界

门禁变严后，任何仓的方案继承/契约矩阵/主方案登记台账漂移都会阻断提交（这正是目的）；不构成状态提升。
