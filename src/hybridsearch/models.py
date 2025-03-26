from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, conset


class ChunkMod(str, Enum):
    NAIVE = "naive"
    SEMANTIC = "semantic"

    class Config:
        use_enum_values = True


class EmbeddingModel(Enum):
    """
    Insert the path of the model in the enum
    """

    ALL_MINILM_L12_V2 = "ts/all-MiniLM-L12-v2"
    E5_SMALL = "ts/e5-small"
    E5_SMALL_V2 = "ts/e5-small-v2"
    E5_LARGE = "ts/e5-large"
    E5_LARGE_V2 = "ts/e5-large-v2"
    DISTILUSE_BASE_MULTILINGUAL_CASED_V2 = "ts/distiluse-base-multilingual-cased-v2"
    DISTILBERT_BASE_UNCASED = "ts/distilbert-base-uncased"
    GTE_LARGE = "ts/gte-large"
    GTE_SMALL = "ts/gte-small"
    JINA_EMBEDDINGS_V2_BASE_EN = "ts/jina-embeddings-v2-base-en"
    MULTILINGUAL_E5_LARGE = "ts/multilingual-e5-large"
    MULTILINGUAL_E5_SMALL = "ts/multilingual-e5-small"


class ReRankModel(Enum):
    # JINA_RERANK_V2 = "jina-rerank-v2"
    BGE_RERANKER_LARGE = "bge-m3-Rerank"
    MXBAI_RERANKER_LARGE = "mxbai-rerank-large-V1"


class Preprocessing(BaseModel):
    chunk_mode: ChunkMod = ChunkMod.NAIVE
    chunk_size: int = 100
    overlap_size: int = 20
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


class Entry(BaseModel):
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
