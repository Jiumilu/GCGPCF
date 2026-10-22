---
doc_id: GPCF-DOC-930D214E1F
title: PKC 候选接入页 E2E 报告（F-036 / F-034 M3 前置）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/reports/PKC候选页E2E报告.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/reports/PKC候选页E2E报告.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# PKC 候选接入页 E2E 报告（F-036 / F-034 M3 前置）

- 时间：2026-10-22T13:31:59.154Z
- 结论：通过

| 判据 | 结果 | 详情 |
|---|---|---|
| A3 默认 dry-run：未配置嵌入地址时无 iframe | ✓ | iframe 数=0 |
| A3 默认 dry-run：未发起外部请求 | ✓ | 请求源仅 http://127.0.0.1:49280 |
| A3b 未配置时给出空态与说明（含 VITE_PKC_EMBED_URL 指引） | ✓ | pkc-embed-disabled=1｜未配置受控嵌入地址 未设置 VITE_PKC_EMBED_URL：本页保持预演状态，不向 PKC 运行时发起任何请求。 |
| A8 非声明在位（候选态 + 不声明已接入等） | ✓ | 边界与非声明 不声明 PKC 已接入 / 已集成 / 生产就绪 / 客户验收； 本页为候选态演练入口，PKC 仓业务代码未由 WAE 侧改写； 受控嵌入只在配置 |
| A9 无 pageerror | ✓ | 0 条 |

> 非声明：本报告不声明 PKC「已接入/已集成/生产就绪/客户验收」；不提升任何 Feature/项目状态。
