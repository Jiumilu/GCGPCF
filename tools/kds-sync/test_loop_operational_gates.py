#!/usr/bin/env python3
"""Regression tests for Loop operational gate signal filtering."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / ".codex/skills/globalcloud-loop-orchestrator/scripts/loop_operational_gates.py"


def load_module():
    spec = importlib.util.spec_from_file_location("loop_operational_gates", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class LoopOperationalGatesTest(unittest.TestCase):
    def test_source_record_monitor_hold_does_not_block_operational_gates(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = root / "docs/harness/evidence"
            harness.mkdir(parents=True)
            (root / ".harness").mkdir()
            (root / ".harness/README.md").write_text(
                "测试结果 pass\n验收矩阵 pass\ncustomer feedback collected\n",
                encoding="utf-8",
            )
            (harness / "was-real-source-record-monitor-021-20260621.md").write_text(
                "当前 `accepted_for_quality_profile=0`、`accepted_for_next_gate=0`、"
                "`hold_required=1`，质量检验证据不得替代 KDS source-of-record。\n",
                encoding="utf-8",
            )
            (harness / "was-real-source-record-monitor-041-20260622.md").write_text(
                "当前 `accepted_for_customer_after_sales_profile=0`、`accepted_for_next_gate=0`、"
                "`hold_required=1`，客户满意度反馈不得替代 KDS source-of-record。\n",
                encoding="utf-8",
            )
            (harness / "was-real-source-record-monitor-049-20260622.md").write_text(
                "客户投诉和返工处置只有补齐证据后才能绑定到下游 WAES/KDS/runtime 门禁中。\n"
                "| accepted_for_customer_change_capa_profile | `0` |\n"
                "| hold_required | `1` |\n"
                "本证据不创建 KDS 正式事实、WAES review、runtime primary key、review queue、"
                "runtime intake、verified artifact，也不形成 accepted、integrated 或 production ready 状态。\n",
                encoding="utf-8",
            )

            corpus = [(path, module.read_text(path)) for path in module.iter_markdown(root)]
            gates = {spec.name: module.evaluate_gate(spec, corpus, root) for spec in module.GATES}

        self.assertEqual(gates["quality"]["gate"], "pass")
        self.assertEqual(gates["customer_satisfaction"]["gate"], "pass")


if __name__ == "__main__":
    unittest.main()
