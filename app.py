import os

import aws_cdk as cdk

from infra.stack import StartupStack

app = cdk.App()
StartupStack(
    app, "DelExcelAlMillon",
    env=cdk.Environment(account=os.environ.get("CDK_DEFAULT_ACCOUNT"), region="us-west-2"),
)
app.synth()
