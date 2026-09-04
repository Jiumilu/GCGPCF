from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/kds-sync/build_gcworld_identity_high_priority_anchor_packages.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("gcworld_identity_high_priority_anchor_packages", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def priority_row(review_id: str, order: int, subject_type: str, priority: str = "高") -> dict:
    return {
        "复核项标识": review_id,
        "输入排序序号": order,
        "全局处理序号": order,
        "等级内处理序号": order,
        "数据等级": "S2",
        "显示名称": f"名称-{review_id}",
        "主体类型建议": subject_type,
        "处理优先级": priority,
        "处理评分": 4,
        "候选证据数量": 40,
        "候选证据摘要": "a" * 64,
        "来源证据数量": 40,
        "来源证据摘要": "b" * 64,
        "关系证据数量": 40,
        "关系证据摘要": "c" * 64,
        "最大证据数量": 40,
        "SLA状态": "未启动",
        "身份决定": None,
        "自动合并": False,
        "正式世界资产标识": None,
        "KDS写入授权": False,
        "事实提升授权": False,
        "权限授予授权": False,
    }


class GCWorldIdentityHighPriorityAnchorPackagesTest(unittest.TestCase):
    def test_four_queues_are_exhaustive_and_disjoint(self) -> None:
        builder = load_builder()
        rows = [
            priority_row("政一", 1, "政府或公共机构候选"),
            priority_row("人一", 2, "自然人候选"),
            priority_row("法一", 3, "法人或市场主体候选"),
            priority_row("组一", 4, "其他组织候选，需人工确认"),
            priority_row("中一", 5, "自然人候选", "中"),
        ]

        packages = builder.build_packages(rows, batch_size=20)
        items = [item for package in packages for item in package["复核项"]]

        self.assertEqual({item["复核项标识"] for item in items}, {"政一", "人一", "法一", "组一"})
        self.assertEqual(len(items), len({item["复核项标识"] for item in items}))
        self.assertEqual({package["责任路由队列"] for package in packages}, set(builder.TYPE_CONFIG[type_name]["队列"] for type_name in builder.TYPE_CONFIG))

    def test_packages_respect_batch_size_and_stable_order(self) -> None:
        builder = load_builder()
        rows = [priority_row(f"法{index}", index, "法人或市场主体候选") for index in range(1, 6)]

        packages = builder.build_packages(list(reversed(rows)), batch_size=2)

        self.assertEqual([len(package["复核项"]) for package in packages], [2, 2, 1])
        self.assertEqual(
            [item["复核项标识"] for package in packages for item in package["复核项"]],
            ["法1", "法2", "法3", "法4", "法5"],
        )

    def test_anchor_request_keeps_formal_boundaries_closed(self) -> None:
        builder = load_builder()
        package = builder.build_packages([priority_row("人一", 1, "自然人候选")])[0]
        item = package["复核项"][0]

        self.assertEqual(package["SLA状态"], "未启动")
        self.assertIsNone(item["身份决定"])
        self.assertIsNone(item["正式世界资产标识"])
        self.assertFalse(item["自动合并"])
        self.assertFalse(item["KDS写入授权"])
        self.assertFalse(item["事实提升授权"])
        self.assertFalse(item["权限授予授权"])

    def test_changed_formal_boundary_is_rejected(self) -> None:
        builder = load_builder()
        row = priority_row("人一", 1, "自然人候选")
        row["自动合并"] = True

        with self.assertRaisesRegex(ValueError, "未决边界被改变"):
            builder.build_packages([row])


if __name__ == "__main__":
    unittest.main()
