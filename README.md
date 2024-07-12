# Hybrid Search SDK

The Hybrid Search SDK is a Python library that provides an interface to interact with the Typesense search engine. It allows you to perform both semantic search and hybrid search operations.

## Installation

To install the Hybrid Search SDK, you can use pip:

```shell
pip install git+https://github.com/Aidia-srl/hybrid-search-sdk.git@dev
```

## Usage

To use the Hybrid Search SDK, you need to import the `HybridSearch` class from the `hybridsearch.hybridsearch` module:

```python
from hybridsearch.hybridsearch import HybridSearch
```
For more detailed documentation see `src/readme.md`

## Definitions

### Collection

In Typesense, a collection is a logical grouping of documents. It represents a searchable entity, such as a product catalog or a knowledge base. You can createand delete collections using the Hybrid Search SDK.

### Schema
A schema defines the structure of the documents within a collection. It specifies the fields and their data types. You can define a schema for a collection using the Hybrid Search SDK.

### Query

A query is a request for information from the search engine. With the Hybrid Search SDK, you can construct and execute queries to retrieve relevant documents from a collection. You can specify search keywords, filters, sorting criteria, and other parameters to customize the query.

For detailed usage examples and API reference, please refer to the [Hybrid Search SDK documentation](https://github.com/Aidia-srl/hybrid-search-sdk/tree/dev/src).
