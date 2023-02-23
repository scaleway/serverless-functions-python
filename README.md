# Serverless Functions Python 💜

Scaleway Serverless Functions is a framework to provide a good developer experience to write Serverless Functions.

Serverless Functions make it easy to deploy, scale, and optimize your workloads on the cloud.

Get started with Scaleway Functions (we support multiple languages :rocket:):

- [Scaleway Serverless Functions Documentation](https://www.scaleway.com/en/docs/serverless/functions/quickstart/)
- [Scaleway Serverless Framework plugin](https://github.com/scaleway/serverless-scaleway-functions)
- [Scaleway Serverless Examples](https://github.com/scaleway/serverless-examples)
- [Scaleway Cloud Provider](https://scaleway.com)

Testing frameworks for Scaleway Serverless Functions in other languages can be found here:

- [Node](https://github.com/scaleway/serverless-functions-node)
- [Go](https://github.com/scaleway/serverless-functions-go)
- [PHP](https://github.com/scaleway/serverless-functions-php)
- [Rust](https://github.com/scaleway/serverless-functions-rust)

## 🚀 Features

This repository aims to provide the best experience: **local testing, utils, documentation etc...**
additionally we love to share things with the community and we want to expose receipts to the public. That's why we make our framework publicly available to help the community!

## 🏡 Local testing

What this package does:

- **Format Input**: FaaS have a specific input format encapsulating the body received by functions to add some useful data.
  The local testing package lets you interact with this data.
- **Advanced debugging**: To improve developer experience you can run your handler locally, on your computer to make
  it simpler to debug by running your code step-by-step or reading output directly before deploying it.

What this package does not:

- **Build functions**: When your function is uploaded we build it in an environment that can be different than yours. Our build pipelines support
  tons of different packages but sometimes it requires a specific setup, for example, if your function requires a specific 3D system library.
If you have compatibility issues, please see the help section.

## 🛟 Help & support

- Scaleway support is available on Scaleway Console.
- Additionally, you can join our [Slack Community](https://www.scaleway.com/en/docs/tutorials/scaleway-slack-community/)

## 🎓 Contributing

We welcome all contributions to our open-source projects, please see our contributing guidelines <link>.

Do not hesitate to raise issues and pull requests we will have a look at them.

## Usage

```python
from serverless_functions_python import serve_handler_locally

def handler(event, context):
    return "Hello World!"

if __name__ == "__main__":
    serve_handler_locally(handler)
```

This file will expose your handler on a local web server allowing you to test your function.

Some information will be added to requests for example specific headers. For local development, additional header values are hardcoded
to make it easy to differentiate them. In production, you will be able to observe headers with exploitable data.

Local testing part of this framework does not aim to simulate 100% production but it aims to make it easier to work with functions locally.

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

## 🏛️ Architecture