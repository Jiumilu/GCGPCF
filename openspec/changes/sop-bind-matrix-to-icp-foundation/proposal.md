---
doc_id: GPCF-OS-ICP-SOP-COUPLING-PROPOSAL-20260713
title: ICP-SOP 基础强协同变更提案
project: GPCF
related_projects: [ICP, SOP, GPCF, WAES, KDS]
domain: openspec
status: draft
version: v0.1
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/sop-bind-matrix-to-icp-foundation/proposal.md
source_path: openspec/changes/sop-bind-matrix-to-icp-foundation/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-07-13
supersedes: []
superseded_by: []
---

## Why

ICP 已形成产业模型、资源池、场景规则和控制候选，SOP 已形成会话、规则晋升和稀疏矩阵能力，但两个项目尚未先从长期目标、总体方案、实施方案、协同需求和应用场景上建立一致基线。若直接实施矩阵绑定，容易把局部技术引用误作长期项目关系，并产生 SOP 复制、重新解释或弱化 ICP 基础的风险。

## What Changes

- 先修订 ICP、SOP 各自的长期目标、总体方案和实施方案，明确 ICP 回答“产业上必须是什么”，SOP 回答“作业上具体怎么做”。
- 建立 ICP→SOP 的权威基础单向供给关系，以及 SOP→ICP 的覆盖、漂移、缺口和演进建议反馈关系；反馈不得直接改写 ICP 基线。
- 建立板—箱、工业母粒、循环箱托、磷石膏产业链、武汉城市圈运营和宪法修订治理等首批协同应用场景。
- 在战略与场景基线完成后，建立版本化 ICP 基础、SOP 精确锁定、矩阵继承、约束不可弱化、变更影响和 fail-closed 校验。
- 将全部工作绑定到 GPCF Feature `F-012`，由 Feature journal、evidence 与 Harness handoff 保留可回放结果。
- 保持所有新增方案和规格为 `draft/candidate/partial/human_required`；不自动提升任何验收、集成或生产状态。

## Capabilities

### New Capabilities

- `icp-sop-strategic-plan-alignment`: 规定 ICP、SOP 长期目标、总体方案和实施方案的职责、继承、阶段目标与先后顺序。
- `icp-sop-collaboration-scenarios`: 规定两个项目协同需求、责任边界、输入输出、反馈回路和首批应用场景。
- `sop-icp-foundation-binding`: 规定 SOP 矩阵对版本化 ICP 模型、规则、模板和约束的精确引用、不可复制、不可弱化和失配阻断行为。

### Modified Capabilities

无。GPCF 当前主规格目录尚无对应能力，本变更仅新增 delta specs。

## Impact

- Program：GlobalCloud 项目群总体方案体系与实施方案体系。
- Projects：ICP、SOP、GPCF；WAES 负责授权和状态裁决，KDS 负责受控知识与 canonical 边界。
- Feature：`F-012 icp-sop-foundation-coupling`。
- Repositories：`GlobalCloud ICP`、`GlobalCloud SOP`、`GlobalCoud GPCF`。
- Documents：ICP/SOP 两份总体方案、两份实施方案，以及 GPCF 项目群主方案中的协同传导和依赖关系。
- Dependencies：ICP 当前候选资产需先形成可版本化 Git 基线；SOP 现有矩阵保持 `candidate/partial`；项目群文档、Git、Evidence 和人工确认门禁继续有效。
- Non-goals：不写入真实业务主账，不执行真实 KDS API 写入，不补造支付/回收规则，不自动批准 SOP 规则，不提交、不推送、不部署，不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
- Rollback：恢复修订前的四份项目主方案和项目群传导段落，撤回候选锁定与矩阵绑定实现，保留 OpenSpec、Feature journal 和 evidence 审计记录；由于不迁移业务事实，无业务数据回滚。
