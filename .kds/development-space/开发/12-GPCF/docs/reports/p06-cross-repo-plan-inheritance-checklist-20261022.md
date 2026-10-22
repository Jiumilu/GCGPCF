---
doc_id: GPCF-DOC-F2B6092574
title: P06 跨仓收尾清单：WAME / PVA 总体方案补继承声明（交属主执行）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p06-cross-repo-plan-inheritance-checklist-20261022.md
source_path: docs/reports/p06-cross-repo-plan-inheritance-checklist-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P06 跨仓收尾清单：WAME / PVA 总体方案补继承声明（交属主执行）

- 日期：2026-10-22｜依据：老卢 Q（P06 授权）+ 群级纪律⑤「跨项目仓改动由属主执行，GPCF 只出清单」
- GPCF 侧已修完：plan register 路径/拼写/缺行（WAS、PVA、GPCF 三处路径 + `GlobalCoud`→`GlobalCloud` + Project/FireQuote 两行）
- 剩余 2 项为**跨仓文档改动**，GCPF 不代写

## 1. 校验器原文

```text
validate_project_plan_inheritance.py:
  GlobalCloud WAME 总体方案.md: missing control token GPCF:01-architecture/GlobalCloud 项目群总体方案.md
  GlobalCloud PVA 总体方案.md: missing control token GPCF:01-architecture/GlobalCloud 项目群总体方案.md
```

## 2. 属主执行步骤

### WAME（`GlobalCloud WAME/GlobalCloud WAME 总体方案.md`）

在文档头部「继承关系」或「控制口径」章节补一行（与 WAE/GPCF 等已通过项目一致）：

```text
继承：GPCF:01-architecture/GlobalCloud 项目群总体方案.md（项目级总体方案必须继承项目群总体方案）
```

### PVA（`GlobalCloud PVA/GlobalCloud PVA 总体方案.md`）

同样补一行：

```text
继承：GPCF:01-architecture/GlobalCloud 项目群总体方案.md（项目级总体方案必须继承项目群总体方案）
```

## 3. 完成判据

```bash
cd "../GlobalCloud GPCF"
python3 tools/kds-sync/validate_project_plan_inheritance.py   # exit 0
python3 tools/kds-sync/validate_project_master_plan_register.py  # exit 0（已通过）
```

## 4. 回滚

文档单行改动，`git revert` 即可；不涉及代码与数据。
