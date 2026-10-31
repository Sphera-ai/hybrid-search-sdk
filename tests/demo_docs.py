from __future__ import annotations

from enum import StrEnum

from hybridsearch import Document, DocumentInformations, HybridSearch, Preprocessing

"""
The standard demo document set shared by the integration tests.
"""


class FilesTestsUrls(StrEnum):
    """File urls to be used in the tests"""

    YUGIOH = "https://img.konami.com/yugioh/worldchampionship/2025/data/limitregulation-tcg.pdf"
    # was https://www.itaerferrarin.edu.it/pasw4/didattica/pallacanestro.pdf (404).
    # A 90-page FIP rules PDF and the full Wikipedia article were also tried:
    # both produce far too many chunks and flood the candidate pool of the
    # six-collection tests. The wikiversity intro is small and on-topic,
    # matching the scale of the original document.
    BASKET = "https://it.wikiversity.org/wiki/Introduzione_alla_pallacanestro"
    DOLCI = "https://comune.ravenna.it/wp-content/uploads/2025/09/Ricettario-per-dolci-momenti-insieme.pdf"
    # Raw content urls: blob/gist PAGES are HTML and get rate-limited by
    # GitHub after repeated server-side fetches, which made ingestion flaky
    H3_HEADER = "https://gist.githubusercontent.com/rt2zz/e0a1d6ab2682d2c47746950b84c0b6ee/raw/markdown-sample.md"
    INLINE_LINK = (
        "https://raw.githubusercontent.com/mxstbr/markdown-test-file/master/TEST.md"
    )
    INSTALLATION = "https://raw.githubusercontent.com/othneildrew/Best-README-Template/main/README.md"
    DRAWIO = "https://cidoc-crm.org/sites/default/files/Draw.io%20to%20Triples.pdf"
    # The original mobilesport.ch drill-sheet PDF is diagram-heavy: its
    # extracted text is mostly OCR noise and can never rank for sport
    # queries. The Wikipedia article is text-rich and stable.
    HOCKEY = "https://it.wikipedia.org/wiki/Hockey_su_ghiaccio"
    TENNIS = "https://www.sergvese.it/smba/files/tennis.pdf"
    VIDEOGAMES = "https://www.chateaudeprangins.ch/chateaudeprangins/medias/games/la-storia-dei-videogiochi-2021_it.pdf"


# Demo document set: file_id -> source url
DEMO_DOCS: dict[str, str] = {
    "test_file_yugioh": FilesTestsUrls.YUGIOH,
    "test_file_dolci": FilesTestsUrls.DOLCI,
    "test_file_md_1": FilesTestsUrls.H3_HEADER,
    "test_file_md_3": FilesTestsUrls.INSTALLATION,
    "test_drawio": FilesTestsUrls.DRAWIO,
    "test_basket": FilesTestsUrls.BASKET,
    "test_tennis": FilesTestsUrls.TENNIS,
    "test_videogames": FilesTestsUrls.VIDEOGAMES,
    "test_hockey": FilesTestsUrls.HOCKEY,
    "test_inline": FilesTestsUrls.INLINE_LINK,
}


def setup_document(input_file_id: str, input_file: str) -> Document:
    """Setup a Document instance for create_document

    Args:
        input_file_id (str): The file_id to assign to the document
        input_file (str): The url of the document

    Returns:
        Document: Document instance
    """
    return Document(
        preprocessing=Preprocessing(),
        default_fields=DocumentInformations(file_id=input_file_id),
        file=input_file,
        fields={},
    )


def ingest_documents(
    hs: HybridSearch, collection_name: str, file_ids: list[str]
) -> None:
    """Ingest the demo documents with the given file_ids into a collection

    Args:
        hs (HybridSearch): The client for the running microservice
        collection_name (str): Name of the collection to ingest into
        file_ids (list[str]): The file_ids of the demo documents to ingest,
            must be keys of DEMO_DOCS
    """
    for file_id in file_ids:
        hs.create_document(collection_name, setup_document(file_id, DEMO_DOCS[file_id]))
