from sentence_transformers import SentenceTransformer
import json
import numpy as np

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_embedding(text: str) -> str:
    vec = get_model().encode(text)
    return json.dumps(vec.tolist())

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    a, b = np.array(vec1), np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))