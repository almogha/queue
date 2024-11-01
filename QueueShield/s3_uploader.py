import boto3
import logging
from QueueShield.config import S3_BUCKET_NAME, S3_BUCKET_REGION

def upload_log_to_s3(file_path='log.txt'):
    """Uploads the log file to an S3 bucket."""
    s3 = boto3.client('s3', region_name=S3_BUCKET_REGION)
    s3.upload_file(file_path, S3_BUCKET_NAME, 'log.txt')
    logging.info("Log file uploaded to S3 successfully.")
