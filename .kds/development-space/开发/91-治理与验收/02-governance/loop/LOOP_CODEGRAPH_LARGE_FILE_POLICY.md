---
doc_id: GPCF-DOC-622398264F
title: Loop CodeGraph Large File Policy
project: WAES
related_projects: [GFIS, GPC, WAES, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md
source_path: 02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop CodeGraph Large File Policy

## 目标

本政策用于处理 CodeGraph 在项目群中遇到的超大文件、生成型 validator、历史 harness 复制件或低信号文件导致的 residual notice。

它只定义代码图谱索引策略，不改变项目业务代码，不删除项目文件，不替代测试、源码复核、Harness/WAES 判定或人工验收。

## 适用条件

任一文件满足以下条件之一时，进入 `large_or_generated_file_review`：

| 条件 | 阈值 |
|---|---:|
| 文件大小 | `>= 1,000,000` bytes |
| 文件行数 | `>= 15,000` lines |
| 生成型 validator | `scripts/validate_*_sop_e2e.py`、`scripts/build_*_sop_e2e_*.py` 或同类批量生成脚本 |
| 历史嵌套副本 | `.harness/runs/**/project-copy/**` |
| 依赖或报告产物 | `node_modules/**`、HTML report bundle、trace/report generated assets |

## 状态分类

| 状态 | 含义 | 是否失败 |
|---|---|---|
| `indexed` | 文件已进入 CodeGraph `files` 表并可查询 | 否 |
| `ignored_by_policy` | 文件按明确策略被排除，不应进入索引 | 否 |
| `residual_pending_notice_explained` | CodeGraph 检测到 pending，但证据证明 `.codegraph` Git 保护有效，且候选为超大/生成型文件 | 否 |
| `indexing_failure_unexplained` | pending 无候选解释、`.codegraph` 污染 Git、或覆盖计数无法复核 | 是 |
| `requires_authorization` | 需要拆分、排除、删除、重构或修改项目仓文件 | 需人工确认 |

## 默认处理规则

1. 默认不修改项目仓业务代码。
2. 默认不删除、拆分或重构生成型 validator。
3. 默认不把 residual notice 写成业务代码图谱失败。
4. 必须记录候选文件路径、大小、行数、Git 状态、CodeGraph DB 命中状态和 `.codegraph` Git 状态。
5. 必须继续保留 `.codegraph/` 本地缓存不入 Git。
6. 只有用户明确授权时，才允许在项目仓内实施 `.codegraphignore`、生成目录排除、validator 拆分或生成器修复。
7. 若 residual notice 阻塞项目群监控，优先在 GPCF 证据中登记 `residual_pending_notice_explained`，而不是进入项目内部开发。

## GFIS 当前决策

GFIS `scripts/validate_gfis_runtime_sop_e2e.py` 当前被分类为：

```text
large_generated_validator_exception_candidate
```

判定依据：

| 证据 | 当前值 |
|---|---|
| 文件大小 | `1,589,665` bytes |
| 行数 | `17,784` |
| Git 状态 | tracked + modified |
| CodeGraph DB | 不在 `files` 表 |
| CodeGraph node lookup | `No indexed file matches` |
| GFIS `.codegraph` Git 状态 | `0` entries |
| GFIS CodeGraph pending | `Added: 1 files` |

当前处理决策：

```text
keep_residual_pending_notice_explained
```

不执行 GFIS 业务代码修改，不拆分该 validator，不删除该 validator，不新增 GFIS 项目排除规则，不升级 GFIS 或 GPCF 状态。

## 后续可选策略

| 选项 | 触发条件 | 授权要求 |
|---|---|---|
| 保持解释性 notice | 单仓、单文件、无 Git 污染、不会影响查询主路径 | 无需改项目仓 |
| GPCF 监控白名单 | 多轮稳定且证据完整 | 只改 GPCF 证据/validator |
| 项目级 CodeGraph 排除规则 | residual notice 干扰监控或多文件重复出现 | 需用户授权修改项目仓配置 |
| 拆分生成型 validator | 文件过大影响维护、review 或运行成本 | 需用户授权进入项目开发 |
| 修复生成器 | 多个生成脚本持续产生超大低信号文件 | 需用户授权进入项目开发 |

## 非声明

- 本政策不证明 GFIS runtime SOP E2E 已通过。
- 本政策不证明真实 source-of-record、运行层主键、review queue、runtime intake、WAES review 或 verified artifact 已完成。
- 本政策不授权 GFIS validator 重构、删除、拆分或项目排除规则修改。
- 本政策不授权提交、推送、部署、生产写入、真实外部 API 写入或状态升级。
