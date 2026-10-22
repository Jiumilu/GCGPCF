---
doc_id: GPCF-DOC-F011-STUDIO-WORKBENCH-SUMMARY-20260712
title: 证据摘要
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-011-studio-workbench-ui-runtime-closure/evidence/summary.md
source_path: features/done/F-011-studio-workbench-ui-runtime-closure/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 证据摘要

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass（Feature 专属：Studio 设置页 2 文件 / 13 用例通过；仓级全量 4 项既有失败与本 Feature 无关，记录于 `evidence/verification-2026-10-22.txt`，不计入门禁）
- build: pass（`cd ../GlobalCloud Studio && npm run build` exit 0：openapi:generate + vue-tsc + vite build + server bundle）
- screenshots: pass（设置页运行态截图 + 结构指标；2026-10-22 哈希复核一致、人工复核未见机器接口字段暴露）
- api: waived（本 Feature 仅改设置页前端，无 API 证据要求；理由见 feature.yaml `verification.waivers.api`）
- lint: 已通过 build 证据中的 `git diff --check` 覆盖（GPCF 与 Studio 两仓均 exit 0）。
- ui_product_first_control.gates: functional_completeness=pass、quality_baseline=pass、multi_user_usability=pending、task_flow_e2e_status=fail（设置页之后的既有壳层断言失败，非本 Feature 范围）、accessibility_status=pending、evidence_overexposure_gate=pass；`status_ceiling` 保持 partial。
- risk: 未授权 commit、push、deploy、真实 API、状态提升；未做多用户与无障碍专项验证；不声明 accepted / integrated / production_ready / customer_accepted。
- 复核记录: `evidence/verification-2026-10-22.txt`
