from aws_cdk import aws_s3 as s3
from aws_cdk import core as cdk

class Website(cdk.Construct):
    def __init__(self, scope: cdk.Construct, id_: str, region: str, account_id: str) -> None:
        super().__init__(scope, id_)
        self.website_bucket_name = f"smoothie-website-{region}-{account_id}"
        blockPublicAccess = s3.BlockPublicAccess(block_public_policy=False)
        self.bucket = s3.Bucket(self, self.website_bucket_name,
            bucket_name=self.website_bucket_name,
            website_index_document="index.html",
            block_public_access=blockPublicAccess,
            public_read_access=True
        )
