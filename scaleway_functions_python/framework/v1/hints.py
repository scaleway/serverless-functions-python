import typing as t

try:
    from typing import NotRequired  # type: ignore
except ImportError:
    from typing_extensions import NotRequired


class RequestContext(t.TypedDict):
    """Request context that is sent in the http event."""

    accountId: str
    resourceId: str
    stage: str
    requestId: str
    resourcePath: str
    authorizer: t.Literal[None]
    httpMethod: str
    apiId: str


class Event(t.TypedDict):
    """Event dictionnary passed to the function."""

    path: str
    httpMethod: str
    headers: t.Dict[str, str]
    multiValueHeaders: t.Literal[None]
    queryStringParameters: t.Dict[str, str]
    multiValueQueryStringParameters: t.Literal[None]
    pathParameters: t.Literal[None]
    stageVariable: t.Dict[str, str]
    requestContext: RequestContext
    body: str
    isBase64Encoded: NotRequired[t.Literal[True]]


class Context(t.TypedDict):
    """Context dictionnary passed to the function."""

    memoryLimitInMb: int
    functionName: str
    functionVersion: str


class ResponseRecord(t.TypedDict, total=False):
    """Response dictionnary that the handler is expected to return."""

    body: str
    headers: t.Dict[str, str]
    statusCode: int
    isBase64Encoded: bool


# Type that the Serverless handler is expected to return
Response = t.Union[str, ResponseRecord]

Handler = t.Callable[[Event, Context], Response]
