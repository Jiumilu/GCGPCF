---
doc_id: GPCF-DOC-CD4AF0C1EA
title: P16-3 · UI 仓 e2e / browser / a11y 验收草案
project: GPCF
related_projects: [GPCF, GPC, WAME, PKC, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p16-3-ui-acceptance-draft-20261022.md
source_path: docs/reports/p16-3-ui-acceptance-draft-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P16-3 · UI 仓 e2e / browser / a11y 验收草案

- 日期：2026-10-22｜状态：草案（未接门禁；接入需授权）
- 基线：浏览器与无障碍基线取 **WAE AppsShell**（`pnpm vitest run apps/shell` + DOM 用例）

## 1. UI 仓名单（6 个）

| 仓 | 理由 | 当前 e2e/browser/a11y |
|---|---|---|
| GlobalCloud WAE | 统一壳与角色收敛载体 | 无（需新建） |
| GlobalCloud PKC | 经 WAE 接入（F-036），不自建壳 | 无（随 WAE） |
| GlobalCloud PDC | Web + Electron 双形态 | 无 |
| GlobalCloud GPC | 消费端页面与流规则包回放 | 无 |
| GlobalCloud PQC | 报价作业页（试点项目） | 无 |
| GlobalCloud Studio | **已退役**，仅作历史基线引用 | 不要求 |

## 2. 每仓最低验收（草案）

| job | 最低要求 |
|---|---|
| e2e | 1 条**用户任务完成**用例（不是元素存在）：如"查资产→看详情→返回保持筛选" |
| browser | 1 条真实浏览器运行（Playwright/Chromium），断言 pageerror=[] + 关键 DOM |
| a11y | 1 条自动扫描（axe 或等价），严重级 0 违规；人工检查另记 |

## 3. 与 LOOP UI 硬规则的对应

- `task_flow_e2e`：必须验证用户任务完成，不接受"元素可见"；
- `evidence_overexposure`：机器字段/证据默认折叠；
- `multi_user`：至少 admin/viewer 双角色各 1 条；
- 任一 required gate pending ⇒ 状态上限 `partial`。

## 4. 落地顺序建议

1. 先在 WAE 建基线（browser + a11y）；
2. PQC/PDC 各 1 条用户任务 E2E（真实试点优先）；
3. 再推广到 GPC 与 PKC。

## 5. 需要授权

`_governance/ci-matrix.yaml` 中 P16-3 相关字段由草案转 required **需另行授权**（属全群门禁变更）。
