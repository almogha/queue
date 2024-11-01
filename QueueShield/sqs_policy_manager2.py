# import boto3
# import json
# import logging
# from botocore.exceptions import ClientError
# from .config import AWS_ACCOUNT_ID, MODE

# def get_all_regions():
#     """Fetches all AWS regions."""
#     ec2 = boto3.client('ec2')
#     return [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# def check_and_update_sqs_policy(sqs_client, queue_url):
#     """Checks SQS policy, logs findings, and updates if in update mode."""
#     try:
#         attributes = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['Policy'])
#         if 'Policy' not in attributes['Attributes']:
#             return  # No policy found for this queue

#         policy = json.loads(attributes['Attributes']['Policy'])
#         statements = policy.get("Statement", [])
#         updated = False

#         for statement in statements:
#             principal = statement.get("Principal", {})
#             action = statement.get("Action", [])

#             if "*" in principal.values() or "AWS" in principal and principal["AWS"] != AWS_ACCOUNT_ID:
#                 if any(act in action for act in ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:*"]):
#                     logging.info(f"External access found for SQS queue: {queue_url}")
#                     statement["Principal"] = {"AWS": AWS_ACCOUNT_ID}
#                     found_external_access = True
#                     if MODE == 'update':
#                         statement["Principal"] = {"AWS": AWS_ACCOUNT_ID}  # Restrict access

#         # If in 'update' mode, apply the policy update if needed
#         if found_external_access and MODE == 'update':
#             sqs_client.set_queue_attributes(
#                 QueueUrl=queue_url,
#                 Attributes={'Policy': json.dumps(policy)}
#             )

#     except ClientError as e:
#         logging.error(f"Error checking/updating policy for {queue_url}: {e}")

# def process_queues_in_all_regions():
#     """Processes all SQS queues in all AWS regions."""
#     regions = get_all_regions()
#     for region in regions:
#         sqs_client = boto3.client('sqs', region_name=region)
#         try:
#             queues = sqs_client.list_queues().get('QueueUrls', [])
#             for queue_url in queues:
#                 check_and_update_sqs_policy(sqs_client, queue_url)
#         except ClientError as e:
#             logging.error(f"Error listing queues in region {region}: {e}")