"""Utility module to inject provider-side headers."""

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask.wrappers import Request, Response

    from ..framework.v1.hints import Event


def inject_ingress_headers(request: "Request", event: "Event") -> None:
    """Inject headers for incoming requests.

    ..note::

        Because WGSI request headers are immutable,
        it's simpler to inject them into the event object directly.
    """
    if not request.remote_addr:
        raise RuntimeWarning("remote_addr is not set in the request")
    headers = {
        "Forwarded": f"for={request.remote_addr};proto=http",
        "X-Forwarded-For": request.remote_addr,
        "X-Envoy-External-Adrdress": request.remote_addr,
        "X-Forwarded-Proto": "http",
        # In this context "X-Forwared-For" == "X-Envoy-External-Address"
        # this property doesn't hold for actual functions
        "X-Envoy-External-Address": request.remote_addr,
        "X-Request-Id": str(uuid.uuid4()),
    }
    # Not using |= to keep compatibility with python 3.8
    event["headers"].update(**headers)


def inject_egress_headers(response: "Response") -> None:
    """Inject headers for outgoing requests."""
    response.headers.add("server", "envoy")
