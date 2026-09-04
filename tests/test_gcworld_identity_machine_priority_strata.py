from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/kds-sync/build_gcworld_identity_machine_priority_strata.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("gcworld_identity_machine_priority_strata", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compressed_row(review_id: str, order: int, subject_type: str, candidate_count: int, relation_count: int) -> dict:
    return {
        "复核项标识": review_id,
        "输入排序序号": order,
        "数据等级": "S2",
        "显示名称": f"名称-{review_id}",
        "主体类型建议": subject_type,
        "候选证据数量": candidate_count,
        "候选证据摘要": "a" * 64,
        "来源证据数量": candidate_count,
        "来源证据摘要": "b" * 64,
        "关系证据数量": relation_count,
        "关系证据摘要": "c" * 64,
        "压缩状态": "机器证据摘要已生成，身份仍未决",
        "SLA状态": "未启动",
        "身份决定": None,
        "自动合并": False,
        "正式世界资产标识": None,
        "KDS写入授权": False,
        "事实提升授权": False,
        "权限授予授权": False,
    }


class GCWorldIdentityMachinePriorityStrataTest(unittest.TestCase):
    def test_thresholds_and_tiers_are_explainable(self) -> None:
        builder = load_builder()
        rows = [
            compressed_row("高", 1, "政府或公共机构候选", 90, 90),
            compressed_row("中", 2, "自然人候选", 10, 10),
            compressed_row("低", 3, "其他组织候选，需人工确认", 10, 10),
        ]

        result = builder.build_priority_rows(rows)
        by_id = {row["复核项标识"]: row for row in result}

        self.assertEqual(by_id["高"]["处理优先级"], "高")
        self.assertEqual(by_id["高"]["证据规模分"], 3)
        self.assertEqual(by_id["高"]["主体治理敏感度分"], 3)
        self.assertEqual(by_id["中"]["处理优先级"], "中")
        self.assertEqual(by_id["低"]["处理优先级"], "低")

    def test_equal_inputs_receive_equal_tiers(self) -> None:
        builder = load_builder()
        rows = [
            compressed_row("甲", 2, "法人或市场主体候选", 36, 36),
            compressed_row("乙", 1, "法人或市场主体候选", 36, 36),
        ]

        result = builder.build_priority_rows(rows)

        self.assertEqual(result[0]["处理优先级"], result[1]["处理优先级"])
        self.assertEqual(result[0]["处理评分"], result[1]["处理评分"])

    def test_priority_does_not_change_identity_or_authorization_boundaries(self) -> None:
        builder = load_builder()
        result = builder.build_priority_rows(
            [compressed_row("一", 1, "自然人候选", 18, 18)]
        )[0]

        self.assertIsNone(result["身份决定"])
        self.assertIsNone(result["正式世界资产标识"])
        self.assertFalse(result["自动合并"])
        self.assertFalse(result["KDS写入授权"])
        self.assertFalse(result["事实提升授权"])
        self.assertFalse(result["权限授予授权"])
        self.assertEqual(result["SLA状态"], "未启动")

    def test_changed_formal_boundary_is_rejected(self) -> None:
        builder = load_builder()
        row = compressed_row("一", 1, "自然人候选", 18, 18)
        row["KDS写入授权"] = True

        with self.assertRaisesRegex(ValueError, "未决边界被改变"):
            builder.build_priority_rows([row])


if __name__ == "__main__":
    unittest.main()
