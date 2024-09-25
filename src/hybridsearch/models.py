from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, conset


class ChunkMod(str, Enum):
    NAIVE = "naive"
    SEMANTIC = "semantic"

    class Config:
        use_enum_values = True


class WordCharacter(str, Enum):
    WORD = "words"
    CHARACTER = "characters"

    class Config:
        use_enum_values = True


class Document(BaseModel):
    field: str = "tetxt"
    chunk_mode: ChunkMod = ChunkMod.NAIVE
    chunk_size: int = 100
    overlap_size: int = 20
    mode: WordCharacter = WordCharacter.WORD
    model_to_semantic_chunk: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    urls: conset(str, min_length=1)  # type: ignore
