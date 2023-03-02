import binascii
from base64 import b64decode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask.wrappers import Request

    from ..framework.v1.hints import Event, RequestContext


def _format_request_context(request: "Request") -> "RequestContext":
    """Format the request context from the request."""
    return {
        "accountId": "",
        "resourceId": "",
        "stage": "",
        "requestId": "",
        "resourcePath": "",
        "authorizer": None,
        "httpMethod": request.method,
        "apiId": "",
    }


def format_http_event(request: "Request") -> "Event":
    """Format the event from a generic http request."""
    context = _format_request_context(request)
    body = request.get_data(as_text=True)
    event: "Event" = {
        "path": request.path,
        "httpMethod": request.method,
        "headers": dict(request.headers.items()),
        "multiValueHeaders": None,
        "queryStringParameters": request.args.to_dict(),
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariable": {},
        "requestContext": context,
        "body": body,
    }  # type: ignore # NotRequired works with Pylance here but not mypy 1.0 (bug?)
    try:
        b64decode(body, validate=True).decode("utf-8")
        event["isBase64Encoded"] = True
    except (binascii.Error, UnicodeDecodeError):
        pass
    return event
