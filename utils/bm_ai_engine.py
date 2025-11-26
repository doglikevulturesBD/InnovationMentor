import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

def load_model_vectors(path="data/bm_model_vectors.json"):
    with open(path) as f:
        return json.load(f)


def compute_ai_boost(tag_vectors, model_vectors, boost_strength=0.2):
    """
    Compute the soft AI boost based on user tag embeddings.
    tag_vectors = list of embedded vectors (numpy arrays)
    """
    if not tag_vectors:
        return {bm: 0.0 for bm in model_vectors.keys()}

    user_vec = np.mean(np.array(tag_vectors), axis=0).reshape(1, -1)

    boosts = {}
    for bm, vec in model_vectors.items():
        model_vec = np.array(vec).reshape(1, -1)
        sim = cosine_similarity(user_vec, model_vec)[0][0]
        boosts[bm] = sim * boost_strength

    return boosts
