from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/kds-sync/build_gcworld_identity_priority_human_review_packages.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("gcworld_identity_priority_human_review_packages", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def suggestion(review_id: str, order: int, name: str, group_id: str, group_size: int, codes: list[str]) -> dict:
    return {
        "复核项标识": review_id,
        "输入排序序号": order,
        "数据等级": "S2",
        "显示名称": name,
        "同名候选组标识": group_id,
        "同名候选组数量": group_size,
        "主体类型建议": "其他组织候选，需人工确认",
        "机器建议状态": "候选建议已生成，禁止自动决定",
        "机器建议动作": "保持未决",
        "证据包建议": {
            "候选标识": [f"候选-{review_id}"],
            "来源证据标识": [f"来源-{review_id}"],
            "关系证据标识": [f"关系-{review_id}"],
            "建议核验锚点": ["权威登记记录"],
        },
        "主复核责任路由建议": "动态路由至相应业务责任人",
        "第二复核": "F-013独立复核线程",
        "例外代码": codes,
        "SLA状态": "未启动",
        "身份决定": None,
        "自动合并": False,
        "正式世界资产标识": None,
        "KDS写入授权": False,
        "事实提升授权": False,
        "权限授予授权": False,
    }


class GCWorldIdentityPriorityHumanReviewPackagesTest(unittest.TestCase):
    def test_builds_independent_conflict_and_same_name_packages(self) -> None:
        builder = load_builder()
        rows = [
            suggestion("复核-1", 1, "甲组织", "组-甲", 1, ["权威锚点未登记", "多类型冲突"]),
            suggestion("复核-2", 2, "乙 团队", "组-乙", 2, ["权威锚点未登记", "同名候选需独立复核"]),
            suggestion("复核-3", 3, "乙团队", "组-乙", 2, ["权威锚点未登记", "同名候选需独立复核"]),
            suggestion("复核-4", 4, "普通候选", "组-普通", 1, ["权威锚点未登记"]),
        ]

        packages = builder.build_packages(rows)

        self.assertEqual(len(packages), 2)
        self.assertEqual([item["复核包类型"] for item in packages], ["多类型冲突", "同名候选组"])
        self.assertEqual([item["复核项数量"] for item in packages], [1, 2])
        self.assertEqual(
            {row["复核项标识"] for package in packages for row in package["复核项"]},
            {"复核-1", "复核-2", "复核-3"},
        )
        self.assertTrue(all(package["主复核责任主体标识"] is None for package in packages))
        self.assertTrue(all(package["SLA状态"] == "未启动" for package in packages))
        self.assertTrue(all(package["允许当前包直接产生正式结果"] is False for package in packages))

    def test_same_name_group_size_mismatch_is_rejected(self) -> None:
        builder = load_builder()
        rows = [
            suggestion("复核-1", 1, "甲团队", "组-甲", 3, ["同名候选需独立复核"]),
            suggestion("复核-2", 2, "甲 团队", "组-甲", 3, ["同名候选需独立复核"]),
        ]

        with self.assertRaisesRegex(ValueError, "同名候选组数量不一致"):
            builder.build_packages(rows)

    def test_decided_or_write_enabled_item_is_rejected(self) -> None:
        builder = load_builder()
        row = suggestion("复核-1", 1, "甲组织", "组-甲", 1, ["多类型冲突"])
        row["身份决定"] = "合并"

        with self.assertRaisesRegex(ValueError, "未决边界被改变"):
            builder.build_packages([row])


if __name__ == "__main__":
    unittest.main()
