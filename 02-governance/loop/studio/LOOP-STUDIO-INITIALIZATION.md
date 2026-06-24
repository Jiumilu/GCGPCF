---
doc_id: GPCF-DOC-31D8E9632A
title: GlobalCloud Studio LOOP Initialization
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, PKC, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/studio/LOOP-STUDIO-INITIALIZATION.md
source_path: 02-governance/loop/studio/LOOP-STUDIO-INITIALIZATION.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud Studio LOOP Initialization

## 启动声明

本轮在 GPCF LOOP 治理框架下，启动 GlobalCloud Studio 的 L4 实施 LOOP。

## LOOP 参数

| 参数 | 值 |
|------|-----|
| 模式 | L4 |
| Round ID 前缀 | `GPCF-STUDIO-LR` |
| 总预算 | 10 小时（用户明确授权，超越默认 L4 4 小时上限） |
| 最多轮次 | 20 轮 |
| 工作目录 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC`（当前） |
| 目标仓库 | `GlobalCloud Studio`（由 XiaoG 全量拷贝 + PKC 服务层新建） |
| KDS TOKEN | `bfd9553d`（私有文件，不入库） |
| 数据源 | KDS :8080（经 MMC :8000），dev 模式可旁路 |

## 实施目标（10小时）

### Goal 1：Studio monorepo 骨架（~1.5h）
- 创建 `GlobalCloud Studio` monorepo
- XiaoG 全量源码拷贝到 `packages/`
- pnpm workspace 配置
- `pnpm dev` 可运行，原有功能不变

### Goal 2：核心基础设施层（~2.5h）
- 实现 `packages/server/src/services/core/mmc-client.ts`
- 实现 `packages/server/src/services/core/kds-client.ts`
- KDS 搜索/读取/写入 全链路验证
- MMC Registry 注册 gpc_green_supply_chain（占位）

### Goal 3：知识治理服务层（~3h）
- 实现 `services/governance/task-state-machine.ts` + vitest 全通过
- 实现 `services/governance/doctor-service.ts` + vitest
- 实现 `services/governance/agent-run-service.ts`
- 实现 `services/governance/ask-service.ts`
- 数据库 Migration（SQLite）

### Goal 4：端到端验证（~2h）
- Studio BFF → MMC → KDS 搜索链路验证
- Studio BFF → MMC → KDS 文档读取验证
- Studio BFF → MMC → KDS 文档创建验证
- 对话 Function Calling：搜索 KDS 返回运营数据

### Goal 5：治理闭环（~1h）
- XiaoG 补齐 PROJECT_HARNESS_MANIFEST.md
- 各 LOOP round 文档归档到 GPCF
- loop_document_gate.py pass
- Git 状态 clean（仅受控变更）

## 边界

- ✅ 允许：读取/分析本地文档、创建受控文档、实现代码、运行测试、dry-run/mock
- ✅ 允许：经 MMC dev mode 旁路调用 KDS
- ✅ 允许：本地 Git 变更（不 push）
- ❌ 禁止：Git push、生产写入、真实外部 API、bench migrate、部署
- ❌ 禁止：写入真实 KDS TOKEN 到代码/文档
- ❌ 禁止：触碰 GFIS/GPC Docker 运行态

## 停止条件

| 类型 | 条件 |
|------|------|
| hard_stop | 系统异常、文件损坏 |
| user_stop | 用户明确停止 |
| budget_exhausted | 10 小时用尽 |
| authorization_boundary | 触及禁止操作边界 |
| completed | 5 个 Goal 全部验收通过 |

## 状态跟踪

| 字段 | 初始值 |
|------|--------|
| declared_rounds | 0/20 |
| substantive_rounds | 0/20 |
| generated_items | 0 |
| substance_gate | pending |
| stop_type | not_applicable |
