---
doc_id: GPCF-LOOP-PROJECT-GROUP-DEV-P0-PROJECT-VALIDATION-001
title: Loop Round GPCF-PROJECT-GROUP-DEV-P0-PROJECT-VALIDATION-001
project: GPCF
related_projects: [GPC, WAES, KDS, PKC, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-PROJECT-VALIDATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-PROJECT-VALIDATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-PROJECT-GROUP-DEV-P0-PROJECT-VALIDATION-001

## run

- 输入：P0-A dirty 分类后，继续执行 P0-B 项目级最小验证。
- 范围：GPC、Studio、MMC、KDS、PKC。
- 执行：
  1. 读取各项目验证入口。
  2. 运行 GPC JS check 与目标 Playwright E2E。
  3. 运行 Studio harness check。
  4. 运行 MMC runtime pytest。
  5. 运行 KDS API smoke pytest。
  6. 运行 PKC Vite build。
  7. 检查测试/构建生成物的 Git 状态边界。

## stop

| 字段 | 值 |
|---|---|
| stop_type | project_validation_passed |
| stop_reason | P0-B 覆盖项目的最小验证全部通过；剩余阻点转入 generated/output/dist 隔离与 GPCF 大工作区拆分 |

## verify

通过命令：

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC" && npm run check:js
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC" && npx playwright test tests/e2e/gcfis-core-flow.spec.js --reporter=list
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio" && npm run harness:check
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC" && MMC_TEST_MODE=true PYTHONDONTWRITEBYTECODE=1 python3 -m pytest runtime/tests -q
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS" && PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_api_smoke.py -q
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC" && npm run build
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_dev_p0_project_validation_20260626.py
```

## recover

- 本轮未提交、未推送、未部署、未生产写入、未 schema migrate。
- PKC build 生成物保留在既有 `dist` dirty 分类中，后续 P0-C 决定隔离方式。
- GPC Playwright 本地 webServer 由 Playwright 生命周期管理，本轮结束后无报告目录进入 Git 状态。

## debug

- GPC E2E 全部通过，说明测试文件 dirty 不再是开发态验证阻点。
- Studio harness 通过，release review 仍只能作为提交前候选，不触发发布。
- MMC/KDS pytest 通过，未触发真实 KDS Token 写入。
- PKC build 通过，但生成物变化仍是提交前隔离项。

## 输出

- `docs/harness/evidence/globalcloud-project-group-dev-p0-project-validation-20260626.md`
- `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-PROJECT-VALIDATION-001.md`
- `tools/kds-sync/validate_project_group_dev_p0_project_validation_20260626.py`

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| project_validation_ready | true |
| 开发态是否可推进 | yes |
| 是否提交/推送 | no |
| 是否 accepted/integrated/production_ready | no |
