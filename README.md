# Serverless Functions Python 💜

Scaleway Serverless Functions is a framework to provide a good developer experience to write Serverless Functions.

Serverless Functions make it easy to deploy, scale, and optimize your workloads on the cloud.

## ⚙️ Installation

You can use `pip` to install the framework:

```console
pip install scaleway-functions-python
```

## 📦 Usage

### 🏡 Local testing

When working with Serverless functions, it can be hard to test your function without deploying it. The framework provides a utility function that will run your handler locally:

```python
# In handler.py

# Define your Serverless Handler.
def handler(event, _context):
    if event["method"] != "GET":
         return {"statusCode": 405, "body": "Invalid method!"}
    return "Hello World!"

if __name__ == "__main__":
    # The import is conditional so that you do not need
    # to package the library when deploying on Scaleway Functions.
    from scaleway_functions_python import serve_handler_locally
    serve_handler_locally(handler, port=8080)
```

This adds an entry point to your Python script to run your Serverless handler locally.

```console
$ python handler.py
$ curl http://localhost:8080
> Hello World!
$ curl -X POST http://localhost:8080
> Invalid method!
```

### 🧱 Type hints

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

We love feedback.
Don't hesitate to open a [Github issue](https://github.com/scaleway/serverless-functions-python/issues/new) or
feel free to reach us on [Scaleway Slack community](https://slack.scaleway.com/),
we are waiting for you on [#serverless-functions](https://scaleway-community.slack.com/app_redirect?channel=serverless-functions).
