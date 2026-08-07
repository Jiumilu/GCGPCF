---
doc_id: GPCF-DOC-F013-KNOWLEDGE-ASSET-VALIDATION-20260802
title: F-013 知识资产模型验证证据
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/knowledge-asset-model-validation.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/knowledge-asset-model-validation.md
sync_direction: bidirectional
last_reviewed: 2026-08-02
supersedes: []
superseded_by: []
---

# F-013 知识资产模型验证证据

日期：2026-08-02

## 机器契约

| 检查 | 结果 |
|---|---|
| `knowledge-asset-envelope.schema.json` JSON 解析 | pass |
| `knowledge-asset-envelope.example.json` JSON 解析 | pass |
| `knowledge-object.example.json` JSON 解析与 OKF Schema 校验 | pass |
| `knowledge-asset-vocabulary.yaml` YAML 解析 | pass |
| Draft 2020-12 Schema 自检 | pass |
| 飞书会议纪要示例 Schema + format 校验 | pass |
| 八组受控枚举与 Schema/词表一致性 | pass |
| 11 个上下文引用字段 URI 命名空间约束 | pass |
| 15 种 Envelope `assetType` 到 OKF `objectType` 默认/兼容映射 | pass |
| 七空间到 OKF knowledge domain/domain policy 映射 | 7/7 pass |
| 三种跨空间投影模式正例 | 3/3 pass |
| 跨空间投影 Schema/语义负例 | 6/6 全部拒绝 |
| `approved_copy` 派生 KnowledgeObject 解析与 lineage 正例 | pass |
| `approved_copy` 派生对象引用、tenant、lineage、人工确认负例 | 4/4 全部拒绝 |
| KDS 外部 bridge fixture 测试 / OpenSpec strict | 4/4 pass / pass（未计入跨仓集成） |
| KDS vendored 合同完整性 | 当前 GPCF manifest 漂移 1 项；KDS 重新镜像后方可恢复 6/6 一致 |
| canonical/Envelope linkage 正例及 5 个错配负例 | 正例通过、负例全部拒绝 |
| 授权写入合成正例 | pass |
| 第二主账字段、维度折叠、跨命名空间引用、无授权写入和投影缺口等 19 个 Schema 负例 | 全部拒绝 |
| canonical manifest 核心产物与 OKF 依赖哈希 | pass |
| 七访问空间、七知识域和七治理规则一致性 | pass |
| 模型文档 GPCF/draft 契约源 frontmatter | pass |
| `document_control.py` 单文档元数据回放保持 GPCF/draft/v0.1 | pass |
| 项目群双主方案传导与 KDS P1 handoff | pass |

校验命令：

```text
python3 -m json.tool okf/knowledge-asset-envelope.schema.json
python3 -m json.tool okf/knowledge-asset-envelope.example.json
python3 -c '... yaml.safe_load(...) ...'
python3 -c '... Draft202012Validator(...).validate(example) ...'
python3 tools/kds-sync/validate_knowledge_asset_model_system.py
python3 tools/kds-sync/validate_f013_kds_apply_admission.py
```

校验器结果：

```text
knowledge_asset_model_gate=pass contract_id=globalcloud.knowledge_asset contract_version=v0.1 contract_status=draft artifacts=7 dependencies=2 access_spaces=7 knowledge_domains=7 space_domain_mappings=7 orthogonal_context_dimensions=11 okf_object_type_mappings=15 controlled_vocabularies=8 governance_rules=7 example_validation=pass projection_modes_positive_cases=3 projection_semantic_negative_cases=1 approved_copy_linkage_positive_case=pass approved_copy_linkage_negative_cases=4 canonical_link_positive_case=pass canonical_link_negative_cases=5 authorization_positive_case=pass negative_cases=19 hashes=pass master_plan_propagation=pass document_control_override=pass kds_handoff=planning_complete kds_apply_admission=separate_gate completion_status=not_complete accepted=false integrated=false production_ready=false customer_accepted=false kds_write_authorized=false deployment_authorized=false
```

## KDS P1 Apply 准入

```text
f013_kds_apply_admission_gate=pass change=adopt-knowledge-asset-envelope planning=complete strict_validation=pass kds_worktree_dirty=true changed_entries=66 staged_entries=0 ahead=0 behind=0 admission=blocked_dirty_worktree contract_mirror=blocked mirror_missing=0 mirror_mismatched=1 kds_write_authorized=false deployment_authorized=false completion_status=not_complete
kds_admission_side_effect_audit=pass status_snapshot_unchanged=true
```

`admission=blocked_dirty_worktree` 证明当前只能保持规划完成状态；本轮未修改 KDS 源码、未创建隔离工作树、未执行迁移或真实语料回填。

另在 KDS 外部工作树以禁用 pytest cache/bytecode 的方式执行 `tests/test_knowledge_asset_model_bridge.py`，4 个测试通过，`openspec validate establish-kds-knowledge-intake-core --strict` 通过。模型 gate 修正后更新了 canonical manifest 中 validator 的 SHA-256，因此准入 gate 当前为 `contract_mirror=blocked mirror_missing=0 mirror_mismatched=1`；KDS 必须重新镜像该 manifest 后才可恢复一致。即使镜像恢复，KDS 脏工作树、真实 adapter/ACL/查询投影/迁移证据仍须单独交接，不能据此宣称 F-013 跨仓集成完成。

## Feature 局部证据

```text
gpcf_feature_evidence feature=F-013 tests=pass build=pass screenshots=waived api=waived summary=pass
```

UI 和 API 均不在本轮范围；`waived` 不代表后续 KDS/Brain 实现已验证。

## 项目群门禁

```text
loop_document_gate=pass
gate_reasons=none
missing_metadata=0
missing_readme_dirs=0

project_group_gate_readiness=pass
checked_repos=17
passed=17
failed=0
gfis_status_ceiling=repair_required
```

F-013 本地模型、Feature Workspace、文档门禁与项目群 readiness 当前均通过；GFIS 状态上限仍为 `repair_required`，不构成 KDS apply、Feature close 或状态提升授权。该结果不解除 F-013 的 KDS 脏工作树、缺失契约镜像、外部本地镜像审阅、真实实现或人工确认边界；Feature 继续保持 active，不执行 close、commit、push、deploy 或状态提升。

文档控制台账已恢复本轮契约源归属并加入防复发回放。验证期间检测到非本任务触发的 `document_control.py` 全量运行，已产生仓库内 `.kds` 本地镜像/ledger 写入；这些外部改动未删除，已登记阻塞并等待人工审阅。未发现真实 KDS API 同步证据，本任务没有发起 KDS API 写入。
