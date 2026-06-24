---
doc_id: GPCF-DOC-514115E964
title: GPCF-L4-GFIS-REPAIR-184 GFIS 运行层定位源文档门禁扩展
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-184.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-184.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-184 GFIS 运行层定位源文档门禁扩展

## Round Summary

| 字段 | 值 |
|---|---|
| control_round | GPCF-L4-GFIS-REPAIR-184 |
| runtime_round | GFIS-RUNTIME-SOP-E2E-177 |
| mode | L4 自我纠错与 GFIS 运行层修复 |
| target | 将用户确认的 GFIS 当前现代精工 OEM / 未来葛化自建工厂运行层定位纳入 GFIS 主文档防污染门禁，并回写 GPCF 总控 |
| subject | GFIS 运行层；现代精工 OEM 代加工生产期间使用，葛化自建工厂投产后继续作为同一运行时系统使用 |
| forbidden_subject | GFIS Demo；只允许作为展示、培训和前端回归 |
| gate_result | partial / repair_required |
| stop_type | authorization_boundary |

## Runtime Evidence

GFIS `GFIS-RUNTIME-SOP-E2E-177` 修订早期主文档并扩展 runtime positioning consistency validator，使以下主文档都必须包含现代精工 OEM、葛化自建工厂、GFIS、运行层口径：

- `README.md`
- `docs/03-mvp-implementation-plan.md`
- `docs/05-construction-proof-workplan.md`
- `docs/06-erpnext-local-validation-path.md`
- `docs/17-gcfis-functional-specification.md`
- `docs/20-gcfis-core-flow-closure-matrix.md`
- `docs/21-gcfis-risk-ledger-and-uat-plan.md`

关键输出：

```text
liaoning_yuanhang_runtime_positioning_consistency_guard=pass
positioning_rules=7
rules_passed=7
wrong_subjects_blocked=4
demo_subject_allowed=0
current_runtime_sites=1
future_runtime_sites=1
review_queue=0
runtime_intake=0
waes_review=0
verified=0
state=runtime_positioning_consistency_guard_passed_no_release
runtime_sop_e2e=repair_required
```

## Validation

| 检查 | 命令 | 结果 |
|---|---|---|
| GFIS positioning py_compile | `python3 -m py_compile scripts/validate_gfis_liaoning_yuanhang_runtime_positioning_consistency_guard.py` | pass |
| GFIS positioning validator | `python3 scripts/validate_gfis_liaoning_yuanhang_runtime_positioning_consistency_guard.py` | pass；见上方关键输出 |
| GFIS runtime SOP validator | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GFIS diff check | `git diff --check -- .` | pass |

## Non-Claims

- 本轮不证明派发确认、owner response、submission package、live proof、运行层业务单据、KDS/WAES 回指事实或 accepted/integrated 已成立。
- 本轮不执行 Git push、生产写入、真实外部 API 写入、数据库迁移、schema sync、权限变更、部署或 ECS/阿里云/Caddy/隧道/Docker 变更。
- GFIS Demo 继续只作为展示、培训、追溯说明和前端回归，不作为 SOP 实现主体、业务验收主体或运行层证据。

## Reality Counters

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |
