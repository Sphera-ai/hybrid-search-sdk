from __future__ import annotations

from enum import Enum
from typing import Union

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


class Preprocessing(BaseModel):
    chunk_mode: ChunkMod = ChunkMod.NAIVE
    chunk_size: int = 100
    overlap_size: int = 20
    mode: WordCharacter = WordCharacter.WORD
    semantic_chunk_model: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )


class DocumentInformations(BaseModel):
    field: str = "text"
    file_id: str


class Document(BaseModel):
    preprocessing: Preprocessing
    fields: DocumentInformations
    file: str | bytes


class DocumentBatch(BaseModel):
    documents: conset(Document, min_length=1)  # type: ignore
