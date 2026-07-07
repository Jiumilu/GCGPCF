---
doc_id: GPCF-DOC-7373A1BEDE
title: Repair Loop
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/loops/repair_loop.md
source_path: loops/repair_loop.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# Repair Loop

Repair Loop 只处理 Evidence Gate 失败项。

失败项必须回写到 `feature.yaml` 的 `blockers`，并在 `journal.md` 追加一轮五问记录。修复完成后重新运行：

```bash
python scripts/gpcf_check_evidence.py <FEATURE_ID>
```
