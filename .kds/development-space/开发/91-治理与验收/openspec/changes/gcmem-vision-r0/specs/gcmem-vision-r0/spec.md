---
doc_id: GPCF-GCMEM-VISION-R0-SPEC-20261021
title: GCMEM R0 能力规格（gcmem-vision-r0）
project: GPCF
related_projects: [GCMEM, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/gcmem-vision-r0/specs/gcmem-vision-r0/spec.md
source_path: openspec/changes/gcmem-vision-r0/specs/gcmem-vision-r0/spec.md
sync_direction: local_only
last_reviewed: 2026-10-21
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/GlobalCloud 项目群总体方案.md
---

# gcmem-vision-r0 能力规格

**结论：本规格定义 R0 变更包的 10 条需求、33 个 Given/When/Then 场景，全部回指 PRD v2.0 需求 ID 与 D0 冻结契约文件；规格只描述「应满足的行为与判定方式」，不描述实现细节，也不改变实现状态——文件齐备不等于功能已实现。**

## 0. 范围与阅读约定

| 项 | 内容 |
|---|---|
| 能力域 | `gcmem-vision-r0`（对应本目录；内部 4 个能力组：ContextPack v1 / meta v2 / 评测集 v2 / 可回滚与接口兼容） |
| 覆盖阶段 | R0 可信基线 = 设计 D0 设计冻结 + D1 可信基线（设计 §14.0） |
| 需求源 | PRD v2.0 §5（CTX/CAP/EVA/INT/OPS 等）；设计 v2.0 §7.5、§4.5、§10、§9、§13.3/§13.4 |
| 契约源 | `contracts/*.json`（位于 **GCMEM 仓**，WP-D0-02/03/04 产出）。**本规格只引用文件名与设计章节，不复制契约正文**。2026-10-21 只读核验：7 份契约文件已落盘且 `scripts/validate_contracts.py` 全部 PASS（合法 4+5+3 / 非法 8+10+8 条样例）；`docs/GCMEM-评测集v2-分类与holdout规则.md` 写作时未落盘，属 WP-D0-04 交付物，缺失不作为本规格失败依据，交付判定以 D0 门禁核对为准 |
| 场景语义 | GIVEN = 前置条件与数据；WHEN = 触发动作/命令；THEN = 可观察、可判定的结果 |
| 状态上界 | 本规格任何条目通过，最多支撑 `candidate` / `ready_for_review` 候选；不产生受控状态提升 |

## ADDED Requirements

### Requirement: ContextPack v1 契约冻结

系统 SHALL 提供并冻结 ContextPack v1 契约，使四端在同一查询下消费同一结构、同一预算、同一降级语义的上下文包；契约覆盖 PRD CTX-01、CTX-02。

#### Scenario: Schema 冻结并通过 2020-12 校验

- **GIVEN** 设计 §7.5 的 ContextPack Schema 全文与字段表已发布（`v2.0`，4113 行文档内）
- **WHEN** 运行 `PYTHONPATH= python3 scripts/validate_contracts.py`，对 `contracts/contextpack.v1.schema.json` 与 `contracts/contextpack.v1.examples.json` 逐条校验
- **THEN** Schema 使用 `https://json-schema.org/draft/2020-12/schema`；必填字段 `pack_version`/`query_id`/`created_at`/`strategy`/`memories`/`budget`/`degraded` 齐备；合法样例全部通过、非法样例全部被拒（合法 ≥3 / 非法 ≥5）

#### Scenario: 预算裁剪不静默

- **GIVEN** 候选记忆 20 条，预算上限 `max_items=8`、`max_tokens=1500`（PRD CTX-02）
- **WHEN** 编译上下文包
- **THEN** `memories` 长度 ≤8、`budget.estimated_tokens` ≤1500、`budget.trimmed` >0，且每条被裁项在 `trim[]` 中有 `reason`（`budget_items`/`budget_tokens`/`duplicate`/`superseded`/`low_relevance` 之一）；不得静默截断

#### Scenario: 非法策略与超预算参数被拒

- **GIVEN** 调用方提交 `strategy=unknown` 或 `max_tokens=5000`
- **WHEN** 调用 `/v2/context/compile`
- **THEN** 返回 422（`E_STRATEGY_INVALID` / `E_TOKEN_BUDGET` 语义码），响应体含可读 `message`；不得返回 200 掩盖失败

> 契约引用：`contracts/contextpack.v1.schema.json`、`contracts/contextpack.v1.examples.json`（源：设计 §7.5、§7.4、§9.2.2）

### Requirement: 上下文去重与冲突消解

系统 SHALL 在注入前对同一事实的多版本去重、对跨条目近重复合并，且合并结果可回溯；覆盖 PRD CTX-06、RET-03。

#### Scenario: 同一事实多版本只取当前有效

- **GIVEN** 同一事实存在 3 个版本（1 条活跃 + 2 条被 `sup:` 替代）
- **WHEN** 编译 ContextPack
- **THEN** 包内只出现 1 条（当前活跃版本）；`superseded=true` 的条目只在审计面出现，默认面不出现

#### Scenario: 合并项可回溯

- **GIVEN** 两条近重复但分属不同 `mid` 的活跃条目同时进入候选
- **WHEN** 编译执行去重合并
- **THEN** 保留高分者，另一条记录在 `merged_from`，审计可查到被合并的 `mid`；账本不发生任何修改

#### Scenario: 不同事实不被误合并

- **GIVEN** 两条字面相近、语义不同的条目（对照组用例）
- **WHEN** 执行同一去重规则
- **THEN** 两条都保留；不得因文本相似度阈值把不同事实合并

> 契约引用：`contracts/contextpack.v1.schema.json`（源：设计 §7.3、§7.4、§4.3）

### Requirement: 四端统一消费与注入容错

系统 SHALL 让 Hermes / Codex / Reasonix / DSH 四端在同一 query 下得到同一语义的 ContextPack，并在注入失败时降级而不阻塞会话；覆盖 PRD CTX-03、CTX-04、CTX-05、INT-02、INT-07。

#### Scenario: 四端同一查询结果集一致

- **GIVEN** 四端均接入（Hermes 插件、Codex/Reasonix MCP、DSH 技能 HTTP）
- **WHEN** 四端对同一 query 各自取一次上下文包（端侧更严阈值允许存在）
- **THEN** 四端 `memories[].mid` 集合一致；若某端因更严预算/阈值过滤，必须提供 `filter_reason` 说明；不得出现无解释差异

#### Scenario: 注入失败跳过并熔断

- **GIVEN** API 不可用或注入超时（预取 3s、检索 15s）
- **WHEN** 会话继续发生
- **THEN** 注入被跳过且会话不阻塞，日志可见跳过原因；Hermes 连续 5 次失败后在 120s 内不再重试（熔断），恢复后自动恢复注入

#### Scenario: 默认不展示内部细节

- **GIVEN** 普通会话（用户未要求解释、无冲突、非审计）
- **WHEN** 注入上下文包
- **THEN** 默认注入文本不含得分、通道名、行号等内部字段；用户显式展开、审计模式或出现冲突时才展示 `reason`/`source_ref`

#### Scenario: 旧消费者容忍新增字段

- **GIVEN** 新增一个可选字段（如 `explain.algo`）后的 ContextPack
- **WHEN** 旧版消费者解析
- **THEN** 旧消费者忽略未知字段、不报错；生产端 `additionalProperties:false` 仍严格校验；破坏性变更必须升 `pack_version`

> 契约引用：`contracts/contextpack.v1.schema.json`（源：设计 §9.6、§7.5、§7.6）

### Requirement: meta v2 兼容契约

系统 SHALL 定义 13 个可选 meta 键的契约，保证旧条目零回写、非法键行为显式、非法值被拒；覆盖 PRD CAP-03、RET-08 前置。

#### Scenario: 旧条目零回写

- **GIVEN** 账本 221 条（2026-10-21 实测，活跃 193 / 替代标注 38），均无 v2 新键
- **WHEN** 升级解析与写入逻辑后运行 `python3 gcmem.py doctor --json` 与全量解析
- **THEN** 解析结果与升级前一致、条目数不减少、账本 sha 在无写入时不变；**不得回写历史条目**（补 `valid_from` 等只能靠新条目 + `sup:`/`evidence=` 表达）

#### Scenario: 带新键写入可回读

- **GIVEN** 写入方显式提供 `event_time`/`confidence`/`importance`/`evidence`（或 `idem`）
- **WHEN** 经 `POST /v1/memories/` 与 MCP `gcmem_add` 写入并按 `mid` 回读
- **THEN** 四字段（及 `idem`）可经 API/MCP 回读，值与写入一致；行尾 `meta:` 串符合 `k=v;k2=v2` 格式

#### Scenario: 非法值被拒

- **GIVEN** 提交 `confidence=high` 以外的枚举、`importance=9`、`valid_to=2026-13-01`、`idem` 长度/字符不合法
- **WHEN** 写入
- **THEN** 返回 400/422 并给出字段级说明；不得静默落盘

#### Scenario: 非法键静默丢弃且可计数

- **GIVEN** 写入 meta 含非法键（如 `bad key=1`）或值含分号
- **WHEN** 经 `meta_to_str`/`parse_meta` 处理
- **THEN** 非法项被丢弃（与现有 `parse_meta` 的 `\w+` 校验一致），写入仍成功；`W_META_DROPPED` 告警可计数、可在日志定位

> 契约引用：`contracts/ledger-meta.v2.schema.json`、`contracts/ledger-meta.v2.contract.md`、`contracts/ledger-meta.v2.examples.json`（源：设计 §4.5、§4.6、§4.7）

### Requirement: 幂等写入与写入后置降级

系统 SHALL 支持幂等键写入，且派生状态（索引/投影）失败不回滚账本、不静默；覆盖 PRD CAP-07、CAP-09。

#### Scenario: 同键同内容重放不重复入账

- **GIVEN** 客户端已提交一次带 `idem=abc12345` 的写入并成功
- **WHEN** 用同一 `idem` 重放同内容写入（网络重试场景）
- **THEN** 返回首次写入的同一 `mid` 与结果，账本行数不变；不得产生第二条孪生条目

#### Scenario: 同键不同内容冲突

- **GIVEN** 已存在 `idem=abc12345` 对应内容 A
- **WHEN** 用同一 `idem` 提交内容 B
- **THEN** 返回 409（`E_IDEM_CONFLICT` 语义码）并说明冲突；不得覆盖或丢弃内容 A

#### Scenario: 索引同步失败不回滚账本

- **GIVEN** 账本写入成功但 `sync_index` 返回失败
- **WHEN** 查看写入响应与账本状态
- **THEN** 写入仍成功、账本可读、响应 `synced=false` 且带失败原因；索引滞后可经 API/CLI 重试入口或管理台「同步索引」补救；不得因此回滚账本

> 契约引用：`contracts/ledger-meta.v2.schema.json`（`idem` 键）、`contracts/contextpack.v1.schema.json`（`degraded` 透传）（源：设计 §4.8、§5.5）

### Requirement: 评测集 v2 与 dev/holdout 纪律

系统 SHALL 提供 ≥100 条真实查询评测集，覆盖 8 类能力并区分 dev/holdout，报告六字段可复现；覆盖 PRD EVA-01、EVA-04、EVA-05、EVA-07、RET-05。

#### Scenario: 条数与类目达标

- **GIVEN** 评测集 v2 数据集
- **WHEN** 运行数据集校验（`contracts/eval-dataset.v2.schema.json`）
- **THEN** 条数 ≥100、8 类各 ≥10、`class` 取值在 8 类枚举内、`split` 仅为 `dev`/`holdout`；非法样本被 Schema 拒绝

#### Scenario: holdout 不参与调参

- **GIVEN** 含 holdout 子集的数据集（holdout ≥20%、按类分层、同一事件族不跨 split）
- **WHEN** 调参或权重标定
- **THEN** 调参记录中 holdout 命中为 0；holdout 只在版本验收时评估一次；轮换有记录（时间/新增条数/旧 holdout 去向）

#### Scenario: 报告六字段与复跑一致

- **GIVEN** 同账本快照（`ledger_sha` 固定）与同一数据集版本
- **WHEN** 连续运行两次评测
- **THEN** 报告均含 `ledger_total`/`ledger_sha`/算法版本/模型/数据集版本/运行时间六字段；两次指标差异为 0；缺任一字段视为不可复现

#### Scenario: 真实与合成分列，跨规模不可比

- **GIVEN** 真实查询评测（22 条起，目标 ≥100 条）与 45 条合成基准
- **WHEN** 输出报告与对外描述
- **THEN** 两类报告分列且标注口径；合成指标必须带「合成」限定词；跨不同 `ledger_total` 的指标不得直接比较（以 `ledger_total`/`ledger_sha` 为准）

> 契约引用：`contracts/eval-dataset.v2.schema.json`、`contracts/eval-dataset.v2.examples.json`、`docs/GCMEM-评测集v2-分类与holdout规则.md`（源：设计 §10.1、§10.2、§10.3、§10.5、§10.7）

### Requirement: 五段诊断与双组指标

系统 SHALL 把检索质量与回答质量分开报告，并对每个失败样本给出五段归因；覆盖 PRD EVA-02、EVA-03、EVA-08。

#### Scenario: 双组指标并列

- **GIVEN** 一次评测运行
- **WHEN** 生成报告
- **THEN** 同一报告内并列「检索指标（Hit@k/Recall/MRR）」与「有证据回答正确率」两组；任一组缺失即报告校验失败；不得用检索指标代替回答质量

#### Scenario: 每个失败样本至少一个诊断码

- **GIVEN** 任一失败样本
- **WHEN** 运行诊断
- **THEN** 输出 `Capture`/`Encode`/`Retrieve`/`Compile`/`Answer` 五段之一（可多码）或 `UNKNOWN`；码表固定 5 类 + `UNKNOWN`，不得自造码；抽 20 条人工复核一致性 ≥80%

#### Scenario: 挖掘统计可追溯

- **GIVEN** 夜挖/捕获运行
- **WHEN** 查询 `/admin/api/mining-stats`
- **THEN** 每条统计可回溯到具体日期与通道（`sessions`/`calls`/`items`/`added`/`candidates`/`skipped`）；样本不足以做趋势结论时必须标注

> 契约引用：`contracts/eval-dataset.v2.schema.json`（`class`/`expect` 支撑归因）（源：设计 §10.4、§12.3）

### Requirement: 可回滚与开关清单

系统 SHALL 为 6 类新能力提供独立开关，默认保守、纯配置生效、关闭后行为回基线；覆盖 PRD CTX-07、OPS-06、EVA-06。

#### Scenario: 6 类开关齐备且默认关闭

- **GIVEN** 变更包 `design.md` §5 回滚开关清单
- **WHEN** 逐项核对
- **THEN** 6 类对象（ContextPack 编译接口 / v2 检索策略 / meta v2 新键 / 派生投影 / 幂等写入 / 四端适配）各有开关名、默认值（全部保守：`0`/`v1`/`off`）、关闭后行为、影响面、验证方式；无空列

#### Scenario: 关闭后与开启前一致

- **GIVEN** 新能力已开启并验证生效
- **WHEN** 关闭对应开关（不改代码、不重建）
- **THEN** 该能力行为回到 D0 前基线（响应形状、`mid` 集合、默认排序一致）；回归 113/113；开关状态在管理台系统页/指标可见

#### Scenario: 无消融报告不上线

- **GIVEN** 新检索通道/权重/算法变更提案
- **WHEN** 评估是否上线
- **THEN** 必须附消融表（至少 Hit@1/MRR/延迟三列）与回滚开关；门槛判断有书面结论；无报告即不合并

> 契约引用：`contracts/contextpack.v1.schema.json`（`degraded`/`trim` 回退可见性）、`design.md` §5（源：设计 §13.3、§13.4、§12.1）

### Requirement: 接口兼容与四端适配

系统 SHALL 保持 v1 端点与 MCP 5 工具行为冻结，新增能力只做加法，四端适配可独立启停；覆盖 PRD INT-01、INT-03、INT-04、INT-05、INT-08。

#### Scenario: v1 行为冻结

- **GIVEN** 现有 v1 端点（`/health`、`/stats`、`/v1/doctor`、`/v1/memories/*`、`/admin/api/*`）与 MCP 5 工具
- **WHEN** 升级后跑现有 113 条用例与契约测试
- **THEN** 响应形状、状态码、默认语义（活跃面/时间倒序/`include_superseded`）不变；新增字段只做可选扩展；新增 MCP 工具不替换 5 工具

#### Scenario: 错误码与降级语义一致

- **GIVEN** 非法请求（空 query、非法 type/sort、删除记忆、LLM 缺 key、gbrain 故障）
- **WHEN** 调用对应端点
- **THEN** 返回 400/403/422/503 与可读说明；删除恒 403；`degraded=true` 场景返回 200 + 标记（不算错误）；不得用 200 掩盖失败

#### Scenario: 四端可独立启停

- **GIVEN** 四端均已适配 ContextPack（逐端开关）
- **WHEN** 停用任一端的新能力或整体接入
- **THEN** 其余三端与主账不受影响；该端回退 v1 检索；每端有一次「检索 + 写入」实调记录

#### Scenario: 文档不先于实现

- **GIVEN** 接口文档与接入说明
- **WHEN** 核对文档中每个端点/工具
- **THEN** 均可对应到实际存在的路由或工具（脚本核对）；文档描述的必须是已存在行为，未实现能力标注「目标/未实现」

> 契约引用：`contracts/contextpack.v1.schema.json`（新增消费面）、`contracts/ledger-meta.v2.schema.json`（meta 过滤语法）（源：设计 §9.1、§9.3、§9.4、§9.5、§9.6）

### Requirement: 状态上界与不提升

系统 SHALL 保持文档与项目的状态上界，不因任务完成、测试通过或门禁通过而提升受控状态；覆盖 PRD GOV-09、SEC-05、通用门禁 U7。

#### Scenario: 门禁通过不提升状态

- **GIVEN** D0/D1 门禁全部 PASS、回归全绿
- **WHEN** 检查文档 frontmatter 与项目状态
- **THEN** 文档 `status` 仍为 `candidate`、项目仍为 `partial`；四禁词只在否定/禁止语境出现；任何提升需真实业务证据 + 项目群门禁 + 人工确认

#### Scenario: 过滤不宣传为权限

- **GIVEN** 文档、接口说明与界面文案
- **WHEN** 扫描 `meta`/`scope` 过滤相关表述
- **THEN** 只描述为「筛选/过滤」，不得表述为权限隔离或 ACL；「不是 ACL」必须显式写出（SEC-05）；无 ACL 实现代码

> 契约引用：`contracts/ledger-meta.v2.contract.md`（`scope` 非 ACL 口径）（源：PRD §0.2、§9.5 U7；设计 §11.5）

## MODIFIED Requirements

无。R0 对 v1 已实现能力只做可选扩展（新增 meta 键、新增 `/v2` 路径、新增 MCP 工具、新增返回字段），不改 v1 语义与账本行语法（设计 §4.6、§9.5）。

## 需求覆盖表（PRD ID → 本规格）

| PRD ID | 需求主题（简） | 本规格 Requirement | 场景数 |
|---|---|---|---:|
| CTX-01 | ContextPack v1 schema 冻结、六要素齐备 | ContextPack v1 契约冻结 | 3 |
| CTX-02 | 预算 ≤8 条 / ≤1500 tokens + `trim_reason` | ContextPack v1 契约冻结 | 3 |
| CTX-03 | 四端统一注入契约 | 四端统一消费与注入容错 | 4 |
| CTX-04 | 注入失败不阻塞、熔断 | 四端统一消费与注入容错 | 4 |
| CTX-05 | 解释面按需展开 | 四端统一消费与注入容错 | 4 |
| CTX-06 | 上下文去重与冲突消解 | 上下文去重与冲突消解 | 3 |
| CTX-07 | 新能力可开关与回退 | 可回滚与开关清单 | 3 |
| CTX-08 | 自适应预算分档（R2） | **不在本包**：属 D2/R2 目标，需评测分档数据 | — |
| CAP-03 | meta v2 四字段扩展 | meta v2 兼容契约 | 4 |
| CAP-07 | 幂等与并发安全 | 幂等写入与写入后置降级 | 3 |
| CAP-09 | 写入成功后才更新派生状态 | 幂等写入与写入后置降级 | 3 |
| RET-03 | 默认活跃语义 | 上下文去重与冲突消解 | 3 |
| RET-04 | 排序原因与来源回指 | ContextPack v1 契约冻结 / 四端消费 | 3 / 4 |
| RET-05 | 相关性排序不得退步 | 评测集 v2 与 dev/holdout 纪律 | 4 |
| RET-08 | 双时间语义（前置条件） | meta v2 兼容契约 | 4 |
| EVA-01 | ≥100 条真实评测集 | 评测集 v2 与 dev/holdout 纪律 | 4 |
| EVA-02 | 检索质量与回答质量分开报告 | 五段诊断与双组指标 | 3 |
| EVA-03 | 五段诊断归因 | 五段诊断与双组指标 | 3 |
| EVA-04 | 评测版本化六字段 | 评测集 v2 与 dev/holdout 纪律 | 4 |
| EVA-05 | 真实集与合成基准分列 | 评测集 v2 与 dev/holdout 纪律 | 4 |
| EVA-06 | 消融与上线门槛 | 可回滚与开关清单 | 3 |
| EVA-07 | 防过拟合（dev/holdout） | 评测集 v2 与 dev/holdout 纪律 | 4 |
| EVA-08 | 捕获与挖掘质量指标 | 五段诊断与双组指标 | 3 |
| INT-01 | HTTP v1 契约稳定 | 接口兼容与四端适配 | 4 |
| INT-02 | MCP 5 工具契约冻结 | 四端统一消费与注入容错 / 接口兼容 | 4 |
| INT-03 | 错误码与语义成文 | 接口兼容与四端适配 | 4 |
| INT-04 | 四端适配契约 | 接口兼容与四端适配 / 四端消费 | 4 |
| INT-05 | 兼容矩阵与弃用策略 | 接口兼容与四端适配 | 4 |
| INT-06 | Python 内嵌契约（壳层不下沉） | 接口兼容与四端适配（既有约束，不新增） | 4 |
| INT-07 | 默认语义一致（HTTP/MCP） | 四端统一消费与注入容错 | 4 |
| INT-08 | 接口文档与自检清单 | 接口兼容与四端适配 | 4 |
| OPS-06 | 新能力支持关闭与回退 | 可回滚与开关清单 | 3 |
| GOV-09 | 文档与运行一致性门禁 | 状态上界与不提升 | 2 |
| SEC-05 | 过滤不是 ACL | 状态上界与不提升 | 2 |

> 「场景数」列 = 所属 Requirement 的场景总数（同一 Requirement 被多条 PRD 需求共享，故不按 PRD ID 重复计数）；10 条 Requirement 合计 33 个场景。

**本包不覆盖的 PRD 需求（含理由）**

| 需求组 | 不覆盖理由 |
|---|---|
| MEM-01..09（分层记忆） | 属 D2（R1 分层记忆），本包 Non-goals；D0 仅冻结 meta 中 `memory_class` 键位 |
| CAP-01/02/04/05/06/08（写入统一管线/元数据补全/敏感守卫/替代链/情景结构/判重分层） | 已在现行实现中运行（【现有】），R0 不改语义；其中 CAP-06 情景结构属 R1 |
| RET-01/02/06/09/10/11（分类/多路/拒答/实体多跳/缓存/排序切换） | 分类与多路属 D3（R2）；拒答 R1 门槛在 R0 后评估；缓存与排序切换为现行行为，本包只要求其不退化 |
| GOV-01..08（治理动作与可视化） | 现行能力或属 R1（GOV-05/06 可视化与人工确认门禁），本包只引用 GOV-09 一致性门禁 |
| OPS-01..05、OPS-07..09 | 现行运维能力；本包只把 OPS-06 开关纳入回滚清单，OPS-01/02 RPO 由 WP-D1-06 承接 |
| SEC-01..04、SEC-06/07 | 现行安全边界；R0 不改变监听、凭据、脱敏与注入防护；SEC-06（ACL）明确不在本包 |

## 契约引用总表

| 契约文件 | 对应 Requirement | 设计源 | 产出 WP |
|---|---|---|---|
| `contracts/contextpack.v1.schema.json` | ContextPack v1 契约冻结 / 四端统一消费 / 上下文去重 | §7.5、§7.4 | WP-D0-02 |
| `contracts/contextpack.v1.examples.json` | ContextPack v1 契约冻结 | §7.5 | WP-D0-02 |
| `contracts/ledger-meta.v2.schema.json` | meta v2 兼容契约 / 幂等写入 | §4.5、§4.8 | WP-D0-03 |
| `contracts/ledger-meta.v2.contract.md` | meta v2 兼容契约 / 状态上界（`scope` 非 ACL） | §4.5、§4.6、§4.7、§11.5 | WP-D0-03 |
| `contracts/ledger-meta.v2.examples.json` | meta v2 兼容契约 | §4.5、§4.7 | WP-D0-03 |
| `contracts/eval-dataset.v2.schema.json` | 评测集 v2 与 dev/holdout 纪律 / 五段诊断 | §10.1、§10.2 | WP-D0-04 |
| `contracts/eval-dataset.v2.examples.json` | 评测集 v2 与 dev/holdout 纪律 | §10.2 | WP-D0-04 |
| `docs/GCMEM-评测集v2-分类与holdout规则.md` | 评测集 v2 与 dev/holdout 纪律 / 五段诊断 | §10.1、§10.3、§10.5 | WP-D0-04 |

## 验证与状态边界

1. **验证入口**：契约 → `PYTHONPATH= python3 scripts/validate_contracts.py`；行为 → 回归 113/113 + D1 新增用例；开关 → `design.md` §6.2 五步演练；四端 → 各端一次实调记录。
2. **判定纪律**：场景 THEN 中的每一条都必须可观察、可复跑；不可判定即视为场景未通过。
3. **状态边界**：本规格全部场景通过也不产生 `accepted` / `integrated` / `production_ready` / `customer_accepted`；也不代表功能已实现——实现证据以 `tasks.md` 对应 WP 的留证为准。
