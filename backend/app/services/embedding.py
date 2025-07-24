from typing import TYPE_CHECKING

try:  # runtime optional import
    from sentence_transformers import SentenceTransformer as _ST
except Exception:  # pragma: no cover
    _ST = None

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer
else:  # pragma: no cover
    SentenceTransformer = object if _ST is None else _ST  # type: ignore

model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global model
    if model is None:
        if _ST is None:
            raise RuntimeError("sentence-transformers not installed")
        model = _ST("all-mpnet-base-v2")
    return model


def embed(text: str) -> list[float]:
    return get_model().encode(text).tolist()
