from __future__ import annotations

import json

import requests as req

from .exceptions import CollectionNotFound, DocumentCreationFailed, InvalidApiKey
from .models import Document


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
            raise InvalidApiKey("Invalid API key")

    def get_all_collections(self):
        """This function returns all the collections in the database

        Returns:
            json: response with all the collections
        """
        response = req.get(
            f"http://{self.url}:{self.port}/collections",
            headers={"x-typesense-api-key": self.api_key},
        )
        if response.status_code == 401:
            raise InvalidApiKey("Invalid API key")
        if response.status_code == 404:
            raise CollectionNotFound("No collection found")
        
        

        if response.status_code == 200:
            return {"status": 200, "description": response.json()}
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
            f"http://{self.url}:{self.port}/collections/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return {"status": response.status_code, "description": response.json()}
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
            return {"status": response.status_code, "description": response.json()}
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
            response: dict
        """
        response = req.post(
            f"http://{self.url}:{self.port}/create-collection",
            headers={"x-typesense-api-key": self.api_key},
            params={"name": collection_name},
        )

        if response.status_code == 200:
            return {"status": response.status_code, "description": response.json()}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def create_document(self, collection_name: str, schema: Document):
        """This function creates a document in the collection

        Args:
            collection_name (str): Name of the collection
            schema (dict): schema of the preprocesseing and pdf urls

        Returns:
            json: response
        """
        response = req.post(
            f"http://{self.url}:{self.port}/create-document/",
            headers={"x-typesense-api-key": self.api_key},
            params={"name": collection_name},
            json=schema,
        )
        if response.status_code == 404:
            raise CollectionNotFound(collection_name)
        elif response.status_code == 400:
            raise DocumentCreationFailed(json.loads(response.text)["detail"])
        else:
            return {"status": 200, "description": "Document created successfully"}

    def delete_document(self, collection_name: str, field: str, pdf_id: str):
        """This function deletes a document in the collection

        Args:
            collection_name (str): Name of the collection
            field (str): field name to search the pdf document
            pdf_id (str): Id of the pdf document

        Returns:
            json: response
        """
        response = req.delete(
            f"http://{self.url}:{self.port}/delete-document",
            headers={"x-typesense-api-key": self.api_key},
            params={
                "name": collection_name,
                "document_id": pdf_id,
                "field": field,
            },
        )

        if response.status_code == 200:
            return {"status": 200, "description": "Document deleted successfully"}
        return {
            "status": int(response.status_code),
            "description": json.loads(response.text)["detail"],
        }

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
            f"http://{self.url}:{self.port}/collections-semanticsearch",
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
            return {"status": response.status_code, "description": response.json()}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    def hybrid_search_filter(
        self,
        collection_name: str,
        query: str,
        num_results: int,
        field: str,
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
            field (str): fields to search
            rerank (bool, optional): If True, rerank the results. Defaults to False.
            rerank_model (str, optional): Model to rerank the results. Defaults to None.
        Returns:
            response: json
        """

        payload = {
            "collection_name": collection_name,
            "query": query,
            "num_results": num_results,
            "search_field": field,
            "rerank": rerank,
            "rerank_model": rerank_model,
            "filters": filters,
        }
        response = req.post(
            f"http://{self.url}:{self.port}/hybridsearch_filter/",
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
            f"http://{self.url}:{self.port}/embedding_models",
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
            f"http://{self.url}:{self.port}/rerank_models",
            headers={"x-typesense-api-key": self.api_key},
        )

        if response.status_code == 200:
            return {"status": response.status_code, "description": response.json()}
        else:
            return {
                "status": response.status_code,
                "description": json.loads(response.text)["detail"],
            }

    # def create_documents_for_list(
    #     self,
    #     collection_name: str,
    #     url_list: list,
    #     field: str,
    #     chunk_mode: str = "naive",  # naive or semantic
    #     chunk_size: int = 1000,
    #     overlap_size=200,
    #     mode: str = "words",
    #     model_to_semantic_chunk: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    # ):
    #     """This function creates documents from a list of urls

    #     Args:
    #         collection_name (str): collection name
    #         list (list): list of urls
    #         field (str): field to insert the text
    #         chunk_mode (str, optional): chunk mode. Defaults to "naive".
    #         chunk_size (int, optional): chunk size. Defaults to 1000.
    #         overlap_size (int, optional): overlap size. Defaults to 200.
    #         mode (str, optional): mode. Defaults to "words".
    #         model_to_semantic_chunk (str, optional): model to semantic chunk. Defaults to "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2".
    #     """

    #     if chunk_mode not in ["naive", "semantic"]:
    #         raise ValueError("chunk_mode should be 'naive' or 'semantic'")

    #     # create a .tmp folder where the files are donwloaded
    #     if not os.path.exists(".tmp"):
    #         os.makedirs(".tmp")

    #     for url in url_list:
    #         # download the files
    #         response = req.get(url)
    #         pdf_name = url.split("/")[-1]
    #         with open(f".tmp/{pdf_name}", "wb") as f:
    #             f.write(response.content)

    #     pdfs = os.listdir(".tmp")
    #     list_response = []
    #     for pdf in pdfs:
    #         response = self.create_document_from_file(
    #             collection_name,
    #             f".tmp/{pdf}",
    #             field,
    #             chunk_mode,
    #             chunk_size,
    #             overlap_size,
    #             mode,
    #             model_to_semantic_chunk,
    #         )
    #         list_response.append(response)

    #     # create a dict with the response for each pdf
    #     response = {}
    #     for i, pdf in enumerate(pdfs):
    #         response[pdf] = list_response[i]
    #     # delete the .tmp folder and the contents
    #     for pdf in pdfs:
    #         os.remove(f".tmp/{pdf}")
    #     os.rmdir(".tmp")

    #     return response

    # def create_document_from_document(self, collection_name: str, pdf_file):
    #     """This function creates a document in the collection

    #     Args:
    #         collection_name (str): Name of the collection

    #     Returns:
    #         json: response
    #     """
    #     response = req.post(
    #         f"http://{self.url}:{self.port}/create-document_1",
    #         headers={"x-typesense-api-key": self.api_key},
    #         params={"name": collection_name},
    #         files={"file": pdf_file},
    #     )

    #     if response.status_code == 200:
    #         return {"status": 200, "description": "Document sent successfully"}
    #     return {
    #         "status": int(response.status_code),
    #         "description": json.loads(response.text)["detail"],
    #     }

    # def create_document_from_list(
    #     self, collection_name: str, urls: list, preprocessing: dict
    # ):
    #     schema = {}
    #     # insert urls in the schema
    #     urls_ = []
    #     for i, url in enumerate(urls):
    #         urls_.append(url)

    #     schema["urls"] = urls_
    #     schema.update({key: value for key, value in preprocessing.items()})

    #     response = req.post(
    #         f"http://{self.url}:{self.port}/create-document_1/",
    #         headers={"x-typesense-api-key": self.api_key},
    #         params={"name": collection_name},
    #         json=schema,  # Ensure that you're using `json=` to send the body as JSON
    #     )

    #     if response.status_code == 200:
    #         return {"status": 200, "description": "Document sent successfully"}
    #     return {
    #         "status": int(response.status_code),
    #         "description": json.loads(response.text)["detail"],
    #     }

    # def create_document_from_file(
    #     self,
    #     collection_name: str,
    #     file_path: str,
    #     field: str,
    #     chunk_mode: str = "naive",  # naive or semantic
    #     chunk_size: int = 1000,
    #     overlap_size=200,
    #     mode: str = "words",
    #     model_to_semantic_chunk: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    # ):
    #     """This function creates documents from a pdf file

    #     Args:
    #         collection_name (str): collection name
    #         file_path (str): path to the file
    #         field (str): field to insert the text
    #         chunk_mode (str, optional): chunk mode. Defaults to "naive".
    #         chunk_size (int, optional): chunk size. Defaults to 1000.
    #         overlap_size (int, optional): overlap size. Defaults to 200.
    #         mode (str, optional): mode. Defaults to "words".
    #         model_to_semantic_chunk (str, optional): model to semantic chunk. Defaults to "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2".
    #     """

    #     if chunk_mode not in ["naive", "semantic"]:
    #         raise ValueError("chunk_mode should be 'naive' or 'semantic'")

    #     if chunk_mode == "semantic":
    #         if model_to_semantic_chunk == "":
    #             raise ValueError("model_to_semantic_chunk should be provided")

    #         chunker = SemanticChunking(file_path, model_to_semantic_chunk)
    #         chunks, _ = chunker.create_chunks()

    #     if chunk_mode == "naive":
    #         if mode not in ["words", "characters"]:
    #             raise ValueError("mode should be 'words' or 'characters'")

    #         try:
    #             chunker = NaiveChunking(file_path, chunk_size, overlap_size, mode)
    #         except Exception as e:
    #             logger.error(f"Error in naive chunking: {str(e)}")
    #         chunks = chunker.create_chunks()

    #     for chunk in chunks:
    #         schema = {
    #             field: chunk["text"],
    #             "page": chunk["page"],
    #             "start_line": chunk["start_line"],
    #             "end_line": chunk["end_line"],
    #         }

    #         response = self.create_document(collection_name, schema)
    #         if response["status"] != 200:
    #             return response
    #     return response
