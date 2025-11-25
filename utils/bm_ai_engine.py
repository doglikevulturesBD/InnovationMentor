# utils/bm_ai_engine.py

import json
from typing import Dict, List

import numpy as np

# If you use OpenAI in your environment, you can uncomment and configure this.
# from openai import OpenAI
# client = OpenAI()


def load_model_vectors(path: str = "data/bm_model_vectors.json") -> Dict[str, List[float]]:
    """
    Load precomputed embeddings for each business model.
    Expecting: { "ModelName": [embedding_values...] }
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback: no vectors yet
        return {}


def embed_text(text: str) -> np.ndarray | None:
    """
    Stub for embedding text.
    Replace with real OpenAI embeddings when you are ready.
    """
    text = (text or "").strip()
    if not text:
        return None

    # Example (commented out):
    # resp = client.embeddings.create(
    #     model="text-embedding-3-large",
    #     input=text,
    # )
    # return np.array(resp.data[0].embedding)

    # Temporary dummy behaviour: return None so AI scores = 0
    return None


def ai_scores_for_models(full_text: str, model_names: List[str]) -> Dict[str, float]:
    """
    Compute AI-based similarity scores for each model.
    If embeddings are not set up yet, returns 0 for all models,
    so the hybrid falls back to rule-based only.
    """
    vec = embed_text(full_text)
    vectors = load_model_vectors()

    # If we have no vector or no model vectors, return zeros
    if vec is None or not vectors:
        return {m: 0.0 for m in model_names}

    scores: Dict[str, float] = {}
    for model in model_names:
        mvec_list = vectors.get(model)
        if not mvec_list:
            scores[model] = 0.0
            continue
        mvec = np.array(mvec_list)
        sim = float(np.dot(vec, mvec) / (np.linalg.norm(vec) * np.linalg.norm(mvec)))
        scores[model] = sim

    # Normalise to 0–100
    vals = list(scores.values())
    vmin, vmax = min(vals), max(vals)
    if vmax == vmin:
        return {m: 0.0 for m in model_names}

    norm_scores = {
        m: 100.0 * (s - vmin) / (vmax - vmin)
        for m, s in scores.items()
    }
    return norm_scores

