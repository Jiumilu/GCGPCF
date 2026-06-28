#!/usr/bin/env python3
"""Validate the GCKF distributed knowledge system control prompt coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROMPT = ROOT / "03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统完整实施提示词.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-KDS-DKS-PROMPT-REFRESH-20260628.md"

FUNCTION_DOMAINS = [
    "葛化 GFIS 知识问答助手",
    "葛化 GFIS 使用助手",
    "葛化 GFIS 文档验收助手",
    "AI 候选事实生成与写回候选机制",
    "候选事实驱动 SOP 建议机制",
    "葛化订单运行母版 / 预运营期订单",
    "辽宁远航链路补证与知识缺口悬赏",
    "现代精工 OEM 过渡责任拆分",
    "质量 / 发货 / POD / 金融凭证门禁",
    "湖北磷材拓厂项目知识库",
    "湖北磷材原料 / 行业 / 订单知识库",
    "新工厂复制模板",
    "知识积分、产值积分、潜在产值积分",
    "AI 额度自购、自用、共享、贡献、奖励计量",
    "统一收益池、知识收益、系统收益、业务收益",
    "知识缺口悬赏机制",
    "委员会 DecisionRecord 与争议处理机制",
    "底座 11 池挂接与增强治理账本",
    "RAG 安全准入分级",
    "KDS / WAES / GFIS / GPCF / WIKI / 小即 / 飞书协同边界",
]

CONTROL_TOKENS = [
    "real_business_lane=repair_required",
    "不得未经授权写真实 KDS API",
    "不得自动声明 accepted、complete、integrated、production_ready 或 customer_accepted",
    "AI 可以输出",
    "AI 不得直接输出为",
    "必须人工确认",
    "必须委员会确认",
    "合作单位自购 AI 额度先自用，不进入统一收益池",
    "到账进入正式收入和收益池；开票只作为统计和财务过程口径",
    "无实际收入只能计入知识贡献或潜在产值贡献，不能计入正式产值",
    "每个对象都必须至少挂接一个池",
    "safe：可安全调用",
    "limited：可有限引用",
    "repair_required：需要补证",
    "blocked：不得调用",
    "底座可用知识闭环率",
    "run -> stop -> verify -> recover -> debug",
    "最终控制权属于用户",
]

POOL_TOKENS = [
    "订单池",
    "运力池",
    "产能池",
    "资金池",
    "政策池",
    "装备池",
    "数据池",
    "能源池",
    "原料池",
    "人才池",
    "场景池",
]

FORBIDDEN_UPGRADE_TOKENS = [
    "accepted。",
    "complete。",
    "integrated。",
    "production_ready。",
    "customer_accepted。",
    "real_business_lane=repaired。",
    "formal_revenue_confirmed。",
    "formal_contribution_confirmed。",
    "bounty_settled。",
    "committee_decided。",
    "rag_strong_reference_approved。",
    "gfis_writeback_executed。",
    "waes_gate_passed。",
    "kds_api_synced。",
]

LOOP_TOKENS = ["### run", "### stop", "### verify", "### recover", "### debug"]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing_file:{path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(label: str, text: str, tokens: list[str], failures: list[str]) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        failures.append(f"missing_{label}:{','.join(missing)}")


def main() -> int:
    failures: list[str] = []
    prompt_text = read(PROMPT, failures)
    loop_text = read(LOOP, failures)

    require_tokens("function_domains", prompt_text, FUNCTION_DOMAINS, failures)
    require_tokens("control_tokens", prompt_text, CONTROL_TOKENS, failures)
    require_tokens("pool_tokens", prompt_text, POOL_TOKENS, failures)
    require_tokens("forbidden_upgrade_tokens", prompt_text, FORBIDDEN_UPGRADE_TOKENS, failures)
    require_tokens("loop_tokens", loop_text, LOOP_TOKENS, failures)

    if "本文件是主控实施提示词，不是业务完成证明" not in prompt_text:
        failures.append("missing_prompt_not_business_completion_boundary")
    if "不做真实业务写入" not in loop_text:
        failures.append("missing_loop_no_real_business_write_boundary")
    if "accepted_allowed=false" not in loop_text:
        failures.append("missing_loop_accepted_boundary")
    if "production_ready_allowed=false" not in loop_text:
        failures.append("missing_loop_production_boundary")

    result = {
        "gckf_prompt_control_coverage_20260628": "pass" if not failures else "fail",
        "function_domain_count": len(FUNCTION_DOMAINS),
        "control_token_count": len(CONTROL_TOKENS),
        "pool_token_count": len(POOL_TOKENS),
        "forbidden_upgrade_token_count": len(FORBIDDEN_UPGRADE_TOKENS),
        "loop_control_token_count": len(LOOP_TOKENS),
        "prompt": str(PROMPT.relative_to(ROOT)),
        "loop": str(LOOP.relative_to(ROOT)),
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
