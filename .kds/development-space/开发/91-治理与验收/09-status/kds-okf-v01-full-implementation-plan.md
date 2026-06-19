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
last_reviewed: 2026-06-12
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
| Phase 3 | Governance、Architecture bundle 标准化 | multi-bundle OKF tree | bundle root index/log pass |
| Phase 4 | 搜索/图谱消费试运行 | consumer smoke evidence | Agent 查找证据准确率提升 |
| Phase 5 | 密级评审后逐批允许正文摘要 | approved summary sections | owner approval + sensitivity pass |
| Phase 6 | 全量持续生成 | scheduled or Loop-triggered generation | no stale bundle, no double-source |

## 当前已执行

| item | result |
| --- | --- |
| 生成器 | `tools/kds-sync/generate_okf_bundle.py` |
| 校验器 | `tools/kds-sync/validate_okf_bundle.py` |
| 首批 bundle | `.okf/bundles/kds-v0.1` |
| 当前 concept 数量 | 40 |
| evidence report | `docs/harness/evidence/kds-okf-v01-phase1-bundle-report-20260619.md` |
| reserved filename remap | `index.md` / `log.md` source documents generate as `index-concept.md` / `log-concept.md` |

## 全量放行标准

| gate | required result |
| --- | --- |
| OKF conformance | `okf_bundle_gate=pass` |
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

Phase 2 当前 seed 扩展已执行并通过。下一阶段需要补充 link/backlink gate、stale bundle gate 和 Agent 消费 smoke test；如存在已废弃或未确认文档，应先标记 `archive`、`deprecated` 或从 bundle seed 中排除。
