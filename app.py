#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from smoothie_stack import SmoothieStack

app = cdk.App()
stage = os.getenv("SMOOTHIE_STAGE")
if not stage:
    stage = "dev"

smoothie_stack = SmoothieStack(app, f"SmoothieStack{stage.capitalize()}",
    stage=stage,
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)
app.synth()
