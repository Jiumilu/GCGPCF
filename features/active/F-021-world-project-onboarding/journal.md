---
doc_id: GPCF-WORLD-FEATURES-ACTIVE-F-021-WORLD-PROJECT-ONBOARDING-JOURNAL-MD
title: F-021 world-project-onboarding
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-021-world-project-onboarding/journal.md
source_path: features/active/F-021-world-project-onboarding/journal.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

# F-021 world-project-onboarding

## LOOP 日志

### Iteration 0

1. 这轮做什么？
   - 创建 Feature Workspace。
2. 改了什么？
   - 初始化 feature.yaml、journal.md、evidence/、artifacts/。
3. 怎么验证？
   - 关闭前运行 gpcf_check_evidence.py。
4. 发现什么问题？
   - none
5. 是否可以提交？
   - 否，Evidence Gate 仍待验证。

### Iteration 1

1. 这轮做什么？
   - Builder 执行 runtime 调度。
2. 改了什么？
   - Builder -> Evaluator；status=evaluate
3. 怎么验证？
   - 22项目OpenSpec覆盖通过；技能链存在既有wae目录登记不一致
4. 发现什么问题？
   - 未发现调度阻塞项。
5. 是否可以提交？
   - 否，commit/push 仍需明确授权。

### Iteration 2

1. 这轮做什么？
   - 采集本地可回放证据。
2. 改了什么？
   - 更新 evidence 文件和 feature.yaml 证据状态。
3. 怎么验证？
   - 运行工作区 validator、py_compile、git diff --check 和范围证据门禁。
4. 发现什么问题？
   - Evidence checks passed；保留治理阻塞：既有中央文档门禁 rework_required
5. 是否可以提交？
   - 否。

## 本轮真实结果与授权澄清

用户明确授权并确认推荐的本地/私有远端建立方案，World 初始提交已同步。自动模板所写“commit/push仍需授权”不适用于本轮已授权范围。F-021证据检查通过，但中央文档与技能链存在既有阻塞，保留未关闭。

## 2026-10-18 阻塞复核

中央文档结构门禁现为 `pass`（复核债使状态上限仍为 `partial`），WAE 已按用户裁定纳入 24 项项目清单；这两条旧阻塞不再适用。只读证据检查仍返回 `close_candidate=false`：缺少 Feature 专属 tests/build 命令及范围特定的截图/API 豁免说明。World 总体方案的 Ontology 版本冲突尚未裁定，继续保持 `blocked`，不修改历史证据或提升纳管状态。
