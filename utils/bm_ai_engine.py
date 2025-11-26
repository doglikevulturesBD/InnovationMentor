# utils/bm_ai_engine.py

import json
import numpy as np
from typing import Dict, List

from openai import OpenAI
client = OpenAI()


# -------------------------------------------------------------
# 1. Load Model Embeddings
# -------------------------------------------------------------
def load_model_vectors(path: str = "data/bm_model_vectors.json") -> Dict[str, List[float]]:
    """
    Load precomputed embeddings for each business model.
    Expecting: { "BM01": [values...], "BM02": [...] }
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


# -------------------------------------------------------------
# 2. Embed User Text
# -------------------------------------------------------------
def embed_text(text: str) -> np.ndarray | None:
    """
    Converts free-text input into an embedding vector.
    Must match the SAME embedding model used to generate bm_model_vectors.json.
    """

    text = (text or "").strip()
    if not text:
        return None

    # IMPORTANT:
    # If your bm_model_vectors.json was generated with "text-embedding-3-large",
    # the embedder must match exactly:
    try:
        resp = client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
        )
        return np.array(resp.data[0].embedding)

    except Exception as e:
        print("Embedding error:", e)
        return None


# -------------------------------------------------------------
# 3. Compute AI Similarity Scores
# -------------------------------------------------------------
def ai_scores_for_models(full_text: str, model_names: List[str]) -> Dict[str, float]:
    """
    Returns AI similarity scores (0–100) between user description
    and each business model embedding.
    If any piece is missing, returns all zeros (safe fallback).
    """

    vec = embed_text(full_text)
    vectors = load_model_vectors()

    # If no embeddings available, fallback
    if vec is None or not vectors:
        return {m: 0.0 for m in model_names}

    scores = {}

    for model in model_names:
        mvec_list = vectors.get(model)

        if not mvec_list:
            scores[model] = 0.0
            continue

        mvec = np.array(mvec_list)

        # Cosine similarity
        sim = float(np.dot(vec, mvec) / (np.linalg.norm(vec) * np.linalg.norm(mvec)))
        scores[model] = sim

    # -------------------------------
    # Normalise cosine values to 0–100
    # -------------------------------
    vals = list(scores.values())
    vmin, vmax = min(vals), max(vals)

    if vmax == vmin:
        # avoid divide-by-zero
        return {m: 0.0 for m in model_names}

    norm_scores = {
        m: 100.0 * (s - vmin) / (vmax - vmin)
        for m, s in scores.items()
    }

    return norm_scores


