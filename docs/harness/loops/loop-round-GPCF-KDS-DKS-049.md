---
doc_id: GPCF-DOC-79DFDC9D79
title: LOOP Round GPCF-KDS-DKS-049 - 葛化订单运行母版字段与单据映射
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-049.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-049.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-049 - 葛化订单运行母版字段与单据映射

日期：2026-06-19
轮次：`GPCF-KDS-DKS-049`
模式：`LOOP / L1 controlled documentation implementation`
状态：`controlled_documentation_increment`

## 1. 本轮输入

| 类型 | 路径 |
|---|---|
| AGENTS 规则 | `AGENTS.md` |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` |
| DKS-048 分析 | `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统当前实施分析与下一阶段推进.md` |
| DKS-048 LOOP | `docs/harness/loops/loop-round-GPCF-KDS-DKS-048.md` |
| 葛化三件套 | `03-data-ai-knowledge/GlobalCloud葛化第一阶段GFISAI助手三件套实施清单.md` |
| 本轮目标文档 | `03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md` |

## 2. 本轮目标

补齐葛化订单运行母版正文，形成可供 GFIS 使用助手、文档验收助手、候选事实驱动 SOP 和湖北磷材新工厂复制模板复用的受控字段与单据映射。

## 3. 本轮动作

1. 复核 DKS-048 的下一轮建议和 GFIS/GPCF 当前 `repair_required` 状态。
2. 确认目标文档仅有 frontmatter，缺少正文。
3. 补齐“预运营期订单”的对象链、统一编号、字段清单、状态机、GFIS 候选映射、底座 11 池挂接、RAG 准入和红线。
4. 明确目标工厂与 OEM 承接方同时记录但责任区分。
5. 明确收入、产值、潜在产值、知识积分、AI 额度和知识缺口悬赏的候选/确认边界。

## 4. 本轮输出

| 输出 | 路径 | 状态 |
|---|---|---|
| 葛化订单运行母版字段与单据映射专项清单 | `03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md` | controlled_master_draft |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-049.md` | controlled |

## 5. 本轮检查计划

| 门禁 | 命令或检查 | 预期 |
|---|---|---|
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录既有阻塞 |
| 本轮差异格式 | `git diff --check -- 03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md docs/harness/loops/loop-round-GPCF-KDS-DKS-049.md` | pass |

## 6. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| 文档控制 | pass | `python3 tools/kds-sync/document_control.py` 无错误输出；新增本轮 LOOP 记录并更新文档台账、KDS 同步台账和 `.kds/sync-ledger.jsonl` |
| KDS 本地镜像 | pass | `docs/harness/loops/loop-round-GPCF-KDS-DKS-049.md` 已镜像到 `.kds/development-space/开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-049.md` |
| 订单母版镜像 | pass | `document_control.py` 自动将订单母版归入 KDS 路径：`.kds/development-space/开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md`；旧 `90-跨项目架构` 镜像路径显示删除差异，属于归类迁移，不是源文件删除 |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；Token 未写入文档或 evidence |
| LOOP 文档门禁 | pass | `repo_md=1006`; `kds_md=1019`; `local_mirror_ledger_lines=1006`; `api_sync_ledger_lines=105`; `missing_metadata=0`; `missing_readme_dirs=0` |
| 本轮差异格式 | pass | scoped `git diff --check -- 03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md docs/harness/loops/loop-round-GPCF-KDS-DKS-049.md` 无输出 |
| LOOP 编排器 | partial | `document_gate=pass`; `kds_token_status=pass`; 全仓 `git_gate=rework_required` 来源于既有大量 Markdown EOF 空行差异；`operational_gates=blocked` 来源于 GFIS/GPCF 既有 `repair_required`、质量和客户满意阻断信号 |
| 状态升级 | not_allowed | 本轮仅补齐受控母版和 LOOP 记录，不升级 `accepted`、`complete` 或 `integrated` |

## 7. 风险与边界

| 风险 | 控制 |
|---|---|
| 把预运营期订单误写成正式订单 | 固定 `orderStage=pre_operation_candidate`，GFIS 写入模式默认为 no_write / candidate_only |
| 把 OEM 承接误写成目标工厂已投产 | 同时记录目标工厂和 OEM 承接方，但字段明确事实责任拆分 |
| 把开票统计误写成到账收入 | 正式收入以到账为准，开票只做统计和财务过程口径 |
| 把 AI SOP 建议误写成正式 SOP | `AIS-GH-SOP-*` 默认为 suggestion_only，需人工确认 |
| 把 KDS 本地镜像误写成真实 API 回执 | 本轮只做本地文档控制和镜像，不宣称真实 API 写入 |
| 把文档治理通过误写成业务完成 | GFIS/GPCF 保持 `repair_required`，不升级状态 |

## 8. 本轮不做范围

本轮不做：

- 真实 KDS API 写入；
- WAES 写入、放行或裁决；
- GFIS / GPC / PVAOS / Finance 主账写入；
- 真实订单、客户确认、质量放行、POD、到账、收益、积分或悬赏确认；
- 资料填报、人工确认或委员会裁决；
- RAG 强引用；
- 指挥舱强引用；
- `accepted`、`complete` 或 `integrated` 状态升级。

## 9. 下一轮建议

建议 `GPCF-KDS-DKS-050` 执行葛化 GFIS AI 助手三件套首批评测运行记录，输出：

1. `AssistantOutputRecord`。
2. `EvalRecord`。
3. `DefectRecord`。
4. `WritebackCandidate`。
5. 不写 GFIS 主账的候选写回边界复核。

## 10. 反馈

本轮把 DKS-048 识别出的关键缺口从“只有 frontmatter 的入口文件”推进为可引用的受控母版。母版已经能支撑下一轮三件套评测、辽宁远航链路补证、现代精工 OEM 责任拆分和湖北磷材新工厂复制差异分析。

本轮仍不证明真实资料已收到、真实评测已通过、GFIS 主账可写、WAES 已放行、RAG 可强引用或收益积分可结算。
