#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_stack import LambdaLearningStack

app = cdk.App()
LambdaLearningStack(app, "LambdaLearningStack")

app.synth() 