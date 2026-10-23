---
doc_id: GPCF-GCMEM-VISION-R0-DESIGN-20261021
title: GCMEM R0 变更设计（gcmem-vision-r0）
project: GPCF
related_projects: [GCMEM, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/gcmem-vision-r0/design.md
source_path: openspec/changes/gcmem-vision-r0/design.md
sync_direction: local_only
last_reviewed: 2026-10-21
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/GlobalCloud 项目群总体方案.md
---

# GCMEM R0 变更设计（gcmem-vision-r0）

**结论：本设计把 R0 的冻结对象收敛为「3 份契约 + 1 份变更包 + 6 类回滚开关」，全部内容以 PRD v2.0 与详细设计 v2.0 为源；D0 只冻结不实现，D1 按 WP 顺序实现并逐项留证；任何新能力默认关闭、关闭后回 v1 行为、账本永不回滚。「勾选不改变状态上界：项目仍为 `partial`，文档仍为 `candidate`。」**

## 1. Context

| 项 | 现状（2026-10-21 实测/R0 起点） | 与本设计的关系 |
|---|---|---|
| 回归 | 113/113（gcmem 52 / api 22 / admin 24 / dsh_capture 15） | D1 退出基线，「只增不减」 |
| 账本 | 221 条（活跃 193、替代标注 38；fact 86 / decision 53 / correction 48 / preference 34 / entity 0） | meta v2 兼容基线（旧条目零回写） |
| doctor | `healthy=true`、`issues=[]`、`notes=[]` | WP-D0-03 / WP-D1-06 校验基线 |
| 文档 | PRD v2.0（1434 行）、详细设计 v2.0（4113 行），均 `candidate` | 本设计的唯一内容源 |
| 契约 | `contracts/` 目录（位于 GCMEM 仓）由 WP-D0-02/03/04 产出；2026-10-21 只读核验：7 份契约文件已落盘，`PYTHONPATH= python3 scripts/validate_contracts.py` 全部 PASS（合法 4+5+3 / 非法 8+10+8） | 本设计只引用文件名与设计章节，不复制契约正文 |
| 变更包 | GCMEM 仓 `openspec/` 首次引入；GPCF 中央登记副本已建立（2026-10-21，A1 授权） | 登记副本以 GCMEM 源为准，只改 frontmatter 与登记状态句 |
| 上游控制 | GPCF Feature F-026（只读）、项目群总体/实施方案（继承） | 不改 GPCF 其他内容、不写 KDS；状态上界受 F-026 `status_ceiling: partial` 约束 |

## 2. Goals / Non-Goals

**Goals（本包要达成的 6 件事）**

1. ContextPack v1 Schema 冻结为可校验契约（`pack_version=v1`，2020-12），并给出合法/非法样例集；
2. meta v2 13 键契约冻结：全可选、旧条目零回写、非法键静默丢弃 + `W_META_DROPPED` 告警语义；
3. 评测集 v2 schema 与 8 类/holdout 规则冻结（≥100 条扩展路径、30 条种子查询、六字段版本化报告）；
4. 回滚开关清单冻结为 6 类对象 × 5 列（开关名/默认值/关闭后行为/影响面/验证方式），可执行、可演练；
5. 变更包四件套可回读：proposal / design / specs / tasks 与 PRD 需求 ID 逐条对应；
6. 全部交付留证：命令 + 输出 + 时间戳 + sha256。

**Non-Goals（明确不做）**

1. 不写业务代码（D0）、不改 `src/`/`tests/`/`admin/`/`deploy/`/账本；
2. 不做 L2/L3 投影、时间/实体图检索、跨项目共享、ACL（属 D2+，且须真实需求与授权）；
3. 不改账本行语法、不删改现有 meta 键、不回写历史条目、不新增第六类记忆；
4. 不改 GPCF 共享仓其他内容、不写 KDS 仓；中央登记已按 A1 授权单独执行，本设计不做任何状态提升；
5. 不以「文档完成」表述「功能已实现/已验收」。

## 3. 冻结范围

**结论：冻结对象只有 4 个——ContextPack v1、meta v2、评测集 v2、变更包本身；冻结判定以「可校验、可回读、可回滚」三条为准，不以「写完文档」为准。**

### 3.1 ContextPack v1

| 项 | 内容 |
|---|---|
| 设计源 | 详细设计 §7.5（Schema 全文 + 字段表）、§7.4（预算裁剪）、§9.2.2（`POST /v2/context/compile`） |
| 契约文件 | `contracts/contextpack.v1.schema.json`（逐字取 §7.5，`$id` 改 `urn:gcmem:contextpack:v1`）、`contracts/contextpack.v1.examples.json` |
| 冻结判定 | 2020-12 校验通过；`memories`≤8、`budget.estimated_tokens`≤1500、`reason`≥1、`source_ref`≥1、`strategy` 7 枚举、`additionalProperties:false`、`pack_version` const `v1` |
| 冻结后演进 | 只增可选字段；破坏性变更 → `pack_version=v2` 双版本并行 ≥1 个发布周期（§9.7） |
| 消费方 | 四端（Hermes/Codex/Reasonix/DSH）+ 管理台（D2 展示）+ 评测 |

### 3.2 meta v2（13 键）

| 项 | 内容 |
|---|---|
| 设计源 | 详细设计 §4.5（字段总表）、§4.6（兼容演进）、§4.7（校验与错误）、§4.8（幂等与并发） |
| 契约文件 | `contracts/ledger-meta.v2.schema.json`、`contracts/ledger-meta.v2.contract.md`、`contracts/ledger-meta.v2.examples.json` |
| 13 键 | `project` / `origin` / `session` / `memory_class` / `event_time` / `valid_from` / `valid_to` / `confidence` / `importance` / `evidence` / `scope` / `schema` / `idem`（全部可选、全字符串） |
| 冻结判定 | 13 键全部 `additionalProperties:false`；各键 pattern/enum 与 §4.5 一致；「旧条目零回写」硬规则成文；非法键行为与 `parse_meta`/`meta_to_str` 对照一致 |
| 冻结后演进 | 只加键/加枚举值；禁删键、禁回写（§4.6） |
| 消费方 | 写入（四端 + 捕获桥 + 夜挖）、检索过滤、投影生成（D2）、管理台筛选 |

### 3.3 评测集 v2

| 项 | 内容 |
|---|---|
| 设计源 | 详细设计 §10.1（8 类能力）、§10.2（schema 与扩展路径）、§10.3（指标公式）、§10.5（holdout）、§10.7（合成 vs 真实） |
| 契约文件 | `contracts/eval-dataset.v2.schema.json`、`contracts/eval-dataset.v2.examples.json`、`docs/GCMEM-评测集v2-分类与holdout规则.md` |
| 冻结判定 | `version` const `v2`；query 含 `id`/`q`/`class`（8 类枚举）/`split`(dev/holdout)/`expect`(≥1)/`expect_mids`/`notes`；`additionalProperties:false`；报告六字段（`ledger_total`/`ledger_sha`/算法版本/模型/数据集版本/运行时间） |
| 冻结后演进 | 只增字段；8 类枚举不得自造（与 §10.1 一致）；`ledger_total`/`ledger_sha` 为必填防跨规模比较 |

### 3.4 变更包本体

| 项 | 内容 |
|---|---|
| 文件 | `.openspec.yaml`、`README.md`、`proposal.md`、`design.md`、`tasks.md`、`specs/gcmem-vision-r0/spec.md` |
| 冻结判定 | YAML 可解析且 `schema: spec-driven`；5 份 md 均 16 键 frontmatter；需求场景均可回指 PRD ID；6 类开关齐备；旧口径 0 命中；四禁词仅否定语境 |
| 状态 | GPCF 受控状态 `draft`（已登记，2026-10-21）；不等同生效规格，实现状态以证据为准 |

## 4. 与 PRD / 详细设计章节映射

**结论：每个 WP 都能定位到一组设计章节与 PRD 需求 ID，无「无源任务」。**

### 4.1 D0（设计冻结，5 WP / 12 人日）

| WP | 内容 | 设计章节 | PRD 需求 ID | 交付物 | 退出门禁 |
|---|---|---|---|---|---|
| WP-D0-01 | 双文档对齐、需求 ID 与章节索引校订 | §0.2、§0.3、§19.D、§15.2 | 全部（追踪矩阵入口） | 双文档 v2.0 + 追踪矩阵 + §19.E 索引（既有） | 章节索引 100% 可解析；78 条需求 ID 唯一 |
| WP-D0-02 | 冻结 ContextPack Schema v1 | §7.5、§7.4、§9.2.2 | CTX-01、CTX-02、RET-04 | `contracts/contextpack.v1.*` | `jsonschema` 校验通过；字段表与 Schema 一致 |
| WP-D0-03 | 冻结 meta v2（13 键） | §4.5、§4.6、§4.7、§4.8 | CAP-03、RET-08 前置 | `contracts/ledger-meta.v2.*` | 旧条目解析零变化（`doctor` 基线不变）；零回写成文 |
| WP-D0-04 | 评测分类、100+ schema、holdout 规则 | §10.1、§10.2、§10.3、§10.5 | EVA-01/04/05/07、RET-05 | `contracts/eval-dataset.v2.*` + `docs/GCMEM-评测集v2-分类与holdout规则.md` | schema 校验通过；8 类各 ≥3 条种子；split 规则成文 |
| WP-D0-05 | 变更包 + 回滚开关清单 | §13.3、§13.4、§14.1、§14.2 | OPS-06、CTX-07、EVA-06 | 本目录 6 文件 | proposal 可回读；回滚清单覆盖 6 类对象 |

### 4.2 D1（可信基线，7 WP / 39 人日）

| WP | 内容 | 设计章节 | PRD 需求 ID | 退出门禁 |
|---|---|---|---|---|
| WP-D1-01 | 真实评测集 ≥100 条（8 类 + holdout ≥20%） | §10.2、§10.5 | EVA-01/04/05/07 | 条数 ≥100；8 类各 ≥10；holdout ≥20%；报告复跑一致 |
| WP-D1-02 | 五段诊断器 | §10.4 | EVA-02/03 | 每个失败样本 ≥1 码；5 阶段均有码 |
| WP-D1-03 | ContextPack 编译器 + `/v2/context/compile` + MCP `gcmem_context` | §7.4、§7.5、§9.2.2、§9.3 | CTX-01/02/06、INT-02 | `items≤8`、`tokens≤1500` 断言 100%；字段完整率 100% |
| WP-D1-04 | `/v2/memories/search` + 解释字段 + `gcmem_explain` | §7.6、§9.2、§9.3 | RET-04、INT-01/07 | v1 兼容回归通过；解释字段完整 |
| WP-D1-05 | 幂等写入（`idem=`）+ 影子模式 + 回滚开关 | §4.8、§13.3、§13.4 | CAP-07/09、CTX-07、OPS-06、EVA-06 | 幂等用例通过；开关演练通过 |
| WP-D1-06 | 备份 RPO 治理 | §12.2 | OPS-01/02 | RPO ≤24h（本机通道）；KDS Git 通道有 ≤7 天口径或书面声明 |
| WP-D1-07 | 四端 ContextPack 适配 + 回归 | §9.6 | CTX-03/04/05、INT-04 | 四端自检全过；113/113 + 新增用例全绿 |

## 5. 回滚开关清单（6 类对象）

**结论：6 类对象全部有独立开关、默认关闭、纯配置生效；关闭后的行为与开启前逐字节一致（回归对照），开关状态可在管理台系统页查看，每次演练留证。开关名在本包冻结，D1 落地时不得重命名（改名视为契约变更）。**

| # | 对象 | 开关名（env / config 键） | 默认值 | 关闭后行为 | 影响面 | 验证方式 |
|---|---|---|---|---|---|---|
| 1 | ContextPack 编译接口 | `GCMEM_V2_CTX_COMPILE` / `gcmem.v2.context_compile` | `0`（off） | `POST /v2/context/compile` 路由不注册（404）；MCP `gcmem_context` 不暴露；四端回退 v1 `/v1/memories/search` 注入 | 四端注入路径、`/v2` 端点、MCP 工具列表；不影响 v1 端点与账本 | 关闭后 `curl /v2/context/compile` 返回 404；四端各一次实调 `mid` 集合与 v1 基线一致；回归 113/113 |
| 2 | v2 检索策略（分类/多路/重排） | `GCMEM_RETRIEVAL_V2` / `gcmem.retrieval.algo`（取值 `v1` 或 `v2`） | `v1`（off） | 检索走现行本地 bigram 主体 + gbrain 补充、`sort=relevance` 默认；`/v2/memories/search` 不注册；`reason` 仍由 v1 响应字段提供 | 检索质量与延迟、`/v2/memories/search`、`gcmem_explain`、权重标定报告 | 同评测集同账本 `ledger_sha` 各跑一次，Hit@1/MRR 不低于基线；非法 `algo` 值返回 422（`E_STRATEGY_INVALID` 类）；抽检 10 条排序结果一致 |
| 3 | meta v2 新键（写入侧） | `GCMEM_META_V2_WRITE` / `gcmem.meta.schema`（取值 `v1` 或 `v2`） | `v1`（off） | 写入只补 `project`/`origin`/`session` 三键；`event_time`/`confidence`/`importance`/`evidence`/`idem` 等新键不落盘；读侧继续容忍未知键 | 写入响应、meta 过滤、投影生成（D2）、评测时间类查询 | 关闭后写 1 条带新键的条目：账本行尾无新键、`W_META_DROPPED` 计数为 0；旧条目全量解析 `doctor` 不变；回归 113/113 |
| 4 | 派生投影（D2 起） | `GCMEM_PROJECTION` / `gcmem.projection.enabled`（取值 `off`/`shadow`/`on`） | `off`（D1 前无投影） | 不生成/不读取 `projections/`；检索回退 L1 原子检索并标 `degraded=["projection_missing"]`；`/v2/projections/status` 不注册 | 检索召回面、ContextPack 组装、管理台系统页、`/v2/projections/status` | 置 off 后检索仍可用且 `degraded` 标记可见；删除投影目录后重建 sha256 一致（D2 门禁）；`doctor` `healthy=true` |
| 5 | 幂等写入（`idem=`） | `GCMEM_IDEM_WRITE` / `gcmem.idem.enabled` | `0`（off） | `idem=` 键按「未知/被禁用键」丢弃（不校验、不落盘、不影响判重）；写入行为回现行 `_find_dups` + `llm_judge` 判重；重放不做幂等返回 | 写入路径、并发用例、捕获桥重试、夜挖重放 | 关闭后重放同 `idem` 写入：行为与 D0 前一致（第二次仍走判重，可能 skipped）；开启后同键同内容返回首次结果、同键不同内容 409 `E_IDEM_CONFLICT`；并发 10 线程 10 条不丢 |
| 6 | 四端适配 | `GCMEM_PACK_HERMES` / `GCMEM_PACK_CODEX` / `GCMEM_PACK_REASONIX` / `GCMEM_PACK_DSH`（逐端独立；config 键 `gcmem.clients.<end>.contextpack`） | 全部 `0`（off） | 对应端继续用 v1 检索接口与现有注入逻辑；Hermes 保持预取阈值 0.45 / ≤3 条 / 3s / 15s / 5 次·120s 熔断；MCP 端不调用 `gcmem_context`；DSH 技能回 `/v1/memories/search` | 单端注入体验与延迟；不影响其余三端与主账；不影响 `docs/GCMEM-四端接入说明.md` 现行描述 | 逐端「开→验证→关→验证」：关闭后该端检索结果与 D0 前一致；同一 query 四端 `mid` 集合一致且差异带 `filter_reason`；单端停用不影响其余三端（对照测试） |

### 5.1 开关纪律（6 条，D1 门禁必查）

1. **默认保守**：新能力默认关闭（`0`/`v1`/`off`），开启需显式配置；不允许「默认开 + 隐藏开关」。
2. **纯配置生效**：改开关不改代码、不重启 API 也可生效（需重启的必须写进开关说明，并在演练记录标注）。
3. **可观测**：开关状态在管理台系统页/`/admin/api/metrics` 可见；切换事件写日志（时间、操作者、旧值→新值）。
4. **正交**：6 类开关互不依赖，可单独关闭；任意 1 类关闭不得导致其它 5 类异常。
5. **可验证**：每类开关提供「开 → 验证 → 关 → 验证回基线」的最小命令序列，写入 `docs/GCMEM-D0-契约冻结记录.md`（Lead 收口产出，本包不写该文件）与 D1 演练记录。
6. **随发布记录**：每次开关默认值变更必须进变更记录并回传 PRD/设计（设计 §0.5 变更传导）。

## 6. 影子运行与回退步骤

**结论：影子运行是上线前的唯一观察窗口——旧路径照常返回，新路径旁路执行并只写报告；连续 7 天 ≥200 条样本且不劣于旧路径才允许评估转正；回退按「关开关 → 验基线 → 删派生 → 重建 → 记录」五步走，账本不动。**

### 6.1 影子运行（对应 WP-D1-05，设计 §13.3）

| 项 | 规定 |
|---|---|
| 开关 | `GCMEM_SHADOW=1` / `shadow.enabled=true`，**默认关闭** |
| 行为 | ①旧路径照常执行并返回；②新路径旁路执行（同 query、不同召回/评分/编译）；③两者结果写 `~/.hermes/reports/gcmem-shadow/<date>.jsonl`；④**不做任何写操作**（不写账本、不改索引、不改投影） |
| 报告字段 | `ts`、`query`、`old_mids[]`、`new_mids[]`、`old_ms`、`new_ms`、`degraded`、`diff_reason` |
| 约束 | 影子异常不影响主路径（try/except + 失败计数）；query 先过 `is_sensitive`，样本不含凭据；按天文件保留 30 天；指标单独命名 `shadow.*`，不混入线上指标 |
| 退出条件 | 连续 7 天影子样本 ≥200 条，且新路径在可判定样本上不劣于旧路径（Hit@1/MRR 不退步）；产出影子对比报告后方可评估转正 |
| 转正前提 | 评测报告（六字段）+ 消融表 + 开关演练记录三项齐备；缺一项不评估 |

### 6.2 回退步骤（D1 门禁必做，设计 §13.4）

| 步 | 动作 | 通过判据 |
|---|---|---|
| ① | 打开新开关，验证新行为生效 | 日志/响应可见新字段或新路径；样例结果符合契约 |
| ② | 关闭开关，验证回到 v1 行为 | 响应形状与基线一致；`mid` 集合一致；回归 113/113 |
| ③ | 删除派生目录（投影，D2）/ 置 off（D1） | 检索仍可用；`degraded=["projection_missing"]` 可见；不抛 500 |
| ④ | 恢复/重建（投影） | 重建 sha256 一致；manifest 与账本 SHA 一致 |
| ⑤ | 记录耗时与结果 | 写入 `docs/GCMEM-D0-契约冻结记录.md` 与四端回归记录；含时间戳、命令、输出 |

### 6.3 回退不做什么

1. **账本不回滚**：任何错误用新条目 + `sup:` 修正（append-only 铁律）；
2. 不删除历史影子报告（保留 30 天后归档，不物理删除证据）；
3. 不靠「改数据库/批量改 meta」回退（属回写，需老卢确认且默认不做）；
4. 不用「重启进程」代替开关关闭（重启不改变行为即视为开关未落地）。

## 7. 降级行为（与设计 §12.1 对齐）

**结论：新能力不得改变既有 12 类降级的系统行为；新增能力只允许「关闭即降级」，且降级必须显式可见、可计数、可恢复。**

| 故障（§12.1 编号） | 既有行为 | 本包新增约束 |
|---|---|---|
| F-01/F-02 gbrain 不可用/超时 | 返回本地 bigram，`degraded=["semantic_unavailable"]` | ContextPack 必须透传该标记；不得因编译失败改判为成功 |
| F-03/F-08 索引同步失败 | `synced=false`，账本已写 | 幂等写入不得因 sync 失败回滚账本（CAP-09） |
| F-04 LLM 不可用 | 判重降级为普通写入，`note="[LLM判重不可用: ...]"` | meta v2 推断字段不得因 LLM 缺失而阻塞写入 |
| F-05 投影缺失 | 回退 L1 原子检索，`degraded=["projection_missing"]` | 投影开关 off 即等价于 F-05，行为一致 |
| F-06 投影过期 | 用旧投影但标记 `projection_stale` | 过期投影不得进入默认 ContextPack（strict 场景 503 `E_PROJECTION_MISSING`） |
| F-09 账本不可读 | 保护模式：停止写入，读取报错/503 | 所有新端点（v2）必须同样进入保护模式，不得绕开 |
| F-10 磁盘满 | 写入失败显式 500 `E_WRITE_IO` | 影子报告写失败不得影响主路径 |
| 新增：关闭开关 | — | 视为「主动降级」：行为回 v1，指标计数 `feature_off.<name>`，管理台可见 |

## 8. 实施顺序、部署与生效方式

**结论：先契约后代码、先本机后四端、先影子后转正；每步双处部署 + 重启成对，避免「开发仓改了但生产路径没变」的假绿。**

| 序 | 阶段 | 内容 | 生效要求 |
|---|---|---|---|
| 1 | D0 | 契约冻结 + 变更包 + 开关清单（本包） | 校验脚本 + sha256 留档；不碰运行态 |
| 2 | D1 前置 | 评测集 v2（≥100 条）+ 诊断器 | 只改 `tests/` 与数据集；报告可复跑 |
| 3 | D1 核心 | 编译器 + `/v2/context/compile` + `/v2/memories/search` + MCP 新工具 | `src/` ↔ `~/.hermes/scripts/` 双处同步 + API 重启 + MCP 客户端新会话 |
| 4 | D1 治理 | 幂等写入 + 影子框架 + 6 类开关 | 开关默认 off；影子只写报告；演练留证 |
| 5 | D1 收口 | 四端适配 + RPO 治理 + 回归 | 四端逐端实调；113/113 + 新增用例全绿；`gate_check.sh` PASS |

部署纪律：`src/` 与 `~/.hermes/scripts/` SHA 必须一致（OPS-05）；API 改动 `launchctl unload/load`；MCP 改动客户端新会话；DSH 技能下次会话生效；管理台 `pnpm build` 后部署 `dist`。

## 9. 风险与缓解

**结论：最大风险不是技术，而是「契约漂移」与「以目标当现状」；缓解手段是单一内容源、机器校验、证据留档与状态上界。**

| # | 风险 | 概率/影响 | 缓解 | 触发信号 |
|---|---|---|---|---|
| R1 | 契约漂移（代码/样例/设计三处不一致） | 中/高 | 契约唯一源=设计 §7.5/§4.5/§10.2；`validate_contracts.py` 机器校验；改契约须回传 PRD/设计/四端 | 校验失败或样例与 Schema 不符 |
| R2 | 四端口径不一（同一 query 不同 `mid`） | 中/高 | ContextPack 作为共同消费面；四端 `mid` 集合一致性对照；差异必须带 `filter_reason` | 四端回归出现无解释差异 |
| R3 | 开关未真正落地（关不掉/关了没变） | 中/中 | 6 类开关逐项演练；关闭后必须与基线一致；开关状态可观测 | 关闭后行为仍变化，或需重启不生效 |
| R4 | 影子成本拖慢主路径 | 低/中 | 旁路 try/except + 失败计数 + 超时上限；影子期间指标单独命名 | 主路径 P95 上升或错误计数增加 |
| R5 | 评测集不足/合成凑数 | 中/高 | 8 类各 ≥10、holdout ≥20%、真实查询来源可溯；合成与真实分列报告（EVA-05） | 报告类目分布不达标或用合成指标对外 |
| R6 | 幂等键冲突误判（同键不同内容被吞） | 低/高 | 同键不同内容返回 409 `E_IDEM_CONFLICT`，不静默覆盖；键格式 `[0-9a-zA-Z_-]{8,32}` | 写入返回成功但内容缺失 |
| R7 | 文档失真（把「目标」写成「现状」） | 中/高 | 现状/目标分列；数字带实测时间戳；旧口径 grep；四禁词仅否定语境 | 门禁 grep 命中或数字与 `/stats` 不符 |
| R8 | 两仓副本漂移（GPCF 副本与 GCMEM 源不一致） | 中/中 | 副本只改 frontmatter 与登记状态句；源变更时同步副本；两仓不一致以 GCMEM 源为准并回传 | 两仓文件 sha256 不一致且无同步说明 |
| R9 | RPO 治理未达标（KDS Git 通道 >7 天） | 中/中 | 双通道 RPO 口径成文；本机快照 ≤24h 先达标；KDS 通道给书面口径 | 演练记录缺失或 Git 提交超 7 天 |
| R10 | 数字口径冲突（设计 §14.1 写「219 条」，D0 实测 221 条） | 高/低 | 本包按实测 221 条（2026-10-21，活跃 193 / 替代标注 38）；「零变化」用 doctor 对比基线判定，不绑定具体数字；已列入 §10 待确认项回报 Lead | 文档间数字不一致 |

## 10. 待确认项（Open Questions，需老卢拍板）

| # | 问题 | 本包保守默认 | 影响 | 谁定 |
|---|---|---|---|---|
| Q1 | `idem` 是否进入正式 meta 契约（13 键之一） | 纳入可选键，标注「待确认」 | 写入幂等契约、D1 WP-D1-05 | 老卢 |
| Q2 | 评测集是否允许含项目名/人名（对应 D-03） | 项目名可含；人名脱敏或标注，不写凭据 | 评测集 v2 数据与脱敏规则 | 老卢 |
| Q3 | holdout 比例是否固定 ≥20% | 按 PRD §14 / 设计 §10.5 取 ≥20%，同类分层、事件族不跨 split | 评测统计口径 | 老卢 |
| Q4 | 能力域是 1 个（`gcmem-vision-r0`）还是拆 4 个 capability 目录 | 已按 1 个能力域登记（2026-10-21）；拆分需另立变更 | 中央登记结构 | 老卢（如需拆分时） |
| Q5 | 中央登记由谁执行、登记到哪个变更台账 | **已关闭**：2026-10-21 老卢全部授权，登记至 GPCF 本目录 + `openspec/README.md` + `09-status/globalcloud-document-control-register.md` | 治理链完整性 | 老卢（已确认） |
| Q6 | 设计 §14.1 WP-D0-03 门禁「现有 219 条」与 D0 实测 221 条的口径统一 | 按实测 221 条执行，门禁改为「doctor 基线零变化」 | 文档一致性 | Lead 回传设计作者 |

## 11. 变更记录

| 版本 | 日期 | 变更 | 状态 |
|---|---|---|---|
| v1.0 | 2026-10-21 | 首版：冻结范围、章节映射、6 类回滚开关清单、影子与回退步骤、降级对齐、10 条风险、6 项待确认 | candidate（GCMEM 源副本） |
| v1.1 | 2026-10-21 | GPCF 中央登记：变更包行与 R8 更新、Q5 关闭（A1 授权）、frontmatter 按 GPCF 口径调整 | draft（GPCF 中央登记副本） |
