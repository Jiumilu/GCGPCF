---
doc_id: GPCF-DOC-FC299296D9
title: 设计：场景流的版本化承接
project: KDS
related_projects: [WAME, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/was-scenario-flow-extension/design.md
source_path: openspec/changes/was-scenario-flow-extension/design.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# 设计：场景流的版本化承接

## 1. 背景与约束

- 定义单源：老卢 2026-10-16 裁定文本；GCWORLD V1.0.1 九流表。
- U16：理论层「维度／流为开放集合」；契约层 8+8 基线，扩展走版本化。
- WAS 仓《AGENTS.md》：核心术语变更须显式兼容性决定；三层资产/八维/八流/生命周期不得无决定变更；跨项目变更协议六项声明。

## 2. 承接方式（两级）

1. **登记（本变更）**：以「扩展登记件」形式登记场景流为受控兼容扩展（candidate）。登记 ≠ 契约变更；它是版本化纳入的前置准入。
2. **纳入（后续流程）**：WAS 治理复核通过后，按版本发布把场景流并入主方案流清单与相关登记位；届时回填 KDS GCWORLD V1.0.1 注记（「扩展由 WAS 版本化承接」→「已承接于…」）。

两级之间保持 candidate 标注（见 spec「提前引用防护」）。

## 3. 兼容性六项声明（WAS AGENTS 协议）

| # | 项 | 声明 |
| --- | --- | --- |
| 1 | WAS 基线版本 | v1.3.0（2026-10-12 转正） |
| 2 | Ontology 版本与被影响术语 | 新增术语候选「场景流 ScenarioFlow」；既有 8 流与 8 维术语不变不删 |
| 3 | XWAIL 影响 | 若 `flowType` 采用封闭枚举需评估新增档位（候选 `ScenarioFlow`）；Schema/Validator 影响待 XWAIL 侧确认——本变更不代改 |
| 4 | AaaS 影响 | 无直接变更；ServicePackage / Metering / SLA / EvidenceRequirement 不涉 |
| 5 | WAME 影响 | 不涉及注册/授权/发布动作；流类目登记位如需启用走 WAME 后续流程 |
| 6 | 迁移决定 | **compatible**（纯新增；既有数据与契约无需迁移；不 deprecated 任何内容） |

未决项按 `candidate/partial` 标注，不得以默认值填充、不得据此提升状态。

## 4. 文档与证据

- **Feature 绑定：** F-022 `was-scenario-flow-extension`（journal 与证据目录随 Feature 保留）。
- **文档控制：** 本 change 全部文档经 `document_control.py`（`DOCUMENT_CONTROL_SCOPE` 增量模式）登记进 `09-status/globalcloud-document-control-register.md` 与 `09-status/kds-development-space-sync-register.md`，并镜像至 KDS 开发空间（`开发/05-KDS/openspec/changes/was-scenario-flow-extension/`）。
- **验证证据：** 术语一致性核对（登记草案定义 vs 裁定文本 vs GCWORLD V1.0.1，归一化逐字比对）；文档门禁运行结果。
- **Harness 交接：** 本变更不声明完成；状态提升（如纳入确认）由 Harness 治理与人工确认决定。

## 5. 边界

- 不把「登记完成」表述为「已纳入」。
- 不改写 WAS 主方案正文（留 tasks §3，待复核）。
- 定义文本一字不改（照录裁定与 GCWORLD V1.0.1 既定定义）。
