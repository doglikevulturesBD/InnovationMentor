import json

def load_rules(path="data/bm_rule_weights.json"):
    with open(path) as f:
        return json.load(f)


def normalize_rule_weights(rules):
    """
    Normalize model weights inside each answer so no question dominates.
    """
    normalized = {}

    for qid, answers in rules.items():
        normalized[qid] = {}

        for answer_key, detail in answers.items():
            models = detail.get("models", {})

            if not models:
                continue

            total = sum(abs(v) for v in models.values())
            if total == 0:
                total = 1.0

            normalized[qid][answer_key] = {
                bm: v / total for bm, v in models.items()
            }

    return normalized


def compute_rule_score(selected_answers, normalized_rules, question_importance=1.0):
    """
    Computes the deterministic (explainable) rules engine score.
    """
    # Initialize model scores
    all_models = set()
    for qid in normalized_rules:
        for answer_key in normalized_rules[qid]:
            all_models.update(normalized_rules[qid][answer_key].keys())

    scores = {bm: 0.0 for bm in all_models}

    # Apply scoring
    for qid, ans in selected_answers.items():
        if qid not in normalized_rules:
            continue
        if ans not in normalized_rules[qid]:
            continue

        for bm, w in normalized_rules[qid][ans].items():
            scores[bm] += w * question_importance

    return scores

