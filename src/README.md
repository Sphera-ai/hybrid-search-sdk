# HybridSearch Class Documentation

## Overview

The `HybridSearch` class provides a convenient interface to interact with a microservice powered by Typesense and FastAPI. This class enables users to perform various operations such as checking API keys, managing collections, creating documents, and performing searches (semantic and hybrid) within the database.

## Initialization

### `__init__(self, api_key: str, url: str = "localhost", port: int = 8000)`

Initializes the `HybridSearch` class.

- **Parameters:**
  - `api_key` (str, required): API key to access the database.
  - `url` (str, optional): URL of the microservice. Default is "localhost".
  - `port` (int, optional): Port of the microservice. Default is 8000.

- **Example:**
```python
# Check API key validity
search_client.check_api_key()
```
## Methods

### `check_api_key(self)`

Checks if the provided API key is valid.

- **Raises:**
  - `Exception`: If the API key is invalid.

- **Example:**
```python
# Initialize the search client
search_client = HybridSearch(api_key="your_api_key")
```
### `get_all_collections(self)`

Returns all the collections in the database.

- **Returns:**
  - `json`: Response with all the collections.

- **Example:**
```python
# Get all collections
collections = search_client.get_all_collections()
```
### `get_collection(self, collection_name)`

Returns the collection with the given name.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.

- **Returns:**
  - `json`: Response with the collection information.
- **Example:**
```python
# Get a specific collection
collection_info = search_client.get_collection("example_collection")
```
### `create_custom_collection(self, schema)`
Creates a custom collection in the database.

- **Parameters:**
  - `embedding_field` (str, required): field to embed using the model.
  - `model_name` (str, required): model_name to be used to embed the field.
  - `schema` (json, required): Schema of the collection.

- **Returns:**
  - `json`: Response of the created collection.
- **Example:**
```python
# Create a custom collection
schema = {
  "name": "text",     # name of the collection
  "fields": [         # one of the field name should match with embedding field!
    {"name": "text1", "type": "string"},
    {"name": "text2", "type": "int"}
  ]
}

created_collection = search_client.create_custom_collection(schema)
```


### `create_collection(self, collection_name)`
Creates a general collection in the database.

- **Parameters:**
  - `collection_name` (str, required): Collection name.

- **Returns:**
  - `json`: Response of the created collection.
- **Example:**
```python
created_collection = search_client.create_collection(test)

# Example of collection that will be created
schema = {
        "name": test,
        "fields": [
            {"name": ".*", "type": "auto"},
            {"name": "text", "type": "string"},
            {
                "name": "embedding",
                "type": "float[]",
                "embed": {
                    "from": ["text"],
                    "model_config": {"model_name": "ts/e5-small"},
                },
            },
        ]
  }
```

### `delete_collection(self, collection_name)`

Deletes the collection with the given name.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.

- **Returns:**
  - `json`: Response of the deletion operation.
- **Example:**
```python
# Delete a collection
deleted_collection = search_client.delete_collection("example_collection")
```
### `create_document(self, collection_name: str, document: str)`

Creates a document in the specified collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `schema` (dict, required): schema of the document to be inserted.

- **Returns:**
  - `json`: Response of the document creation.
- **Example:**
```python
# Create a document
schema = {
    "field_name": "example 1",
    "field_name_2": "example 2",
    "field_name_3": "example 2",
}
created_document = search_client.create_document("example_collection", document)
```

### `create_document_from_file(self, collection_name: str, document: str)`

Creates a document in the specified collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `file_path` (str, required): Path of the pdf file.
  - `field` (str, required): Field where to insert the the embedding
  - `chunk_size` (int, 1000): chunk size
  - `overlap_size`(int, 200), Overlap size to

- **Returns:**
  - `json`: Response of the document creation.
- **Example:**
```python
created_document = search_client.create_document("example_collection", document)

```

### `semantic_search(self, collection_name: str, query: str, num_results: int)`

Performs a semantic search on the specified collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `query` (str, required): Query to search.
  - `num_results` (int, required): Number of results to return.

- **Returns:**
  - `json`: Response of the semantic search.
- **Example:**
```python
# Perform a semantic search
semantic_search_results = search_client.semantic_search("example_collection", "example query", 5)
```
### `hybrid_search(self, collection_name: str, query: str, num_results: int, field: str)`

Performs a hybrid search on the specified collection, combining semantic search and full-text search on user-specified fields.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `query` (str, required): Query to search.
  - `num_results` (int, required): Number of results to return.
  - `field` (str, required): Fields to search.

- **Returns:**
  - `json`: Response of the hybrid search.
- **Example:**
```python
# Perform a hybrid search
hybrid_search_results = search_client.hybrid_search("example_collection", "example query", 5, "title")

```
### `get_schema_attributes(self, collection_name)`

Returns the schema attributes of an existing collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.

- **Returns:**
  - `json`: Response with the schema attributes of the collection.

- **Example:**
```python
# Get schema attributes
schema_attributes = search_client.get_schema_attributes("example_collection")
```
### `get_model_name(self)`

Returns the models name used to do embedding.


- **Returns:**
  - `json`: Response with the list of all the embeddings

- **Example:**
```python
# Get schema attributes
model_names = search_client.get_model_name()
```

### `create_document_from_file(self, collection_name: str, file_path: str, field: string, chunk_size: int, overlap_size:int)`

Create document starting from a pdf.
- **Parameters**
    - `collection_name` (str, required): Name of the collection.
    - `file_path`: str,  Path to the pdf file
    - `chunk_size`: int,Size of the chunks
    - `overlap_size`: int, Size of the overlap between chunks
- **Returns:**
  - `int`: Status code of the response

- **Example:**
```python
# Get schema attributes
model_names = search_client.create_document_from_file("example_collection", "./test.pdf", "text", 1000, 200)
```


# Preprocessing Documentation

## Method
### `preprocess_text(self, pdf_path: str, chunk_size: int, overlap_size:int)`

This function creates chunks of text starting from a pdf given in input

- **Parameter**
  - `pdf_path`: path of the document to chunk
  - `chunk_size`:  chunk size (default:1000)
  - `overlap_size`: overlap size, to give more
- **Returns:**
  - `string[]`: List of chunks

- **Example:**
```python
# Get schema attributes
model_names = search_client.create_document_from_file("example_collection", "./test.pdf", "text", 1000, 200)
```
