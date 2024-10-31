import os
import boto3


# Retrieve S3_BUCKET_NAME from the environment
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

# Retrieve AWS_ACCOUNT_ID from boto3 STS call or fallback to environment
AWS_ACCOUNT_ID = boto3.client("sts").get_caller_identity().get("Account") or os.environ.get("AWS_ACCOUNT_ID")

# Load the mode (log or update) from an environment variable, defaulting to 'update'
MODE = os.environ.get('MODE', 'update').lower()


if not S3_BUCKET_NAME or not AWS_ACCOUNT_ID:
    raise EnvironmentError("S3_BUCKET_NAME and AWS_ACCOUNT_ID must be set in the environment")
