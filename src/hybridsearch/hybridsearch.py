from __future__ import annotations

import json

import requests as req

from .preprocessing import process_pdf_to_chunks


class HybridSearch:
    def __init__(self, api_key: str, url: str = "localhost", port: int = 8000):
        """This class is used to interact with the microservice typesense+fastapi

        Args:
            api_key (str): API key to access the database
            url (str, optional): URL of the microservice. Defaults to "localhost".
            port (int, optional): Port of the microservice. Defaults to 8000.
        """

        self.api_key = api_key
        self.port = port
        self.url = url

        self.check_api_key()

    def check_api_key(self):
        """
        This function checks if the API key is valid

        Raises
        ------
        Exception: If the API key is invalid
        """
        status_code = req.get(
            f"http://{self.url}:{self.port}/api-key",
            headers={"x-typesense-api-key": self.api_key},
        ).status_code
        if status_code != 200:
            raise Exception("Invalid API Key")

    def get_all_collections(self):
        """This function returns all the collections in the database

        Returns:
            json: response with all the collections
        """
        response = req.get(
            f"http://{self.url}:{self.port}/collections",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def get_collection(self, collection_name):
        """This function returns the collection with the given name

        Args:
            collection_name (str): Name of the collection

        Returns:
            json: response with the collection information
        """
        response = req.get(
            f"http://http://{self.url}:{self.port}/collections/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def create_custom_collection(
        self, embedding_field: str, model_name: str, schema: dict
    ):
        """This function creates a collection in the database

        Args:
            embedding_field (str, required): field to embed
            model_name (str, required): model  name used to embed the field
            schema (dict, required): schema of the fields

        Returns:
            json: response of the created collection
        """

        response = req.post(
            f"http://{self.url}:{self.port}/create-collection-custom",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "embedding_field": embedding_field,
                "model_name": model_name,
            },
            json=schema,
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def create_collection(self, collection_name):
        """This function creates a general collection in the database,
        with a field text with is autoembeded with the model name e5-small

        Args:
            collection_name (str, required): Name of the collection
        Returns:
            response: json
        """
        response = req.post(
            f"http://{self.url}:{self.port}/create-collection",
            headers={"x-typesense-api-key": self.api_key},
            params={"name": collection_name},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def create_document(self, collection_name: str, schema: dict):
        """This function creates a document in the collection

        Args:
            collection_name (str): Name of the collection

        Returns:
            json: response
        """
        response = req.post(
            f"http://{self.url}:{self.port}/create-document",
            headers={"x-typesense-api-key": self.api_key},
            params={"name": collection_name},
            json=schema,
        )

        return (
            response.status_code
            if response.status_code == 200
            else {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }
        )

    def create_document_from_file(
        self,
        collection_name: str,
        file_path: str,
        field: str,
        chunk_size: int = 1000,
        overlap_size=200,
    ):
        """This function creates a documents from a pdf file

        Args:
            collection_name (str): collection name
            file_path (str): path to the file
            field (str): field to insert the text
        """

        chunks = process_pdf_to_chunks(file_path, chunk_size, overlap_size)

        for chunk in chunks:
            schema = {
                field: chunk["text"],
                "page": chunk["page"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
            }

            response = self.create_document(collection_name, schema)
            if response.status_code != 200:
                return response

        return response

    def delete_collection(self, collection_name):
        """This function deletes the collection with the given name

        Args:
            collection_name (str): Name of the collection

        Returns:
            json: response
        """
        response = req.delete(
            f"http://{self.url}:{self.port}/collections-delete/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return response.json()
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
            "http://localhost:8000/collections-semanticsearch",
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
            return response.json()
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
        field: str,
        rerank: bool = False,
        rerank_model: str = None,
    ):
        """This function performs a hybrid search on the collection, combining semantic search and full text search
        on a field or fields choose by the user

        Args:
            collection_name (str): Name of the collection
            query (str): Query to search
            num_results (int): Number of results
            field (str): fields to search
            rerank (bool, optional): If True, rerank the results. Defaults to False.
            rerank_model (str, optional): Model to rerank the results. Defaults to None.
        Returns:
            response: json
        """
        response = req.post(
            f"http://{self.url}:{self.port}/collections-hybridsearch/",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "collection_name": collection_name,
                "query": query,
                "num_results": num_results,
                "search_field": field,
                "rerank": rerank,
                "rerank_model": rerank_model,
            },
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def get_schema_attributes(self, collection_name):
        """This function returns the schema attributes of an existing collection

        Args:
            collection_name (_type_): Name of the collection

        Returns:
            response: json
        """

        pass

    def get_model_name(self):
        """This function returns the model name used to embed

        Returns:
            response: json with a list of the models used for embedding
        """
        response = req.get(
            f"http://{self.url}:{self.port}/embedding_models",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return response.json()
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
            f"http://{self.url}:{self.port}/rerank_models",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }
