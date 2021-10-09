#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from smoothie.smoothie_stack import SmoothieStack

app = cdk.App()
stage = "prod" if os.getenv("IS_SMOOTHIE_PROD") else "dev"
smoothie_stack = SmoothieStack(app, f"SmoothieStack{stage.capitalize()}",
    stage=stage,
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)
app.synth()
