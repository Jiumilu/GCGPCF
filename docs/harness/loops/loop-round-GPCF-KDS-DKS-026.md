---
doc_id: GPCF-DOC-16FCBF24B0
title: Loop Round GPCF-KDS-DKS-026
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-026.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-026.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-026

日期：2026-06-17  
状态：controlled  
主题：首批资料回收包字段验收与候选 SOP 写回建议  
项目群范围：GFIS、GPC、WAES、KDS、MMC、GPCF。

## 1. 输入

1. `GPCF-KDS-DKS-025` 已建立知识缺口悬赏与真实资料回收跟踪台账。
2. DKS-025 建议将 `RRT-GH-ORD-202606-0001`、`RRT-HBLC-FEA-202606-0001`、`RRT-GH-LY-202606-0001` 转成可填报回收包。
3. 葛化试点仍需围绕预运营期订单、辽宁远航链路、现代精工 OEM 过渡、质量、发货、POD 和金融凭证门禁继续补证。
4. 湖北磷材并行线当前重点仍是拓厂项目知识库、原料 / 行业 / 订单知识库和新工厂复制模板，不做 GFIS 深度运行。
5. 当前 GFIS/GPCF 仍为 `repair_required`，真实业务 source-of-record 和真实提交文件仍未取得。
6. 本轮仍不得创建真实账号、配置生产权限、调用真实外部 API、写生产数据、发布真实悬赏、确认积分或确认业务收益。

## 2. 动作

1. 新增 `03-data-ai-knowledge/GlobalCloud首批资料回收包字段验收与候选SOP写回建议.md`。
2. 将三条 RRT 转成 `RPK-GH-ORD-202606-0001`、`RPK-HBLC-FEA-202606-0001`、`RPK-GH-LY-202606-0001`。
3. 定义回收包公共字段、必填性、验收规则和禁止声明。
4. 建立字段级验收 checklist，区分 pass / partial / returned / blocked / disputed。
5. 输出候选 SOP 写回公共格式和三条 `SOPC` 候选建议。
6. 定义写回门禁、人工确认后关闭记录模板和 AI 助手使用边界。
7. 明确本轮只形成字段、验收和候选写回模板，不接收真实未脱敏资料，不写业务主账。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| DKS-026 主任务包 | `03-data-ai-knowledge/GlobalCloud首批资料回收包字段验收与候选SOP写回建议.md` | 首批回收包字段、字段验收 checklist、候选 SOP 写回格式、写回门禁和关闭记录模板 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-026.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py`；主任务包 `GPCF-DOC-B49150CE25` 和本 Loop 记录 `GPCF-DOC-16FCBF24B0` 已进入 `globalcloud-document-control-register.md` |
| KDS 本地开发空间镜像 | pass | 已镜像到 `开发/05-KDS/03-data-ai-knowledge/` 和 `开发/12-GPCF/docs/harness/loops/`；同步状态保持 `pending_api` |
| scoped git diff check | pass | 已对本轮触达文件运行 scoped `git diff --check`，无输出 |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass, repo_md=825, kds_md=838, missing_metadata=0, missing_readme_dirs=0` |
| 项目群 Loop 编排器 | partial | `document_gate=pass`；全局 `git_gate=rework_required` 源于既有多文件 EOF 空行；运营门禁仍受 GFIS/GPCF 既有修复态影响；本轮不得升级状态 |

## 5. 反馈

1. 本轮把 DKS-025 的三条真实资料回收任务推进为可填报回收包。
2. 本轮为葛化预运营期订单、湖北磷材拓厂项目来源和辽宁远航链路建立统一字段验收机制。
3. 本轮输出三条候选 SOP 写回建议，但全部保持 `candidate` 和 `blocked_until_confirmed`。
4. 本轮没有接收真实未脱敏资料正文，没有创建真实账号，没有配置生产权限，没有调用真实外部 API，没有写业务主账。
5. 下一阶段建议进入 `GPCF-KDS-DKS-027` 葛化 GFIS AI 助手内测问答与资料回收包联动规则。

## 6. Definition of Done

| 检查项 | 状态 |
|---|---|
| 三条 RRT 回收包字段 | done |
| 公共字段验收规则 | done |
| 字段级 checklist | done |
| 候选 SOP 写回公共格式 | done |
| 三条候选 SOP 建议 | done |
| 写回门禁 | done |
| 关闭记录模板 | done |
| AI 助手使用边界 | done |
| 文档治理和 KDS 镜像 | done |
