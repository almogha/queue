# QueueShield

**QueueShield** is a Python script designed to scan all SQS queues in all AWS regions of an AWS account and ensure that access policies are restricted to the current account only. If any queue policy allows external principals to perform SQS actions, the script logs the queue information, updates the policy to allow only the specified AWS account, and uploads the log file to an S3 bucket for audit purposes.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Setup](#setup)
- [Usage](#usage)
- [Docker Setup](#docker-setup)
- [Logging](#logging)

## Features
- **Multi-Region**: Automatically scans all AWS regions for SQS queues.
- **Policy Check & Update**: Identifies and updates SQS queue policies that allow external access, restricting them to the current AWS account.
- **Log Mode**: Run the script in "log" mode to only log findings without making any policy updates.
- **Logging and Auditing**: Logs identified queues with external access permissions and uploads the log to an S3 bucket for easy auditing.
- **Environment Configurable**: Uses environment variables for configuration, making it secure and CI/CD-friendly.

## Requirements
- **Python 3.7+**
- **AWS CLI Credentials**: Configured locally or in your environment with permissions to:
  - Listing and describing AWS regions.
  - Listing SQS queues and modifying SQS policies.
  - Uploading the log.txt file to the specified S3 bucket.

## Configuration
Ensure that:
- **AWS Credentials** are configured either through environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) or through an [AWS CLI profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
- **Environment Variables** `S3_BUCKET_NAME`, `AWS_ACCOUNT_ID`(optional), and `MODE`(optional) are set as shown in the [Setup](#setup) section.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Hakakalmog/QueueShield.git
   cd QueueShield
   ```

2. **Set Environment Variables**:
   This project requires two environment variables for configuration:
   - `S3_BUCKET_NAME`: The S3 bucket name where `log.txt` will be uploaded.
   - `AWS_ACCOUNT_ID`(optional): Your AWS account ID to restrict SQS policies.
   - `MODE`(optional): Set to `log` to run in log-only mode (no policy changes), or `update` to both log findings and update policies.


   Example (Unix-based systems):
   ```bash
   export S3_BUCKET_NAME=your-s3-bucket-name
   export AWS_ACCOUNT_ID=your-account-id
   export MODE=log  # or MODE=update for policy updates
   ```

   Example (Windows):
   ```cmd
   set S3_BUCKET_NAME=your-s3-bucket-name
   set AWS_ACCOUNT_ID=your-account-id
   set MODE=log  # or MODE=update for policy updates
   ```

3. **Install Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Modes of Operation

- **Log Mode (`MODE=log`)**: Only logs SQS queues with external access permissions, without making any changes to their policies. This is useful for auditing purposes without modifying any resources.
- **Update Mode (`MODE=update`)(default)**: Logs and updates SQS policies to restrict external access. In this mode, QueueShield will detect queues with external access permissions, log them, and update the policy to allow access only from your AWS account.

## Usage
Run the script using:

```bash
python -m QueueShield.main
```

### Example Output

The `log.txt` file will contain entries similar to:

```
2023-10-30 12:34:56 - External access found for SQS queue: https://sqs.us-west-2.amazonaws.com/123456789012/MyQueue
```

## Docker Setup

To build and run QueueShield as a Docker container, follow these steps:

1. **Build the Docker Image**:
   In the root directory of the project, build the Docker image using:
   ```bash
   docker build -t queueshield:latest .
   ```

2. **Run the Docker Container**:
   Run the Docker container with the required environment variables:
   ```bash
   docker run -e AWS_ACCESS_KEY_ID=your-access-key-id \
              -e AWS_SECRET_ACCESS_KEY=your-secret-access-key \
              -e S3_BUCKET_NAME=your-s3-bucket-name \
              -e AWS_ACCOUNT_ID=your-account-id \
              -e MODE=log \ # (Optional)
              queueshield:latest
   ```

   Replace `your-access-key-id`, `your-secret-access-key`, `your-s3-bucket-name`, `your-account-id`, and `MODE` with the appropriate values.

## Logging

- **Log File**: The script creates a `log.txt` file in the project directory, recording all queues with detected external access permissions.
- **Log Upload**: After processing, `log.txt` is automatically uploaded to the configured S3 bucket (`S3_BUCKET_NAME`).
- **Log Format**: Each log entry includes the timestamp, region, and URL of the SQS queue with external access permissions.
