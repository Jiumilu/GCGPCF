---
doc_id: GPCF-DOC-F150434D98
title: GlobalCloud 项目群文档与软件中文化治理规范
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群文档与软件中文化治理规范.md
source_path: 02-governance/GlobalCloud项目群文档与软件中文化治理规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群文档与软件中文化治理规范

## 目标

本规范把“文档全面中文化”和“软件中文化治理”纳入 Loop Engineering 门禁，避免项目群在自动化实施、证据归档、脚本生成、界面交付和 KDS 同步过程中继续产生未受控英文材料。

## 适用范围

- GPCF 仓库内当前有效、草案、运行类和状态类 Markdown 文档。
- Loop 工程生成的轮次文档、证据索引、状态报告、治理看板和 KDS 同步台账。
- `packages/`、`scripts/`、`fixtures/` 中可能面向用户、运营、审计或验收人员展示的软件文案、接口消息、报告字段和样例数据。
- 其它项目仓库在纳入 GPCF/KDS 开发空间前，必须按本规范完成中文化自检。

## 中文化要求

| 对象 | 要求 | 允许保留 |
| --- | --- | --- |
| 文档标题、摘要、结论、验收口径 | 必须使用中文，英文只能作为括号内补充或技术名词 | 项目代号、产品代号、协议名、API 名称 |
| Loop 轮次记录 | 输入、动作、证据、结论、阻塞、下一步必须中文表达 | 文件路径、命令、状态枚举 |
| 软件界面文案 | 用户可见按钮、提示、菜单、空状态、错误信息必须中文优先 | 标准错误码、开发者日志级别 |
| 报告和 fixture | 业务含义、验收结论、审计说明必须中文 | JSON key、协议字段、测试编号 |
| 脚本输出 | 面向治理/验收的输出必须中文或中英双语，且中文在前 | CLI 参数名、机器可解析字段 |

## 门禁接入

中文化门禁脚本为：

```bash
python3 tools/kds-sync/check_chinese_localization_gate.py
```

该脚本纳入 `tools/kds-sync/loop_document_gate.py` 的硬检查项。发现英文重度文档或疑似英文用户可见软件文案时，Loop 文档门禁不得判定为 `pass`，本轮状态最高为 `rework_required`，除非该项被明确登记为受控债务且状态不高于 `partial`。

## 治理流程

1. 每轮 Loop 结束前运行中文化门禁。
2. 对门禁输出按项目、目录、文档类型和软件表面分类。
3. 对新产生文件要求本轮修正；对历史存量文件建立治理清单，不得在未修正时作为完成证据。
4. 翻译不得改变业务状态、证据结论、接口契约、对象 ID、哈希、路径或命令。
5. 完成修正后重新运行中文化门禁、文档污染检查、KDS Token 检查和 Loop 文档门禁。

## 状态规则

- `pass`：无英文重度文档，无疑似英文用户可见软件文案。
- `rework_required`：本轮新增或修改内容触发中文化门禁。
- `partial`：只剩历史存量债务，且已有明确责任、范围和计划。
- `blocked`：中文化修正需要外部项目仓库、真实产品确认或 KDS 权限但当前不可执行。

## 不视为违规的内容

- `KDS`、`API`、`Loop`、`OKF`、`WAES`、`GFIS` 等项目或技术专名。
- 文件路径、命令、环境变量、状态枚举、数据库字段、JSON key。
- 引用外部协议、库名、包名、错误码、版本号。
- 历史归档中为了审计必须保留的原文，但不得把归档原文重新作为当前有效规范。
