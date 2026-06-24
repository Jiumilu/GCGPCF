---
doc_id: GPCF-DOC-C0F0BD428C
title: LOOP Round GPCF-KDS-DKS-040 - 湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-040.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-040.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-040 - 湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练

日期：2026-06-17  
轮次：`GPCF-KDS-DKS-040`  
模式：`LOOP / L1 文档治理`  
状态：`controlled_documentation`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-039`，使用虚拟脱敏样例演练空白执行台账和“底座可用知识闭环率”的判定效果，验证可有限引用、候选修复、退回补源、委员会触发和硬停止边界。

## 2. 输入文档

| 类型 | 路径 | 用途 |
|---|---|---|
| DKS-039 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批空白执行台账.md` | 提供空白执行台账和底座可用知识闭环率 |
| DKS-038 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材SOP候选写回规则到缺口悬赏与人工确认任务包.md` | 提供任务包对象来源 |
| 底座运行报告 | `GlobalCloud KDS/工业绿链/底座/99_底座运行报告.md` | 提供状态覆盖、DQ、写回队列和自动化初评口径 |
| 数据质量评分体系 | `GlobalCloud KDS/体系/data-governance/数据质量评分体系.md` | 提供 DQ 和一票否决边界 |
| 指挥舱取数契约 | `GlobalCloud KDS/工业绿链/底座/指挥舱取数契约.md` | 提供 RAG 与经营引用边界 |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 确认当前仍不得升级 accepted / integrated |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` | 确认 GFIS / GPCF 仍为 repair_required |

## 3. 输出文档

| 类型 | 路径 | 状态 |
|---|---|---|
| DKS-040 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md` | controlled |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-040.md` | controlled |

## 4. 本轮动作

| 动作 | 结果 |
|---|---|
| 建立虚拟样例集 | 已建立拓厂项目来源、行业权威来源、订单线索、越权收入 4 条虚拟样例 |
| 演练闭环率计算 | 已按六维权重计算虚拟闭环率 |
| 演练状态迁移 | 已形成 repair、limited report、blocked、committee trigger 四类判定 |
| 生成写回候选 | 已形成 4 条 `WBC-HBLC-*` 写回候选 |
| 演练悬赏边界 | 已明确不发布、不冻结、不结算、不分配 |
| 演练 RAG 与指挥舱边界 | 已明确有限报告不等于 RAG 强引用或经营强引用 |

## 5. 明确不做范围

本轮不做：

- 接收、保存或展示真实资料；
- 真实评分入账；
- 发布悬赏；
- 冻结积分、收益、AI 额度或其他资源；
- 积分结算；
- 收益分配；
- AI 额度发放；
- 委员会真实备案或裁决；
- Brain 页面正式发布；
- WAES 放行；
- 真实 KDS API 写入；
- GFIS、GPC、PVAOS 或其他业务系统主账写入；
- 生产配置、权限、部署、数据库迁移或外部系统写入；
- `accepted` 或 `integrated` 状态升级。

## 6. Evidence 计划

| 门禁 | 命令或检查 | 预期 |
|---|---|---|
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录全仓既有阻塞 |
| 差异格式 | `git diff --check -- 03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md docs/harness/loops/loop-round-GPCF-KDS-DKS-040.md` | pass |
| 禁止词扫描 | 对本轮两个新增文档执行禁止词扫描 | pass |

## 7. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| 文档控制 | pass | `tools/kds-sync/document_control.py` 已执行完成；主文档 doc_id=`GPCF-DOC-8454CB5BDD`，本轮 LOOP 记录 doc_id=`GPCF-DOC-C0F0BD428C` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；未写入 TOKEN 明文 |
| LOOP 文档门禁 | pass | `repo_md=859`; `kds_md=872`; `local_mirror_ledger_lines=859`; `api_sync_ledger_lines=60`; `missing_metadata=0`; `missing_readme_dirs=0` |
| LOOP 编排器文档门禁 | pass | `document_gate=pass`; `loop_governance_docs.gate=pass`; `kds_token_status.gate=pass` |
| 本轮差异格式 | pass | `git diff --check -- 03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md docs/harness/loops/loop-round-GPCF-KDS-DKS-040.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮两个新增文档未命中禁止旧口径、旧 AI 定位和真实性污染关键词 |
| 文档台账 | pass | `09-status/globalcloud-document-control-register.md` 已登记两个 doc_id |
| KDS 本地镜像 | pass | `.kds/local-mirror-ledger.jsonl` 已记录两个 `git_to_kds_local_mirror` 条目；同步状态为 `pending_api` |
| 全仓格式门禁 | partial | LOOP 编排器报告 `git_gate.gate=partial`，原因为工作区仍存在既有 dirty 状态；本轮新增文件 scoped diff check 通过 |
| 运行治理门禁 | blocked / rework | 仍受 `09-status/gpcf-project-status-matrix.md` 中 GFIS/GPCF `repair_required` 和既有阻塞信号影响；本轮不升级 `accepted` 或 `integrated` |

## 8. 风险与边界

| 风险 | 控制 |
|---|---|
| 虚拟样例被误认为真实资料 | 全文标记 `virtual_rehearsal_only` 和 `virtual_sample` |
| 闭环率被误认为业务完成度 | 明确只衡量治理与调用可用性 |
| 有限报告候选被误认为 RAG 强引用 | 单独列出 RAG 与指挥舱边界 |
| 悬赏候选被误认为已发布 | 明确不发布、不冻结、不结算、不分配 |
| 委员会触发被误认为裁决 | 只形成候选触发，不替代真实裁决 |

## 9. 下一轮建议

建议进入 `GPCF-KDS-DKS-041`：底座可用知识闭环率计算样表与字段字典。
