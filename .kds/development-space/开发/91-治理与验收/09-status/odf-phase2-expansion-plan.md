---
doc_id: GPCF-DOC-808690228D
title: ODF Phase 2 扩大样本验证计划
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-phase2-expansion-plan.md
source_path: 09-status/odf-phase2-expansion-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# ODF Phase 2 扩大样本验证计划

日期：2026-06-17

## 目标

在 ODF 第一轮 `pilot_closed` 的基础上，将 ODF metadata envelope 样本扩展到 10 个，覆盖治理、KDS/知识、OKF 导航、业务资料导入、Loop/Harness evidence 五类场景，验证 ODF 能否跨类型稳定工作。

## 禁止事项

- 不全量导入 ODF。
- 不批量改写 Markdown 正文。
- 不替代 Git、KDS、OKF 或 Loop evidence。
- 不自动升级 `accepted` 或 `integrated`。
- 不将其它并行工作线的 KDS create/update 混入本阶段同步批次。

## 样本分布

| category | count | sample ids |
| --- | ---: | --- |
| governance | 2 | `ODF-PHASE2-20260617-001` 至 `002` |
| kds-knowledge | 2 | `ODF-PHASE2-20260617-003` 至 `004` |
| okf-navigation | 1 | `ODF-PHASE2-20260617-005` |
| business-import | 3 | `ODF-PHASE2-20260617-006` 至 `008` |
| loop-harness-evidence | 2 | `ODF-PHASE2-20260617-009` 至 `010` |

## 证据

| artifact | path |
| --- | --- |
| Phase 2 sample ledger Markdown | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` |
| Phase 2 sample ledger JSON | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.json` |
| Phase 2 envelopes | `docs/harness/evidence/odf-samples/phase2/*.json` |
| Phase 2 closure report | `docs/harness/evidence/odf-phase2-closure-report-20260617.md` |

## 完成门禁

1. 样本数量不少于 10。
2. 每个样本具备 12 个准入字段。
3. `source_hash`、`markdown_hash`、`odf_hash` 可复算。
4. 污染检查通过。
5. KDS TOKEN 检查通过。
6. Loop 文档门禁通过。
7. KDS 本地镜像冲突检查通过。
8. KDS 同步计划通过。
9. Phase 2 ODF 相关 KDS 待同步项为 0。

## 同步规则

Phase 2 必须继续使用定向同步：

```bash
python3 tools/kds-sync/kds_sync_apply.py \
  --confirm-development-space \
  --max-writes 25 \
  --batch-size <N> \
  --source-path <ODF Phase 2 artifact>
```

## 当前状态

当前状态：`phase2_closed`

关闭报告：`docs/harness/evidence/odf-phase2-closure-report-20260617.md`

不得声明：

- `full_rollout`
- `accepted`
- `integrated`
