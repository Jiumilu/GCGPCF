---
doc_id: GPCF-DOC-78DAA04814
title: KDS OKF v0.1 全量派生层实施方案
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/kds-okf-v01-full-implementation-plan.md
source_path: 09-status/kds-okf-v01-full-implementation-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# KDS OKF v0.1 全量派生层实施方案

日期：2026-06-19

## 目标

在不改变 KDS 主存地位的前提下，建立 OKF v0.1 conformant 派生层，使 KDS 受控文档可被 Agent、搜索、图谱、可视化和跨系统交换工具稳定消费。

## 架构口径

```text
KDS / Git controlled documents = source of record
document control register + sync ledger = evidence of governance
OKF v0.1 bundle = derived consumption and exchange layer
ODF envelope = controlled import layer
```

OKF 不替代 KDS、Git、KDS 同步流水、ODF ledger 或 Loop evidence。

## 字段映射

| OKF field | KDS / Git source | 生成规则 | 边界 |
| --- | --- | --- | --- |
| `type` | `source_path`、title | 由路径和标题分类为 KDS Document、Governance Plan、Governance Gate、Governance Report、KDS Ledger、Knowledge Index 或 Architecture Document | 仅用于消费分组，不作为业务状态 |
| `title` | 源文档 frontmatter `title` 或一级标题 | 优先取 frontmatter；缺失时取正文第一个 `#` 标题 | 不改写源标题 |
| `description` | `.okf/<bundle>/index.md` 的 purpose | 直接继承 source index 的 purpose | 只做摘要入口 |
| `resource` | Git 源文件绝对路径 | `file://<source_path>` | 不复制源正文 |
| `tags` | bundle、路径、标题关键词 | 加入 `okf-derived`、`controlled` 与主题 tag | 不作为验收标签 |
| `timestamp` | 源文档 `last_reviewed` | 转为 `YYYY-MM-DDT00:00:00Z` | 不代表最新业务发生时间 |
| `kds_path` | source index 的 KDS 路径 | 原样写入 concept frontmatter | 指向 KDS 开发空间事实位置 |
| `source_path` | source index 的 Git 路径 | 原样写入 concept frontmatter | 回源主键 |
| `source_hash` | Git 源文件 bytes | SHA-256 | stale gate 的判定依据 |
| `source_of_record` | 固定治理口径 | 固定为 `kds` | 防止 OKF 被误当主账 |
| `derivation_policy` | 固定治理口径 | 固定为 `metadata_only_no_body_copy` | 防止正文扩散 |

## 实施原则

1. 先 metadata-only 派生，不复制源文档正文。
2. 所有 OKF concept 必须声明 `source_of_record: kds`。
3. 所有 OKF concept 必须声明 `derivation_policy: metadata_only_no_body_copy`。
4. 每个 concept 的 `resource` 指向 Git 源文件，`kds_path` 指向 KDS 开发空间路径。
5. 事实判断必须回源到受控文档和 KDS 同步流水。
6. 全量 rollout 前必须通过 OKF conformance、污染、TOKEN、KDS conflict、sync plan 和 Loop 文档门禁。

## 分阶段实施

| phase | scope | output | release rule |
| --- | --- | --- | --- |
| Phase 1 | KDS bundle 首批 25 个高价值文档 | `.okf/bundles/kds-v0.1`、Phase 1 report | conformance pass；不复制正文 |
| Phase 2 | 扩展到全部 `.okf/kds/index.md` source documents | current KDS seed OKF bundle | conformance pass；reserved filename remap pass |
| Phase 3 | Governance、Architecture bundle 标准化 | multi-bundle OKF tree | collection gate pass |
| Phase 4 | 搜索/图谱消费试运行 | consumer smoke evidence | Agent 查找证据准确率提升 |
| Phase 5 | 密级评审后逐批允许正文摘要 | approved summary sections | owner approval + sensitivity pass |
| Phase 6 | 全量持续生成 | scheduled or Loop-triggered generation | no stale bundle, no double-source |

## 当前已执行

| item | result |
| --- | --- |
| 生成器 | `tools/kds-sync/generate_okf_bundle.py` |
| 校验器 | `tools/kds-sync/validate_okf_bundle.py` |
| 首批 bundle | `.okf/bundles/kds-v0.1` |
| 当前 concept 数量 | 36 |
| collection concepts | 81 across KDS, Governance and Architecture bundles |
| evidence report | `docs/harness/evidence/kds-okf-v01-phase1-bundle-report-20260619.md` |
| collection evidence | `docs/harness/evidence/okf-v01-collection-gate-20260620.md` |
| relationship graph evidence | `docs/harness/evidence/okf-v01-relationship-graph-20260620.md` |
| consumption benchmark evidence | `docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md` |
| summary admission evidence | `docs/harness/evidence/okf-v01-summary-admission-gate-20260620.md` |
| summary admission ledger | `docs/harness/evidence/okf-v01-summary-admission-ledger-20260620.md` |
| summary approval request package | `docs/harness/evidence/okf-v01-summary-approval-request-OKF-SUM-20260620-001.md` |
| summary approval request gate | `docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.md` |
| summary approval negative fixtures | `docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md` |
| summary approval expiry gate | `docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md` |
| approved summary writer dry run | `docs/harness/evidence/okf-v01-approved-summary-writer-dry-run-20260620.md` |
| approved summary writer positive fixture | `docs/harness/evidence/okf-v01-approved-summary-writer-positive-fixture-20260620.md` |
| reserved filename remap | `index.md` / `log.md` source documents generate as `index-concept.md` / `log-concept.md` |
| link/backlink/stale gate | `tools/kds-sync/validate_okf_bundle.py` |
| Agent consumption smoke | `tools/kds-sync/smoke_okf_agent_consumption.py` |
| Agent smoke evidence | `docs/harness/evidence/kds-okf-v01-agent-consumption-smoke-20260620.md` |
| relationship graph | `tools/kds-sync/build_okf_relationship_graph.py` |
| consumption benchmark | `tools/kds-sync/benchmark_okf_consumption.py` |
| summary admission gate | `tools/kds-sync/validate_okf_summary_admission_gate.py` |
| dynamic seed exclusion | sync plan, generated registers, health report and derived reports stay index-referenced but are not stale-enforced concepts |

## 全量放行标准

| gate | required result |
| --- | --- |
| OKF conformance | `okf_bundle_gate=pass` |
| OKF link/backlink | `links=pass backlinks=pass` |
| OKF stale source hash | `stale=pass` |
| OKF collection | `okf_collection_gate=pass` |
| OKF relationship graph | `okf_relationship_graph=pass` |
| Agent consumption smoke | `okf_agent_smoke=pass` |
| OKF consumption benchmark | `okf_consumption_benchmark=pass` |
| OKF summary admission gate | `okf_summary_admission_gate=pass` |
| OKF summary approval expiry gate | `okf_summary_approval_expiry_gate=pass` |
| 文档污染 | `document_pollution=pass` |
| KDS TOKEN | `kds_token=pass` |
| KDS 本地镜像冲突 | `kds_conflict_guard=pass` |
| KDS sync plan | `kds_sync_plan=pass` |
| Loop 文档门禁 | `gate=pass` |
| 敏感信息 | 不导出 TOKEN、账号、金融凭证、合同全文或未授权客户材料 |
| 状态边界 | 不升级 `accepted`、`complete` 或 `integrated` |

## 风险与控制

| risk | control |
| --- | --- |
| OKF 被误当主账 | concept 声明 source_of_record；报告声明 KDS 主存 |
| 双主账漂移 | OKF 只生成，不手工改事实；后续加入 stale bundle gate |
| 敏感信息扩散 | Phase 1 metadata-only；正文摘要需 owner 批准 |
| 上下文膨胀 | index/log progressive disclosure；按 bundle 分层 |
| 全量盲写 KDS | 只允许 `--source-path` 定向同步治理产物 |
| 并行写入冲突 | 共享工具和 `.kds` 镜像由主线程串行执行 |

## 下一批次

下一阶段建议执行：

```bash
python3 tools/kds-sync/generate_okf_bundle.py --limit 0
python3 tools/kds-sync/validate_okf_bundle.py
```

Phase 2 当前 seed 扩展已执行并通过。link/backlink gate、stale bundle gate 和 Agent 消费 smoke test 已补齐。Phase 3 已生成 Governance 与 Architecture OKF v0.1 bundle，并通过 collection gate。Phase 4 已补齐跨 bundle 关系图和消费侧 benchmark。Phase 5 已建立摘要准入门禁、候选台账、首条批准请求包、负向夹具、approval expiry gate、approved summary 写入器 dry-run 和正向 dry-run 夹具；当前准入状态为 `metadata_only_locked`，候选请求保持 `pending_review`，首条请求等待 human confirmation，partial approval 和 sensitivity 未通过不会被放行，过期 pending request 会被阻断，summary admission gate 已强依赖 approval request gate 与 approval expiry gate，真实 dry-run 当前 `would_write=0`，临时正向夹具证明满足条件时 dry-run 可识别 `would_write=1`，未批准任何正文摘要。下一步只有在 owner approval、source sensitivity review、explicit summary scope、有效期门禁和敏感信息检查均通过后，才允许逐批引入 approved summary。
