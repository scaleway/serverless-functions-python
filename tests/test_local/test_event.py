import pytest
from flask import Flask, Request, request
from werkzeug.test import EnvironBuilder

from scaleway_functions_python.local.event import format_http_event


@pytest.fixture()
def app():
    app = Flask("test")
    app.config.update({"TESTING": True})
    yield app


def test_format_http_event(app):
    expected_request_context = {
        "accountId": "",
        "resourceId": "",
        "stage": "",
        "requestId": "",
        "resourcePath": "",
        "authorizer": None,
        "httpMethod": "GET",
        "apiId": "",
    }
    expected_query_string_parameters = {"param_1": "value_1", "param_2": "value_2"}

    with app.test_request_context(
        query_string="param_1=value_1&param_2=value_2",
        path="/path",
        headers={"Content-Type": "text/plain"},
        method="GET",
    ):
        app.preprocess_request()
        event = format_http_event(request)

        assert event["path"] == "/path"
        assert event["headers"]["Content-Type"] == "text/plain"
        assert event["multiValueHeaders"] is None

        assert event["queryStringParameters"] == expected_query_string_parameters

        assert event["multiValueQueryStringParameters"] is None
        assert event["pathParameters"] is None
        assert not event["stageVariable"]

        assert event.get("isBase64Encoded")

        assert event["requestContext"] == expected_request_context

        assert event["body"] == ""


def test_format_http_event_with_non_unicode_body():
    # Create a request with non-unicode body
    non_unicode_body = b"\xff\xfe\xfd"  # Invalid UTF-8 sequence
    builder = EnvironBuilder(method="POST", data=non_unicode_body)
    req = Request(builder.get_environ())

    # Call the function and check the result
    event = format_http_event(req)

    assert event is not None
    assert "body" in event
    assert event.get("isBase64Encoded", False) is False
