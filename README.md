# Serverless Functions Python 💜

Scaleway Serverless Functions is a framework to provide a good developer experience to write Serverless Functions.

Serverless Functions make it easy to deploy, scale, and optimize your workloads on the cloud.

Get started with Scaleway Functions (we support multiple languages :rocket:):

- [Scaleway Serverless Functions Documentation](https://www.scaleway.com/en/docs/serverless/functions/quickstart/)
- [Scaleway Serverless Framework plugin](https://github.com/scaleway/serverless-scaleway-functions)
- [Scaleway Serverless Examples](https://github.com/scaleway/serverless-examples)
- [Scaleway Cloud Provider](https://scaleway.com)

Testing frameworks for Scaleway Serverless Functions in other languages can be found here:

- [Go](https://github.com/scaleway/serverless-functions-go)
- [Node](https://github.com/scaleway/serverless-functions-node)
- [PHP](https://github.com/scaleway/serverless-functions-php)
- [Rust](https://github.com/scaleway/serverless-functions-rust)

## ⚙️ Quickstart

You can use `pip` to install the framework:

```console
pip install scaleway-functions-python
```

```python
def handler(event, context):
    return "Hello World!"

if __name__ == "__main__":
    from scaleway_functions_python import serve_handler_locally
    serve_handler_locally(handler)
```

For advanced usage please check the [usage section](#📦-Usage).

## 🛟 Help & support

- Scaleway support is available on Scaleway Console.
- Additionally, you can join our [Slack Community](https://www.scaleway.com/en/docs/tutorials/scaleway-slack-community/)

## 🎓 Contributing

We welcome all contributions to our open-source projects, please see our [contributing guidelines](docs/CONTRIBUTING.md).

Do not hesitate to raise issues and pull requests we will have a look at them.

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

```console
$ python handler.py
$ curl http://localhost:8080
> Hello World!
$ curl -X POST http://localhost:8080
> Invalid method!
```

### 🧱 Type hints

The framework provides some types hints to make it easier to develop your handler. See this [example](examples/mirror.py) for more information on how to use them.

Check out the examples to get started!

## ❓ FAQ

**Why do I need an additional package to call my function?**

Your Function Handler can be served by a simple HTTP server but Serverless Ecosystem involves a lot of different layers
and this package aims to simulate everything your request will go through.

**How my function will be deployed**

Your function will be deployed in an environment that allows your function to easily Scale up and down and it's wrapped into
different pieces of software with different roles. This stack also changes the headers, input and output of your function, that's why
this tool has been developed to simulate this part.

**Do I need to deploy my function differently?**

No. This framework does not affect deployment nor performance.

## Development

This repository is at its early stage and is still in active development.
If you are looking for a way to contribute please read [CONTRIBUTING.md](./docs/CONTRIBUTING.md).

## Reach Us

We love feedback.
Don't hesitate to open a [Github issue](https://github.com/scaleway/serverless-functions-python/issues/new) or
feel free to reach us on [Scaleway Slack community](https://slack.scaleway.com/),
we are waiting for you on [#serverless-functions](https://scaleway-community.slack.com/app_redirect?channel=serverless-functions).
