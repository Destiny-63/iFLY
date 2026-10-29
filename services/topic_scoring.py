"""
命题说话评测 - 时间惩罚与维度四计算

评分细则：缺时 1 分钟以内扣 1-3 分，缺时 1-2 分钟扣 4-6 分，缺时 2 分钟以上扣 7-10 分。
"""

REQUIRED_DURATION_SECONDS = 180  # 3 分钟


def compute_time_penalty(duration_seconds: float) -> dict:
    """
    计算时间惩罚（维度四）。

    规则：
    - 满 3 分钟：不扣分
    - 缺时 1 分钟内（2~3 分钟）：扣 1-3 分
    - 缺时 1-2 分钟（1~2 分钟）：扣 4-6 分
    - 缺时 2 分钟以上（不足 1 分钟）：扣 7-10 分

    Returns:
        dict: {"deduct": int, "reason": str, "shortfall_seconds": float}
    """
    shortfall = max(0, REQUIRED_DURATION_SECONDS - duration_seconds)

    if shortfall <= 0:
        return {
            "deduct": 0,
            "reason": "时长达标，未扣分",
            "shortfall_seconds": 0,
        }

    if shortfall <= 60:
        # 缺时 1 分钟内：扣 1-3 分，按比例
        deduct = max(1, min(3, round(shortfall / 20)))
        return {
            "deduct": deduct,
            "reason": f"缺时约 {int(shortfall)} 秒（2~3 分钟），扣 {deduct} 分",
            "shortfall_seconds": shortfall,
        }

    if shortfall <= 120:
        # 缺时 1-2 分钟：扣 4-6 分
        deduct = max(4, min(6, round(4 + (shortfall - 60) / 30)))
        return {
            "deduct": deduct,
            "reason": f"缺时约 {int(shortfall)} 秒（1~2 分钟），扣 {deduct} 分",
            "shortfall_seconds": shortfall,
        }

    # 缺时 2 分钟以上：扣 7-10 分
    deduct = max(7, min(10, round(7 + (shortfall - 120) / 40)))
    return {
        "deduct": min(10, deduct),
        "reason": f"缺时约 {int(shortfall)} 秒（不足 1 分钟），扣 {deduct} 分",
        "shortfall_seconds": shortfall,
    }
