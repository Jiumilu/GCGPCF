---
doc_id: GPCF-DOC-F013-KDS-P1-HANDOFF-20260802
title: F-013 KDS P1 实施交接
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/artifacts/kds-p1-handoff.md
source_path: features/active/F-013-knowledge-asset-model-system/artifacts/kds-p1-handoff.md
sync_direction: bidirectional
last_reviewed: 2026-08-03
supersedes: []
superseded_by: []
---

# F-013 KDS P1 实施交接

日期：2026-08-03

## GKE-001 交接身份

本交接是 `GlobalCloud Knowledge Engineering`（`GKE-001`）从 GPCF canonical 控制面到 KDS 阶段 A 实现面的受控交接。上位规范为 `03-data-ai-knowledge/GlobalCloud项目群知识工程规范.md`；F-013 只负责契约冻结与独立验收，不拥有 KDS 运行时或真实资料写入权。

```yaml
knowledge_engineering_handoff:
  contract_version: v0.1
  canonical_manifest_sha256: 7134a825c6da5e6a43ac1408f41b8fd0187ce635068d3fb3b8ca81b4fcf6c0be
  implementation_change: adopt-knowledge-asset-envelope
  source_of_truth: KDS
  changed_files:
    - okf/knowledge-asset-contract-manifest.yaml
    - okf/knowledge-asset-envelope.schema.json
    - okf/knowledge-asset-vocabulary.yaml
    - okf/knowledge-asset-envelope.example.json
    - okf/knowledge-object.example.json
    - okf/knowledge-object-approved-copy.example.json
  api_contract: pending_required_for_kds_stage_a_return_handoff
  authorization_boundary: no_real_kds_write_no_production_or_shared_config_no_status_promotion
  migration_dry_run: pending_required_for_kds_stage_a_return_handoff
  acl_tests: pending_required_for_kds_stage_a_return_handoff
  audit_tests: pending_required_for_kds_stage_a_return_handoff
  rollback_boundary: remove_sidecar_projection_and_index_without_deleting_canonical_source_or_knowledge_object
  unresolved_risks:
    - kds_dirty_worktree
    - kds_contract_manifest_drift
    - kds_stage_a_handoff_pending_independent_acceptance
    - studio_browser_task_flow_not_verified
    - human_confirmation_not_completed
  status_ceiling: partial
```

## OpenSpec

- KDS change：`adopt-knowledge-asset-envelope`
- 路径：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/openspec/changes/adopt-knowledge-asset-envelope/`
- artifacts：proposal、design、spec、tasks 均完成。
- `openspec status`：`isComplete=true`，apply requirements 已满足。
- `openspec validate --strict`：pass，issues=0。

这里的 `apply-ready` 只表示规划 artifacts 完整，不表示 KDS 工作树已经满足源码实施准入。

## 机器准入门禁

只读复核命令：

```text
python3 tools/kds-sync/validate_f013_kds_apply_admission.py
```

当前结果（2026-08-02T19:55:05+08:00 只读快照）：

```text
f013_kds_apply_admission_gate=pass change=adopt-knowledge-asset-envelope planning=complete strict_validation=pass kds_worktree_dirty=true changed_entries=319 staged_entries=0 ahead=5 behind=0 admission=blocked_dirty_worktree kds_write_authorized=false deployment_authorized=false completion_status=not_complete
```

门禁 `pass` 表示“阻塞状态与 Feature 边界一致并可机器回放”，不表示 apply 已获授权。
同一 KDS Git status 快照前后运行准入校验器，结果为 `status_snapshot_unchanged=true`，确认校验器本身未写 KDS；本轮计数漂移来自校验器之外的活动工作树变化。

## 已确认现状

- 现有飞书管线已具备一个纪要正本、内容空间分类、关联投影、PostgreSQL `analysis_versions/space_bindings` 和 pending-confirmation outbox。
- `SpaceRegistry` 与 `SpaceClassifier` 当前将“工业绿链”等内容板块和 `personal/team/partner` 等访问空间放在同一分类集合中。
- 现有 `space_bindings` 缺少 ACL policy、projection mode、业务/研发项目分维和词表/契约版本。
- `canonicalize-project-meeting-relations` 只解决项目详情到会议正本的只读关系，不替代 KnowledgeAssetEnvelope。

## P1 实施边界

允许：

- 固定 GPCF v0.1 Schema/词表镜像和校验和。
- 读取 `asset_type_compatibility`，新对象使用 `default_okf_object_type`，既有对象仅在 `compatible_okf_object_types` 内无改 ID 接入。
- 镜像当前 draft 必须保留受控资产/关系枚举、11 个上下文引用字段的独立 URI 命名空间、非空 evidence/lineage、partner/public 策略与批准证据，以及 `authorized_write` 外部授权证据约束。
- 新增纯 Envelope adapter、sidecar migration、dry-run、授权读投影和测试。
- Envelope adapter 必须拒绝跨命名空间放置的上下文引用，不得将业务项目、研发项目、系统或组织引用互相代用。
- Envelope adapter 必须校验 `knowledgeObjectRef` 指向现有 canonical 对象，并保持 tenant 与 source/evidence/lineage 一致；不匹配时只返回阻塞结果，不创建 sidecar。
- Envelope adapter 必须按七空间映射校验 primary Space 与 canonical KnowledgeObject domain；`family/ops` 保留内容 domain，不得自动新增或改写 domain。
- 三种投影模式必须执行 GPCF Schema 条件约束：脱敏投影保留 projection lineage；批准副本还必须具备批准证据和不同于原 canonical 的派生对象引用，并解析到同 tenant/source、包含 projection lineage、`human_confirmed` 的 OKF 派生对象；引用/脱敏模式不得伪造派生正本。
- 当前 KDS `knowledge_intake` bridge 的 vendored v0.1 合同仅含 Schema、Envelope 示例和词表；缺少 `okf/knowledge-asset-contract-manifest.yaml`、canonical fixture 与 `okf/knowledge-object-approved-copy.example.json`。`validate_f013_kds_apply_admission.py` 会只读比较 manifest、Schema、词表、Envelope 示例和两个 KnowledgeObject fixture 的哈希；该检查构成 GPCF manifest 哈希复核门禁。在镜像补齐前，不得将 bridge fixture 测试视为 F-013 跨仓集成证据。
- 保留既有 `primary_space/related_spaces` 为内容集合兼容字段。

禁止：

- 将主题分类直接解释为 team/partner/public ACL。
- 改写飞书原始证据、会议 Markdown、既有分析版本、对账结果或 canonical ID。
- 未经确认执行真实语料回填、跨空间共享、Brain/MMC 写入或部署。

## 启动条件

KDS 当前 `main...origin/main [ahead 5]`，并存在大量未跟踪飞书运行产物和多个活动 change。进入 apply 前必须先满足其一：

1. 当前飞书工作单元完成范围确认并沉淀为可审查基线；或
2. 建立包含这些已确认提交、但不包含未确认运行产物的隔离工作树。

未满足启动条件时，F-013 保持 `active/evaluate`，KDS P1 保持 planning/apply-ready，不实施、不提交、不推送。
