---
doc_id: GPCF-DOC-72F18A4F4A
title: 全量体检脚本（门禁之外的校验一次跑完，2026-10-24）
project: KDS
related_projects: [GFIS, WAME, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/full-sweep-script-20261024.md
source_path: docs/reports/full-sweep-script-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 全量体检脚本（门禁之外的校验一次跑完，2026-10-24）

- 脚本：`scripts/gpcf_full_sweep.py`
- 动因：第 36 轮发现 `validate_project_plan_inheritance` 回归**门禁未拦截**（第 37 轮已把该项并入 gate）；
  但仍有若干校验只在人工体检执行，并发编辑可能再次悄悄回退
- 定位：**非阻断工具**（不入门禁、不改 pre-commit），供每轮收口与交付前自检使用

## 1. 覆盖的 14 项

| # | 检查 | 说明 |
|---:|---|---|
| 1 | `loop_document_gate --check-only` | 主门禁（已含 3 项回归校验） |
| 2 | `validate_project_group_caliber_baseline` | 分母 29 口径（门禁因 GFIS guard 元检查未纳入） |
| 3 | `render_project_group_completion --check` | 完成度渲染一致性 |
| 4 | `validate_project_master_plan_register` | 主方案登记台账 |
| 5 | `validate_project_plan_inheritance` | 跨仓方案继承声明 |
| 6 | `validate_contract_matrix` | 跨项目契约矩阵 |
| 7 | `validate_gpcf_2_feature_workspace` | Feature 工作区规范 |
| 8 | `validate_project_group_live_status_snapshot` | 快照结构 |
| 9 | `daily_project_status_audit --check` | 日状态审计 |
| 10 | `check_chinese_localization_gate` | 中文化门禁 |
| 11 | `check_python_bytecode` | 字节码残留 |
| 12 | `validate_loop_v11_slimming_delivery_recovery` | LOOP v1.1 交付恢复（含 KDS diff-check） |
| 13 | `derive_status_views --check` | 队列与 feature.yaml 派生一致性 |
| 14 | `pytest tests/ -q` | 回归测试 |

## 2. 实测（2026-10-24）

```
汇总：14/14 通过，用时 36.0s
```

## 3. 用法

```bash
python3 scripts/gpcf_full_sweep.py          # 人读表格，任一失败 exit 1
python3 scripts/gpcf_full_sweep.py --json   # 机器可读（供报告/CI 引用）
```

## 4. 边界

- 不改变门禁行为，不阻断提交；
- 只证明"门禁与证据一致"，不证明产品可用；不构成任何状态提升。
