# HybridSearch Class Documentation

## Overview

The `HybridSearch` class provides a Python interface to interact with a microservice powered by Typesense and FastAPI. It allows users to manage collections, create documents, and perform advanced search operations such as semantic and hybrid searches.

---

## Initialization

### `__init__(self, api_key: str, url: str = "http://localhost", port: int = 8000)`

Initializes the `HybridSearch` class.

- **Parameters:**
  - `api_key` (str, required): API key to access the microservice.
  - `url` (str, optional): Base URL of the microservice. Default is `"http://localhost"`.
  - `port` (int, optional): Port of the microservice. Default is `8000`.

- **Example:**

```python
# Initialize the HybridSearch client
search_client = HybridSearch(api_key="your_api_key")
```

---

## Methods

### `check_api_key(self)`

Validates the provided API key.

- **Returns:**
  - `bool`: `True` if the API key is valid, `False` otherwise.

- **Example:**

```python
# Check API key validity
is_valid = search_client.check_api_key()
```

---

### Collection Management

#### `create_custom_collection(self, collection_name: str, schema: dict)`

Creates a custom collection with a user-defined schema.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `schema` (dict, required): Schema defining the collection fields.

- **Returns:**
  - `dict`: Response from the API.

- **Raises:**
  - `InvalidApiKey`: If the API key is invalid.
  - `CollectionAlreadyExists`: If the collection already exists.
  - `ServerError`: For other server-side errors.

- **Example:**

```python
schema = {
    "fields": [
        {"name": "text", "type": "string"},
        {"name": "embedding", "type": "float[]"},
    ]
}
response = search_client.create_custom_collection("example_collection", schema)
```

---

#### `create_collection(self, collection_name: str, model_name: EmbeddingModel = EmbeddingModel.MULTILINGUAL_E5_SMALL)`

Creates a general-purpose collection with a default schema.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `model_name` (EmbeddingModel, optional): Embedding model to use. Default is `MULTILINGUAL_E5_SMALL`.

- **Returns:**
  - `dict`: Response from the API.

- **Example:**

```python
response = search_client.create_collection("example_collection")
```

---

#### `get_collection(self, collection_name: str)`

Retrieves information about a specific collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.

- **Returns:**
  - `dict`: Collection details.

- **Raises:**
  - `CollectionNotFound`: If the collection does not exist.

- **Example:**

```python
collection_info = search_client.get_collection("example_collection")
```

---

#### `get_all_collections(self)`

Retrieves information about all collections.

- **Returns:**
  - `list[dict]`: List of collections.

- **Example:**

```python
collections = search_client.get_all_collections()
```

---

#### `delete_collection(self, collection_name: str)`

Deletes a collection by name.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.

- **Returns:**
  - `bool`: `True` if the collection was successfully deleted.

- **Example:**

```python
is_deleted = search_client.delete_collection("example_collection")
```

---

### Document Management

#### `create_document(self, collection_name: str, document: Document)`

Adds a document to a collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `document` (Document, required): Document to add.

- **Returns:**
  - `dict`: Response from the API.

- **Example:**

```python
document = Document(field1="value1", field2="value2")
response = search_client.create_document("example_collection", document)
```

---

#### `delete_documents(self, collection_name: str, document_id: str | None = None, filter_by: str | None = None)`

Deletes documents from a collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `document_id` (str, optional): ID of the document to delete.
  - `filter_by` (str, optional): Filter to match documents for deletion.

- **Returns:**
  - `bool`: `True` if the documents were successfully deleted.

- **Example:**

```python
is_deleted = search_client.delete_documents("example_collection", document_id="123")
```

---

### Search Operations

#### `semantic_search(self, collection_name: str, query: str, num_results: int, rerank: bool = False, rerank_model: ReRankModel = ReRankModel.BGE_RERANKER_LARGE, filters: list[Filter] | None = None)`

Performs a semantic search on a collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `query` (str, required): Search query.
  - `num_results` (int, required): Number of results to return.
  - `rerank` (bool, optional): Whether to rerank results. Default is `False`.
  - `rerank_model` (ReRankModel, optional): Rerank model to use. Default is `BGE_RERANKER_LARGE`.
  - `filters` (list[Filter], optional): Filters to apply.

- **Returns:**
  - `list[dict]`: Search results.

- **Example:**

```python
results = search_client.semantic_search("example_collection", "example query", 5)
```

---

#### `hybrid_search(self, collection_name: str, query: str, num_results: int, ft_search_field: str, rerank: bool = False, rerank_model: ReRankModel = ReRankModel.BGE_RERANKER_LARGE, filters: list[Filter] | None = None)`

Performs a hybrid search combining semantic and full-text search.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `query` (str, required): Search query.
  - `num_results` (int, required): Number of results to return.
  - `ft_search_field` (str, required): Field for full-text search.
  - `rerank` (bool, optional): Whether to rerank results. Default is `False`.
  - `rerank_model` (ReRankModel, optional): Rerank model to use. Default is `BGE_RERANKER_LARGE`.
  - `filters` (list[Filter], optional): Filters to apply.

- **Returns:**
  - `list[dict]`: Search results.

- **Example:**

```python
results = search_client.hybrid_search("example_collection", "example query", 5, "title")
```

---

### Model Information

#### `get_model_names(self)`

Retrieves available embedding models.

- **Returns:**
  - `list[str]`: List of model names.

- **Example:**

```python
models = search_client.get_model_names()
```

---

#### `get_rerank_model_names(self)`

Retrieves available rerank models.

- **Returns:**
  - `list[str]`: List of rerank model names.

- **Example:**

```python
rerank_models = search_client.get_rerank_model_names()
```

---

#### `get_supported_documents(self)`

Retrieves supported document formats.

- **Returns:**
  - `list[str]`: List of supported formats.

- **Example:**

```python
supported_docs = search_client.get_supported_documents()
```
