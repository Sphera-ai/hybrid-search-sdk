from __future__ import annotations

import json

import hybridsearch.hybridsearch as hs_module
import pytest
from hybridsearch import HybridSearch
from hybridsearch.exceptions import ServerError

"""
Unit tests for the error handling of the client. They do not need the
microservice: the shared session is replaced with a fake response.
"""


class FakeResponse:
    def __init__(self, status_code: int, body: str, reason: str = ""):
        self.status_code = status_code
        self.text = body
        self.reason = reason

    def json(self):
        return json.loads(self.text)


class FakeSession:
    def __init__(self, response: FakeResponse):
        self.response = response

    def post(self, *args, **kwargs):
        return self.response

    def get(self, *args, **kwargs):
        return self.response

    def delete(self, *args, **kwargs):
        return self.response


def _client_with(monkeypatch, response: FakeResponse) -> HybridSearch:
    monkeypatch.setattr(hs_module, "session", FakeSession(response))
    return HybridSearch(api_key="test")


def test_non_json_error_body_is_reported(monkeypatch):
    """A gateway HTML page must not turn into a JSONDecodeError."""
    client = _client_with(
        monkeypatch,
        FakeResponse(502, "<html><body>Bad Gateway</body></html>", "Bad Gateway"),
    )

    with pytest.raises(ServerError) as exc_info:
        client.create_collection("test_collection")

    error = exc_info.value
    assert error.status_code == 502
    assert error.err_type == "http"
    assert "Bad Gateway" in error.message


def test_empty_error_body_falls_back_to_status(monkeypatch):
    """An empty 500 body must surface the HTTP status."""
    client = _client_with(monkeypatch, FakeResponse(500, "", "Internal Server Error"))

    with pytest.raises(ServerError) as exc_info:
        client.create_collection("test_collection")

    error = exc_info.value
    assert error.status_code == 500
    assert error.err_type == "http"
    assert "500" in error.message


def test_structured_error_detail_is_preserved(monkeypatch):
    """The usual {"detail": {...}} payload keeps its type and message."""
    body = json.dumps({"detail": {"error_type": "typesense", "strerror": "boom"}})
    client = _client_with(monkeypatch, FakeResponse(500, body, "Internal Server Error"))

    with pytest.raises(ServerError) as exc_info:
        client.create_collection("test_collection")

    error = exc_info.value
    assert error.status_code == 500
    assert error.err_type == "typesense"
    assert error.message == "boom"
    assert str(error) == "typesense: boom"


def test_string_error_detail_is_reported(monkeypatch):
    """FastAPI plain-string details must not raise a TypeError."""
    body = json.dumps({"detail": "Not Found"})
    client = _client_with(monkeypatch, FakeResponse(400, body, "Bad Request"))

    with pytest.raises(ServerError) as exc_info:
        client.create_collection("test_collection")

    error = exc_info.value
    assert error.status_code == 400
    assert error.message == "Not Found"


def test_non_json_success_body_raises_server_error(monkeypatch):
    """A 200 with an undecodable body is a server error, not a crash."""
    client = _client_with(monkeypatch, FakeResponse(200, "not json at all", "OK"))

    with pytest.raises(ServerError) as exc_info:
        client.create_collection("test_collection")

    error = exc_info.value
    assert error.status_code == 200
    assert error.err_type == "invalid_response"
