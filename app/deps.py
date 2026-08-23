from typing import Annotated
from fastapi import Depends
from sentence_transformers import SentenceTransformer

model: SentenceTransformer | None = None

def get_model() -> SentenceTransformer:
    if model is None:
        raise RuntimeError("Modelo ainda não carregado")
    return model

ModelDep = Annotated[SentenceTransformer, Depends(get_model)]