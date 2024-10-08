from __future__ import annotations

from enum import Enum
from typing import Optional

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
    default_fields: DocumentInformations
    file: str
    fields: dict


class DocumentBatch(BaseModel):
    documents: conset(Document, min_length=1)  # type: ignore


class Collections:
    def __init__(self, result: dict) -> None:
        self.result = result

    def get_collection_names(self) -> list[str]:
        return [collection["name"] for collection in self.result]

    def get_collection(self, collection_name: str) -> dict:
        return [
            collection
            for collection in self.result
            if collection["name"] == collection_name
        ][0]

    def get_collection_fields(self, collection_name: str) -> list[dict]:
        return [
            collection["fields"]
            for collection in self.result
            if collection["name"] == collection_name
        ]


class DocumentResponse:
    def __init__(
        self,
        doc_id: int,
        embedding: list[float],
        start_page: int,
        end_page: int,
        text: str,
        page: int,
        file_id: str,
        kwargs,
    ):
        self.id = doc_id
        self.embedding = embedding
        self.start_page = start_page
        self.end_page = end_page
        self.text = text
        self.page = page
        self.file_id = file_id
        self.kwargs = kwargs

    def get_document_id(self) -> int:
        return self.id

    # implement other getters
    def get_embedding(self) -> list[float]:
        return self.embedding

    def get_start_line(self) -> int:
        return self.start_page

    def get_end_line(self) -> int:
        return self.end_page

    def get_text(self) -> str:
        return self.text

    def get_page(self) -> int:
        return self.page

    def get_file_id(self) -> str:
        return self.file_id

    def get_kwargs(self) -> dict:
        return self.kwargs


class SearchResponse:
    def __init__(self, result: dict) -> None:
        self.result = result

    def get_results(self) -> list[DocumentResponse]:
        return [
            DocumentResponse(
                doc_id=document["document"]["id"],
                embedding=document["document"]["embedding"],
                start_page=document["document"]["start_line"],
                end_page=document["document"]["end_line"],
                text=document["document"]["text"],
                page=document["document"]["page"],
                file_id=document["document"]["file_id"],
                kwargs={
                    k: v
                    for k, v in document["document"].items()
                    if k
                    not in {
                        "id",
                        "embedding",
                        "start_line",
                        "end_line",
                        "text",
                        "page",
                        "file_id",
                    }
                },
            )
            for document in self.result
        ]
