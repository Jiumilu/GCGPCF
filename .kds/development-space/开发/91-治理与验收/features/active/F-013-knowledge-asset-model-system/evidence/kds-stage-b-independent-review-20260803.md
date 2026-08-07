---
doc_id: GPCF-F013-EVIDENCE-KDS-STAGE-B-REVIEW-20260803
title: KDS Stage B 独立只读复核
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/kds-stage-b-independent-review-20260803.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/kds-stage-b-independent-review-20260803.md
sync_direction: bidirectional
last_reviewed: 2026-08-03
supersedes: []
superseded_by: []
---

# KDS Stage B 独立只读复核

结论：`rework_required`。本结论不否定已通过的本地测试，但阻止 Stage B 进入 Studio intake。

## 已验证

- handoff 与 knowledge-engineering handoff 可解析，v0.3/A2 SHA、changed paths、授权边界和外部角色视图排除一致。
- 非数据库回归 51/51、disposable PostgreSQL 12/12 由 F-013 独立复跑通过；临时数据库清理后计数为 0。
- canonical manifest SHA-256 为 `8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de`，8 个镜像/依赖文件匹配。
- GPCF model gate 通过；admission 正确返回 `blocked_dirty_worktree`，未授权真实写入、迁移、提交、推送、部署或状态提升。

## 阻塞发现

1. `DocumentExtractionService.process_next` 在 claim 后发现既有 failed run 时直接返回，retry 不会再次调用 parser，且新 attempt 保持 `leased`。
2. memory/PostgreSQL extracted search 查询资产的全部历史 extraction content，没有限定当前 `knowledge_assets.extraction_ref`；旧内容仍会进入普通搜索。
3. EvidenceLink lineage/locator 校验失败时只抛错，不追加规范要求的 safe failed audit。
4. repository 与迁移未以复合约束保证 job asset、source version、extraction run、block 的 exact lineage；当前成功路径依赖调用方正确组装。
5. PostgreSQL content page 在游标越过末尾、返回空 rows 时把已授权 total 降为 0，分页 total 不稳定。

## 只读复现

```text
retry first=failed second=failed parser_calls=1 job_state=leased lease_owner=w2
active_new=True stale_search_total=1
bad_link=ValueError audit_delta=0
```

返修仅限 v0.4/A3 envelope 既有 KDS allowlist；必须增加对应 memory/PostgreSQL/API 回归并返回修订 handoff。状态保持 `active / partial / not_complete`。

## 第二次复核

A3 首轮五项修复已通过 55 项非数据库与 14 项 disposable PostgreSQL 独立复跑，但仍有以下阻塞：

1. `process_next` 只捕获 `ExtractionError`。parser/storage/runtime 抛出包含本地路径或源内容的其它异常时，原始消息向调用方外溢，claim 保持 `leased`，没有失败 run、audit 或 outbox。
2. 初始 extraction claim 与过期 lease recovery 只创建 JobAttempt，没有追加 OpenSpec 要求的 AuditEvent。

只读复现：

```text
raised=RuntimeError raw=/private/source/customer-secret.txt: ACME
job_state=leased lease_owner=worker audit_delta=0 extraction_runs=0
```

因此第二次结论仍为 `rework_required`；A3 第一轮修复有效，但 Stage B 尚未通过 F-013。

## 第三次复核

第二次返修已解决 sensitive exception 和 claim/recovery audit 缺口。F-013 独立复跑非数据库 58/58、disposable PostgreSQL/迁移 16/16，OpenSpec strict、canonical mirror 8/8、model/admission 均通过；复核数据库删除后存在计数为 0。

代码级审查发现以下新的阻塞项：

1. claim 只原子记录 job attempt 和 start/recovery audit，parser 运行前并未持久化 `ExtractionRun(state=running)`。worker 中断时依然没有 running run 历史，不满足 initial claim 和 task 4.1。
2. `ParserProfile.timeout_seconds` 只传入 OCR 子进程，通用 parser/storage 路径没有 wall-clock 超时执行器。在 1 秒上限下注入 1.25 秒 parser，run 仍以 `succeeded` 完成。
3. PDF 空页 OCR 调用 `get_pixmap` 前没有核对 `max_image_pixels`。将上限设为 1 后，100x100 PDF 仍被渲染并成功生成 OCR block。
4. 第一个 profile 成功后，对同一 source version 使用不同 governed profile 再次调用只返回 `None`；未创建规范要求的独立逻辑 extract job/run。
5. extraction list 和 EvidenceLink list 路由没有 limit/cursor；content 路由只限制 block 数，仍返回所选 block 的全部 cells，单个 XLSX block 可使响应达到全局 cell 上限，不满足 bounded status/content projection。

独立复现：

```text
timeout: elapsed=1.26s run_state=succeeded job_state=succeeded error_code=None
pdf_ocr_pixels: result_blocks=1 first_kind=ocr limit_pixels=1
profile_change: second_run=None run_count=1 job_count=1
running_history: runs_visible_while_parser_active=[]
```

第三次结论仍为 `rework_required`。返修必须保持 v0.4/A3 现有 allowlist，不得引入新仓或扩大授权。

## 第四次复核

第三次返修已覆盖此前五项缺口。F-013 独立复跑非数据库 62/62、disposable PostgreSQL/迁移 19/19，OpenSpec strict、canonical/model hash、admission 与 diff-check 均通过；复核数据库删除后计数为 0。

租约恢复的并发终结边界仍有一个阻塞缺陷：

1. 旧 worker claim attempt 1 并进入 parser 后租约过期。
2. 新 worker recovery claim 同一逻辑 job，创建 running extraction version 2。
3. 新 worker尚在解析时，旧 worker 完成 version 1；repository 只检查当前 job 为 `leased` 及 asset/source lineage，没有检查当前 `lease_owner`、attempt number 或 claim token，因此接受旧结果。
4. 旧结果把 job 标记为 `succeeded` 并切换 active projection；随后新 worker 的合法 version 2 无法终结并永久留在 `running`。
5. `record_extraction_failure` 使用相同的不完整校验，旧 worker 也可错误终结新 worker 所持有的 job/attempt。

独立复现：

```text
old_completion succeeded 1
new_completion ValueError:job and extraction lineage do not match
job_state succeeded lease_owner None
run_history [(1, succeeded), (2, running)]
active_extraction_version 1
```

该结果违反 bounded lease ownership、exact attempt lineage、recovery history 与 concurrent loser 不得发布 active result 的契约。第四次结论仍为 `rework_required`；必须在既有 allowlist 内把 running run 与 exact job attempt/claim token 绑定，并为 stale success 与 stale failure 增加 memory/PostgreSQL 交错回归。

## 第五次独立复核

第四次返修已把 running run 与 `job_ref + attempt_number + claim_owner` 绑定，并在 memory/PostgreSQL 中拒绝 recovery claim 后旧 worker 的 success/failure。独立回放结果为非数据库 64/64、disposable PostgreSQL/迁移 21/21，测试数据库清理计数 0；OpenSpec strict、53/53 tasks、GPCF model/admission、锁缺席与 diff-check 均通过。

但终态校验只比较 state、owner、attempt 与 run claim，没有验证当前租约时间仍有效。受控复现未启动 recovery worker，仅令 attempt 1 的 completion 发生在 `lease_expires_at + 1s`：

```text
expired_completion=ACCEPTED
lease_expired_at_completion=True
job_state=succeeded
active=old_expired_claim_extraction
```

因此一个已过期但尚未被重领的 worker 仍可发布 active result；failure 路径使用相同校验并存在同一窗口。这违反 design 明示的 `an expired worker receives only KDS_EXTRACTION_CLAIM_STALE`。第五次结论为 `rework_required`：memory 与 PostgreSQL 的终态事务必须以受控当前时间原子验证 `lease_expires_at` 尚未到期，过期 success/failure 均不得修改 job、attempt、run、content、active selection、audit 或 outbox。

## 第六次独立复核

第五次返修已补齐租约时间边界。独立回放结果：

- 非数据库 66/66；disposable PostgreSQL/迁移 23/23；测试数据库删除后计数 0。
- OpenSpec strict 通过，tasks 57/57；handoff YAML、envelope SHA、OpsX 锁缺席与 diff-check 通过。
- PostgreSQL 在 `FOR UPDATE` 锁定 job 与 running run 后读取 `clock_timestamp()`；即使调用方把 `terminal_at` 伪造为前一天，expired-unreclaimed success/failure 仍返回 `KDS_EXTRACTION_CLAIM_STALE`。
- memory 使用显式受控 terminal time；expired-unreclaimed success/failure 与 recovered stale success/failure 均在写入前拒绝，job、JobAttempt、run、content、active selection、audit、outbox 保持不变。
- GPCF canonical/model hash 与 admission 通过；admission 仍为 `blocked_dirty_worktree`，未产生状态提升。

第六次复核未发现新的 Stage B 技术阻塞，结论为 `technical_review_verified_governance_partial`。这只解除 KDS Stage B 的 F-013 返工状态，不代表 commit、push、部署、生产迁移、真实资料写入、Studio 集成、Brain E2E、MMC 委托、人工确认、`accepted`、`integrated` 或 `production_ready`。
