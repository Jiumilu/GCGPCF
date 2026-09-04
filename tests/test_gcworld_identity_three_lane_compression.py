from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/kds-sync/build_gcworld_identity_three_lane_compression.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("gcworld_identity_three_lane_compression", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def route(review_id: str, order: int, machine_owner: str | None) -> dict:
    return {
        "复核项标识": review_id,
        "输入排序序号": order,
        "数据等级": "S2",
        "显示名称": f"名称-{review_id}",
        "主体类型建议": "法人或市场主体候选",
        "机器归一与证据整理责任主体": machine_owner,
        "主复核责任路由": "动态路由",
        "SLA状态": "未启动",
        "身份决定": None,
        "自动合并": False,
        "正式世界资产标识": None,
        "KDS写入授权": False,
        "事实提升授权": False,
        "权限授予授权": False,
    }


def suggestion(review_id: str, order: int, refs: list[str]) -> dict:
    return {
        "复核项标识": review_id,
        "输入排序序号": order,
        "数据等级": "S2",
        "显示名称": f"名称-{review_id}",
        "主体类型建议": "法人或市场主体候选",
        "机器建议动作": "保持未决",
        "证据包建议": {
            "候选标识": refs,
            "来源证据标识": [f"来源-{x}" for x in refs],
            "关系证据标识": [f"关系-{x}" for x in refs],
            "建议核验锚点": ["企业登记记录"],
        },
        "例外代码": ["权威锚点未登记", "真实业务责任主体未验证"],
        "SLA状态": "未启动",
        "身份决定": None,
        "自动合并": False,
        "正式世界资产标识": None,
        "KDS写入授权": False,
        "事实提升授权": False,
        "权限授予授权": False,
    }


class GCWorldIdentityThreeLaneCompressionTest(unittest.TestCase):
    def test_partition_is_disjoint_and_exhaustive(self) -> None:
        builder = load_builder()
        routes = [route("一", 1, "GKE-001"), route("二", 2, "GKE-001"), route("三", 3, "GKE-001"), route("四", 4, None)]
        suggestions = [suggestion("一", 1, ["甲"]), suggestion("二", 2, ["乙"]), suggestion("三", 3, ["丙"])]
        priority = [{"复核包标识": "包-一", "复核项": [{"复核项标识": "二"}]}]

        partition, compressed = builder.build_outputs(routes, suggestions, priority)

        self.assertEqual(len(partition), 4)
        self.assertEqual(len(compressed), 2)
        self.assertEqual(
            {row["复核项标识"]: row["处理车道"] for row in partition},
            {"一": "机器证据压缩车道", "二": "优先人工例外车道", "三": "机器证据压缩车道", "四": "直接业务责任车道"},
        )

    def test_evidence_digest_is_order_independent(self) -> None:
        builder = load_builder()
        routes = [route("一", 1, "GKE-001")]
        first = [suggestion("一", 1, ["甲", "乙"])]
        second = [suggestion("一", 1, ["乙", "甲"])]

        _, first_compressed = builder.build_outputs(routes, first, [])
        _, second_compressed = builder.build_outputs(routes, second, [])

        self.assertEqual(first_compressed[0]["候选证据摘要"], second_compressed[0]["候选证据摘要"])
        self.assertEqual(first_compressed[0]["来源证据摘要"], second_compressed[0]["来源证据摘要"])
        self.assertEqual(first_compressed[0]["关系证据摘要"], second_compressed[0]["关系证据摘要"])

    def test_formal_result_boundary_change_is_rejected(self) -> None:
        builder = load_builder()
        row = route("一", 1, "GKE-001")
        row["自动合并"] = True

        with self.assertRaisesRegex(ValueError, "未决边界被改变"):
            builder.build_outputs([row], [suggestion("一", 1, ["甲"])], [])


if __name__ == "__main__":
    unittest.main()
