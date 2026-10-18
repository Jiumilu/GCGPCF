---
doc_id: GPCF-DOC-GCMEM-MEM0-CMP
title: GCMEM 与 mem0 全量对比（v1.5 · 2026-10-17）
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gcmem/GCMEM-vs-mem0-对比.md
source_path: projects/gcmem/GCMEM-vs-mem0-对比.md
sync_direction: bidirectional
last_reviewed: 2026-10-17
supersedes: []
superseded_by: []
---

# GCMEM 与 mem0 全量对比（v1.5）

> 基准日：2026-10-17。GCMEM 侧为本地实测事实；mem0 侧基于开源项目（mem0ai/mem0）公开能力，非本机实测。

## 结论

**GCMEM v1.5 已全面达到 mem0 的功能面**（写入提炼、语义判重、冲突合并、多端接口、历史追溯均实测闭环）；在**审计性、数据主权、多端覆盖**上超过 mem0；在**真更新/真删除、元数据过滤、run_id 级作用域、多向量库**上存在有意的设计取舍（见 §4），全部有替代路径或补救方案。

## 全量对比表

| # | 维度 | mem0 | GCMEM v1.5 | 判定 |
|---|---|---|---|---|
| 1 | 定位形态 | 开源 SDK + 云平台（mem0 platform） | 本地服务：账本+API+MCP+CLI | 均可用，GCMEM 全本地 |
| 2 | 存储 | 向量库（Qdrant/Chroma/Weaviate…）+ SQLite | append-only markdown 账本 + gbrain 索引 | GCMEM 可审计性更强 |
| 3 | 写入 add | LLM 自动提取事实 + 三态判断（add/update/duplicate） | CLI 判重（归一化+相似）＋ API/MCP `infer` 走 LLM 三态判断（duplicate/supersede/add） | 对齐（实测同义改写拒写） |
| 4 | 对话提炼 | FACT_EXTRACTION 提示词自动提炼 | `llm_extract`（API messages 模式，实测提炼 2 条）+ 夜挖自动迭代（23:00+12:30 双档） | 对齐且多一层夜间挖掘 |
| 5 | 更新 update | 真更新（改原记忆，history 保留） | 新条目+替代标注（sup 链），PUT /{mid} | 等价语义；GCMEM 不可变账本，审计更强 |
| 6 | 删除 delete | 真删除 | 403 政策（append-only 禁删） | 设计取舍：GCMEM 永不丢史 |
| 7 | 检索 search | 向量+阈值+recency 加权+元数据过滤 | 账本条目 bigram 本地排序（原文+时间+类型直出）+ gbrain 语义补充；sort=relevance/recency/blend | 对齐（检索质量实测优于纯向量命中 chunk 标题） |
| 8 | 相关性过滤 | 阈值参数 | 分数直出、调用端自行取舍；注入阈值 0.45（Hermes） | 对齐 |
| 9 | 历史 history | 操作历史（events 表） | 替代链 GET /{mid}/history（sup 链上下游闭合，实测） | 对齐（口径=记忆版本史） |
| 10 | 多租户 | user_id / agent_id / run_id 三级过滤 | src 标注 + agent 过滤 get_all（四端已各打各的 src） | 二级对齐；缺 run_id 级 |
| 11 | 元数据过滤 | metadata 键值过滤 | 仅 type / agent / 时间排序 | 差距（见 §4） |
| 12 | 接口面 | Python/TS SDK、REST（OpenMemory） | REST（mem0 风格 8 端点）＋ MCP（5 工具）＋ CLI（9 子命令）＋ Hermes provider 插件＋ DSH 技能 | 覆盖更广（四端实测） |
| 13 | LLM 后端 | OpenAI/DeepSeek/Ollama… 可换 | DeepSeek chat 直连（判重/提炼） | 对齐（单一供应商，够用） |
| 14 | 嵌入/向量 | 可换（openai/fastembed/ollama） | gbrain 语义索引（KDS 体系内） | 对齐（体系化） |
| 15 | 自动迭代 | 无内置（靠 SDK 调用方） | 夜挖自动入账（≤条数/日+门控）+ 日中档 + 候选留存 | GCMEM 超出 |
| 16 | 运维/工程化 | 依赖调用方 | doctor 巡检、回归 22/22、熔断器（5 败 120s）、launchd 常驻、备份纪律、`GCMEM_LEDGER_PATH` 测试注入 | GCMEM 超出 |
| 17 | 数据主权 | 云平台数据出境 | 全本地（KDS 账本） | GCMEM 超出 |
| 18 | 成本 | 云配额（曾因配额耗尽退役） | 零存储；LLM 判重≈¥0.001/次 | GCMEM 超出 |

## 差距清单与补救

| 差距 | 影响 | 补救方案 | 状态 |
|---|---|---|---|
| ~~无 metadata 键值过滤~~ | ~~调用方按自定义维度筛记忆~~ | ~~API search/get_all 加 metadata 参数~~ | ✅ 已补（v1.5.1，2026-10-17）：条目行尾 `· meta:k=v;…`，API/MCP/CLI 全链支持，过滤 AND 语义，回归 26/26 |
| 无 run_id 级作用域 | 单会话级记忆隔离 | 账本加 `· run:` 标注即可（格式已支持 src 同级扩展） | 低（暂缓） |
| 检索无多向量库/重排 | 大规模（>1万条）时 bigram 本地排序退化 | 账本达千条级再评估：接 KDS 已有多路召回或 LLM rerank | 低（当前 35 条） |
| 单一 LLM 供应商 | DeepSeek 不可用时判重/提炼降级为字符串路径 | 已内置降级（infer 失败→快路径，不阻塞写入） | 低 |

## 边界声明

- GCMEM 侧全部能力经本机实测（检索 0.09-0.95 命中、同义改写拒写、替代链闭环、四端实弹）。
- mem0 侧为其开源文档声明的能力；「真更新/真删除」等为默认行为，未在本机复验。
- 本对比不含 mem0 云平台的企业功能（SSO/审计台/团队空间），老卢场景（单用户多端）无需。
