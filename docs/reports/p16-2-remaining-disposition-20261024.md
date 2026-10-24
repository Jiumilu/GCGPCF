---
doc_id: GPCF-DOC-8686649F2F
title: "P16-2 剩余缺口逐仓判定（2026-10-24 15:50）"
project: KDS
related_projects: [GPC, KDS, PKC, XGD, MMC, GPCF, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/p16-2-remaining-disposition-20261024.md
source_path: docs/reports/p16-2-remaining-disposition-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P16-2 剩余缺口逐仓判定（2026-10-24 15:50）

- 背景：本轮起按"逐仓核实真实验证入口 → 决策模型裁决 → 只采纳 yes"的方式推进（已补 PQC/SOP/KDS/ICP/AAAS/Mem/FireQuote 共 7 仓）
- 现状：standards **29/29**、test **25/29**、build **21/29**（另有 1 仓因扫描口径修正由缺转有：PMC）
- 原则：**不为凑指标造假 job**；下面每个剩余仓都写明真实原因与建议

## 1. 缺 test 的仓（3）

| 仓 | 实测 | 判定 | 建议 |
|---|---|---|---|
| GlobalCloud WAS | 无 pytest 文件；`make validate` 仅调用 gc_standard（standards 已覆盖） | **无真实测试套件** | 属主决定：补最小冒烟测试，或按"文档/语义仓"申请 P16-2 豁免（需老卢裁定） |
| GlobalCloud XWAIL | 同上；有 `scripts/verify_xap.py`、`xap_verify.py` 但无测试框架 | **无真实测试套件** | 属主可把 verify 脚本包装成 pytest 用例（低成本） |
| GlobalCloud DRC | 仅有 docs 与占位 Makefile 目标 | **无代码可测** | 建议登记 P16-2 豁免（文档仓） |

## 2. 缺 build 的仓（3，MMC 已闭环）

| 仓 | 现状 | 判定 | 建议 |
|---|---|---|---|
| GlobalCloud MMC | 已有 `mmc-ci.yml`（pytest 23 文件 + 契约脚本 + sdk vitest） | ✅ **已补**：2026-10-24 追加 AST 解析 build job（模型 yes 0.621） | 无需属主动作；如不喜欢可回滚 |
| GlobalCloud XGD | `npm run quality:ci` 已含 typecheck + 多个 test/smoke | `build` = electron-builder 三平台打包（重） | 建议以 `npm run typecheck` 作为 build 替代判定，属主确认 |
| GlobalCloud SpaceAI Studio | 无任何构建命令；`node --test` 有测试 | 缺构建 | 属主补 `pnpm -r build` 或声明 legacy 豁免 |
| GlobalCloud PKC | 本地 `npm test` 151 passed、`npm run build` 可用 | 模型裁决 **no 0.455**，按授权边界未执行 | 交属主自行添加（GPCF 不越权） |

## 3. 本轮顺带修正的扫描口径（第 3 次）

| 轮次 | 新增能力 | 效果 |
|---|---|---|
| 第 2 次 | 解析 `run` 引用的本地脚本（`bash scripts/gate.sh`） | PVA/WAE 等由误报转真 |
| 第 3 次 | 展开 npm/pnpm 脚本体（`quality:ci` 递归 3 层） | XGD/SpaceAI Platform/Studio 转真 |
| 第 4 次（本轮） | 识别 `pnpm turbo run build` 等 monorepo 命令 | PMC 由缺 build 转真 |

## 4. 结论

- 指标已接近真实上限：剩余 test 缺口 3 个、build 缺口 3 个，**都不是"漏配 CI"而是"确无测试/无构建产物或模型裁决不通过"**；
- 若要让 P16-2 达到 29/29，需要：WAS/XWAIL 补最小测试、MMC/SpaceAI Studio 补 build job、XGD 确认 typecheck 替代、DRC 豁免裁定、PKC 属主自加。

> **口径提醒（2026-10-24 16:20）**：本文件所说的已补/已覆盖均指**工作区口径**。按已跟踪文件口径，真正进 CI 的为 test 18/29、build 16/29；差集是 GPCF 已准备但未提交的 7 个仓（AAAS、KDS、SOP、ICP、PQC、Mem、FireQuote），需属主提交后才生效。
