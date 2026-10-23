---
doc_id: GPCF-GCMEM-VISION-R0-PROPOSAL-20261021
title: GCMEM R0 可信基线变更提案（gcmem-vision-r0）
project: GPCF
related_projects: [GCMEM, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/gcmem-vision-r0/proposal.md
source_path: openspec/changes/gcmem-vision-r0/proposal.md
sync_direction: local_only
last_reviewed: 2026-10-21
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/GlobalCloud 项目群总体方案.md
---

# GCMEM R0 可信基线变更提案（gcmem-vision-r0）

**结论：本提案申请在 GCMEM 仓内建立首个变更包，把 PRD §14 的「首个变更包 6 项」与设计 D0/D1 的 12 个 WP 固化为可回读、可回滚、可验收的 OpenSpec 变更（已于 2026-10-21 在 GPCF 完成中央登记，A1 授权）；本包只做契约冻结与规则成文（D0），并在 D1 才引入代码与四端改动；不改账本行语法、不做分层记忆/图检索/跨项目共享/ACL，不把文档完成表述为功能实现或验收。**

## Why

**结论：GCMEM 的能力已「能记、能查、能恢复」，但契约是隐式的——四端各说各话的风险已经出现，评测与回滚没有成文依据。**

| # | 现状（截至 2026-10-21 实测） | 缺口 | 本包对应 |
|---|---|---|---|
| 1 | 账本 221 条（活跃 193、替代标注 38），append-only 与 `sup:` 替代链已运行 | 无正式契约判定「什么是合法的上下文包」 | ContextPack v1 Schema（CTX-01/02） |
| 2 | meta 现用 3 键（`project`/`origin`/`session`），解析器对未知键静默丢弃 | 时间/置信度/重要性/证据四类语义无处安放，新旧键行为无成文规则 | meta v2 契约（CAP-03、RET-08 前置） |
| 3 | 回归 113/113、doctor `healthy=true`、`issues=[]` | 评测集仅 22 条真实查询，无分类与 holdout，指标不可复现比较 | 评测集 v2（EVA-01/04/05/07） |
| 4 | 检索本地 bigram 主体 + gbrain 补充可用 | 排序原因、来源回指、预算裁剪未冻结，四端注入口径不一 | CTX-02/03、RET-04 |
| 5 | 回滚散见于各文档（设计 §13.4） | 无逐能力的开关清单（名称/默认/关闭后行为/影响面/验证） | 6 类回滚开关清单（OPS-06、CTX-07、EVA-06） |
| 6 | GPCF 侧有 Feature/Evidence 控制链 | GCMEM 无 OpenSpec 生效面，变更不可回读、不可逐条验收 | 本变更包四件套 |

## What Changes

**结论：变更严格对应 PRD §14「首个变更包 6 项」，逐项给出交付物与阶段归属；D0 只交文档与契约，D1 才交代码。**

| # | 变更项（PRD §14） | 交付物 | 阶段/WP | 关联需求 ID |
|---|---|---|---|---|
| 1 | 评测集扩展与分类规则 | `contracts/eval-dataset.v2.schema.json` + `examples` + `docs/GCMEM-评测集v2-分类与holdout规则.md`（D1 扩到 ≥100 条） | D0/WP-D0-04；D1/WP-D1-01 | EVA-01/04/05/07 |
| 2 | ContextPack v1 JSON Schema | `contracts/contextpack.v1.schema.json` + `examples`（D1 编译器与端点） | D0/WP-D0-02；D1/WP-D1-03 | CTX-01/02、RET-04 |
| 3 | meta v2 兼容契约 | `contracts/ledger-meta.v2.schema.json` + `contract.md` + `examples`（D1 写入与兼容用例） | D0/WP-D0-03；D1/WP-D1-05 | CAP-03、RET-08 前置 |
| 4 | D1 备份 RPO 修复方案 | KDS Git 提交节奏方案 + 双通道 RPO 口径 + 演练脚本增强（D1 落地） | D1/WP-D1-06 | OPS-01/02 |
| 5 | 影子模式与回滚开关 | 本包 `design.md` §5 的 6 类开关清单（D1 落地开关与演练） | D0/WP-D0-05；D1/WP-D1-05 | OPS-06、CTX-07、EVA-06 |
| 6 | OpenSpec 变更包 | 本目录 6 个文件（proposal / design / specs / tasks / README / `.openspec.yaml`） | D0/WP-D0-05 | 全部（入口） |

补充变更（D1，且已被 PRD §14 列或 R0 门禁要求）：

| 变更 | 交付物 | WP | 关联需求 ID |
|---|---|---|---|
| 五段诊断器 | 诊断码枚举 + 分桶报告（D1） | WP-D1-02 | EVA-02/03 |
| `/v2/context/compile` + MCP `gcmem_context` | 编译器模块 + 2 个接口 + 用例（D1） | WP-D1-03 | CTX-01/02/03、INT-02 |
| `/v2/memories/search` + 解释字段 + `gcmem_explain` | 接口 + 用例（D1） | WP-D1-04 | RET-04、INT-01 |
| 幂等写入（`idem=`）+ 影子框架 | 核心改动 + 影子报告 + 开关（D1） | WP-D1-05 | CAP-07/09、EVA-06 |
| 四端 ContextPack 适配 | 四端配置 + 回归记录（D1） | WP-D1-07 | CTX-03/04/05、INT-04 |

## Capabilities

**结论：本包定义 1 个能力域、4 个能力组；能力组只是规格文件内部组织，不改变需求内容。**

### New Capabilities

- `gcmem-vision-r0`（能力域，`specs/gcmem-vision-r0/spec.md`）：
  1. **ContextPack v1 契约**（CTX-01/02/06，RET-04）——统一消费契约与预算裁剪；
  2. **meta v2 兼容契约**（CAP-03，RET-08 前置）——13 键可选、旧条目零回写；
  3. **评测集 v2 与诊断**（EVA-01..08，RET-05，CAP-09）——8 类能力、dev/holdout、六字段版本化；
  4. **可回滚与接口兼容**（CTX-07、OPS-06、INT-01..08）——6 类开关、v1 行为冻结。

### Modified Capabilities

无。v1 已实现能力（写入/检索/治理/运维/四端接入）保持行为不变，只做「可选字段 + 新路径」加法；D0 不新增代码路径。

## Affected

| 面 | 影响 | 写边界 |
|---|---|---|
| GCMEM 仓（本仓） | 新增 `openspec/changes/gcmem-vision-r0/`（本包）、`contracts/`（契约，WP-D0-02/03/04）、`docs/`（评测规则由 WP-D0-04 交付；契约冻结记录由 Lead 收口）、`scripts/validate_contracts.py`（校验脚本，Lead 交付）；D1 起改 `src/`（编译器、幂等、v2 端点）与 `tests/` | 本包只写 6 个文件；不写 `src/`、`tests/`、`admin/`、`deploy/`、账本 |
| 四端：Hermes | 注入改用 ContextPack（≤3 条更严阈值、预取超时 3s、检索超时 15s、5 次/120s 熔断） | 配置在 `~/.hermes/`，D1 才改；本包不写 |
| 四端：Codex | MCP 按需检索，新增 `gcmem_context` / `gcmem_explain`（可选，不替换 5 工具） | `~/.codex/config.toml`，D1 才改；本包不写 |
| 四端：Reasonix | MCP 按需检索，同 Codex 口径（含 wrapper 启动链） | `~/.reasonix/config.json`，D1 才改；本包不写 |
| 四端：DSH | 技能按需 + 捕获桥自动入账，消费 ContextPack | `~/.dsh/skills/` 与捕获桥，D1 才改；本包不写 |
| KDS 账本 | **只读**：D0 不写入、不改行格式；D1 幂等写入仍只经 `gcmem.py` 核心函数，append-only 不变 | 禁止直接编辑账本文件；禁止物理删除 |
| GPCF 仓 | 仅新增本变更包登记副本与文档清单/台账追加行（2026-10-21 A1 授权）；Feature F-026 只读绑定 | 不改 GPCF 其他文件、不改 F-026 文件；GCMEM 仓保留源副本 |
| 依赖 | `jsonschema`（契约校验，实测 4.25.1 可用）、`/usr/bin/python3` 3.9.6、现有 113/113 回归、launchd 服务、gbrain | 均为既有依赖，不新增运行时依赖 |

## Non-goals

**结论：以下事项明确不在本包，违反即为夹带。**

1. 不写业务代码（D0）；D1 也不做 D2 及以后能力。
2. 不做分层记忆（L2/L3 投影）、不做时间/实体图检索、不做跨项目共享、不做 ACL（PRD §4.6「不进入各版本的能力」、§14「首个包纪律」）。
3. 不改账本行语法（`ENTRY_RE` 全量依赖）；不删除或重命名现有 meta 键；不回写历史条目（设计 §4.6）。
4. 不新增第六类记忆（维持 fact/decision/correction/preference/entity）。
5. 不引入图数据库、不引入 CI 平台、不做多租户隔离。
6. 不把 `meta`/`scope` 过滤宣传为权限隔离（SEC-05）。
7. 不改 GPCF 共享仓其他内容、不写 KDS 仓；中央登记已按 A1 授权单独执行，本提案不做任何状态提升。
8. 不以文档完成、测试通过或门禁通过替代真实业务验收；不出现 `accepted` 等四词的非否定表述。

## Rollback boundary

**结论：回滚分「配置关闭」「派生物删除」「代码回退」三类，全部不需要数据迁移；账本永远不回滚。**

| 回滚对象 | 方式 | 影响 | 验证 |
|---|---|---|---|
| 6 类新能力 | 关闭开关（`design.md` §5 清单，配置/环境变量，默认保守关闭） | 四端回到 v1 relevance 行为 | 关闭后回归 113/113 + 对照测试 |
| ContextPack 编译 | 关闭 `/v2/context/compile` 路由，调用方回退 v1 search | 四端用 v1 检索结果 | 四端自检清单 |
| MCP 新工具 | 客户端配置不启用（工具存在但不调用） | 无影响 | 客户端新会话 `tools/list` 检查 |
| 派生投影（D2 起） | 删除 `projections/` 目录并置开关 off | 回退 L1 原子检索，`degraded=["projection_missing"]` | 检索可用 + 降级标记可见 |
| 代码版本 | 恢复上一版文件 + `src/` 与 `~/.hermes/scripts/` 双处同步 + 重启 API | API/MCP 回到旧版 | `bash scripts/gate_check.sh` + 实调 |
| 账本 | **不回滚** | — | 错误用新条目 + `sup:` 修正 |
| 本变更包文档 | 置 `status: superseded` + 指向替代包 | 不影响运行态 | 文档控制与门禁留证 |

## Feature 绑定（GPCF F-026，只读）

| 项 | 值（只读引用） |
|---|---|
| Feature ID | `F-026` |
| Feature 名 | `gcmem-governance-onboarding` |
| 所在 | `features/active/F-026-gcmem-governance-onboarding/`（`feature.yaml` / `journal.md` / `evidence/`） |
| 当前状态 | `active`（`status: active`，`loop.current_step: evaluate`，`status_ceiling: partial`；`feature.yaml` 证据状态：tests/build/summary=pass，screenshots/api=waived） |
| 绑定方式 | 本包作为 GCMEM 侧 OpenSpec 变更入口，提案与任务引用 F-026 ID，并已在 GPCF `openspec/changes/gcmem-vision-r0/` 登记；证据回传 F-026 `evidence/` 与 `journal.md` 由 GPCF 侧另行执行（A1 授权范围不含 Feature 文件改写） |
| 中央登记 | **已登记（2026-10-21 老卢授权 A1）**：`openspec/README.md` 文档清单 + `09-status/globalcloud-document-control-register.md` + GPCF 副本目录；不改 F-026 文件 |
| 状态约束 | F-026 `status_ceiling: partial`，与本包一致；任何提升需人工确认 |

## 证据要求

**结论：每项交付必须可回放——命令 + 输出 + 时间戳 + sha256，缺一项即视为未通过。**

| 类别 | 要求 | 示例 |
|---|---|---|
| 回归 | `cd tests && PYTHONPATH= /usr/bin/python3 -m pytest -q` 输出留档，基线 113/113 只增不减 | `evidence/tests.txt`（D1 由 GPCF 侧留证） |
| 巡检 | `python3 gcmem.py doctor --json` → `healthy=true`、`issues=[]` | 输出 JSON 落档 |
| 契约 | `PYTHONPATH= python3 scripts/validate_contracts.py` 全绿 + 每份契约 sha256 | 校验输出 + 文件 hash |
| 文档 | 16 键 frontmatter、`doc_id` 唯一、旧口径 grep 0 命中、四禁词仅否定语境 | `bash scripts/gate_check.sh` 输出 |
| 四端（D1） | 每端一次「检索 + 写入」实调记录，同一 query 的 `mid` 集合一致（差异须有 `filter_reason`） | 续写 `docs/GCMEM-四端回归记录.md` |
| 回滚（D1） | 6 类开关逐项「开 → 验证 → 关 → 验证回基线」演练记录 | `design.md` §6 五步演练输出 |
| 评测（D1） | 报告含 `ledger_total`/`ledger_sha`/算法版本/模型/数据集版本/运行时间六字段，同账本复跑一致 | `tests/bench_gcmem_report.json` 类报告 |

## 状态与不声明边界

本提案为 `candidate` 文档，项目状态 `partial`。本包完成（即使 6 文件齐备、门禁通过）**不等于**功能已实现、代码已合入、四端已适配、账本已变更；也**不产生** `accepted` / `integrated` / `production_ready` / `customer_accepted` 中的任何状态。后续实现与验收须按 `tasks.md` 逐 WP 留证，并由项目群治理链与老卢确认。
