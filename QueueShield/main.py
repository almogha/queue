import logging
from QueueShield.sqs_policy_manager import process_queues_in_all_regions
from QueueShield.s3_uploader import upload_log_to_s3

logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    process_queues_in_all_regions()
    upload_log_to_s3()

if __name__ == '__main__':
    main()
