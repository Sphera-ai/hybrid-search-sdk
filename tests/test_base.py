from __future__ import annotations

from random import randint

from hybridsearch import (
    Document,
    DocumentInformations,
    EmbeddingModel,
    Entry,
    HybridSearch,
    Preprocessing,
)

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


def test_init_should_raise_exeption_when_api_key_is_invalid():
    """
    This function tests the __init__ function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    try:
        HybridSearch(api_key="invalid")
    except Exception as e:
        assert str(e) == "Invalid API Key"


def test_document_collection():
    """
    This function tests the document_collection function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    random_int = randint(1, 1000)
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

    random_int = randint(1, 1000)
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


"""
Create custom collection
1 - Embedding field not found
2 - Model name already exists
3 - Schema not in the correct format
"""

"""
Get collection by name
1 - Collection name not found
"""

"""
create_document
1 - Collection name not found
"""

"""
delete collection
1 - Collection name not found
"""

"""
semantic_search
1 - Collection name not found
2 - Query is empty
3 - Number of results should  be greater than 0
"""

"""
hybrid search
1 - Collection name not found
2 - Query is empty
3 - Number of results should  be greater than 0
4 - Field not in the collection
"""

"""
get schema attributes
1 - Collection name not found
"""
