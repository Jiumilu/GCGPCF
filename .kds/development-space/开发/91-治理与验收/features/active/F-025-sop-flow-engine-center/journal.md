---
doc_id: GPCF-DOC-F025-SOP-FLOW-ENGINE-CENTER
title: F-025 sop-flow-engine-center
project: GPCF
related_projects: [SOP, GPC, WAS, XWAIL, WAME, GFIS, PVAOS, PQC, KDS, MMC, ICP, Brain, Studio]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-025-sop-flow-engine-center/journal.md
source_path: features/active/F-025-sop-flow-engine-center/journal.md
sync_direction: bidirectional
last_reviewed: 2026-10-17
supersedes: []
superseded_by: []
---

# F-025 sop-flow-engine-center

## 2026-10-18 · GPC 流规则包消费改造开工 · LOOP 五问

### 这轮做什么？
- 按「继续」推进：三仓 push、3 条开发侧流模型转正、GPC 侧流规则包消费改造开工。

### 改了什么？
- SOP 仓：3 条开发侧流模型（loop-governance-flow/openspec-change-flow/harness-engineering-flow）candidate→approved v1.0（老卢确认），4 条流模型全部 approved；三仓 push（GCSOP/GCGPC/GCGPCF 全部同步远端）。
- GPC 仓：新增 `gpc_native/flow_package/` 消费器（FlowRulePackage 模型、发布者校验、哈希防篡改、状态词约束、证据要求读取）+ 首条流规则包样例 FRP-chain-factory-transport-sales-recovery-service-v1.0 + 生成脚本。
- GPC models 改造：SOPDefinition 移除、SOPExecution→FlowStageExecution、sop_deployment→flow_package_deployment、sop_refs→flow_package_refs——SOP 引擎残留清除。

### 怎么验证？
- pytest 8/8 通过：样例包加载、篡改拒收、伪造发布者拒收、缺哈希拒收、状态词越界、禁声明、证据要求读取、模型可用。
- 环境坑：Hermes shell 会话 PYTHONPATH 指向 Hermes 自带 venv（py3.14）导致项目 venv 的 pydantic 加载失败——unset PYTHONPATH 后重建 .venv 解决。

### 发现什么问题？
- GPC-Native 实际代码只有 models 195 行（api/engine/db 未建），消费器是独立模块，FastAPI 集成留后续。
- SOP 仓会话收口时 validate_sop_assets 抓到 project.json 本体 active_session_id 未同步——已修复并记入流引擎技能。

### 是否可以提交？
- authorization：老卢 2026-10-18「继续」。
- confirmation：流规则包接口契约仍为草案，GPC API 集成未实施；不声明流规则包链路生产可用。

## 2026-10-17 · 流引擎中心定位升级（裁定承接）· LOOP 五问

### 这轮做什么？
- 承接老卢 2026-10-17 两条裁定：①GPC 平台「SOP 引擎」作废，GlobalCloud SOP 项目为项目群**唯一流引擎**；②流引擎范围覆盖业务侧、开发侧及所有与流有关的内容。
- 以 WAS 九流（2026-10-16 四仓联动纳入，权威源 `WAS世界资产体系/okf/was/was-flows.yaml`）为流引擎语义底座。

### 改了什么？
- SOP 仓：新增《GlobalCloud 流引擎中心总体方案》草案 v0.1（`docs/architecture/flow-engine-center-master-plan.md`，status=draft）；定义三层流口径（WAS 九流=语义坐标系 / 项目群四流=运行时横切 / 业务与开发流=实例登记治理）、五层架构（L0 流语义→L1 流模型→L2 规则装配→L3 流实例会话→L4 收口晋升）、与各仓边界。
- GPC 仓：`gpc_sop_engine/` 目录（68K，9 文件）作废归档至 `~/.hermes/archive/gpc-sop-engine-20261017/`；7 个文档（README/Harness Manifest/继续开发路线/GPC-Native 实施规划/总体方案/全面分析报告/公共服务平台总体方案）中「SOP 引擎」表述全部标记已作废，GPC 定位改为「流规则包消费执行点」。
- GPCF 仓：项目群系统架构图（2026-10-17 v0.1）同步——L2 层表、主图 SOP/GPC 节点、图3 供应链节点、项目映射矩阵第 7/18 行更新为流引擎中心口径。
- 建立本 feature journal（F-025），登记定位升级治理流。

### 怎么验证？
- SOP 仓门禁：`validate_chinese_document_gate` pass（15 文档）；`validate_sop_assets` OK。
- GPC 仓下架断言：`grep -rn "SOP 引擎"` 仅存「已作废」标记文本，无现役定位表述；`gpc_sop_engine/` 目录已不存在，归档目录 9 文件 68K 可核。
- 架构图口径：GPC 条目、SOP 条目、L2 层表、图3 均已更新（diff 可核）。

### 发现什么问题？
- GPC 仓历史 dirty 状态（.harness/runs/ 8 月遗留产物）与本次改动无关，未触碰；本次 GPC 改动按白名单文件提交。
- 待办（不阻塞本裁定）：①SOP 仓新增 flow-registry/flow-instance schema 骨架与首批流模型登记（链厂运销回服晋升）；②GPC「流规则包」接口契约设计（与流引擎中心协同）；③开发侧流（LOOP/openspec/Harness）第二批接管规划。

### 是否可以提交？
- authorization：老卢 2026-10-17「按建议继续」（归档+修订+传导全执行）。
- confirmation：流引擎中心总体方案为 draft，未转 controlled；GPC 流规则包消费改造未实施；不声明任何流已建成或生效。