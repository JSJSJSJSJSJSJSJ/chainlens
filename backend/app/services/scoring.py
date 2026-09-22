"""Deterministic rule v1.0.0; confidence is neither materiality nor probability."""

from datetime import date, datetime

RULE_VERSION = "1.0.0"


def independent_count(evidence: list[dict]) -> int:
    """A repeated origin OR identical excerpt connects documents into one source group."""
    groups: list[set[str]] = []
    for item in evidence:
        group = {"origin:" + item["independence_key"], "hash:" + item["content_sha256"]}
        remaining = []
        for existing in groups:
            if existing & group:
                group |= existing
            else:
                remaining.append(existing)
        # A bridge may have joined groups visited earlier. Iterate to a fixed point.
        while any(existing & group for existing in remaining):
            next_remaining = []
            for existing in remaining:
                if existing & group:
                    group |= existing
                else:
                    next_remaining.append(existing)
            remaining = next_remaining
        groups = remaining + [group]
    return len(groups)


def calculate_score(
    relationship: dict, evidence: list[dict], cutoff: date, calculated_at: datetime | str
) -> dict:
    supporting = [item for item in evidence if item["stance"] == "supports"]
    contradicting = [item for item in evidence if item["stance"] == "contradicts"]
    direct = any(item["directness"] == "direct" for item in supporting)
    components = []

    def add(key: str, label: str, points: int, maximum: int, reason: str):
        components.append(
            {"key": key, "label": label, "points": points, "max_points": maximum, "reason": reason}
        )

    add(
        "directness",
        "结论直接性",
        30 if direct else 12 if supporting else 0,
        30,
        "存在直接支持此结论的证据" if direct else "只有间接支持" if supporting else "尚无支持证据",
    )
    authority = max(
        (
            {"regulatory": 25, "company": 22, "media": 12}[item["source_type"]]
            for item in supporting
        ),
        default=0,
    )
    add(
        "authority",
        "来源可信度",
        authority,
        25,
        "支持来源取最高等级：监管25、公司22、媒体12；来源等级不能消除利益冲突",
    )
    count = independent_count(supporting)
    add(
        "independence",
        "独立来源",
        min(count, 2) * 5,
        10,
        f"{count} 个独立支持来源；同一来源标识或相同摘录合并，转载不累加",
    )
    known_event = bool(relationship["valid_from"] or relationship["valid_to"])
    published_dates = [
        date.fromisoformat(item["published_at"])
        if isinstance(item["published_at"], str)
        else item["published_at"]
        for item in supporting
        if item["published_at"]
    ]
    dated = bool(published_dates)
    age = (cutoff - max(published_dates)).days if dated else None
    historical = relationship["temporal_status"] == "historical"
    freshness = 10 if age is not None and age <= 365 else 7 if age is not None and age <= 730 else 3
    time_points = (
        (10 if known_event else 5)
        if historical and dated
        else (max(0, freshness - (0 if known_event else 5)) if dated else 0)
    )
    add(
        "time",
        "时间明确度",
        time_points,
        10,
        (
            "历史事实：有事件边界10分，仅发布日期5分；历史不因年久扣分"
            if historical and dated
            else f"最新支持证据距研究截止日{age}天；365日内10分、730日内7分、更早3分；无事件边界减5分"
            if dated
            else "支持证据发布日期未知，时间项0分"
        ),
    )
    identity_points = {"exact": 10, "mapped": 6, "uncertain": 0}[relationship["entity_resolution"]]
    add(
        "identity",
        "实体身份",
        identity_points,
        10,
        {
            "exact": "来源直接对应上市主体",
            "mapped": "通过母子公司或品牌映射，需复核映射说明",
            "uncertain": "上市主体归属仍有歧义",
        }[relationship["entity_resolution"]],
    )
    semantics = (
        15 if relationship["fact_status"] == "confirmed" and direct else 7 if supporting else 0
    )
    if relationship["relationship_type"] == "peer" and not relationship["comparison_dimension"]:
        semantics = 0
    add(
        "semantics",
        "关系判定",
        semantics,
        15,
        "直接证据与已确认结论一致；peer 必须具有比较维度"
        if semantics == 15
        else "仍为推断或证据不足；共现、产品使用与直接采购不可等同",
    )
    conflicts = independent_count(contradicting)
    add(
        "conflict",
        "来源冲突",
        -min(conflicts * 30, 60),
        0,
        f"{conflicts} 个独立反方来源，每个扣30分，最多扣60分；仍保留全部冲突证据",
    )
    add(
        "quantitative",
        "量化信息",
        0,
        0,
        "金额或规模仅解释业务范围，不计入关系置信度；缺少金额不扣分",
    )
    subtotal = sum(component["points"] for component in components)
    cap = {"confirmed": 100, "inferred": 69, "unknown": 39}[relationship["fact_status"]]
    total = max(0, min(cap, subtotal))
    add(
        "status_cap",
        "状态上限与边界",
        total - subtotal,
        0,
        f"{relationship['fact_status']} 状态上限为{cap}，最终分限制在0—100",
    )
    valid_to = relationship["valid_to"]
    if isinstance(valid_to, str):
        valid_to = date.fromisoformat(valid_to)
    if relationship["temporal_status"] == "historical" or (valid_to and valid_to < cutoff):
        validity = "historical_only"
    elif (
        relationship["temporal_status"] == "current"
        and relationship["valid_from"]
        and direct
        and not conflicts
        and relationship["fact_status"] == "confirmed"
    ):
        # Current validity requires a recent corroborating observation; it is separate from score.
        dates = [
            date.fromisoformat(item["published_at"])
            if isinstance(item["published_at"], str)
            else item["published_at"]
            for item in supporting
            if item["published_at"]
        ]
        validity = "supported" if dates and (cutoff - max(dates)).days <= 730 else "unestablished"
    else:
        validity = "unestablished"
    timestamp = calculated_at.isoformat() if isinstance(calculated_at, datetime) else calculated_at
    return {
        "total": total,
        "rule_version": RULE_VERSION,
        "calculated_at": timestamp,
        "components": components,
        "current_validity": validity,
        "explanation": "确定性规则描述证据对具体结论的支持强度，不代表概率、业务重要性或投资价值。"
        "历史事实可信度与截至研究日的持续性分别判断；当前持续性要求明确起点、"
        "current 标注、730日内直接支持且无冲突。所有条目待用户人工复核。",
    }
