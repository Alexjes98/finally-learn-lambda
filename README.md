# AWS Lambda Learning Project

This project demonstrates how to create, deploy, and test AWS Lambda functions using different deployment methods:

1. **Plain Lambda Function**: A simple Lambda function with external dependencies packaged in a zip file
2. **Docker Image Lambda Function**: A Lambda function packaged as a Docker container
3. **Lambda Function with Layers**: A Lambda function that uses Lambda layers for dependencies and demonstrates proper package importing

## Project Structure

```
finally-learn-lambda/
├── README.md                # This file
├── cdk-app/                 # AWS CDK application for deployment
│   ├── app.py               # CDK application entry point
│   ├── cdk_stack.py         # CDK stack definition
│   └── requirements.txt     # CDK dependencies
├── lambda-functions/        # Lambda function implementations
│   ├── plain-lambda/        # Simple Lambda implementation
│   │   ├── lambda_function.py # Function code
│   │   └── requirements.txt # Dependencies
│   ├── docker-lambda/       # Docker-based Lambda
│   │   ├── Dockerfile       # Docker configuration
│   │   ├── lambda_function.py # Function code
│   │   └── requirements.txt # Dependencies
│   └── layer-lambda/        # Lambda with layers
│       ├── src/             # Lambda function code
│       │   ├── lambda_function.py # Main function
│       │   └── utils/       # Local imports example
│       │       └── helper.py # Helper module
│       └── layers/          # Lambda layers
│           └── dependencies/ # Dependencies layer
└── template.yaml           # AWS SAM template for local testing
```

## Prerequisites

- AWS CLI installed and configured
- AWS CDK CLI installed (`npm install -g aws-cdk`)
- Python 3.8+ installed
- Docker installed (for Docker-based Lambda and SAM local testing)
- AWS SAM CLI installed

## Setup Instructions

1. Set up a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install CDK dependencies:
```bash
cd cdk-app
pip install -r requirements.txt
```

3. Bootstrap CDK (if you haven't already):
```bash
cdk bootstrap
```

## Deployment

To deploy all Lambda functions:
```bash
cd cdk-app
cdk deploy
```

## Local Testing

To test the Lambda functions locally:
```bash
sam local invoke PlainLambdaFunction -e events/event.json
sam local invoke DockerLambdaFunction -e events/event.json
sam local invoke LayerLambdaFunction -e events/event.json
```

## Step-by-Step Guide

See the detailed sections below for explanations on each Lambda function type. 