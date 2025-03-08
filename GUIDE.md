# AWS Lambda Learning Project: Step-by-Step Guide

This guide will walk you through the process of creating, packaging, deploying, and testing three different types of AWS Lambda functions.

## Project Structure Overview

```
finally-learn-lambda/
├── README.md                # Project overview
├── GUIDE.md                 # This step-by-step guide
├── cdk-app/                 # CDK application
├── lambda-functions/        # Lambda implementations
├── events/                  # Test events
└── template.yaml           # SAM template
```

## Prerequisites

- AWS CLI installed and configured
- AWS CDK CLI installed
- Python 3.8+ installed
- Docker installed (for Docker-based Lambda and local testing)
- AWS SAM CLI installed

## Step 1: Setting Up the Project

```bash
# Create project structure
mkdir -p cdk-app lambda-functions/plain-lambda lambda-functions/docker-lambda lambda-functions/layer-lambda/src lambda-functions/layer-lambda/layers/dependencies

# Initialize Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install CDK dependencies
cd cdk-app
pip install -r requirements.txt
cd ..
```

## Step 2: Understanding the Lambda Function Types

### Type 1: Plain Lambda Function

This is a simple Lambda function where all dependencies are packaged with the function code in a single zip file.

**Key Files:**
- `lambda-functions/plain-lambda/lambda_function.py`: Main function code
- `lambda-functions/plain-lambda/requirements.txt`: Function dependencies

**Key Points:**
- CDK's bundling feature automatically packages dependencies with the function code
- No need to create a separate deployment package manually
- Simple to set up but can lead to large deployment packages

### Type 2: Docker Image Lambda Function

This Lambda function is packaged as a Docker container, which provides full control over the runtime environment.

**Key Files:**
- `lambda-functions/docker-lambda/lambda_function.py`: Main function code
- `lambda-functions/docker-lambda/Dockerfile`: Docker image configuration
- `lambda-functions/docker-lambda/requirements.txt`: Function dependencies

**Key Points:**
- Provides complete control over the runtime environment
- Can include custom binaries, libraries, or system dependencies
- Unlimited deployment package size (compared to the 250MB limit for zip packages)
- Slower cold starts compared to zip-based Lambda functions

### Type 3: Lambda Function with Layers

This Lambda function separates application code from dependencies using Lambda layers. It also demonstrates how to handle Python package imports correctly.

**Key Files:**
- `lambda-functions/layer-lambda/src/lambda_function.py`: Main function code
- `lambda-functions/layer-lambda/src/utils/helper.py`: Helper module demonstrating local imports
- `lambda-functions/layer-lambda/layers/dependencies/requirements.txt`: Dependencies for the Lambda layer

**Key Points:**
- Separates application code from dependencies
- Allows sharing common dependencies across multiple functions
- Reduces deployment package size for each function
- Python packages must be installed in the `python/` directory within the layer

## Step 3: Local Testing with AWS SAM

AWS SAM (Serverless Application Model) allows you to test Lambda functions locally before deploying them to AWS.

### Testing Plain Lambda Function

```bash
# Install dependencies for local testing
cd lambda-functions/plain-lambda
pip install -r requirements.txt
cd ../..

# Invoke function locally
sam local invoke PlainLambdaFunction -e events/event.json
```

### Testing Docker Lambda Function

```bash
# Build the Docker image locally
cd lambda-functions/docker-lambda
docker build -t lambda-docker .
cd ../..

# Invoke function locally
sam local invoke DockerLambdaFunction -e events/event.json
```

### Testing Lambda Function with Layers

```bash
# Prepare the dependencies layer
mkdir -p lambda-functions/layer-lambda/layers/dependencies/python
pip install -r lambda-functions/layer-lambda/layers/dependencies/requirements.txt -t lambda-functions/layer-lambda/layers/dependencies/python

# Invoke function locally
sam local invoke LayerLambdaFunction -e events/event.json
```

### Starting a Local API

```bash
# Start local API for all functions
sam local start-api
```

Then you can access:
- Plain Lambda: http://localhost:3000/plain
- Docker Lambda: http://localhost:3000/docker
- Layer Lambda: http://localhost:3000/layer

## Step 4: Deploying with CDK

```bash
# Bootstrap CDK (first-time only)
cd cdk-app
cdk bootstrap

# Deploy the stack
cdk deploy
```

## Step 5: Packaging a Plain Lambda Function Manually

For the plain Lambda function, if you want to package it manually instead of using CDK bundling:

```bash
# Create a deployment package
cd lambda-functions/plain-lambda
pip install -r requirements.txt -t ./package
cp lambda_function.py ./package/
cd package
zip -r ../function.zip .
cd ..

# Now function.zip can be deployed manually via AWS CLI or Console
```

## Troubleshooting Common Issues

### Python Import Issues in Lambda Functions with Layers

The most common issue with Lambda layers in Python is incorrect import paths. Here's how to solve it:

1. **Ensure proper directory structure**: Dependencies in Lambda layers must be in a `python` directory:
   ```
   dependencies/
   └── python/
       └── [packages]
   ```

2. **Check for path conflicts**: If your Lambda function and layer have modules with the same name, conflicts can occur.

3. **Use relative imports correctly**: In Python, package imports can be tricky. Use relative imports for local modules:
   ```python
   from .utils import helper  # Use relative import
   ```

### Docker-based Lambda Issues

1. **Permissions**: Ensure your Dockerfile sets the correct permissions.
2. **Size limits**: While Docker-based Lambdas don't have the 250MB limit, they do have a 10GB limit.
3. **Base image**: Using the AWS-provided base images ensures compatibility.

### Plain Lambda with Dependencies

1. **Package size**: The deployment package must be under 250MB unzipped.
2. **Binary dependencies**: Some packages with compiled components may need to be built for the Lambda environment.
3. **Path issues**: Always package from within the directory to maintain correct paths.

## Conclusion

This guide has walked you through creating three different types of AWS Lambda functions. Each approach has pros and cons:

- **Plain Lambda**: Simple but potentially large packages
- **Docker Lambda**: Maximum flexibility but slower cold starts
- **Lambda with Layers**: Better organization and reuse of dependencies

Choose the approach that best fits your specific requirements and constraints. 