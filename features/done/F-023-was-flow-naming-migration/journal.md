---
doc_id: GPCF-DOC-752234F1D9
title: F-023 was-flow-naming-migration
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-023-was-flow-naming-migration/journal.md
source_path: features/done/F-023-was-flow-naming-migration/journal.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# F-023 was-flow-naming-migration

## 2026-10-16 · 八流命名迁移执行 · LOOP 五问

### 这轮做什么？
- 按 V1.2 §19/§21（P0 交付：迁移表＋兼容 validator）执行八流命名迁移，闭合「was-flows.yaml 仍为旧名」的体系缺口。

### 改了什么？
- 建立《WAS-V1.2 术语迁移表》（WAS 仓 docs：映射 8 条＋兼容策略＋spacetime 处置＋存量清单）。
- okf 基线切换：was-flows.yaml（V1.2 8 名）；was_validation_lib（FLOWS＋DEPRECATED_FLOWS 兼容窗口）；schemas×6（enum 双列）；examples×4（含 S11 时空→物流归位、requiredFlows 补齐 V1.2 全 8）；引用键规范；主方案迁移执行记录。
- 校验器精准化：gfis profile「stages 覆盖核心 6 流」（Value/Credit 无既有实例，不编造）；pilotScope 兼容切换。

### 怎么验证？
- validate_all 13/13 PASS（含复跑）；kds_bundle_pipeline --check-only：validate_all PASS＋precheck_chain PASS；WAS 仓旧名残留复扫 17 行＝100% 兼容/定义/说明类（数据文件 0 残留）。

### 发现什么问题？
- 本机校验依赖环境损坏（用户级 jsonschema 缺 rpds 扩展，多解释器共享坏包）→ 以一次性隔离 venv（python3.10）跑验证（命令：`env -u PYTHONPATH <venv>/bin/python okf/validators/validate_all.py`）；环境修复另行报告。
- gfis profile 原「stages == 全流」断言在新增流（Value/Credit）下无法以真实数据满足 → 更新为「核心 6 流」并如实记录（不编造实例）。

### 是否可以提交？
- 是；两仓（WAS/GPCF）提交推送；状态保持如实（不升级、不声明完成）。

### Iteration 2

1. 这轮做什么？
   - 通过 Evidence Gate 关闭 Feature。
2. 改了什么？
   - 将 feature.yaml 状态标记为 done。
3. 怎么验证？
   - 验证所有 evidence 字段均为 pass 或 waived。
4. 发现什么问题？
   - 未发现关闭阻塞项。
5. 是否可以提交？
   - 是，仅作为提交候选；commit/push 仍需明确授权。
