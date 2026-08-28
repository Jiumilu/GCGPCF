from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/kds-sync/build_gcworld_identity_machine_suggestions.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("gcworld_identity_machine_suggestions", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def high_frequency(review_id: str, order: int, name: str) -> dict:
    return {
        "人工复核状态": "待复核",
        "候选数量": 1,
        "候选标识": [f"候选-{review_id}"],
        "候选类型": "组织",
        "关系证据数量": 1,
        "关系证据标识": [f"关系-{review_id}"],
        "复核项标识": review_id,
        "排序序号": order,
        "数据等级": "S2",
        "显示名称": name,
        "权威锚点状态": "未验证",
        "来源证据数量": 1,
        "来源证据标识": [f"来源-{review_id}"],
        "正式世界资产标识": None,
        "自动合并": False,
    }


def type_suggestion(review_id: str, order: int, name: str, subject_type: str) -> dict:
    return {
        "主体类型建议": subject_type,
        "复核项标识": review_id,
        "建议核验锚点": ["权威登记记录", "业务责任人确认"],
        "数据等级": "S2",
        "显示名称": name,
        "权威锚点状态": "当前受控输入未登记，不代表现实中不存在",
        "权威锚点结构化字段已登记": False,
        "自动合并": False,
        "输入排序序号": order,
    }


def route(review_id: str, order: int, name: str, owner: str | None = "GKE-001") -> dict:
    return {
        "KDS写入授权": False,
        "SLA状态": "未启动",
        "临时路由模型状态": "人工已批准",
        "主复核责任路由": "动态路由至相应业务责任人",
        "事实提升授权": False,
        "复核项标识": review_id,
        "数据等级": "S2",
        "显示名称": name,
        "机器归一与证据整理责任主体": owner,
        "权限授予授权": False,
        "正式世界资产标识": None,
        "独立第二复核角色": "F-013独立复核线程",
        "真实业务责任主体接受状态": "待识别与接受",
        "真实业务责任主体标识": None,
        "自动合并": False,
        "身份决定": None,
        "输入排序序号": order,
    }


class GCWorldIdentityMachineSuggestionsTest(unittest.TestCase):
    def test_same_normalized_name_remains_two_unresolved_review_items(self) -> None:
        builder = load_builder()
        high = [high_frequency("复核-2", 2, "甲 团队"), high_frequency("复核-1", 1, "甲团队")]
        types = [
            type_suggestion("复核-2", 2, "甲 团队", "其他组织候选，需人工确认"),
            type_suggestion("复核-1", 1, "甲团队", "其他组织候选，需人工确认"),
        ]
        routes = [route("复核-2", 2, "甲 团队"), route("复核-1", 1, "甲团队")]

        suggestions, exceptions = builder.build_suggestions(high, types, routes)

        self.assertEqual([item["复核项标识"] for item in suggestions], ["复核-1", "复核-2"])
        self.assertEqual(len({item["复核项标识"] for item in suggestions}), 2)
        self.assertEqual(len({item["同名候选组标识"] for item in suggestions}), 1)
        self.assertTrue(all(item["身份决定"] is None for item in suggestions))
        self.assertTrue(all(item["正式世界资产标识"] is None for item in suggestions))
        self.assertTrue(all(item["自动合并"] is False for item in suggestions))
        self.assertTrue(all("同名候选需独立复核" in item["例外代码"] for item in exceptions))

    def test_direct_business_route_is_excluded(self) -> None:
        builder = load_builder()
        high = [high_frequency("复核-1", 1, "甲项目组")]
        types = [type_suggestion("复核-1", 1, "甲项目组", "项目组织候选")]
        routes = [route("复核-1", 1, "甲项目组", owner=None)]

        suggestions, exceptions = builder.build_suggestions(high, types, routes)

        self.assertEqual(suggestions, [])
        self.assertEqual(exceptions, [])

    def test_evidence_count_mismatch_is_rejected(self) -> None:
        builder = load_builder()
        high = high_frequency("复核-1", 1, "甲公司")
        high["来源证据数量"] = 2

        with self.assertRaisesRegex(ValueError, "证据计数不一致"):
            builder.build_suggestions(
                [high],
                [type_suggestion("复核-1", 1, "甲公司", "法人或市场主体候选")],
                [route("复核-1", 1, "甲公司")],
            )


if __name__ == "__main__":
    unittest.main()
