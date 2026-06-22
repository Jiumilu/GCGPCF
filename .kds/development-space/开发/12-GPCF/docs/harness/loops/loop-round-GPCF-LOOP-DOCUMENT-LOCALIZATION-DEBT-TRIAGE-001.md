---
doc_id: GPCF-DOC-EDD3670D2E
title: Loop Round GPCF-LOOP-DOCUMENT-LOCALIZATION-DEBT-TRIAGE-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-LOOP-DOCUMENT-LOCALIZATION-DEBT-TRIAGE-001.md
source_path: docs/harness/loops/loop-round-GPCF-LOOP-DOCUMENT-LOCALIZATION-DEBT-TRIAGE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-LOOP-DOCUMENT-LOCALIZATION-DEBT-TRIAGE-001

## 输入

- 上轮输出：`GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005`。
- 独立阻塞项：`GPCF-LOOP-DOCUMENT-LOCALIZATION-DEBT-TRIAGE`。
- 当前门禁：`loop_document_gate.py --check-only` 返回 `rework_required`，原因包含 `localization_debt=true`。

## 目标

对中文化债务做分桶和治理排序，形成下一轮可执行范围。当前轮不批量翻译历史文档，不改变业务状态，不升级 accepted / integrated / production_ready。

## 动作

- 刷新 `check_chinese_localization_gate.py --json --write-report`。
- 保留 `09-status/globalcloud-chinese-localization-governance-report.md` 作为当前债务快照。
- 建立 triage 证据，区分当前有效治理文档、历史证据、模板和软件用户可见文本。
- 明确下一轮只处理高优先级、低风险、当前有效的文档债务。

## 输出

- `09-status/globalcloud-chinese-localization-governance-report.md`
- `docs/harness/evidence/loop-document-localization-debt-triage-20260622.md`

## 检查

- 中文化门禁仍允许返回 `fail`，但必须有受控报告。
- 污染检查必须通过。
- TOKEN 检查必须通过。
- KDS 冲突保护必须通过。
- 不得把本轮 triage 写成债务清零。

## 反馈

本轮状态为 `triage_controlled_rework_required`。当前债务快照显示中文化门禁仍为 `fail`，问题总数为 367。下一轮应优先处理：

1. 当前有效治理文档中的英文重句。
2. 当前 Loop/Harness 活跃轮次中的英文重句。
3. 软件用户可见文本中的英文字符串。

历史归档和长文件名型 evidence 标题只做登记，不在下一轮批量改写。

## 非声明

- 不声明中文化债务已清零。
- 不声明 Loop 文档门禁已恢复 `pass`。
- 不声明历史归档已全部中文化。
- 不声明业务系统、生产系统、真实 KDS API 或外部 API 已写入。

## 下一轮

`GPCF-LOOP-DOCUMENT-LOCALIZATION-DEBT-REPAIR-002`
