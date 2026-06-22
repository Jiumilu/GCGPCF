---
doc_id: GPCF-DOC-B4456BFC1B
title: Loop Round GPCF-KDS-DKS-025
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-025.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-025.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-025

日期：2026-06-17  
状态：controlled  
主题：知识缺口悬赏与真实资料回收跟踪台账  
项目群范围：GFIS、GPC、WAES、KDS、MMC、GPCF。

## 1. 输入

1. 用户要求绿色供应链分布式知识系统纳入 LOOP 工程治理。
2. `GPCF-KDS-DKS-024` 已建立葛化和湖北磷材真实脱敏资料接收任务包，并将两个演练记录判定为 `returned_for_evidence`。
3. 葛化试点仍需围绕预运营期订单、辽宁远航链路、现代精工 OEM 过渡、质量、发货、POD 和金融凭证门禁继续补证。
4. 湖北磷材并行线当前重点是拓厂项目知识库、原料 / 行业 / 订单知识库和新工厂复制模板，不做 GFIS 深度运行。
5. 当前 GFIS/GPCF 仍为 `repair_required`，真实业务 source-of-record 和真实提交文件仍未取得。
6. 本轮仍不得创建真实账号、配置生产权限、调用真实外部 API、写生产数据、发布真实悬赏、确认积分或确认业务收益。

## 2. 动作

1. 新增 `03-data-ai-knowledge/GlobalCloud知识缺口悬赏与真实资料回收跟踪台账.md`。
2. 定义 KnowledgeGapRequest、RealSourceRecoveryTask、KnowledgeGapBountyCandidate、CandidateScoringRecord 和 GapClosureRecord。
3. 将 `RHR-GH-ORD-202606-0001` 转成 `KGR-GH-ORD-202606-0001`、`RRT-GH-ORD-202606-0001` 和 `KGB-GH-ORD-202606-0001`。
4. 将 `RHR-HBLC-FEA-202606-0001` 转成 `KGR-HBLC-FEA-202606-0001`、`RRT-HBLC-FEA-202606-0001` 和 `KGB-HBLC-FEA-202606-0001`。
5. 将辽宁远航既有链路缺口延续登记为 `KGR-GH-LY-202606-0001`、`RRT-GH-LY-202606-0001` 和 `KGB-GH-LY-202606-0001`。
6. 定义候选评分规则、状态机、可见性边界和 SOP 写回建议边界。
7. 明确本轮只形成候选和跟踪台账，不发布真实悬赏，不确认积分或收益，不写真实业务主账。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| DKS-025 主台账 | `03-data-ai-knowledge/GlobalCloud知识缺口悬赏与真实资料回收跟踪台账.md` | 知识缺口、真实资料回收任务、悬赏候选、候选评分、状态机和 SOP 写回边界 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-025.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py`；主台账 `GPCF-DOC-C60ECF8A71` 和本 Loop 记录 `GPCF-DOC-B4456BFC1B` 已进入 `globalcloud-document-control-register.md` |
| KDS 本地开发空间镜像 | pass | 已镜像到 `开发/05-KDS/03-data-ai-knowledge/` 和 `开发/12-GPCF/docs/harness/loops/`；同步状态保持 `pending_api` |
| scoped git diff check | pass | 已对本轮触达文件运行 scoped `git diff --check`，无输出 |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass, repo_md=823, kds_md=836, missing_metadata=0, missing_readme_dirs=0` |
| 项目群 Loop 编排器 | partial | `document_gate=pass`；全局 `git_gate=rework_required` 源于既有多文件 EOF 空行；运营门禁仍受 GFIS/GPCF 既有修复态影响；本轮不得升级状态 |

## 5. 反馈

1. 本轮把 DKS-024 的 `returned_for_evidence` 进一步推进为可跟踪的知识缺口和真实资料回收任务。
2. 本轮把葛化预运营期订单、湖北磷材拓厂项目来源和辽宁远航链路三个高优先级缺口纳入同一台账。
3. 本轮只形成 `candidate_only` 悬赏候选，没有冻结资源、发布悬赏、确认积分或确认收益。
4. 本轮没有接收真实未脱敏资料正文，没有创建真实账号，没有配置生产权限，没有调用真实外部 API，没有写业务主账。
5. 下一阶段建议进入 `GPCF-KDS-DKS-026` 首批资料回收包字段验收与候选 SOP 写回建议。

## 6. Definition of Done

| 检查项 | 状态 |
|---|---|
| 知识缺口对象字段 | done |
| 真实资料回收任务字段 | done |
| 悬赏候选字段 | done |
| 葛化预运营期订单缺口 | done |
| 湖北磷材拓厂项目来源缺口 | done |
| 辽宁远航链路缺口延续 | done |
| 候选评分规则 | done |
| 状态机和可见性边界 | done |
| SOP 写回建议边界 | done |
| 文档治理和 KDS 镜像 | done |
