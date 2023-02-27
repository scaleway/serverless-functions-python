import base64
import uuid

import pytest
from flask.testing import FlaskClient

from testing.serving import _create_flask_app

from .. import handlers as h


@pytest.fixture(scope="function")
def client(request) -> FlaskClient:
    app = _create_flask_app(request.param)
    app.config.update({"TESTING": True})
    return app.test_client()


@pytest.mark.parametrize(
    "client, expected",
    [
        (h.handler_that_returns_string, {"statusCode": 200, "body": h.HELLO_WORLD}),
        (h.handler_with_404_status, {"statusCode": 404, "body": ""}),
        (
            h.handler_with_content_type,
            {
                "statusCode": 200,
                "body": h.HELLO_WORLD,
                "headers": {"Content-Type": "text/plain"},
            },
        ),
    ],
    indirect=["client"],
)
def test_serve_handler(client, expected):
    resp = client.get("/")

    assert resp.status_code == expected.get("statusCode")
    assert resp.text == expected.get("body")

    for hkey, hval in expected.get("headers", {}).items():
        assert resp.headers.get(hkey) == hval


@pytest.mark.parametrize(
    "client", [h.handler_returns_is_base_64_encoded], indirect=True
)
def test_serve_handler_b64_parameter_correct(client):
    data = base64.b64encode(h.HELLO_WORLD.encode("utf-8"))
    resp = client.post("/", data=data)
    assert resp.text == "true\n"

    resp = client.post("/", data=h.HELLO_WORLD)
    # Gets should return None which gets json-encoded into null
    assert resp.text == "null\n"


@pytest.mark.parametrize(
    "client", [h.handler_returns_base64_encoded_body], indirect=True
)
def test_serve_handler_with_b64_encoded_body(client):
    resp = client.get("/")
    assert resp.text == h.HELLO_WORLD


@pytest.mark.parametrize("client", [h.handler_returns_exception], indirect=True)
def test_serve_handler_with_exception(client):
    resp = client.get("/")
    assert resp.text == h.EXCEPTION_MESSAGE


@pytest.mark.parametrize("client", [h.mirror_handler], indirect=True)
def test_serve_handler_inject_infra_headers(client):
    resp = client.get("/")

    # Check the response headers
    assert resp.headers["server"] == "envoy"

    body = resp.get_json()
    headers = body["event"]["headers"]

    # Check the headers injected in the event object
    assert headers["Forwarded"] == "for=127.0.0.1;proto=http"
    assert headers["X-Forwarded-For"] == "127.0.0.1"
    assert headers["X-Envoy-External-Adrdress"] == "127.0.0.1"
    assert headers["X-Forwarded-Proto"] == "http"

    uuid.UUID(headers["X-Request-Id"])
