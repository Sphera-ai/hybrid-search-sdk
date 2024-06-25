from __future__ import annotations

import requests as req


class HybridSearch:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_all_collections(self):
        return req.get(
            "http://localhost:8000/collections",
            headers={"x-typesense-api-key": self.api_key},
        ).json()

    def get_collection(self, collection_name):
        return req.get(
            f"http://localhost:8000/collections/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        ).json

    def create_collection(self, schema):
        return req.post(
            "http://localhost:8000/collections",
            headers={"x-typesense-api-key": self.api_key},
            json=schema,
        ).json

    def delete_collection(self, collection_name):
        return req.delete(
            f"http://localhost:8000/collections/{collection_name}",
            headers={"x-typesense-api-key": self.api_key},
        ).json

    def create_document(self, collection_name, document):
        return req.post(
            f"http://localhost:8000/collections/{collection_name}/documents",
            headers={"x-typesense-api-key": self.api_key},
            json=document,
        ).json

    def get_document(self, collection_name, document_id):
        return req.get(
            f"http://localhost:8000/collections/{collection_name}/documents/{document_id}",
            headers={"x-typesense-api-key": self.api_key},
        ).json

    def delete_document(self, collection_name, document_id):
        return req.delete(
            f"http://localhost:8000/collections/{collection_name}/documents/{document_id}",
            headers={"x-typesense-api-key": self.api_key},
        ).json

    def search(self, collection_name, search_params):
        return req.get(
            f"http://localhost:8000/collections/{collection_name}/documents/search",
            headers={"x-typesense-api-key": self.api_key},
            params=search_params,
        ).json


hs = HybridSearch("xyz")
e = hs.get_all_collection()
print(0)
