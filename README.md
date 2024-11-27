# Serverless Functions Python 💜

[![PyPI version](https://badge.fury.io/py/scaleway-functions-python.svg)](https://badge.fury.io/py/scaleway-functions-python)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/scaleway/serverless-functions-python/main.svg)](https://results.pre-commit.ci/latest/github/scaleway/serverless-functions-python/main)
![pre-commit.ci status](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11-blue.svg)

Scaleway Serverless Functions Python is a framework that simplifies Scaleway [Serverless Functions](https://www.scaleway.com/fr/serverless-functions/) local development.
It enables you to debug your function locally and provide the event data format used in Scaleway Serverless Functions.

This library helps you to write functions but for deployment please refer to the documentation.

Get started with Scaleway Functions:

- [Scaleway Serverless Functions Documentation](https://www.scaleway.com/en/docs/serverless/functions/quickstart/)
- [Scaleway Serverless Framework plugin](https://github.com/scaleway/serverless-scaleway-functions)
- [Scaleway Serverless Examples](https://github.com/scaleway/serverless-examples)
- [Scaleway Cloud Provider](https://scaleway.com)

Testing frameworks for Scaleway Serverless Functions in other languages can be found here:

- [Go](https://github.com/scaleway/serverless-functions-go)
- [Node](https://github.com/scaleway/serverless-functions-node)

## ⚙️ Quickstart

You can use `pip` to install the framework:

```console
pip install scaleway-functions-python
```

```python
# handler.py

# Standard entrypoint to a Scaleway serverless function
def handler(event, context):
    if event["httpMethod"] != "GET":
         return {"statusCode": 405, "body": "Invalid method!"}
    return "Hello World!"

if __name__ == "__main__":
    # The import is conditional so that you do not need
    # to package the library when deploying on Scaleway Functions.
    from scaleway_functions_python import local
    local.serve_handler(handler, port=8080)
```

You can then run your function locally:

```console
$ python handler.py
$ curl http://localhost:8080
> Hello World!
$ curl -X POST http://localhost:8080
> Invalid method!
```

## 🚀 Features

This repository aims to provide a better experience on **local testing, utils, and documentation**

### 🏡 Local testing

What this package does:

- **Format Input**: Serverless Functions have a specific input format encapsulating the body received by functions to add some useful data.
  The local testing package lets you interact with the formatted data.
- **Advanced debugging**: To improve developer experience you can run your handler locally and debug it by running your code step-by-step or reading output directly before deploying it.

What this package does not:

- **Simulate performance**: Scaleway FaaS lets you choose different options for CPU/RAM that can have an impact
  on your development. This package does not provide specific limits for your function on local testing but you can profile your application or you can use our metrics available in [Scaleway Console](https://console.scaleway.com/)
  to monitor your application.
- **Deploy functions**: When your function is uploaded we package it in an environment that can be different than yours. Our build pipelines support several dependencies but sometimes require specific system dependencies (especially those related to lib c) that we don't support
  If you have compatibility issues, please see the help section.

### 🧱 Type hints

The framework provides some types hints to make it easier to develop your handler. See this [example](examples/mirror.py) for more information on how to use them.

## ❓ FAQ

**Why do I need an additional package to call my function?**

Your Function Handler can be served by a simple HTTP server but Serverless Ecosystem involves a lot of different layers that will change changes the headers, input and output of your function. This package aims to simulate everything your request will go through to help you debug your application properly.
This library is not mandatory to use Scaleway Serverless Functions.

**How my function will be deployed**

To deploy your function please refer to our official documentation.

**Do I need to deploy my function differently?**

No, this framework does not affect deployment or performance.

**How can I use my packaged dependencies?**

When deploying Python functions, your dependencies must be bundled in a `package` folder at the root of your project. For local testing, you can set `PYTHONPATH=$(pwd)/package` to make your dependencies available. This can be useful to avoid packaging your dependencies in multiple locations.

Please note that this does not work for native dependencies as the Scaleway Python runtime is different from your local machine.

**Why are my logs not showing up when using the print function?**

By default, stdout is buffered in Python, so calling `print` without `flush=True` can lead to missing logs when running locally.
If you experience this issue, you can export the environment variable `PYTHONUNBUFFERED` with `export PYTHONUNBUFFERED=1`.
This will flush stdout on every print call.

## 🎓 Contributing

We welcome all contributions to our open-source projects, please see our [contributing guidelines](./.github/CONTRIBUTING.md).

Do not hesitate to raise issues and pull requests we will have a look at them.

## 📭 Reach Us

We love feedback. Feel free to:

- Open a [Github issue](https://github.com/scaleway/serverless-functions-python/issues/new)
- Send us a message on the [Scaleway Slack community](https://slack.scaleway.com/), in the [#serverless-functions](https://scaleway-community.slack.com/app_redirect?channel=serverless-functions) channel.
