from __future__ import annotations

from asyncio.log import logger

import requests as req  # type: ignore

from .exceptions import (
    CollectionAlreadyExists,
    CollectionNotFound,
    InvalidApiKey,
    InvalidRequest,
    ServerError,
)
from .models import Document, EmbeddingModel, Entry, Filter, ReRankModel


class HybridSearch:
    def __init__(self, api_key: str, url: str = "http://localhost", port: int = 8002):
        """This class is used to interact with the microservice typesense+fastapi

        Args:
            api_key (str): API key to access the database
            url (str, optional): URL of the microservice. Defaults to "localhost".
            port (int, optional): Port of the microservice. Defaults to 8002.
        """

        self.api_key = api_key
        self.port = port
        self.url = url

    def check_api_key(self):
        """
        This function checks if the API key is valid.
        Returns true if the API key is valid.
        """
        status_code = req.get(
            f"{self.url}:{self.port}/api-key",
            headers={"x-typesense-api-key": self.api_key},
        ).status_code

        if status_code == 500:
            logger.error("Internal server error")
            return False
        if status_code != 200:
            logger.error("Invalid API key")
            return False

        logger.info("API key is valid")
        return True

    def create_custom_collection(self, collection_name: str, schema: dict):
        """This function creates a collection in the database with the provided schema.

        Example schema:
        ```json
        {
            "fields": [
                {"name": ".*", "type": "auto"},
                {"name": "text", "type": "string"},
                {
                    "name": "embedding",
                    "type": "float[]",
                    "embed": {
                        "from": ["text"],
                        "model_config": {"model_name": "ts/multilingual-e5-small"},
                    },
                },
                {"name": "page", "type": "int32"},
                {"name": "start_sentence", "type": "int32"},
                {"name": "end_sentence", "type": "int32"},
                {"name": "entry_id", "type": "string"}
            ]
        }
        ```

        Args:
            collection_name (str, required): Name of the collection
            schema (dict, required): schema of the fields

        Returns:
            json: response of the created collection
        """

        response = req.post(
            f"{self.url}:{self.port}/create-collection-custom",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
            },
            json=schema,
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 409:
            logger.error("Collection already exists")
            raise CollectionAlreadyExists(collection_name=collection_name)

        if response.status_code == 500:
            logger.error("Internal server error")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def create_collection(
        self,
        collection_name: str,
        model_name: EmbeddingModel = EmbeddingModel.MULTILINGUAL_E5_SMALL,
        prev_next_chunks: bool = False,
    ):
        """This function creates a document collection in the database,
        with a text field which is embedded with the model specified or the default ts/multilingual-e5-small.

        The default collections is created with the following schema:

        {
            id: string
            embedding: float,
            text: string,
            start_sentence: int,
            end_sentence: int,
            page: int,
            file_id: string
        }

        If prev_next_chunks is True, the schema will be:
        {
            id: string
            embedding: float,
            text: string,
            start_sentence: int,
            end_sentence: int,
            page: int,
            file_id: string
            prev_chunk: string not indexed
            next_chunk: string not indexed
        }

        Args:
            collection_name (str, required): Name of the collection
            model_name (EmbeddingModel): The model to use for embeddings. Defaults to EmbeddingModel.MULTILINGUAL_E5_SMALL.
            prev_next_chunks (bool): Whether to include previous and next chunks texts in the schema. Defaults to False.

        Returns:
            response: dict

        Raises:

        """
        response = req.post(
            f"{self.url}:{self.port}/create-collection",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
                "model_name": model_name.value,
                "prev_next_chunks": prev_next_chunks,
            },
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 409:
            logger.error("Collection already exists")
            raise CollectionAlreadyExists(collection_name=collection_name)

        if response.status_code == 500:
            logger.error("Internal server error")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def get_collection(self, collection_name: str):
        """This function returns the collection with the given name

        Args:
            collection_name (str): Name of the collection

        Returns:
            json: response with the collection information

        Raises:
            CollectionNotFound: If the collection is not founda
            InvalidApiKey: If the API key is invalid
        """
        response = req.get(
            f"{self.url}:{self.port}/collections/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")
        elif response.status_code == 404:
            raise CollectionNotFound("No collection found")
        elif response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def get_all_collections(self):
        """This function returns all the collections in the database

        Returns:
            json: response with a list of json containing information of the collections

        Raises:
            CollectionNotFound: If the collection is not found
            InvalidApiKey: If the API key
        """
        response = req.get(
            f"{self.url}:{self.port}/collections",
            headers={"x-typesense-api-key": self.api_key},
        )
        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")
        elif response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def create_document(
        self,
        collection_name: str,
        document: Document,
    ):
        """This function creates a document in the specified collection.
        The collection must be created before calling this function.
        The collection must be a "document" collection.

        Args:
            collection_name (str): Name of the collection
            schema (dict): schema of the preprocesseing and pdf urls

        Returns:
            json: response
        """

        response = req.post(
            f"{self.url}:{self.port}/create-document",
            headers={"x-typesense-api-key": self.api_key},
            params={"collection_name": collection_name},
            json=document.model_dump(),
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 404:
            logger.error("Collection not found")
            raise CollectionNotFound(collection_name)

        if response.status_code == 406:
            logger.error("Invalid request")
            raise InvalidRequest("Invalid request")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def create_entry(self, collection_name: str, entry: Entry):
        """This function creates an entry in the specified collection.

        Args:
            name (str): The collection name
            entry (Entry): The entry to be created. It contains the field values.

        Returns:
            json: response
        """
        response = req.post(
            f"{self.url}:{self.port}/create-entry",
            headers={"x-typesense-api-key": self.api_key},
            params={"collection_name": collection_name},
            json=entry.model_dump(),
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 404:
            logger.error("Collection not found")
            raise CollectionNotFound(collection_name)

        if response.status_code == 406:
            logger.error("Invalid request")
            raise InvalidRequest("Invalid request")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def delete_collection(self, collection_name: str):
        """This function deletes the collection with the given name.

        Args:
            collection_name (str): Name of the collection

        Returns:
            json: response
        """
        response = req.delete(
            f"{self.url}:{self.port}/collections-delete/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 404:
            logger.error("Collection not found")
            raise CollectionNotFound(collection_name)

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return True

    def delete_documents(
        self,
        collection_name: str,
        document_id: str | None = None,
        filter_by: str | None = None,
    ):
        """This function deletes a document in the specified collection.

        Args:
            collection_name (str): Name of the collection.
            document_id (str): Id of the document.
            filter_by (str): Filter that matches the documents to delete.

        Returns:
            json: response
        """
        response = req.delete(
            f"{self.url}:{self.port}/delete-documents",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
                "document_id": document_id,
                "filter_by": filter_by,
            },
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 404:
            logger.error("Collection not found")
            raise CollectionNotFound(collection_name)

        if response.status_code == 406:
            logger.error("Invalid request")
            raise InvalidRequest("Invalid request")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return True

    def delete_entries(
        self,
        collection_name: str,
        entry_id: str | None = None,
        filter_by: str | None = None,
    ):
        """This function deletes an entry in the specified collection.

        Args:
            collection_name (str): Name of the collection.
            entry_id (str): Id of the entry.
            filter_by (str): Filter that matches the entries to delete.

        Returns:
            json: response
        """
        response = req.delete(
            f"{self.url}:{self.port}/delete-entries",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
                "entry_id": entry_id,
                "filter_by": filter_by,
            },
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 404:
            logger.error("Collection not found")
            raise CollectionNotFound(collection_name)

        if response.status_code == 406:
            logger.error("Invalid request")
            raise InvalidRequest("Invalid request")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return True

    def semantic_search(
        self,
        collection_name: str,
        query: str,
        num_results: int,
        rerank: bool = False,
        rerank_model: ReRankModel = ReRankModel.GTE_MULTILINGUAL_RERANKER_BASE,
        filters: list[Filter] | None = None,
    ):
        """This function performs a semantic search on the specified collection.

        Args:
            collection_name (str): collection name. Can be a comma-separated list of collections
            query (str): Query to search
            num_results (int): Number of results
            rerank (bool, optional): If True, rerank the results. Defaults to False.
            rerank_model (ReRankModel): Model to rerank the results. Defaults to ReRankModel.GTE_MULTILINGUAL_RERANKER_BASE.
            filters (list[Filter], optional): List of filters to apply. Defaults to None.

        Returns:
            json: response
        """
        if filters is None or len(filters) == 0:
            response = req.post(
                f"{self.url}:{self.port}/collections-semanticsearch",
                headers={"x-typesense-api-key": self.api_key},
                params={
                    "collection_name": collection_name,
                    "query": query,
                    "num_results": num_results,
                    "rerank": rerank,
                    "rerank_model": rerank_model.value,
                },
            )
        else:
            response = req.post(
                f"{self.url}:{self.port}/collections-semanticsearch",
                headers={"x-typesense-api-key": self.api_key},
                params={
                    "collection_name": collection_name,
                    "query": query,
                    "num_results": num_results,
                    "rerank": rerank,
                    "rerank_model": rerank_model.value,
                },
                json=[f.model_dump() for f in filters],
            )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 404:
            logger.error("Collection not found")
            raise CollectionNotFound(collection_name)

        if response.status_code == 406:
            logger.error("Invalid request")
            raise InvalidRequest("Invalid request")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def hybrid_search(
        self,
        collection_name: str,
        query: str,
        num_results: int,
        ft_search_field: str,
        rerank: bool = False,
        rerank_model: ReRankModel = ReRankModel.GTE_MULTILINGUAL_RERANKER_BASE,
        filters: list[Filter] | None = None,
    ):
        """This function performs a hybrid search on the collection, combining semantic search and full text search
        on a field or fields choose by the user

        Args:
            collection_name (str): collection name. Can be a comma-separated list of collections
            query (str): Query to search
            num_results (int): Number of results
            ft_search_field (str): field to execute the full text search
            rerank (bool, optional): If True, rerank the results. Defaults to False.
            rerank_model (ReRankModel): Model to rerank the results. Defaults to ReRankModel.GTE_MULTILINGUAL_RERANKER_BASE.
            filters (list[Filter], optional): List of filters to apply. Defaults to None.

        Returns:
            response: json
        """
        if filters is None or len(filters) == 0:
            response = req.post(
                f"{self.url}:{self.port}/collections-hybridsearch",
                headers={"x-typesense-api-key": self.api_key},
                params={
                    "collection_name": collection_name,
                    "query": query,
                    "num_results": num_results,
                    "search_field": ft_search_field,
                    "rerank": rerank,
                    "rerank_model": rerank_model.value,
                },
            )
        else:
            response = req.post(
                f"{self.url}:{self.port}/collections-hybridsearch",
                headers={"x-typesense-api-key": self.api_key},
                params={
                    "collection_name": collection_name,
                    "query": query,
                    "num_results": num_results,
                    "search_field": ft_search_field,
                    "rerank": rerank,
                    "rerank_model": rerank_model.value,
                },
                json=[f.model_dump() for f in filters],
            )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code == 404:
            logger.error("Collection not found")
            raise CollectionNotFound(collection_name)

        if response.status_code == 406:
            logger.error("Invalid request")
            raise InvalidRequest("Invalid request")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def get_model_names(self):
        """This function returns the model names that can be used to embed.

        Returns:
            response: json with a list of the models used for embedding.
        """
        response = req.get(
            f"{self.url}:{self.port}/embedding_models",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def get_rerank_model_names(self):
        """This function returns the model names that can be used to rerank.

        Returns:
            response: json with a list of the models used for embedding
        """
        response = req.get(
            f"{self.url}:{self.port}/rerank_models",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()

    def get_supported_documents(self):
        """This function returns the supported documents that can be added to a document collection.

        Returns:
            response: json with a list of the supported document formats
        """
        response = req.get(
            f"{self.url}:{self.port}/supported_documents",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 401:
            logger.error("Invalid API key")
            raise InvalidApiKey("Invalid API key")

        if response.status_code != 200:
            logger.error("Error calling the API")
            error = response.json()["detail"]
            raise ServerError(error["error_type"], error["strerror"])

        return response.json()
