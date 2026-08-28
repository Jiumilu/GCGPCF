from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/kds-sync/build_gcworld_identity_responsibility_verification.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("gcworld_identity_responsibility_verification", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GCWorldIdentityResponsibilityVerificationTest(unittest.TestCase):
    def test_missing_business_authority_remains_unresolved_and_unsent(self) -> None:
        builder = load_builder()
        packages = [
            {
                "复核包标识": "复核包-1",
                "复核包类型": "同名候选组",
                "优先级": "二级",
                "数据等级": "S2",
                "复核项数量": 2,
                "主复核责任角色建议": "动态路由至业务责任人",
                "主复核责任主体标识": None,
                "主复核接受状态": "待识别与接受",
                "第二复核角色": "F-013独立复核线程",
                "调度状态": "未发送",
                "SLA状态": "未启动",
                "允许当前包直接产生正式结果": False,
                "允许自动身份合并": False,
                "允许正式世界资产生成": False,
                "允许KDS写入": False,
                "允许事实提升": False,
                "允许权限授予": False,
            }
        ]

        receipts = builder.build_receipts(packages)

        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["责任主体核验状态"], "证据不足，保持未决")
        self.assertEqual(receipts[0]["交付状态"], "未发送")
        self.assertEqual(receipts[0]["F-013发起状态"], "未发起")
        self.assertEqual(receipts[0]["SLA状态"], "未启动")
        self.assertIsNone(receipts[0]["真实业务主复核责任主体标识"])

    def test_existing_formal_result_boundary_change_is_rejected(self) -> None:
        builder = load_builder()
        package = {
            "复核包标识": "复核包-1",
            "复核包类型": "多类型冲突",
            "优先级": "一级",
            "数据等级": "S2",
            "复核项数量": 1,
            "主复核责任角色建议": "动态路由至业务责任人",
            "主复核责任主体标识": None,
            "主复核接受状态": "待识别与接受",
            "第二复核角色": "F-013独立复核线程",
            "调度状态": "未发送",
            "SLA状态": "未启动",
            "允许当前包直接产生正式结果": True,
            "允许自动身份合并": False,
            "允许正式世界资产生成": False,
            "允许KDS写入": False,
            "允许事实提升": False,
            "允许权限授予": False,
        }

        with self.assertRaisesRegex(ValueError, "正式结果边界被改变"):
            builder.build_receipts([package])


if __name__ == "__main__":
    unittest.main()
