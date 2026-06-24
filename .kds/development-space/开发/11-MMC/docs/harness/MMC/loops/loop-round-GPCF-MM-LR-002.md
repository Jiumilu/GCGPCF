---
doc_id: GPCF-DOC-36599EF2A8
title: Loop Round GPCF-MM-LR-002：MMC 治理模板字段字典
project: MMC
related_projects: [GPC, WAES, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: MMC
kds_space: 开发
kds_path: 开发/11-MMC/docs/harness/MMC/loops/loop-round-GPCF-MM-LR-002.md
source_path: docs/harness/MMC/loops/loop-round-GPCF-MM-LR-002.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-MM-LR-002：MMC 治理模板字段字典

| 字段 | 值 |
|---|---|
| Round ID | `GPCF-MM-LR-002` |
| 模式 | L3 托管冲刺模式 |
| declared_rounds | 15/15 |
| substantive_rounds | 15/15 |
| generated_items | 50 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | budget_exhausted |
| 输入 | MMC 已有 Manifest/loop-state，但治理模板字段字典与复用验证清单仍未完成 |
| 动作 | 建立 MMC 治理模板字段字典草案和复用验证清单，不改变项目战略定位 |
| 输出 | MMC governance template field dictionary |
| 检查 | `validate_l3_second_wave_lr011_lr015.py` |
| 反馈 | L3 本次达到 15/15；后续真实项目仓、真实运行态和主结论必须另行授权 |

## 治理模板字段字典

| 字段 | 用途 | 必填 | 状态 |
|---|---|---|---|
| project_code | 项目标识 | yes | draft-controlled |
| loop_round | 微循环轮次 | yes | draft-controlled |
| gate_result | 门禁结果 | yes | draft-controlled |
| evidence_path | 证据路径 | yes | draft-controlled |
| authorization_boundary | 授权边界 | yes | draft-controlled |
| rollback_path | 回滚路径 | yes | draft-controlled |
| customer_feedback | 客户满意/反馈 | no | draft-controlled |

当前状态保持 `partial`；本轮只建立受控治理字典，不标记任何项目 accepted/integrated。
