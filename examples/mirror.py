import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from serverless_functions_python import Context, Event, Response


def handler(event: "Event", context: "Context") -> "Response":
    """Function that mirrors its parameters in the body."""
    return {
        "body": json.dumps(
            {
                "event": event,
                "context": context,
            }
        )
    }


if __name__ == "__main__":
    from serverless_functions_python import serve_handler_locally

    serve_handler_locally(handler)
