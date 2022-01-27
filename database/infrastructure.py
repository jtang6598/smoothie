from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk
from python_settings import settings

class GroupsTable(cdk.Construct):
	def __init__(self, scope: cdk.Construct, id_: str) -> None:
		super().__init__(scope, id_)
		
		# TODO: Update read and write capacity with better estimates
        # Create DDB table
		self.table = dynamodb.Table(self, "SmoothieGroupsTable",
            table_name=settings.GROUPS_TABLE,
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="access_token", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            read_capacity=5,
            write_capacity=5
        )
