---
doc_id: GPCF-DOC-84E98967D1
title: Loop Round GPCF-KDS-DKS-023
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-023.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-023.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-023

日期：2026-06-17  
状态：controlled  
主题：葛化、湖北磷材提交前审核清单与人工确认工作台  
项目群范围：GFIS、GPC、WAES、KDS、MMC、GPCF。

## 1. 输入

1. 用户要求绿色供应链分布式知识系统纳入 LOOP 工程治理。
2. `GPCF-KDS-DKS-022` 已形成葛化、湖北磷材首批候选实例包与提交门禁。
3. 本轮需要把候选实例推进为提交前审核清单、人工确认工作台、WAES 规则记录、委员会备案和用户急停最小记录模板。
4. 本轮仍不得创建真实账号、配置生产权限、调用真实外部 API、写生产数据或确认业务收益。

## 2. 动作

1. 新增 `03-data-ai-knowledge/GlobalCloud葛化湖北磷材提交前审核清单与人工确认工作台.md`。
2. 定义 6 类候选实例的人工审核条目。
3. 定义 3 类 MMC 参数候选的提交前审核条目。
4. 明确 KDS 记录员、WAES 审核人、项目负责人、GFIS 操作员、财务联系人、委员会和用户治理代表的确认边界。
5. 建立退回路径、阻断路径、WAESRuleRecord、CommitteeFilingRecord、UserEmergencyStopRecord、HumanReviewDecision 和 `submitted` 状态迁移规则。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| DKS-023 主工作台 | `03-data-ai-knowledge/GlobalCloud葛化湖北磷材提交前审核清单与人工确认工作台.md` | 提交前审核清单、人工确认职责、退回路径、最小记录模板和状态迁移规则 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-023.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py`；主工作台 `GPCF-DOC-014389A572` 和本 Loop 记录 `GPCF-DOC-84E98967D1` 已进入 `globalcloud-document-control-register.md` |
| KDS 本地开发空间镜像 | pass | 已镜像到 `开发/05-KDS/03-data-ai-knowledge/` 和 `开发/12-GPCF/docs/harness/loops/`；同步状态保持 `pending_api` |
| scoped git diff check | pass | 已对本轮触达文件运行 scoped `git diff --check`，无输出 |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass, repo_md=819, kds_md=832, missing_metadata=0, missing_readme_dirs=0` |
| 项目群 Loop 编排器 | partial | `document_gate=pass`；全局 `git_gate=rework_required` 源于既有多文件 EOF 空行和同步计划空值尾随空格；运营门禁仍受既有 GFIS/GPCF 修复态影响；本轮不得升级状态 |

## 5. 反馈

1. 本轮把 DKS-022 的候选实例转成提交前人工审核工作台。
2. 本轮没有把候选实例写成真实业务事实，也没有把 KDS 本地镜像写成真实 KDS API 同步。
3. 本轮没有创建真实账号、没有配置生产权限、没有调用真实外部 API、没有确认真实积分或收益。
4. 下一阶段建议进入 `GPCF-KDS-DKS-024` 真实脱敏资料接收任务包与首批人工审核演练。

## 6. Definition of Done

| 检查项 | 状态 |
|---|---|
| 6 类候选实例审核清单 | done |
| 3 类 MMC 参数候选审核清单 | done |
| 人工确认角色与边界 | done |
| WAES / 委员会 / 用户急停 / 人工决策最小记录模板 | done |
| submitted 状态迁移规则 | done |
| 文档治理和 KDS 镜像 | done |
