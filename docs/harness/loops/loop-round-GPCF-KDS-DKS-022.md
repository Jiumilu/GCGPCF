---
doc_id: GPCF-DOC-68D7099FB6
title: Loop Round GPCF-KDS-DKS-022
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-022.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-022.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-022

日期：2026-06-17  
状态：controlled  
主题：葛化、湖北磷材首批填报实例包与提交门禁  
项目群范围：GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC / 小即、XGD、XiaoG、MMC、GPCF。

## 1. 输入

1. 用户要求继续推进 GlobalCloud 项目群分布式 KDS 知识事实体系和绿色供应链试点落地。
2. `GPCF-KDS-DKS-021` 已形成葛化、湖北磷材试点样本表与 MMC 参数基线。
3. 本轮需要把样本表推进到首批可提交的候选实例包和提交门禁。
4. 本轮仍不得编造真实客户、供应商、订单、价格、POD、到账、金融凭证或生产事实。

## 2. 动作

1. 新增 `03-data-ai-knowledge/GlobalCloud葛化湖北磷材首批填报实例包与提交门禁.md`。
2. 定义葛化预运营期订单、辽宁远航链路补证和 GFIS AI 评分候选实例。
3. 定义湖北磷材拓厂来源、原料知识源和订单线索候选实例。
4. 定义 MMC 首批参数备案候选。
5. 定义提交包字段完整性检查、可见范围和本轮不处理范围。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| DKS-022 主实例包 | `03-data-ai-knowledge/GlobalCloud葛化湖北磷材首批填报实例包与提交门禁.md` | 首批候选实例骨架、提交门禁、可见范围和不处理范围 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-022.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py`；主实例包和本 Loop 记录已进入 `globalcloud-document-control-register.md` |
| KDS 本地开发空间镜像 | pass | 已镜像到 `开发/05-KDS/03-data-ai-knowledge/` 和 `开发/12-GPCF/docs/harness/loops/`；同步状态保持 `pending_api` |
| scoped git diff check | pass | 已对本轮触达文件运行 scoped `git diff --check`，无输出 |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass, repo_md=813, kds_md=826, missing_metadata=0, missing_readme_dirs=0` |
| 项目群 Loop 编排器 | partial | `document_gate=pass`；全局 `git_gate=rework_required` 源于既有多文件 EOF 空行问题，运营门禁仍受 GFIS/GPCF 既有修复态影响；本轮不得升级状态 |

## 5. 反馈

1. 本轮把 DKS-021 的样本表推进为首批候选实例骨架。
2. 本轮没有创建真实账号、没有配置生产权限、没有写生产数据、没有调用真实外部 API、没有确认真实积分或收益。
3. 本轮没有把候选实例写成真实业务事实，也没有把 KDS 本地镜像写成真实 KDS API 同步。
4. 下一阶段建议进入 `GPCF-KDS-DKS-023` 提交前审核清单与人工确认工作台。

## 6. Definition of Done

| 检查项 | 状态 |
|---|---|
| 葛化三类候选实例 | done |
| 湖北磷材三类候选实例 | done |
| MMC 三类参数备案候选 | done |
| 提交包字段完整性检查 | done |
| 可见范围和不处理范围 | done |
| 文档治理和 KDS 镜像 | done |
