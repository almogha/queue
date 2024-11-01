import boto3
import json
import logging
from botocore.exceptions import ClientError
from .config import AWS_ACCOUNT_ID, MODE

def get_queue_policy(sqs_client, queue_url):
    """Fetches the SQS policy for the specified queue."""
    try:
        attributes = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['Policy'])
        return json.loads(attributes['Attributes'].get('Policy', '{}'))
    except ClientError as e:
        logging.error(f"Error retrieving policy for {queue_url}: {e}")
        return {}

def find_external_access(statements):
    """Identifies external access in policy statements."""
    found_external_access = False
    for statement in statements:
        principal = statement.get("Principal", {})
        print(principal)
        # action = statement.get("Action", [])
        
        if "*" in principal or principal.get("AWS") != AWS_ACCOUNT_ID:
            # if any(act in action for act in ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:*"]):
            logging.info(f"External access found in statement: {statement}")
            statement["Principal"] = {"AWS": AWS_ACCOUNT_ID}
            found_external_access = True
    return found_external_access

def update_policy(sqs_client, queue_url, policy):
    """Updates the SQS policy if external access was found and MODE is 'update'."""
    try:
        sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={'Policy': json.dumps(policy)}
        )
        logging.info(f"Policy updated for queue: {queue_url}")
    except ClientError as e:
        logging.error(f"Error updating policy for {queue_url}: {e}")

def check_and_update_sqs_policy(sqs_client, queue_url):
    """Checks SQS policy and updates if external access is found and in update mode."""
    policy = get_queue_policy(sqs_client, queue_url)
    if not policy:
        logging.info(f"No policy found for SQS queue: {queue_url}")
        return

    statements = policy.get("Statement", [])
    found_external_access = find_external_access(statements)

    if found_external_access:
        logging.info(f"External access found for queue: {queue_url}")
        if MODE == 'update':
            update_policy(sqs_client, queue_url, policy)
    else:
        logging.info(f"No external access found for queue: {queue_url}")

def get_all_regions():
    """Fetches all AWS regions."""
    ec2 = boto3.client('ec2')
    return [region['RegionName'] for region in ec2.describe_regions()['Regions']]

def process_queues_in_all_regions():
    """Processes all SQS queues in all AWS regions."""
    regions = get_all_regions()
    for region in regions:
        sqs_client = boto3.client('sqs', region_name=region)
        try:
            queues = sqs_client.list_queues().get('QueueUrls', [])
            for queue_url in queues:
                check_and_update_sqs_policy(sqs_client, queue_url)
        except ClientError as e:
            logging.error(f"Error listing queues in region {region}: {e}")
