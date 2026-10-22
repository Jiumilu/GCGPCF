---
doc_id: GPCF-DOC-7C0B5F0FD1
title: "门禁与证据体检（2026-10-22 23:35）"
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/health-sweep-20261022.md
source_path: docs/reports/health-sweep-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 门禁与证据体检（2026-10-22 23:35）

- 方法：对 13 项关键校验逐条实跑，记录 exit code（0=通过）
- 结论：**12/13 通过**；唯一失败为 P06 的跨仓继承声明（已知、属主待办）

| # | 校验 | exit |
|---:|---|---:|
| 1 | `loop_document_gate.py --check-only` | 0 |
| 2 | `validate_project_group_caliber_baseline.py` | 0 |
| 3 | `render_project_group_completion.py --check` | 0 |
| 4 | `validate_project_master_plan_register.py` | 0 |
| 5 | **`validate_project_plan_inheritance.py`** | **1** ← WAME/PVA 总体方案缺继承声明（跨仓，清单已出） |
| 6 | `validate_contract_matrix.py` | 0 |
| 7 | `validate_gpcf_2_feature_workspace.py` | 0 |
| 8 | `validate_project_group_live_status_snapshot_20260626.py` | 0 |
| 9 | `daily_project_status_audit.py --check` | 0 |
| 10 | `check_chinese_localization_gate.py` | 0 |
| 11 | `check_python_bytecode.py` | 0 |
| 12 | `derive_status_views.py --check` | 0 |
| 13 | `pytest tests/` | 0（62 passed） |

## 新增维护工具（本轮）

`tools/kds-sync/check_exceptions_expiry.py` —— P17 受控例外到期检查：
- 到期 → exit 1（到期自动失效，不得自动续期）；
- 30 天内到期 → `expiring_soon` 提醒；
- 缺 `approved_by` → `invalid`；
- 实测：当前 4 条例外均未到期（pass）；模拟 2027-02-01 → 4 条全部 expired（fail）。

## 边界

体检只证明"门禁与证据一致"，不证明产品可用；不构成任何状态提升。
