import json

def load_weights(path):
    with open(path, "r") as f:
        return json.load(f)


def calculate_rule_scores(features, weights):
    """
    features: list of selected feature codes e.g. ["customer_businesses"]
    weights: dict mapping q_id → option → {tags, models}
    """
    model_scores = {}

    for feature in features:
        for qid, options in weights.items():
            if feature in options:
                entry = options[feature]

                for model_id, val in entry.get("models", {}).items():
                    model_scores[model_id] = model_scores.get(model_id, 0) + val

    return model_scores


