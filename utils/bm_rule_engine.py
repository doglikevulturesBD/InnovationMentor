# utils/bm_rule_engine.py

import json
from typing import Dict, List


def load_weights(path: str = "config/business_model_weights.json") -> Dict:
    with open(path, "r") as f:
        return json.load(f)


def calculate_rule_scores(
    selected_features: List[str],
    weights: Dict[str, Dict[str, int]],
) -> Dict[str, float]:
    """
    selected_features: list of feature keys chosen via questionnaire
    weights: {model_name: {feature_key: weight, ...}}
    """
    scores = {model: 0.0 for model in weights.keys()}
    for model, feature_weights in weights.items():
        for feat in selected_features:
            if feat in feature_weights:
                scores[model] += feature_weights[feat]
    return scores

