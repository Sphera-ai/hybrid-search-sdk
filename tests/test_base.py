from __future__ import annotations

from hybridsearch.hybridsearch import HybridSearch

"""
This file contains the tests for the base class HybridSearch
"""


# TODO: Unit tests and integration tests


def test_init():
    """
    This function tests the __init__ function of the HybridSearch class
    It assert that the object is created successfully without any exceptions
    """

    HybridSearch(api_key="xyz")
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
