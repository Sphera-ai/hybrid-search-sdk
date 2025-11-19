from __future__ import annotations

import inspect
from random import randint
from time import time

# from hybridsearch import (
#     ChunkMod,
#     Document,
#     DocumentInformations,
#     EmbeddingModel,
#     Entry,
#     HybridSearch,
#     Preprocessing,
#     ReRankModel,
# )
# from hybridsearch.exceptions import (
#     CollectionAlreadyExists,
#     CollectionNotFound,
#     InvalidApiKey,
# )
# from hybridsearch.models import Filter, Operator

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

class FilesTestsUrls:
    YUGIOH = "https://img.konami.com/yugioh/worldchampionship/2025/data/limitregulation-tcg.pdf"
    HOCKEY = "https://www.hockeypergine.it/wp-content/uploads/2018/02/colouring_book_iihf.pdf"
    DOLCI = "https://comune.ravenna.it/wp-content/uploads/2025/09/Ricettario-per-dolci-momenti-insieme.pdf"
    H3_HEADER = "https://gist.github.com/rt2zz/e0a1d6ab2682d2c47746950b84c0b6ee#file-markdown-sample-md"
    INLINE_LINK = "https://raw.githubusercontent.com/mxstbr/markdown-test-file/master/TEST.md"
    INSTALLATION = "https://github.com/othneildrew/Best-README-Template/blob/main/README.md"

def setup_document(input_file_id,input_file):
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

# def test_collection_with_documents():
#     # mio test
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     random_int_collections = []
#     collection_names = []
#     num_collections = 6
#     for i in range(num_collections):
#         random_int_collections.append(randint(1, 10000))  # noqa: PERF401
#         collection_names.append(f"test_collection_{random_int_collections[i]}")
#         hybrid_search.create_collection(collection_names[i])

#     doc_yugioh = setup_document(
#         "test_file_yugioh",
#         FilesTestsUrls.YUGIOH
#     )

#     doc_hockey = setup_document(
#         "test_file_hockey",
#         FilesTestsUrls.HOCKEY
#     )

#     doc_dolci = setup_document(
#         "test_file_dolci",
#         FilesTestsUrls.DOLCI
#     )

#     doc_md_1 = setup_document(
#         "test_file_md_1",
#         FilesTestsUrls.H3_HEADER
#     )

#     doc_md_2 = setup_document(
#         "test_file_md_2",
#         FilesTestsUrls.INLINE_LINK
#     )

#     doc_md_3 = setup_document(
#         "test_file_md_3",
#         FilesTestsUrls.INSTALLATION
#     )

#     # aggiungo yugioh alla prima collection
#     hybrid_search.create_document(collection_names[0], doc_yugioh)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[0],
#         query="che carte bannate ci sono",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU YUGIOH SINGLE SEARCH", res[0]["document"]["text"])

#     # aggiungo dolci alla terza collection
#     hybrid_search.create_document(collection_names[2], doc_dolci)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[2],
#         query="impugnature hockey",
#         num_results=2,
#         ft_search_field="text",
#     )
#     # aggiungo file md 1 alla terza collection
#     hybrid_search.create_document(collection_names[2], doc_md_1)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[2],
#         query="impugnature hockey",
#         num_results=2,
#         ft_search_field="text",
#     )
#     # aggiungo file md 3 alla terza collection
#     hybrid_search.create_document(collection_names[2], doc_md_3)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[2],
#         query="come si la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )
#     # aggiungo file md 2 alla seconda collection
#     hybrid_search.create_document(collection_names[1], doc_md_2)
#     # definisco la lista di collections per la multi search
#     collections = collection_names[0],collection_names[1],collection_names[2]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="cosa abbiamo su installation",
#         num_results=8,
#         ft_search_field="text",
#     )
#     print(res[0]["document"]["text"])

#     # definisco la lista di collections per la multi search
#     collections = collection_names[0],collection_names[1],collection_names[2]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="cosa abbiamo su installation",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU INSTALLATION MULTI SEARCH", res[0]["document"]["text"])

#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="che carte bannate ci sono",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU YUGIOH MULTI SEARCH", res[0]["document"]["text"])
#     assert True

# def test_collection_with_documents_two_collections_dolci_then_yugioh():
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     random_int_collections = []
#     collection_names = []
#     num_collections = 2
#     for i in range(num_collections):
#         random_int_collections.append(randint(1, 10000))  # noqa: PERF401
#         collection_names.append(f"test_collection_{random_int_collections[i]}")
#         hybrid_search.create_collection(collection_names[i])

#     doc_yugioh = setup_document(
#         "test_file_yugioh",
#         FilesTestsUrls.YUGIOH
#     )

#     doc_dolci = setup_document(
#         "test_file_dolci",
#         FilesTestsUrls.DOLCI
#     )

#     doc_md_1 = setup_document(
#         "test_file_md_1",
#         FilesTestsUrls.H3_HEADER
#     )

#     doc_md_2 = setup_document(
#         "test_file_md_2",
#         FilesTestsUrls.INLINE_LINK
#     )

#     # aggiungo yugioh alla prima collection
#     hybrid_search.create_document(collection_names[0], doc_yugioh)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[0],
#         query="che carte bannate ci sono",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU YUGIOH SINGLE SEARCH", res[0]["document"]["text"])

#     # aggiungo dolci alla seconda collection
#     hybrid_search.create_document(collection_names[1], doc_dolci)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )
#     # aggiungo file md 1 alla terza collection
#     hybrid_search.create_document(collection_names[1], doc_md_1)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )

#     # aggiungo file md 2 alla seconda collection
#     hybrid_search.create_document(collection_names[1], doc_md_2)
#     # definisco la lista di collections per la multi search
#     collections = [collection_names[0],collection_names[1]]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="come si fa la torta paradiso",
#         num_results=8,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print(res[0]["document"]["text"])

#     # definisco la lista di collections per la multi search
#     collections = [collection_names[0],collection_names[1]]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print("CHE COSA ABBIAMO SU DOLCI MULTI SEARCH", res[0]["document"]["text"])

#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="che carte bannate ci sono in yugioh",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print("CHE COSA ABBIAMO SU YUGIOH MULTI SEARCH", res[0]["document"]["text"])
#     assert True

# def test_collection_with_documents_two_collections_yugioh_then_dolci():
#     # mio test
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     random_int_collections = []
#     collection_names = []
#     num_collections = 2
#     for i in range(num_collections):
#         random_int_collections.append(randint(1, 10000))  # noqa: PERF401
#         collection_names.append(f"test_collection_{random_int_collections[i]}")
#         hybrid_search.create_collection(collection_names[i])

#     doc_yugioh = setup_document(
#         "test_file_yugioh",
#         FilesTestsUrls.YUGIOH
#     )

#     doc_dolci = setup_document(
#         "test_file_dolci",
#         FilesTestsUrls.DOLCI
#     )

#     doc_md_1 = setup_document(
#         "test_file_md_1",
#         FilesTestsUrls.H3_HEADER
#     )

#     doc_md_2 = setup_document(
#         "test_file_md_2",
#         FilesTestsUrls.INLINE_LINK
#     )

#     # aggiungo yugioh alla prima collection
#     hybrid_search.create_document(collection_names[0], doc_yugioh)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[0],
#         query="che carte bannate ci sono",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU YUGIOH SINGLE SEARCH", res[0]["document"]["text"])

#     # aggiungo dolci alla seconda collection
#     hybrid_search.create_document(collection_names[1], doc_dolci)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )
#     # aggiungo file md 1 alla terza collection
#     hybrid_search.create_document(collection_names[1], doc_md_1)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )

#     # aggiungo file md 2 alla seconda collection
#     hybrid_search.create_document(collection_names[1], doc_md_2)
#     # definisco la lista di collections per la multi search
#     collections = [collection_names[0],collection_names[1]]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="come si fa la torta paradiso",
#         num_results=8,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print(res[0]["document"]["text"])

#     # definisco la lista di collections per la multi search
#     collections = [collection_names[0],collection_names[1]]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="che carte bannate ci sono in yugioh",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print("CHE COSA ABBIAMO SU YUGIOH MULTI SEARCH", res[0]["document"]["text"])

#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print("CHE COSA ABBIAMO SU DOLCI MULTI SEARCH", res[0]["document"]["text"])
#     assert True

# def test_collection_with_documents_two_collections_installation():
#     # mio test
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     random_int_collections = []
#     collection_names = []
#     num_collections = 2
#     for i in range(num_collections):
#         random_int_collections.append(randint(1, 10000))  # noqa: PERF401
#         collection_names.append(f"test_collection_{random_int_collections[i]}")
#         hybrid_search.create_collection(collection_names[i])

#     doc_yugioh = setup_document(
#         "test_file_yugioh",
#         FilesTestsUrls.YUGIOH
#     )

#     doc_dolci = setup_document(
#         "test_file_dolci",
#         FilesTestsUrls.DOLCI
#     )

#     doc_md_1 = setup_document(
#         "test_file_md_1",
#         FilesTestsUrls.H3_HEADER
#     )

#     doc_md_3 = setup_document(
#         "test_file_md_3",
#         FilesTestsUrls.INSTALLATION
#     )

#     # aggiungo yugioh alla prima collection
#     hybrid_search.create_document(collection_names[0], doc_yugioh)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[0],
#         query="che carte bannate ci sono",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU YUGIOH SINGLE SEARCH", res[0]["document"]["text"])

#     # aggiungo dolci alla seconda collection
#     hybrid_search.create_document(collection_names[1], doc_dolci)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )
#     # aggiungo file md 1 alla terza collection
#     hybrid_search.create_document(collection_names[1], doc_md_1)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa la torta paradiso",
#         num_results=2,
#         ft_search_field="text",
#     )

#     # aggiungo file md 3 alla seconda collection
#     hybrid_search.create_document(collection_names[1], doc_md_3)
#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa l'installation",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU INSTALLATION SINGLE SEARCH", res[0]["document"]["text"])
#     # definisco la lista di collections per la multi search
#     collections = [collection_names[0],collection_names[1]]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="come si fa l'installation",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print("CHE COSA ABBIAMO SU INSTALLATION SINGLE SEARCH", res[0]["document"]["text"])
#     # definisco la lista di collections per la multi search
#     collections = [collection_names[0],collection_names[1]]
#     res = hybrid_search.hybrid_search(
#         collection_name=collections,
#         query="come si fa l'installation",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("COLLECTIONS", collections)
#     print("CHE COSA ABBIAMO SU INSTALLATION MULTI SEARCH", res[0]["document"]["text"])

#     res = hybrid_search.hybrid_search(
#         collection_name=collection_names[1],
#         query="come si fa l'installation",
#         num_results=2,
#         ft_search_field="text",
#     )
#     print("CHE COSA ABBIAMO SU INSTALLATION SINGLE SEARCH", res[0]["document"]["text"])
#     assert True

def test_collection_with_documents_single_installation_with_dolci():
    # mio test
    hybrid_search = HybridSearch(api_key=demo_api_key)
    def_name = inspect.currentframe().f_code.co_name
    random_int_collections = []
    collection_names = []
    num_collections = 2
    num_results = 10
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i])

    doc_yugioh = setup_document(
        "test_file_yugioh",
        FilesTestsUrls.YUGIOH
    )

    doc_dolci = setup_document(
        "test_file_dolci",
        FilesTestsUrls.DOLCI
    )

    doc_md_1 = setup_document(
        "test_file_md_1",
        FilesTestsUrls.H3_HEADER
    )

    doc_md_3 = setup_document(
        "test_file_md_3",
        FilesTestsUrls.INSTALLATION
    )

    # aggiungo yugioh alla prima collection
    hybrid_search.create_document(collection_names[0], doc_yugioh)

    # aggiungo dolci alla seconda collection
    hybrid_search.create_document(collection_names[1], doc_dolci)
    
    # aggiungo file md 1 alla terza collection
    hybrid_search.create_document(collection_names[1], doc_md_1)

    # aggiungo file md 3 alla seconda collection
    #hybrid_search.create_document(collection_names[1], doc_md_3)
    res = hybrid_search.semantic_search(
        collection_name=collection_names[1],
        query="come si fa l'h2 header'",
        num_results=num_results,
        #ft_search_field="text",
        rerank=True
    )
    for elem in res:
        elem["document"]["embedding"] = ""
    #print("CHE COSA ABBIAMO SU INSTALLATION SINGLE SEARCH", def_name, res[0]["document"]["text"])
    print("CHE COSA ABBIAMO SU H2 HEADER SINGLE SEARCH", def_name, res)
    for elem in res:
        print("SCORE", elem["text_match_info"]["score"])

    assert True

def test_collection_with_documents_single_installation_without_dolci():
    # mio test
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 2
    num_results = 10
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i])

    doc_yugioh = setup_document(
        "test_file_yugioh",
        FilesTestsUrls.YUGIOH
    )

    doc_dolci = setup_document(
        "test_file_dolci",
        FilesTestsUrls.DOLCI
    )

    doc_md_1 = setup_document(
        "test_file_md_1",
        FilesTestsUrls.H3_HEADER
    )

    doc_md_3 = setup_document(
        "test_file_md_3",
        FilesTestsUrls.INSTALLATION
    )

    # aggiungo yugioh alla prima collection
    hybrid_search.create_document(collection_names[0], doc_yugioh)
    
    # aggiungo file md 1 alla terza collection
    hybrid_search.create_document(collection_names[1], doc_md_1)

    # aggiungo file md 3 alla seconda collection
    hybrid_search.create_document(collection_names[1], doc_md_3)
    res = hybrid_search.hybrid_search(
        collection_name=collection_names[1],
        query="come si fa l'installation",
        num_results=num_results,
        ft_search_field="text",
    )
    #print("CHE COSA ABBIAMO SU INSTALLATION SINGLE SEARCH", res[0]["document"]["text"])
    #print("CHE COSA ABBIAMO SU INSTALLATION SINGLE SEARCH", def_name, res)
    assert True

def test_collection_with_documents_single_installation_with_dolci_in_first_collection():
    # mio test
    hybrid_search = HybridSearch(api_key=demo_api_key)
    random_int_collections = []
    collection_names = []
    def_name = inspect.currentframe().f_code.co_name
    num_collections = 2
    num_results = 10
    for i in range(num_collections):
        random_int_collections.append(randint(1000000, 100000000))  # noqa: PERF401
        collection_names.append(f"test_collection_{random_int_collections[i]}")
        hybrid_search.create_collection(collection_names[i])

    doc_yugioh = setup_document(
        "test_file_yugioh",
        FilesTestsUrls.YUGIOH
    )

    doc_dolci = setup_document(
        "test_file_dolci",
        FilesTestsUrls.DOLCI
    )

    doc_md_1 = setup_document(
        "test_file_md_1",
        FilesTestsUrls.H3_HEADER
    )

    doc_md_3 = setup_document(
        "test_file_md_3",
        FilesTestsUrls.INSTALLATION
    )

    # aggiungo yugioh alla prima collection
    hybrid_search.create_document(collection_names[0], doc_yugioh)

    # aggiungo dolci alla seconda collection
    hybrid_search.create_document(collection_names[0], doc_dolci)
    
    # aggiungo file md 1 alla terza collection
    hybrid_search.create_document(collection_names[1], doc_md_1)

    # aggiungo file md 3 alla seconda collection
    #hybrid_search.create_document(collection_names[1], doc_md_3)
    res = hybrid_search.hybrid_search(
        collection_name=collection_names[1],
        query="come funziona l'h3 header",
        num_results=num_results,
        ft_search_field="text",
    )
    #print("CHE COSA ABBIAMO SU H3_HEADER SINGLE SEARCH", res[0]["document"]["text"])

    res = hybrid_search.hybrid_search(
        collection_name=[collection_names[0],collection_names[1]],
        query="cosa abbiamo su yugioh",
        num_results=num_results,
        ft_search_field="text",
    )
    for elem in res:
        elem["document"]["embedding"] = ""
    #print("CHE COSA ABBIAMO SU DOLCI SINGLE SEARCH", res[0]["document"]["text"])
    #print("CHE COSA ABBIAMO SU YUGIOH SINGLE SEARCH", def_name, res)
    assert True


# def test_document_collection():
#     """
#     This function tests the document_collection function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     hybrid_search.create_collection(f"test_collection_{random_int}")
#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert collection_present

#     doc = Document(
#         preprocessing=Preprocessing(),
#         default_fields=DocumentInformations(file_id="test_file"),
#         file="https://css4.pub/2015/textbook/somatosensory.pdf",
#         fields={},
#     )
#     hybrid_search.create_document(f"test_collection_{random_int}", doc)
#     res = hybrid_search.hybrid_search(
#         collection_name=f"test_collection_{random_int}",
#         query="sensory information in receptors",
#         num_results=2,
#         ft_search_field="text",
#     )
#     assert res is not None

#     hybrid_search.delete_collection(f"test_collection_{random_int}")

#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert not collection_present


# def test_custom_collection():
#     """
#     This function tests the create_custom_collection function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     schema = {
#         "fields": [
#             {"name": ".*", "type": "auto"},
#             {"name": "text", "type": "string"},
#             {
#                 "name": "embedding",
#                 "type": "float[]",
#                 "embed": {
#                     "from": ["text"],
#                     "model_config": {
#                         "model_name": EmbeddingModel.MULTILINGUAL_E5_SMALL.value
#                     },
#                 },
#             },
#             {"name": "message_id", "type": "int32"},
#             {"name": "chat_id", "type": "int32"},
#             {"name": "role", "type": "string"},
#         ],
#         "metadata": {"embedding_model": EmbeddingModel.MULTILINGUAL_E5_SMALL.value},
#     }
#     hybrid_search.create_custom_collection(
#         f"test_collection_{random_int}", schema=schema
#     )
#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert collection_present

#     entry1 = Entry(
#         fields={
#             "text": "This is a test",
#             "message_id": 1,
#             "chat_id": 1,
#             "role": "user",
#         }
#     )
#     entry2 = Entry(
#         fields={
#             "text": "Ciao come stai?",
#             "message_id": 1,
#             "chat_id": 1,
#             "role": "user",
#         }
#     )

#     hybrid_search.create_entry(
#         f"test_collection_{random_int}",
#         entry1,
#     )
#     hybrid_search.create_entry(
#         f"test_collection_{random_int}",
#         entry2,
#     )

#     res = hybrid_search.hybrid_search(
#         collection_name=f"test_collection_{random_int}",
#         query="test",
#         num_results=1,
#         ft_search_field="text",
#     )
#     assert res is not None

#     hybrid_search.delete_collection(f"test_collection_{random_int}")

#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert not collection_present


# def test_supported_documents():
#     """
#     This function tests the supported_documents function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     supported_documents = hybrid_search.get_supported_documents()
#     assert isinstance(supported_documents, dict)
#     assert len(supported_documents.keys()) > 0
#     assert len(supported_documents["supportd_extensions"]) > 0
#     assert len(supported_documents["supported_mimetypes"]) > 0


# def test_already_existing_cutom_collection():
#     """
#     This function tests the already_existing_collection function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     schema = {
#         "fields": [
#             {"name": ".*", "type": "auto"},
#             {"name": "text", "type": "string"},
#             {
#                 "name": "embedding",
#                 "type": "float[]",
#                 "embed": {
#                     "from": ["text"],
#                     "model_config": {
#                         "model_name": EmbeddingModel.MULTILINGUAL_E5_SMALL.value
#                     },
#                 },
#             },
#             {"name": "message_id", "type": "int32"},
#             {"name": "chat_id", "type": "int32"},
#             {"name": "role", "type": "string"},
#         ],
#         "metadata": {"embedding_model": EmbeddingModel.MULTILINGUAL_E5_SMALL.value},
#     }
#     hybrid_search.create_custom_collection(
#         f"test_collection_{random_int}", schema=schema
#     )
#     try:
#         hybrid_search.create_custom_collection(
#             f"test_collection_{random_int}", schema=schema
#         )
#         exception_raised = False
#     except CollectionAlreadyExists:
#         exception_raised = True
#     except Exception as e:
#         print(e)
#         exception_raised = False
#     finally:
#         hybrid_search.delete_collection(f"test_collection_{random_int}")

#     assert exception_raised


# def test_already_existing_collection():
#     """
#     This function tests the already_existing_collection function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     hybrid_search.create_collection(f"test_collection_{random_int}")
#     try:
#         hybrid_search.create_collection(f"test_collection_{random_int}")
#         exception_raised = False
#     except CollectionAlreadyExists:
#         exception_raised = True
#     except Exception as e:
#         print(e)
#         exception_raised = False
#     finally:
#         hybrid_search.delete_collection(f"test_collection_{random_int}")

#     assert exception_raised


# def test_collection_not_existing():
#     """
#     This function tests the collection_not_existing function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     hybrid_search.create_collection(f"test_collection_{random_int}")
#     try:
#         hybrid_search.delete_collection(f"test_collection_{random_int + 1}")
#         exception_raised = False
#     except CollectionNotFound:
#         exception_raised = True
#     except Exception as e:
#         print(e)
#         exception_raised = False
#     finally:
#         hybrid_search.delete_collection(f"test_collection_{random_int}")
#     assert exception_raised


# def test_filters():
#     """
#     This function tests the filters function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     hybrid_search.create_collection(f"test_collection_{random_int}")

#     doc = Document(
#         preprocessing=Preprocessing(),
#         default_fields=DocumentInformations(file_id="test_file"),
#         file="https://css4.pub/2015/textbook/somatosensory.pdf",
#         fields={},
#     )
#     hybrid_search.create_document(f"test_collection_{random_int}", doc)
#     res = hybrid_search.hybrid_search(
#         collection_name=f"test_collection_{random_int}",
#         query="sensory information in receptors",
#         num_results=2,
#         ft_search_field="text",
#         filters=[Filter(field="start_page", operator=Operator.EQUAL, value=0)],
#     )
#     pages = [result["document"]["start_page"] for result in res]
#     assert res is not None
#     assert all(page == 0 for page in pages)

#     hybrid_search.delete_collection(f"test_collection_{random_int}")


# def test_semantic_chunks():
#     """
#     This function tests the document_collection function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     hybrid_search.create_collection(
#         f"test_collection_{random_int}", prev_next_chunks=True
#     )
#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert collection_present

#     doc = Document(
#         preprocessing=Preprocessing(chunk_mode=ChunkMod.SEMANTIC, semantic_thr_std=1.5),
#         default_fields=DocumentInformations(file_id="test_file"),
#         file="https://css4.pub/2015/textbook/somatosensory.pdf",
#         fields={},
#     )
#     hybrid_search.create_document(f"test_collection_{random_int}", doc)
#     start_time = time()
#     res = hybrid_search.hybrid_search(
#         collection_name=f"test_collection_{random_int}",
#         query="sensory information in receptors",
#         num_results=2,
#         ft_search_field="text",
#     )
#     end_time = time()
#     print(f"Search time: {end_time - start_time} seconds")
#     assert res is not None

#     hybrid_search.delete_collection(f"test_collection_{random_int}")

#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert not collection_present


# def test_reranker():
#     """
#     This function tests the document_collection function of the HybridSearch class
#     It assert that the object is created successfully without any exceptions
#     """

#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     hybrid_search.create_collection(f"test_collection_{random_int}")
#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert collection_present

#     doc = Document(
#         preprocessing=Preprocessing(chunk_mode=ChunkMod.SEMANTIC, semantic_thr_std=1.5),
#         default_fields=DocumentInformations(file_id="test_file"),
#         file="https://css4.pub/2015/textbook/somatosensory.pdf",
#         fields={},
#     )
#     hybrid_search.create_document(f"test_collection_{random_int}", doc)
#     start_time = time()
#     res = hybrid_search.hybrid_search(
#         collection_name=f"test_collection_{random_int}",
#         query="sensory information in receptors",
#         num_results=2,
#         ft_search_field="text",
#         rerank_model=ReRankModel.GTE_MULTILINGUAL_RERANKER_BASE,
#         rerank=True,
#     )
#     end_time = time()
#     print(f"Search time with Rerank: {end_time - start_time} seconds")
#     assert res is not None

#     hybrid_search.delete_collection(f"test_collection_{random_int}")

#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert not collection_present


# def test_remote_embedding():
#     """
#     This function tests the document_collection function of the HybridSearch class with a remote embedding model
#     """
#     random_int = randint(1, 10000)
#     hybrid_search = HybridSearch(api_key=demo_api_key)
#     hybrid_search.create_collection(
#         f"test_collection_{random_int}", model_name=EmbeddingModel.REMOTE_QWEN_3_8B
#     )
#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert collection_present

#     doc = Document(
#         preprocessing=Preprocessing(),
#         default_fields=DocumentInformations(file_id="test_file"),
#         file="https://css4.pub/2015/textbook/somatosensory.pdf",
#         fields={},
#     )
#     hybrid_search.create_document(f"test_collection_{random_int}", doc)
#     res = hybrid_search.hybrid_search(
#         collection_name=f"test_collection_{random_int}",
#         query="sensory information in receptors",
#         num_results=2,
#         ft_search_field="text",
#         rerank=True,
#         rerank_model=ReRankModel.REMOTE_QWEN_3_8B,
#     )
#     assert res is not None

#     hybrid_search.delete_collection(f"test_collection_{random_int}")

#     c = hybrid_search.get_all_collections()
#     collection_present = any(
#         collection["name"] == f"test_collection_{random_int}" for collection in c
#     )
#     assert not collection_present
