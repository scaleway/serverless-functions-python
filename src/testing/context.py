from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from serverless_functions_python.hints import Context, Handler


def format_context(handler: "Handler") -> "Context":
    """Formats the request context from the request."""
    return {
        "memoryLimitInMb": 128,
        "functionName": handler.__name__,
        "functionVersion": "",
    }
