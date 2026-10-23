---
doc_id: GPCF-F-019-EVIDENCE-SUMMARY-ICP-INDUSTRY-CONSOLE
title: F-019 证据索引（evidence summary）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-019-icp-industry-console/evidence/summary.md
source_path: features/done/F-019-icp-industry-console/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# F-019 证据索引（evidence summary）

> 交付方式：本线（Hermes）实施 M1-M2；本目录为**如实**证据索引（每条可溯源）。

## 1. 服务化（ICP 侧）

| 项 | 结果 |
|---|---|
| API 启动 | `PYTHONPATH=src python3 -m uvicorn gc_icp.api:app --port 8091`·health 200 |
| CORS | GET 带 Origin → `access-control-allow-origin: http://localhost:4300` ✓ |
| OPTIONS 预检 | 200＋`access-control-allow-methods: GET, OPTIONS` ✓ |
| 测试套件 | **33/33 passed**（改动后复验） |
| 5 GET 实测 | health（24/11/3·candidate/partial/human_required）｜industry-model｜resource-pools（projectionOnly）｜scenarios（3）｜constitution-governance（5 角色） |

## 2. 提交记录（changelog）

| 仓 | 提交 | 说明 |
|---|---|---|
| ICP | `80b8aaa` | CORS 接入 WAE 宿主（M1·D1.2） |
| WAE | `e84c7de` | 模块包＋母本第 7 项＋对账表 v0.7（M2） |
| WAE | `f87a27a` | lockfile 补全 |
| KDS | `02dd054b` | registry v0.7（icp-console available·README 16） |
| KDS | `c57894b6` | 规划件 v0.1＋总索引登记 |

## 3. E2E 真机（浏览器）

- 地址：`http://localhost:4300/global-cloud-workbench/icp`（WAE 母本·第 7 项）。
- 六页签：概览/产业模型/资源池/场景/控制决策/宪法治理——切换实测通过。
- 关键断言：产业模型表 **24 行**（含 material.gypsum）｜资源池 **11 行**＋projectionOnly 徽章｜场景卡（板—箱/进入门禁/证据/退出）｜宪法角色矩阵（industry_domain_owner 等）。
- 截图（本地）：`~/.hermes/cache/scratch/icp_console_v1.png`。

## 4. 诚实记录（不作为验收声明）

- 只读边界：模块零写路径（grep）；CORS 仅 GET/OPTIONS；POST（评估/回放/修订候选）一期不接（分级见规划 §一）。
- 候选态：全域 candidate/partial/human_required 如实标注；`productionReady=false`。
- 生产就绪声明：`production_ready=false`（无生产/发布/接受声明）。

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: pass
- api: fail
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: 未授权 commit、push、deploy、真实 API、状态提升。
<!-- GPCF_EVIDENCE_GATE_END -->

## 2026-10-23 API 复核

- 启动 `gc_icp.api:app` :8091，5 个 GET 全部 200：health / industry-model / resource-pools / scenarios / constitution-governance。
- `PYTHONPATH=src python3 -m pytest -q` → 33 passed。
- api evidence 更新为 pass；summary 更新为 pass；服务已停止。
- multi_user_usability 仍 pending（三角色实测未做），不声明关闭。

## 2026-10-24 multi_user 处置

- 控制台为只读；角色可见性由 WAE shell 收敛（F-034 双角色 E2E 已证 admin 可见 / viewer 不可见）。
- 控制台内“角色矩阵”是展示内容，不是访问控制；按“无新增多用户行为”waive `multi_user_usability`。
- C_dev 不变（ICP-VU-03 保持 S2）；如后续升 S3 需单独授权。
