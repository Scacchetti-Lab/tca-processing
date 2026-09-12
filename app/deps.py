from typing import Annotated
from fastapi import Depends
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from os import getenv

load_dotenv()
hf_token = getenv('HF_TOKEN')

model = SentenceTransformer(
    'sentence-transformers/all-MiniLM-L6-v2',
    token=hf_token 
)

def get_model() -> SentenceTransformer:
    if model is None:
        raise RuntimeError("Modelo ainda não carregado")
    return model

ModelDep = Annotated[SentenceTransformer, Depends(get_model)]