from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_notifications as _s3_notifications,
)
from constructs import Construct

class PyDocxtopdfStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the source S3 bucket
        source_bucket = _s3.Bucket(self, "docx-source")

        # Create the destination S3 bucket
        destination_bucket = _s3.Bucket(self, "pdf-dest")

        # Existing layer ARN
        libreoffice_layer_arn = "arn:aws:lambda:ap-south-1:764866452798:layer:libreoffice-brotli:1"
        brotlipy_layer_arn = "arn:aws:lambda:ap-south-1:<<ACCOUNT ID>>:layer:brotlipy-layer:1"


        # Create the Lambda function
        lambda_function = _lambda.Function(
            self, "DocxToPdfConverter",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambda_function"),
            handler="index.lambda_handler",
            environment={
                "DESTINATION_BUCKET": destination_bucket.bucket_name
            },
            timeout=Duration.seconds(300),
            memory_size=512,
            layers=[
                _lambda.LayerVersion.from_layer_version_arn(self, "libreoffice-brotli", libreoffice_layer_arn),
                _lambda.LayerVersion.from_layer_version_arn(self, "brotlipy-layer", brotlipy_layer_arn)
            ]
        )

        # Grant the Lambda function permission to access the source and destination buckets
        source_bucket.grant_read(lambda_function)
        destination_bucket.grant_write(lambda_function)

        # Create an S3 notification to trigger the Lambda function when a file is uploaded to the source bucket
        notification = _s3_notifications.LambdaDestination(lambda_function)
        source_bucket.add_event_notification(_s3.EventType.OBJECT_CREATED, notification)
        