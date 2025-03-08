from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python,
    aws_iam as iam,
    Duration,
)
from constructs import Construct
import os


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
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("lambda-functions/plain-lambda", 
                bundling=lambda_.BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_8.bundling_image,
                    command=[
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ]
                )
            ),
            timeout=Duration.seconds(30),
            memory_size=128,
            role=lambda_role,
            description="A simple Lambda function with bundled dependencies",
        )

        # 2. Docker Image Lambda Function
        docker_lambda = lambda_.DockerImageFunction(
            self, "DockerLambdaFunction",
            function_name="docker-lambda-function",
            code=lambda_.DockerImageCode.from_image_asset("lambda-functions/docker-lambda"),
            timeout=Duration.seconds(30),
            memory_size=128,
            role=lambda_role,
            description="A Lambda function packaged as a Docker image",
        )

        # 3. Lambda Function with Layers
        # First, create a layer for dependencies
        dependencies_layer = lambda_.LayerVersion(
            self, "DependenciesLayer",
            code=lambda_.Code.from_asset("lambda-functions/layer-lambda/layers/dependencies", 
                bundling=lambda_.BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_8.bundling_image,
                    command=[
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output/python && cp -au . /asset-output"
                    ]
                )
            ),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_8],
            description="Layer containing external dependencies",
        )

        # Then create the Lambda function with the layer
        layer_lambda = lambda_.Function(
            self, "LayerLambdaFunction",
            function_name="layer-lambda-function",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("lambda-functions/layer-lambda/src"),
            timeout=Duration.seconds(30),
            memory_size=128,
            role=lambda_role,
            layers=[dependencies_layer],
            description="A Lambda function using Lambda layers for dependencies",
        ) 