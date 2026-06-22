---
doc_id: GPCF-DOC-2E5C5639B8
title: LOOP Round GPCF-KDS-DKS-037 - 湖北磷材 Brain 知识页评审样例到 SOP 候选写回规则
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-037.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-037.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-037 - 湖北磷材 Brain 知识页评审样例到 SOP 候选写回规则

日期：2026-06-17  
轮次：`GPCF-KDS-DKS-037`  
模式：`LOOP / L1 文档治理`  
状态：`controlled_documentation`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-036`，将湖北磷材 Brain 知识页虚拟评审样例转成 SOP 候选写回规则，形成：

1. SOP 候选控制点。
2. 候选 KDS 字段写回规则。
3. 候选 WAES 规则写回记录。
4. Brain 页面候选状态规则。
5. 禁止写回清单。
6. 人工确认清单和回撤规则。

## 2. 输入文档

| 类型 | 路径 | 用途 |
|---|---|---|
| DKS-036 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选评审实例包与人工填报示例.md` | 提供三类虚拟评审样例和 AI 写回建议 |
| DKS-035 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选运行评审空白台账与发布前问题清单.md` | 提供评审台账、发布前问题、退回原因和悬赏候选边界 |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 确认当前仍为修复态和受控边界 |
| LOOP 自治政策 | `02-governance/loop/LOOP_AUTONOMY_POLICY.md` | 确认本轮为 L1 文档治理，不升级 L3/L4/L5 |
| 文档治理策略 | `.codex/skills/globalcloud-document-governance/references/document-control-policy.md` | 确认 frontmatter、KDS 本地镜像和 evidence 要求 |
| 防污染规则 | `.codex/skills/globalcloud-document-governance/references/anti-pollution-rules.md` | 防止把候选规则写成业务完成或真实系统写入 |

## 3. 输出文档

| 类型 | 路径 | 状态 |
|---|---|---|
| DKS-037 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页评审样例到SOP候选写回规则.md` | controlled |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-037.md` | controlled |

## 4. 本轮动作

| 动作 | 结果 |
|---|---|
| 抽取 DKS-036 三类样例 | 拓厂、行业资料、订单线索均被转成候选控制点 |
| 建立 SOPCandidateControlPoint | 已覆盖拓厂项目评审前、行业资料可信来源补证、订单线索收益边界 |
| 建立 CandidateKdsFieldWriteback | 已明确候选字段和禁止升级字段 |
| 建立 CandidateWaesRuleWriteback | 已明确发布边界、可信来源和收益边界规则候选 |
| 建立 BrainPageStatusCandidate | 已明确页面候选状态和可见范围 |
| 建立 ForbiddenWritebackList | 已禁止真实 KDS API 写入、WAES 放行、GFIS 主账、正式订单和收入等误写 |
| 建立 HumanConfirmationChecklist | 已明确来源、脱敏、KDS 池、WAES 规则、积分收益、权限等人工确认项 |
| 建立回撤与重评规则 | 已明确来源、脱敏、收益边界和 WAES 规则不适用时的回退动作 |

## 5. 明确不做范围

本轮不做：

- 真实 KDS API 写入；
- WAES 规则正式生效或放行；
- GFIS 主账、订单、生产、质量、发货、POD 或金融凭证写入；
- Brain 页面正式发布；
- 正式 SOP 生效；
- 积分、收益、悬赏、潜在产值的正式确认或分配；
- 开票、到账收入或正式财务确认；
- 生产配置、权限、部署、数据库迁移或外部系统写入；
- `accepted` 或 `integrated` 状态升级。

## 6. Evidence 计划

| 门禁 | 命令或检查 | 预期 |
|---|---|---|
| 文档控制 | `python3 .codex/skills/globalcloud-document-governance/scripts/document_control.py` | pass |
| 文档污染 | `python3 .codex/skills/globalcloud-document-governance/scripts/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass |
| 差异格式 | `git diff --check -- 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页评审样例到SOP候选写回规则.md docs/harness/loops/loop-round-GPCF-KDS-DKS-037.md` | pass |
| 禁止词扫描 | 对本轮两个新增文档执行禁止词扫描 | pass |

## 7. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| 文档控制 | pass | `tools/kds-sync/document_control.py` 已执行完成；主文档 doc_id=`GPCF-DOC-312B5F9215`，本轮 LOOP 记录 doc_id=`GPCF-DOC-2E5C5639B8` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；未写入 TOKEN 明文 |
| LOOP 文档门禁 | pass | `repo_md=850`; `kds_md=863`; `local_mirror_ledger_lines=850`; `api_sync_ledger_lines=56`; `missing_metadata=0`; `missing_readme_dirs=0` |
| LOOP 编排器文档门禁 | pass | `document_gate=pass`; `loop_governance_docs.gate=pass`; `kds_token_status.gate=pass` |
| 本轮差异格式 | pass | `git diff --check -- 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页评审样例到SOP候选写回规则.md docs/harness/loops/loop-round-GPCF-KDS-DKS-037.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮两个新增文档未命中禁止旧口径、旧 AI 定位和真实性污染关键词 |
| 文档台账 | pass | `09-status/globalcloud-document-control-register.md` 已登记两个 doc_id |
| KDS 本地镜像 | pass | `.kds/local-mirror-ledger.jsonl` 已记录两个 `git_to_kds_local_mirror` 条目；同步状态为 `pending_api` |
| 全仓格式门禁 | rework_required | LOOP 编排器仍报告历史 `.md` 文件存在 `new blank line at EOF`；本轮不处理历史格式债务，不将其写成本轮新增文件失败 |
| 运行治理门禁 | blocked / rework | 仍受 `09-status/gpcf-project-status-matrix.md` 中 GFIS/GPCF `repair_required` 和既有阻塞信号影响；本轮不升级 `accepted` 或 `integrated` |

## 8. 风险与边界

| 风险 | 控制 |
|---|---|
| 候选写回被误认为真实写入 | 主文档和本记录均使用 candidate、record、returned 等状态，不写真实完成 |
| 订单线索被误认为收入 | 正式收入按到账确认；开票只作为统计、财务和流程口径 |
| 增强账本游离于 KDS 底座 | 积分、收益、额度、悬赏、争议、潜在产值、SOP、贡献等增强账本必须挂接 KDS 11 池 |
| 行业资料可信层级误升 | 缺权威来源、检索时间或适用范围时保持退回 |
| 跨单位权限污染 | 页面可见范围和跨单位共享必须人工确认 |

## 9. 下一轮建议

建议进入 `GPCF-KDS-DKS-038`：湖北磷材 SOP 候选写回规则到缺口悬赏与人工确认任务包。
