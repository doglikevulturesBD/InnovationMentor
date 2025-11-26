import numpy as np
import json
import os

# ----------------------------------------
# Load vectors for business models
# ----------------------------------------
def load_model_vectors(path="data/bm_model_vectors.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


# ----------------------------------------
# PURE NUMPY COSINE SIMILARITY
# ----------------------------------------
def cosine_sim(a, b):
    a = np.array(a)
    b = np.array(b)

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ----------------------------------------
# Compute AI boost using user embedding
# ----------------------------------------
def compute_ai_boost(user_vector, model_vectors):
    """
    user_vector: list[float]
    model_vectors: dict[BM_NAME → vector]
    """

    if user_vector is None or len(model_vectors) == 0:
        return {k: 0.0 for k in model_vectors.keys()}

    boosts = {}
    for bm, vec in model_vectors.items():
        boosts[bm] = cosine_sim(user_vector, vec)

    return boosts
