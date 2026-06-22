---
doc_id: GPCF-DOC-AGENT-REACH-FULL-IMPLEMENTATION-20260622
title: GlobalCloud 项目群 Agent-Reach 全量实施方案与执行提示词
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群Agent-Reach全量实施方案与执行提示词.md
source_path: 02-governance/GlobalCloud项目群Agent-Reach全量实施方案与执行提示词.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Agent-Reach 全量实施方案与执行提示词

日期：2026-06-22
状态：全量实施蓝图 / 授权前受控方案

## 1. 执行结论

`Panniantong/Agent-Reach` 可以作为 GlobalCloud 项目群的互联网触达能力层进入 Loop，但当前仍必须保持 `limited_candidate_only`。

本轮核验的上游状态：

| 项 | 值 |
| --- | --- |
| upstream repo | `https://github.com/Panniantong/Agent-Reach.git` |
| upstream HEAD | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| package version | `1.5.0` |
| python requirement | `>=3.10` |
| license | `MIT` |
| current GlobalCloud admission | `limited_candidate_only` |

Agent-Reach 在 GlobalCloud 的角色是：

```text
互联网搜索与读取能力层
多渠道后端选择与健康检查
固定查询 benchmark 与回归门禁对象
KDS / WAES / Brain / Harness 的候选外部证据入口
```

Agent-Reach 不得被定位为：

```text
KDS 事实主存
WAES 裁决源
GFIS 运行层 source-of-record
生产配置自动写入器
accepted / integrated / production_ready 的自动升级依据
```

## 2. 全量能力范围

| 能力域 | Agent-Reach 上游能力 | GlobalCloud 首轮用途 | 首轮状态上限 |
| --- | --- | --- | --- |
| Web | Jina Reader 读取网页 | 外部页面候选引用、政策/标准公开页候选 | limited candidate |
| Search | Exa via mcporter | 固定查询 benchmark、候选来源发现 | limited candidate |
| GitHub | gh CLI | 仓库、Issue、PR、release 读取候选 | controlled pilot |
| YouTube | yt-dlp 字幕/信息 | 视频教程/公开演示的候选摘要 | controlled pilot |
| RSS | feedparser | 标准、政策、项目 release feed 订阅候选 | controlled pilot |
| Bilibili | bili-cli / OpenCLI | 中文视频资料候选，不作为业务事实 | controlled pilot |
| V2EX | public API | 工程问题舆情与社区经验候选 | controlled pilot |
| Xueqiu | 行情/帖子读取 | 金融/碳资产讨论候选，禁止替代财务事实 | gated pilot |
| Twitter/X | twitter-cli / OpenCLI | 舆情和技术动态候选，需登录态安全门禁 | gated pilot |
| Reddit | OpenCLI / rdt-cli | 社区问题与讨论候选，需登录态安全门禁 | gated pilot |
| Xiaohongshu | OpenCLI / xiaohongshu-mcp | 市场口碑候选，需专用账号和反污染门禁 | gated pilot |
| LinkedIn | MCP / Jina Reader | 公司/职位/公开 profile 候选 | gated pilot |
| Xiaoyuzhou | Whisper 转写 | 播客资料候选，需转写凭据安全门禁 | gated pilot |
| Doctor | `agent-reach doctor --json` | 通道健康、active backend、缺口诊断 | mandatory |
| Watch | `agent-reach watch` | 定期健康检查和更新提示候选 | controlled pilot |
| Update | `agent-reach check-update` | 上游变化监控 | controlled pilot |
| Skill | `agent-reach skill --install` | 智能体使用指南候选 | authorization required |

## 3. 项目群接入矩阵

| 项目/域 | 接入对象 | 允许动作 | 禁止动作 |
| --- | --- | --- | --- |
| GPCF | Loop 控制板、证据链、validator | 定义门禁、记录能力状态、回放 benchmark | 自动 accepted / integrated |
| KDS | 候选引用、metadata-only、RAG review queue | 生成候选索引和来源追溯 | 写 canonical Markdown |
| WAES | 风险、合规、证据裁决输入 | 审查候选证据与来源可信度 | 替代 WAES 裁决 |
| Brain | 外部检索辅助、知识工作台候选 | 读取和摘要外部候选 | 替代 KDS 主存 |
| GFIS | 供应商、政策、标准、公开资料发现 | 生成待人工核验候选 | 创建 source-of-record |
| GPC | 供应链协作公开资料候选 | 辅助调研和证据链接 | 写业务事实主账 |
| PVAOS | 伙伴公开信息候选 | 受控调研 | 写组织配置 |
| PKC | 个人知识候选 | metadata-only 收藏候选 | 写正式 KDS 事实 |
| XiaoC | 任务调研工具候选 | 受控调用计划 | 真实外部写入 |
| XGD | 风险分析外部材料候选 | 搜索质量回归检查 | 生产自动化 |
| XiaoG | 只读查询辅助候选 | read-only 调研 | 设备或生产写入 |
| MMC | 模板和公开资料候选 | 文档候选补充 | 发布模板 |
| Studio | workflow / release 外部资料候选 | 只读调研 | release write |
| WAS | ontology / OKF 外部公开资料候选 | 语义契约来源候选 | 替代 KDS source of record |

## 4. 阶段实施路线

| 阶段 | 目标 | 主要产物 | 升级条件 |
| --- | --- | --- | --- |
| P0 Source Lock | 锁定上游版本、license、安全边界 | `third_party/agent-reach/*` 审查包 | license/security/source validator pass |
| P1 Isolated Install | 临时 HOME / venv / npm prefix 安装 | install log、doctor JSON、uninstall replay | 无凭据泄露、rollback pass |
| P2 Channel Doctor | 全通道健康基线 | channel matrix、active backend ledger | doctor schema pass |
| P3 Fixed Query Benchmark | 固定查询搜索质量基线 | replay ledger、latency、source provenance | regression gate pass |
| P4 Candidate Ingestion | 候选 metadata-only 摄取 | KDS/WAES review queue dry-run | canonical write count = 0 |
| P5 Project Group Routing | 14 项目/域路由策略 | route policy、allow/deny matrix | 每项目边界 validator pass |
| P6 Authorized Read-Only Live | L3.5 受控真实接口读验证 | endpoint summary、response schema、redaction log | 显式授权字段完整 |
| P7 Human Review | WAES/KDS/owner 人审闭环 | decision ledger、reject reason、promotion request | review quorum pass |
| P8 Controlled Production Admission | 生产前准入包 | rollout plan、rollback plan、monitoring plan | 单独人工批准 |

## 5. 完整实施提示词

将以下提示词交给下一轮执行代理使用：

```text
你是 GlobalCloud 项目群 Agent-Reach 全量能力实施代理。你的目标是在 GPCF Loop 中把 Panniantong/Agent-Reach 作为互联网触达能力层受控纳入项目群，使其提升搜索能力、效率与质量，并建立可持续进化机制。

【硬边界】
1. 当前状态最高为 limited_candidate_only，除非存在单独 WAES/KDS/Owner 明确批准，不得声明 accepted、integrated 或 production_ready。
2. Agent-Reach 只能作为互联网搜索/读取/通道健康检查能力层；不得替代 KDS 事实主存、WAES 裁决、GFIS source-of-record、Brain 知识主存或 Harness 证据验收。
3. 未授权前不得写 KDS canonical Markdown，不得写 GFIS source-of-record，不得写 production configuration，不得写全局 MCP 配置，不得泄露 token/cookie/proxy。
4. 任何外部搜索结果只能先进入 candidate metadata / review queue，必须保留 source provenance、timestamp、query、backend、latency、content hash、review status、rollback path。
5. 任何需要登录态的通道必须使用专用账号、最小权限、可撤销凭据；凭据只允许进入本机受保护配置，禁止进入 Git、文档、日志、evidence。

【当前上游事实】
repo=https://github.com/Panniantong/Agent-Reach.git
verified_head=22d7f03a59401b5740b380c3ad43e3ff7a9dc373
version=1.5.0
python=>=3.10
license=MIT
supported_channels=web, exa_search, github, youtube, rss, bilibili, v2ex, xueqiu, twitter, reddit, xiaohongshu, linkedin, xiaoyuzhou
required_health_command=agent-reach doctor --json

【目标架构】
GlobalCloud Loop 调度 Agent-Reach；Agent-Reach 只负责安装、健康检查、后端路由和搜索/读取能力发现；实际外部内容进入 Harness evidence；WAES 负责风险和准入判定；KDS 负责受控候选索引和最终事实主存；Brain 可使用候选内容做工作台辅助；GFIS/GPC/PVAOS/PKC/XiaoC/XGD/XiaoG/MMC/Studio/WAS 只能按各自 allow/deny matrix 使用候选结果。

【执行阶段】
P0 Source Lock:
- 克隆上游到隔离目录，不写项目生产配置。
- 记录 upstream HEAD、version、license、dependencies、entrypoints、supported channels。
- 产出 OSS_REVIEW、SECURITY_REVIEW、SOURCE、VERSION.lock、MODIFICATIONS。
- 验证：license=MIT，source_head 已锁定，token/cookie 未出现。

P1 Isolated Install:
- 使用临时 HOME、临时 Python venv、临时 npm prefix。
- 执行 install --dry-run，再执行 safe/isolated install。
- 运行 agent-reach doctor --json。
- 执行 uninstall --dry-run 和 rollback 验证。
- 验证：无 ~/.agent-reach 生产配置污染，无全局 MCP 配置污染，rollback pass。

P2 Channel Doctor:
- 将 doctor JSON 转为 channel matrix。
- 每个 channel 必须记录 tier、backends、active_backend、status、message、required credential。
- 对登录态通道标记 gated_pilot，不得自动启用。
- 验证：所有通道有明确 allow/deny 状态。

P3 Fixed Query Benchmark:
- 使用固定查询集覆盖政策/标准/开源工具/供应链/Agent-Reach 自身。
- 每次查询记录 query、backend、latency、result_count、source_count、duplicate_count、failure_reason。
- 质量门禁：search_success_rate >= 0.8；source_provenance_rate == 1.0；duplicate_rate <= 0.2；p50 <= 10s；p95 <= 30s。
- 负向夹具必须覆盖缺失来源、重复率退化、canonical 写入企图、production 写入企图、未授权状态升级。

P4 Candidate Ingestion:
- 只生成 candidate metadata ledger，不写 canonical。
- 每条候选必须有 source provenance、accepted scope、blocked outputs、review status、rollback path。
- 硬门禁：canonical_write_count = 0，production_write_count = 0，credential_leakage_count = 0。
- WAES/KDS review 决策必须独立记录，搜索成功不能替代人审或门禁。

P5 Project Group Routing:
- 为 GPCF、KDS、WAES、Brain、GFIS、GPC、PVAOS、PKC、XiaoC、XGD、XiaoG、MMC、Studio、WAS 分别定义 allow/deny matrix。
- 每个项目只允许只读调研、候选引用、metadata-only 或 dry-run；涉及业务事实、生产写入、配置变更、真实接口写入时必须阻断。

P6 Authorized Read-Only Live:
- 只有收到“启动 Loop L3.5 受控真实接口验证模式”且授权字段完整时执行。
- 授权字段必须包含项目、环境、API、时间窗、允许动作、禁止动作、回滚策略、验收指标。
- 仅允许真实 API 读、真实鉴权、validate-only、sandbox/staging 或单条可回滚测试写入。

P7 Human Review:
- 建立 WAES/KDS/项目 owner review ledger。
- 每条候选决策只能是 accept_limited、reject、needs_more_evidence、promotion_requested。
- promotion_requested 不等于 accepted/integrated。

P8 Controlled Production Admission:
- 生产准入必须单独批准。
- 必须有 rollout plan、monitoring plan、rollback plan、credential rotation plan、abuse/rate-limit plan、failure-mode playbook。
- 机器状态字段必须保持 production_admission=false，直到单独人工批准并完成准入包。
- 未通过前状态保持 limited_candidate_only 或 controlled_pilot。

【必须输出】
1. docs/harness/evidence/agent-reach-full-implementation-*.json
2. docs/harness/evidence/agent-reach-full-implementation-*.md
3. docs/harness/loops/loop-round-GPCF-AGENT-REACH-FULL-IMPLEMENTATION-*.md
4. tools/kds-sync/validate_agent_reach_full_implementation_*.py
5. third_party/agent-reach/ 审查包，只有在 P0 执行时创建

【每轮验证】
- python3 tools/kds-sync/validate_agent_reach_full_implementation_*.py
- python3 tools/kds-sync/check_document_pollution.py
- python3 tools/kds-sync/validate_kds_token.py
- python3 tools/kds-sync/loop_document_gate.py
- git diff --check -- 本轮文件
- codegraph sync . && codegraph status --json .

【完成定义】
只有当 P0-P8 全部有 evidence、validator、WAES/KDS review、rollback、credential safety、regression benchmark 和人工生产准入时，才可申请 production admission。否则只能报告当前阶段状态，不能宣称全量完成。
```

## 6. 本轮目标和下一步

本轮建立 `GPCF-AGENT-REACH-FULL-IMPLEMENTATION-GOAL-001`，只完成全量实施提示词和阶段目标，不执行 P0 隔离安装、不调用 live external search、不升级状态。

下一轮进入：

```text
GPCF-AGENT-REACH-P0-SOURCE-LOCK-001
```

目标是锁定上游源、license、安全边界和依赖入口，并生成 `third_party/agent-reach/` 审查包。
