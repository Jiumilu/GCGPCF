---
doc_id: GPCF-DOC-8E2A7EAEF0
title: Loop Round GPCF-HEADROOM-ADMISSION-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-ADMISSION-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-ADMISSION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-ADMISSION-001

## 输入

- 用户目标：全面在项目群实施 Headroom 接入与应用，纳入 Loop 工程体系，并建立成本评估模型。
- 上轮评估结论：Headroom 可作为条件准入的 AI 上下文压缩基础设施候选，不应直接作为业务项目或生产代理纳入。
- 当前 GPCF 边界：dirty 工作区很重；本轮只做受控文档、evidence 和 validator，不改其他项目仓。

## 动作

1. 读取 GPCF Loop 控制板、自治策略、文档治理技能和成本控制文档。
2. 建立 Headroom 项目群接入应用矩阵。
3. 建立可配置 token 成本评估模型。
4. 定义 Loop 工程对象：`HeadroomScenario`、`HeadroomCostMeasurement`、`HeadroomEquivalenceGate`、`HeadroomSecurityGate`、`HeadroomCostDecision`。
5. 新增 Headroom admission evidence、本地 validator、成本计算器和脱敏 measurement template。

## 输出

- `02-governance/GlobalCloud项目群Headroom接入应用与成本评估模型.md`
- `docs/harness/evidence/headroom-project-group-admission-20260621.json`
- `docs/harness/evidence/headroom-project-group-admission-20260621.md`
- `docs/harness/loops/loop-round-GPCF-HEADROOM-ADMISSION-001.md`
- `tools/kds-sync/validate_headroom_project_group_admission.py`
- `tools/kds-sync/calculate_headroom_cost_model.py`
- `fixtures/headroom/headroom-cost-measurement-template.json`

## 检查

预期校验：

```bash
python3 tools/kds-sync/calculate_headroom_cost_model.py fixtures/headroom/headroom-cost-measurement-template.json
python3 tools/kds-sync/validate_headroom_project_group_admission.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

本轮只完成 L1 治理准入、L2 dry-run 准备和成本模型定义。下一轮应选择非敏样本执行 L2 压缩 dry-run，产出 `HeadroomCostMeasurement` fixture，再判断是否申请 L3.5 或 L4 授权。

本轮不生产写入、不真实外部 API 写入、不真实 KDS 写入、不启用跨项目 memory、不自动写项目规则文件、不部署、不提交、不推送、不升级 accepted、integrated 或 production_ready。
