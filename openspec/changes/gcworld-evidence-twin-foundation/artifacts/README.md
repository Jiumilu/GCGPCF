---
doc_id: GPCF-DOC-GCWORLD-023
title: GCWORLD 受控实施产物
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, MMC, Brain, Studio]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/artifacts/README.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/artifacts/README.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

# GCWORLD 受控实施产物

本目录保存 GCWORLD 规划与只读评估阶段的机器可读授权、清单、报告及证据索引。目录内产物不得被解释为 KDS 写入、跨仓实现、部署、验收或状态提升授权。

| 产物 | 用途 |
| --- | --- |
| `gcworld-kds-readonly-source-authorization-v1.yaml` | 固化KDS全空间只读普查范围、数据分级边界和人工争议裁决责任 |
| `gcworld-kds-readonly-admission-assessment-20260823.md` | 记录KDS工作树前后快照、读取准入阻塞和解除条件 |
| `gcworld-kds-readonly-census-summary-20260823.yaml` | 记录干净快照上的全来源元数据普查、确定性摘要和逐路径分级阻塞 |
| `gcworld-kds-full-classification-authorization-20260823.yaml` | 固化一次性全量受控分级扫描授权、隔离快照和敏感内容输出边界 |
| `gcworld-kds-source-classification-ledger-20260823.jsonl` | 逐来源记录分级、来源摘要和处置状态；S3仅保留授权白名单字段 |
| `gcworld-kds-asset-candidate-ledger-20260823.jsonl` | 记录人员和组织未决候选、来源证据及关系引用，不生成正式世界资产标识 |
| `gcworld-kds-relation-evidence-ledger-20260823.jsonl` | 记录来源提及和候选职能关系证据，不提升为事实关系 |
| `gcworld-kds-classification-exception-queue-20260823.jsonl` | 记录S3、技术排除和格式例外的稳定复核队列 |
| `gcworld-kds-controlled-classification-summary-20260823.json` | 汇总本轮数量、快照、确定性摘要和零写入状态 |
| `gcworld-kds-controlled-classification-report-20260823.md` | 汇总来源覆盖、候选重复、数据质量、确定性证据和剩余风险 |
| `KDS全量组织资产普查与世界初始化规范_v1.0.md` | 定义来源闭环、身份归一、关系证据、四世界边界和例外处置标准 |
| `gcworld-codegraph-impact-declaration-v1.yaml` | 声明GKE-001、F-013、GCWORLD与依赖系统的规划关系及零CodeGraph源码变更 |
| `gcworld-kds-preservation-authorization-20260823.yaml` | 固化KDS保全式整理授权、执行边界、完整状态摘要和恢复要求 |
| `gcworld-kds-preservation-result-20260823.yaml` | 记录773项变更的保全对象、恢复演练、干净快照及后续准入阻塞 |
| `gcworld-world-model.schema.json` | 定义资产、别名、关系、证据和四类世界状态的机器可读契约 |
| `gcworld-world-model-fixtures.json` | 提供三组正例和四组具有明确拒绝原因的反例 |
| `gcworld-role-agent-governance.schema.json` | 定义职能智能体注册、行动信封、执行账本、风险和零写入状态边界 |
| `gcworld-role-agent-governance-fixtures.json` | 覆盖镜像、辅助、委托、自治四种模式，六种账本结果和十二类越权反例 |
| `gcworld-role-agent-governance-contract-manifest.yaml` | 固化治理Schema、夹具、校验器和回归测试的摘要与状态边界 |
| `gcworld-world-auth.schema.json` | 定义身份、角色、任用、授权、委托、世界快照、裁决、回执、撤销和派生资产十类权限责任对象 |
| `gcworld-world-auth-fixtures.json` | 覆盖五类合法授权责任链和十四类具有明确拒绝原因的越权、失效及降级反例 |
| `gcworld-world-auth-contract-manifest.yaml` | 固化世界原生权限与责任Schema、夹具、校验器、回归测试及零真实授权边界 |
| `gcworld-world-runtime.schema.json` | 定义十类运行服务、十阶段闭环、任务、承诺、行动回执、补偿、命令幂等、模拟分支和提升候选 |
| `gcworld-world-runtime-fixtures.json` | 覆盖六类合法运行链路和十五类具有明确拒绝原因的跳步、无证关闭、补偿及模拟隔离反例 |
| `gcworld-world-runtime-contract-manifest.yaml` | 固化世界运行时Schema、夹具、校验器、回归测试及零真实执行边界 |
| `gcworld-workbench.schema.json` | 定义十二个统一工作中心、单一资产档案、八类权限投影面、协作空间、共享契约与可解释记录 |
| `gcworld-workbench-fixtures.json` | 覆盖六类合法工作台链路和十六类具有明确拒绝原因的导航、身份、泄漏及撤销反例 |
| `gcworld-workbench-contract-manifest.yaml` | 固化工作台产品Schema、夹具、校验器、回归测试及零真实跨租户共享边界 |
| `gcworld-engineering-governance.schema.json` | 定义七层数据、七类存储、投影重建、统一标识、八类接口、可靠事件、安全指标与P0—P7门禁 |
| `gcworld-engineering-governance-fixtures.json` | 覆盖七类合法工程治理链路和二十一类具有明确拒绝原因的主账、事件、安全及阶段越界反例 |
| `gcworld-engineering-governance-contract-manifest.yaml` | 固化工程治理Schema、夹具、校验器、回归测试及零真实事件和零凭据变更边界 |
| `GCWORLD总体架构与能力规划_v1.0.md` | 汇总系统边界、核心模型、运行闭环、工作台、实施路线及当前阻塞结论 |
| `../../../../tools/kds-sync/run_gcworld_kds_readonly_census.py` | 固定使用正式授权、默认拒绝并仅向标准输出生成确定性只读来源清单 |
| `../../../../tests/test_gcworld_kds_readonly_census.py` | 验证脏工作树阻断、S3元数据边界、秘密与符号链接隔离、确定性和零写入 |
| `../../../../tools/kds-sync/run_gcworld_kds_controlled_classification.py` | 按固定授权和隔离快照执行全来源受控分级、候选提取及确定性台账输出 |
| `../../../../tests/test_gcworld_kds_controlled_classification.py` | 验证S3最小披露、Office解析、LFS例外、未决身份隔离、确定性和零写入 |
| `../../../../tools/kds-sync/validate_gcworld_role_agent_governance.py` | 确定性校验运行模式、风险上限、高影响动作默认拒绝和账本引用闭环 |
| `../../../../tests/test_gcworld_role_agent_governance.py` | 验证治理Schema、清单摘要、四模式、六结果、十二负例及零外部写入 |
| `../../../../tools/kds-sync/validate_gcworld_world_auth.py` | 确定性复算授权交集、世界版本、职责分离、义务、撤销和派生限制传播 |
| `../../../../tests/test_gcworld_world_auth.py` | 验证十类责任对象、五组正例、十四组负例、摘要固定和零真实授权 |
| `../../../../tools/kds-sync/validate_gcworld_world_runtime.py` | 确定性校验服务职责、闭环顺序、证据关闭、幂等、补偿和模拟事实提升隔离 |
| `../../../../tests/test_gcworld_world_runtime.py` | 验证十类服务、十阶段、六组正例、十五组负例、摘要固定和零真实执行 |
| `../../../../tools/kds-sync/validate_gcworld_workbench.py` | 确定性校验统一导航、资产档案、全链路裁剪、共享期限与撤销后访问阻断 |
| `../../../../tests/test_gcworld_workbench.py` | 验证十二中心、十三档案区段、八投影面、六组正例、十六组负例及零真实共享 |
| `../../../../tools/kds-sync/validate_gcworld_engineering_governance.py` | 确定性校验数据提升、投影重建、存储权威、事件幂等、秘密隔离及阶段授权 |
| `../../../../tests/test_gcworld_engineering_governance.py` | 验证七层、七存储、八接口、十一指标、八阶段、七组正例和二十一组负例 |
