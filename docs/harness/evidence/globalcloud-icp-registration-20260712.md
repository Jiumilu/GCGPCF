---
doc_id: GPCF-EVIDENCE-ICP-REGISTRATION-20260712
title: GlobalCloud ICP 项目群候选登记证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF, ICP]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-icp-registration-20260712.md
source_path: docs/harness/evidence/globalcloud-icp-registration-20260712.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

# GlobalCloud ICP 项目群候选登记证据

## 登记结果

- GC-ICP 已建立独立仓库、总体方案、实施方案和 Harness Manifest。
- 项目群总体/实施方案已将 ICP 登记为第18个项目。
- 总体方案和实施方案控制台账已登记 ICP。
- `projects/icp` 已建立状态、风险和路线图入口。
- 2026-06-28 以前的17项目基线不回写、不重算。

## 当前边界

```yaml
registration_status: candidate
overall_status: partial
confirmation_status: human_required
historical_project_count: 17
current_registered_project_count: 18
real_business_integration: false
accepted: false
integrated: false
production_ready: false
```

本登记只确认项目群治理入口已经建立，不确认真实 KDS/GPC/GFIS 数据接入、WAES 审批、部署、生产运行或客户验收。

## 验证结果

```yaml
icp_project_registration: pass
project_group_implementation_plan: pass
project_group_metadata_coverage: pass
openspec_strict_validation: pass
loop_document_gate: rework_required
loop_gate_hard_failure: false
missing_metadata: 9
missing_readme_dirs: 1
localization_debt: true
```

执行命令：

```bash
python3 tools/kds-sync/validate_icp_project_registration.py
python3 tools/kds-sync/validate_project_group_real_execution_metadata_coverage_20260626.py
python3 tools/kds-sync/validate_project_group_implementation_plan.py
openspec validate register-globalcloud-icp --strict
python3 tools/kds-sync/loop_document_gate.py --check-only
```

文档门禁仍为 `rework_required`，原因是项目群既有的 9 份元数据缺口、1 个 README 缺口和中文本地化债务；本次登记产生的新增元数据/README 缺口与项目覆盖硬失败已清零，因此 ICP 继续保持 `candidate/partial/human_required`。
