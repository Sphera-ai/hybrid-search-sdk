from __future__ import annotations

import pytest
from hybridsearch import (
    Document,
    DocumentInformations,
    EmbeddingModel,
    Filter,
    HybridSearch,
    Operator,
    Preprocessing,
    ReRankModel,
)
from hybridsearch.exceptions import InvalidRequest

from tests.demo_docs import DEMO_DOCS, ingest_documents

"""
Integration tests for the hybrid search and semantic search endpoints of the
microservice, focused on cross-collection ranking.

Requires a running microservice (hybrid-search/docker-compose.yaml) and
network access to fetch the demo documents. Most tests rerank with the local
BGE-m3 reranker (standard architecture, no trust_remote_code) because the GTE
and mxbai rerankers (Alibaba new_impl code) crash intermittently on CPU with
transformers 5.x; the remote rerank path is covered explicitly by
test_three_collections_internal_embedding_remote_reranker (needs a valid
FIREWORKS_APIKEY) and test_base.py::test_remote_embedding.
"""

demo_api_key = "test"


def test_init():
    """
    This function tests the __init__ function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    HybridSearch(api_key=demo_api_key)
    assert True


def test_invalid_key():
    """
    The service must reject an invalid API key and accept the valid one
    """

    assert not HybridSearch(api_key="invalid").check_api_key()
    assert HybridSearch(api_key=demo_api_key).check_api_key()


def test_three_collections_internal_embedding_semantic_search(collection_factory, hs):
    """
    Create 3 collections with internal embedding model, add documents to each
    of these collections and perform semantic search on these collections,
    with the query being about tennis
    """
    num_results = 8
    collection_names = [collection_factory() for _ in range(3)]

    ingest_documents(
        hs,
        collection_names[0],
        ["test_drawio", "test_file_yugioh", "test_file_md_3", "test_videogames"],
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs,
        collection_names[2],
        ["test_basket", "test_tennis", "test_hockey", "test_inline"],
    )

    res = hs.semantic_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo su tennis?",
        num_results=num_results,
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    assert res[0]["document"]["file_id"] == "test_tennis"


def test_three_collections_remote_embedding_semantic_search(collection_factory, hs):
    """
    Create 3 collections with remote embedding model, add documents to each
    of these collections and perform semantic search on these collections,
    with the query being about tennis
    """
    num_results = 8
    collection_names = [
        collection_factory(model_name=EmbeddingModel.REMOTE_QWEN_3_8B) for _ in range(3)
    ]

    ingest_documents(
        hs,
        collection_names[0],
        ["test_drawio", "test_file_yugioh", "test_file_md_3", "test_videogames"],
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs,
        collection_names[2],
        ["test_basket", "test_tennis", "test_hockey", "test_inline"],
    )

    res = hs.semantic_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo su tennis?",
        num_results=num_results,
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    assert res[0]["document"]["file_id"] == "test_tennis"


def test_three_collections_mixed_embedding_semantic_search(collection_factory, hs):
    """
    Create 2 collections with remote embedding model and 1 with internal
    embedding model, add documents to each of these collections and perform
    semantic search on these collections, with the query being about tennis
    """
    num_results = 8
    collection_names = [
        collection_factory(model_name=EmbeddingModel.REMOTE_QWEN_3_8B) for _ in range(2)
    ]
    collection_names.append(collection_factory())

    ingest_documents(
        hs,
        collection_names[0],
        ["test_drawio", "test_file_yugioh", "test_file_md_3", "test_videogames"],
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs,
        collection_names[2],
        ["test_basket", "test_tennis", "test_hockey", "test_inline"],
    )

    res = hs.semantic_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo su tennis?",
        num_results=num_results,
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    assert res[0]["document"]["file_id"] == "test_tennis"


def test_three_collections_internal_embedding_hybrid_search_basket(
    collection_factory, hs
):
    """
    Create 3 collections with internal embedding model, add documents to each
    of these collections and perform hybrid search on these collections, with
    the query being about basket
    """
    num_results = 8
    collection_names = [collection_factory() for _ in range(3)]

    ingest_documents(
        hs, collection_names[0], ["test_drawio", "test_file_yugioh", "test_file_md_3"]
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(hs, collection_names[2], ["test_basket"])

    res = hs.hybrid_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    assert res[0]["document"]["file_id"] == "test_basket"


def test_six_collections_remote_embedding_hybrid_search(collection_factory, hs):
    """
    Create 6 collections with remote embedding model, add documents to each
    of these collections and perform hybrid search on these collections, with
    the query being about hockey
    """
    num_results = 8
    collection_names = [
        collection_factory(model_name=EmbeddingModel.REMOTE_QWEN_3_8B) for _ in range(6)
    ]

    ingest_documents(
        hs, collection_names[0], ["test_drawio", "test_file_yugioh", "test_file_md_3"]
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs, collection_names[2], ["test_tennis", "test_hockey", "test_inline"]
    )
    ingest_documents(hs, collection_names[4], ["test_basket"])
    ingest_documents(hs, collection_names[5], ["test_videogames"])

    res = hs.hybrid_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo sull' hockey?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    found_documents = [d["document"]["file_id"] for d in res]
    assert "test_hockey" in found_documents


def test_six_collections_mixed_embedding_hybrid_search(collection_factory, hs):
    """
    Create 3 collections with remote embedding model and 3 with internal
    embedding model, add documents to each of these collections and perform
    hybrid search on these collections, with the query being about hockey
    """
    num_results = 8
    collection_names = [
        collection_factory(model_name=EmbeddingModel.REMOTE_QWEN_3_8B) for _ in range(3)
    ]
    collection_names.extend(collection_factory() for _ in range(3))

    ingest_documents(
        hs, collection_names[0], ["test_drawio", "test_file_yugioh", "test_file_md_3"]
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs, collection_names[2], ["test_tennis", "test_hockey", "test_inline"]
    )
    ingest_documents(hs, collection_names[4], ["test_basket"])
    ingest_documents(hs, collection_names[5], ["test_videogames"])

    res = hs.hybrid_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo sull' hockey?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    found_documents = [d["document"]["file_id"] for d in res]
    assert "test_hockey" in found_documents


def test_six_collections_mixed_embedding_semantic_search(collection_factory, hs):
    """
    Create 3 collections with remote embedding model and 3 with internal
    embedding model, add documents to each of these collections and perform
    semantic search on these collections, with the query being about hockey
    """
    num_results = 8
    collection_names = [
        collection_factory(model_name=EmbeddingModel.REMOTE_QWEN_3_8B) for _ in range(3)
    ]
    collection_names.extend(collection_factory() for _ in range(3))

    ingest_documents(
        hs, collection_names[0], ["test_drawio", "test_file_yugioh", "test_file_md_3"]
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs, collection_names[2], ["test_tennis", "test_hockey", "test_inline"]
    )
    ingest_documents(hs, collection_names[4], ["test_basket"])
    ingest_documents(hs, collection_names[5], ["test_videogames"])

    res = hs.semantic_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo sull' hockey?",
        num_results=num_results,
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    found_documents = [d["document"]["file_id"] for d in res]
    assert "test_hockey" in found_documents


def test_three_collections_remote_embedding_hybrid_search_videogames(
    collection_factory, hs
):
    """
    Create 3 collections with remote embedding model, add documents to each
    of these collections and perform hybrid search on these collections, with
    the query being about videogames
    """
    num_results = 8
    collection_names = [
        collection_factory(model_name=EmbeddingModel.REMOTE_QWEN_3_8B) for _ in range(3)
    ]

    ingest_documents(
        hs,
        collection_names[0],
        ["test_drawio", "test_file_yugioh", "test_file_md_3", "test_videogames"],
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs,
        collection_names[2],
        ["test_basket", "test_tennis", "test_hockey", "test_inline"],
    )

    res = hs.hybrid_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo sul videogame Monkey Island?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    found_documents = [d["document"]["file_id"] for d in res]
    assert "test_videogames" in found_documents


def test_three_collections_mixed_embedding_hybrid_search_videogames(
    collection_factory, hs
):
    """
    Create 2 collections with remote embedding model and 1 with internal
    embedding model, add documents to each of these collections and perform
    hybrid search on these collections, with the query being about videogames
    """
    num_results = 8
    collection_names = [
        collection_factory(model_name=EmbeddingModel.REMOTE_QWEN_3_8B) for _ in range(2)
    ]
    collection_names.append(collection_factory())

    ingest_documents(
        hs,
        collection_names[0],
        ["test_drawio", "test_file_yugioh", "test_file_md_3", "test_videogames"],
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs,
        collection_names[2],
        ["test_basket", "test_tennis", "test_hockey", "test_inline"],
    )

    res = hs.hybrid_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo sul videogame Monkey Island?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.BGE_RERANKER_LARGE,
    )

    found_documents = [d["document"]["file_id"] for d in res]
    assert "test_videogames" in found_documents


def test_three_collections_internal_embedding_remote_reranker(collection_factory, hs):
    """
    Create 3 collections with internal embedding model, add documents to each
    of these collections and perform semantic search reranked with the REMOTE
    reranker. Requires FIREWORKS_APIKEY to be configured in the service
    environment; the local-reranker equivalents above do not.
    """
    num_results = 8
    collection_names = [collection_factory() for _ in range(3)]

    ingest_documents(
        hs,
        collection_names[0],
        ["test_drawio", "test_file_yugioh", "test_file_md_3", "test_videogames"],
    )
    ingest_documents(hs, collection_names[1], ["test_file_dolci", "test_file_md_1"])
    ingest_documents(
        hs,
        collection_names[2],
        ["test_basket", "test_tennis", "test_hockey", "test_inline"],
    )

    res = hs.semantic_search(
        collection_name=",".join(collection_names),
        query="cosa abbiamo su tennis?",
        num_results=num_results,
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )

    assert res[0]["document"]["file_id"] == "test_tennis"


# ---------------------------------------------------------------------------
# Regression tests for the correctness fixes in the microservice
# ---------------------------------------------------------------------------


def test_num_results_gt10_internal_semantic_search(large_internal_collection, hs):
    """
    Regression: internal-model searches were capped at Typesense's default
    per_page (10), silently ignoring num_results > 10 and shrinking the
    rerank candidate pool
    """
    res = hs.semantic_search(
        collection_name=large_internal_collection,
        query="sport",
        num_results=15,
    )

    assert 10 < len(res) <= 15


def test_semantic_search_excludes_embedding(large_internal_collection, hs):
    """
    Regression: the semantic search internal path did not exclude the
    embedding field, shipping raw embedding vectors in every hit
    """
    res = hs.semantic_search(
        collection_name=large_internal_collection,
        query="cosa abbiamo su tennis?",
        num_results=5,
    )

    assert res
    assert all("embedding" not in hit["document"] for hit in res)


def test_filter_in_operator(large_internal_collection, hs):
    """
    Regression: IN filters were built with a plain f-string, producing
    malformed filter_by clauses for operators like IN
    """
    res = hs.hybrid_search(
        collection_name=large_internal_collection,
        query="sport",
        num_results=10,
        ft_search_field="text",
        filters=[
            Filter(
                field="file_id",
                operator=Operator.IN,
                value=["test_tennis", "test_basket"],
            )
        ],
    )

    assert res
    assert all(
        hit["document"]["file_id"] in {"test_tennis", "test_basket"} for hit in res
    )


def test_mxbai_reranker(large_internal_collection, hs):
    """
    Regression: the mxbai reranker raised TypeError on every call (wrong
    unpacking of the CrossEncoder.rank result) and was silently skipped
    """
    res = hs.semantic_search(
        collection_name=large_internal_collection,
        query="cosa abbiamo su tennis?",
        num_results=5,
        rerank=True,
        rerank_model=ReRankModel.MXBAI_RERANKER_LARGE,
    )

    assert res
    assert res[0]["document"]["file_id"] == "test_tennis"


def test_invalid_num_results(large_internal_collection, hs):
    """
    num_results outside [1, 100] must be rejected with a clean client error
    """
    with pytest.raises(InvalidRequest):
        hs.semantic_search(
            collection_name=large_internal_collection,
            query="sport",
            num_results=0,
        )
    with pytest.raises(InvalidRequest):
        hs.semantic_search(
            collection_name=large_internal_collection,
            query="sport",
            num_results=101,
        )


def test_invalid_overlap_size(hs):
    """
    overlap_size >= chunk_size must be rejected: the naive chunker buffer
    would never shrink, producing duplicated chunks
    """
    document = Document(
        preprocessing=Preprocessing(chunk_size=10, overlap_size=10),
        default_fields=DocumentInformations(file_id="test_invalid_overlap"),
        file=DEMO_DOCS["test_tennis"],
        fields={},
    )
    with pytest.raises(InvalidRequest):
        hs.create_document("any_collection", document)
