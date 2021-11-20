from aws_cdk import (core as cdk,
                     aws_apigateway as apigateway,
                     aws_lambda as lambda_,
                     aws_iam as iam,
                     aws_dynamodb as dynamodb,
                     aws_s3 as s3
)

class SmoothieStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, stage: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        cdk_environment = kwargs["env"]
        account_id = cdk_environment.account
        region = cdk_environment.region
        is_prod = stage == "prod"

        # TODO: Update read and write capacity with better estimates
        # Create DDB table
        groups_table = dynamodb.Table(self, f"SmoothieGroupsTable{stage.capitalize()}",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="token", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            read_capacity=5,
            write_capacity=5
        )
        # Create read write policy statement for Groups table
        groupsTableReadWritePolicyStatement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["dynamodb:BatchGetItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
				"dynamodb:Scan",
				"dynamodb:BatchWriteItem",
				"dynamodb:PutItem",
				"dynamodb:UpdateItem"
            ],
            resources=[groups_table.table_arn]
        )

        # Create a generic lambda role for the stack's handlers
        smoothie_lambda_role = iam.Role(self, f"SmoothieLambdaRole{stage.capitalize()}",
            role_name=f"SmoothieLambdaRole{stage.capitalize()}",
            description="Generic lambda role for Smoothie stack handlers",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")]
        )
        smoothie_lambda_role.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        smoothie_lambda_role.add_managed_policy(groupsTableReadWritePolicyStatement)
        
        # TODO: Update memory and timeout limits with better estimates
        # Create all handlers
        create_group_handler = lambda_.Function(self, f"CreateGroup{stage.capitalize()}Handler",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="create_group.main",
            code=lambda_.Code.from_asset("./lambdas"),
            description="Add a new group and member to the Groups table",
            role=smoothie_lambda_role,
            memory_size=128,
            timeout=cdk.Duration.seconds(10)
        )
        join_group_handler = lambda_.Function(self, f"JoinGroup{stage.capitalize()}Handler",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="join_group.main",
            code=lambda_.Code.from_asset("./lambdas"),
            description="Add a new member to a group in the Groups table",
            role=smoothie_lambda_role,
            memory_size=128,
            timeout=cdk.Duration.seconds(10)
        )
        # TODO: Add Spotify token as env variable (retrieve locally through env variable, use Github secrets when deploying to prod)
        create_playlist_handler = lambda_.Function(self, f"CreatePlaylist{stage.capitalize()}Handler",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="create_playlist.main",
            code=lambda_.Code.from_asset("./lambdas"),
            description="Create a group's playlist",
            role=smoothie_lambda_role
        )

        # Create API deployment and CORS options
        stage_options = apigateway.StageOptions(stage_name=stage)
        # TODO: Allowing all origins will suffice for the dev stage, but should be more restrictive for the prod stage, like
        # allow_origins = [smoothie origin] if is_prod else Cors.ALL_ORIGINS
        cors_options = apigateway.CorsOptions(allow_origins=apigateway.Cors.ALL_ORIGINS, allow_methods=["POST"])

        # Create root API
        smoothie_api = apigateway.RestApi(self, f"smoothie-api-{stage}",
            rest_api_name=f"smoothie-api-{stage}",
            deploy_options=stage_options,
            default_cors_preflight_options=cors_options
        )

        # Setup Lambda integrations
        create_group_integration = apigateway.LambdaIntegration(create_group_handler)
        join_group_integration = apigateway.LambdaIntegration(join_group_handler)
        create_playlist_integration = apigateway.LambdaIntegration(create_playlist_handler)

        # /group
        group_resource = smoothie_api.root.add_resource("group")
        # /group/create
        create_group_resource = group_resource.add_resource("create")
        create_group_resource.add_method("POST", create_group_integration)
        # /group/join/{id}
        join_group_resource = group_resource.add_resource("join").add_resource("{id}")
        join_group_resource.add_method("POST", join_group_integration)

        # /playlist
        playlist_resource = smoothie_api.root.add_resource("playlist")
        # /playlist/create/id
        create_playlist_resource = playlist_resource.add_resource("create").add_resource("{id}")
        create_playlist_resource.add_method("POST", create_playlist_integration)

        # Setup API usage plan
        smoothie_api_key = smoothie_api.add_api_key(f"SmoothieApiKey-{stage}", default_cors_preflight_options=cors_options)
        deploymeny_stage_usage_plan = apigateway.UsagePlanPerApiStage(api=smoothie_api, stage=smoothie_api.deployment_stage)
        smoothie_usage_plan = smoothie_api.add_usage_plan("SmoothieUsagePlan",
            name="SmoothieUsagePlan",
            api_stages=[deploymeny_stage_usage_plan],
            throttle={
                "rate_limit": 10,
                "burst_limit": 2
            },
        )
        smoothie_usage_plan.add_api_key(smoothie_api_key)

        # Apply DESTROY removal policies where applicable
        smoothie_api.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        smoothie_usage_plan.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        
        if is_prod:
            block_public_access_settings = s3.BlockPublicAccess(block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False)
            website_bucket_name = f"smoothie-website-{region}-{account_id}"
            smoothie_website_bucket = s3.Bucket(self, website_bucket_name,
                bucket_name=website_bucket_name,
                website_index_document="index.html",
                block_public_access=block_public_access_settings,
                public_read_access=True
            )
