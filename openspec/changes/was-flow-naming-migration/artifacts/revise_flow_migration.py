#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WAS 八流命名迁移执行（2026-10-16）——dry-run → apply
覆盖：okf/was/was-flows.yaml（重写）、okf/validators/was_validation_lib.py、
okf/schemas/*.json(5)、okf/examples/*.yaml(4)、docs/WAS引用键与数据出口字段规范、主方案记录
"""
import subprocess
import sys
from pathlib import Path

BASE = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系")
APPLY = "--apply" in sys.argv

OLD_KEYS = ["material_flow", "information_flow", "capital_flow", "spacetime_flow",
            "energy_flow", "commerce_flow", "knowledge_flow", "rule_flow"]


def rep(path, old, new, exp=1, label=""):
    p = Path(path)
    t = p.read_text(encoding="utf-8")
    c = t.count(old)
    assert c == exp, "[%s] 命中 %d != %d: %s | %s" % (label, c, exp, path, old[:70])
    if APPLY:
        p.write_text(t.replace(old, new), encoding="utf-8")
    print("[%s] %s | %s" % ("已改" if APPLY else "待改", label, p.name))


# ── 1) was-flows.yaml 全量重写 ──
P_YAML = BASE / "okf/was/was-flows.yaml"
t = P_YAML.read_text(encoding="utf-8")
assert all(k + ":" in t for k in OLD_KEYS), "was-flows.yaml 旧键不全"
NEW_YAML = """# 2026-10-16 迁移：OKF P0 旧名 -> V1.2 规范名（映射与兼容策略见 docs/WAS-V1.2术语迁移表.md）
flows:
  LogisticsFlow:
    description: Movement and transformation of physical assets
    examples: [move, store, transform, produce, deliver, recycle]
  InformationFlow:
    description: Movement and synchronization of data and knowledge assets
    examples: [collect, report, validate, publish, sync, cite, create, transfer, train, infer, reuse, patent]
  FinancialFlow:
    description: Movement and allocation of economic assets
    examples: [invest, pay, settle, distribute, finance, account]
  EnergyFlow:
    description: Supply and consumption of energy
    examples: [supply, consume, convert, meter, optimize]
  ServiceFlow:
    description: Commercial exchange and service delivery
    examples: [quote, order, contract, deliver_service, trade, procure]
  ControlFlow:
    description: Enforcement and propagation of rules
    examples: [enforce, approve, block, review, escalate, confirm]
  ValueFlow:
    description: Value creation, augmentation, distribution, consumption and attribution
    examples: [create_value, augment, distribute, consume, attribute]
  CreditFlow:
    description: Credit, scoring, guarantee, trust and performance reputation changes
    examples: [score, guarantee, trust, endorse, reputation_change]
"""
if APPLY:
    P_YAML.write_text(NEW_YAML, encoding="utf-8")
print("[%s] was-flows.yaml 重写（8 旧键 -> V1.2 8 名 + Value/Credit）" % ("已改" if APPLY else "待改"))

# ── 2) validator ──
V = BASE / "okf/validators/was_validation_lib.py"
FLOWS_OLD = '''FLOWS = {
    "material_flow",
    "information_flow",
    "capital_flow",
    "spacetime_flow",
    "energy_flow",
    "commerce_flow",
    "knowledge_flow",
    "rule_flow",
}'''
FLOWS_NEW = '''# V1.2 规范名（2026-10-16 迁移：OKF P0 旧名 -> V1.2；映射见 docs/WAS-V1.2术语迁移表.md）
FLOWS = {
    "LogisticsFlow",
    "InformationFlow",
    "FinancialFlow",
    "EnergyFlow",
    "ServiceFlow",
    "ControlFlow",
    "ValueFlow",
    "CreditFlow",
}
# 兼容窗口：旧名（deprecated）仍被数据级校验接受；窗口关闭时旧名将报失败
DEPRECATED_FLOWS = {
    "material_flow",
    "information_flow",
    "capital_flow",
    "spacetime_flow",
    "energy_flow",
    "commerce_flow",
    "knowledge_flow",
    "rule_flow",
}
ACCEPTED_FLOWS = FLOWS | DEPRECATED_FLOWS'''
rep(V, FLOWS_OLD, FLOWS_NEW, 1, "validator-FLOWS/DEPRECATED")
rep(V, 'require(relationship["flowType"] in FLOWS,', 'require(relationship["flowType"] in ACCEPTED_FLOWS,', 1, "validator-relationship")
rep(V, 'require(record["flowType"] in FLOWS,', 'require(record["flowType"] in ACCEPTED_FLOWS,', 1, "validator-loop")
rep(V, 'require(scope["flowType"] == "rule_flow", f"{scope_id} must use rule flow")',
    'require(scope["flowType"] in {"ControlFlow", "rule_flow"}, f"{scope_id} must use control flow")', 1, "validator-pilotScope")
rep(V, 'require(gate_input["flowType"] in FLOWS,', 'require(gate_input["flowType"] in ACCEPTED_FLOWS,', 1, "validator-wameGate")

# ── 3) schemas ×5 ──
ENUM_OLD = '"enum": ["material_flow", "information_flow", "capital_flow", "spacetime_flow", "energy_flow", "commerce_flow", "knowledge_flow", "rule_flow"]'
ENUM_NEW = '"enum": ["LogisticsFlow", "InformationFlow", "FinancialFlow", "EnergyFlow", "ServiceFlow", "ControlFlow", "ValueFlow", "CreditFlow", "material_flow", "information_flow", "capital_flow", "spacetime_flow", "energy_flow", "commerce_flow", "knowledge_flow", "rule_flow"]'
for name in ["was-event", "was-loop-record", "was-pool-link", "was-relationship", "was-wame-gate-input"]:
    rep(BASE / ("okf/schemas/%s.schema.json" % name), ENUM_OLD, ENUM_NEW, 1, "schema-" + name)

# ── 4) examples ──
GF = BASE / "okf/examples/gfis-runtime-sop-e2e-was-profile.yaml"
rep(GF, "  - spacetime_flow\n", "", 1, "gfis-requiredFlows-去spacetime")
rep(GF, "    flowType: spacetime_flow", "    flowType: LogisticsFlow", 1, "gfis-S11归位")
MAP = [("material_flow", "LogisticsFlow"), ("information_flow", "InformationFlow"),
       ("capital_flow", "FinancialFlow"), ("energy_flow", "EnergyFlow"),
       ("commerce_flow", "ServiceFlow"), ("knowledge_flow", "InformationFlow"),
       ("rule_flow", "ControlFlow")]
for f in ["valid-was-bundle.yaml", "synthetic-gate-ready.yaml",
          "gfis-runtime-sop-e2e-was-profile.yaml", "kds-real-candidate-bundle.yaml"]:
    p = BASE / ("okf/examples/%s" % f)
    t = p.read_text(encoding="utf-8")
    n = 0
    for old, new in MAP:
        c = t.count(old)
        if c:
            t = t.replace(old, new)
            n += c
    if n:
        if APPLY:
            p.write_text(t, encoding="utf-8")
        print("[%s] example %s：%d 处映射" % ("已改" if APPLY else "待改", f, n))

# ── 5) 引用键规范 ──
rep(BASE / "docs/WAS引用键与数据出口字段规范_v0.1.md",
    "| （旧名兼容）`was:material_flow` 等 OKF P0 命名 | 兼容迁移表（V1.2 §19）；新引用用 V1.2 名 | 兼容 |",
    "| （旧名兼容）`was:material_flow` 等 OKF P0 命名 | 《WAS-V1.2 术语迁移表》（docs/WAS-V1.2术语迁移表.md；V1.2 §19）；新引用用 V1.2 名 | 兼容（deprecated 窗口） |",
    1, "引用键规范")

# ── 6) 主方案记录 ──
MAIN = BASE / "docs/GlobalCloud-WAS总体方案V1.2-GPCF统一重构版.md"
rep(MAIN, "> **场景流扩展登记记录（2026-10-16，候选）**",
    "> **八流命名迁移执行记录（2026-10-16）**：按 §19/§21，WAS 仓 okf 基线（was-flows.yaml／schemas／validator／examples）已从 OKF P0 旧名切换至 V1.2 名；旧名进入兼容窗口（deprecated，见《WAS-V1.2 术语迁移表》docs/WAS-V1.2术语迁移表.md）。§19 要求的迁移表与兼容 validator 已建立。\n\n> **场景流扩展登记记录（2026-10-16，候选）**",
    1, "主方案-迁移执行记录")
rep(MAIN, "| 建立迁移表和兼容 validator |", "| 已建立（2026-10-16：《WAS-V1.2 术语迁移表》＋兼容 validator） |", 1, "主方案-§19表")

# ── 7) apply 后自检 ──
if APPLY:
    print("---- 自检：WAS 仓旧名残留 ----")
    r = subprocess.run(
        ["rg", "-n", "material_flow|information_flow|capital_flow|spacetime_flow|energy_flow|commerce_flow|knowledge_flow|rule_flow",
         ".", "-g", "!docs/WAS-V1.2术语迁移表.md", "-g", "!.git"],
        cwd=str(BASE), capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    for l in lines[:48]:
        print("  ", l[:160])
    print("  （共 %d 行）" % len(lines))
