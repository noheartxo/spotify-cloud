import boto3
import botocore.exceptions
import tempfile
import logging

class S3: 
    def __init__(self, region: str) -> None:
        self.region = region
        try:
            self.s3_client = boto3.client('s3', region_name=region)
            logging.info("Created boto s3 client")
        except botocore.exceptions.BotoCoreError as boto_error:
            logging.error(boto_error)

    def list_buckets(self) -> None:
        logging.info("Listing all S3 buckets for given user")
        try:
            buckets = self.s3_client.list_buckets()
            print('Existing Buckets:')
            for idx, bucket in enumerate(buckets['Buckets']):
                print(f'  {idx+1} - {bucket["Name"]}')
        except botocore.exceptions.BotoCoreError as boto_error:
            logging.error(boto_error)

    def create_bucket(self, bucket_name: str) -> None:
        location = {
            'LocationConstraint': self.region
        }

        PublicAccessConfig = {
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
        try:
            self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            self.s3_client.put_public_access_block(
                Bucket=bucket_name, 
                PublicAccessBlockConfiguration=PublicAccessConfig
            )
            logging.info(f"Created {bucket_name} S3 bucket with blocked public access")
        except botocore.exceptions.ClientError as boto_error:
            logging.error(boto_error)
        except botocore.exceptions.NoRegionError or botocore.exceptions.InvalidRegionError as boto_error:
            logging.error(boto_error)
        
    def delete_bucket(self, bucket_name: str) -> None:
        try: 
            self.s3_client.delete_bucket(Bucket=bucket_name)
            logging.info("Deleted bucket from user account")
        except botocore.exceptions.BotoCoreError as boto_error:
            logging.error(boto_error)

    def upload_object_to_bucket(self, bucket_name: str, key: str, content: any) -> None:
        try:
            with tempfile.NamedTemporaryFile() as temp_file:
                result = str(content)
                temp_file.write(result.encode('utf-8'))
                temp_file.seek(0)
                self.s3_client.upload_fileobj(temp_file, bucket_name, Key=key)
                logging.info(f"Uploaded new file to S3 bucket -- {bucket_name} with name -- {key}")
        except botocore.exceptions.BotoCoreError as boto_error:
            logging.error(boto_error)

    def delete_file_from_bucket(self, bucket_name: str, key: str) -> None:
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=key)
            logging.info(f"Deleted {key} from {bucket_name}")
        except botocore.exceptions.BotoCoreError as boto_error:
            logging.error(boto_error)

    def get_item_from_bucket(self, bucket_name: str, key: str, filename: str) -> None:
        try:
            self.s3_client.download_file(Bucket=bucket_name, Key=key, Filename=filename)
            logging.info(f"Downloaded {key} from bucket with; can be found with filename: {filename}")
        except botocore.exceptions.BotoCoreError as boto_error:
            logging.error(boto_error)

    def get_object_from_bucket(self, bucket_name: str, filename: str) -> str:
        try:
            with tempfile.TemporaryFile() as temp_file:
                self.s3_client.download_fileobj(bucket_name, filename, temp_file)
                temp_file.seek(0)
                response = temp_file.read()
            logging.info("Downloaded file to a temporary file and stored response")
            return response
        except botocore.exceptions.BotoCoreError as boto_error:
            logging.error(boto_error)