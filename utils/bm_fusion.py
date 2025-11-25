# utils/bm_fusion.py

from typing import Dict


def fuse_scores(
    rule_scores: Dict[str, float],
    ai_scores: Dict[str, float],
    rule_weight: float = 0.7,
) -> Dict[str, float]:
    """
    Hybrid score = rule_weight * rule_score + (1 - rule_weight) * ai_score
    """
    final: Dict[str, float] = {}
    models = set(rule_scores.keys()) | set(ai_scores.keys())
    ai_weight = 1.0 - rule_weight

    for m in models:
        r = rule_scores.get(m, 0.0)
        a = ai_scores.get(m, 0.0)
        final[m] = rule_weight * r + ai_weight * a

    return final

