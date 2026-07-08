---
doc_id: GPCF-DOC-08716345C2
title: Review Loop
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/loops/review_loop.md
source_path: loops/review_loop.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# Review Loop

Review Loop 只复核 Feature 是否具备关闭条件，不扩张过程文档。

最低检查：

- `feature.yaml` 状态完整。
- `journal.md` 有五问记录。
- `evidence/` 至少有一份可验证结果。
- 风险已登记。
- 未越过 commit、push、deploy、真实 API、真实 KDS API 或状态提升边界。
- runtime 队列中 active Feature 与 `features/active/` 一致。
- Evidence Gate 不得用默认 `not_required` 代替可执行证据或明确豁免。
- 已关闭 Feature 必须保留 `runtime/logs/F-xxx.jsonl`，并在 queue 中标记 `closed` 与 `Recorder`。
