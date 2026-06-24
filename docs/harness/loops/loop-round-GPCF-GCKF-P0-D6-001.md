---
doc_id: GPCF-DOC-B6DF5BB059
title: GC-Knowledge Fabric P0-D6 KDS 状态候选更新 Dry-run LOOP evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D6-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D6-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0-D6 KDS 状态候选更新 Dry-run LOOP evidence

## 本轮目标

完成 P0-D6：建立候选事实到人工确认包再到 KDS 状态候选更新的 dry-run，并锁死 `verified`、`accepted`、`published`、`written_back` 不可由 AI、WAES dry-run、KWE dry-run 或 LOOP 直接写入。

## 本轮输入资料

- `okf/status-machine-policy.yaml`
- `okf/kds-lifecycle-transition-audit-packet-policy.yaml`
- `okf/kwe-promotion-request-policy.yaml`
- `fixtures/kwe/gckf-p0-kwe-minimum-workflow-dry-run-v0.1.json`
- `docs/gc-knowledge-fabric/kds-state-candidate-update-dry-run-v0.1.md`
- `fixtures/kds/gckf-p0-kds-state-candidate-update-dry-run-v0.1.json`

## 本轮新增知识对象

- `docs/gc-knowledge-fabric/kds-state-candidate-update-dry-run-v0.1.md`
- `fixtures/kds/gckf-p0-kds-state-candidate-update-dry-run-v0.1.json`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D6-001.md`

## 本轮检查

| 检查项 | 结果 |
|---|---|
| 是否引用 P0-D5 KWE dry-run 输出 | 是 |
| 是否生成 PromotionRequestCandidate | 是 |
| 是否生成 LifecycleAuditCandidate | 是 |
| 是否阻断 AI 直接 accepted | 是 |
| 是否阻断 LOOP 直接 published | 是 |
| 是否写入 KDS lifecycle | 否 |
| 是否写入 accepted fact / published object / written_back | 否 |
| 是否写入业务系统、收益或积分 | 否 |

## 风险与阻塞

| 风险 | 等级 | 处理 |
|---|---|---|
| 状态候选被误认为真实状态变更 | P1 | fixture 明确 `writesKdsLifecycle=0` |
| 人工确认包被误认为 accepted | P1 | accepted 仍需 human/committee confirmation 与 Harness evidence |
| publication 候选绕过 redaction/external share | P1 | LOOP 请求 published 直接 blocked |

## 下一轮动作

进入 P0-D7：

- 建立 API 骨架输入清单：KDS v2、WAES、KWE、GFIS Assistant、Governance/LOOP。
- 将 P0-D2 至 P0-D6 的 fixtures 归并为 API dry-run 输入矩阵。
