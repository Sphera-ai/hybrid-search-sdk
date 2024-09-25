from __future__ import annotations


class CollectionNotFound(Exception):
    def __init__(self, collection_name):
        self.collection_name = collection_name
        super().__init__(f"Collection '{collection_name}' not found.")


class InvalidApiKey(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class DocumentCreationFailed(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
