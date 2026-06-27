---
doc_id: GPCF-DOC-PROJECT-GROUP-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626
title: GlobalCloud 项目群 KDS Diff Check Cleanup 授权命令包 2026-06-26
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-kds-diffcheck-cleanup-command-pack-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-kds-diffcheck-cleanup-command-pack-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 KDS Diff Check Cleanup 授权命令包 2026-06-26

## 1. 任务信息

| 项 | 内容 |
|---|---|
| task_id | `GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001` |
| 授权项 | `AUTH-KDS-DIFFCHECK-CLEANUP-20260626` |
| 前置证据 | `globalcloud-project-group-kds-diffcheck-blocker-20260626.md` |
| 当前结论 | `project_group_kds_diffcheck_cleanup_command_pack_20260626 = controlled` |
| 状态候选 | `kds_diffcheck_cleanup_command_pack_ready` |
| command_pack_count | `1` |
| recheck_date | `2026-06-27` |
| target_repo | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS` |
| target_path | `.env.production.example` |
| current_live_git_gate | `blocked` |
| current_blocker | `sensitive_path_review_required` |
| authorization_granted | `false` |
| cleanup_executed | `false` |
| kds_api_sync_executed | `false` |
| commit_executed | `false` |
| push_executed | `false` |

本文保留 `AUTH-KDS-DIFFCHECK-CLEANUP-20260626` 历史授权项编号，但按 2026-06-27 live recheck 重新解释为 KDS sensitive path review / optional cleanup command pack。当前 `git diff --check` 仍为 pass，项目群 Git gate 的真实硬阻塞已从历史 whitespace/diffcheck blocker 切换为 `GlobalCloud KDS/.env.production.example` 的 `sensitive_path_review_required`。本文只定义执行前命令、预期证据、门禁、回滚和禁止声明，不修改 KDS 文件，不执行真实 KDS API 写入，不 stage、commit、push。

## 2. 执行前命令包

| 阶段 | 目的 | 命令/动作 | 预期证据 | 门禁 | 回滚/停止边界 |
|---|---|---|---|---|---|
| precheck | 确认 KDS 仓当前状态和 sensitive path 仍存在 | `cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"`；`git status --short --untracked-files=all`；`git diff --check -- .`；`git ls-files --stage -- .env.production.example` | `docs/harness/KDS/evidence/kds-sensitive-path-review-precheck-*.md` | KDS sensitive path precheck gate | 若 `.env.production.example` 不再处于 Git gate 敏感路径集合，停止并重新建证据 |
| classify | 确认 `.env.production.example` 的模板属性、跟踪方式和授权路线 | `test -f .env.production.example`；`sed -n '1,120p' .env.production.example`；`git check-ignore -v .env.production.example || true` | `docs/harness/KDS/evidence/kds-sensitive-path-classification-*.md` | sensitive path classification gate | 若发现真实密钥、TOKEN 或生产凭据，立即停止并转入安全阻断，不进入 cleanup |
| cleanup | 仅在显式授权后按分类结论执行路径归类、改名、忽略或删除之一 | 允许的动作必须严格落在授权回执声明的 route：`keep_with_owner_ack` / `rename_to_non_sensitive_template` / `move_out_of_git_scope` / `delete_as_noise`；默认不执行任何文件改动 | `docs/harness/KDS/evidence/kds-sensitive-path-cleanup-diff-*.patch` | sensitive path cleanup gate、authorization receipt gate | 若 diff 超出授权 route，或出现内容事实变更，立即回滚 cleanup |
| verify | 复核 KDS 局部门禁 | `git diff --check -- .`；`git diff -- .env.production.example`；`git status --short --untracked-files=all` | `docs/harness/KDS/evidence/kds-sensitive-path-verify-*.md` | KDS sensitive path verify gate | 若 `.env.production.example` 仍被识别为 sensitive_path，保持 `sensitive_path_review_required` |
| project_group_gate | 复跑项目群 Git clean 门禁 | `python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --allow-non-pass-exit-zero` | `docs/harness/evidence/globalcloud-project-group-git-clean-after-kds-diffcheck-cleanup-*.md` | project group Git clean gate | 若其它仓仍 dirty/blocked，仍不得声明项目群 Git 全量 clean |
| receipt | 登记授权回执和执行证据 | 更新授权回执总账，登记 `AUTH-KDS-DIFFCHECK-CLEANUP-20260626` 的授权来源、执行时间、命令输出和回滚点 | `docs/harness/KDS/evidence/kds-diffcheck-cleanup-receipt-*.md` | receipt ledger gate、Loop document gate | 未登记回执不得进入 stage、commit、push |

## 3. 执行约束

| 约束 | 要求 |
|---|---|
| scope | 只允许处理 `GlobalCloud KDS/.env.production.example` 的 sensitive path review 和授权后 route-specific cleanup |
| content_boundary | 不写入真实密钥、TOKEN、生产凭据；不把模板文件伪造成真实运行配置；不改变业务事实 |
| api_boundary | 不执行真实 KDS API 同步 |
| git_boundary | 不 stage、commit、push，除非另有明确授权 |
| evidence_boundary | 必须生成 cleanup evidence 和回执后才能传导状态 |
| status_boundary | cleanup 通过也只能尝试解除 KDS sensitive_path 硬阻塞，不自动升级 accepted/integrated/customer accepted |

## 4. 状态传导

| 输入状态 | 授权后成功输出 | 失败/未授权输出 |
|---|---|---|
| `kds_diffcheck_blocker_controlled / diff_check_pass_current` | `kds_sensitive_path_cleanup_verified_candidate` | `kds_diffcheck_blocker_controlled / diff_check_pass_current` |
| `project_group_git_clean = blocked` | 只在项目群 Git clean gate 复核后更新，不由本文直接改变 | `project_group_git_clean = blocked` |
| `ready_for_review_advancement_queue_ready` | 可进入下一轮 Git clean 收口审查 | 保持队列受控但不得升级 |

## 5. 禁止声明

```text
authorization_granted=false
cleanup_executed=false
kds_api_sync_executed=false
commit_executed=false
push_executed=false
accepted=false
integrated=false
production_ready=false
customer_accepted=false
```

- 不声明 KDS diff check 已修复。
- 不声明 KDS sensitive_path 已解除。
- 不声明项目群 Git 全量 clean。
- 不声明 KDS API 已同步。
- 不声明任何项目已自动升级到 `ready_for_review`。
- 不声明 review、stage、commit、push、merge、deploy、release 或客户验收已经发生。
