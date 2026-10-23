---
doc_id: GPCF-GCMEM-VISION-R0-TASKS-20261021
title: GCMEM R0 变更任务清单（gcmem-vision-r0）
project: GPCF
related_projects: [GCMEM, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/gcmem-vision-r0/tasks.md
source_path: openspec/changes/gcmem-vision-r0/tasks.md
sync_direction: local_only
last_reviewed: 2026-10-21
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/GlobalCloud 项目群总体方案.md
---

# GCMEM R0 变更任务清单（gcmem-vision-r0）

> **⚠️ 勾选不等于交付/验收。** 本清单是施工顺序与证据要求，不是验收结论：
> ① 勾选只表示「该条动作已执行且证据已归档」，不代表 WP 通过、阶段完成或功能可用；
> ② 任何勾选若无可回放证据（命令 + 输出 + 时间戳 + sha256），视为未执行；
> ③ 阶段完成以 `docs/GCMEM-D0-契约冻结记录.md`（Lead 收口产出，本包不写该文件）的 WP 门禁核对为准，不以 checkbox 计数为准；
> ④ 本清单不改变状态上界：项目仍为 `partial`，文档仍为 `candidate`。

**结论：共 12 个 WP / 46 条任务（D0 5 WP / 20 条，D1 7 WP / 26 条），按「契约冻结 → 评测与诊断 → 编译与接口 → 幂等与开关 → 四端与 RPO」五段推进；D0 只交文档与契约，D1 才动代码；每条任务都标注依赖与证据要求，禁止跳过、合并或夹带（PRD §14「首个包纪律」）。**

## 0. 使用规则

### 0.1 checkbox 语义

| 标记 | 含义 |
|---|---|
| `- [ ]` | 未开始或进行中；D0 冻结期间默认全部保持未勾选 |
| `- [x]` | 动作已执行**且**证据已归档（证据路径写在任务行尾的「证据：」后） |
| 证据缺失 | 即使动作完成，也按未完成处理并回退为 `- [ ]` |

### 0.2 证据要求（每条任务共用）

| 证据类型 | 最低要求 |
|---|---|
| 命令输出 | 可复跑命令 + 原始输出（贴入证据文件或命令记录），含时间戳 |
| 文件证据 | 交付文件 sha256 + 行数；契约文件另需 `jsonschema` 校验输出 |
| 运行证据 | 回归 113/113、`doctor healthy=true`、`/stats` 实测值 |
| 文档证据 | 16 键 frontmatter、旧口径 grep 0 命中、四禁词仅否定语境 |
| 授权证据 | 涉及 GPCF/KDS/状态提升/中央登记的动作，需老卢书面授权记录（A1 中央登记已于 2026-10-21 授权并执行，记录见 `README.md` §6） |

### 0.3 勾选不等于交付/验收（显著声明）

1. **勾选 ≠ 交付**：勾选是「动作已做」的自我记录，交付是「产物已入库且可回放」；两者之间隔着独立复核。
2. **勾选 ≠ 验收**：验收由 `docs/GCMEM-D0-契约冻结记录.md`（D0）与 R0 门禁清单（D1）执行，且通过验收也不提升任何受控状态。
3. **勾选 ≠ 生效**：开关落地、双处部署、四端新会话生效，缺一项即「未生效」。
4. **勾选 ≠ 可对外宣称**：不得以任务完成度对外表述「功能已实现」「已上线」「已验收」。

### 0.4 执行纪律

1. 严格按 WP 顺序与依赖执行，不跳 WP、不合并任务；证据不齐不开下一条。
2. 不夹带 PRD §14 未列出的能力（图库、跨项目共享、ACL、CI 平台、多租户均不在本包）。
3. 只写本包范围；GPCF 侧仅允许本包登记副本与文档清单/台账追加（A1 授权）；不写 KDS；D0 不改 `src/`/`tests/`/账本。
4. 发现设计缺口（如字段缺失、章节号错位）→ 记入 `design.md` §10 并回报 Lead，不私改设计与 PRD。
5. 每次勾选变更同步更新 §3 门禁核对表与 `docs/GCMEM-D0-契约冻结记录.md` 的证据索引。

## 1. D0 设计冻结（5 WP / 12 人日 / 20 条任务）

### 1.1 WP-D0-01 PRD 与详细设计对齐、需求 ID 与章节索引校订（2 人日）

| 项 | 内容 |
|---|---|
| 依赖 | 无（D0 入口） |
| 退出门禁 | 章节索引 100% 可解析；78 条需求 ID 唯一且前缀合法（CAP/MEM/RET/CTX/GOV/EVA/OPS/SEC/INT） |
| 证据要求 | 追踪矩阵覆盖报告（PRD §13）；双文档 `§` 交叉引用核验输出；frontmatter 16 键检查输出 |

- [ ] 01.1 核验 PRD §5 的 78 条需求 ID 唯一性与前缀分布（D0 时点实测值留档）。证据：ID 清单 + 计数脚本输出。
- [ ] 01.2 核验 PRD §13 追踪矩阵对 78 条需求覆盖 100%（无缺行、无重复行）。证据：矩阵行数=78 的核对输出。
- [ ] 01.3 核验双文档 `§` 交叉引用可解析（PRD 指向详细设计的章节存在且主题匹配）。证据：交叉引用核验清单（命中/不命中逐条）。
- [ ] 01.4 核验双文档 frontmatter 16 键、`status=candidate`、`version=v2.0`，以及旧口径 grep 0 命中。证据：检查脚本输出。

### 1.2 WP-D0-02 冻结 ContextPack Schema v1 + 校验用例（3 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D0-01 |
| 退出门禁 | Schema 通过 `jsonschema` 校验；字段表与 Schema 逐字段一致（0 缺失/0 多出/0 类型漂移） |
| 证据要求 | `contracts/contextpack.v1.schema.json` + `examples.json`；校验脚本输出；sha256 |

- [ ] 02.1 按设计 §7.5 逐字产出 `contracts/contextpack.v1.schema.json`（`$schema` 2020-12，`$id` = `urn:gcmem:contextpack:v1`，纯 JSON、2 空格、尾换行）。证据：文件 sha256 + 行数。
- [ ] 02.2 产出 `contracts/contextpack.v1.examples.json`：合法样例 ≥3（四端/多策略/裁剪场景）、非法样例 ≥5（覆盖 `maxItems` 8、`maxTokens` 1500、`reason` 空、`source_ref` 空、`strategy` 非法、`additionalProperties`、`pack_version` 非 v1）。证据：样例 valid/invalid 计数。
- [ ] 02.3 用 `jsonschema` 逐条校验样例，`valid` 与 `invalid` 与期望 100% 一致。证据：校验命令 + 输出（含版本 4.25.1）。
- [ ] 02.4 将 Schema 与设计 §7.5 字段表逐字段对照，输出差异表（目标：0 差异）。证据：对照表（字段/类型/必填/枚举/上限）。
- [ ] 02.5 核验预算与枚举硬约束（`memories`≤8、`estimated_tokens`≤1500、`reason`≥1 且 7 枚举、`type` 五枚举、`strategy` 7 枚举）在 Schema 中可被机器断言。证据：约束清单 + 断言输出。

### 1.3 WP-D0-03 冻结 v2 meta 契约（13 键）+ 旧条目零回归用例设计（2 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D0-01 |
| 退出门禁 | 现有账本全量解析零变化（`doctor` 基线不变）；「旧条目零回写」成文；13 键全可选 |
| 证据要求 | 3 份契约文件；`doctor` 基线 JSON（`healthy=true`、`issues=[]`）；零回写规则条文位置 |

- [ ] 03.1 产出 `contracts/ledger-meta.v2.schema.json`：13 键（`project`/`origin`/`session`/`memory_class`/`event_time`/`valid_from`/`valid_to`/`confidence`/`importance`/`evidence`/`scope`/`schema`/`idem`）全部 `additionalProperties:false`、全部非必填、各键 pattern/enum 与设计 §4.5 一致。证据：schema sha256 + 键数=13 断言。
- [ ] 03.2 产出 `contracts/ledger-meta.v2.contract.md`：13 键表（含义/取值/示例/默认/校验/引入/消费面）、「旧条目零回写」硬规则、非法键静默丢弃与 `W_META_DROPPED` 告警、与 `parse_meta`/`meta_to_str` 行为对照、兼容与升版规则、`idem` 标注待确认。证据：文件 16 键 frontmatter + 条文位置索引。
- [ ] 03.3 产出 `contracts/ledger-meta.v2.examples.json`：合法样例 ≥4、非法样例 ≥4（非法枚举、`importance=9`、`valid_to` 非法、`idem` 长度/字符不合法、键名含非法字符）。证据：样例计数 + 校验输出。
- [ ] 03.4 设计旧条目零回归用例 `test_meta_v2_compat`（D1 实现）：注入 221 条（2026-10-21 实测）旧格式条目，断言解析字段与现状一致、`doctor` 不变、行数不减。证据：用例设计稿 + `doctor` 基线 JSON。

### 1.4 WP-D0-04 评测分类、100+ 数据集 schema、holdout 规则（3 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D0-01 |
| 退出门禁 | schema 校验通过；8 类各 ≥3 条种子示例；split 比例规则（holdout ≥20%）成文 |
| 证据要求 | `eval-dataset.v2.*` 2 份 + 分类与 holdout 规则文档；8 类枚举与设计 §10.1 逐字对照表 |

- [ ] 04.1 产出 `contracts/eval-dataset.v2.schema.json`：顶层 `version`(const `v2`)/`created`/`ledger_total`/`ledger_sha256`/`split_rule`/`classes`/`queries[]`；query 含 `id`/`q`/`class`(8 类枚举)/`split`(dev/holdout)/`expect`(≥1)/`expect_mids`/`notes`；`additionalProperties:false`。证据：schema sha256 + 校验输出。
- [ ] 04.2 产出 `contracts/eval-dataset.v2.examples.json`：合法样例 ≥2（含完整 8 类样例集）、非法样例 ≥4（class 非法、split 缺失、expect 空、版本错）。证据：样例计数 + 校验输出。
- [ ] 04.3 产出 `docs/GCMEM-评测集v2-分类与holdout规则.md`：8 类定义与判定规则、dev/holdout 划分（≥20%、同一事件族不跨 split、按类分层）、标注规范（`expect` 可判定、禁凭据）、100+ 扩展路径、30 条种子查询（8 类各 ≥3）、指标口径（Hit@1/Hit@3/Recall@5/MRR + `ledger_total`/`ledger_sha256` 必填）。证据：文件 16 键 frontmatter + 8 类分布统计。
- [ ] 04.4 核验 8 类枚举与设计 §10.1 逐字一致、指标公式与设计 §10.3 一致（不自造类别、不改公式）。证据：对照表 + 差异 0 的核对输出。

### 1.5 WP-D0-05 OpenSpec proposal/design/specs/tasks + 回滚开关清单（2 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D0-02 / WP-D0-03 / WP-D0-04 |
| 退出门禁 | proposal 可回读；回滚清单覆盖 6 类对象；6 文件齐备且 5 份 md 均 16 键 |
| 证据要求 | 本目录 6 文件 + YAML 解析输出 + 6 类开关核对表 |

- [ ] 05.1 产出变更包四件套 + `.openspec.yaml` + `README.md`（proposal / design / tasks / specs / README / YAML），并以 PRD §14 六项逐项对应。证据：文件清单 + 行数 + sha256。
- [ ] 05.2 产出回滚开关清单：6 类对象（①ContextPack 编译接口 ②v2 检索策略 ③meta v2 新键 ④派生投影 ⑤幂等写入 ⑥四端适配）× 5 列（开关名/默认值/关闭后行为/影响面/验证方式），无空列。证据：`design.md` §5 表 + 逐列核对输出。
- [ ] 05.3 变更包可回读自检：YAML 可解析且 `schema: spec-driven`；5 份 md 均 16 键 frontmatter；每条需求引用 PRD ID；6 类开关齐备；旧口径 grep 0 命中；四禁词仅否定语境。证据：自检脚本输出 + grep 结果。

## 2. D1 可信基线（7 WP / 39 人日 / 26 条任务）

### 2.1 WP-D1-01 真实评测集 ≥100 条（8 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D0-04 |
| 退出门禁 | 条数 ≥100；8 类各 ≥10；holdout ≥20%；报告复跑一致 |
| 证据要求 | `tests/eval_queries.json v2` + 分类统计 + 基线报告（六字段） |

- [ ] 06.1 从真实使用中采集查询并脱敏（无凭据、无会话全文），形成 ≥100 条候选。证据：采集来源记录 + 脱敏检查输出。
- [ ] 06.2 按 8 类标注并保证每类 ≥10 条，`expect` 使用可判定短语/`expect_mids`。证据：8 类分布表。
- [ ] 06.3 划分 dev/holdout（holdout ≥20%、按类分层、同一事件族不跨 split），并记录划分规则版本。证据：split 统计 + 规则文件。
- [ ] 06.4 产出基线报告：含 `ledger_total`/`ledger_sha`/算法版本/模型/数据集版本/运行时间六字段，同账本复跑结果一致。证据：报告 JSON + 两次运行 diff=0。

### 2.2 WP-D1-02 五段诊断器（5 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D1-01 |
| 退出门禁 | 每个失败样本至少一个诊断码；5 阶段均有码 |
| 证据要求 | `tests/eval_diagnose.py` + 诊断码分布报告 + 抽检一致性记录 |

- [ ] 07.1 实现诊断码枚举：Capture / Encode / Retrieve / Compile / Answer 五段 + `UNKNOWN`，码表固定成文。证据：码表 + 枚举断言。
- [ ] 07.2 对每个失败样本归因，保证至少一个诊断码（允许多码）。证据：失败样本 × 码 映射表。
- [ ] 07.3 产出诊断分布报告 + 抽 20 条人工复核（一致性 ≥80%）。证据：复核记录 + 一致性计算。

### 2.3 WP-D1-03 ContextPack 编译器 + 2 个接口（8 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D0-02 |
| 退出门禁 | `items≤8`、`tokens≤1500` 断言 100% 通过；字段完整率 100% |
| 证据要求 | 编译器模块 + `/v2/context/compile` + MCP `gcmem_context` + 用例输出 |

- [ ] 08.1 实现编译器：分类策略选择、预算裁剪（≤8 条 / ≤1500 tokens）、`trim_reason`、`sort`/`dedupe` 规则与设计 §7.4 一致。证据：单测输出 + 20 条候选裁剪样例。
- [ ] 08.2 实现 `POST /v2/context/compile`，返回严格符合 `contracts/contextpack.v1.schema.json` 的包；超预算参数返回 422（`E_TOKEN_BUDGET`）。证据：契约校验 + 端到端 curl 输出。
- [ ] 08.3 实现 MCP 工具 `gcmem_context`（不替换现有 5 工具，新增可选）。证据：`tools/list` + `tools/call` 实调输出。
- [ ] 08.4 预算断言 100%：构造 20 条候选注入条数=8、`budget.trimmed>0`、`trim_reason` 存在；字段完整率 100%（六要素齐备）。证据：断言用例输出。

### 2.4 WP-D1-04 `/v2/memories/search` + 解释字段 + `gcmem_explain`（5 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D1-03 |
| 退出门禁 | v1 兼容回归通过；解释字段完整 |
| 证据要求 | 端点 + `reason`/`source_ref` 样例 + `gcmem_explain` 输出 + v1 回归输出 |

- [ ] 09.1 实现 `POST /v2/memories/search`：每条结果含 `reason.channels[]` 与 `source_ref`，单条解释 ≤200 字。证据：响应样例 + 长度断言。
- [ ] 09.2 实现 MCP `gcmem_explain`（按需展开，默认不展开）。证据：`tools/call` 实调输出。
- [ ] 09.3 v1 兼容回归：v1 端点形状/状态码/默认语义不变，HTTP 与 MCP `mid` 集合一致。证据：兼容用例输出 + 两入口对照表。

### 2.5 WP-D1-05 幂等写入 + 影子模式 + 回滚开关（5 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D0-03 |
| 退出门禁 | 幂等用例通过；开关演练通过 |
| 证据要求 | 核心改动 + 影子报告样例 + 6 类开关落地 + 演练记录 |

- [ ] 10.1 `idem=` 键校验（`[0-9a-zA-Z_-]{8,32}`）：同键同内容返回首次结果、同键不同内容 409（`E_IDEM_CONFLICT`）、非法长度/字符 422。证据：三组用例输出。
- [ ] 10.2 幂等与并发用例：并发 10 线程/多进程写入不丢条；重放不重复入账；判重与幂等不互相破坏。证据：并发用例输出 + 账本行数断言。
- [ ] 10.3 影子框架：`GCMEM_SHADOW=1` 旁路执行、只写 `~/.hermes/reports/gcmem-shadow/<date>.jsonl`、不写账本/索引/投影，异常不影响主路径。证据：影子报告样例 + 账本 sha256 前后一致。
- [ ] 10.4 6 类回滚开关落地（`GCMEM_V2_CTX_COMPILE` / `GCMEM_RETRIEVAL_V2` / `GCMEM_META_V2_WRITE` / `GCMEM_PROJECTION` / `GCMEM_IDEM_WRITE` / `GCMEM_PACK_<END>`），默认全部保守。证据：6 类配置项清单 + 默认值断言输出。
- [ ] 10.5 回滚演练：6 类开关逐项执行「开 → 验证生效 → 关 → 验证回基线」，记录耗时与结果（设计 §13.4 五步）。证据：演练记录表（开关/开-验证/关-验证/耗时/结果）。

### 2.6 WP-D1-06 备份 RPO 治理（3 人日）

| 项 | 内容 |
|---|---|
| 依赖 | 无（可与 D1 并行） |
| 退出门禁 | 演练 RPO ≤24h（本机通道）；KDS Git 通道有 ≤7 天口径或书面声明 |
| 证据要求 | 双通道 RPO 口径文档 + 快照校验自动化输出 + 恢复演练记录 |

- [ ] 11.1 成文双通道 RPO 口径：本机快照（每日 23:50 + sha256）与 KDS Git 通道（现状与目标）；KDS 写入需授权。证据：口径文档 + `git log` 实测距今。
- [ ] 11.2 快照校验自动化：连续 7 天快照存在 + sha256 校验通过，异常可告警。证据：7 天清单 + 校验脚本输出。
- [ ] 11.3 恢复演练（只读沙箱）：RTO ≤30min，记录耗时与步骤。证据：演练记录（命令/耗时/结果）。

### 2.7 WP-D1-07 四端 ContextPack 适配 + 回归（5 人日）

| 项 | 内容 |
|---|---|
| 依赖 | WP-D1-03 |
| 退出门禁 | 四端自检清单全过；回归 113/113 + 新增用例全绿 |
| 证据要求 | 四端配置变更 + 四端各一次实调记录 + 回归输出 |

- [ ] 12.1 Hermes：预取改 `gcmem_context`，保留阈值 0.45 / ≤3 条 / 预取 3s / 检索 15s / 熔断 5 次·120s。证据：插件配置 + 一次实调记录。
- [ ] 12.2 Codex / Reasonix：MCP 新工具可选启用（不替换 5 工具），按需检索。证据：两端 `tools/call` 实调记录。
- [ ] 12.3 DSH：技能优先调 `/v2/context/compile`，捕获桥行为不变（只认真人消息、凭据不入账）。证据：技能文件 diff + 一次实调记录。
- [ ] 12.4 四端一致性：同一 query 的 `mid` 集合一致（差异必须带 `filter_reason`）；单端停用不影响其余三端；回归 113/113 + 新增用例全绿。证据：对照表 + `pytest -q` 输出。

## 3. 阶段退出门禁核对（不计入任务条数）

### 3.1 D0 退出门禁（设计 §14.1，6 条）

| # | 门禁 | 判据 | 核对状态 |
|---|---|---|---|
| 1 | 双文档对齐 | `status=candidate`，章节索引一致，`§` 交叉引用全部可解析 | 未核对 |
| 2 | ContextPack Schema 冻结 | Schema 通过 `jsonschema` 校验；字段表一致（未实现编译亦可） | 未核对 |
| 3 | meta v2 契约冻结 | 13 键成文；「旧条目零回写」声明在案 | 未核对 |
| 4 | 评测数据集 schema 冻结 | 8 类 schema 通过校验；100+ 扩展路径与 holdout 规则成文 | 未核对 |
| 5 | 变更包可回读 | proposal 可读；回滚清单覆盖 6 类对象 | 未核对 |
| 6 | 门禁留证 | 项目群文档门禁结果留档，不改变 `candidate`/`partial` | 未核对 |

### 3.2 D1 退出门禁（设计 §14.2，7 条）

| # | 门禁 | 判据 | 核对状态 |
|---|---|---|---|
| 1 | 真实评测 | ≥100 条，报告含 dev/holdout 与账本 SHA | 未核对 |
| 2 | 契约可用 | ContextPack 预算断言 100% | 未核对 |
| 3 | 五段诊断 | 可对失败样本归因（每样本 ≥1 码） | 未核对 |
| 4 | RPO 治理 | 演练 ≤24h 且留证 | 未核对 |
| 5 | 影子与回滚 | 影子可开关，回滚演练通过 | 未核对 |
| 6 | 回归不回退 | 113/113 + 新增用例全绿 | 未核对 |
| 7 | v1 兼容 | 全部 v1 端点行为不变（兼容矩阵验证） | 未核对 |

## 4. 任务统计

| 阶段 | WP 数 | 任务条数 | 估算人日 | 依赖链 |
|---|---:|---:|---:|---|
| D0 设计冻结 | 5 | 20 | 12 | D0-01 → {D0-02, D0-03, D0-04} → D0-05 |
| D1 可信基线 | 7 | 26 | 39 | D0-04 → D1-01 → D1-02；D0-02 → D1-03 → {D1-04, D1-07}；D0-03 → D1-05；D1-06 可并行 |
| 合计 | 12 | 46 | 51 | 关键路径：D0-01→D0-02→D1-03→D1-07 |

> 人日来自设计 §14.1（12）与 §14.2（39）；按每周 2–3 有效人日，D0+D1 的 51 人日需 17–26 周，超出 0～3 月窗口，**必须分两批交付**（设计 §14 章结论）。
