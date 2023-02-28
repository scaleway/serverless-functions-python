# Serverless Functions Python 💜

This repo contains utilities for testing your Python handlers for Scaleway Serverless Functions.

## ⚙️ Quick Start

You can use `pip` to install the framework:

```console
pip install scaleway-functions-python
```

```python
# handler.py

# Standard entrypoint to a Scaleway serverless function
def handler(event, context):
    if event["method"] != "GET":
         return {"statusCode": 405, "body": "Invalid method!"}
    return "Hello World!"

if __name__ == "__main__":
    # The import is conditional so that you do not need
    # to package the library when deploying on Scaleway Functions.
    from scaleway_functions_python import serve_handler_locally
    serve_handler_locally(handler, port=8080)
```

You can then run your function locally:

```console
$ python handler.py
$ curl http://localhost:8080
> Hello World!
$ curl -X POST http://localhost:8080
> Invalid method!
```

## 🧱 Type hints

The framework provides some types hints to make it easier to develop your handler. See this [example](examples/mirror.py) for more information on how to use them.

## 🌍 Resources

Get started with Scaleway Functions:

- [Scaleway Serverless Functions Documentation](https://www.scaleway.com/en/docs/serverless/functions/quickstart/)
- [Scaleway Serverless Framework plugin](https://github.com/scaleway/serverless-scaleway-functions)
- [Scaleway Serverless Examples](https://github.com/scaleway/serverless-examples)
- [Scaleway Cloud Provider](https://scaleway.com)

Testing frameworks for Scaleway Serverless Functions in other languages can be found here:

- [Go](https://github.com/scaleway/serverless-functions-go)

## 🎓 Contributing

We welcome all contributions to our open-source projects, please see our [contributing guidelines](docs/CONTRIBUTING.md).

Do not hesitate to raise issues and pull requests we will have a look at them.

## 💜 Reach Us

We love feedback. Feel free to:

- Open a [Github issue](https://github.com/scaleway/serverless-functions-python/issues/new)
- Send us a message on the [Scaleway Slack community](https://slack.scaleway.com/), in the [#serverless-functions](https://scaleway-community.slack.com/app_redirect?channel=serverless-functions) channel.
