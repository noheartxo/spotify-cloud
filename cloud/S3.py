import boto3
import botocore.exceptions
import tempfile
import json
import logging

logging = logging.getLogger().setLevel(logging.INFO)

class S3: 
    def __init__(self, region: str) -> None:
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)

    def list_buckets(self):
        logging.info("Listing all S3 buckets for given user")
        buckets = self.s3_client.list_buckets()
        print('Existing Buckets:')
        for idx, bucket in enumerate(buckets['Buckets']):
            print(f'  {idx+1} - {bucket["Name"]}')

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
        except botocore.exceptions.ClientError as e:
            logging.error(e)
        except botocore.exceptions.NoRegionError or botocore.exceptions.InvalidRegionError as e:
            logging.error(e)
        
    def delete_bucket(self, bucket_name: str) -> None:
        logging.info("Deleted bucket from user account")
        self.s3_client.delete_bucket(Bucket=bucket_name)

    def upload_to_bucket(self, bucket_name: str, key: str, content: dict) -> None:
        try:
            with tempfile.NamedTemporaryFile(suffix='.json') as temp_file:
                result = json.dumps(content)
                temp_file.write(result.encode('utf-8'))
                temp_file.seek(0)
                
                self.s3_client.upload_fileobj(temp_file, bucket_name, Key=key)
                logging.info(f"Uploaded new file to S3 bucket -- {bucket_name} with name -- {key}")
        except botocore.exceptions.ClientError as e:
            logging.error(e)

    def delete_file_from_bucket(self, bucket_name: str, key: str) -> None:
        self.s3_client.delete_object(Bucket=bucket_name, Key=key)
        logging.info(f"Deleted {key} from {bucket_name}")

    def get_item_from_bucket(self, bucket_name: str, key: str, filename: str) -> None:
        self.s3_client.download_file(Bucket=bucket_name, Key=key, Filename=filename)
        logging.info(f"Downloaded {key} from bucket with; can be found with filename: {filename}")

    def get_object_from_bucket(self, bucket_name: str, filename: str) -> dict:
        with tempfile.TemporaryFile() as data:
            self.s3_client.download_fileobj(bucket_name, filename, data)
            data.seek(0)
            response = json.loads(data.read())
        logging.info("Downloaded file to a temporary file and stored response")
        return response
    