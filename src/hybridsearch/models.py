from enum import Enum
from typing import List

from pydantic import BaseModel, Field, validator


class ChunkMod(str, Enum):
    NAIVE = "naive"
    SEMANTIC = "semantic"

    class Config:
        use_enum_values = True


class WordCharcter(BaseModel):
    word: str
    character: str

    class Config:
        use_enum_values = True


class Document(BaseModel):
    field: str
    chunk_mode: ChunkMod
    chunk_size: int
    overlap_size: int
    mode: str
    model_to_semantic_chunk: str # sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    urls: List[str]
