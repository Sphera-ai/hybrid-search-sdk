from __future__ import annotations

import inspect
from random import randint
from time import time

from hybridsearch import (
    ChunkMod,
    Document,
    DocumentInformations,
    EmbeddingModel,
    Entry,
    HybridSearch,
    Preprocessing,
    ReRankModel,
)
from hybridsearch.exceptions import (
    CollectionAlreadyExists,
    CollectionNotFound,
    InvalidApiKey,
)
from hybridsearch.models import Filter, Operator

"""
This file contains the tests for the base class HybridSearch
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
    This function tests the __init__ function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    try:
        HybridSearch(api_key="invalid")
    except InvalidApiKey:
        assert True
    except Exception as e:
        print(e)
        assert False

def test_document_collection():
    """
    This function tests the document_collection function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    hybrid_search.create_collection(f"test_collection_{random_int}")
    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert collection_present

    doc = Document(
        preprocessing=Preprocessing(),
        default_fields=DocumentInformations(file_id="test_file"),
        file="https://css4.pub/2015/textbook/somatosensory.pdf",
        fields={},
    )
    hybrid_search.create_document(f"test_collection_{random_int}", doc)
    res = hybrid_search.hybrid_search(
        collection_name=f"test_collection_{random_int}",
        query="sensory information in receptors",
        num_results=2,
        ft_search_field="text",
    )
    assert res is not None

    hybrid_search.delete_collection(f"test_collection_{random_int}")

    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert not collection_present


def test_custom_collection():
    """
    This function tests the create_custom_collection function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    schema = {
        "fields": [
            {"name": ".*", "type": "auto"},
            {"name": "text", "type": "string"},
            {
                "name": "embedding",
                "type": "float[]",
                "embed": {
                    "from": ["text"],
                    "model_config": {
                        "model_name": EmbeddingModel.MULTILINGUAL_E5_SMALL.value
                    },
                },
            },
            {"name": "message_id", "type": "int32"},
            {"name": "chat_id", "type": "int32"},
            {"name": "role", "type": "string"},
        ],
        "metadata": {"embedding_model": EmbeddingModel.MULTILINGUAL_E5_SMALL.value},
    }
    hybrid_search.create_custom_collection(
        f"test_collection_{random_int}", schema=schema
    )
    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert collection_present

    entry1 = Entry(
        fields={
            "text": "This is a test",
            "message_id": 1,
            "chat_id": 1,
            "role": "user",
        }
    )
    entry2 = Entry(
        fields={
            "text": "Ciao come stai?",
            "message_id": 1,
            "chat_id": 1,
            "role": "user",
        }
    )

    hybrid_search.create_entry(
        f"test_collection_{random_int}",
        entry1,
    )
    hybrid_search.create_entry(
        f"test_collection_{random_int}",
        entry2,
    )

    res = hybrid_search.hybrid_search(
        collection_name=f"test_collection_{random_int}",
        query="test",
        num_results=1,
        ft_search_field="text",
    )
    assert res is not None

    hybrid_search.delete_collection(f"test_collection_{random_int}")

    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert not collection_present


def test_supported_documents():
    """
    This function tests the supported_documents function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    hybrid_search = HybridSearch(api_key=demo_api_key)
    supported_documents = hybrid_search.get_supported_documents()
    assert isinstance(supported_documents, dict)
    assert len(supported_documents.keys()) > 0
    assert len(supported_documents["supportd_extensions"]) > 0
    assert len(supported_documents["supported_mimetypes"]) > 0


def test_already_existing_cutom_collection():
    """
    This function tests the already_existing_collection function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    schema = {
        "fields": [
            {"name": ".*", "type": "auto"},
            {"name": "text", "type": "string"},
            {
                "name": "embedding",
                "type": "float[]",
                "embed": {
                    "from": ["text"],
                    "model_config": {
                        "model_name": EmbeddingModel.MULTILINGUAL_E5_SMALL.value
                    },
                },
            },
            {"name": "message_id", "type": "int32"},
            {"name": "chat_id", "type": "int32"},
            {"name": "role", "type": "string"},
        ],
        "metadata": {"embedding_model": EmbeddingModel.MULTILINGUAL_E5_SMALL.value},
    }
    hybrid_search.create_custom_collection(
        f"test_collection_{random_int}", schema=schema
    )
    try:
        hybrid_search.create_custom_collection(
            f"test_collection_{random_int}", schema=schema
        )
        exception_raised = False
    except CollectionAlreadyExists:
        exception_raised = True
    except Exception as e:
        print(e)
        exception_raised = False
    finally:
        hybrid_search.delete_collection(f"test_collection_{random_int}")

    assert exception_raised


def test_already_existing_collection():
    """
    This function tests the already_existing_collection function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    hybrid_search.create_collection(f"test_collection_{random_int}")
    try:
        hybrid_search.create_collection(f"test_collection_{random_int}")
        exception_raised = False
    except CollectionAlreadyExists:
        exception_raised = True
    except Exception as e:
        print(e)
        exception_raised = False
    finally:
        hybrid_search.delete_collection(f"test_collection_{random_int}")

    assert exception_raised


def test_collection_not_existing():
    """
    This function tests the collection_not_existing function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    hybrid_search.create_collection(f"test_collection_{random_int}")
    try:
        hybrid_search.delete_collection(f"test_collection_{random_int + 1}")
        exception_raised = False
    except CollectionNotFound:
        exception_raised = True
    except Exception as e:
        print(e)
        exception_raised = False
    finally:
        hybrid_search.delete_collection(f"test_collection_{random_int}")
    assert exception_raised


def test_filters():
    """
    This function tests the filters function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    hybrid_search.create_collection(f"test_collection_{random_int}")

    doc = Document(
        preprocessing=Preprocessing(),
        default_fields=DocumentInformations(file_id="test_file"),
        file="https://css4.pub/2015/textbook/somatosensory.pdf",
        fields={},
    )
    hybrid_search.create_document(f"test_collection_{random_int}", doc)
    res = hybrid_search.hybrid_search(
        collection_name=f"test_collection_{random_int}",
        query="sensory information in receptors",
        num_results=2,
        ft_search_field="text",
        filters=[Filter(field="start_page", operator=Operator.EQUAL, value=0)],
    )
    pages = [result["document"]["start_page"] for result in res]
    assert res is not None
    assert all(page == 0 for page in pages)

    hybrid_search.delete_collection(f"test_collection_{random_int}")


def test_semantic_chunks():
    """
    This function tests the document_collection function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    hybrid_search.create_collection(
        f"test_collection_{random_int}", prev_next_chunks=True
    )
    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert collection_present

    doc = Document(
        preprocessing=Preprocessing(chunk_mode=ChunkMod.SEMANTIC, semantic_thr_std=1.5),
        default_fields=DocumentInformations(file_id="test_file"),
        file="https://css4.pub/2015/textbook/somatosensory.pdf",
        fields={},
    )
    hybrid_search.create_document(f"test_collection_{random_int}", doc)
    start_time = time()
    res = hybrid_search.hybrid_search(
        collection_name=f"test_collection_{random_int}",
        query="sensory information in receptors",
        num_results=2,
        ft_search_field="text",
    )
    end_time = time()
    print(f"Search time: {end_time - start_time} seconds")
    assert res is not None

    hybrid_search.delete_collection(f"test_collection_{random_int}")

    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert not collection_present


def test_reranker():
    """
    This function tests the document_collection function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    hybrid_search.create_collection(f"test_collection_{random_int}")
    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert collection_present

    doc = Document(
        preprocessing=Preprocessing(chunk_mode=ChunkMod.SEMANTIC, semantic_thr_std=1.5),
        default_fields=DocumentInformations(file_id="test_file"),
        file="https://css4.pub/2015/textbook/somatosensory.pdf",
        fields={},
    )
    hybrid_search.create_document(f"test_collection_{random_int}", doc)
    start_time = time()
    res = hybrid_search.hybrid_search(
        collection_name=f"test_collection_{random_int}",
        query="sensory information in receptors",
        num_results=2,
        ft_search_field="text",
        rerank_model=ReRankModel.GTE_MULTILINGUAL_RERANKER_BASE,
        rerank=True,
    )
    end_time = time()
    print(f"Search time with Rerank: {end_time - start_time} seconds")
    assert res is not None

    hybrid_search.delete_collection(f"test_collection_{random_int}")

    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert not collection_present


def test_remote_embedding():
    """
    This function tests the document_collection function of the HybridSearch class with a remote embedding model
    """
    random_int = randint(1000000, 100000000)
    hybrid_search = HybridSearch(api_key=demo_api_key)
    hybrid_search.create_collection(
        f"test_collection_{random_int}", model_name=EmbeddingModel.REMOTE_QWEN_3_8B
    )
    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert collection_present

    doc = Document(
        preprocessing=Preprocessing(),
        default_fields=DocumentInformations(file_id="test_file"),
        file="https://css4.pub/2015/textbook/somatosensory.pdf",
        fields={},
    )
    hybrid_search.create_document(f"test_collection_{random_int}", doc)
    res = hybrid_search.hybrid_search(
        collection_name=f"test_collection_{random_int}",
        query="sensory information in receptors",
        num_results=2,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    assert res is not None

    hybrid_search.delete_collection(f"test_collection_{random_int}")

    c = hybrid_search.get_all_collections()
    collection_present = any(
        collection["name"] == f"test_collection_{random_int}" for collection in c
    )
    assert not collection_present
