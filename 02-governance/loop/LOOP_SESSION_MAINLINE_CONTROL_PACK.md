---
doc_id: GPCF-DOC-6C7A1E9D2B
title: LOOP 会话主线控制包
project: WAES
related_projects: [GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md
source_path: 02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP 会话主线控制包

本控制包把 LOOP 会话主线、防偏离、跨会话交接和多智能体并行边界纳入启动/恢复前置门禁。它服务于 [LOOP 工程体系整体实施规范](./LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md)，不替代 `LOOP_CONTROL_BOARD.md`、`LOOP_AUTONOMY_POLICY.md` 或具体项目 evidence。

## 1. 适用范围

| 范围 | 要求 |
|---|---|
| GPCF 总控治理 | 每轮启动、恢复、继续或下一步前必须确认当前 `session_mainline` |
| 项目本地 LOOP | 接续项目仓任务前必须读取项目本地 loop-state、最近 round、Git 状态和 evidence |
| 多会话协作 | 其它会话的任务不得被隐式接管，必须有 handoff evidence 和用户确认 |
| 多智能体并行开发 | 必须拆成互不重叠的 scope，最终集成和状态裁决回到主会话 |
| 能力族治理 | CodeGraph、Agent-Reach、Ontology、Headroom、WAS、OKF/ODF、LCX、RAG/语义索引和外部检索均受本控制包约束 |

## 2. 启动/恢复前置声明

每次 LOOP 启动、恢复、继续或跨会话接续前，必须生成或等价确认 `session_mainline` 声明。推荐模板为 [LOOP 会话主线声明模板](../../templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md)。

最低字段：

| 字段 | 要求 |
|---|---|
| `session_mainline` | 当前会话唯一主线，不得为空 |
| `objective` | 本轮目标，必须可验证 |
| `scope_in` | 允许读取或修改的项目、目录、文件、能力或任务包 |
| `scope_out` | 明确不处理的项目、目录、文件、能力或任务包 |
| `allowed_actions` | 允许动作，例如只读检查、局部文档修改、局部 validator |
| `forbidden_actions` | 禁止动作，至少包含生产写入、真实外部 API 写入、真实 KDS API 写入、commit、push、deploy、accepted/integrated 升级 |
| `stop_conditions` | 触发暂停或请求确认的条件 |
| `owner_session` | 当前任务 owner 会话或主会话 |
| `evidence_inputs` | 本轮必须读取的控制板、round、evidence、validator 或 Git 状态 |

## 3. 跨会话交接

接续其它会话、其它项目、其它任务包或其它智能体输出时，必须先完成 handoff。推荐模板为 [LOOP 跨会话交接模板](../../templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md)。

最低条件：

- 用户明确确认接管或继续该会话任务。
- 已读取目标会话最后一轮 `loop-round`、evidence、validator 输出和 Git 状态。
- 新会话记录 `handoff_source`、`handoff_time`、`scope_delta`、`authorization_delta` 和 `remaining_risks`。
- 若涉及其它项目仓、真实 KDS API、外部 API、提交、推送、部署或状态升级，必须重新请求授权。
- 若没有完整交接证据，只能生成建议，不能执行写入。

## 4. 偏离判定

出现任一情况时，必须标记 `mainline_drift_detected`，并暂停写入：

| 信号 | 判定 |
|---|---|
| 用户请求与当前 `session_mainline` 不一致 | 需要重新确认主线 |
| 当前工作目录或目标项目与 `scope_in` 不一致 | 需要重新确认范围 |
| Git dirty 文件包含非本轮 scope | 只允许只读核对或请求确认 |
| 任务包、validator 或 evidence 指向其它会话 | 需要 handoff evidence |
| 多智能体输出触碰重叠 scope | 主会话必须暂停集成 |
| 需要 commit、push、deploy、真实 API 写入、schema sync 或状态升级 | 必须重新请求授权 |

发现偏离后允许的动作只有：

- 只读核对当前状态。
- 生成偏离报告或建议。
- 请求用户确认。
- 回到当前 `session_mainline`。

不得继续写入、同步其它仓库、更新其它会话任务状态或关闭其它会话结论。

## 5. Validator 与门禁接入

硬门禁：

```bash
python3 tools/kds-sync/validate_loop_session_mainline_control.py
```

该 validator 必须由 `loop_document_gate.py` 调用，作为每轮 LOOP 启动/恢复前置门禁和文档门禁的一部分。它检查：

- 本控制包为 `controlled`。
- 主实施规范包含会话主线边界。
- 两个模板存在并包含必填字段。
- 总文档门禁接入 `validate_loop_session_mainline_control.py`。
- 不出现允许未授权本地提交、推送、部署、真实 API 写入或 accepted/integrated 的正向表述。

## 6. 状态边界

本控制包不创建业务事实、不接管其它会话、不证明任务完成、不授权真实 KDS API 写入、不授权外部 API 写入、不授权跨仓执行、不授权 commit、push、deploy、accepted、integrated 或 production_ready。

它只能把会话主线控制从口头约束转成文档和机器门禁。任何跨会话执行仍以用户确认、handoff evidence、Git 状态和项目本地 evidence 为准。
