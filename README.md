# Serverless Functions Python 💜

Scaleway Serverless Functions Python is a framework which simplify Scaleway [Serverless Functions](https://www.scaleway.com/fr/serverless-functions/) local development. 
It enables you to debug your function locally and provide the event data format used in Scaleway Serverless Functions.

Be careful, this framework does not enable you to build and deploy your function (for more information, refer to the official documentation)

Get started with Scaleway Functions (we support multiple languages :rocket:):

- [Scaleway Serverless Functions Documentation](https://www.scaleway.com/en/docs/serverless/functions/quickstart/)
- [Scaleway Serverless Framework plugin](https://github.com/scaleway/serverless-scaleway-functions)
- [Scaleway Serverless Examples](https://github.com/scaleway/serverless-examples)
- [Scaleway Cloud Provider](https://scaleway.com)

Testing frameworks for Scaleway Serverless Functions in other languages can be found here:
- [Go](https://github.com/scaleway/serverless-functions-go)

## ⚙️ Quick Start

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

This repository aims to provide the best experience: **local testing, utils, documentation etc...**
additionally we love to share things with the community and we want to expose receipts to the public. That's why
we make our framework publicly available to help the community!

### 🏡 Local testing

What this package does:

- **Format Input**: Serverless Functions have a specific input format encapsulating the body received by functions to add some useful data.
  The local testing package lets you interact with the formatted data.
- **Advanced debugging**: To improve developer experience you can run your handler locally and debug it by running your code step-by-step or reading output directly before deploying it.

What this package does not:

- **Simulate performance**: Scaleway FaaS lets you choose different options for CPU/RAM that can have an impact
  on your development. This package does not provide specific limits for your function on local testing but you can
  add [Profile your application](*LINK TO EDIT*) or you can use our metrics available in [Scaleway Console](https://console.scaleway.com/)
  to monitor your application.
- **Deploy functions**: When your function is uploaded we package it in an environment that can be different than yours. Our build pipelines support several dependencies but sometimes it requires specific system dependencies (especially those related to lib c) that we don't support
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

No. This framework does not affect deployment nor performance.


## 🧑‍💻 Development

This repository is at its early stage and is still in active development.
If you are looking for a way to contribute please read [CONTRIBUTING.md](./docs/CONTRIBUTING.md).

## 🛟 Help & support

- Scaleway support is available on Scaleway Console.
- Additionally, you can join our [Slack Community](https://www.scaleway.com/en/docs/tutorials/scaleway-slack-community/)

## 🎓 Contributing

We welcome all contributions to our open-source projects, please see our contributing guidelines <link>.

Do not hesitate to raise issues and pull requests we will have a look at them.

## 📭 Reach Us

We love feedback.
Don't hesitate to open a [Github issue](https://github.com/scaleway/serverless-functions/go/issues/new) or
feel free to reach us on [Scaleway Slack community](https://slack.scaleway.com/),
we are waiting for you on [#serverless-functions](https://scaleway-community.slack.com/app_redirect?channel=serverless-functions).
