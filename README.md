# Scaleway Functions Python 💜

A framework that provides tools when working with Scaleway Serverless Functions in Python.

## Installation

You can use `pip` to install the framework:

```console
pip install scaleway-functions-python
```

## Usage

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

## 🛟 Help & support

- Scaleway support is available on Scaleway Console.
- Additionally, you can join our [Slack Community](https://www.scaleway.com/en/docs/tutorials/scaleway-slack-community/)

## ❓ FAQ

**Why do I need an additional package to call my function?**

Your Function Handler can be served by a simple HTTP server but Serverless Ecosystem involves a lot of different layers
and this package aims to simulate everything your request will go through.

**How my function will be deployed**

Your function will be deployed in an environment that allows your function to easily Scale up and down and it's wrapped into
different pieces of software with different roles. This stack also changes the headers, input and output of your function, that's why
this tool has been developed to simulate this part.

**Do I need to deploy my function differently?**

No. This framework does not affect deployment or performance.

## 🎓 Contributing

We welcome all contributions to our open-source projects, please see our contributing guidelines.

Do not hesitate to raise issues and pull requests we will have a look at them.
