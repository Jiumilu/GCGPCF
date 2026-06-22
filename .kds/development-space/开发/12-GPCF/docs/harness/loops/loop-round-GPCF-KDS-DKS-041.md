---
doc_id: GPCF-DOC-4424900CA7
title: LOOP Round GPCF-KDS-DKS-041 - 底座可用知识闭环率计算样表与字段字典
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-041.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-041.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-041 - 底座可用知识闭环率计算样表与字段字典

日期：2026-06-17  
轮次：`GPCF-KDS-DKS-041`  
模式：`LOOP / L1 文档治理`  
状态：`controlled_documentation`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-040`，把“底座可用知识闭环率”沉淀为字段字典、计算样表、一票否决规则、RAG 与指挥舱调用门禁，并明确葛化、湖北磷材和后续工厂复制线的适用边界。

## 2. 输入文档

| 类型 | 路径 | 用途 |
|---|---|---|
| DKS-040 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md` | 提供虚拟样例和评分分层 |
| DKS-039 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批空白执行台账.md` | 提供指标公式和执行字段 |
| 数据质量评分体系 | `GlobalCloud KDS/体系/data-governance/数据质量评分体系.md` | 提供 DQ 与一票否决参考 |
| 指挥舱取数契约 | `GlobalCloud KDS/工业绿链/底座/指挥舱取数契约.md` | 提供 RAG 与经营引用边界 |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 确认当前仍不得升级 accepted / integrated |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` | 确认 GFIS / GPCF 仍为 repair_required |

## 3. 输出文档

| 类型 | 路径 | 状态 |
|---|---|---|
| DKS-041 主文档 | `03-data-ai-knowledge/GlobalCloud底座可用知识闭环率计算样表与字段字典.md` | controlled |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-041.md` | controlled |

## 4. 本轮动作

| 动作 | 结果 |
|---|---|
| 建立字段字典 | 已定义底座知识对象、六维评分、否决项、判定分层和允许用途字段 |
| 建立六维评分口径 | 已定义 100 / 70 / 50 / 0 分条件 |
| 建立一票否决规则 | 已覆盖无来源、AI 写事实、收入误认、订单误认、账本游离、敏感越界等 10 类 |
| 建立计算样表 | 已覆盖湖北磷材拓厂、行业、订单和葛化 GFIS 候选 |
| 建立调用门禁 | 已区分 RAG 强引用、有限报告、指挥舱强引用 |
| 建立适用边界 | 已明确葛化、湖北磷材和后续复制线的首批应用范围 |

## 5. 明确不做范围

本轮不做：

- 真实评分入账；
- 真实 RAG 准入；
- 指挥舱强引用；
- 缺口关闭；
- 悬赏发布；
- 积分结算；
- 收益分配；
- AI 额度发放；
- 委员会真实裁决；
- WAES 放行；
- 真实 KDS API 写入；
- GFIS、GPC、PVAOS 或其他业务系统主账写入；
- `accepted` 或 `integrated` 状态升级。

## 6. Evidence 计划

| 门禁 | 命令或检查 | 预期 |
|---|---|---|
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录全仓既有阻塞 |
| 差异格式 | `git diff --check -- 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率计算样表与字段字典.md docs/harness/loops/loop-round-GPCF-KDS-DKS-041.md` | pass |
| 禁止词扫描 | 对本轮两个新增文档执行禁止词扫描 | pass |

## 7. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| 文档控制 | pass | `tools/kds-sync/document_control.py` 已执行完成；主文档 doc_id=`GPCF-DOC-038B869EBF`，本轮 LOOP 记录 doc_id=`GPCF-DOC-4424900CA7` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；未写入 TOKEN 明文 |
| LOOP 文档门禁 | pass | `repo_md=861`; `kds_md=874`; `local_mirror_ledger_lines=861`; `api_sync_ledger_lines=61`; `missing_metadata=0`; `missing_readme_dirs=0` |
| LOOP 编排器文档门禁 | pass | `document_gate=pass`; `loop_governance_docs.gate=pass`; `kds_token_status.gate=pass` |
| 本轮差异格式 | pass | `git diff --check -- 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率计算样表与字段字典.md docs/harness/loops/loop-round-GPCF-KDS-DKS-041.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮两个新增文档未命中禁止旧口径、旧 AI 定位和真实性污染关键词 |
| 文档台账 | pass | `09-status/globalcloud-document-control-register.md` 已登记两个 doc_id |
| KDS 本地镜像 | pass | `.kds/local-mirror-ledger.jsonl` 已记录两个 `git_to_kds_local_mirror` 条目；同步状态为 `pending_api` |
| 全仓格式门禁 | partial | LOOP 编排器报告 `git_gate.gate=partial`，原因为工作区仍存在既有 dirty 状态；本轮新增文件 scoped diff check 通过 |
| 运行治理门禁 | blocked / rework | 仍受 `09-status/gpcf-project-status-matrix.md` 中 GFIS/GPCF `repair_required` 和既有阻塞信号影响；本轮不升级 `accepted` 或 `integrated` |

## 8. 风险与边界

| 风险 | 控制 |
|---|---|
| 总分被误认为事实完成 | 明确总分只是治理与调用可用性指标 |
| 分数抵消一票否决 | 明确一票否决优先于总分 |
| 有限报告候选被误认为 RAG 强引用 | 单独建立 RAG 与指挥舱调用门禁 |
| 增强账本脱离 KDS 11 池 | 明确增强账本必须挂接到底座池 |
| 字段字典被误用为真实写入接口 | 明确本文不是 API 写入记录或业务主账 |

## 9. 下一轮建议

建议进入 `GPCF-KDS-DKS-042`：底座可用知识闭环率评分脚本 dry-run 规格。
