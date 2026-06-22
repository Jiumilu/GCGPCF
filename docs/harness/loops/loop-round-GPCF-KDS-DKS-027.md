---
doc_id: GPCF-DOC-F53170657E
title: LOOP Round GPCF-KDS-DKS-027 - 葛化 GFIS AI 助手内测问答与资料回收包联动规则
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-027.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-027.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-027 - 葛化 GFIS AI 助手内测问答与资料回收包联动规则

## 1. 轮次目标

在 DKS-025 知识缺口/悬赏机制与 DKS-026 资料回收包/候选 SOP 的基础上，建立葛化第一阶段三类 GFIS AI 助手的内测联动规则，使问答、使用引导、文档验收能够回流到资料回收包、候选 SOP、KDS 11 底座池与 WAES/人工/委员会门禁。

## 2. 输入

- `03-data-ai-knowledge/GlobalCloud知识缺口悬赏与真实资料回收跟踪台账.md`
- `03-data-ai-knowledge/GlobalCloud首批资料回收包字段验收与候选SOP写回建议.md`
- `03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录模板.md`
- `03-data-ai-knowledge/GlobalCloud葛化GFISAI助手首批问答与文档验收评测集.md`
- `02-governance/loop/LOOP_CONTROL_BOARD.md`
- `09-status/gpcf-project-status-matrix.md`

## 3. 输出

- `03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测问答与资料回收包联动规则.md`

## 4. 关键规则

- 本轮只建立候选联动规则，不确认真实上线、真实资料、真实写回、正式积分或正式收益。
- GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手均只能输出候选事实、候选 SOP、候选资料验收、候选贡献事件。
- KDS 11 底座池是事实基础，积分池、收益池、额度池、悬赏池、争议池、潜在产值池、SOP 账本、贡献账本均为增强账本。
- WAES 在规则内记录，在规则外或重大事项中触发复核；最终确认由人工或委员会完成。
- 有实际收入的事项才可进入正式产值贡献；到账为正式收入口径，开票为统计和财务过程口径。

## 5. 本轮动作

| 动作 | 结果 |
|---|---|
| 建立 GFIS 三类助手与 RPK/KGR/SOPC 的映射 | done |
| 建立内测问答到资料回收包联动结构 | done |
| 建立写回候选与缺口回流结构 | done |
| 明确 KDS 11 底座池挂接规则 | done |
| 明确 WAES/人工/委员会门禁边界 | done |
| 执行文档控制与 KDS 本地镜像检查 | done |
| 执行防污染、TOKEN、LOOP 文档门禁检查 | done |

## 6. 证据

### 6.1 文档控制

已执行：`python3 tools/kds-sync/document_control.py`。

结果：

- 主文档 doc_id：`GPCF-DOC-1CF8B46A53`；
- LOOP 记录 doc_id：`GPCF-DOC-F53170657E`；
- 主文档本地镜像：`开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测问答与资料回收包联动规则.md`；
- LOOP 记录本地镜像：`开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-027.md`；
- API 同步状态：`pending_api`，未执行真实 KDS API 写入。

### 6.2 防污染检查

已执行：`python3 tools/kds-sync/check_document_pollution.py`。

结果：`document_pollution=pass`。

### 6.3 KDS TOKEN 检查

已执行：`python3 tools/kds-sync/validate_kds_token.py`。

结果：`kds_token=pass fingerprint=bfd9553d`。

### 6.4 LOOP 文档门禁

已执行：`python3 tools/kds-sync/loop_document_gate.py`。

结果：

- `gate=pass`；
- `repo_md=831`；
- `kds_md=844`；
- `local_mirror_ledger_lines=831`；
- `api_sync_ledger_lines=50`；
- `missing_metadata=0`；
- `missing_readme_dirs=0`。

### 6.5 scoped git diff 检查

已执行两类检查：

- DKS-027 主文档、LOOP 记录、`document_control.py` 精准 scoped 检查：pass；
- 包含整个 `.kds/development-space` 的扩展检查：fail，原因为历史镜像与历史源文档存在 `new blank line at EOF`，不属于 DKS-027 新增规则内容。

### 6.6 LOOP 编排器

已执行：`python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py`。

结果：

- `loop_governance_docs.gate=pass`；
- `kds_token_status.gate=pass`；
- 全局 `git_gate=rework_required`，原因为历史 EOF 差异；
- 全局 `operational_gates=blocked`，原因为 GFIS/GPCF 运行层修复状态仍未关闭；
- 本轮不升级为 accepted 或 integrated。

## 7. 完成状态

当前状态：controlled evidence complete for DKS-027。

本轮完成后仍不得升级为 accepted 或 integrated。GFIS/GPCF 运行层修复与真实系统接入仍需后续 LOOP 轮次处理。

## 8. 下一轮建议

DKS-028 建议进入“葛化 GFIS AI 助手首批问答与文档验收评测集实化”，将现有评测集补齐为可执行样本，并继续保持候选事实、候选 SOP、候选积分与人工确认边界。
