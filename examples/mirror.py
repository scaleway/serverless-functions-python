import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Doing a conditional import avoids the need to install the library
    #  when deploying the function
    from scaleway_functions_python.v1.hints import Context, Event, Response


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
    from scaleway_functions_python import serve_handler_locally

    serve_handler_locally(handler)
