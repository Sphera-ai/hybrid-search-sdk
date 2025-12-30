from __future__ import annotations

import inspect
from enum import StrEnum
from random import randint

from hybridsearch import (
    Document,
    DocumentInformations,
    EmbeddingModel,
    HybridSearch,
    Preprocessing,
    ReRankModel,
)
from hybridsearch.exceptions import InvalidApiKey

"""
This file contains the tests for the hybrid seach and semantic search of class HybridSearch
"""

demo_api_key = "test"


class FilesTestsUrls(StrEnum):
    """_summary_
    File urls to be used in the tests
    """

    YUGIOH = "https://img.konami.com/yugioh/worldchampionship/2025/data/limitregulation-tcg.pdf"
    BASKET = "https://www.itaerferrarin.edu.it/pasw4/didattica/pallacanestro.pdf"
    DOLCI = "https://comune.ravenna.it/wp-content/uploads/2025/09/Ricettario-per-dolci-momenti-insieme.pdf"
    H3_HEADER = "https://gist.github.com/rt2zz/e0a1d6ab2682d2c47746950b84c0b6ee#file-markdown-sample-md"
    INLINE_LINK = (
        "https://raw.githubusercontent.com/mxstbr/markdown-test-file/master/TEST.md"
    )
    INSTALLATION = (
        "https://github.com/othneildrew/Best-README-Template/blob/main/README.md"
    )
    DRAWIO = "https://cidoc-crm.org/sites/default/files/Draw.io%20to%20Triples.pdf"
    HOCKEY = "https://www.mobilesport.ch/assets/lbwp-cdn/mobilesport/files/1713775893/mobilesport-hockey-su-ghiaccio-giovani--forme-di-allenamento-relative-alle-forme-caratteristiche.pdf"
    TENNIS = "https://www.sergvese.it/smba/files/tennis.pdf"
    VIDEOGAMES = "https://www.chateaudeprangins.ch/chateaudeprangins/medias/games/la-storia-dei-videogiochi-2021_it.pdf"


def setup_document(input_file_id, input_file):
    """_summary_
    Setup Document instance for create_document method

    Returns:
        Document: Document instance
    """
    return Document(
        preprocessing=Preprocessing(),
        default_fields=DocumentInformations(file_id=input_file_id),
        file=input_file,
        fields={},
    )


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

def test_L12_V2_three_collections_remote_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.REMOTE_QWEN_3_8B)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"

def test_L12_V2_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.ALL_MINILM_L12_V2)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"


def test_Distilbert_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.DISTILBERT_BASE_UNCASED)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"

def test_DISTILUSE_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.DISTILUSE_BASE_MULTILINGUAL_CASED_V2)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"

def test_E5_LARGE_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.E5_LARGE)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"

def test_E5LARGE_V2_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.E5_LARGE_V2)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"


def test_E5SMALL_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.E5_SMALL)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"


def test_E5SMALL_V2_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.E5_SMALL_V2)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"


def test_GTELARGE_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.GTE_LARGE)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"

def test_GTESMALL_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.GTE_SMALL)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"


def test_JINA_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.JINA_EMBEDDINGS_V2_BASE_EN)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        #print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"

def test_MULILINGUAL_three_collections_internal_embedding_hybrid_search_basket():
    """_summary_
    Create 3 collections with internal embedding model, add documents to each of these collections
    and perform hybrid search on these collections, with the query being about basket
    Returns:
        bool: True if basket document is found, False otherwise
    """
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 3
    num_results = 8
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i],model_name=EmbeddingModel.MULTILINGUAL_E5_LARGE)

    doc_yugioh = setup_document("test_file_yugioh", FilesTestsUrls.YUGIOH)

    doc_dolci = setup_document("test_file_dolci", FilesTestsUrls.DOLCI)

    doc_md_1 = setup_document("test_file_md_1", FilesTestsUrls.H3_HEADER)

    doc_md_3 = setup_document("test_file_md_3", FilesTestsUrls.INSTALLATION)

    doc_drawio = setup_document("test_drawio", FilesTestsUrls.DRAWIO)

    doc_basket = setup_document("test_basket", FilesTestsUrls.BASKET)

    hybrid_search.create_document(collection_names[0], doc_drawio)
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    hybrid_search.create_document(collection_names[1], doc_dolci)
    hybrid_search.create_document(collection_names[1], doc_md_1)
    hybrid_search.create_document(collection_names[0], doc_md_3)
    hybrid_search.create_document(collection_names[2], doc_basket)

    collections = ",".join(collection_names)
    print("COLLECTIONS", collections)
    res = hybrid_search.hybrid_search(
        collection_name=collections,
        query="cosa abbiamo sul basekt?",
        num_results=num_results,
        ft_search_field="text",
        rerank=True,
        rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
    )
    for elem in res:
        elem["document"]["embedding"] = ""

    for elem in res:
        print("FILE NAME", elem["document"]["file_id"])
        print("FILE ID", elem["document"]["id"])
        print("TEXT", elem["document"]["text"])

    print("METHOD", def_name)
    assert res[0]["document"]["file_id"] == "test_basket"