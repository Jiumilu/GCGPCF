---
doc_id: GPCF-DOC-F029-JOURNAL
title: F-029 hermes-ai-runtime-admission
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-029-hermes-ai-runtime-admission/journal.md
source_path: features/active/F-029-hermes-ai-runtime-admission/journal.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# F-029 hermes-ai-runtime-admission

## LOOP 日志

### Iteration 0

1. 这轮做什么？
   - 创建 Feature Workspace。
2. 改了什么？
   - 初始化 feature.yaml、journal.md、evidence/、artifacts/。
3. 怎么验证？
   - 关闭前运行 gpcf_check_evidence.py。
4. 发现什么问题？
   - none
5. 是否可以提交？
   - 否，Evidence Gate 仍待验证。

### 2026-10-18 P0 预检与交接准备

- GPCF 技能链初次复核覆盖 24 个项目；本轮并行变更又将 Project 纳入注册表，最新复核覆盖 25 项并通过校验。文档门禁初次通过，但状态上限为 `partial`。
- Hermes API 8642 有监听；`/v1/skills` 的 500 与不兼容调用参数对应，证据见 `evidence/p0-preflight-20261018.json`。
- 对外域名是独立 Web UI，现返回 502；本机 8648 未监听。隧道与远端代理尚未核验，不宣称单一根因。
- DSH 交接包见 `artifacts/dsh-handoff-20261018.json`；尚无接收确认，责任仍在 Codex/GPCF。
- `dsh` 命令和 headless 参数可用，但实际 headless 调用返回 `MISSING_CREDENTIAL`；未复制 Hermes 的 DeepSeek 密钥给 DSH。
- `gpcf_check_evidence.py F-029 --check-only` 返回 `close_candidate=false`：测试、构建证据及治理阻塞未闭合。
- Hermes 生产源码、服务重启与公开入口恢复均未执行；试点项目、替补与告警通道仍待确定。
- 静态核对 18 个 Hermes Profile，只有 `gccenter` 的 Profile 环境文件声明独立 API key；这是配置线索，不代替运行权限隔离测试。证据见 `evidence/hermes-profile-static-inventory-20261018.json`。

### 2026-10-18 Hermes 本机接口修复

- 用户明确授权备份、修正 `/v1/skills` 参数不兼容、运行定向测试并重启本机 Hermes 网关；DSH 凭据由用户自行配置。对外 Web UI 未获本次恢复授权。
- 两个目标文件备份于 `/private/tmp/gpcf-hermes-f029-backup-20261018-111439`；仅删除不受支持的 `include_editorial` 调用参数，并在现有接口测试中校验调用契约。
- Hermes 规定脚本 `scripts/run_tests.sh tests/gateway/test_api_server.py -k skills -q`：1 通过。完整同文件测试：98 通过、16 失败；抽查一项失败定位于测试隔离守卫拒绝读取真实 Hermes 主目录 `manifest.json`。其余失败待 DSH 逐项复核。
- 已重启本机 `ai.hermes.gateway`；启动延迟后 API 8642 恢复监听。认证复测：`/health/detailed` 200、`/v1/models` 200、`/v1/skills` 200（274 条）；未认证 `/v1/skills` 为 401。证据见 `evidence/hermes-skills-repair-20261018.json`。
- DSH 交接包仍为待送达和待回执；正式试点继续受 Web UI、权限隔离、替补与告警通道等阻塞，不提升状态。

### 2026-10-18 Codex 指挥 DSH 与 Hermes 的实测

- 按用户确认的总控分工，Codex 向 DSH 发起只读 headless 接收检查；DSH 在接收任务前返回 `MISSING_CREDENTIAL`，无接收回执，F-029 责任仍在 Codex/GPCF，队列保留 `Planner/plan`。
- Codex 对 Hermes 本机 API 进行只读认证探测：健康、模型、技能接口均为 200，技能目录 274 项。此结果不代表项目级 AI 运行或监控已经接入。
- 执行回执见 `evidence/tool-control-probe-20261018.json`；待用户在 DSH 内完成凭据配置后重试相同交接包，未授权的对外 Web UI 恢复不在本次动作内。

### 2026-10-18 自动续跑登记

- 用户要求由 Codex 自动指挥 DSH 与 Hermes。已通过 Codex App 创建当前任务的 heartbeat `f-029-dsh-hermes`，状态 `ACTIVE`，每小时检查一次 DSH 接收能力；未变化时不重复写证据或发送例行通知。
- DSH 凭据仍由用户在 DSH 内配置；就绪后自动进行 F-029 只读复核交接、回执核验、Hermes 本机运行复测与 GPCF 门禁。高风险动作仍按人工授权边界办理。
- 当前无 DSH 接收回执，队列仍为 `Planner/plan`，Feature 状态保持 `partial`；自动化建立不等于端到端交接已完成。

### 2026-10-18 DSH 限定范围只读交接

- 用户在 DSH headless 配置中启用本地已保存凭据；Codex 仅修正其 YAML 方括号格式。无项目文件任务返回 `READY`，退出码 0。
- 首次直接派发源码复核被自动审批拦截，原因是将私有源码和项目证据发送到 DSH 模型服务需要更具体的授权；该次任务未送达。用户随后明确授权两处相关改动与 F-029 修复证据的只读复核。
- Codex 仅提交两处改动摘要及现有证据摘录；DSH 退出码 0，返回 F-029、输入版本和限定范围的接收回执。DSH 未直接读取仓库、重跑测试或接管服务。证据见 `evidence/dsh-readonly-review-20261018.json`。
- DSH 判断最小修复方向与当前签名一致；完整文件 16 项失败仅一项有抽查归因，其余 15 项和技能目录内容完整性仍待验证。F-029 保持 `partial`，后续责任回到 Codex/GPCF。

### 2026-10-18 Hermes 接口测试隔离复核与 Web UI 只读复测

- Codex 按 Hermes 规定入口复跑完整 `tests/gateway/test_api_server.py`：安装目录结果 98 通过、16 失败。15 项直接被 `home_io_guard.py` 拒绝读取真实 `~/.hermes`，另 1 项 HTTP 500 的调用栈也以同一守卫错误结束。
- 临时 Git worktree 保留对原仓 `.git/worktrees` 的引用，仍为 98/16；临时独立克隆应用同一两文件补丁后，完整接口文件 114 通过、0 失败。证据见 `evidence/hermes-api-test-isolation-20261018.json`。仅证明此测试文件在隔离目录中通过，不扩大为整个 Hermes 测试套件通过。
- 公开 `https://hermes.csydsc.com/` 仍由 Caddy 返回 502，本机 `127.0.0.1:8648` 连接拒绝而 8642 API 有监听。当前远端 Caddy 路由及 SSH 隧道未核验；未做对外恢复或配置修改。
- F-029 的正式试点仍缺替补值守、告警通道及权限隔离证据，状态上限保持 `partial`。

### 2026-10-18 DSH 补充复核与正式试点值守边界

- Codex 在用户已授权的两处相关改动与 F-029 修复证据范围内，向 DSH 递交隔离测试补充摘要。DSH 返回成功回执，认可独立克隆中同一接口测试文件 114/114 通过的有限结论；DSH 未读取仓库、运行测试或验证完整套件。
- Codex 核对 `_find_all_skills` 的真实签名，仅有 `skip_disabled` 参数，并以本机已有凭据进行只读对比：在线 `/v1/skills` 与本地相同排序函数均为 274 项，名称、描述和分类的内容及顺序一致。此结论只覆盖当前本机目录快照，不代表跨项目权限隔离或公开 Web UI 已恢复。
- 用户确认为主值守，并回复“暂无替补”；告警通道仍未指定。正式试点不满足值守准入条件，继续保持 `partial`，开发与本机验证可继续。

### 2026-10-18 项目群范围增量对账

- 项目群当前登记 27 项，较 F-029 早前的 25 项源码候选清单新增 PDC 与 SLC。Codex 仅对这两个新增仓库做同口径的非忽略文本检索；Hermes 和直连 Provider 关键字均未命中文件。证据见 `evidence/ai-consumer-scope-reconciliation-20261018.json`。
- 该补充检索只更新候选覆盖范围，不证明两个项目没有 AI 能力，也不证明项目群 AI 路径已经通过 Hermes。Hermes 本机 `/health` 仍为 200，对外 Web UI 仍为 502，本机 8648 未监听；F-029 仍为 `partial`。

### Iteration 1

1. 这轮做什么？
   - Dispatcher 执行 runtime 调度。
2. 改了什么？
   - Dispatcher -> Planner；status=plan
3. 怎么验证？
   - features/active/F-029-hermes-ai-runtime-admission/evidence/p0-preflight-20261018.json
4. 发现什么问题？
   - 未发现调度阻塞项。
5. 是否可以提交？
   - 否，commit/push 仍需明确授权。
