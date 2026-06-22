---
doc_id: GPCF-DOC-E7DFFC15E5
title: GC-Knowledge Fabric P0 Repair Path Workpack Dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/repair-path-workpack-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/repair-path-workpack-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Repair Path Workpack Dry-run v0.1

## 定位

本文档定义 P0-D25 repair path workpack 的 dry-run 口径。它从 D24 Harness decision template 中抽取 `repair_required` 和 `scope_violation_found` 两类需要继续流转的结论，生成 KWE/LOOP 候选跟进工单。

本 workpack 不创建真实 KWE 工单，不创建真实 LOOP 跟进，不写 KDS，不写 Harness evidence。

## 覆盖与排除

| 类型 | 决策结论 | 处理 |
|---|---|---|
| 覆盖 | `repair_required` | 生成 evidence repair 候选工单 |
| 覆盖 | `scope_violation_found` | 生成 governance follow-up 候选工单 |
| 排除 | `approved_for_formal_harness_evidence` | 不生成补证工单 |
| 排除 | `rejected` | 不生成补证工单，需要另行生成拒绝归档路径 |

## 候选工单

| ID | 来源结论 | 引擎 | 优先级 | 状态 |
|---|---|---|---|---|
| `GCKF-P0-REPAIR-WI-001` | `repair_required` | KWE | P1 | candidate |
| `GCKF-P0-REPAIR-WI-002` | `scope_violation_found` | LOOP | P0 | candidate |

## 禁止动作

D25 禁止：

- 创建真实 KWE work item。
- 创建真实 LOOP follow-up。
- 写正式 Harness evidence。
- 写 KDS。
- 写业务系统。
- 启动 server。
- 连接数据库。
- 调用外部 API。
- 提升 lifecycle 为 `accepted` 或 `integrated`。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_repair_path_workpack_dry_run.py
```

预期信号：

```text
gckf_p0_repair_path_workpack_dry_run=pass status=candidate source_template_status=candidate covered_decisions=2 excluded_decisions=2 candidate_work_items=2 required_sources=4 kwe_loop_follow_up=covered not_final_acceptance=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 creates_kwe_work_item=0 creates_loop_follow_up=0 no_write=covered
```

## 下一步

D26 建议建立 rejection archive path dry-run，把 `rejected` 结论转为拒绝归档、复审前置条件和新候选包重建规则。
