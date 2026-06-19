---
doc_id: GPCF-DOC-B15126F708
title: KDS Markdown 化与 OKF 兼容层全面实施闭环方案
project: GPCF
related_projects: [GPC, WAES, KDS, Brain, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/kds-md-okf-implementation-closure-plan.md
source_path: 09-status/kds-md-okf-implementation-closure-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# KDS Markdown 化与 OKF 兼容层全面实施闭环方案

日期：2026-06-17

用途：作为 GlobalCloud 项目群推进 KDS 导入文档 Markdown 化、KDS 开发空间一致性收敛、OKF 兼容层试点和 Loop 文档治理闭环的执行控制面。

## 当前阶段判定

当前状态：`ready_for_baseline_reconciliation`

不得判定为：`ready_for_full_rollout`

理由：

- Git 源 Markdown 受控化已基本成熟，当前非 `.kds` 源文档无缺失 frontmatter。
- 污染检查、KDS TOKEN 检查和 Loop 文档门禁通过。
- `kds_conflict_guard.py` 当前仍阻塞，源文档与 KDS 本地镜像存在不一致。
- 真实 KDS 远端仍存在登记文档未匹配项，不能宣称全量同步完成。
- 当前 worktree 存在大量已修改和未跟踪文件，必须先分组、冻结、审计，再执行全量重写类工具。

## Phase 0 基线审计证据

本轮只执行非破坏性检查，不运行会全量重写台账和 `.kds` 镜像的 `document_control.py`。

已执行门禁：

| gate | result | evidence |
| --- | --- | --- |
| 文档污染检查 | pass | `python3 tools/kds-sync/check_document_pollution.py` |
| KDS TOKEN 检查 | pass | `python3 tools/kds-sync/validate_kds_token.py`，仅记录指纹，不记录 TOKEN |
| Loop 文档门禁 | pass | `python3 tools/kds-sync/loop_document_gate.py` |
| KDS 本地镜像冲突检查 | blocked | `09-status/globalcloud-document-health-report.md` 与 KDS 本地镜像不一致 |

当前已知阻塞：

| id | blocker | impact | required disposition |
| --- | --- | --- | --- |
| B-001 | `kds_conflict_guard.py` blocked | 阻止真实 KDS 同步计划和全量 OKF 生成放行 | 在保护用户 worktree 的前提下确认源文档与镜像的权威侧，再刷新镜像或登记债务 |
| B-002 | worktree 大量 dirty/untracked | 阻止全量 `document_control.py` 安全执行 | 对 `.kds`、`docs/harness/loops`、工具脚本、状态台账和业务文档分组 |
| B-003 | 真实 KDS 远端存在缺失匹配 | 阻止宣称 KDS 全量闭环成熟 | 重新运行只读探测，逐项标记 sync、skip、archive 或 debt |

最新 `kds_conflict_guard.py` 已知不一致项：

| source_path | kds_mirror_path |
| --- | --- |
| `02-governance/loop/LOOP_CONTROL_BOARD.md` | `开发/91-治理与验收/02-governance/loop/LOOP_CONTROL_BOARD.md` |
| `02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md` | `开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md` |
| `02-governance/loop/README.md` | `开发/91-治理与验收/02-governance/loop/README.md` |
| `09-status/globalcloud-document-health-report.md` | `开发/91-治理与验收/09-status/globalcloud-document-health-report.md` |
| `docs/harness/evidence/README.md` | `开发/05-KDS/docs/harness/evidence/README.md` |
| `docs/harness/evidence/evidence-index.md` | `开发/12-GPCF/docs/harness/evidence/evidence-index.md` |
| `docs/harness/evidence/loop-governance-dashboard-20260617.md` | `开发/05-KDS/docs/harness/evidence/loop-governance-dashboard-20260617.md` |
| `docs/harness/loop-state.md` | `开发/12-GPCF/docs/harness/loop-state.md` |

## Phase 1 导入文档 Markdown 化准入

所有导入文档先进入准入队列，不得直接变更为 `controlled`。

每个导入文档必须具备：

| field | requirement |
| --- | --- |
| source_uri | 原始来源路径、URL 或 KDS 原始记录 |
| source_hash | 原始内容 hash |
| markdown_hash | Markdown 化后内容 hash |
| conversion_method | 转换工具、人工整理或混合方式 |
| conversion_actor | 执行者或工具角色 |
| doc_id | 按 `source_path` 可复算的文档 ID |
| source_path | Git 源路径 |
| kds_path | KDS `开发` 空间目标路径 |
| owner | 责任项目或责任人 |
| status | `imported_raw`、`draft`、`controlled`、`archive`、`deprecated` 或 `superseded` |
| citations | 原始依据、外部链接或受控文档引用 |
| sensitivity_check | TOKEN、账号、客户敏感信息和业务秘密检查结果 |

建议状态流转：

```text
raw_source
→ imported_raw
→ draft
→ controlled
```

异常分支：

```text
imported_raw → archive
draft → deprecated
controlled → superseded
```

## Phase 2 KDS 三层一致性闭环

三层对象：

1. Git 源文档。
2. `.kds/development-space/开发` 本地镜像。
3. 真实 KDS `开发` 远端空间。

放行顺序：

```bash
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
python3 tools/kds-sync/kds_conflict_guard.py
python3 tools/kds-sync/kds_readonly_probe.py
python3 tools/kds-sync/kds_sync_plan.py --require-clean-plan
```

只有同步计划为 clean plan 且人工确认写入窗口后，才能执行：

```bash
python3 tools/kds-sync/kds_sync_apply.py --confirm-development-space --max-writes 25
```

执行写入后必须检查：

- `.kds/sync-ledger.jsonl` 已追加审计流水。
- 不包含 TOKEN 明文。
- `kds_readonly_probe.py` 重新探测后缺失数减少或归零。
- 未把 KDS 本地镜像误写为真实 API 已同步。

## Phase 3 OKF 兼容层试点

OKF 兼容层只作为 Agent 导航和交换层，不替代 KDS、Git 或文档控制台账。

首批 bundle：

| bundle | scope | rollout rule |
| --- | --- | --- |
| governance-bundle | 文档治理、Loop、Harness、状态机、门禁 | 只读索引，不复制正文 |
| architecture-bundle | 项目群总架构、主线对齐、跨项目架构 | 只链接受控源文档 |
| kds-bundle | KDS 同步、安全、镜像和导入规则 | 必须引用同步台账与安全规则 |

Agent 读取顺序：

```text
.okf/index.md
→ bundle/index.md
→ concept
→ source_path 原始受控文档
→ 09-status/* 台账校验
```

禁止事项：

- 不得把 OKF 摘要当最终事实。
- 不得把 OKF 生成视为业务完成。
- 不得让 Brain 替代 KDS 主存。
- 不得把 KDS 本地镜像写成真实 KDS API 已同步。

## Phase 4 Loop 纳入闭环

每轮 Loop 至少保留：

- 本轮输入文档列表。
- 本轮输出文档列表。
- 文档控制检查结果。
- KDS 同步检查结果。
- 污染检查结果。
- KDS TOKEN 检查结果。
- 如有文档债务，必须列明 `due_loop` 和 `max_status`。

状态门禁：

| condition | max_status |
| --- | --- |
| 无文档记录 | below `evidence_ready` |
| 有文档债务 | `partial` |
| KDS 同步失败 | `partial` 或 `blocked` |
| 污染检查失败 | `rework_required` |
| TOKEN 检查失败 | `blocked` |

## 第一阶段执行准备清单

| item | status | next action |
| --- | --- | --- |
| 当前 dirty worktree 分组 | open | 生成按目录、状态、风险等级分组的变更清单 |
| 健康报告源/镜像不一致 | open | 确认权威侧并刷新派生镜像，或登记文档债务 |
| 真实 KDS missing remote 清单 | open | 重新运行只读探测并生成处置表 |
| MD 化准入字段 | proposed | 后续固化为导入验收矩阵 |
| OKF bundle 范围 | proposed | 等三层一致性通过后创建只读索引 |

## 全量放行标准

全面实施前必须同时满足：

1. `kds_conflict_guard=pass`。
2. `document_pollution=pass`。
3. `kds_token=pass`。
4. `loop_document_gate=pass`。
5. `kds_sync_plan.py --require-clean-plan` 通过。
6. 真实 KDS missing remote 为 0，或每条都有 `skip_reason`、`archive_reason` 或 `doc_debt`。
7. 导入文档均具备原始来源、hash、转换记录和敏感信息检查。
8. OKF 兼容层先完成只读试点，不直接全量复制正文。

## 当前结论

KDS Markdown 化与 OKF 兼容层已完成受控实施闭环的第一轮收敛：

- KDS 真实远端写入已按 `--max-writes 25` 小批量执行，并写入 `.kds/sync-ledger.jsonl`。
- KDS 三层一致性同步计划已收敛为 `create=0`、`update=0`、`conflicts=0`、`missing_local=0`。
- `09-status/kds-development-space-sync-plan.md` 与 `09-status/kds-readonly-probe-report.md` 属于自刷新治理报告，已在计划中归类为 `self_refresh`，不作为业务文档差异追逐。
- OKF 兼容层只读试点已建立：`.okf/index.md`、`.okf/governance/index.md`、`.okf/architecture/index.md`、`.okf/kds/index.md`。

当前仍不得宣称业务完成、验收完成或 accepted/integrated 状态升级。后续全量推广必须继续保留小批量 KDS 写入、只读探测、文档门禁和人工验收判定。

## 2026-06-19 治理闭环收口更新

当前状态：`governance_closure_complete_with_remote_backlog`。

本次收口完成：

- OKF 保持只读导航层，不替代 Git、KDS、台账或 ODF ledger。
- ODF 已建立小批量准入、人工确认、metadata-only envelope、漂移监控和动态源 reference-only 策略。
- KDS 同步继续使用 sync plan 与 directed `--source-path`，不执行全量盲写。
- Loop 文档治理保持可审计状态，但 dirty worktree 和 `.kds` 镜像债务未归因前，不升级状态。

当前 KDS sync plan 快照：`remote_documents=742`、`create=216`、`update=156`、`skip=98`、`self_refresh=2`、`conflicts=0`、`missing_local=0`。因此，前文历史阶段中的 `create=0`、`update=0` 不作为当前全局 KDS 完成声明；本次只声明最终闭环相关文档已完成定向同步。

本次收口不代表：

- 业务完成。
- 全局 KDS pending writes 全部完成。
- 状态升级。
- 源文档语义已被 ODF 替代。
