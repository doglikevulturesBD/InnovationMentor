from engine.rules_engine import load_rules, normalize_rule_weights, compute_rule_score
from engine.ai_engine import load_model_vectors, compute_ai_boost
import json

# Load configs
with open("config/scoring_config.json") as f:
    cfg = json.load(f)

RULES = load_rules()
NORM_RULES = normalize_rule_weights(RULES)
MODEL_VECTORS = load_model_vectors()

def rank_business_models(selected_answers, tag_vectors):
    rule_scores = compute_rule_score(
        selected_answers,
        normalized_rules=NORM_RULES,
        question_importance=cfg["question_importance_default"]
    )

    ai_scores = compute_ai_boost(
        tag_vectors,
        model_vectors=MODEL_VECTORS,
        boost_strength=cfg["ai_boost_strength"]
    )

    # Combine
    final_scores = {}
    for bm in rule_scores:
        final_scores[bm] = rule_scores[bm] + ai_scores.get(bm, 0.0)

    # Sort
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    return ranked[:3], ranked

