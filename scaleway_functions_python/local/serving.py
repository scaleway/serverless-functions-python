import logging
from base64 import b64decode
from json import JSONDecodeError
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, Union, cast

from flask import Flask, json, jsonify, make_response, request
from flask.views import View

from ..local import infra
from ..local.context import format_context
from ..local.event import format_http_event

if TYPE_CHECKING:
    from flask.wrappers import Request as FlaskRequest
    from flask.wrappers import Response as FlaskResponse

    from ..framework.v1 import hints

# TODO?: Switch to https://docs.python.org/3/library/http.html#http-methods
# for Python 3.11+
ALL_HTTP_METHODS = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH",
]
MAX_CONTENT_LENGTH = 6291456


class HandlerWrapper(View):  # type: ignore # Subclass of untyped class
    """View that emulates the provider-side processing of requests."""

    init_every_request: ClassVar[bool] = False

    def __init__(self, handler: "hints.Handler") -> None:
        self.handler = handler

    @property
    def logger(self) -> "logging.Logger":
        """Utility function to get a logger."""
        return logging.getLogger(self.handler.__name__)

    def dispatch_request(self, *_args: Any, **_kwargs: Any) -> "FlaskResponse":
        """Handle http requests."""
        self.emulate_core_preprocess(request)

        event = format_http_event(request)
        infra.inject_ingress_headers(request, event)

        context = format_context(self.handler)

        sub_response = self.emulate_subruntime(event, context)
        record = self.emulate_core_postprocess(sub_response)

        resp = self.resp_record_to_flask_response(record)
        infra.inject_egress_headers(resp)

        return resp

    def emulate_core_preprocess(self, req: "FlaskRequest") -> None:
        """Emulate the CoreRT guard."""
        if req.content_length and req.content_length > MAX_CONTENT_LENGTH:
            self.logger.warning(
                "Request is too big, should not exceed %s Mb but is %s Mb",
                MAX_CONTENT_LENGTH / (1 << 20),
                req.content_length / (1 << 20),
            )
        if req.path in ["/favicon.ico", "/robots.txt"]:
            self.logger.warning(
                "Requests to either favicon.ico or robots.txt are dropped"
            )

    def emulate_subruntime(
        self, event: "hints.Event", context: "hints.Context"
    ) -> "FlaskResponse":
        """Emulate the subruntime."""
        try:
            function_result = self.handler(event, context)
        except Exception as e:  # pylint: disable=broad-exception-caught # from subRT
            self.logger.warning(
                "Exception caught in handler %s, this will return a 500 when deployed",
                self.handler.__name__,
            )
            raise e
        if isinstance(function_result, str):
            return make_response(function_result)
        return jsonify(function_result)

    def emulate_core_postprocess(
        self, sub_response: "FlaskResponse"
    ) -> "hints.ResponseRecord":
        """Emulate the CoreRT runtime response processing.

        While it seems unecessary to generate an intermediate response,
        the serialization followed by a deserizalization does affect the final response.
        It also makes it easier to maintain compatibility with the CoreRT.
        """
        body = sub_response.get_data(as_text=True)
        response: "hints.ResponseRecord" = {
            "statusCode": sub_response.status_code,
            "headers": dict(sub_response.headers.items()),
            "body": body,
        }
        try:
            record = json.loads(body)
            if not isinstance(record, dict):
                return response

            # Not using the |= operator to manually drop unexpected keys
            response = cast(
                "hints.ResponseRecord",
                {
                    key: val
                    for key, val in record.items()
                    if key in response or key == "isBase64Encoded"
                },
            )
            return response
        except JSONDecodeError:
            return response

    def resp_record_to_flask_response(
        self, record: "hints.ResponseRecord"
    ) -> "FlaskResponse":
        """Transform the ReponseRecord into an http reponse."""
        body: Union[str, bytes] = record.get("body", "")
        if record.get("isBase64Encoded") and body:
            body = b64decode(cast(str, body).encode("utf-8"), validate=True)

        resp = make_response(body, record.get("statusCode"))

        # Those headers are added for convenience, but will be
        # overwritten if set in the handler
        resp.headers.add("Access-Control-Allow-Origin", "*")
        resp.headers.add("Access-Control-Allow-Headers", "Content-Type")

        resp.headers.update(record.get("headers") or {})

        return resp


class LocalFunctionServer:
    """LocalFunctionServer serves Scaleway FaaS handlers on a local http server."""

    def __init__(self) -> None:
        self.app = Flask("serverless_local")

    def add_handler(
        self,
        handler: "hints.Handler",
        relative_url: Optional[str] = None,
        http_methods: Optional[List[str]] = None,
    ) -> "LocalFunctionServer":
        """Add a handler to be served by the server.

        :param handler: serverless python handler
        :param relative_url: path to the handler, defaults to / + handler's name
        :param http_methods: HTTP methods for the handler, defaults to all methods
        """
        relative_url = relative_url if relative_url else "/" + handler.__name__
        if not relative_url.startswith("/"):
            relative_url = "/" + relative_url

        http_methods = http_methods if http_methods else ALL_HTTP_METHODS
        http_methods = [method.upper() for method in http_methods]

        view = HandlerWrapper(handler).as_view(handler.__name__, handler)

        # By default, methods contains ["GET", "HEAD", "OPTIONS"]
        self.app.add_url_rule(
            f"{relative_url}/<path:path>", methods=http_methods, view_func=view
        )
        self.app.add_url_rule(
            relative_url,
            methods=http_methods,
            defaults={"path": ""},
            view_func=view,
        )

        return self

    def serve(
        self, *args: Any, port: int = 8080, debug: bool = True, **kwargs: Any
    ) -> None:
        """Serve the added FaaS handlers.

        :param port: port that the server should listen on, defaults to 8080
        :param debug: run Flask in debug mode, enables hot-reloading and stack trace.
        """
        kwargs["port"] = port
        kwargs["debug"] = debug
        self.app.run(*args, **kwargs)


def serve_handler(
    handler: "hints.Handler",
    *args: Any,
    port: int = 8080,
    debug: bool = True,
    **kwargs: Any,
) -> None:
    """Serve a single FaaS handler on a local http server.

    :param handler: serverless python handler
    :param port: port that the server should listen on, defaults to 8080
    :param debug: run Flask in debug mode, enables hot-reloading and stack trace.

    Example:
        >>> def handle(event, _context):
        ...     return {"body": event["httpMethod"]}
        >>> serve_handler_locally(handle, port=8080)
    """
    server = LocalFunctionServer()
    server.add_handler(handler=handler, relative_url="/")
    server.serve(*args, port=port, debug=debug, **kwargs)
