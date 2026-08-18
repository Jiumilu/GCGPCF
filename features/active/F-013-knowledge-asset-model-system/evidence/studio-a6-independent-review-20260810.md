---
doc_id: GPCF-DOC-F013-STUDIO-A6-INDEPENDENT-REVIEW-20260810
title: Studio A6 独立只读复核
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/studio-a6-independent-review-20260810.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/studio-a6-independent-review-20260810.md
sync_direction: bidirectional
last_reviewed: 2026-08-10
supersedes: []
superseded_by: []
---

# Studio A6 独立只读复核

## 判定

```yaml
handoff_result:
  change_id: integrate-studio-kds-knowledge-intake
  amendment: GKE-001-COORDINATION-20260810-002-A6
  amendment_sha256: bba9f2f33a1c43066df551ba8b086bcaa5f3c2d655b2ca6af831aefb40ee8f3c
  reviewed_baseline: 755f7b5d3583601418fc51abc828837d4dc1df30
  audit_timestamp: 2026-08-10T02:28:51Z
  final_status: partial
  technical_decision: technical_revalidation_passed_governance_pending
  repository_state: uncommitted_allowlisted_delta_main_equals_origin_main
  phase_1_classification: simulated_only
  phase_2_authorized: false
  real_kds_or_mmc_write: false
  allow_archive: false
  status_ceiling: partial
  completion: not_complete
```

A6 在冻结的未提交 Studio 基线上完成六项返工。允许角色、authoritative target tenant/org、canonical v0.1 只读声明、确定性 SHA-256 与项目范围幂等键、1 MiB 文本文件边界和七类模拟浏览器场景均已实现并通过独立复跑。该结论只适用于 Phase 1 `simulated_only` 技术返工，不构成真实 Studio 登录态、KDS/MMC 读写、Brain E2E、`accepted`、`integrated` 或 Feature 完成。

## 独立证据

| Evidence ID | Source | Command/File | Result | Freshness | Trust Level | Status Impact |
|---|---|---|---|---|---|---|
| STUDIO-A6-R1 | Studio frozen worktree | exact changed-path scan | 14 个最终路径全部在 A6 allowlist，OpsX lock 缺失，HEAD 与 origin/main 均为 `755f7b5d` | current | machine_generated | scope verified |
| STUDIO-A6-R2 | Studio frozen worktree | focused Vitest | 3 files, 10/10 passed | current | machine_generated | implementation verified |
| STUDIO-A6-R3 | Studio frozen worktree | full Vitest | 312 files passed、1 file skipped；2740 passed、3 skipped、0 failed | current | machine_generated | regression baseline verified |
| STUDIO-A6-R4 | Studio frozen worktree | Playwright, Chromium, one worker, isolated port 8681 | 7/7 passed | current | machine_generated | simulated browser flow verified |
| STUDIO-A6-R5 | Studio frozen worktree | `npm run build` | passed | current | machine_generated | build verified |
| STUDIO-A6-R6 | Studio frozen worktree | OpenSpec strict, Loop validator, Harness, diff-check | all passed; LR-875 sealed and selected | current | machine_generated | local governance evidence valid |
| STUDIO-A6-R7 | Studio/KDS source comparison | typed declarations and delta scan | manifest pin `8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de`; no executable KDS/MMC method or local fact ledger | current | independently_reviewed | declaration-only boundary verified |

第一次 coordinator 浏览器复跑使用默认 `8679` 时与仍活跃的 Studio 清理动作冲突：首项通过后服务被终止，后续六项为连接拒绝。该轮不计产品证据。切换到独立端口 `8681` 后七项全部通过；F-013 独立会话也以单 worker 重放 7/7，通过结论一致。

## Finding 到证据

- `allowed_roles`：服务端仅允许 `admin`、`super_admin`；非允许角色返回无项目细节的 403。
- `authoritative_scope`：认证 tenant 匹配 binding tenant；target ref 解析出的 tenant/org 匹配 binding；permission 必须为 allowed；未修改用户映射、store 或 schema。
- `canonical_read_contract`：声明 v0.1 Stage A/B 八个只读端点及 snake_case 资产、版本、提取、内容、游标和 EvidenceLink 类型；无可执行网络调用。
- `deterministic_descriptor`：浏览器计算小写内容和项目范围 SHA-256，服务端校验精确幂等键。
- `file_boundary`：客户端与服务端都拒绝空文件、非 text/plain 或 text/markdown、超过 1 MiB 的文件。
- `browser_scenarios`：success、duplicate、409、429/502/503/504、failed/retry-blocked、403/404 no-leak、cancellation/navigation 共 7/7。

## 保持成立的阻塞

- A4 明示禁止 commit/push，但外部 daily sync 已形成 `1f63a464` 与 `755f7b5d` 远端历史；治理 owner 尚未处置，A5 不追认该行为。
- KDS Stage B 技术 handoff 已复核，但 KDS dirty admission、真实或共享 KDS 写入和生产迁移均未解除。
- MMC restricted relay 的技术复核不等于 prepare/retry 与完整 Studio intake 的生产准入；Phase 2 仍被阻塞。
- 真实角色、真实 KDS ACL/audit/lineage/read/write、Brain Search/WikiPreview/Chat E2E、MMC 委托和人工确认尚未执行。

## 后续边界

Studio A6 未提交工作树再次冻结。不得提交、推送、部署、进入 Phase 2、调用 KDS/MMC、创建知识事实或提升状态。下一步只能由 GKE-001 coordinator 在治理处置和后续精确 amendment 下继续串行编排。
