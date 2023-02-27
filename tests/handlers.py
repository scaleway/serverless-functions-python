"""A collection of handlers used for testing."""

import base64
import json

HELLO_WORLD = "Hello World"
EXCEPTION_MESSAGE = "oops"

# pylint: disable=missing-function-docstring


def mirror_handler(event, context):  # noqa
    return {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"event": event, "context": context}),
    }


def handler_that_returns_string(_event, _context):  # noqa
    return HELLO_WORLD


def handler_with_404_status(_event, _context):  # noqa
    return {"statusCode": 404}


def handler_with_content_type(_event, _context):  # noqa
    return {
        "body": HELLO_WORLD,
        "headers": {
            "Content-Type": ["text/plain"],
        },
    }


def handler_returns_is_base_64_encoded(event, _context):  # noqa
    return event.get("isBase64Encoded")


def handler_returns_base64_encoded_body(_event, _context):  # noqa
    return {
        "body": base64.b64encode(HELLO_WORLD.encode("utf-8")).decode("utf-8"),
        "isBase64Encoded": True,
    }


def handler_returns_exception(_event, _context):  # noqa
    raise RuntimeError(EXCEPTION_MESSAGE)
