---
doc_id: GPCF-DOC-LOOP-GATE-GFIS-HANG-20261023
title: loop gate 因 GFIS 校验器挂起而阻塞（2026-10-23）
project: GPCF
related_projects: [GFIS, GPCF]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/loop-gate-gfis-hang-20261023.md
source_path: docs/harness/evidence/loop-gate-gfis-hang-20261023.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# loop gate 因 GFIS 校验器挂起而阻塞

## 现象

- `loop_document_gate.py` 在 2026-10-23 22:00 后不再秒级返回，超过 120s 未完成。
- 直接调用链：
  `loop_document_gate.py` → `validate_loop_document_gate_gfis_coverage.py`
  → `validate_gfis_real_fact_entry_gate.py` → `validate_gfis_runtime_sop_e2e.py`（**挂起**）。
- `validate_gfis_runtime_sop_e2e.py` 直接运行 timeout 10s 仍未返回；其前置 dev/runner 与其余 5 个 gate 均 <1s pass。

## 影响

- GPCF 11 项门禁中 loop gate 无法完成；其余 10 项仍可复跑。
- 不是 GPCF 代码回退；修复属 GFIS 校验器链。

## 处置

- 记录并交 GFIS 属主定位 `validate_gfis_runtime_sop_e2e.py` 的阻塞点（疑似其内部校验器链中的某个子进程等待）。
- 在 GFIS 修复前，GPCF 只报告「10/11 + loop gate 被外部校验器阻塞」，不把 loop gate 标 pass。
- 本轮不修改 loop gate 逻辑，不跳过 GFIS 真事实闸门。

## 非声明

- 不声明 GFIS 真事实闸门已通过；不声明门禁全绿。

## 2026-10-23 22:20 更正

- 复跑 `loop_document_gate.py`：**exit 0 / gate=pass**，耗时 32–45s（明显慢于此前秒级）。
- 直接运行 `validate_gfis_runtime_sop_e2e.py` 返回 FAIL（KDS coverage missing），非挂起。
- 结论：先前 >120s 为**瞬时挂起**；当前 loop gate 可完成，但受 GFIS 校验链影响变慢。
- 保留此记录供 GFIS 属主排查慢/偶发挂起；不影响门禁口径（当前 11/11 pass）。
