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
# Initialize the search client
search_client = HybridSearch(api_key="your_api_key")
```
## Methods

### `check_api_key(self)`

Checks if the provided API key is valid.

- **Raises:**
  - `Exception`: If the API key is invalid.

```python
# Check API key validity
search_client.check_api_key()
```

- **Example:**
### `get_all_collections(self)`
Returns a list of dict containing the informations of the database.

- **Returns:**
```
  {
    "status": int,
    "description": list[dict] | str   # list of collection or error string
  }
```

- **Example:**
```python
# Get all collections
status_code, collections = search_client.get_all_collections()
```
### `get_collection(self, collection_name)`

Returns the collection with the given name.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.

- **Returns:**
```
  {
    "status": int,
    "description": dict | str   # Collection or error string
  }
```
- **Example:**
```python
# Get a specific collection
status_code,collection_info = search_client.get_collection("example_collection")
```
### `create_custom_collection(self, embedding_field, model_name, schema)`
Creates a custom collection in the database.

- **Parameters:**
  - `embedding_field` (str, required): field to embed using the model.
  - `model_name` (str, required): model_name to be used to embed the field.
  - `schema` (dict, required): Schema of the collection.

models names can be retrieved using the function `get_model_name()`

- **Returns:**
```
  {
    "status": int,
    "description": dict | str   # list of collection or error string
  }
```
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

By default the field named `text` will be used to be embedded.

- **Returns:**
```
  {
    "status": int,
    "description": dict | str   # list of collection or error string
  }
```
- **Example:**
```python
status_code, created_collection = search_client.create_collection(test)

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
```
  {
    "status": int,
    "description": str
  }
```
- **Example:**
```python
# Delete a collection
deleted_collection = search_client.delete_collection("example_collection")
```
### `create_document(self, collection_name: str, schema: dict)`

Creates a document in the specified collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `schema` (dict, required): schema of the document to be inserted.

- **Returns:**
```{"status": int,"description": str}```

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

### `create_document_from_file(self, collection_name: str,file_path:str, field:str, chunk_size:int, overlap_size:int, mode=str)`

Creates a document in the specified collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `file_path` (str, required): Path of the pdf file.
  - `field` (str, required): Field where to insert the the embedding
  - `chunk_mode` (str): "naive" or "semantic", default: "naive".
  - `chunk_size` (int): chunk size, default 1000.
  - `overlap_size`(int): Overlap size to have more, default 200.
  - `mode`(str):  mode should be 'words' or 'characters', defualt: "words".
  - `model_to_semantic_chunk`(str):  model used to execute semanti chunking. Default "paraphrase-multilingual-MiniLM-L12-v2"


- **Returns:**
``` {"status": int, description": str } ```

- **Example:**
```python
status_code,created_document = search_client.create_document("example_collection","./test.pdf","text")

```

### `semantic_search(self, collection_name: str, query: str, num_results: int, rerank:bool, rerank_model:str)`

Performs a semantic search on the specified collection.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `query` (str, required): Query to search.
  - `num_results` (int, required): Number of results to return.
  - `rerank` (bool, optional): If true it execute the reranking of the resultsm using the selected rerank model. Default False.
  - `rerank_model` (str, optional): Name of the rerank model, if rerank is true then this paramter is required.

Available rerank models can be retrieved using the function `get_rerank_model_name`

- **Returns:**
```
  {
    "status": int,
    "description": list[dict] | str   # list of results or error string
  }
```
- **Example:**
```python
# Perform a semantic search
status_code, semantic_search_results = search_client.semantic_search("example_collection", "example query", 5)
```

### `hybrid_search(self, collection_name: str, query: str, num_results: int, field: str, rerank:bool, rerank_model:str)`

Performs a hybrid search on the specified collection, combining semantic search and full-text search on user-specified fields.

- **Parameters:**
  - `collection_name` (str, required): Name of the collection.
  - `query` (str, required): Query to search.
  - `num_results` (int, required): Number of results to return.
  - `field` (str, required): Fields to search.
  - `rerank` (bool, optional): If true it execute the reranking of the resultsm using the selected rerank model. Default False.
  - `rerank_model` (str, optional): Name of the rerank model, if rerank is true then this paramter is required.

- Available rerank models can be retrieved using the function `get_rerank_model_name`
- If you want to select multiple field for the hybrid-search, seperates the fields using a comma. `field1, field2, ..`

- **Returns:**
```
  {
    "status": int,
    "description": list[dict] | str   # list of results or error string
  }
```
- **Example:**
```python
# Perform a hybrid search
status_code, hybrid_search_results = search_client.hybrid_search("example_collection", "example query", 5, "title")

```

### `get_model_name(self)`
Returns the models name used to do embedding.

- **Returns:**
```
  {
    "status": int,
    "description": list[dict] | str   # list of results or error string
  }
```
- **Example:**
```python
# Get schema attributes
model_names = search_client.get_model_name()
```

### `get_rerank_model_name(self)`
Returns the models name used to do rerank.

- **Returns:**
```
  {
    "status": int,
    "description": list[dict] | str   # list of results or error string
  }
```
- **Example:**
```python
# Get schema attributes
model_names = search_client.get_model_name()
```


# Preprocessing Documentation

## Method
### `process_pdf_to_chunks(self, pdf_path: str, chunk_size: int, overlap_size:int)`

This function creates chunks of text starting from a pdf given in input

- **Parameter**
  - `pdf_path`: path of the document to chunk
  - `chunk_size`:  chunk size (default:1000)
  - `overlap_size`: overlap size, to give more
- **Returns:**
  - `list[dict]`:
  ```
  [{
    "page": int,
    "start_line": int,
    "end_line":int,
    "text": str
  },]
  ```

- **Example:**
```python
# Get schema attributes
model_names = search_client.process_pdf_to_chunks("example_collection", "./test.pdf", "text", 1000, 200)
```
