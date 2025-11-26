import json
import numpy as np
from engine.rules_engine import score_rules
from engine.ai_engine import load_model_vectors, compute_ai_boost

# Load AI vectors once
MODEL_VECTORS = load_model_vectors()

def rank_business_models(selected_answers, user_vector=None):
    """
    selected_answers: dict of qID → {"tags":{}, "models":{}}
    user_vector: list[float] representing AI embedding (optional)
    """

    # 1. RULE-BASED SCORING
    rule_scores = score_rules(selected_answers)

    # 2. AI BOOST (OPTIONAL)
    if user_vector is not None and len(MODEL_VECTORS) > 0:
        ai_scores = compute_ai_boost(user_vector, MODEL_VECTORS)
    else:
        ai_scores = {bm: 0.0 for bm in rule_scores.keys()}

    # 3. COMBINE
    final_scores = {}
    for bm in rule_scores:
        final_scores[bm] = rule_scores[bm] + ai_scores.get(bm, 0)

    # Sort
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    # Return top 3 + full list
    return ranked[:3], ranked

