---
doc_id: GPCF-DOC-86E433AAA5
title: F-030（PDC 纳管）重采清单（交 PDC 属主执行）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p05-pdc-f030-resample-checklist-20261022.md
source_path: docs/reports/p05-pdc-f030-resample-checklist-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-030（PDC 纳管）重采清单（交 PDC 属主执行）

- 依据：老卢 2026-10-22 21:12 裁定「出清单交 PDC 属主，GPCF 不代跑跨项目仓」
- 现状：`gpcf_feature_evidence.py F-030 --check-only` → `evidence is incomplete; governance blockers remain`
- 根因：`tests` 与 `summary` 为 fail；经查该 fail 来自 **GPCF 全群门禁**（project_group_live_status_current 等），而该门禁已于 2026-10-22 改为 SHA 语义并 `pass`

## 属主在 PDC 仓执行的步骤

```bash
cd "GlobalCloud PDC"
# 1) 重跑测试（按 PDC 既有命令入口；若 Makefile 有 test 目标优先用）
npm test 2>&1 | tee /tmp/pdc-tests.log || true
# 2) 汇总证据写回 GPCF Feature 工作区
cp /tmp/pdc-tests.log "../GlobalCloud GPCF/features/active/F-030-pdc-project-group-onboarding/evidence/tests.txt"
```

3) 在 PDC 仓生成本次 summary（范围/结论/证据路径），写入
`GlobalCloud GPCF/features/active/F-030-pdc-project-group-onboarding/evidence/summary.md`

4) 回到 GPCF 复核：
```bash
cd "../GlobalCloud GPCF"
python3 scripts/gpcf_check_evidence.py F-030 --check-only
```
期望：`evidence is incomplete` 消失，只剩 `governance blockers remain`（再走解除流程）。

## 完成判据

1. `evidence/tests.txt` 首行为本次执行时间与命令，结论 pass；
2. `evidence/summary.md` 含范围、结论、证据路径与"不声明 accepted/integrated"字样；
3. `gpcf_check_evidence.py F-030 --check-only` 不再报 evidence 类理由。

## 回滚

仅替换 2 个证据文件，`git checkout -- features/active/F-030-*/evidence/` 即可。
