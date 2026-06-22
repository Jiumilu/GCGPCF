---
doc_id: GPCF-DOC-00E5F89359
title: Loop Round GPCF-KDS-DKS-021
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-021.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-021.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-021

日期：2026-06-17  
状态：controlled  
主题：葛化、湖北磷材试点样本表与 MMC 参数基线落地包  
项目群范围：GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC / 小即、XGD、XiaoG、MMC、GPCF。

## 1. 输入

1. 用户要求继续推进 GlobalCloud 项目群分布式 KDS 知识事实体系和绿色供应链试点落地。
2. `GPCF-KDS-DKS-018` 已完成葛化 GFIS 资料包入库验收与 AI 助手试运行任务书。
3. `GPCF-KDS-DKS-019` 已完成湖北磷材拓厂与新工厂复制试点任务书。
4. `GPCF-KDS-DKS-020` 已完成积分、收益、额度、悬赏、争议联动规则。
5. 本轮需要把上游规则转成可填报样本表、评分记录和 MMC 参数基线。

## 2. 动作

1. 新增 `03-data-ai-knowledge/GlobalCloud葛化湖北磷材试点样本表与MMC参数基线落地包.md`。
2. 定义葛化七类资料包样本表和三类 GFIS AI 输出评分记录样本位。
3. 定义湖北磷材拓厂评估样本表、原料 / 行业 / 订单知识源目录和新工厂复制模板记录。
4. 定义 MMC 权重、兑换系数、额度、冻结、扣减、可见范围和阈值参数基线。
5. 继续保留候选态、WAES 门禁、人工确认、委员会裁决和用户治理权边界。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| DKS-021 主落地包 | `03-data-ai-knowledge/GlobalCloud葛化湖北磷材试点样本表与MMC参数基线落地包.md` | 样本表、评分记录、拓厂评估、知识源目录、复制模板和 MMC 参数基线 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-021.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py`；主落地包和本 Loop 记录已进入 `globalcloud-document-control-register.md` |
| KDS 本地开发空间镜像 | pass | 已镜像到 `开发/05-KDS/03-data-ai-knowledge/` 和 `开发/12-GPCF/docs/harness/loops/`；同步状态保持 `pending_api` |
| scoped git diff check | pass | 已对本轮触达文件运行 scoped `git diff --check`，无输出 |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass, repo_md=809, kds_md=822, missing_metadata=0, missing_readme_dirs=0` |
| 项目群 Loop 编排器 | partial | `document_gate=pass`；全局 `git_gate=rework_required` 源于既有多文件 EOF 空行问题，运营门禁仍受 GFIS/GPCF 既有修复态影响；本轮不得升级状态 |

## 5. 反馈

1. 本轮把 DKS-018、DKS-019 和 DKS-020 的规则推进为可填报落地模板。
2. 本轮没有创建真实账号、没有配置生产权限、没有写生产数据、没有调用真实外部 API、没有发布真实悬赏、没有确认真实积分或收益。
3. 本轮不升级 accepted / integrated；GFIS 运行层 SOP E2E 未完成前，项目群仍应保持 partial / rework 边界。
4. 下一阶段建议进入 `GPCF-KDS-DKS-022` 首批填报实例包。

## 6. Definition of Done

| 检查项 | 状态 |
|---|---|
| 葛化样本表和评分记录 | done |
| 湖北磷材拓厂评估、知识源目录和复制模板 | done |
| MMC 参数基线 | done |
| KDS 11 池和增强账本挂接 | done |
| WAES / 人工 / 委员会 / 用户治理边界 | done |
| 文档治理和 KDS 镜像 | done |
