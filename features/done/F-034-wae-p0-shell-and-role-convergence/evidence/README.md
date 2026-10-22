---
doc_id: GPCF-DOC-FB2AE48234
title: F-034 证据包（WAE 侧）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/README.md
source_path: features/done/F-034-wae-p0-shell-and-role-convergence/evidence/README.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-034 证据包（WAE 侧）

> 这是 **WAE 仓内的证据包**，不是 GPCF 的官方证据归档。
> 官方归档目标：`GlobalCloud GPCF/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/`
> ——**跨仓写入，需老卢授权**；本包是"待复制源"，授权后按同结构复制即可。

## 一、目录

| 路径 | 内容 |
|---|---|
| `collect.sh` | 采集脚本：真跑 12 条判据命令，写 `logs/<id>.log` + `logs/<id>.exit` |
| `logs/` | 每条命令的原始输出 + 退出码（**唯一结果来源**，不手写） |
| `screens/` | 真机截图：双角色 admin/viewer、PKC dry-run、M2 能力阀 on/off、WAME 回归 |
| `manifest.json` | 机器可读清单：命令、退出码、结果、日志路径、截图 sha256/字节数、commit |
| `summary.md` | 人读版：M1 判据逐项对账 + 非声明 + 剩余项 |

## 二、怎么重放（两步）

```bash
# ① 采集：真跑 12 条命令（约 3–5 分钟；e2e 会各自起独立 dev 端口）
bash docs/evidence/F-034/collect.sh

# ② 汇总：校验存在性 + 算 sha256 + 读退出码 → 重写 manifest.json
pnpm evidence:collect
```

> 退出码语义：`0=pass`；`2=环境不可用(skip)`；`11(采集侧记为 1)=预期差异`（跨仓令牌比对）；其它=`fail`。
> **没有日志的项一律标 `missing`，不猜结果。**

## 三、本次清单（2026-10-22 夜）

`total=12 ｜ pass=11 ｜ expected_diff=1 ｜ skip=0 ｜ fail=0 ｜ missing=0`

| id | 判据 | 命令 | 结果 |
|---|---|---|---|
| 01 | 框架全量单测 | `pnpm test` | pass |
| 02 | 框架 typecheck | `pnpm typecheck` | pass |
| 03 | WAME 全量单测 | `pnpm --dir apps/wame exec vitest run` | pass |
| 04 | WAME 生产构建 | `pnpm --dir apps/wame exec vite build` | pass |
| 05 | **双角色收敛 E2E** | `pnpm e2e:dual-role` | pass（admin 7 项可见 + users 200；viewer 0/0 + users 403；pageerror 0） |
| 06 | **PKC 候选页 dry-run E2E** | `pnpm e2e:pkc-intake` | pass（无 iframe、无外部请求、非声明在位、pageerror 0） |
| 07 | 落位校验 P001–P010 | `pnpm check:apps` | pass |
| 08 | 生成物新鲜度 | `pnpm gen:apps --check` | pass |
| 09 | 装配×落位对账 A1–A4 | `pnpm check:app-assembly` | pass |
| 10 | 注册表/加载器一致性 | `pnpm check:registry` | pass |
| 11 | O2 跨仓令牌一致性（只读） | `pnpm check:tokens-parity` | **expected_diff**（PKC 快照过期；见比对报告） |
| 12 | 框架包构建（A2 后 6 包） | `pnpm build:packages` | pass |

## 四、纪律

1. 本包**不提升**任何 Feature/项目状态；F-034 仍 `active/plan`；
2. 截图与日志是**真跑产物**，不接受"设计态代替真机"；
3. 跨仓归档、向 PKC/Brain 属主发整改请求，均需老卢点头后执行。
