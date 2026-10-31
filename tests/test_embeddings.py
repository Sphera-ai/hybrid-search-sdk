from __future__ import annotations

import pytest
from hybridsearch import EmbeddingModel, ReRankModel

from tests.demo_docs import ingest_documents

"""
Integration tests running the same hybrid search against collections backed
by every supported embedding model.

Requires a running microservice (hybrid-search/docker-compose.yaml) and
network access to fetch the demo documents. Collections with a remote
embedding model additionally require OPENROUTER_APIKEY to be configured in
the service environment. Reranking uses the local BGE-m3 reranker (standard
architecture, no trust_remote_code) because the GTE and mxbai rerankers
(Alibaba new_impl code) crash intermittently on CPU with transformers 5.x;
the remote rerank call path is covered by test_base.py::test_remote_embedding.
"""

# Every embedding model covered by the original per-model test functions
EMBEDDING_MODELS_UNDER_TEST = [
    EmbeddingModel.REMOTE_QWEN_3_8B,
    EmbeddingModel.ALL_MINILM_L12_V2,
    EmbeddingModel.DISTILBERT_BASE_UNCASED,
    EmbeddingModel.DISTILUSE_BASE_MULTILINGUAL_CASED_V2,
    EmbeddingModel.E5_LARGE,
    EmbeddingModel.E5_LARGE_V2,
    EmbeddingModel.E5_SMALL,
    EmbeddingModel.E5_SMALL_V2,
    EmbeddingModel.GTE_LARGE,
    EmbeddingModel.GTE_SMALL,
    EmbeddingModel.JINA_EMBEDDINGS_V2_BASE_EN,
    EmbeddingModel.MULTILINGUAL_E5_LARGE,
]


@pytest.mark.parametrize(
    "model_name",
    EMBEDDING_MODELS_UNDER_TEST,
    ids=[model.value for model in EMBEDDING_MODELS_UNDER_TEST],
)
def test_hybrid_search_basket(collection_factory, hs, model_name):
    """
    Create 3 collections backed by the given embedding model, add documents
    to each of these collections and perform hybrid search on these
    collections, with the query being about basket.

    Asserts the basket document is surfaced among the results: rank-1 is too
    strict as a universal bar across models of very different quality (e.g.
    English-only models queried in Italian), and proves flaky run-to-run.
    """
    collection_names = [collection_factory(model_name=model_name) for _ in range(3)]

    ingest_documents(
        hs, collection_names[0], ["test_drawio", "test_file_yugioh", "test_file_md_3"]
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(hs, collection_names[2], ["test_basket"])

    res = hs.hybrid_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo sul basekt?",
        num_results=8,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    found_documents = [d["document"]["file_id"] for d in res]
    assert "test_basket" in found_documents
