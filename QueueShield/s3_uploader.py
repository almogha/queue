import boto3
import logging
from botocore.exceptions import ClientError
from .config import S3_BUCKET_NAME

def upload_log_to_s3(file_path='log.txt'):
    """Uploads the log file to an S3 bucket."""
    s3 = boto3.client('s3', region_name='eu-west-1')
    try:
        s3.upload_file(file_path, S3_BUCKET_NAME, 'log.txt')
        logging.info("Log file uploaded to S3 successfully.")
    except ClientError as e:
        logging.error(f"Failed to upload log file to S3: {e}")
