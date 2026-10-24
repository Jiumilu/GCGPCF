---
doc_id: GPCF-DOC-OWNER-ACTION-INDEX-20261024
title: 属主动作包索引（2026-10-24）
project: GPCF
related_projects: [KDS, GFIS, GPC, WAME, Brain, PKC, GPCF, Studio, ICP]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/owner-action-index-20261024.md
source_path: docs/harness/evidence/owner-action-index-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# 属主动作包索引

| Feature | 包 | 需要谁 |
|---|---|---|
| F-022 | `features/active/F-022.../evidence/owner-action-pack-20261024.md` | WAS 属主 |
| F-034 | `features/active/F-034.../evidence/owner-action-pack-20261024.md` | Brain/Studio/PKC 属主 |
| F-036 | `features/active/F-036.../evidence/owner-action-pack-20261024.md` | WAE/PKC 属主 + 老卢 |
| F-012 | `features/active/F-012.../evidence/owner-action-pack-20261024.md` | SOP/ICP 属主 |
| F-032 | `features/active/F-032.../evidence/owner-action-pack-20261024.md` | PQC/PVA 属主 |
| F-038 | `features/active/F-038.../evidence/owner-action-pack-20261024.md` | SpaceAI 属主 |
| F-025 | `features/active/F-025.../evidence/owner-action-pack-20261024.md` | WAME/SpaceAI/World 属主 |
| 批次 2 | `docs/harness/evidence/batch2-input-intake-form-20261024.md` | GFIS/GPC 属主 |
| 全局 | `docs/harness/evidence/owner-action-tracker-20261024.md` | 各属主 |
| 阻塞 | `docs/harness/evidence/goal-blocker-register-20261024.md` | GPCF |

## 使用方式

1. 属主打开对应包，按「需属主动作」执行；
2. 完成后回传证据路径；
3. GPCF 更新 blocker/resolved，再走 check-only + 关闭授权。

## 非声明

- 本索引不构成授权；不声明任何事项已完成。

## PMC 路由（2026-10-24）

父项：**GC-356**（[GPCF] 属主待办：F-022/F-034/F-036/批次2）

| 子项 | Ref | 属主 |
|---|---|---|
| F-022 场景流复核 | GC-357 | WAS |
| F-034 Brain 令牌 | GC-358 | Brain |
| F-034 侧栏/M3 | GC-359 | Studio/PKC |
| F-036 部署/SSO/签字 | GC-360 | WAE/PKC |
| 批次2 GFIS 单据 | GC-361 | GFIS |
| 批次2 GPC PG-11 | GC-362 | GPC |
| F-038 人工验收 | GC-363 | SpaceAI |
| F-012 引用清单 | GC-364 | SOP/ICP |
| F-032 接口清单 | GC-365 | PQC/PVA |
| F-025 架构迭代 | GC-366 | WAME/SpaceAI/World |

状态（2026-10-24）：10 个子项均已从 Backlog 置为 **Todo**；仍不替代属主签署。

说明：PMC 子项为路由/跟踪，不替代属主签署；完成后回传证据路径，GPCF 再清 blocker。

## 回执登记

- `runtime/owner-receipts.yaml`：10 个属主回执（GC-357..GC-366），当前 10 pending。
- 校验：`python3 tools/kds-sync/validate_owner_receipts.py`。
- approved 必须填 signed_by/signed_at/evidence_paths，且 evidence 文件存在。

## 回执录入命令

```bash
python3 tools/kds-sync/record_owner_receipt.py \
  --ref GC-357 --status approved \
  --signed-by WAS --signed-at 2026-10-24 \
  --evidence path/to/receipt.md \
  --note "六项声明已签"
```

- 默认写 `runtime/owner-receipts.yaml` 并自动跑校验；
- `approved` 必须带签署人/日期/证据路径；
- 可先加 `--dry-run` 预览。
\n