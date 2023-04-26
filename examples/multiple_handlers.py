from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Doing a conditional import avoids the need to install the library
    # when deploying the function
    from scaleway_functions_python.framework.v1.hints import Context, Event, Response


def hello(_event: "Event", _context: "Context") -> "Response":
    """Say hello!"""
    return {"body": "hello"}


def world(_event: "Event", _context: "Context") -> "Response":
    """Say world!"""
    return {"body": "world"}


if __name__ == "__main__":
    from scaleway_functions_python import local

    server = local.LocalFunctionServer()
    server.add_handler(hello)
    server.add_handler(world)
    server.serve(port=8080)

    # Functions can be queried with:
    # curl localhost:8080/hello
    # curl localhost:8080/world
