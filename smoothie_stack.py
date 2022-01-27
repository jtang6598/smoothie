from aws_cdk import core as cdk
from api.infrastructure import SmoothieApi
from database.infrastructure import GroupsTable
from website.infrastructure import Website

class SmoothieStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, stage: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        database = GroupsTable(self, "SmoothieGroupsTable")
        api = SmoothieApi(self, "SmoothieApi", dynamodb_table=database.table)
        if stage == "prod":
            cdk_environment = kwargs["env"]
            account_id = cdk_environment.account
            region = cdk_environment.region
            website = Website(self, "SmoothieWebsite", region=region, account_id=account_id)
