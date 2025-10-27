from sentence_transformers import SentenceTransformer
from .config import settings

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBED_MODEL)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return model.encode(texts, show_progress_bar=False, convert_to_numpy=True).tolist()
