---
doc_id: GPCF-DOC-8A341D2005
title: LOOP Round GPCF-KDS-DKS-031 - 湖北磷材拓厂评估与知识源评测集
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-031.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-031.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-031 - 湖北磷材拓厂评估与知识源评测集

## 1. 轮次目标

在 DKS-030 已建立湖北磷材 FEA、RAW、IND、ORD、TPL 五类知识对象空白台账的基础上，建立首批评测集，明确评分维度、红线清单、样本索引、预期输出、缺口回流、写回候选和通过条件。

## 2. 输入

- `03-data-ai-knowledge/GlobalCloud湖北磷材首批知识对象运行空白台账.md`
- `03-data-ai-knowledge/GlobalCloud湖北磷材拓厂项目知识库与新工厂复制模板.md`
- `03-data-ai-knowledge/GlobalCloud葛化湖北磷材首批填报实例包与提交门禁.md`
- `02-governance/loop/LOOP_CONTROL_BOARD.md`
- `09-status/gpcf-project-status-matrix.md`

## 3. 输出

- `03-data-ai-knowledge/GlobalCloud湖北磷材拓厂评估与知识源评测集.md`

## 4. 本轮动作

| 动作 | 结果 |
|---|---|
| 建立湖北磷材评测总规则 | done |
| 建立五维 100 分评分规则 | done |
| 建立 `RED-HBLC-*` 红线清单 | done |
| 建立 FEA / RAW / IND / ORD / TPL / MIX 样本索引 | done |
| 建立缺口与悬赏回流候选 | done |
| 建立 KDS / WAES / Brain 写回候选矩阵 | done |
| 建立通过条件与下一轮建议 | done |
| 执行文档控制与门禁检查 | done |

## 5. 边界

- 本轮只建立评测集，不执行真实评测。
- 不执行真实资料接收，不进行网络检索，不确认权威政策或标准适用。
- 不确认真实拓厂评估、投资、合作、订单、原料采购、合同、POD、到账或收益。
- 不启动 GFIS 深度运行，不写 GFIS/GCFIS 主账。
- 不创建真实账号、不配置生产权限、不写生产数据、不调用真实外部 API。
- 不写真实 KDS API，不写真实 WAES API。
- 不确认正式积分、收益、额度、悬赏、争议或 SOP 生效。
- 不升级 accepted 或 integrated。

## 6. 证据

### 6.1 文档控制

已执行：

- `/Users/lujunxiang/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/kds-sync/document_control.py`

结果：

- 湖北磷材评测集已受控，doc_id=`GPCF-DOC-7B1983E735`。
- 本轮 LOOP 记录已受控，doc_id=`GPCF-DOC-8A341D2005`。
- 湖北磷材评测集纳入本地 KDS 镜像：`.kds/development-space/开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材拓厂评估与知识源评测集.md`。
- 本轮 LOOP 记录纳入本地 KDS 镜像：`.kds/development-space/开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-031.md`。
- API 同步状态保持 `pending_api`，本轮未执行真实 KDS API 写入。

### 6.2 防污染检查

已执行：`check_document_pollution.py`。

结果：`document_pollution=pass`。

### 6.3 KDS TOKEN 检查

已执行：`validate_kds_token.py`。

结果：`kds_token=pass fingerprint=bfd9553d`。

### 6.4 LOOP 文档门禁

已执行：`loop_document_gate.py`。

结果：

- `gate=pass`
- `repo_md=838`
- `kds_md=851`
- `local_mirror_ledger_lines=838`
- `api_sync_ledger_lines=56`
- `missing_metadata=0`
- `missing_readme_dirs=0`

### 6.5 scoped git diff 检查

已执行：DKS-031 评测集与 LOOP 记录 scoped `git diff --check`。

结果：pass，无输出。

### 6.6 LOOP 编排器

已执行：`.codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py`。

结果：

- `document_gate=pass`
- `loop_governance_docs.gate=pass`
- `kds_token_status.gate=pass`
- `git_gate.gate=rework_required`，原因是全仓历史 EOF 空行 diff_check 失败；DKS-031 scoped diff 已通过。
- `operational_gates.gate=blocked`，原因是 GFIS/GPCF 仍处于 `repair_required` 主线修复状态；本轮不升级 accepted/integrated。
- recommendation=`continue`

## 7. DKS-031 完成定义

本轮完成条件：

1. 湖北磷材评测集建立并受控。
2. 评测集覆盖 FEA、RAW、IND、ORD、TPL 和综合挂接样本。
3. 评分维度、红线、预期输出、缺口回流、写回候选和通过条件完整。
4. 所有样本保持 planned 状态，不生成真实评测结果。
5. 纳入本地 KDS 镜像与 LOOP 轮次记录。
6. 通过防污染、TOKEN、文档门禁和 scoped diff 检查。

## 8. 下一轮建议

DKS-032 建议进入“湖北磷材评测运行记录首批空白台账”，将本文样本转为可填报运行记录，覆盖输入摘要、输出摘要、可信级别、人工评分、红线缺陷、缺口悬赏、写回候选和贡献候选。
