---
doc_id: GPCF-F013-EVIDENCE-STUDIO-INTAKE-TRANSPORT-20260803
title: Studio Intake 传输协议只读复核
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/studio-intake-transport-review-20260803.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/studio-intake-transport-review-20260803.md
sync_direction: bidirectional
last_reviewed: 2026-08-03
supersedes: []
superseded_by: []
---

# Studio Intake 传输协议只读复核

结论：`rework_required`。MMC commit `0261804` 已实现受限原始二进制 relay，但当前受控注册策略未准入该 delegated operation，且独立复核发现资源控制和上游错误投影缺口，因此不得启动 Studio intake 实现。

## 已验证链路

1. Studio `packages/server/src/services/core/mmc-client.ts` 将 `invoke` 的 `body` 限定为 object，并把 method、path、body、headers 与 delegation 统一 JSON 序列化后提交 MMC。
2. MMC `runtime/app/api/v1/connectors.py` 将 `InvokeInput.body` 定义为 `Optional[dict]`；`runtime/app/gateway/proxy.py` 以 `json=body` 转发并默认设置 `Content-Type: application/json`。
3. KDS `knowledge_intake/api.py` 的 `POST /api/v1/knowledge-assets/{asset_id}/complete-upload` 通过 `request.stream()` 接收原始字节；`tests/test_knowledge_intake_api.py` 以 `content=b"phase-a-source"` 验证该契约。
4. Studio 现有 project material draft 路由声明 `persistence: hermes_local_draft`，服务把上传文件和 `drafts.json` 写入本地 profile 目录。该链只能作为临时交互草案，不能继续持有正式资料、版本、哈希、证据或审计主账。

## MMC commit 0261804 独立复核

已通过：

- `MMC_TEST_MODE=true python3 -m pytest runtime/tests -q`：`86 passed`。
- 聚焦 upload API 与 gateway：`14 passed`。
- `bash runtime/scripts/contract_test.sh`：KDS/MMC 两套 schema 与必需 path 通过。
- `openspec validate mmc-kds-binary-upload-relay --strict`：通过。
- `git diff --check 0261804^ 0261804`：通过。
- `validate_mmc_loop_harness.py`：通过；commit-readiness 在 clean worktree 下按设计拒绝“无待提交改动”，不作为本提交失败。

阻塞发现：

1. **P1 注册准入缺失。** `runtime/state.json` 的 active `kds_llm_wiki_api.delegated_operations` 不包含 `POST /api/v1/knowledge-assets/*/complete-upload`。用真实注册数据调用 `PermissionGuard.check_delegated_operation` 返回 `False / not allowed`。成功测试在 `runtime/tests/test_api.py` 中 monkeypatch `_load` 注入了该权限，不能证明当前运行策略可达。
2. **P1 资源门禁晚于完整缓冲。** 路由先把最多 100 MiB 写入 `bytearray`，再以 `bytes(content)` 复制后调用 proxy；rate limit 与 circuit check 位于 proxy 内，发生在完整读取之后。单请求峰值可同时持有两份 payload，且被限流请求仍可先消耗完整缓冲资源，不满足设计中的“MMC buffers at most 100 MiB”边界。
3. **P1 上游 4xx 投影错误。** proxy 对 KDS 4xx 返回 `{status, body}` 而不设置 `error`；专用 route 随后返回 HTTP 200、`ok: true`，只在 data 内嵌上游 4xx。上传 token、ACL 或幂等冲突因此不能作为稳定失败状态被 Studio 处理。
4. **P2 审计覆盖不足。** 已验证 delegation/permission 拒绝会审计，但 streamed oversize 和若干前置格式拒绝没有对应 status-only audit 断言；成功 API 测试使用 FakeProxy，gateway 测试又替换 audit，尚未证明规范要求的“一次状态审计”边界。

因此 `0261804` 只可记为 `real_partial / implementation_verified / admission_rework_required`，不得记为 integrated、accepted 或 Studio intake 已解锁。

## MMC 本地返工第一次复审

已独立确认原四项问题中的 seed 准入、body 前 admission、KDS 4xx 投影和已覆盖审计路径得到修复：全量测试 `90/90`、聚焦 API `6/6`、gateway `12/12`，contract、OpenSpec strict、MMC Harness、py_compile 与 diff-check 均通过。

复审仍为 `rework_required`：

1. **P1 1 MiB 内存上限不成立。** `_spooled_upload_content` 把每个 ASGI chunk 整体传给 `SpooledTemporaryFile.write`，Python 在写入完成后才 rollover。以 `max_size=1 MiB` 写入单个 8 MiB chunk 的受控 `tracemalloc` 测量得到 `rolled=True`、峰值 `8,403,063 bytes`。因此单个大 chunk 可短暂占用接近完整 chunk 的进程内存，不能满足 OpenSpec“retain no more than 1 MiB”的要求。
2. **P1 大文件磁盘 I/O 阻塞事件循环。** spool rollover 后的 `content.write(chunk)` 与 `_spooled_content_stream` 的 `content.read(64 KiB)` 都是同步文件调用，虽然外层使用 async iterator，仍会在事件循环线程执行最长 100 MiB 的磁盘读写。
3. **P2 非法 asset ID 缺少拒绝审计。** `_knowledge_asset_upload_path` 在 registry、principal 和 audit helper 建立前执行；非 canonical asset ID 直接返回 422，没有 status-only audit，也没有对应回归。

下一次复审必须包含可达的大单 chunk 内存边界与临时文件清理回归、不会阻塞事件循环的磁盘 I/O 边界，以及非法 asset ID 审计回归。Studio intake 继续冻结。

## MMC 资源边界返工复审

正常路径的 P1/P2 缺口已修复：直接 `TemporaryFile`、64 KiB `memoryview`、`asyncio.to_thread` 读写不再创建第二个任意大小副本或同步阻塞事件循环；malformed asset ID 使用固定占位路径产生 422 status-only audit。独立复跑全量 `91/91`、API+gateway `39/39`、contract、OpenSpec strict、Harness、py_compile 与 diff-check 均通过。

复审仍为 `rework_required`，剩余一个可达 P1：`_temporary_upload_content` 仅以 `except Exception` 关闭文件，而 `asyncio.CancelledError` 继承 `BaseException`。受控请求先产出 64 KiB 再抛出取消，保留的 SpyFile 结果为 `cancelled_temp_closed=False`、`written=65536`。客户端断连或任务取消可绕过自动删除边界，现有测试只覆盖成功与 HTTPException。

须在 cancellation-safe 的 `finally`/`BaseException` 边界确定关闭临时文件，并增加 intake 期间取消及上游 streaming/cleanup 取消回归后再次复审。

## MMC cancellation cleanup 复审

首次 request-stream 取消与 upstream 取消现在均能关闭 TemporaryFile；独立复跑全量 `93/93`、API+gateway `41/41`、contract、OpenSpec strict、Harness、py_compile 与 diff-check 均通过。

复审仍为 `rework_required`：`_close_temporary_upload_content` 的 `shield(close_task)` 只防止内部 close task 被取消，但外层在清理中的第二次取消会立即传播。受控 blocking-close 回放在 worker 已启动后取消外层任务，得到 `outer_done=True`、`closed_when_cancel_propagated=False`，释放 worker 后才变为 `closed_after_background_completion=True`。这与 OpenSpec “close before cancellation propagates” 不一致；现有两个取消测试均未覆盖清理中的第二次取消。

须记住并延迟重复 `CancelledError`，持续 shield/wait 到 close task 确实完成，再消费 close 结果并传播取消；同时增加确定性的 blocking-close 双重取消回归。

## MMC deferred-cancellation 第五次复审

结论：`technical_review_verified / governance_partial`，本轮未发现剩余技术缺陷。实现循环吸收重复 `CancelledError`，等待 close task 完成并消费结果后才传播取消。独立真实 blocking-close 回放连续执行第二次、第三次取消时，close worker 释放前外层任务始终 pending；释放后先确认 `final_closed=True`，随后才观察到 `CancelledError`。

独立验证：全量 `94/94`、API+gateway `42/42`、contract、OpenSpec strict、MMC Harness、py_compile、diff-check 均通过，OpsX lock 缺席。此前 seed 准入、body 前 admission、资源边界、KDS 非 2xx 投影、status-only audit 和取消清理 findings 均有可达回归。

该结论只关闭 MMC relay 的 F-013 技术返工，不构成 accepted、integrated、production_ready、真实 KDS upload 或 Studio intake 授权。下一步必须由 GKE-001 coordinator 建立新的精确 Studio intake amendment。

## Studio intake A4 amendment

`GKE-001-COORDINATION-20260803-001-A4` 已建立，SHA-256 为 `c1c7963b0f66e5c66d471817c0f25219fe1653182362c5b4b3fe01010bfc6f3a`。Phase 1 仅授权 Studio 指定文件范围内的本地 TDD、契约、UI 与 mock 浏览器验证；不得调用真实或共享 KDS。

KDS 正式契约为 `v0.1`，canonical manifest SHA-256 为 `8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de`。现有 MMC seed 已准入受限 `complete-upload`，但尚未准入 `POST /api/v1/knowledge-assets/intake` 与 `POST /api/v1/knowledge-assets/*/retry`。因此 Phase 2 隔离 disposable E2E 必须等待这两项策略实现及 F-013 独立复核，再由 coordinator 发送继续回执。共享或持久 KDS 写入继续禁止。

## 门禁

- 禁止 Studio 直接绕过 MMC 调用 KDS。
- 禁止把二进制编码进现有任意 JSON body 后未经契约治理直接转发。
- 禁止把 `hermes_local_draft` 提升为正式 intake 或第二知识主账。
- 在 MMC 补齐受控 registry/seed 准入、把限流/熔断前置到 body 缓冲前或采用受控流式边界、正确投影 KDS 4xx，并补齐审计回归后，不创建 Studio intake implementation amendment。

状态保持 `active / partial / not_complete`。本次只读复核没有产品代码写入、真实资料/API 写入、commit、push、deploy 或状态提升。
