from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class LambdaLearningStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM role for our Lambda functions
        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        # 1. Plain Lambda Function (with dependencies packaged together)
        plain_lambda = lambda_.Function(
            self, "PlainLambdaFunction",
            function_name="plain-lambda-function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("../lambda-functions/plain-lambda", 
                bundling={
                    "image": lambda_.Runtime.PYTHON_3_10.bundling_image,
                    "command": [
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output && find /asset-output -type f -name '*.py' -exec chmod 644 {} +"
                    ]
                }
            ),
            timeout=Duration.seconds(30),
            memory_size=256,  # Increased memory for better performance
            role=lambda_role,
            environment={
                "POWERTOOLS_SERVICE_NAME": "plain-lambda",
                "POWERTOOLS_METRICS_NAMESPACE": "PlainLambda",
                "LOG_LEVEL": "INFO"
            },
            description="A Lambda function with pure Python dependencies demonstrating various features",
        )

        # 2. Docker Image Lambda Function
        docker_lambda = lambda_.DockerImageFunction(
            self, "DockerLambdaFunction",
            function_name="docker-lambda-function",
            code=lambda_.DockerImageCode.from_image_asset("../lambda-functions/docker-lambda"),
            timeout=Duration.seconds(30),
            memory_size=128,
            role=lambda_role,
            description="A Lambda function packaged as a Docker image",
        )

        # 3. Lambda Function with Layers
        # First, create a layer for dependencies
        dependencies_layer = lambda_.LayerVersion(
            self, "DependenciesLayer",
            code=lambda_.Code.from_asset("../lambda-functions/layer-lambda/layers/dependencies", 
                bundling={
                    "image": lambda_.Runtime.PYTHON_3_10.bundling_image,
                    "command": [
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output/python && cp -au . /asset-output"
                    ]
                }
            ),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description="Layer containing external dependencies",
        )

        # Then create the Lambda function with the layer
        layer_lambda = lambda_.Function(
            self, "LayerLambdaFunction",
            function_name="layer-lambda-function",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("../lambda-functions/layer-lambda/src"),
            timeout=Duration.seconds(30),
            memory_size=128,
            role=lambda_role,
            layers=[dependencies_layer],
            description="A Lambda function using Lambda layers for dependencies",
        ) 