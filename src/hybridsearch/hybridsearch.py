from __future__ import annotations

import json
from asyncio.log import logger

import requests as req

from .exceptions import CollectionNotFound, GenericError, InvalidApiKey
from .models import Document


class HybridSearch:
    def __init__(self, api_key: str, url: str = "http://localhost", port: int = 8000):
        """This class is used to interact with the microservice typesense+fastapi

        Args:
            api_key (str): API key to access the database
            url (str, optional): URL of the microservice. Defaults to "localhost".
            port (int, optional): Port of the microservice. Defaults to 8000.
        """

        self.api_key = api_key
        self.port = port
        self.url = url

    def check_api_key(self):
        """
        This function checks if the API key is valid
        returns true if the API key is valid

        """
        status_code = req.get(
            f"{self.url}:{self.port}/api-key",
            headers={"x-typesense-api-key": self.api_key},
        ).status_code

        if status_code == 500:
            logger.error("Internal server error")
        if status_code != 200:
            logger.error("Invalid API key")

        logger.info("API key is valid")
        return True

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
            raise InvalidApiKey("Invalid API key")
        elif response.status_code == 404:
            raise CollectionNotFound("No collection found")

        return response.json()

    def get_collection(self, collection_name):
        """This function returns the collection with the given name

        Args:
            collection_name (str): Name of the collection

        Returns:
            json: response with the collection information

        Raises:
            CollectionNotFound: If the collection is not founda
            InvalidApiKey: If the API key

        """
        response = req.get(
            f"{self.url}:{self.port}/collections/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 401:
            raise InvalidApiKey("Invalid API key")
        elif response.status_code == 404:
            raise CollectionNotFound("No collection found")

        return response.json()

    def create_custom_collection(self, collection_name: str, schema: dict):
        """This function creates a collection in the database

        Args:
            collection_name (str, required): Name of the collection
            schema (dict, required): schema of the fields

        Returns:
            json: response of the created collection

        Raises:

        """

        response = req.post(
            f"{self.url}:{self.port}/create-collection-custom",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
            },
            json=schema,
        )

        # execptions

        return response.json()

    def create_collection(self, collection_name):
        """This function creates a general collection in the database,
        with a field text with is autoembeded with the model name e5-small

        The default collections is created with the following schema:

        {
            id: string
            embedding: float,
            text: string,
            start_line: int,
            end_line: int,
            page: int,
            file_id: string
        }

        Args:
            collection_name (str, required): Name of the collection

        Returns:
            response: dict

        Raises:

        """
        response = req.post(
            f"{self.url}:{self.port}/create-collection",
            headers={"x-typesense-api-key": self.api_key},
            params={"name": collection_name},
        )

        return response.json()

    def create_document(
        self,
        collection_name: str,
        document: Document,
    ):
        """This function creates a document in the collection

        Args:
            collection_name (str): Name of the collection
            schema (dict): schema of the preprocesseing and pdf urls

        Returns:
            json: response
        """

        response = req.post(
            f"{self.url}:{self.port}/create-document/",
            headers={"x-typesense-api-key": self.api_key},
            params={"name": collection_name},
            json=document,
        )

        return response.json()

    def delete_document(
        self, collection_name: str, filter_by: str = None, document_id: id = None
    ):
        """This function deletes a document in the collection

        Args:
            collection_name (str): Name of the collection
            field (str): field name to search the pdf document
            pdf_id (str): Id of the pdf document

        Returns:
            json: response
        """
        req.delete(
            f"{self.url}:{self.port}/delete-document",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "name": collection_name,
                "document_id": document_id,
                "filter_by": filter_by,
            },
        )

        # TODO: exceptions
        return True

    def delete_collection(self, collection_name):
        """This function deletes the collection with the given name

        Args:
            collection_name (str): Name of the collection

        Returns:
            json: response
        """
        response = req.delete(
            f"{self.url}:{self.port}/collections-delete/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return {"status": response.status_code, "description": "Collection deleted"}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def semantic_search(
        self,
        collection_name: str,
        query: str,
        num_results: int,
        rerank: bool = False,
        rerank_model: str = None,
    ):
        """This function performs a semantic search on the collection

        Args:
            collection_name (str): Name of the collection
            query (str): Query to search
            num_results (int): Number of results

        Returns:
            json: response
        """
        response = req.post(
            f"{self.url}:{self.port}/collections-semanticsearch",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
                "query": query,
                "num_results": num_results,
                "rerank": rerank,
                "rerank_model": rerank_model,
            },
        )
        if response.status_code == 200:
            return {"status": response.status_code, "description": response.json()}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def hybrid_search(
        self,
        collection_name: str,
        query: str,
        num_results: int,
        ft_search_field: str,
        rerank: bool = False,
        rerank_model: str = None,
    ):
        """This function performs a hybrid search on the collection, combining semantic search and full text search
        on a field or fields choose by the user

        Args:
            collection_name (str): Name of the collection
            query (str): Query to search
            num_results (int): Number of results
            ft_search_field (str): field to execute the full text search
            rerank (bool, optional): If True, rerank the results. Defaults to False.
            rerank_model (str, optional): Model to rerank the results. Defaults to None.
        Returns:
            response: json
        """
        response = req.post(
            f"{self.url}:{self.port}/collections-hybridsearch/",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
                "query": query,
                "num_results": num_results,
                "search_field": ft_search_field,
                "rerank": rerank,
                "rerank_model": rerank_model,
            },
        )

        if response.status_code != 200:
            raise GenericError(json.loads(response.text)["detail"])
        else:
            return response.json()

    def hybrid_search_filter(
        self,
        collection_name: str,
        query: str,
        num_results: int,
        ft_search_field: str,
        rerank: bool = False,
        rerank_model: str = None,
        filters: list = None,
    ):
        """This function performs a hybrid search on the collection, combining semantic search and full text search
        on a field or fields choose by the user

        Args:
            collection_name (str): Name of the collection
            query (str): Query to search
            num_results (int): Number of results
            ft_search_field (str): field to execute the full text search
            rerank (bool, optional): If True, rerank the results. Defaults to False.
            rerank_model (str, optional): Model to rerank the results. Defaults to None.
        Returns:
            response: json
        """

        payload = {
            "collection_name": collection_name,
            "query": query,
            "num_results": num_results,
            "search_field": ft_search_field,
            "rerank": rerank,
            "rerank_model": rerank_model,
            "filters": filters,
        }

        response = req.post(
            f"{self.url}:{self.port}/hybridsearch_filter/",
            headers={"x-typesense-api-key": self.api_key},
            json=payload,
        )

        if response.status_code == 200:
            return {"status": response.status_code, "description": response.json()}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def get_model_name(self):
        """This function returns the model name used to embed

        Returns:
            response: json with a list of the models used for embedding
        """
        response = req.get(
            f"{self.url}:{self.port}/embedding_models",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return {"status": response.status_code, "description": response.json()}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def get_rerank_model_name(self):
        """This function returns the model name used to rerank

        Returns:
            response: json with a list of the models used for embedding
        """
        response = req.get(
            f"{self.url}:{self.port}/rerank_models",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return {"status": response.status_code, "description": response.json()}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }
