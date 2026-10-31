from __future__ import annotations

import logging
from random import randint

import pytest
from hybridsearch import EmbeddingModel, HybridSearch

from tests.demo_docs import DEMO_DOCS, ingest_documents

"""
Shared fixtures for the integration tests.

These tests run against a live microservice (see hybrid-search/docker-compose.yaml)
and need network access to fetch the demo documents.
"""

logger = logging.getLogger(__name__)

demo_api_key = "test"


@pytest.fixture(scope="module")
def hs() -> HybridSearch:
    """Client for the running microservice (stateless, shared per module)."""
    return HybridSearch(api_key=demo_api_key)


@pytest.fixture
def collection_factory(hs: HybridSearch):
    """Create test collections that are automatically deleted on teardown."""
    created: list[str] = []

    def _create(
        model_name: EmbeddingModel = EmbeddingModel.MULTILINGUAL_E5_SMALL,
        prev_next_chunks: bool = False,
    ) -> str:
        name = f"test_collection_{randint(1000000, 100000000)}"
        hs.create_collection(
            name, model_name=model_name, prev_next_chunks=prev_next_chunks
        )
        created.append(name)
        return name

    yield _create

    for name in created:
        try:
            hs.delete_collection(name)
        except Exception:  # noqa: PERF203 - one failed cleanup must not block the others
            logger.warning("Could not clean up collection %s", name)


@pytest.fixture(scope="module")
def large_internal_collection(hs: HybridSearch):
    """A single built-in-model collection holding the full demo document set.

    Shared by the regression tests that need well over 10 chunks in one
    collection (Typesense used to cap results at its default per_page of 10).
    """
    name = f"test_collection_{randint(1000000, 100000000)}"
    hs.create_collection(name)
    ingest_documents(hs, name, list(DEMO_DOCS))
    yield name
    try:
        hs.delete_collection(name)
    except Exception:
        logger.warning("Could not clean up collection %s", name)
