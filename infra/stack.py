from pathlib import Path

from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from aws_cdk import aws_apigatewayv2 as apigw
from aws_cdk import aws_apigatewayv2_integrations as integrations
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_logs as logs
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_notifications as s3n
from constructs import Construct

LAMBDA_DIR = str(Path(__file__).resolve().parent.parent / "lambda")
DOMINIO = "demo.builtbyandres.com"
AI_ACTIONS = ["rekognition:DetectLabels", "textract:AnalyzeExpense", "comprehend:DetectSentiment"]


class StartupStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Memory: one bucket, one folder per "sense". Old receipts go cold (Stage 1: Glacier).
        bucket = s3.Bucket(
            self, "Archivos",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            lifecycle_rules=[s3.LifecycleRule(
                prefix="facturas/",
                transitions=[s3.Transition(
                    storage_class=s3.StorageClass.GLACIER, transition_after=Duration.days(90)
                )],
            )],
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Memory: on-demand table, pays per request (Stage 3: the viral peak).
        table = dynamodb.TableV2(
            self, "Resultados",
            partition_key=dynamodb.Attribute(name="archivo", type=dynamodb.AttributeType.STRING),
            billing=dynamodb.Billing.on_demand(),
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Brain: one function, routed by folder.
        fn = lambda_.Function(
            self, "Sentidos",
            runtime=lambda_.Runtime.PYTHON_3_14,
            architecture=lambda_.Architecture.ARM_64,
            handler="handler.handler",
            code=lambda_.Code.from_asset(LAMBDA_DIR),
            timeout=Duration.seconds(30),
            environment={"TABLE": table.table_name},
            log_group=logs.LogGroup(
                self, "SentidosLogs",
                retention=logs.RetentionDays.ONE_WEEK,
                removal_policy=RemovalPolicy.DESTROY,
            ),
        )
        bucket.grant_read(fn)
        table.grant_write_data(fn)
        # These three actions do not support resource-level permissions.
        fn.add_to_role_policy(iam.PolicyStatement(actions=AI_ACTIONS, resources=["*"]))

        for folder in ("productos/", "facturas/", "resenas/"):
            bucket.add_event_notification(
                s3.EventType.OBJECT_CREATED,
                s3n.LambdaDestination(fn),
                s3.NotificationKeyFilter(prefix=folder),
            )

        # Public demo: same senses behind an HTTP API. No S3 access; visitors' files are never stored.
        publico = lambda_.Function(
            self, "Publico",
            runtime=lambda_.Runtime.PYTHON_3_14,
            architecture=lambda_.Architecture.ARM_64,
            handler="web.handler",
            code=lambda_.Code.from_asset(LAMBDA_DIR),
            timeout=Duration.seconds(15),
            memory_size=256,
            reserved_concurrent_executions=5,
            environment={"TABLE": table.table_name},
            log_group=logs.LogGroup(
                self, "PublicoLogs",
                retention=logs.RetentionDays.ONE_WEEK,
                removal_policy=RemovalPolicy.DESTROY,
            ),
        )
        # Only the quota item and web/* results, nothing else in the table.
        publico.add_to_role_policy(iam.PolicyStatement(
            actions=["dynamodb:UpdateItem", "dynamodb:PutItem"],
            resources=[table.table_arn],
            conditions={"ForAllValues:StringLike": {"dynamodb:LeadingKeys": ["_cupo", "web/*"]}},
        ))
        publico.add_to_role_policy(iam.PolicyStatement(actions=AI_ACTIONS, resources=["*"]))

        # The deploy waits here until the validation CNAME is added in Cloudflare (DNS only).
        cert = acm.Certificate(self, "Certificado", domain_name=DOMINIO,
                               validation=acm.CertificateValidation.from_dns())
        dominio = apigw.DomainName(self, "Dominio", domain_name=DOMINIO, certificate=cert)
        # Only reachable through the custom domain (Cloudflare), not the execute-api URL.
        api = apigw.HttpApi(self, "Api", create_default_stage=False, disable_execute_api_endpoint=True)
        integracion = integrations.HttpLambdaIntegration("Web", publico)
        for ruta, metodo in (("/", apigw.HttpMethod.GET), ("/muestras/{archivo}", apigw.HttpMethod.GET),
                             ("/analizar", apigw.HttpMethod.POST)):
            api.add_routes(path=ruta, methods=[metodo], integration=integracion)
        # Page loads are cheap and arrive all at once; analysis gets about 96 requests per minute
        # for everyone together. The DynamoDB quota caps the total.
        etapa = apigw.HttpStage(
            self, "Etapa", http_api=api, stage_name="$default", auto_deploy=True,
            throttle=apigw.ThrottleSettings(rate_limit=20, burst_limit=50),
            domain_mapping=apigw.DomainMappingOptions(domain_name=dominio),
        )
        etapa.node.default_child.route_settings = {
            "POST /analizar": {"ThrottlingRateLimit": 1.6, "ThrottlingBurstLimit": 5},
        }

        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "TableName", value=table.table_name)
        CfnOutput(self, "CloudflareCname", value=dominio.regional_domain_name)
