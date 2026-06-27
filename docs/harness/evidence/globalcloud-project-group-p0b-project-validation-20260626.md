---
doc_id: GPCF-DOC-P0B-PROJECT-VALIDATION-20260626
title: GlobalCloud 项目群 P0-B 项目级验证复跑证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-p0b-project-validation-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-p0b-project-validation-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 P0-B 项目级验证复跑证据

## 授权边界

- 输入：用户要求“下一步”，承接 P0-A dirty 分类后的 P0-B 项目级验证。
- 范围：只复跑已有明确本地验证入口的 Brain、MMC、KDS、PKC、Studio。
- 允许动作：本地构建、pytest smoke、本地 harness check、生成 evidence、KDS 本地镜像同步。
- 禁止动作：提交、推送、部署、生产写入、schema migrate、真实外部 API 写入、标记 accepted、integrated、production_ready、customer_accepted。
- 判定边界：P0-B 只证明开发态验证入口可运行，不证明验收通过，不关闭 GFIS/GPCF 真实业务 repair_required。2026-06-28 live recheck 下，项目群 Git gate 已回到 `blocked`，但不影响这些本地验证结论仍然成立。

## P0-B 复跑结果

| 项目 | 命令 | 结果 | 关键输出 | 非阻断 warning / 边界 |
|---|---|---|---|---|
| GlobalCloud Brain | `npm run build -- --mode development` | pass | Vite build completed; 2100 modules transformed; `dist/index.html`; build in 2.05s | Node `DEP0205` deprecation warning only |
| GlobalCloud MMC | `MMC_TEST_MODE=true PYTHONDONTWRITEBYTECODE=1 python3 -m pytest runtime/tests/ -q -o cache_dir=/tmp/globalcloud-p0b-mmc-pytest-cache` | pass | `36 passed in 1.29s` | pytest cache placed under `/tmp` |
| GlobalCloud KDS | `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_api_smoke.py -q -o cache_dir=/tmp/globalcloud-p0b-kds-pytest-cache` | pass | `.. [100%]`; exit code 0 | smoke only; no real KDS token written |
| GlobalCloud PKC | `npm run build -- --mode development` | pass | Vite build completed; 1732 modules transformed; `dist/assets/index-BOLbn-u7.css`; `dist/assets/index-BUcdFj8z.js`; build in 1.64s | npm `onlyBuiltDependencies` warning and Node `DEP0205`; `dist` remains build-artifact review candidate |
| GlobalCloud Studio | `npm run harness:check` | pass | `Harness check passed` | release/write workflows remain review_required_before_commit |

## Dirty 影响复核

| 项目 | 复跑后工作区观察 | P0-B 判定 |
|---|---|---|
| Brain | 仍为 AGENTS + 总体/实施方案传导 dirty；build 未新增敏感路径 | dev_validation_pass |
| MMC | 仍为 AGENTS + 总体/实施方案传导 dirty；pytest cache 不写入仓库 | dev_validation_pass |
| KDS | 知识导入/治理同步 dirty 仍存在；smoke exit code 0 | dev_validation_pass_with_knowledge_queue |
| PKC | `dist` bundle 仍为 build-artifact review candidate；build exit code 0 | dev_validation_pass_with_dist_review |
| Studio | release review / harness dirty 仍存在；harness check exit code 0 | dev_validation_pass_with_release_review |

## 当前未关闭事项

- 17 仓 Git gate 当前为 `blocked`；原因是 7 仓 dirty 且 `GlobalCloud KDS/.env.production.example` 命中 sensitive_path；不得声明全仓 clean。
- GFIS/GPCF 真实业务 lane 仍为 `repair_required`；P0-B 不创建真实 source-of-record、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- WAES/人工确认仍是验收态、状态提升、提交/推送/发布前边界。
- PKC `dist` 和 KDS 知识导入仍需后续 review queue 拆分。

## 验证命令

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain" && npm run build -- --mode development
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC" && MMC_TEST_MODE=true PYTHONDONTWRITEBYTECODE=1 python3 -m pytest runtime/tests/ -q -o cache_dir=/tmp/globalcloud-p0b-mmc-pytest-cache
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS" && PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_api_smoke.py -q -o cache_dir=/tmp/globalcloud-p0b-kds-pytest-cache
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC" && npm run build -- --mode development
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio" && npm run harness:check
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_p0b_project_validation_20260626.py
```

## 状态声明

- p0b_project_validation_ready = true
- development_start_allowed = true
- project_group_git_gate = blocked
- dirty_repo_count = 7
- sensitive_repos = GlobalCloud KDS(.env.production.example)
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
