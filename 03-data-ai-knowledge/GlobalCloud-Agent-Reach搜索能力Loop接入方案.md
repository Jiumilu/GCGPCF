---
doc_id: GPCF-DOC-A4F06F496D
title: GlobalCloud Agent-Reach搜索能力Loop接入方案
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud-Agent-Reach搜索能力Loop接入方案.md
source_path: 03-data-ai-knowledge/GlobalCloud-Agent-Reach搜索能力Loop接入方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud Agent-Reach搜索能力Loop接入方案

## 1. 接入结论

Agent-Reach 可以作为 GlobalCloud Loop 的外部搜索、网页读取、平台资料发现和工具健康诊断候选能力包，但不得直接登记为已集成生产能力。

本方案只允许把 Agent-Reach 纳入 `candidate_search_capability` 和 `research_input` 层。Agent-Reach 输出不得直接升级为 KDS canonical Markdown、GFIS source-of-record、WAES accepted evidence、GPCF integrated 状态或生产可用声明。

## 2. 当前只读核查事实

| 项 | 事实 |
|---|---|
| 仓库 | `https://github.com/Panniantong/Agent-Reach.git` |
| 本轮核查方式 | 临时目录只读克隆，未写入 GPCF 项目仓 |
| 包类型 | Python CLI 包 |
| 包名 | `agent-reach` |
| 核查版本 | `1.5.0` |
| Python 要求 | `>=3.10` |
| 核心定位 | 安装、配置、诊断、渠道路由能力层 |
| 实际读取方式 | Agent 直接调用上游工具或 MCP 后端 |
| 默认禁止 | Cookie 写入 Git、真实账号自动配置、生产环境自动安装、真实外部平台写入 |

## 3. Loop 纳入层级

| 阶段 | 名称 | 允许动作 | 禁止动作 | 输出 |
|---|---|---|---|---|
| L0 | 只读评估 | 阅读源码、README、许可证、依赖、风险 | 安装、配置 Cookie、修改 MCP、调用登录平台 | 评估文档 |
| L1 | 受控方案 | 建立接入方案、指标、门禁、回滚要求 | 宣称已集成、写入 KDS canonical、升级状态 | 本文档与 validator |
| L2 | 隔离 PoC | 独立虚拟环境、`agent-reach doctor --json`、固定查询集 benchmark | 使用主账号 Cookie、写生产系统、改项目主状态 | evidence JSON/Markdown |
| L3 | 托管轮次 | 在明确授权后连续跑搜索质量、速度、引用强度、fallback 测试 | 真实平台批量抓取、绕过风控、生产写入 | Loop round 与门禁结果 |
| L3.5 | 受控真实接口验证 | 白名单 API 读、登录态只读验证、可回滚单点测试 | 批量写、删除、权限变更、不可回滚动作 | 接口验证 evidence |
| L4/L5 | 自动运营/生产自治 | 仅在单独强授权后评估 | 默认不得进入 | 单独授权包 |

## 4. 能力边界

### 4.1 可使用能力

| 能力 | GlobalCloud 用途 | 证据要求 |
|---|---|---|
| 网页读取 | 读取公开政策、标准、供应链资料、项目页面 | URL、抓取时间、摘要、引用片段、失败状态 |
| GitHub 仓库读取 | 分析开源仓库、Issue、Release、依赖风险 | repo、commit 或 release、命令输出摘要 |
| RSS | 订阅政策、标准、行业网站更新 | feed URL、item id、发布时间 |
| YouTube/B站 | 提取公开技术视频字幕或搜索结果 | 视频 URL、字幕来源、时间戳 |
| Exa 搜索 | 全网语义检索和候选来源发现 | query、top-k、引用 URL、重复率 |
| Twitter/Reddit/小红书 | 舆情与经验线索候选 | 登录态来源、专用小号、平台风险提示、弱引用标记 |

### 4.2 不可替代能力

Agent-Reach 不替代以下系统：

| 系统 | 不可替代原因 |
|---|---|
| KDS | KDS 是知识主存，Agent-Reach 只能发现候选来源 |
| Brain | Brain 是知识编制与知识 UI 平台，Agent-Reach 不是发布面 |
| WAES | WAES 是证据、门禁、风险和状态裁决层 |
| GFIS | GFIS 是工厂执行系统和工厂事实主账 |
| GPC | GPC 是绿色供应链公共服务平台本体 |

## 5. 搜索质量指标

每轮 PoC 或 L3 搜索轮次必须输出以下指标。

| 指标 | 目标 | 不达标处理 |
|---|---:|---|
| `doctor_available_channel_rate` | >= 60% | 降级为 L1 方案态 |
| `search_success_rate` | >= 80% | 记录失败渠道与 fallback |
| `citation_validity_rate` | >= 90% | 低于目标不得进入 RAG 强引用 |
| `source_provenance_rate` | 100% | 缺 provenance 的结果全部降为候选 |
| `duplicate_rate` | <= 20% | 去重规则进入下一轮 |
| `latency_p50_seconds` | <= 10 | 标记效率债务 |
| `latency_p95_seconds` | <= 30 | 标记效率债务 |
| `fallback_success_rate` | >= 70% | 后端路由待修复 |
| `credential_leakage_count` | 0 | 立即 hard_stop |
| `production_write_count` | 0 | 立即 hard_stop |

## 6. 引用强度映射

| Agent-Reach 来源 | 默认 TrustLevel | 默认 RAG Admission | 升级条件 |
|---|---|---|---|
| 权威政策、标准、官方网站 | T1 | limited | 保留版本、日期、适用范围后可申请 safe |
| 合作单位公开资料 | T2 | limited | 人工确认和 WAES 证据后可申请 safe |
| GitHub 官方仓库 | T2/T3 | limited | 绑定 commit/release、许可证和维护状态后提升 |
| 第三方文章、搜索结果 | T4 | limited 或 repair_required | 交叉验证后提升 |
| 社交平台内容 | T4 | repair_required | 只能作为线索，需独立来源确认 |
| AI 总结结果 | T5 | blocked | 绑定真实来源并经 WAES 后才可进入召回 |

## 7. 安全与凭据规则

1. 禁止把 Cookie、Token、代理账号、浏览器登录态导出内容写入 Git。
2. 禁止把 Cookie、Token、代理账号、浏览器登录态导出内容写入 `.kds/`、Loop evidence、日志或 Markdown 正文。
3. Twitter、Reddit、小红书等登录态平台必须使用专用小号，不得使用主账号。
4. 生产服务器默认只允许 `--safe` 或 `--dry-run`，不得自动安装系统包。
5. 本地 PoC 必须使用隔离目录和可删除虚拟环境。
6. MCP 配置修改必须单独授权，并记录回滚步骤。
7. 任何平台风控、403、验证码、封号风险必须进入 evidence，不得绕过。

## 8. Definition of Done

L1 接入方案完成的最低标准：

- 本文档存在并包含受控 frontmatter。
- 明确 Agent-Reach 是候选搜索能力包，不是生产集成能力。
- 明确 L0 到 L3.5 纳入边界。
- 明确搜索质量、效率、引用、fallback、安全指标。
- 明确凭据和 Cookie 禁写规则。
- 明确不得替代 KDS、Brain、WAES、GFIS、GPC。
- `python3 tools/kds-sync/validate_agent_reach_loop_admission.py` 输出 pass。

L2 隔离 PoC 的最低标准：

- 使用独立虚拟环境或临时工具目录。
- 输出 `agent-reach doctor --json` 结果。
- 至少覆盖公开网页、GitHub、RSS、语义搜索 4 类只读渠道。
- 每条结果保留来源、时间、失败原因和引用强度。
- 不写真实外部平台，不写生产系统，不写真实 KDS API。

## 9. 下一轮候选输入

| Round | 输入 | 动作 | 检查 | 反馈 |
|---|---|---|---|---|
| GPCF-AGENT-REACH-L1-001 | 本方案 | 运行 validator | L1 pass | 是否授权 L2 PoC |
| GPCF-AGENT-REACH-L2-001 | L2 授权 | 隔离安装与 doctor | 渠道可用率 | 选择可用渠道 |
| GPCF-AGENT-REACH-BENCH-001 | 固定查询集 | 搜索 benchmark | 质量和延迟指标 | 调整 fallback |
| GPCF-AGENT-REACH-GOV-001 | 安全策略 | Cookie/MCP/日志门禁 | 泄露数为 0 | 决定是否进入 L3 |

## 10. 非声明

本文档不声明：

- Agent-Reach 已安装到 GlobalCloud 运行环境。
- Agent-Reach 已接入真实 KDS、Brain、WAES、GFIS 或 GPC。
- 任何登录平台 Cookie 已配置。
- 任何真实外部 API 已调用或写入。
- GFIS runtime SOP E2E 已通过。
- GPCF L4 聚合门禁已修复。
- 任何项目状态可升级到 accepted、integrated 或 production_ready。
