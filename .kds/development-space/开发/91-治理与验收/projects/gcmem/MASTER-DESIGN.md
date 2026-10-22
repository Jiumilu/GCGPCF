---
doc_id: GPCF-DOC-2252D3D171
title: GCMEM 总体设计（v1.2 · 2026-10-20）
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.2
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gcmem/MASTER-DESIGN.md
source_path: projects/gcmem/MASTER-DESIGN.md
sync_direction: bidirectional
last_reviewed: 2026-10-20
supersedes: []
superseded_by: []
---

> 同步说明（2026-10-20，老卢授权 E4）：正文由 GCMEM 仓 `docs/docs/MASTER-DESIGN.md` 同步；事实源以 GCMEM 仓为最新，本副本随 E4 同步流程更新。

# GCMEM 总体设计（v1.1 · 2026-10-17）

## 1. 背景

mem0（云记忆）于 2026-10-16 因配额耗尽与数据主权考量退役。跨会话长期记忆需要**本地、单一主存、可审计、可自动迭代**的承载；KDS 已是知识事实主存、gbrain 已提供语义检索——长期记忆并入同一体系，不另立系统。

## 2. 定位

GCMEM ＝ 基于 KDS 的长期记忆服务：跨会话记忆的**唯一主存与迭代通道**。

## 3. 架构（四层一体）

| 层 | 载体 | 说明 |
|---|---|---|
| 记忆主存 | `KDS/_meta/hermes-memory-log.md` | append-only 账本；类型 fact / decision / correction / preference / entity |
| 语义检索 | gbrain（KDS 索引） | 定向 `import _meta --no-embed --include-gitignored` + `embed --stale`（≈3 秒） |
| 服务接口 | `~/.hermes/scripts/gcmem.py` | `add` / `search` / `sync` / `stats` / `candidates` / `import-candidates` |
| 自动迭代 | 夜间对话挖掘（23:00） | 当日对话 → 高置信记忆自动入账（≤8条/日、去重）→ 报告留存全量候选供人工/agent 复核 |

## 4. 数据流

对话（Hermes 全部会话，含小G 通道）→ 夜间挖掘 → 记忆提炼 → 账本（+来源标注）→ gbrain 索引 → 检索注入（会话 / 小G / 周报指标）

## 5. 迭代机制

1. **每夜**：挖掘提炼 → 自动入账（高置信：明确决策/纠正/偏好句式；去重、限量）→ 定向同步索引。
2. **每周**：体系进化周报统计「KDS 记忆条目数」。
3. **人工**：老卢或 agent 随时 `gcmem add` 补录、`import-candidates` 复核导入。

## 6. 验收与指标

- 检索可用：`gcmem search` 命中账本条目（2026-10-16 首验 0.91 ✓）。
- 自动迭代：连续 3 日挖掘产出 ≥1 条有效记忆（待验）。
- 索引时效：账本写入后 24h 内可被 gbrain 检索（由 sync 保证）。

## 7. 边界与风险

- 不建立第二套记忆主账；mem0 / cognee / local-jsonl 旧栈均为退役或降级对象（容器侧见 §9）。
- 记忆条目为 working 级，不改变业务事实与状态；噪声风险由去重、置信过滤与人工复核控制。

## 8. 与既有件关系

- **继承**：KDS 记忆迭代首版（账本＋脚本，2026-10-16）；Hermes 技能库 `hermes-agent → references/multi-session-contention.md`。
- **替代**：mem0（云记忆，已卸载）。
- **关联**：GKE-001 知识工程 —— 长期记忆条目受其上位规范约束，不得建立平行记忆主账。

## 9. 小G 记忆迁移（进行中）

容器侧 `xiaoji_memory_backend.py` / `xiaoji_mem0_memory.py` / `xiaoji_memory_patrol.py` 现依赖 mem0_local / cognee 旧栈。迁移目标：记忆读写走 GCMEM（账本＋gbrain）。迁移步骤与验收另行登记；迁移完成前不得声明小G 长期记忆已切换。

## 10. v1.1 增补（2026-10-17 · 全量评估后同步）

> 本节为 v1.0 正文的增量修订，v1.0 各节不逐条改写；与本节冲突处以本节为准。

1. **检索架构升级**（修订 §3 语义检索层）：检索主体 = 账本条目字级 bigram 本地排序（原文＋时间＋类型直出，零延迟）；gbrain 仅为补充命中（≤3 条）。gbrain 故障 / 超时 / 缺失时自动降级为仅本地结果（`degraded` 标记），补充通道故障不拖垮主通道。
2. **LLM 能力下沉核心**：`llm_extract`（对话提炼）与 `llm_judge`（语义判重 / 冲突合并）均实现于核心 `gcmem.py`，API / MCP / CLI 只做参数装配与错误映射。
3. **服务接口扩充**（修订 §3 服务接口）：`gcmem.py` CLI ＋ MCP server（stdio 零依赖，5 工具）＋ HTTP API（mem0 兼容 REST，127.0.0.1:19090，launchd 常驻 `ai.globalcloud.gcmem-api`）。
4. **四端共账本**：Hermes（provider 插件）/ Codex（MCP）/ Reasonix（MCP）/ DSH（技能，HTTP API 通道）读写同一账本，不做副本、不做同步逻辑。
5. **挖掘限量**：现行为 ≤3 条/日（v1.2 起施行；原 §3「≤8 条/日」为立项初版口径）。
6. **并发与完整性加固**（2026-10-17 全量评估）：`_append` 读-改-写全程 fcntl 文件锁＋线程锁（四端并发写无丢失）；写入统一净化换行/控制字符；text ≤300 全入口显式校验（超长拒绝，不静默截断）；非法 type 显式拒绝；`cmd_sync` 走 `_gbrain_bin()` 绝对路径回退（launchd PATH 安全）。
7. **metadata 过滤**（v1.5.1）：检索 / 读取支持 meta 过滤（AND），meta 格式 `k=v;k2=v2`（key 限 `\w+`）。

## 11. v1.2 增补（2026-10-20 · 实现现状对齐）

> 本节为 v1.0/v1.1 之后的增量修订；与前述冲突处以本节为准。

1. **四端接入补齐**：Hermes（provider 插件：预取注入 + 即时捕获）、Codex/Reasonix（MCP stdio）、DSH（技能 HTTP 通道 + 自动捕获桥 `~/.hermes/scripts/gcmem_dsh_capture.py`，launchd 双服务）。
2. **挖掘双通道**：Hermes 侧夜间对话挖掘（23:00，仅 correction/preference 自动入账，≤8 条/日）+ DSH 侧日终 LLM 挖掘（23:40，`llm_extract`：correction/preference 自动入账 ≤10 条/日、走 `infer` 语义判重，其余进候选文件）。§3「≤8 条/日」与 §10.5「≤3 条/日」口径作废，以本节为准。
3. **即时捕获口径**：Hermes sync_turn 与 DSH 桥复用 `gcmem.py capture` 句式门控（correction/preference，含「记住/记下/记一下」）；新增 `is_sensitive` 凭据守卫（token/令牌/密钥/密码/secret/bearer/长随机串一律不入账）。
4. **列表默认语义与排序**：`/v1/memories/` 与 MCP `gcmem_get` 默认只返回活跃记忆（`include_superseded=true` 走审计面）；列表接口统一默认**最近时间优先**（time/desc），支持 `sort`/`order`；管理台表头可点击切排序。
5. **防重复**：写入统一判重（相同/包含 + 可选 LLM 语义判重）；DSH 挖掘另加 difflib ≥0.90 近似重复守卫；历史近似重复以 append-only 替代链处置，不物理删除。
6. **检索指标基线（2026-10-20）**：45 条合成查询 top1/top3 命中 100%；本地检索链 0.38ms（2000 条约 6.9ms）；字符串判重准确率 100%（报告 `tests/bench_gcmem_report.json`）。
7. **验收状态**：回归 **113/113**；doctor healthy、notes 归零；连续三日夜挖验收（A1）与四端客户端新会话回归（A2）进行中，见 `docs/GCMEM-下一迭代规划.md`；`overall_status` 仍为 `partial`。
8. **运行与备份（2026-10-20）**：API 进程内运行指标 `GET /admin/api/metrics`（请求/错误/分组延迟 P50/P95/写入速率/LLM 判重统计，重启清零）；账本每日 23:50 快照（launchd `ai.globalcloud.gcmem-backup`，落 `~/.hermes/backups/gcmem-ledger/` + sha256，不自动删除）；恢复流程与演练见 `docs/GCMEM-备份恢复演练.md`。
