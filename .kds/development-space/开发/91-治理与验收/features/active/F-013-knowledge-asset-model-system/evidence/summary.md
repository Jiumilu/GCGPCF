---
doc_id: GPCF-DOC-F013-KNOWLEDGE-ASSET-EVIDENCE-SUMMARY-20260802
title: 证据摘要
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/summary.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

# 证据摘要

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: KDS Stage B 第六次独立复核中，非数据库 66/66 与 disposable PostgreSQL/迁移 23/23 通过；临时数据库清理计数为 0。
- contract: OpenSpec strict、canonical/model hash 与 F-013 admission 通过；admission 正确保持 `blocked_dirty_worktree`。
- review: `technical_review_verified_governance_partial`。五轮返工项均有独立可达回归；KDS dirty 与后续 Studio/Brain/MMC 门禁仍未解除。
- studio: A8 独立复核确认现有 `super_admin / gehua / operator` 上下文完成唯一一次临时会话删除；前置 GET 200、DELETE 200 `ok=true/deleted=true`、后置 GET 404，16 个未截断网络事件中无 KDS、MMC 或 intake 请求。该结论仅关闭清理证明，不构成真实知识只读 E2E。
- brain: A8 独立复核确认标准 OpsX 包完整、7 文件 patch 精确、59/59 与静态 alignment/OpenSpec/diff-check 一致且 lock 已释放；全局 typecheck 仍有 86 个错误，tranche 2 与真实 E2E 继续冻结。
- a9: F-013 独立复核确认 KDS 66+23 与 MMC 两操作受控子集技术证据通过；A9R1 六项 rollback addendum 也已独立通过，serial exit 技术要求为 `5/5`。这不构成 KDS 真实 read admission、MMC 全局只读、A10 授权或 real E2E。
- a10p0: 已签发三线零写入预检，仓库 allowlist 全为空。协调器静态核对发现 Stage B knowledge-assets 与 Brain 使用的 projects 读模型不是同一契约，Studio bridge 尚未绑定 authoritative project，Brain typecheck 当前仍为 86 errors，MMC 仍有 `GET *` 和 15 项 A9 外操作；三份报告和 F-013 复核完成前 live-read/real E2E 均未授权。
- a10p0-handoffs: 三份报告已收齐。Studio/MMC 3/3、Brain 84/84 与 alignment 通过，业务仓基线/dirty/lock 均未变化；KDS 复用 A9 哈希并明确 legacy routes 无 delegation/ACL/KDS audit、Stage B extraction/evidence GET 缺完整 per-read audit。当前等待 F-013 独立复核。
- a10p0-review: F-013 独立确认三份报告完整可信，但判定 live-read 入口条件未满足。Stage B 与 legacy projects 不兼容，Studio 缺 authoritative project binding，MMC/KDS 端到端逐读审计不足。
- a10p1: 已签发 `GKE-001-COORDINATION-20260811-006-A10P1`，SHA-256 为 `264a50bb1020a97777761371fb331f6a6c05e6ed3698875d27107b0c79bfd1bb`。Studio/MMC 与 KDS 仅返回空 allowlist 契约收敛报告；Brain 仅可在精确六文件内做本地 TDD。三份 handoff 与 F-013 复核完成前不授权 live-read 或 real E2E。
- a10p1-handoffs: 三份交接已收齐。Brain 六文件聚焦测试 29/29，typecheck 从 86/25 降至 49/19，run-scoped OpsX 包完整且 lock 已释放；KDS 与 Studio/MMC 报告均保持零写入。两份 API 提案的 method/path/identity 不一致，已转 F-013 独立复核，当前不冻结任一提案。
- a10p1-review: F-013 独立接受三份 handoff 和 Brain 本地 tranche，但退回两份 facade；裁决方向为 KDS canonical 投影语义加 Studio 服务端 session ownership，并压缩为两个 POST operation。
- a10p2: 候选合同 SHA-256 为 `11e15a3448279c7ddcdc97ea25b80cfefbef17a332c08cd20f41efc97a6667f8`；A10P2 控制 SHA-256 为 `e2a0cb491bcb626bb29507be5e51612e4cb26ddf1427b94e70f7bd3f1b7f249e`。Studio/MMC 与 KDS 空 allowlist 报告已派发，Brain 冻结；候选尚未冻结或实施。
- a10p2-handoffs: 两份报告对 operation matrix SHA `e2fc18d9287d45ae2fc4ac8015febea9187246840d91b06a6b33e16de8e865c4`、MMC candidate fingerprint `3cab2c7eef531c13bc0af32af61836f3947aa23ac8b2461f84a05f47378dbaf2` 和 restore fingerprint 达成一致。field-level projection/cursor/error schema 与 Studio/MMC 精确未来路径仍不完整，已转 F-013 freeze review。
- a10p2-review: F-013 只接受两操作、服务端身份、canonical identity、session ACL、逐读审计和 no-second-ledger 为不可回退决策基线；A10P2 整体仍未冻结。字段类型、投影白名单、totals/cursors、排序、错误映射和精确文件隔离必须返工。
- a10p3: OpenAPI 3.1 候选 raw SHA 为 `48dfcb0967a894ee2bd760311d7f84023054b0bcc2bc578292d826e73fbc7c18`，A10P3 control SHA 为 `9a3fe20c87d269263e442b5a6899f6f75581319adc7a8800a27e0669abcd22e4`。Studio/MMC 与 KDS 两条空 allowlist 报告线已派发；Brain 冻结，合同、实现、live-read 和 real E2E 均未授权。
- a10p3-reports: 两线均判定 `rework_required`。SearchRequest 的 `allOf` 合法实例失败，matrix 缺单一可执行 normalizer，Stage B 生命周期、digest/OCR/confidence、有界文本和无损 locator 映射不完整；Studio 10、MMC 8 与隔离后的 KDS 12 个未来路径已明确。
- a10p3r1: 修订 schema SHA 为 `74b51affabf79d2ba4a908d2d9397671bdd0b07bc80814a0c36dd8d83faa7e14`，normalizer SHA 为 `d820e8103b2af74aab06381fe4034c9cec525acc8c7e1efdb074bd8a4a3aa4e4`，control SHA 为 `c8b76dcde4ffdee835fe426edbd44c33c975b6bcbd25dd60ad0dd827134f6060`。本地 OpenAPI、三类请求和六类 locator 合法实例通过；双报告与 F-013 复核前仍未冻结。
- a10p3r1-handoffs: 双线哈希和 normalizer 一致；KDS 合法请求/响应/locator 与 11 种 Stage B 定位 round-trip 通过，Studio/MMC BFF/error 与 10+8 路径一致。Schema 内 MMC candidate fingerprint 占位值已显式交由 F-013 裁决，三线重新冻结。
- a10p3r1-review-a10p3r2: F-013 判定字段 schema 通过、仅 MMC 指纹占位值阻塞。A10P3R2 只改一行，新 schema raw SHA 为 `cc5865ac5f76e82d7ea86891f020e196073a0a23cd5a4f6bb44a3a279b0b0de0`，control SHA 为 `d4b21c2ccfbc9d2878ce5c020c232f26c53b704b51313a92da6d8345748b12bc`；normalizer/matrix 不变，hash-only 回执进行中。
- a10p3r2-freeze: 两条哈希回执与 F-013 最终字节复核通过，精确 R2 bytes 登记为 `contract_frozen_for_future_implementation_not_integrated`。冻结记录 SHA 为 `a7dbdcf6a64a4f9b6c6cd11e4ae2fe02405624b29e4ad009a317510de557a23f`；KDS 12、Studio 10、MMC 普通代码 6 与 MMC 高风险策略 2 个路径均保持未实施、未授权。
- a10i1: 已按当前仓库事实建立首批实现控制，SHA 为 `8f4087ca09a4695a0cdec021d0d22270c4866ec9903dc86c0c8cbff8069d37c3`。Studio 10 文件 handoff 已回传并冻结，119 个聚焦测试与 2747 个全量测试通过；KDS 12 文件 handoff 也已回传并冻结，聚焦 41、相关非数据库 101、一次性 PostgreSQL/迁移 29 均通过且数据库残留为 0。两条 OpsX 锁均已释放，当前等待 F-013 联合独立只读复核。MMC 普通代码、MMC 策略配置、Brain、live-read 与真实 E2E 未授权。
- a10i1-handoffs: Studio 基线 `88769078f5c230ae9ed973815de4861cc6317a5c`、KDS 基线 `f28edb5113e0493ed60fec423cb6c7e1a6252de8` 均与 origin 一致且 staged/ahead/behind 为 0。KDS canonical mirror 8/8、冻结控制/OpenAPI/normalizer/matrix 哈希、OpenSpec strict、model/admission 与 diff-check 通过；KDS 文档门禁仍仅因 localization debt 为 `rework_required`，CodeGraph 因写范围越界未运行。状态保持 `partial/not_complete`。
- a10i1-review-a10i1r1: F-013 独立复核确认 KDS 技术实现通过，但 Studio Search 仍使用 query 500/limit 200 边界、上游错误码与 correlation 未按冻结 ErrorBody 收敛，且 Studio run 缺 evidence-index、acceptance-matrix、patches 和 run-scoped build 结果；KDS 还缺 A10I1 要求的 CodeGraph 证据。已签发 A10I1R1，Studio 仅两文件返工，KDS 仅治理回放，serial gate 保持未关闭。
- a10i1r1-closure: Studio 定向 7/7、全量 2749/3 skip 与冻结契约边界通过；KDS CodeGraph 达到 632 files、5326 nodes、13240 edges 且索引最新。F-013 最终验证 Studio 补丁 SHA `914909d2e15f15ce6dc869f3372934ffee157f64934842e7b613a6b287db6111`、两文件边界及 pre-R1 -> R1 正反向隔离回放通过，判定 `A10I1 KDS+Studio first implementation batch joint serial gate = closed`。该关闭不授权 MMC、Brain、live-read、真实 E2E、Git 发布、部署或状态提升。
- a10i2: 已签发 MMC 普通代码实现控制 `GKE-001-COORDINATION-20260811-013-A10I2`，SHA-256 为 `8ab2dd88b45c33669a4d3a14dc8065765738e113ff1728965b1defaa3776aacf`。仅授权 clean 基线 `8bb60fcffb8de14e839de0631e646c8c73418092` 上六个标准产品/测试路径及 run-scoped OpenSpec/证据；`runtime/scripts/seed.sh`、`runtime/state.json`、核心 delegation 模块、运行时策略、真实 KDS/MMC、凭据、commit、push、restart、deploy 与状态提升继续禁止。MMC handoff 与 F-013 独立复核完成前，KDS、Studio、Brain 和真实 E2E 保持冻结。
- a10i2-handoff: MMC 标准 run `20260811-132225-implement-release0-canonical-read-relay-a10i2` 已冻结。最终 4 个产品/测试文件均在六文件 allowlist；focused 8/8、完整 runtime 103、contract、OpenSpec strict、MMC Harness、CodeGraph 与 diff-check 由 handoff 报告通过，协调器复跑 focused 8/8、OpenSpec/Harness/diff 通过。产品 patch SHA 为 `a7ebcef4ad5c4b87e78973174c6915ca34bad56b629c31efb07c46c305427270`，高风险 4 文件哈希未变，lock 已释放。当前仅转 F-013 独立只读复核，不构成 accepted、integrated、策略配置或 live admission。
- a10i2-review-a10i2r1: F-013 判定 `technical_rework_required / handoff_not_accepted`：MMC delegation 的 audience 与 permissions/project/session scopes 不被当前 KDS verifier 接受；OpenAPI 的 closed authority `allOf` 使合法 search/read 实例失败且成功响应未字段冻结；现有测试未覆盖 read/graph/wiki-preview；bypass 403 缺 bounded denied audit。已签发 `GKE-001-COORDINATION-20260811-014-A10I2R1`，SHA-256 `ef4065c374f5f2be480c170b3a4e60bef54a72b0d8ee40c3bd3c7fb5e12cbd2e`，继续限制在原六文件，不授权 `contract_test.py`、核心 delegation、策略配置、live-read 或发布动作。
- a10i2r1-handoff: A10I2R1 run `20260811-135512-rework-release0-canonical-read-relay-a10i2r1` 已冻结。focused 15/15、完整 runtime 109、直接 KDS DelegationVerifier/ReadAuthorityVerifier、字段级 Search/Graph/Wiki schema、OpenSpec/Harness/CodeGraph/diff 与累计 patch `ad18f0340e8ff5269bfd6d1454f155419e7514990cf7c475e2f6e55eea7c0447` 由 handoff 报告通过；协调器复跑 focused 15/15、OpenSpec/Harness/diff 通过。最终仍为 4/6 文件，高风险哈希未变、lock absent；当前等待 F-013 定向复审。
- a10i2r1-review-a10i2r2: F-013 确认 delegation、三类请求、三视图 transport 与 bypass audit 已闭合，但嵌套 Search/Graph/Wiki canonical projection 仍为空开放对象，400/403/404/503 error code/retryable 组合也未按状态冻结。已签发两文件 A10I2R2 `GKE-001-COORDINATION-20260811-015-A10I2R2`，SHA `bae892222772f306c41999631a5d1bf27cc9ea17f79e88cc42c1e9163a6b2d11`；只允许 OpenAPI 与 contract tests，运行代码和策略均冻结。
- a10i2r2-handoff: A10I2R2 run `20260811-151500-rework-release0-response-schema-a10i2r2` 已冻结。仅 OpenAPI 与 contract test 存在 R2 delta；focused 9/9、八类投影字段交叉校验、完整 runtime 114、contract、OpenSpec strict、MMC Harness、CodeGraph、diff 与隔离 patch `d8eb4b2094e48fbf1d3d2d06d8a14cd25e587c6b5a19522450664fbc8789bfac` 由 handoff 报告通过，协调器复跑 focused 9/9、contract、OpenSpec strict、Harness 与 diff-check 通过。高风险文件未变且 OpsX lock absent；当前仅等待 F-013 最终定向复审。
- a10i2r2-closure: F-013 最终结论为 `independent_technical_rereview_passed_schema_and_mocked_contract_only`，未发现阻断 finding；八类嵌套投影、空/附加字段拒绝、400/403/404/503 code/retryable、冻结 KDS R2 对齐及两文件隔离均通过。A10I2 MMC 普通代码技术门关闭，但策略 apply、live-read、真实 E2E、凭据、Git 发布、部署与状态提升仍未授权。
- a10i3p0: report-only policy safety preflight `GKE-001-COORDINATION-20260811-016-A10I3P0` SHA `4a7de8561f2882940caea5b9ed55a790e53f9c44ea5cfb3c359e5ff9791b73df` 记录 current 17-operation fingerprint `40a674...a5e` 与 target 19-operation fingerprint `e99be2...d0c2`。当前 PATCH 缺 admin role/CAS/atomic save/fail-closed audit，seed force 会覆盖 10 个额外 API；因此只转 F-013 复核 H1 hardening、H2 source、H3 runtime apply 三段提案，未触碰 MMC。
- a10i3h1: F-013 独立确认三组指纹、seed-force 禁令及五项 mutation-boundary 缺口，并允许协调器单独签发零策略变化的本地 H1 TDD。控制 `GKE-001-COORDINATION-20260811-017-A10I3H1` SHA `a3fc12a42b47e23d39a867719bcde0da10ec452751378d5a0128f38bb54cdbff` 仅覆盖四个产品/测试路径及临时测试状态；H2/H3、真实策略、live read 和 E2E 仍需人工授权。
- a10i3h1-handoff: MMC run `20260811-153000-harden-mmc-delegated-operation-policy-a10i3h1` 已冻结；focused 21、full runtime 129、contract/OpenSpec/Harness/CodeGraph/diff/patch 均通过，seed/state 与 17-operation policy 未变。协调器额外复现“回滚状态恢复失败后 target policy 仍有效”和“ordinary PATCH 被 guarded 全状态替换覆盖”两项安全缺口，现只转 F-013 独立复核，不授权 H2/H3。
- a10i3h1-review-a10i3h1r1: F-013 将回滚恢复吞错、ordinary PATCH lost update、进程内锁和审计短写列为四项 blocker，判定 `technical_rework_required`。已签发同四文件 H1R1 `GKE-001-COORDINATION-20260811-018-A10I3H1R1`，SHA `8a5470cfa1adfdab1ff18307aad3739bc3af6fbd32b10c3353ff8e8545875850`；只授权本地跨进程锁、durable recovery、完整或零字节审计追加及失败/取消回归，H2/H3 和真实策略继续冻结。
- a10i3h1r1-handoff: MMC run `20260811-161500-rework-mmc-delegated-operation-policy-a10i3h1r1` 已冻结；focused 66、full runtime 139、contract/OpenSpec/Harness/CodeGraph/diff 与四文件正反向 patch replay 通过，协调器补跑 guarded-create/delete 交错也通过。seed/state 与 17-operation policy 未变，现只转 F-013 独立复核。
- a10i3h1r1-replay-a10i3h1r2: 协调器继续核对共享 `runtime/state.json` 后可达复现两项 P0：未完成恢复时 `registry_apis` 返回 503，但 connector 仍读取 target policy；guarded API policy patch 与 LLM registry patch 交错时，后者先报告 `rpm=2` 成功，最终状态却回退为 `rpm=1`。已签发八文件 H1R2 `GKE-001-COORDINATION-20260811-019-A10I3H1R2`，SHA `880980dbd38462c58fa8da34ea67fca593c3e2bae2958e3410a6a74b1222c731`，只允许本地共享状态锁/恢复 TDD；H2/H3 与真实策略继续冻结。
- a10i3h1r2-baseline-reconciliation: H1R2 签发后检测到外部 daily clean sync `b06f58a78ac7713197deed47d1125bec7a260e8c` 已提交并推送既有 MMC 改动。协调器不追认该 Git 动作；八文件中七个现有文件哈希保持不变，新共享模块仍不存在。已签发基线对账 `GKE-001-COORDINATION-20260811-020-A10I3H1R2R0`，SHA `a40e54f14ff5bd1e7b9474097e466f6ac0f6dea854ac3c35f0c34f59d4e62152`，仅将执行与回滚基线改为 clean `b06f58a`。
- a10i3h1r2-handoff: MMC run `20260812-002227-rework-mmc-shared-registry-state-a10i3h1r2` 已冻结；八文件 shared registry state 边界的 focused 75、full runtime 146、合同/OpenSpec/Harness/CodeGraph/diff 与隔离 patch `d5083a534e0daf0342a54dfba4992867574650df442b11709109d2ab475a6938` 通过，17-operation policy 与 seed/state 哈希未变，OpsX 锁和临时 sidecar 均已释放。stock evidence validator 的首个计数退出缺陷及 allowlist 外 `runtime/app/db/session.py` count-only reader 已披露；当前只转 F-013 只读复核。
- a10i3h1r2r1-coordinator-review: 临时文件双进程回放证实 `resolved_state_equal=true` 但 `lock_path_equal=false`，第二进程在第一进程持锁时仍成功进入。H1R2 违反自身 resolved-path advisory-lock 冻结要求，分类降为 `technical_rework_required_pending_f013_confirmation`；提议 H1R3 仅覆盖 shared state、db/session 和两测试文件，但在 F-013 确认前不授权实现。Studio/Brain 外部 daily sync 新基线已只读登记，未追认 Git 动作。
- a10i3h1r3-closure: canonical F-013 批准十路径后完成 shared canonical state identity、startup hydration 与 operational dependency dry-run。首轮复核发现 missing-target recovery 被提前 existence check 阻断，原两文件返工后 dependency 8/8、focused 86/86、full runtime 158/158；Contract/OpenSpec/Harness/CodeGraph/diff 与 patch/hash 边界通过。F-013 最终分类 `technical_revalidation_passed / governance_reconciled`，H1R3 有界串行门关闭；H2/H3、真实策略、live read、真实 E2E 与发布仍未授权。
- gckf: D185-D190 no-write 主线回放通过；DKS-054 至 DKS-060 为 `merged_precondition_controlled`，四项 resume triggers 均未满足，`nextExecutableRounds=0`。
- api: waived；未执行真实 KDS API 或资料写入。
- risk: KDS dirty admission、Brain 剩余类型错误、Studio 权威项目绑定、canonical read facade、逐读审计、真实浏览器证据、MMC 策略隔离、MMC/human authorization 与 localization debt 仍未闭合；不得据 A10P0 预检通过或 A10P1 派发而授权 live-read、real E2E、accepted/integrated、Phase 2、deploy、真实资料/长期记忆/关系/业务状态写入或状态提升。
- stageb-run-handoff-eof-rework: R8+R8R1 人工授权已按精确边界执行。目标文件从 1175 字节 `a90228ec...5478` 修正为 1174 字节 `4fa7ea7c...6bd67`；corrected 13-file manifest 为 `11a373670ba3a9d01c12fdd5aab7ca7aabb3accd1008e98f7c11a269bac666bc`，deterministic patch 为 `00a37e1e7a1d480896aa904257deaa35f685e052fbc16ace132c708c9c3dac83`。F-013 独立分类 `one_byte_rework_and_corrected_report_only_preflight_independent_review_passed`；未 stage/commit/push，未来 13 文件本地提交仍需单独人工授权。
- stageb-run-handoff-commit-request: A10I1D4R9 封存精确 13 路径、父提交 `a7ec8741`、pathset SHA `dee9d08e...a525`、corrected manifest 和 patch，提交主题固定为 `chore(kds): record document extraction handoff`。当前仅进入 F-013 事前只读复核；stage/commit/push 仍未授权。
- stageb-run-handoff-commit-review: F-013 返回 `authorization_request_review_passed_human_13_file_local_commit_authorization_required`。该结论仅证明授权包可供人工决定；未修改文件，未授权或执行 stage/commit/push。
- stageb-run-handoff-local-commit: 用户按 A10I1D4R9 授权后，KDS 创建本地提交 `690ea04a`，精确包含 13 个 run/handoff 文件；F-013 返回 `local_stageb_run_handoff_13_commit_independent_review_passed`。未 push，未执行后续单元；`66+23` 仍为 inherited/not rerun/not live。
- stageb-four-commit-push-preflight: A10I1D4R10 只读核对真实远端仍为 `f28edb51`、本地 ahead/behind `4/0`、精确四提交链且无额外提交；指定 dry-run 显示 `f28edb51..690ea04a` fast-forward，前后状态不变。F-013 分类为 `push_preflight_independent_review_passed_separate_exact_push_authorization_required`。A10I1D4R11 仅为精确 push 人工授权请求，真实 push 尚未授权。
- stageb-four-commit-push: 用户按 A10I1D4R11 授权后，仅执行一次精确非 force push；远端 `main`、本地 `HEAD` 与 `origin/main` 均收敛到 `690ea04a`，ahead/behind/staged 为 `0/0/0`，dirty 数量与 NUL porcelain 哈希保持不变。F-013 独立提交后分类为 `kds_stageb_four_commit_exact_non_force_push_independent_postpush_review_passed`；该结论不关闭 dirty admission、集成、部署或状态提升门禁。

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: pass
- api: waived
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: 未授权 commit、push、deploy、真实 API、状态提升。
<!-- GPCF_EVIDENCE_GATE_END -->
