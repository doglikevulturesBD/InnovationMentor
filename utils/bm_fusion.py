def fuse_scores(rule_scores, ai_scores, rule_weight=0.7):
    """
    Combines rule-based + AI scores into hybrid.
    """
    final = {}

    for model_id in rule_scores:
        r = rule_scores.get(model_id, 0)
        a = ai_scores.get(model_id, 0)
        final[model_id] = r * rule_weight + a * (1 - rule_weight)

    return final


