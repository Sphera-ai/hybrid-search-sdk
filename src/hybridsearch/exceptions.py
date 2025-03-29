from __future__ import annotations


class CollectionNotFound(Exception):  # 404
    def __init__(self, collection_name):
        self.collection_name = collection_name
        super().__init__(f"Collection '{collection_name}' not found.")


class CollectionAlreadyExists(Exception):  # 409
    def __init__(self, collection_name):
        self.collection_name = collection_name
        super().__init__(f"Collection '{collection_name}' already exists.")


class InvalidApiKey(Exception):  # 401
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class InvalidRequest(Exception):  # 406
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ServerError(Exception):
    def __init__(self, err_type, message):
        self.message = message
        self.err_type = err_type
        super().__init__(message)

    def __str__(self):
        return f"{self.err_type}: {self.message}"
