import aws_cdk as cdk
from aws_cdk.assertions import Match, Template

from infra.stack import StartupStack


def test_stack_has_the_demo_pieces():
    t = Template.from_stack(StartupStack(cdk.App(), "T"))
    t.has_resource_properties("AWS::DynamoDB::GlobalTable", {"BillingMode": "PAY_PER_REQUEST"})
    t.has_resource_properties("AWS::Lambda::Function", {"Runtime": "python3.14", "Architectures": ["arm64"]})
    t.has_resource_properties("AWS::S3::Bucket", {"LifecycleConfiguration": {"Rules": [Match.object_like(
        {"Prefix": "facturas/", "Transitions": [{"StorageClass": "GLACIER", "TransitionInDays": 90}]})]}})
    notif = t.find_resources("Custom::S3BucketNotifications")
    prefixes = {r["Filter"]["Key"]["FilterRules"][0]["Value"] for n in notif.values()
                for r in n["Properties"]["NotificationConfiguration"]["LambdaFunctionConfigurations"]}
    assert prefixes == {"productos/", "facturas/", "resenas/"}


def test_public_demo_is_throttled_and_capped():
    t = Template.from_stack(StartupStack(cdk.App(), "T"))
    t.has_resource_properties("AWS::Lambda::Function", {"Handler": "web.handler", "ReservedConcurrentExecutions": 5})
    t.has_resource_properties("AWS::ApiGatewayV2::Stage", {"StageName": "$default",
        "DefaultRouteSettings": {"ThrottlingRateLimit": 20, "ThrottlingBurstLimit": 50},
        "RouteSettings": {"POST /analizar": {"ThrottlingRateLimit": 1.6, "ThrottlingBurstLimit": 5}}})
    t.has_resource_properties("AWS::ApiGatewayV2::Api", {"DisableExecuteApiEndpoint": True})
    t.has_resource_properties("AWS::IAM::Policy", {"PolicyDocument": {"Statement": Match.array_with([Match.object_like({
        "Action": ["dynamodb:UpdateItem", "dynamodb:PutItem"],
        "Condition": {"ForAllValues:StringLike": {"dynamodb:LeadingKeys": ["_cupo", "web/*"]}}})])}})
    t.has_resource_properties("AWS::ApiGatewayV2::DomainName", {"DomainName": "demo.builtbyandres.com"})
    t.resource_count_is("AWS::ApiGatewayV2::Route", 3)
