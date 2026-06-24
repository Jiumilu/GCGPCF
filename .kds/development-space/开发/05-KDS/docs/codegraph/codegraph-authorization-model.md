---
doc_id: GPCF-DOC-ACDBF80B37
title: CodeGraph 授权模型
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/codegraph/codegraph-authorization-model.md
source_path: docs/codegraph/codegraph-authorization-model.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 授权模型

CodeGraph 采用六层授权：

| 授权层 | 控制点 | 默认结论 |
|---|---|---|
| 工具级 | 读取、解析、建图、同步本地索引 | 允许只读和本地索引更新 |
| 仓库级 | include/exclude、敏感路径、风险等级 | 按项目 registry 执行 |
| Agent 级 | Codex、Review、Test、Doc、WAES、Loop Agent 权限差异 | 只读查询优先，写入需授权 |
| Loop 阶段级 | intake、planning、implementation、validation、evidence、closure | 按阶段限定查询能力 |
| KDS/OKF 级 | CodeGraph 输出事实状态 | 只能 candidate |
| WAES/人员级 | 高风险变更审批 | AI 不拥有最终批准权 |

权威配置文件：

- `governance/codegraph/agent-codegraph-permissions.yaml`
- `governance/codegraph/repo-codegraph-registry.yaml`
- `governance/codegraph/waes-codegraph-gates.yaml`
- `governance/codegraph/kds-codegraph-mapping.yaml`

任何偏离授权模型的动作必须进入 Harness evidence，并由 WAES 或人工角色确认。
