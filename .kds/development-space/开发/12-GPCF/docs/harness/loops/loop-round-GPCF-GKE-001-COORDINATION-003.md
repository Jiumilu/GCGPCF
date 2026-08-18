---
doc_id: GPCF-DOC-LOOP-GKE-001-COORDINATION-003
title: Loop Round GPCF-GKE-001-COORDINATION-003
project: GPCF
related_projects: [GPC, WAES, KDS, Brain, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-003.md
source_path: docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-003.md
sync_direction: bidirectional
last_reviewed: 2026-08-03
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GKE-001-COORDINATION-003

## 目标

由当前 `GKE-001` 会话统一主控 Studio、KDS、Brain 三条工程 lane，不直接合并三个会话内容；通过唯一 coordination envelope 固定 thread、change、owner、文件锁、依赖、handoff 与授权边界。

## Governance Loop

### run

- 建立 `GKE-001-COORDINATION-20260803-001` envelope v0.4，SHA-256 为 `e95307a21c4197798d692a7efe18be22f7d305c145942ce47a1afc24f06ceeff`。
- A1 amendment 允许 Studio 临时 `.harness/opsx.lock` 与 `loop-round-GPCF-STUDIO-LR-872.md`，用于封装已完成的实现证据；临时锁不得暂存、提交或作为产品改动交接。
- KDS 出现两个 allowlist 外回归测试写入后，coordinator 立即 HOLD 并只读审查；A2 只允许 `tests/test_knowledge_intake_api.py` 与 `tests/test_knowledge_intake_postgres.py`，用于 Stage B API ACL 与 disposable PostgreSQL 原子/回滚证明。
- A3 仅把 KDS 必需的 `.harness/opsx.lock` 声明为 execution-only，并登记 F-013 对 Stage B handoff 的返修结论；不扩张产品源码范围。
- KDS 第五次返修经 F-013 第六次独立复核为 `technical_review_verified_governance_partial`；Studio intake 前置只读检查发现 MMC 仅支持 JSON invoke，而 KDS complete-upload 要求原始字节流。
- MMC commit `0261804` 已提供专用 raw upload relay，独立复跑 86/86 全量测试、14/14 聚焦测试、contract 与 OpenSpec strict 均通过；但真实 connector registry 未准入 complete-upload，且 rate/circuit 位于完整缓冲后、100 MiB payload 会被复制、KDS 4xx 被包装成 HTTP 200，因此 F-013 判定 `rework_required`。
- MMC 第一轮本地返工修复 registry seed、body 前 admission 和 KDS 4xx 投影，独立复跑 90/90 全量、API 6/6、gateway 12/12 通过；但单个大 ASGI chunk 在 `SpooledTemporaryFile` rollover 前可突破 1 MiB 内存声明，磁盘 spool 读写同步阻塞事件循环，非法 asset ID 仍未审计，因此继续 `rework_required`。
- MMC 第二轮返工以 direct TemporaryFile、64 KiB memoryview/to_thread 和固定 malformed-ID audit 修复正常路径，独立复跑 91/91 与 API+gateway 39/39 通过；但 intake 期间 CancelledError 绕过 `except Exception`，受控复现临时文件未关闭，故继续 `rework_required`。
- MMC cancellation 返工以 BaseException 与 shielded close 修复首次 request/upstream 取消，独立复跑 93/93 与 API+gateway 41/41 通过；但清理中的第二次取消仍在 close 完成前传播，违背 OpenSpec 顺序保证，故继续 `rework_required`。
- MMC deferred-cancellation 第五次复审独立通过 94/94、API+gateway 42/42 与真实重复取消回放；close worker 完成前外层保持 pending，文件关闭后才传播取消。restricted relay 达到 `technical_review_verified_governance_partial`，但不构成 accepted/integrated/production_ready 或 Studio intake 授权。
- Studio intake A4 已建立，SHA-256 为 `c1c7963b0f66e5c66d471817c0f25219fe1653182362c5b4b3fe01010bfc6f3a`。Phase 1 允许精确 allowlist 内的本地 TDD、契约与 UI；Phase 2 仍等待 MMC prepare/retry delegated-operation 准入及 F-013 独立复核，共享 KDS 写入继续禁止。
- A5 reconciliation 发现 A1+A4 已由 Studio 外部 daily sync 提交并推送为 `1f63a464`，LR-874 已提交并推送为 `755f7b5d`；当前 Studio clean、`main == origin/main`、Loop/Harness 通过。A5 不追认 A4 禁止的 commit/push，冻结 Studio 新写入并把 committed A4 转入 F-013 只读复核。
- Studio 已确认 A5 ID/SHA 与冻结边界；Stage 7 只读验收进行中，只能返回报告，禁止任何仓库或外部写入。
- F-013 已独立重放 A4 committed scope：focused Vitest 101/101、mocked Playwright 3/3、build、OpenSpec 与 Studio Harness 通过；但允许角色、org 认证绑定、canonical 只读合同、浏览器场景、deterministic SHA 与文件边界存在缺口，判定 `rework_required`，A5 冻结继续生效。
- A6 精确返工 amendment 已下发，SHA-256 为 `bba9f2f33a1c43066df551ba8b086bcaa5f3c2d655b2ca6af831aefb40ee8f3c`；仅允许 allowlist 内本地 TDD、合同、UI、七类模拟浏览器场景和单一 LR-875 证据轮次，handoff 后再次冻结。
- A6 未提交 handoff 已返回并再次冻结。14 个最终路径均在 allowlist；F-013 与 coordinator 独立复核确认 focused 10/10、全量 Vitest 2740 passed/3 skipped、Playwright 7/7、build、OpenSpec、Loop validator、Harness 与 diff-check 通过，结论为 `technical_revalidation_passed_governance_pending`。
- 登记 Studio `019ee242-2575-73f1-b5bb-d43e7e49468e`、KDS `019fc4e3-bce5-7541-85e3-8885c7e78aea`、Brain `019edfb4-21ef-77e1-afdb-891df25c4068`。
- 只向各线程下发其本仓 lane，不复制源码、事实或未审查 Git 改动。

### stop

- KDS 角色视图外部改动进入 Stage B allowlist。
- Studio ahead 20 或 Brain 未提交桥接被直接合并、提交或推送。
- Brain 在 Studio 登录态可用前新增代码或文件。
- handoff 缺少 tests、ACL read/count、audit、lineage、mirror SHA、migration dry-run、rollback 或授权状态。
- 发生真实 KDS、长期记忆、业务状态、部署或状态提升写入。
- Studio 绕过 MMC、把二进制未经受控契约直接编码进 JSON，或把 `hermes_local_draft` 提升为正式资料主账。

### verify

- `python3 tools/kds-sync/validate_gke001_three_lane_coordination.py`
- `python3 tools/kds-sync/validate_loop_session_registry.py`
- `python3 tools/kds-sync/validate_knowledge_asset_model_system.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- Studio 必须确认 A4 ID 与 SHA，只执行 Phase 1 allowlist；在 MMC prepare/retry delegated operations 独立复核通过并收到 coordinator 继续回执前，不得进入 Phase 2 disposable E2E。Brain 继续冻结。
- A5 后不得创建新的 LR-874、修改 Studio validator、重写或回滚已发布历史；只允许读取 `1f63a464` 与 `755f7b5d` 并执行 F-013 独立复核。
- A4 返工只能按 A6 allowlist 与 `gke001-studio-kds-intake-a6-rework-lock` 执行；不得修改 user auth/user store/schema、越过 LR-875、提交或推送。
- A6 handoff 后 Studio 再次冻结；技术复核通过不授权 Phase 2、真实 KDS/MMC、Brain E2E 或状态提升。
- MMC H1R3 在 canonical F-013 十路径批准下完成：canonical state identity、alias/symlink 锁与恢复、startup hydration 和 operational dependency dry-run 纳入同一边界。F-013 首轮发现 missing-target recovery 被提前 existence check 阻断，原两文件返工后三种缺失目标场景、dependency 8/8、focused 86/86、full runtime 158/158 及静态门禁通过；最终结论为 `technical_revalidation_passed / governance_reconciled`。该关闭仅适用于 H1R3 本地范围，不授权 H2/H3 或真实策略应用。

### recover

- 某 lane 越过 allowlist 时停止该 lane，不回滚其它用户改动；由仓库 owner 按自己的 OpenSpec/OpsX 边界恢复。
- envelope 漂移时停止跨仓 handoff，以 GPCF canonical 文件重新计算 SHA 后重新下发。
- Studio 登录态或 KDS handoff 未满足时，Brain 继续冻结，不以 mock 替代真实只读 E2E。

### debug

- 对比控制板、会话总账和 envelope 的 thread/change/lock 集合。
- 对比 KDS `git status`，确认 `_registries/global-object-registry.yaml` 与 `entities/green-supply-chain-role-view-entity.md` 不在 Stage B allowlist。
- 对比 Brain `git status`，确认改动集合没有超出五个冻结文件。
- 对比 Studio health、8647 登录态和 runtime handoff，不把运行恢复当成 KDS API 已验收。
- 对比 Studio MMC invoke、MMC proxy 与 KDS complete-upload body 语义，不以 JSON fixture 替代真实二进制传输契约。

## Delivery Loop

```yaml
goal: 建立可持续的 GKE-001 三线协同执行面
changed:
  - coordination envelope
  - LOOP control board
  - LOOP session registry
  - F-013 evidence and validator
verified: brain_a10p1t4_passed_and_mmc_h1r3_technical_governance_reconciled
risk: KDS dirty admission, MMC H2/H3 policy apply, Studio Phase2, real Studio/KDS replay, Brain read-only E2E and human confirmation remain incomplete
next: keep Studio and real E2E frozen; require separate human authorization before MMC H2/H3 or any live read/write
product_delta: none_governance_coordination_only
user_visible_delta: none
task_flow_e2e_status: not_complete
```

## 状态边界

本轮不是 GCKF D191，不改变 D190 `0/4`。三线协调状态保持 `active / partial / not_complete`；KDS Stage B 本地开发授权不等于真实 KDS 写入、commit、push、部署或状态提升授权。
